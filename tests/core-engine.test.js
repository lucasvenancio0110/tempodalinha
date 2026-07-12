import test from 'node:test';
import assert from 'node:assert/strict';

import { parseCycleToSeconds, getShiftWindow } from '../src/core/time-engine.js';
import { sumTrays, estimateCurrentShiftProduction } from '../src/core/production-engine.js';
import { calculateMaterial } from '../src/core/material-engine.js';
import { classifyStatus } from '../src/core/status-engine.js';
import { calculateMachine } from '../src/core/calc-engine.js';

const localDate = (year, month, day, hour, minute, second = 0) => new Date(year, month - 1, day, hour, minute, second, 0);

test('2,24 significa 2 minutos e 24 segundos', () => {
  assert.equal(parseCycleToSeconds('2,24'), 144);
  assert.equal(parseCycleToSeconds('2:24'), 144);
  assert.equal(parseCycleToSeconds('144s'), 144);
  assert.equal(parseCycleToSeconds('2m24s'), 144);
  assert.equal(parseCycleToSeconds('2,60'), Number.NaN);
});

test('produção dos turnos passados é exatamente a soma dos gabaritos', () => {
  assert.equal(sumTrays([60, 40, 39, 22]), 161);
  assert.equal(sumTrays([]), 0);
});

test('produção atual estimada considera apenas o turno atual', () => {
  const now = localDate(2026, 7, 10, 17, 4);
  assert.equal(estimateCurrentShiftProduction({ now, cycleSeconds: 144 }), 60);
});

test('capacidade da barra usa peça + bedame e arredonda para baixo', () => {
  const material = calculateMaterial({
    barLength: 3000,
    pieceLength: 12,
    kerfWidth: 1,
    currentBarMode: 'pieces',
    currentBarValue: 150,
    fullBars: 2
  });
  assert.equal(material.perBar, 230);
  assert.equal(material.currentPieces, 150);
  assert.equal(material.totalCapacity, 610);
});

test('barra parcial em milímetros é convertida em peças', () => {
  const material = calculateMaterial({
    barLength: 3600,
    pieceLength: 12,
    kerfWidth: 1,
    currentBarMode: 'millimeters',
    currentBarValue: 1300,
    fullBars: 0
  });
  assert.equal(material.currentPieces, 100);
});

test('previsão permanece fixa e contador diminui', () => {
  const input = {
    cycle: '2,24',
    target: 1000,
    trays: [100],
    barLength: 3000,
    pieceLength: 12,
    kerfWidth: 1,
    currentBarMode: 'pieces',
    currentBarValue: 150,
    fullBars: 2
  };
  const started = localDate(2026, 7, 10, 16, 0);
  const first = calculateMachine(input, { now: started, calculationStartedAt: started });
  const later = calculateMachine(input, { now: localDate(2026, 7, 10, 18, 0), calculationStartedAt: started });

  assert.equal(first.valid, true);
  assert.equal(first.forecast.reason, 'material');
  assert.equal(first.forecast.piecesUntilStop, 610);
  assert.equal(first.forecast.endAt.getTime(), later.forecast.endAt.getTime());
  assert.ok(later.forecast.remainingSeconds < first.forecast.remainingSeconds);
});

test('status usa os turnos reais', () => {
  const now = localDate(2026, 7, 10, 16, 0);
  assert.equal(classifyStatus({ now, endAt: localDate(2026, 7, 10, 20, 0) }).key, 'red');
  assert.equal(classifyStatus({ now, endAt: localDate(2026, 7, 11, 2, 0) }).key, 'orange');
  assert.equal(classifyStatus({ now, endAt: localDate(2026, 7, 11, 8, 0) }).key, 'green');
});

test('turno da madrugada cruza corretamente a meia-noite', () => {
  const shift = getShiftWindow(localDate(2026, 7, 11, 2, 0));
  assert.equal(shift.id, 3);
  assert.equal(shift.start.getDate(), 10);
  assert.equal(shift.end.getDate(), 11);
});

test('entrada inválida não produz números falsos', () => {
  const result = calculateMachine({ cycle: '0', target: 0, pieceLength: -1, trays: [] });
  assert.equal(result.valid, false);
  assert.ok(result.validation.errors.length >= 3);
  assert.equal(result.confidence, 0);
});
