import { Api } from 'chessground/api';
import { Color, Key } from 'chessground/types';
import { Tooltip } from 'bootstrap';

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
      },
    });

    if (afterMove) {
      cg.set({
        movable: {
          events: {
            after: afterMove,
          },
        },
      });
    }
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
    const sidebarMenuMain = document.getElementById('sidebarMenuMain');
    const sidebarMenuMainNavLinks = sidebarMenuMain.querySelectorAll('.nav-link');
    const sidebarMenuMainTooltipsElements = [].slice.call(
      sidebarMenuMain.querySelectorAll('[data-bs-toggle="tooltip"]'),
    );
    const menuLabels = document.querySelectorAll('.menu-label');
    const sidebarMinWidth = 249;
    const buttonMinWidth = 50;
    const isPortraitOrientation = (
      width < parseFloat(px.substring(0, px.length - 2)) + sidebarMinWidth * 2
    );
    if (isPortraitOrientation) {
      sidebarMenu.style.position = 'relative';
      sidebarMenuMain.classList.remove('flex-column');
      sidebarMenuMain.classList.add('flex-row');
      menuLabels.forEach((menuLabel) => {
        menuLabel.classList.remove('d-inline');
        menuLabel.classList.add('d-none');
      });
      sidebarMenuMainTooltipsElements.forEach((tooltipElement) => {
        const tooltip = Tooltip.getInstance(tooltipElement);
        tooltip.enable();
      });
    } else {
      sidebarMenu.style.position = 'absolute';
      sidebarMenuMain.classList.remove('flex-row');
      sidebarMenuMain.classList.add('flex-column');
      menuLabels.forEach((menuLabel) => {
        menuLabel.classList.remove('d-none');
        menuLabel.classList.add('d-inline');
      });

      sidebarMenuMainTooltipsElements.forEach((tooltipElement) => {
        const tooltip = Tooltip.getInstance(tooltipElement);
        tooltip.disable();
      });
    }

    if ((isPortraitOrientation)
        && (sidebarMenuMain.offsetWidth < buttonMinWidth * menuLabels.length)) {
      sidebarMenuMainNavLinks.forEach((navLink) => {
        navLink.classList.add('px-0');
      });
    } else {
      sidebarMenuMainNavLinks.forEach((navLink) => {
        navLink.classList.remove('px-0');
      });
    }
  }
}
