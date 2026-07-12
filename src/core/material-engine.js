export function piecesPerFullBar({ barLength = 3600, pieceLength, kerfWidth = 1 }) {
  const bar = Number(barLength);
  const piece = Number(pieceLength);
  const kerf = Number(kerfWidth);
  const consumption = piece + kerf;
  if (![bar, piece, kerf, consumption].every(Number.isFinite) || bar <= 0 || piece <= 0 || kerf < 0 || consumption <= 0) return 0;
  return Math.max(0, Math.floor(bar / consumption));
}

export function currentBarPieces({ mode = 'pieces', value = 0, pieceLength, kerfWidth = 1, perBar }) {
  let pieces = 0;
  if (mode === 'full') pieces = perBar;
  else if (mode === 'millimeters') {
    const consumption = Number(pieceLength) + Number(kerfWidth);
    pieces = consumption > 0 ? Math.floor(Math.max(0, Number(value) || 0) / consumption) : 0;
  } else pieces = Math.max(0, Math.floor(Number(value) || 0));
  return perBar > 0 ? Math.min(perBar, pieces) : pieces;
}

export function calculateMaterial(input) {
  const perBar = piecesPerFullBar(input);
  const currentPieces = currentBarPieces({
    mode: input.currentBarMode,
    value: input.currentBarValue,
    pieceLength: input.pieceLength,
    kerfWidth: input.kerfWidth,
    perBar
  });
  const fullBars = Math.max(0, Math.floor(Number(input.fullBars) || 0));
  const fullBarsCapacity = fullBars * perBar;
  const totalCapacity = currentPieces + fullBarsCapacity;
  const currentPercent = perBar > 0 ? Math.max(0, Math.min(100, currentPieces / perBar * 100)) : 0;

  return { perBar, currentPieces, fullBars, fullBarsCapacity, totalCapacity, currentPercent };
}
