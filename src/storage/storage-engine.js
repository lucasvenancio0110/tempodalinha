export const STORAGE_SCHEMA_VERSION = 1;
export const STORAGE_KEY = 'pulse-cnc-state-v1';
export const LEGACY_STORAGE_KEYS = ['expertcnc-reformulado-v1'];
export const MIGRATION_BACKUP_KEY = 'pulse-cnc-migration-backup-v1';

const APP_VERSION = '1.0.0-beta';

function finiteNumber(value, fallback = 0) {
  const normalized = typeof value === 'string' ? value.replace(',', '.') : value;
  const number = Number(normalized);
  return Number.isFinite(number) ? number : fallback;
}

function nonNegativeInteger(value, fallback = 0) {
  return Math.max(0, Math.trunc(finiteNumber(value, fallback)));
}

function validTimestamp(value, fallback = null) {
  const number = Number(value);
  return Number.isFinite(number) && number > 0 ? number : fallback;
}

function normalizeCellId(value) {
  if (value === null || value === undefined || value === '') return null;
  const numeric = Number.parseInt(String(value), 10);
  if (!Number.isFinite(numeric) || numeric < 1) return null;
  return String(numeric).padStart(2, '0');
}

function makeId(machineNumber = '', index = 0) {
  const machine = String(machineNumber || 'machine').padStart(3, '0');
  return `m-${machine}-${index}`;
}

export function createDefaultSettings() {
  return {
    barLength: 3600,
    kerfWidth: 1,
    presetLimitHours: 16,
    turnMinutes: 480,
    gabaritoMode: 'individual'
  };
}

export function createDefaultMachine({ machine = '', id = null, index = 0 } = {}) {
  return {
    id: id || makeId(machine, index),
    machine: String(machine || '').replace(/\D/g, '').padStart(3, '0').slice(-3),
    cycle: '',
    target: '',
    pieceLength: '',
    fullBars: 0,
    currentBarMode: 'pieces',
    currentBarValue: '',
    trays: [''],
    calculationStartedAt: null,
    baseTimestamp: null,
    preset: {
      brought: false,
      type: 'sequencia',
      itemCode: ''
    }
  };
}

function normalizePreset(machine = {}) {
  const source = machine.preset && typeof machine.preset === 'object' ? machine.preset : {};
  const legacyMode = machine.presetMode;
  const brought = typeof source.brought === 'boolean'
    ? source.brought
    : legacyMode === 'yes';
  const allowedTypes = new Set(['sequencia', 'azul', 'verde', 'vermelho']);
  const typeCandidate = source.type ?? machine.presetType ?? 'sequencia';
  return {
    brought,
    type: allowedTypes.has(typeCandidate) ? typeCandidate : 'sequencia',
    itemCode: String(source.itemCode ?? machine.itemCode ?? '')
  };
}

export function normalizeMachine(machine = {}, index = 0) {
  const machineNumber = String(machine.machine ?? '').replace(/\D/g, '').padStart(3, '0').slice(-3);
  const modeCandidate = machine.currentBarMode ?? machine.barMode ?? 'pieces';
  const allowedModes = new Set(['pieces', 'partialMm', 'full']);
  const currentBarMode = allowedModes.has(modeCandidate) ? modeCandidate : 'pieces';

  let currentBarValue = machine.currentBarValue;
  if (currentBarValue === undefined) {
    if (currentBarMode === 'partialMm') currentBarValue = machine.partialMm ?? '';
    else if (currentBarMode === 'full') currentBarValue = '';
    else currentBarValue = machine.partialPieces ?? '';
  }

  const trays = Array.isArray(machine.trays)
    ? machine.trays.map(value => String(value ?? ''))
    : [''];

  const calculationStartedAt = validTimestamp(machine.calculationStartedAt);
  const baseTimestamp = validTimestamp(machine.baseTimestamp, calculationStartedAt);

  return {
    ...createDefaultMachine({ machine: machineNumber, id: machine.id, index }),
    id: String(machine.id || makeId(machineNumber, index)),
    machine: machineNumber,
    cycle: String(machine.cycle ?? machine.timeInput ?? ''),
    target: String(machine.target ?? ''),
    pieceLength: String(machine.pieceLength ?? ''),
    fullBars: nonNegativeInteger(machine.fullBars),
    currentBarMode,
    currentBarValue: String(currentBarValue ?? ''),
    trays: trays.length ? trays : [''],
    calculationStartedAt,
    baseTimestamp,
    preset: normalizePreset(machine)
  };
}

export function createDefaultState() {
  return {
    schemaVersion: STORAGE_SCHEMA_VERSION,
    appVersion: APP_VERSION,
    selectedCell: null,
    settings: createDefaultSettings(),
    cells: {},
    updatedAt: null
  };
}

function normalizeSettings(settings = {}) {
  const defaults = createDefaultSettings();
  return {
    barLength: finiteNumber(settings.barLength, defaults.barLength) > 0
      ? finiteNumber(settings.barLength, defaults.barLength)
      : defaults.barLength,
    kerfWidth: finiteNumber(settings.kerfWidth, defaults.kerfWidth) >= 0
      ? finiteNumber(settings.kerfWidth, defaults.kerfWidth)
      : defaults.kerfWidth,
    presetLimitHours: finiteNumber(settings.presetLimitHours ?? settings.requestLimit, defaults.presetLimitHours) > 0
      ? finiteNumber(settings.presetLimitHours ?? settings.requestLimit, defaults.presetLimitHours)
      : defaults.presetLimitHours,
    turnMinutes: finiteNumber(settings.turnMinutes, defaults.turnMinutes) > 0
      ? finiteNumber(settings.turnMinutes, defaults.turnMinutes)
      : defaults.turnMinutes,
    gabaritoMode: settings.gabaritoMode === 'sum' ? 'sum' : 'individual'
  };
}

export function normalizeState(state = {}) {
  const cellsSource = state.cells && typeof state.cells === 'object' ? state.cells : {};
  const cells = {};

  for (const [rawCellId, machines] of Object.entries(cellsSource)) {
    const cellId = normalizeCellId(rawCellId);
    if (!cellId || !Array.isArray(machines)) continue;
    cells[cellId] = machines.map((machine, index) => normalizeMachine(machine, index));
  }

  return {
    schemaVersion: STORAGE_SCHEMA_VERSION,
    appVersion: APP_VERSION,
    selectedCell: normalizeCellId(state.selectedCell),
    settings: normalizeSettings(state.settings),
    cells,
    updatedAt: validTimestamp(state.updatedAt)
  };
}

export function migrateLegacyState(legacyState = {}) {
  const cells = legacyState.cells && typeof legacyState.cells === 'object'
    ? legacyState.cells
    : {};

  // Algumas versões mantinham a célula ativa apenas em `machines`.
  const selectedCell = normalizeCellId(legacyState.selectedCell);
  const migratedCells = { ...cells };
  if (selectedCell && Array.isArray(legacyState.machines) && !Array.isArray(migratedCells[selectedCell])) {
    migratedCells[selectedCell] = legacyState.machines;
  }

  return normalizeState({
    selectedCell,
    settings: legacyState.settings,
    cells: migratedCells,
    updatedAt: Date.now()
  });
}

function parseJson(raw) {
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

function assertStorage(storage) {
  if (!storage || typeof storage.getItem !== 'function' || typeof storage.setItem !== 'function') {
    throw new TypeError('Um armazenamento compatível com localStorage é obrigatório.');
  }
}

export function saveState(storage, state, now = Date.now()) {
  assertStorage(storage);
  const normalized = normalizeState({ ...state, updatedAt: now });
  storage.setItem(STORAGE_KEY, JSON.stringify(normalized));
  return normalized;
}

export function loadState(storage, { now = Date.now() } = {}) {
  assertStorage(storage);

  const currentRaw = storage.getItem(STORAGE_KEY);
  const current = parseJson(currentRaw);
  if (current) {
    return {
      state: normalizeState(current),
      source: 'current',
      migrated: false,
      recovered: false
    };
  }

  for (const legacyKey of LEGACY_STORAGE_KEYS) {
    const legacyRaw = storage.getItem(legacyKey);
    const legacy = parseJson(legacyRaw);
    if (!legacy) continue;

    if (!storage.getItem(MIGRATION_BACKUP_KEY)) {
      storage.setItem(MIGRATION_BACKUP_KEY, JSON.stringify({
        createdAt: now,
        sourceKey: legacyKey,
        raw: legacyRaw
      }));
    }

    const migratedState = migrateLegacyState(legacy);
    const saved = saveState(storage, migratedState, now);
    return {
      state: saved,
      source: legacyKey,
      migrated: true,
      recovered: false
    };
  }

  return {
    state: createDefaultState(),
    source: 'default',
    migrated: false,
    recovered: false
  };
}

export function readMigrationBackup(storage) {
  assertStorage(storage);
  return parseJson(storage.getItem(MIGRATION_BACKUP_KEY));
}

export function restoreMigrationBackup(storage) {
  assertStorage(storage);
  const backup = readMigrationBackup(storage);
  if (!backup || !backup.sourceKey || typeof backup.raw !== 'string') return false;
  storage.setItem(backup.sourceKey, backup.raw);
  storage.removeItem(STORAGE_KEY);
  return true;
}
