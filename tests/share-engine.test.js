import test from 'node:test';
import assert from 'node:assert/strict';
import { buildCellReport } from '../src/share/share-engine.js';

const machines = [
  { machine: '061', preset: { brought: true, type: 'azul' } },
  { machine: '052', preset: { brought: false, type: 'sequencia' } },
  { machine: '060', preset: { brought: false, type: 'sequencia' } }
];

const results = new Map([
  ['061', { valid: true, status: { key: 'green', label: 'Produção normal' }, forecast: { remainingMs: 7200000, endAt: new Date('2026-07-12T20:00:00-03:00') }, production: { remainingOrder: 400, currentEstimated: 80 }, preset: { required: false } }],
  ['052', { valid: true, status: { key: 'red', label: 'Encerra neste turno' }, forecast: { remainingMs: 3600000, endAt: new Date('2026-07-12T19:00:00-03:00') }, production: { remainingOrder: 120, currentEstimated: 40 }, preset: { required: true } }],
  ['060', { valid: false, validation: { errors: [] } }]
]);

function calculate(machine) {
  return results.get(machine.machine);
}

test('gera resumo com contagens corretas', () => {
  const report = buildCellReport({ cellId: '05', machines, calculate, now: new Date('2026-07-12T18:00:00-03:00') });
  assert.deepEqual(report.counts, { calculated: 2, total: 3, red: 1, orange: 0, green: 1, pending: 1 });
  assert.match(report.text, /PULSE CNC · CÉLULA 05/);
  assert.match(report.text, /Calculadas: 2\/3/);
});

test('ordena crítico antes de normal e pendente', () => {
  const report = buildCellReport({ cellId: '05', machines, calculate, now: Date.now() });
  assert.deepEqual(report.rows.map(row => row.machine.machine), ['052', '061', '060']);
});

test('inclui produção, previsão e situação do preset', () => {
  const report = buildCellReport({ cellId: '05', machines, calculate, now: Date.now() });
  assert.match(report.text, /052 · ENCERRA NESTE TURNO/);
  assert.match(report.text, /Faltam: 120 · Estimada no turno: 40/);
  assert.match(report.text, /Preset: ainda não trouxe/);
  assert.match(report.text, /060 · SEM CÁLCULO/);
});
