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


one(
    '<title>Tempo da Linha | VENANC Tools V9.2</title>',
    '<title>Tempo da Linha | VENANC Tools V9.3</title>',
    'versão',
)

one(
    '''    .appHeader {
      position: sticky;
      top: 0;
      z-index: 50;''',
    '''    .appHeader {
      position: relative;
      z-index: 1;''',
    'cabeçalho não flutuante',
)

one(
    '    .btnDanger { color: var(--bad); background: var(--bad-bg); border-color: #ffd3d6; }',
    '''    .btnDanger { color: var(--bad); background: var(--bad-bg); border-color: #ffd3d6; }
    .machineDangerZone {
      margin-top: 12px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
      border: 1px solid #f0d4d7;
      border-radius: 15px;
      padding: 13px 14px;
      background: linear-gradient(145deg, #fffafa, #fff3f4);
    }
    .machineDangerZone strong { display:block; color:#6e2229; font-size:14px; }
    .machineDangerZone span { display:block; margin-top:4px; color:#93656a; font-size:11px; font-weight:750; line-height:1.35; }
    .clearMachineBtn { flex:0 0 auto; min-height:44px; }
    @media (max-width: 620px) {
      .machineDangerZone { align-items:stretch; flex-direction:column; }
      .clearMachineBtn { width:100%; }
    }''',
    'estilo da limpeza',
)

one(
    '        <div class="section requestBox" data-role="requestBox">',
    '''        <div class="machineDangerZone">
          <div>
            <strong>Reiniciar esta máquina</strong>
            <span>Apaga apenas os dados preenchidos e mantém a TNL na célula.</span>
          </div>
          <button class="btn btnDanger clearMachineBtn" data-action="clearMachine" type="button">🗑 Limpar dados</button>
        </div>

        <div class="section requestBox" data-role="requestBox">''',
    'botão limpar dados',
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
        collapsed: true
      });
    }

    function bindActions(root, machine) {
      root.querySelector('[data-action="toggle"]').addEventListener("click", () => {''',
    'função limpar máquina',
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
        const confirmed = window.confirm(`Limpar os dados da ${label}?\n\nTodos os dados preenchidos desta máquina serão apagados. A máquina continuará na célula.`);
        if (!confirmed) return;
        clearMachineData(machine);
        saveState();
        render();
      });
      root.querySelector('[data-action="minusBar"]').addEventListener("click", () => {''',
    'ação limpar máquina',
)

required = [
    'position: relative;',
    'data-action="clearMachine"',
    'function clearMachineData(machine)',
    'machine: preservedMachine',
    'collapsed: true',
]
for token in required:
    if token not in text:
        raise RuntimeError(f'ausente: {token}')

path.write_bytes(text.replace('\n', newline).encode('utf-8'))
print('V9.3 aplicada com sucesso.')
