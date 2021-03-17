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
