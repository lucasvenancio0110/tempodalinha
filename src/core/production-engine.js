import { elapsedShiftSeconds } from './time-engine.js';

export function sumTrays(trays = []) {
  return trays.reduce((total, value) => {
    const number = Number(String(value ?? '').replace(',', '.'));
    return total + (Number.isFinite(number) && number > 0 ? Math.floor(number) : 0);
  }, 0);
}

export function estimateCurrentShiftProduction({ now, cycleSeconds }) {
  if (!Number.isFinite(cycleSeconds) || cycleSeconds <= 0) return 0;
  return Math.max(0, Math.floor(elapsedShiftSeconds(now) / cycleSeconds));
}

export function calculateProduction({ target, trays, now, cycleSeconds }) {
  const previousShifts = sumTrays(trays);
  const currentEstimated = estimateCurrentShiftProduction({ now, cycleSeconds });
  const completedEstimated = previousShifts + currentEstimated;
  const orderTarget = Math.max(0, Math.floor(Number(target) || 0));
  const remainingOrder = Math.max(0, orderTarget - completedEstimated);

  return {
    target: orderTarget,
    previousShifts,
    currentEstimated,
    completedEstimated,
    remainingOrder
  };
}
