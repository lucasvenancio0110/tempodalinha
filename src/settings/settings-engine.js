export function moveMachine(machines, machineId, direction) {
  if (!Array.isArray(machines)) return [];
  const copy = [...machines];
  const index = copy.findIndex(machine => machine.id === machineId);
  if (index < 0) return copy;
  const nextIndex = Math.max(0, Math.min(copy.length - 1, index + direction));
  if (nextIndex === index) return copy;
  [copy[index], copy[nextIndex]] = [copy[nextIndex], copy[index]];
  return copy;
}

export function restoreMachineOrder(machines, defaultNumbers = []) {
  if (!Array.isArray(machines)) return [];
  const rank = new Map(defaultNumbers.map((number, index) => [String(number).padStart(3, '0'), index]));
  return [...machines].sort((a, b) => {
    const aRank = rank.has(a.machine) ? rank.get(a.machine) : Number.MAX_SAFE_INTEGER;
    const bRank = rank.has(b.machine) ? rank.get(b.machine) : Number.MAX_SAFE_INTEGER;
    return aRank - bRank;
  });
}

export function sanitizeSettings(input = {}, defaults = {}) {
  const positive = (value, fallback) => {
    const number = Number(String(value).replace(',', '.'));
    return Number.isFinite(number) && number > 0 ? number : fallback;
  };
  const nonNegative = (value, fallback) => {
    const number = Number(String(value).replace(',', '.'));
    return Number.isFinite(number) && number >= 0 ? number : fallback;
  };
  return {
    ...defaults,
    barLength: positive(input.barLength, defaults.barLength ?? 3600),
    kerfWidth: nonNegative(input.kerfWidth, defaults.kerfWidth ?? 1),
    presetLimitHours: positive(input.presetLimitHours, defaults.presetLimitHours ?? 16),
    turnMinutes: positive(input.turnMinutes, defaults.turnMinutes ?? 480),
    gabaritoMode: input.gabaritoMode === 'sum' ? 'sum' : 'individual'
  };
}
