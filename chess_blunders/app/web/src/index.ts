import { Chessground } from 'chessground';
import './styles/chessground.css';
import './styles/chessground-theme.css';
import 'bootstrap/dist/css/bootstrap.min.css';

const config = {};
Chessground(document.getElementById('puzzle'), config);

const socket = new WebSocket('wss://so6khh47cg.execute-api.us-east-1.amazonaws.com/dev');

document.forms['blunders-form'].onsubmit = function () {
  const outgoingMessage = {
    action: 'request-blunders',
    n_games: 3,
    username: this.username.value,
    source: this.source.value,
  };
  console.log(outgoingMessage);
  socket.send(JSON.stringify(outgoingMessage));
  return false;
};

socket.onmessage = function (event) {
  const message = JSON.parse(event.data);
  console.log(message);
  if (message.action === 'blunder') {
    const blunderText = `${message.blunder.pgn}\n\n`;
    document.getElementById('blunders').textContent += blunderText;
  }
};
