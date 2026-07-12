import { parseCycleToSeconds } from './time-engine.js';
import { calculateProduction } from './production-engine.js';
import { calculateMaterial } from './material-engine.js';
import { classifyStatus, calculatePresetWindow } from './status-engine.js';
import { validateMachineInput } from './validation-engine.js';

export function calculateMachine(input, context = {}) {
  const now = new Date(context.now ?? Date.now());
  const calculationStartedAt = new Date(context.calculationStartedAt ?? now);
  const validation = validateMachineInput(input);

  if (!validation.valid) {
    return {
      valid: false,
      validation,
      confidence: 0,
      audit: { inputs: { ...input }, errors: validation.errors }
    };
  }

  const cycleSeconds = parseCycleToSeconds(input.cycle);
  const production = calculateProduction({
    target: input.target,
    trays: input.trays || [],
    now,
    cycleSeconds
  });
  const material = calculateMaterial({
    barLength: input.barLength ?? 3600,
    pieceLength: input.pieceLength,
    kerfWidth: input.kerfWidth ?? 1,
    currentBarMode: input.currentBarMode ?? 'pieces',
    currentBarValue: input.currentBarValue ?? 0,
    fullBars: input.fullBars ?? 0
  });

  const piecesUntilStop = Math.min(production.remainingOrder, material.totalCapacity);
  const stopReason = production.remainingOrder <= material.totalCapacity ? 'order' : 'material';
  const durationSeconds = piecesUntilStop * cycleSeconds;
  const endAt = new Date(calculationStartedAt.getTime() + durationSeconds * 1000);
  const remainingMs = Math.max(0, endAt.getTime() - now.getTime());
  const status = classifyStatus({ now, endAt });
  const preset = calculatePresetWindow({ now, endAt, limitHours: input.presetLimitHours ?? 16 });

  const confidencePenalties = validation.warnings.length * 10;
  const confidence = Math.max(0, 100 - confidencePenalties);

  return {
    valid: true,
    cycle: {
      informed: String(input.cycle),
      seconds: cycleSeconds,
      decimalMinutes: cycleSeconds / 60
    },
    production,
    material,
    forecast: {
      calculationStartedAt,
      endAt,
      remainingMs,
      remainingSeconds: Math.ceil(remainingMs / 1000),
      piecesUntilStop,
      reason: stopReason
    },
    status,
    preset,
    confidence,
    validation,
    audit: {
      production: {
        formula: 'produção turnos passados + produção estimada do turno atual',
        previousShifts: production.previousShifts,
        currentEstimated: production.currentEstimated,
        completedEstimated: production.completedEstimated,
        remainingOrder: production.remainingOrder
      },
      material: {
        formula: 'barra atual + barras inteiras × peças por barra',
        pieceConsumptionMm: Number(input.pieceLength) + Number(input.kerfWidth ?? 1),
        perBar: material.perBar,
        currentPieces: material.currentPieces,
        totalCapacity: material.totalCapacity
      },
      forecast: {
        formula: 'menor entre saldo da OP e capacidade de MP × ciclo',
        piecesUntilStop,
        cycleSeconds,
        durationSeconds,
        stopReason
      }
    }
  };
}
