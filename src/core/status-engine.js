import { getShiftWindow, getNextShiftWindow } from './time-engine.js';

export function classifyStatus({ now, endAt }) {
  const current = getShiftWindow(now);
  const next = getNextShiftWindow(current);
  const end = new Date(endAt);
  if (end <= current.end) return { key: 'red', label: 'Encerra neste turno' };
  if (end <= next.end) return { key: 'orange', label: 'Encerra no próximo turno' };
  return { key: 'green', label: 'Produção normal' };
}

export function calculatePresetWindow({ now, endAt, limitHours = 16 }) {
  const remainingMs = Math.max(0, new Date(endAt).getTime() - new Date(now).getTime());
  return { required: remainingMs < limitHours * 3600000, remainingHours: remainingMs / 3600000 };
}
