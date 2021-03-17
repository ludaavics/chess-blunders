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

export function resizeChessground(width: number, height: number) {
  const el = document.querySelector('.cg-wrap') as HTMLElement;
  if (el) {
    const px = `${Math.min(width, height) * 0.75}px`;
    el.style.width = px;
    el.style.height = px;
    document.body.dispatchEvent(new Event('chessground.resize'));
  }
}
