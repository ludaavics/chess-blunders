import { Chess } from 'chess.js';
import { Chessground } from 'chessground';
import { Api } from 'chessground/api';
import bootstrap from 'bootstrap';
import feather from 'feather-icons';
import {
  giveHandToOtherSide, toDests, toColor, resizeChessground,
} from './utilities';
import './styles/chessground.css';
import './styles/chessground-theme.css';
import './styles/layout.css';
import 'bootstrap/dist/js/bootstrap.bundle.min';
import 'bootstrap/dist/css/bootstrap.min.css';

const INITIAL_POSITION_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR';
const BLUNDERS_BUFFER_SIZE = 5;
const socket = new WebSocket(process.env.API_URL);

/* ---------------------------------------------------------------------------------- */
/*                                      Handlers                                      */
/* ---------------------------------------------------------------------------------- */

/* ---------------------------- Update Buttons and Prompt --------------------------- */
function updateNextBlunderBtn(nextBlunders) {
  const btn = document.getElementById('next-blunder');
  if (nextBlunders.length === 0) {
    btn.classList.add('disabled');
    btn.classList.add('text-muted');
  } else {
    btn.classList.remove('disabled');
    btn.classList.remove('text-muted');
  }
}

function updateMakeCorrectMoveBtn(blunder, chess) {
  const btn = document.getElementById('make-correct-move');
  const ply = chess.history().length - 1;
  if (blunder.solution.length > ply) {
    btn.classList.remove('disabled');
    btn.classList.remove('text-muted');
  } else {
    btn.classList.add('disabled');
    btn.classList.add('text-muted');
  }
}

function spinRequestButton() {
  const btn = document.getElementById('btn-request-blunders');
  btn.classList.add('disabled');
  btn.innerHTML = (
    '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true">'
    + '</span> Generating...'
  );
}

function stopRequestButton() {
  const btn = document.getElementById('btn-request-blunders');
  btn.classList.remove('disabled');
  btn.innerHTML = 'Generate';
}

function updatePrompt(prompt) {
  document.getElementById('prompt').innerHTML = prompt;
}

/* ------------------------------- Update Chess Board ------------------------------- */
function makeMove(cg, chess, from, to, callback) {
  const cgFen = cg.getFen();
  const chessFen = chess.fen();
  const cgHasAlreadyMoved = chessFen.slice(0, cgFen.length) !== cgFen;
  if (!cgHasAlreadyMoved) {
    cg.move(from, to);
  }
  giveHandToOtherSide(cg, chess, callback)(from, to);
}

function makeCorrectMove(cg, chess, blunder) {
  const ply = chess.history().length - 1;
  const solutionMoveFrom = blunder.solution[ply][0];
  const solutionMoveTo = blunder.solution[ply][1];
  makeMove(cg, chess, solutionMoveFrom, solutionMoveTo, null);

  if (blunder.solution.length > ply + 2) {
    const responseMoveFrom = blunder.solution[ply + 1][0];
    const responseMoveTo = blunder.solution[ply + 1][1];

    const afterMove = checkAgainstSolution(cg, chess, blunder);
    makeMove(cg, chess, responseMoveFrom, responseMoveTo, afterMove);
    updatePrompt('Go on...');
  } else {
    updatePrompt('Well done!');
  }
}

function checkAgainstSolution(cg: Api, chess, blunder) {
  return (orig, dest, metadata) => {
    const ply = chess.history().length - 1;
    const solutionMoveFrom = blunder.solution[ply][0];
    const solutionMoveTo = blunder.solution[ply][1];
    const isCorrectMove = (orig === solutionMoveFrom) && (dest === solutionMoveTo);
    if (isCorrectMove) {
      makeCorrectMove(cg, chess, blunder);
    } else {
      setTimeout(() => {
        cg.move(dest, orig);
        if ('captured' in metadata) {
          cg.newPiece(metadata.captured, dest);
        }
        cg.set({
          turnColor: toColor(chess),
          movable: {
            color: toColor(chess),
            dests: toDests(chess),
          },
        });
      }, 350);
      updatePrompt("That's not the best move...");
    }
  };
}

function showNextBlunder(cg: Api) {
  const nextBlunders: Array<any> = JSON.parse(window.sessionStorage.getItem('chess-blunders.nextBlunders')) ?? [];

  if (nextBlunders.length < 1) {
    return;
  }

  // const blunder = nextBlunders.pop();
  const blunder = nextBlunders[0];
  console.log(blunder.solution);
  window.sessionStorage.setItem('chess-blunders.nextBlunders', JSON.stringify(nextBlunders));
  if (blunder === undefined) {
    return;
  }

  // reload blunders in the background, if necessary
  const runningLowOnBlunders = nextBlunders.length <= BLUNDERS_BUFFER_SIZE;
  if (runningLowOnBlunders) {
    const username = window.sessionStorage.getItem('chess-blunders.username');
    const source = window.sessionStorage.getItem('chess-blunders.source');
    requestBlunders(username, source);
  }

  // get the game details from the headers
  const fullGame = new Chess();
  fullGame.load_pgn(blunder.pgn); // final position
  const black = fullGame.header().Black;
  const username = window.sessionStorage.getItem('chess-blunders.username');
  const userColor = username === black ? 'black' : 'white';
  const opponentColor = username === black ? 'white' : 'black';

  // reset the board to the setup position
  const chess = new Chess(blunder.starting_fen);
  if (chess.turn() !== opponentColor[0]) {
    throw new Error('Something went wrong while parsing the game.');
  }
  cg.set({
    fen: blunder.starting_fen,
    orientation: userColor,
    turnColor: opponentColor,
  });

  // make the opponent's move right before our blunder
  const leadingMoveFrom = blunder.leading_move[0];
  const leadingMoveTo = blunder.leading_move[1];
  cg.move(leadingMoveFrom, leadingMoveTo);
  const afterMove = checkAgainstSolution(cg, chess, blunder);
  giveHandToOtherSide(cg, chess, afterMove)(leadingMoveFrom, leadingMoveTo);

  // set up the prompt
  const blunderMove = blunder.refutations[0][0];
  chess.move({ from: blunderMove[0], to: blunderMove[1] });
  const blunderMoveSAN = chess.history()[chess.history().length - 1];
  const fen = chess.fen().split(' ');
  chess.undo();
  const fullMoveCount = fen[fen.length - 1];
  const ellipsis = userColor === 'black' ? '...' : '';
  const prompt = (
    '<small>Find the alternative to <br /><br /> '
    + `${fullMoveCount}. ${ellipsis}<strong>${blunderMoveSAN}??</strong></small>`
  );
  updatePrompt(prompt);

  // bind the next move button to the new blunder
  document.getElementById('make-correct-move').onclick = () => {
    makeCorrectMove(cg, chess, blunder);
  };

  // reload blunders, if necessary

  updateNextBlunderBtn(nextBlunders);
  updateMakeCorrectMoveBtn(blunder, chess);
  return blunder;
}

function initializeBoard() {
  const chess = new Chess();
  const cg = Chessground(document.getElementById('puzzle'), {
    coordinates: true,
    animation: {
      enabled: true,
      duration: 750,
    },
    movable: {
      free: false,
      color: 'white',
      dests: toDests(chess),
    },
    resizable: true,
  });
  // resizeChessground(window.innerWidth, window.innerHeight);

  window.cg = cg; // for messing up with it from the browser console

  showNextBlunder(cg);

  return cg;
}

function requestBlunders(
  username: string,
  source: string,
  nGames: number = 3,
  nodes: number = 500000,
) {
  const outgoingMessage = {
    action: 'request-blunders',
    n_games: nGames,
    username,
    source,
    nodes,
  };
  socket.send(JSON.stringify(outgoingMessage));
  window.sessionStorage.setItem('chess-blunders.username', username);
  window.sessionStorage.setItem('chess-blunders.source', source);
}

/* ------------------------------------- Binding ------------------------------------ */
const cg = initializeBoard();

document.forms['blunders-form'].onsubmit = function () {
  if (this === undefined) {
    return false;
  }
  spinRequestButton();
  requestBlunders(this.username.value, this.source.value);
  return false;
};

document.getElementById('next-blunder').onclick = () => {
  showNextBlunder(cg);
};

socket.onmessage = (event) => {
  const nextBlunders: Array<any> = JSON.parse(
    window.sessionStorage.getItem('chess-blunders.nextBlunders'),
  ) ?? [];

  const message = JSON.parse(event.data);
  if (message.action === 'blunder') {
    nextBlunders.push(message.blunder);
    window.sessionStorage.setItem('chess-blunders.nextBlunders', JSON.stringify(nextBlunders));

    const isFirstBlunder = cg.getFen() === INITIAL_POSITION_FEN;
    if (isFirstBlunder) {
      showNextBlunder(cg);
    } else {
      updateNextBlunderBtn(nextBlunders);
    }
    stopRequestButton();
  }
};

// window.onresize = () => {
//   resizeChessground(window.innerWidth, window.innerHeight);
// };
