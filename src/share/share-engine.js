const PRIORITY = { red: 0, orange: 1, green: 2, neutral: 3 };

function pad(value) {
  return String(value).padStart(2, '0');
}

function machineLabel(value) {
  return String(Number.parseInt(value, 10) || 0).padStart(3, '0');
}

function formatClock(milliseconds) {
  const total = Math.max(0, Math.ceil(Number(milliseconds || 0) / 1000));
  return `${pad(Math.floor(total / 3600))}:${pad(Math.floor((total % 3600) / 60))}:${pad(total % 60)}`;
}

function formatDateTime(value) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '-';
  return `${pad(date.getDate())}/${pad(date.getMonth() + 1)} ${pad(date.getHours())}:${pad(date.getMinutes())}`;
}

function presetText(machine, result) {
  if (!result.valid || !result.preset.required) return null;
  if (!machine.preset?.brought) return 'Preset: ainda não trouxe';
  const names = { sequencia: 'Sequência', azul: 'Setup azul', verde: 'Setup verde', vermelho: 'Setup vermelho' };
  return `Preset: disponível · ${names[machine.preset.type] || 'Sequência'}`;
}

export function buildCellReport({ cellId, machines, calculate, now = Date.now() }) {
  if (typeof calculate !== 'function') throw new TypeError('calculate é obrigatório');
  const rows = machines.map(machine => ({ machine, result: calculate(machine, now) }));
  rows.sort((a, b) => {
    const aKey = a.result.valid ? a.result.status.key : 'neutral';
    const bKey = b.result.valid ? b.result.status.key : 'neutral';
    const priority = PRIORITY[aKey] - PRIORITY[bKey];
    return priority || Number(a.machine.machine) - Number(b.machine.machine);
  });

  const valid = rows.filter(row => row.result.valid);
  const counts = {
    calculated: valid.length,
    total: rows.length,
    red: valid.filter(row => row.result.status.key === 'red').length,
    orange: valid.filter(row => row.result.status.key === 'orange').length,
    green: valid.filter(row => row.result.status.key === 'green').length,
    pending: rows.length - valid.length
  };

  const lines = [
    `PULSE CNC · CÉLULA ${String(cellId).padStart(2, '0')}`,
    `Atualizado em ${formatDateTime(now)}`,
    '',
    `Calculadas: ${counts.calculated}/${counts.total}`,
    `Neste turno: ${counts.red}`,
    `Próximo turno: ${counts.orange}`,
    `Produção normal: ${counts.green}`,
    `Pendentes: ${counts.pending}`,
    ''
  ];

  for (const { machine, result } of rows) {
    const number = machineLabel(machine.machine);
    if (!result.valid) {
      lines.push(`${number} · SEM CÁLCULO`);
      continue;
    }
    lines.push(`${number} · ${result.status.label.toUpperCase()}`);
    lines.push(`Restante: ${formatClock(result.forecast.remainingMs)} · Previsão: ${formatDateTime(result.forecast.endAt)}`);
    lines.push(`Faltam: ${result.production.remainingOrder} · Estimada no turno: ${result.production.currentEstimated}`);
    const preset = presetText(machine, result);
    if (preset) lines.push(preset);
    lines.push('');
  }

  return { text: lines.join('\n').trim(), counts, rows };
}
