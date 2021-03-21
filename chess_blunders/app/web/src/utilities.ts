import { Api } from 'chessground/api';
import { Color, Key } from 'chessground/types';

export function toDests(chess: any): Map<Key, Key[]> {
  const dests = new Map();
  chess.SQUARES.forEach((s) => {
    const ms = chess.moves({ square: s, verbose: true });
    if (ms.length) dests.set(s, ms.map((m) => m.to));
  });
  return dests;
}

export function toColor(chess: any): Color {
  return (chess.turn() === 'w') ? 'white' : 'black';
}

export function giveHandToOtherSide(cg: Api, chess, afterMove) {
  return (orig, dest) => {
    chess.move({ from: orig, to: dest });
    cg.set({
      turnColor: toColor(chess),
      movable: {
        free: false,
        color: toColor(chess),
        dests: toDests(chess),
        events: {
          after: afterMove,
        },
      },
    });
  };
}

export function resizeChessground() {
  const el = document.getElementById('puzzle') as HTMLElement;
  if (el) {
    const width = el.parentElement.offsetWidth;
    const height = el.parentElement.offsetHeight;
    const px = `${Math.floor((Math.min(width, height) * 0.95) / 8) * 8}px`;
    el.style.width = px;
    el.style.height = px;
    document.body.dispatchEvent(new Event('chessground.resize'));

    const sidebarMenu = document.getElementById('sidebarMenu');
    const sidebarMenuNav = sidebarMenu.querySelector('ul');
    if (width < height) {
      sidebarMenu.style.position = 'relative';
    } else {
      sidebarMenu.style.position = 'absolute';
    }
  }
}
