import { parseCycleToSeconds } from './time-engine.js';
import { sumTrays } from './production-engine.js';

export function validateMachineInput(input) {
  const errors = [];
  const warnings = [];
  const cycleSeconds = parseCycleToSeconds(input.cycle);
  const target = Number(input.target);
  const pieceLength = Number(input.pieceLength);
  const kerfWidth = Number(input.kerfWidth ?? 1);
  const barLength = Number(input.barLength ?? 3600);
  const previousShifts = sumTrays(input.trays || []);

  if (!Number.isFinite(cycleSeconds) || cycleSeconds <= 0) errors.push({ field: 'cycle', code: 'INVALID_CYCLE', message: 'Informe um ciclo válido.' });
  if (!Number.isFinite(target) || target <= 0) errors.push({ field: 'target', code: 'INVALID_TARGET', message: 'A Meta da OP deve ser maior que zero.' });
  if (!Number.isFinite(pieceLength) || pieceLength <= 0) errors.push({ field: 'pieceLength', code: 'INVALID_PIECE_LENGTH', message: 'O comprimento da peça deve ser maior que zero.' });
  if (!Number.isFinite(kerfWidth) || kerfWidth < 0) errors.push({ field: 'kerfWidth', code: 'INVALID_KERF', message: 'A largura do bedame não pode ser negativa.' });
  if (!Number.isFinite(barLength) || barLength <= 0) errors.push({ field: 'barLength', code: 'INVALID_BAR_LENGTH', message: 'O comprimento da barra deve ser maior que zero.' });
  if (Number.isFinite(target) && target > 0 && previousShifts > target) warnings.push({ field: 'trays', code: 'PAST_PRODUCTION_OVER_TARGET', message: 'A produção dos turnos passados ultrapassa a Meta da OP.' });
  if (Number.isFinite(pieceLength) && Number.isFinite(kerfWidth) && Number.isFinite(barLength) && pieceLength + kerfWidth > barLength) errors.push({ field: 'pieceLength', code: 'PIECE_LARGER_THAN_BAR', message: 'A peça com o bedame é maior que a barra.' });

  return { valid: errors.length === 0, errors, warnings, normalized: { cycleSeconds, target, pieceLength, kerfWidth, barLength, previousShifts } };
}
