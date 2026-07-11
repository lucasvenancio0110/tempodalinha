from pathlib import Path

path = Path('index.html')
raw = path.read_bytes()
newline = '\r\n' if b'\r\n' in raw else '\n'
text = raw.decode('utf-8').replace('\r\n', '\n').replace('\r', '\n')


def one(old: str, new: str, label: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'{label}: esperado 1, encontrado {count}')
    text = text.replace(old, new, 1)


one('<title>Tempo da Linha | VENANC Tools V9.2</title>', '<title>Tempo da Linha | VENANC Tools V9.4</title>', 'versão')
one(
    '''    .appHeader {
      position: sticky;
      top: 0;
      z-index: 50;''',
    '''    .appHeader {
      position: relative;
      z-index: 1;''',
    'cabeçalho não flutuante'
)
one(
    '    .btnDanger { color: var(--bad); background: var(--bad-bg); border-color: #ffd3d6; }',
    '''    .btnDanger { color: var(--bad); background: var(--bad-bg); border-color: #ffd3d6; }
    .calculationStartBox {
      margin-top:12px; display:flex; align-items:center; justify-content:space-between; gap:12px;
      border:1px solid #d9e5e8; border-radius:14px; padding:12px 14px;
      background:linear-gradient(145deg,#f8fbfc,#eef7f6);
    }
    .calculationStartBox span { color:#687b84; font-size:11px; font-weight:900; letter-spacing:.08em; text-transform:uppercase; }
    .calculationStartBox strong { color:#18343c; font-size:13px; font-weight:950; text-align:right; font-variant-numeric:tabular-nums; }
    .machineDangerZone {
      margin-top:12px; display:flex; align-items:center; justify-content:space-between; gap:14px;
      border:1px solid #f0d4d7; border-radius:15px; padding:13px 14px;
      background:linear-gradient(145deg,#fffafa,#fff3f4);
    }
    .machineDangerZone strong { display:block; color:#6e2229; font-size:14px; }
    .machineDangerZone span { display:block; margin-top:4px; color:#93656a; font-size:11px; font-weight:750; line-height:1.35; }
    .clearMachineBtn { flex:0 0 auto; min-height:44px; }
    @media (max-width:620px) {
      .calculationStartBox { align-items:flex-start; flex-direction:column; }
      .calculationStartBox strong { text-align:left; }
      .machineDangerZone { align-items:stretch; flex-direction:column; }
      .clearMachineBtn { width:100%; }
    }''',
    'estilos novos'
)
one(
    '        <div class="projectionCard" data-role="projectionCard">',
    '''        <div class="calculationStartBox">
          <span>Cálculo iniciado</span>
          <strong data-role="calculationStartedAt">Ainda não iniciado</strong>
        </div>

        <div class="projectionCard" data-role="projectionCard">''',
    'horário no card'
)
one(
    '        <div class="section requestBox" data-role="requestBox">',
    '''        <div class="machineDangerZone">
          <div>
            <strong>Reiniciar esta máquina</strong>
            <span>Apaga os dados preenchidos e mantém a TNL na célula.</span>
          </div>
          <button class="btn btnDanger clearMachineBtn" data-action="clearMachine" type="button">🗑 Limpar dados</button>
        </div>

        <div class="section requestBox" data-role="requestBox">''',
    'limpar dados no card'
)
one(
    '''      baseTimestamp,
      machine: "",''',
    '''      baseTimestamp,
      calculationStartedAt: null,
      machine: "",''',
    'campo início'
)
one(
    '''        ...machine,
        baseTimestamp,
        trays: Array.isArray(machine.trays) && machine.trays.length ? machine.trays : [""],''',
    '''        ...machine,
        baseTimestamp,
        calculationStartedAt: Number.isFinite(Number(machine && machine.calculationStartedAt))
          ? Number(machine.calculationStartedAt)
          : null,
        trays: Array.isArray(machine.trays) && machine.trays.length ? machine.trays : [""],''',
    'migração início'
)
one(
    '''    function fmtTime(d) {
      if (!d) return "-";
      return `${pad2(d.getHours())}:${pad2(d.getMinutes())}`;
    }''',
    '''    function fmtTime(d) {
      if (!d) return "-";
      return `${pad2(d.getHours())}:${pad2(d.getMinutes())}`;
    }

    function fmtExactDateTime(timestamp) {
      const date = new Date(timestamp);
      if (!Number.isFinite(date.getTime())) return "Ainda não iniciado";
      return `${fmtDate(date)} às ${pad2(date.getHours())}:${pad2(date.getMinutes())}:${pad2(date.getSeconds())}.${String(date.getMilliseconds()).padStart(3, "0")}`;
    }''',
    'formato exato'
)
one(
    '''      applyDynamicCard(node, machine, calc);

      bindField(node, machine, "timeInput");''',
    '''      applyDynamicCard(node, machine, calc);
      const calculationStartedAt = node.querySelector('[data-role="calculationStartedAt"]');
      if (calculationStartedAt) calculationStartedAt.textContent = fmtExactDateTime(machine.calculationStartedAt);

      bindField(node, machine, "timeInput");''',
    'mostrar início'
)
one(
    '''      state.machines.forEach(machine => {
        const calc = calcMachine(machine);
        calcs.push(calc);
        el.cards.appendChild(renderCard(machine, calc));
      });''',
    '''      state.machines.forEach(machine => {
        let calc = calcMachine(machine);
        if (calc.valid && !machine.calculationStartedAt) {
          const preservedStart = Number(machine.baseTimestamp);
          machine.calculationStartedAt = Number.isFinite(preservedStart) && preservedStart > 0
            ? preservedStart
            : Date.now();
          calc = calcMachine(machine);
        }
        calcs.push(calc);
        el.cards.appendChild(renderCard(machine, calc));
      });''',
    'migração visual de cálculos existentes'
)
one(
    '''        const calc = calcMachine(machine);
        applyDynamicCard(root, machine, calc);''',
    '''        let calc = calcMachine(machine);
        if (calc.valid && !machine.calculationStartedAt) {
          const exactStart = Date.now();
          machine.calculationStartedAt = exactStart;
          machine.baseTimestamp = exactStart;
          calc = calcMachine(machine);
          saveState();
        }
        const calculationStartedAt = root.querySelector('[data-role="calculationStartedAt"]');
        if (calculationStartedAt) calculationStartedAt.textContent = fmtExactDateTime(machine.calculationStartedAt);
        applyDynamicCard(root, machine, calc);''',
    'registrar início exato'
)
one(
    '''    function bindActions(root, machine) {
      root.querySelector('[data-action="toggle"]').addEventListener("click", () => {''',
    '''    function clearMachineData(machine) {
      const preservedId = machine.id;
      const preservedMachine = machine.machine;
      const clean = DEFAULT_MACHINE(Date.now());
      Object.assign(machine, clean, {
        id: preservedId,
        machine: preservedMachine,
        calculationStartedAt: null,
        collapsed: true
      });
    }

    function bindActions(root, machine) {
      root.querySelector('[data-action="toggle"]').addEventListener("click", () => {''',
    'função limpar'
)
one(
    '''      const removeButton = root.querySelector('[data-action="remove"]');
      if (removeButton) removeButton.style.display = "none";
      root.querySelector('[data-action="minusBar"]').addEventListener("click", () => {''',
    '''      const removeButton = root.querySelector('[data-action="remove"]');
      if (removeButton) removeButton.style.display = "none";
      const clearButton = root.querySelector('[data-action="clearMachine"]');
      if (clearButton) clearButton.addEventListener("click", () => {
        const label = `TNL ${formatTnl(machine.machine)}`;
        const confirmed = window.confirm(`Limpar os dados da ${label}?\n\nTodos os dados preenchidos serão apagados. A máquina continuará na célula.`);
        if (!confirmed) return;
        clearMachineData(machine);
        saveState();
        render();
      });
      root.querySelector('[data-action="minusBar"]').addEventListener("click", () => {''',
    'ação limpar'
)

required = [
    '<title>Tempo da Linha | VENANC Tools V9.4</title>',
    'data-action="clearMachine"',
    'function clearMachineData(machine)',
    'calculationStartedAt: null',
    'data-role="calculationStartedAt"',
    'function fmtExactDateTime(timestamp)',
    'machine.calculationStartedAt = exactStart',
    'machine.baseTimestamp = exactStart'
]
for token in required:
    if token not in text:
        raise RuntimeError(f'ausente: {token}')

path.write_bytes(text.replace('\n', newline).encode('utf-8'))
print('V9.4 aplicada.')
