export function parseCycleToSeconds(value) {
  if (value == null) return NaN;
  const text = String(value).trim().toLowerCase().replace(/\s+/g, "");
  if (!text) return NaN;

  const minuteSecond = text.match(/^(\d+)[,:](\d{1,2})$/);
  if (minuteSecond) {
    const minutes = Number(minuteSecond[1]);
    const seconds = Number(minuteSecond[2]);
    if (seconds >= 60) return NaN;
    return minutes * 60 + seconds;
  }

  const explicitSeconds = text.match(/^(\d+(?:[.,]\d+)?)s$/);
  if (explicitSeconds) return Number(explicitSeconds[1].replace(",", "."));

  const explicitMinutes = text.match(/^(\d+)m(?:(\d{1,2})s?)?$/);
  if (explicitMinutes) {
    const minutes = Number(explicitMinutes[1]);
    const seconds = Number(explicitMinutes[2] || 0);
    if (seconds >= 60) return NaN;
    return minutes * 60 + seconds;
  }

  if (/^\d+$/.test(text)) return Number(text);
  if (/^\d+\.\d+$/.test(text)) return Number(text) * 60;
  return NaN;
}

export function getShiftWindow(dateLike) {
  const date = new Date(dateLike);
  const base = new Date(date.getFullYear(), date.getMonth(), date.getDate(), 0, 0, 0, 0);
  const make = (hour, minute, dayOffset = 0) => {
    const result = new Date(base);
    result.setDate(result.getDate() + dayOffset);
    result.setHours(hour, minute, 0, 0);
    return result;
  };

  const minuteOfDay = date.getHours() * 60 + date.getMinutes();
  if (minuteOfDay < 390) return { id: 3, start: make(22, 40, -1), end: make(6, 30) };
  if (minuteOfDay < 880) return { id: 1, start: make(6, 30), end: make(14, 40) };
  if (minuteOfDay < 1360) return { id: 2, start: make(14, 40), end: make(22, 40) };
  return { id: 3, start: make(22, 40), end: make(6, 30, 1) };
}

export function getNextShiftWindow(current) {
  return getShiftWindow(new Date(current.end.getTime() + 1000));
}

export function elapsedShiftSeconds(nowLike) {
  const now = new Date(nowLike);
  const shift = getShiftWindow(now);
  return Math.max(0, Math.floor((now.getTime() - shift.start.getTime()) / 1000));
}
