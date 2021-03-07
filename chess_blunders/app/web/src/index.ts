import { Chess } from 'chess.js';
import { Chessground } from 'chessground';
import { Api } from 'chessground/api';
import { playOtherSide, toDests } from './utilities';
import './styles/chessground.css';
import './styles/chessground-theme.css';
import 'bootstrap/dist/css/bootstrap.min.css';

const INITIAL_POSITION_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR';
const BLUNDERS_BUFFER_SIZE = 5;
const socket = new WebSocket(process.env.API_URL);

/* ------------------------------------ Handlers ------------------------------------ */
function updateNextBlunderBtn(nextBlunders) {
  const btn = document.getElementById('next-blunder');
  if (nextBlunders.length === 0) {
    btn.classList.add('disabled');
    btn.classList.add('text-muted');
    btn.innerHTML = 'Next Blunder';
  } else {
    btn.classList.remove('disabled');
    btn.classList.remove('text-muted');
    btn.innerHTML = (
      `Next Blunder <span class="badge bg-secondary">\
      ${nextBlunders.length}</span>`);
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
function showNextBlunder(cg: Api) {
  const nextBlunders: Array<any> = JSON.parse(
    window.sessionStorage.getItem('nextBlunders'),
  ) ?? [];
  const nextBlunder = nextBlunders.pop();
  window.sessionStorage.setItem('nextBlunders', JSON.stringify(nextBlunders));
  if (nextBlunder === undefined) {
    return false;
  }

  // get the game details from the headers
  const fullGame = new Chess();
  fullGame.load_pgn(nextBlunder.pgn); // final position
  const black = fullGame.header().Black;
  const username = window.sessionStorage.getItem('username');
  const userColor = username === black ? 'black' : 'white';
  const opponentColor = username === black ? 'white' : 'black';

  // reset the board to the setup position and make the leading move
  const chess = new Chess(nextBlunder.starting_fen);
  if (chess.turn() !== opponentColor[0]) {
    throw new Error('Something went wrong while parsing the game.');
  }
  cg.set({
    fen: nextBlunder.starting_fen,
    orientation: userColor,
    turnColor: opponentColor,
    movable: {
      free: false,
      color: opponentColor,
      events: {
        after: playOtherSide(cg, chess),
      },
    },
  });
  const leadingMoveFrom = nextBlunder.leading_move[0];
  const leadingMoveTo = nextBlunder.leading_move[1];
  cg.move(leadingMoveFrom, leadingMoveTo);
  playOtherSide(cg, chess)(leadingMoveFrom, leadingMoveTo);

  // set up the prompt
  const blunderMove = nextBlunder.refutations[0][0];
  chess.move({ from: blunderMove[0], to: blunderMove[1] });
  const blunderMoveSAN = chess.history()[chess.history().length - 1];
  const fen = chess.fen().split(' ');
  const fullMoveCount = fen[fen.length - 1];
  const ellipsis = userColor === 'black' ? '...' : '';
  const prompt = (
    '<small>Find the alternative to <br /><br /> '
    + `${fullMoveCount}. ${ellipsis}<strong>${blunderMoveSAN}??</strong></small>`
  );
  updatePrompt(prompt);

  updateNextBlunderBtn(nextBlunders);
  return nextBlunder;
}

function initializeBoard() {
  const chess = new Chess();
  const cg = Chessground(document.getElementById('puzzle'), {
    coordinates: true,
    movable: {
      free: false,
      color: 'white',
      dests: toDests(chess),
    },
  });

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
  window.sessionStorage.setItem('username', username);
  window.sessionStorage.setItem('source', source);
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

  const nextBlunders: Array<any> = JSON.parse(
    window.sessionStorage.getItem('nextBlunders'),
  ) ?? [];
  const runningLowOnBlunders = nextBlunders.length <= BLUNDERS_BUFFER_SIZE;
  if (runningLowOnBlunders) {
    const username = window.sessionStorage.getItem('username');
    const source = window.sessionStorage.getItem('source');
    requestBlunders(username, source);
  }
};

socket.onmessage = (event) => {
  const nextBlunders: Array<any> = JSON.parse(
    window.sessionStorage.getItem('nextBlunders'),
  ) ?? [];

  const message = JSON.parse(event.data);
  if (message.action === 'blunder') {
    nextBlunders.push(message.blunder);
    window.sessionStorage.setItem('nextBlunders', JSON.stringify(nextBlunders));

    const isFirstBlunder = cg.getFen() === INITIAL_POSITION_FEN;
    if (isFirstBlunder) {
      showNextBlunder(cg);
    } else {
      updateNextBlunderBtn(nextBlunders);
    }
    stopRequestButton();
  }
};
