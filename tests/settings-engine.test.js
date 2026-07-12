import test from 'node:test';
import assert from 'node:assert/strict';
import { moveMachine, restoreMachineOrder, sanitizeSettings } from '../src/settings/settings-engine.js';

const machines = [
  { id: 'a', machine: '061' },
  { id: 'b', machine: '052' },
  { id: 'c', machine: '060' }
];

test('move máquina para cima e para baixo sem perder dados', () => {
  const down = moveMachine(machines, 'a', 1);
  assert.deepEqual(down.map(item => item.machine), ['052', '061', '060']);
  const up = moveMachine(down, '060', -1);
  assert.deepEqual(up.map(item => item.machine), ['052', '060', '061']);
  assert.equal(up.find(item => item.id === 'a').machine, '061');
});

test('não ultrapassa limites da lista', () => {
  assert.deepEqual(moveMachine(machines, 'a', -1).map(item => item.machine), ['061', '052', '060']);
  assert.deepEqual(moveMachine(machines, 'c', 1).map(item => item.machine), ['061', '052', '060']);
});

test('restaura a ordem padrão da célula', () => {
  const restored = restoreMachineOrder([machines[2], machines[0], machines[1]], [61, 52, 60]);
  assert.deepEqual(restored.map(item => item.machine), ['061', '052', '060']);
});

test('normaliza ajustes mantendo bedame zero permitido e padrão de 1 mm', () => {
  const defaults = { barLength: 3600, kerfWidth: 1, presetLimitHours: 16, turnMinutes: 480, gabaritoMode: 'individual' };
  assert.deepEqual(sanitizeSettings({}, defaults), defaults);
  const custom = sanitizeSettings({ barLength: '3000', kerfWidth: '0,8', presetLimitHours: 12, gabaritoMode: 'sum' }, defaults);
  assert.equal(custom.barLength, 3000);
  assert.equal(custom.kerfWidth, 0.8);
  assert.equal(custom.presetLimitHours, 12);
  assert.equal(custom.gabaritoMode, 'sum');
});
