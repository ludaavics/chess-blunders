import { Chessground } from 'chessground';
import './styles/chessground.css';
import './styles/chessground-theme.css';
import 'bootstrap/dist/css/bootstrap.min.css';

const config = {};
Chessground(document.getElementById('puzzle'), config);

const socket = new WebSocket('wss://so6khh47cg.execute-api.us-east-1.amazonaws.com/dev');

function requestBlunders(
  username: string, source: string, nGames: number = 3, nodes: number = 500000,
) {
  const outgoingMessage = {
    action: 'request-blunders',
    n_games: nGames,
    username,
    source,
    nodes,
  };
  console.log(outgoingMessage);
  socket.send(JSON.stringify(outgoingMessage));
}
document.forms['blunders-form'].onsubmit = function () {
  requestBlunders(this.username.value, this.source.value);
  return false;
};

socket.onmessage = (event) => {
  const nextBlunders: Array<any> = JSON.parse(window.sessionStorage.getItem('nextBlunders')) ?? [];

  const message = JSON.parse(event.data);
  if (message.action === 'blunder') {
    nextBlunders.push(message.blunder);
    window.sessionStorage.setItem('nextBlunders', JSON.stringify(nextBlunders));
    console.log(`We now have ${nextBlunders.length} blunders in store..`);
  }
};
