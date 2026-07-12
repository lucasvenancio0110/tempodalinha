import test from 'node:test';
import assert from 'node:assert/strict';
import {
  STORAGE_KEY,
  MIGRATION_BACKUP_KEY,
  createDefaultState,
  loadState,
  saveState,
  readMigrationBackup,
  restoreMigrationBackup
} from '../src/storage/storage-engine.js';

class MemoryStorage {
  constructor(initial = {}) {
    this.map = new Map(Object.entries(initial));
  }
  getItem(key) { return this.map.has(key) ? this.map.get(key) : null; }
  setItem(key, value) { this.map.set(key, String(value)); }
  removeItem(key) { this.map.delete(key); }
}

test('estado novo inicia com bedame 1 mm e gabarito individual', () => {
  const storage = new MemoryStorage();
  const result = loadState(storage);
  assert.equal(result.source, 'default');
  assert.equal(result.state.settings.kerfWidth, 1);
  assert.equal(result.state.settings.gabaritoMode, 'individual');
  assert.deepEqual(result.state.cells, {});
});

test('migra formato legado preservando ordem, máquinas e horários', () => {
  const startedAt = 1_720_000_000_000;
  const legacy = {
    selectedCell: '5',
    settings: {
      barLength: 3600,
      kerfWidth: 2,
      requestLimit: 16,
      turnMinutes: 480,
      gabaritoMode: 'sum'
    },
    cells: {
      '05': [
        {
          id: 'old-95',
          machine: '95',
          timeInput: '2,24',
          target: '1000',
          pieceLength: '12',
          fullBars: 2,
          barMode: 'pieces',
          partialPieces: '120',
          trays: ['60', '40', '39', '22'],
          calculationStartedAt: startedAt,
          baseTimestamp: startedAt,
          presetMode: 'yes',
          presetType: 'vermelho'
        },
        {
          id: 'old-94',
          machine: '94',
          timeInput: '90',
          trays: ['10']
        }
      ]
    }
  };
  const storage = new MemoryStorage({
    'expertcnc-reformulado-v1': JSON.stringify(legacy)
  });

  const result = loadState(storage, { now: 1_800_000_000_000 });
  assert.equal(result.migrated, true);
  assert.equal(result.state.selectedCell, '05');
  assert.equal(result.state.settings.kerfWidth, 2);
  assert.equal(result.state.settings.gabaritoMode, 'sum');
  assert.deepEqual(result.state.cells['05'].map(m => m.machine), ['095', '094']);

  const machine = result.state.cells['05'][0];
  assert.equal(machine.cycle, '2,24');
  assert.equal(machine.currentBarMode, 'pieces');
  assert.equal(machine.currentBarValue, '120');
  assert.deepEqual(machine.trays, ['60', '40', '39', '22']);
  assert.equal(machine.calculationStartedAt, startedAt);
  assert.equal(machine.baseTimestamp, startedAt);
  assert.equal(machine.preset.brought, true);
  assert.equal(machine.preset.type, 'vermelho');

  assert.ok(storage.getItem(STORAGE_KEY));
  const backup = readMigrationBackup(storage);
  assert.equal(backup.sourceKey, 'expertcnc-reformulado-v1');
  assert.equal(backup.raw, JSON.stringify(legacy));
});

test('usa machines da célula ativa quando o legado não possui cells', () => {
  const legacy = {
    selectedCell: '5',
    settings: {},
    machines: [
      { machine: 95, timeInput: '1:30', trays: [] },
      { machine: 94, timeInput: '2:00', trays: ['25'] }
    ]
  };
  const storage = new MemoryStorage({
    'expertcnc-reformulado-v1': JSON.stringify(legacy)
  });
  const result = loadState(storage);
  assert.deepEqual(result.state.cells['05'].map(m => m.machine), ['095', '094']);
  assert.deepEqual(result.state.cells['05'][0].trays, ['']);
});

test('save e load preservam o schema normalizado', () => {
  const storage = new MemoryStorage();
  const state = createDefaultState();
  state.selectedCell = '05';
  state.cells['05'] = [{
    id: 'm1',
    machine: '069',
    cycle: '2,24',
    target: '500',
    pieceLength: '12',
    fullBars: 1,
    currentBarMode: 'partialMm',
    currentBarValue: '1800',
    trays: ['100', '50'],
    calculationStartedAt: 1_700_000_000_000,
    baseTimestamp: 1_700_000_000_000,
    preset: { brought: false, type: 'sequencia', itemCode: 'ABC' }
  }];

  saveState(storage, state, 1_900_000_000_000);
  const loaded = loadState(storage);
  assert.equal(loaded.source, 'current');
  assert.equal(loaded.state.updatedAt, 1_900_000_000_000);
  assert.equal(loaded.state.cells['05'][0].machine, '069');
  assert.equal(loaded.state.cells['05'][0].currentBarMode, 'partialMm');
  assert.equal(loaded.state.cells['05'][0].currentBarValue, '1800');
});

test('backup de migração não é sobrescrito e pode ser restaurado', () => {
  const original = JSON.stringify({ selectedCell: '05', settings: {}, cells: {} });
  const storage = new MemoryStorage({
    'expertcnc-reformulado-v1': original,
    [MIGRATION_BACKUP_KEY]: JSON.stringify({
      createdAt: 123,
      sourceKey: 'expertcnc-reformulado-v1',
      raw: 'backup-original'
    })
  });

  loadState(storage);
  assert.equal(readMigrationBackup(storage).raw, 'backup-original');
  assert.equal(restoreMigrationBackup(storage), true);
  assert.equal(storage.getItem('expertcnc-reformulado-v1'), 'backup-original');
  assert.equal(storage.getItem(STORAGE_KEY), null);
});

test('JSON inválido não derruba o app', () => {
  const storage = new MemoryStorage({
    [STORAGE_KEY]: '{quebrado',
    'expertcnc-reformulado-v1': '{tambem-quebrado'
  });
  const result = loadState(storage);
  assert.equal(result.source, 'default');
  assert.equal(result.state.settings.kerfWidth, 1);
});
