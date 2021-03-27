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
const defaultSettings = {
  source: 'chess.com',
  n_games: 3,
  nodes: 500000,
};

/* ---------------------------------------------------------------------------------- */
/*                                       Timers                                       */
/* ---------------------------------------------------------------------------------- */
const AFTER_SOLUTION_MOVE = 1000;
const AFTER_MY_REFUTATION_MOVE = 1000;
const AFTER_THEIR_REFUTATION_MOVE = 1500;

/* ---------------------------------------------------------------------------------- */
/*                                      Handlers                                      */
/* ---------------------------------------------------------------------------------- */

/* ---------------------------- Update Buttons and Prompt --------------------------- */
function updateNextBlunderBtn(nextBlunders) {
  const btn = document.getElementById('next-blunder');
  const counter = document.getElementById('next-blunder-counter');
  if (nextBlunders.length === 0) {
    btn.classList.add('disabled');
    btn.classList.add('text-muted');
    counter.classList.add('d-none');
  } else {
    btn.classList.remove('disabled');
    btn.classList.remove('text-muted');
    counter.classList.remove('d-none');
  }
}

function updateBlunderActionBtns(blunder, chess) {
  const btns = document.querySelectorAll('.blunder-action');
  const ply = chess.history().length - 1;
  if (blunder.solution.length > ply) {
    btns.forEach((btn) => {
      btn.classList.remove('disabled');
      btn.classList.remove('text-muted');
    });
  } else {
    btns.forEach((btn) => {
      btn.classList.add('disabled');
      btn.classList.add('text-muted');
    });
  }
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
  const refutationBtn = document.getElementById('view-refutation');
  const makeCorrectMoveBtn = document.getElementById('make-correct-move');
  refutationBtn.classList.add('disabled');
  refutationBtn.classList.add('text-muted');

  const ply = chess.history().length - 1;
  const solutionMoveFrom = blunder.solution[ply][0];
  const solutionMoveTo = blunder.solution[ply][1];
  makeMove(cg, chess, solutionMoveFrom, solutionMoveTo, null);

  if (blunder.solution.length > ply + 1) {
    const responseMoveFrom = blunder.solution[ply + 1][0];
    const responseMoveTo = blunder.solution[ply + 1][1];

    const afterMove = checkAgainstSolution(cg, chess, blunder);
    setTimeout(() => {
      makeMove(cg, chess, responseMoveFrom, responseMoveTo, afterMove);
      if (blunder.solution.length > ply + 2) {
        updatePrompt('Go on...');
      } else {
        updatePrompt('Well done!');
        makeCorrectMoveBtn.classList.add('disabled');
        makeCorrectMoveBtn.classList.add('text-muted');
      }
    },
    AFTER_SOLUTION_MOVE);
  } else {
    updatePrompt('Well done!');
    makeCorrectMoveBtn.classList.add('disabled');
    makeCorrectMoveBtn.classList.add('text-muted');
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

function makeRefutationMove(cg, chess, blunder) {
  const btn = document.getElementById('make-correct-move');
  btn.classList.add('disabled');
  btn.classList.add('text-muted');

  const ply = chess.history().length - 1;
  const refutationMoveFrom = blunder.refutations[0][ply][0];
  const refutationMoveTo = blunder.refutations[0][ply][1];
  makeMove(cg, chess, refutationMoveFrom, refutationMoveTo, null);

  if (blunder.refutations[0].length > ply + 1) {
    const timeout = (ply % 2 === 0) ? AFTER_MY_REFUTATION_MOVE : AFTER_THEIR_REFUTATION_MOVE;
    setTimeout(() => {
      makeRefutationMove(cg, chess, blunder);
    }, timeout);
  }
}

function copyText(text) {
  navigator.permissions.query({ name: 'clipboard-write' }).then((result) => {
    if (result.state === 'granted' || result.state === 'prompt') {
      navigator.clipboard.writeText(text).then(() => {
        // TODO: popover sayning opcied
      }, () => {
        // TODO: popvers saying not copied
      });
    } else {
      // TODO: popvers saying not copied
    }
  });
}

function getNextBlunder() {
  const nextBlunders: Array<any> = JSON.parse(window.sessionStorage.getItem('chess-blunders.nextBlunders')) ?? [];
  if (nextBlunders.length < 1) {
    return;
  }
  const blunder = nextBlunders.pop();
  window.sessionStorage.setItem('chess-blunders.nextBlunders', JSON.stringify(nextBlunders));
  return blunder;
}

function showNextBlunder(cg: Api, blunder = getNextBlunder()) {
  const nextBlunders: Array<any> = JSON.parse(window.sessionStorage.getItem('chess-blunders.nextBlunders')) ?? [];

  if (!blunder) {
    return;
  }

  // reload blunders in the background, if necessary
  const runningLowOnBlunders = nextBlunders.length <= BLUNDERS_BUFFER_SIZE;
  if (runningLowOnBlunders) {
    const settings = JSON.parse(window.sessionStorage.getItem('chess-blunders.settings'));
    requestBlunders(settings.username);
  }

  // get the game details from the headers
  const fullGame = new Chess();
  fullGame.load_pgn(blunder.pgn); // final position
  const black = fullGame.header().Black;
  const settings = JSON.parse(window.sessionStorage.getItem('chess-blunders.settings'));
  const userColor = settings.username === black ? 'black' : 'white';
  const opponentColor = settings.username === black ? 'white' : 'black';

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
    '<small>Find the alternative to <br/> '
    + `${fullMoveCount}. ${ellipsis}<strong>${blunderMoveSAN}??</strong></small>`
  );
  updatePrompt(prompt);

  // bind blunder-specific buttons
  document.getElementById('make-correct-move').onclick = () => {
    makeCorrectMove(cg, chess, blunder);
  };

  document.getElementById('view-refutation').onclick = () => {
    makeRefutationMove(cg, chess, blunder);
  };

  document.getElementById('restart').onclick = () => {
    showNextBlunder(cg, blunder);
  };

  document.getElementById('copy-pgn').onclick = () => {
    copyText(blunder.pgn);
  };

  document.getElementById('copy-all-pgn').onclick = () => {
    let pgn = '';
    const allBlunders : Array<any> = JSON.parse(
      window.sessionStorage.getItem('chess-blunders.nextBlunders'),
    ) ?? [];
    allBlunders.forEach((item) => {
      pgn += `\n\n${item.pgn}`;
    });
    copyText(pgn);
  };

  updateNextBlunderBtn(nextBlunders);
  updateBlunderActionBtns(blunder, chess);
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
  cg.set({
    movable: {
      events: {
        after: giveHandToOtherSide(cg, chess, null),
      },
    },
  });
  window.cg = cg; // for messing up with it from the browser console
  resizeChessground();

  showNextBlunder(cg);

  return cg;
}

function initializeSettings() {
  const settings = JSON.parse(JSON.stringify(defaultSettings));
  const sessionSettings = JSON.parse(window.sessionStorage.getItem('chess-blunders.settings') ?? '{}');
  Object.assign(settings, sessionSettings);
  window.sessionStorage.setItem('chess-blunders.settings', JSON.stringify(settings));
}

function requestBlunders(
  username: string,
) {
  if (!username) {
    throw new Error('username is a required argument.');
  }
  const settings = JSON.parse(window.sessionStorage.getItem('chess-blunders.settings'));
  const request = { action: 'request-blunders', username };
  Object.assign(request, settings);
  Object.assign(settings, { username });
  window.sessionStorage.setItem('chess-blunders.settings', JSON.stringify(settings));
  socket.send(JSON.stringify(request));
}

/* ------------------------------------- Binding ------------------------------------ */
feather.replace();
const cg = initializeBoard();
initializeSettings();

document.forms['blunders-form'].onsubmit = function () {
  if (this === undefined) {
    return false;
  }
  document.getElementById('blunders-form-spinner').classList.remove('invisible');
  requestBlunders(this.username.value);
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
    document.getElementById('blunders-form-spinner').classList.add('invisible');
  }
};

window.addEventListener('resize', resizeChessground);
