from pathlib import Path

path = Path('index.html')
raw = path.read_bytes()
newline = '\r\n' if b'\r\n' in raw else '\n'
text = raw.decode('utf-8').replace('\r\n','\n').replace('\r','\n')


def one(old, new, label):
    global text
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'{label}: esperado 1, encontrado {count}')
    text = text.replace(old, new, 1)

one('<title>Tempo da Linha | VENANC Tools V8</title>', '<title>Tempo da Linha | VENANC Tools V9</title>', 'titulo')

one('''    .appHeader {
      position: sticky;''', '''    .cellSelector {
      min-height: 100vh;
      display: grid;
      place-items: center;
      padding: 24px 16px;
      background:
        radial-gradient(circle at top, rgba(86,213,199,.14), transparent 38%),
        linear-gradient(145deg, var(--bg), var(--bg-2));
    }
    .cellSelectorPanel {
      width: min(720px, 100%);
      border: 1px solid var(--line-dark);
      border-radius: 24px;
      padding: 22px;
      background: linear-gradient(145deg, #162630, #101b23);
      box-shadow: var(--shadow-strong);
    }
    .cellSelectorBrand { display:flex; align-items:center; gap:12px; margin-bottom:18px; }
    .cellSelectorBrand .mark { flex:0 0 46px; }
    .cellSelectorTitle h1 { margin:0; color:#f5fbfc; font-size:28px; letter-spacing:-.045em; }
    .cellSelectorTitle p { margin:6px 0 0; color:#a9bec6; font-size:14px; font-weight:700; }
    .cellGrid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:10px; }
    .cellBtn {
      min-height:76px;
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:12px;
      border:1px solid rgba(255,255,255,.10);
      border-radius:16px;
      padding:14px 15px;
      color:#eefbfa;
      background:rgba(255,255,255,.055);
      text-align:left;
      transition:transform .15s ease, background .15s ease, border-color .15s ease;
    }
    .cellBtn:hover { transform:translateY(-1px); background:rgba(86,213,199,.12); border-color:rgba(86,213,199,.35); }
    .cellBtn strong { display:block; font-size:18px; }
    .cellBtn span { display:block; margin-top:4px; color:#9fb7be; font-size:11px; font-weight:850; }
    .cellBtn b { color:var(--primary); font-size:22px; }
    body.cell-selection .appHeader, body.cell-selection main { display:none; }
    body:not(.cell-selection) .cellSelector { display:none; }
    .cellIndicator { color:var(--primary); font-size:12px; font-weight:950; letter-spacing:.05em; }
    .machineCard.emptyMachine .cardHead { border-bottom:0; }
    .machineCard.emptyMachine .cardMini .dot,
    .machineCard.emptyMachine [data-role="miniEnd"] { display:none; }
    .machineCard.emptyMachine .cardHead { cursor:pointer; }
    .machineCard.emptyMachine .machineToken { min-width:64px; }

    .appHeader {
      position: sticky;''', 'css seletor')

one('''    @media (max-width: 530px) {
      .heroIntro { padding: 18px 16px; }''', '''    @media (max-width: 530px) {
      .cellSelector { padding:14px 10px; }
      .cellSelectorPanel { padding:16px 12px; border-radius:19px; }
      .cellSelectorTitle h1 { font-size:23px; }
      .cellGrid { grid-template-columns:1fr; gap:8px; }
      .cellBtn { min-height:66px; padding:12px 13px; }
      .heroIntro { padding: 18px 16px; }''', 'css mobile')

one('<body>', '<body class="cell-selection">', 'body class')

selector = '''  <section class="cellSelector" id="cellSelector" aria-label="Selecionar célula">
    <div class="cellSelectorPanel">
      <div class="cellSelectorBrand">
        <div class="mark" aria-hidden="true">TL</div>
        <div class="cellSelectorTitle">
          <h1>Defina a linha</h1>
          <p>Toque na célula para abrir as máquinas correspondentes.</p>
        </div>
      </div>
      <div class="cellGrid" id="cellGrid"></div>
    </div>
  </section>

'''
one('<body class="cell-selection">\n  <header class="appHeader">', '<body class="cell-selection">\n' + selector + '  <header class="appHeader">', 'html seletor')

one('''      <div class="toolbar">
        <button class="btn btnPrimary" id="addMachineBtn" type="button">＋ Máquina</button>
        <button class="btn btnGhost" id="settingsBtn" type="button">⚙ Ajustes</button>
      </div>''', '''      <div class="toolbar">
        <span class="cellIndicator" id="activeCellLabel">-</span>
        <button class="btn btnGhost" id="changeCellBtn" type="button">Trocar célula</button>
        <button class="btn btnGhost" id="settingsBtn" type="button">⚙ Ajustes</button>
      </div>''', 'toolbar')

one('''    <div class="cards" id="cards"></div>
    <div class="empty" id="emptyState">Nenhuma máquina cadastrada.</div>
    <div class="bottomAddWrap">
      <button class="btn btnPrimary bottomAddBtn" id="addMachineBottomBtn" type="button">
        <span class="addButtonIcon" aria-hidden="true">＋</span>
        <span>Adicionar máquina</span>
      </button>
    </div>''', '''    <div class="cards" id="cards"></div>
    <div class="empty" id="emptyState">Nenhuma máquina cadastrada.</div>''', 'remover add inferior')

one('''        <div class="grid2 compactInputs">
          <div class="field">
            <label>Máquina</label>
            <input class="input" data-field="machine" placeholder="Ex.: 95">
          </div>
          <div class="field">
            <label>Ciclo</label>
            <input class="input" data-field="timeInput" inputmode="decimal" placeholder="Ex.: 2,30">
          </div>
        </div>''', '''        <div class="grid2 compactInputs">
          <div class="field" style="grid-column:1 / -1">
            <label>Ciclo</label>
            <input class="input" data-field="timeInput" inputmode="decimal" placeholder="Ex.: 2,30">
          </div>
        </div>''', 'remover campo maquina')

one('      V8 — botão inferior + cronômetro detalhado em tempo real', '      V9 — seleção de célula + TNLs automáticas + cards vazios compactos', 'comentario versao')

cell_js = '''
    const CELL_MACHINES = {
      "01": [2,5,15,19,23,24,25,26,27,29,30,35,46,47,48],
      "02": [3,4,7,8,13,16,17,18,28,31,32,49,50,51,143],
      "03": [9,10,33,34,36,37,39,40,41,43,44],
      "04": [42,52,53,57,58,59,60,61,64,65,66],
      "05": [69,72,83,85,87,88,89,90,91,92,93,94,95],
      "06": [67,68,73,74,75,76,77,79,81,82,84,86],
      "07": [45,54,55,56,62,63,70,71,78,80,102,103,110,111],
      "08": [96,98,104,107,112,113,115,116,118,119,121,122],
      "09": [97,99,100,101,105,106,108,109,114,117,120,123],
      "10": [124,125,126,127,128,129,130,134,135,136,137,138,139,140,141,142]
    };

    function formatTnl(value) {
      return String(parseInt(value, 10) || 0).padStart(3, "0");
    }
'''
one('''    const STORAGE_KEY = "expertcnc-reformulado-v1"; // Mantido para preservar os dados já cadastrados
    const DEFAULT_SETTINGS = {''', '''    const STORAGE_KEY = "expertcnc-reformulado-v1"; // Mantido para preservar os dados já cadastrados
''' + cell_js + '''
    const DEFAULT_SETTINGS = {''', 'const cells')

one('''    function loadState() {
      const nowTimestamp = Date.now();
      try {
        const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || "null");
        if (saved && saved.settings && Array.isArray(saved.machines)) {
          const legacyTimestamp = getTimestampFromLegacyBase(saved.base);
          const migrationTimestamp = Number.isFinite(legacyTimestamp) ? legacyTimestamp : nowTimestamp;
          return {
            settings: { ...DEFAULT_SETTINGS, ...saved.settings },
            machines: saved.machines.length
              ? saved.machines.map(machine => normalizeMachine(machine, migrationTimestamp))
              : [DEFAULT_MACHINE(nowTimestamp)]
          };
        }
      } catch (_) {}
      return { settings: { ...DEFAULT_SETTINGS }, machines: [DEFAULT_MACHINE(nowTimestamp)] };
    }''', '''    function loadState() {
      const nowTimestamp = Date.now();
      try {
        const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || "null");
        if (saved && saved.settings) {
          const legacyTimestamp = getTimestampFromLegacyBase(saved.base);
          const migrationTimestamp = Number.isFinite(legacyTimestamp) ? legacyTimestamp : nowTimestamp;
          const cells = saved.cells && typeof saved.cells === "object" ? saved.cells : {};
          Object.keys(cells).forEach(cell => {
            cells[cell] = Array.isArray(cells[cell])
              ? cells[cell].map(machine => normalizeMachine(machine, migrationTimestamp))
              : [];
          });
          return {
            settings: { ...DEFAULT_SETTINGS, ...saved.settings },
            selectedCell: null,
            cells,
            machines: []
          };
        }
      } catch (_) {}
      return { settings: { ...DEFAULT_SETTINGS }, selectedCell: null, cells: {}, machines: [] };
    }''', 'loadState')

one('''    function saveState() {
      try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch (_) {}
    }''', '''    function saveState() {
      if (state.selectedCell) state.cells[state.selectedCell] = state.machines;
      try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch (_) {}
    }

    function createCellMachines(cell) {
      const existing = Array.isArray(state.cells[cell]) ? state.cells[cell] : [];
      const byNumber = new Map(existing.map(machine => [formatTnl(machine.machine), machine]));
      return CELL_MACHINES[cell].map(number => {
        const key = formatTnl(number);
        const saved = byNumber.get(key);
        if (saved) return { ...normalizeMachine(saved), machine: key };
        const machine = DEFAULT_MACHINE();
        machine.machine = key;
        machine.collapsed = true;
        return machine;
      });
    }

    function selectCell(cell) {
      if (!CELL_MACHINES[cell]) return;
      state.selectedCell = cell;
      state.machines = createCellMachines(cell);
      state.cells[cell] = state.machines;
      document.body.classList.remove("cell-selection");
      document.querySelector("#activeCellLabel").textContent = `CÉLULA ${cell}`;
      render();
      saveState();
      window.scrollTo({ top: 0, behavior: "instant" });
    }

    function showCellSelector() {
      saveState();
      state.selectedCell = null;
      state.machines = [];
      document.body.classList.add("cell-selection");
      window.scrollTo({ top: 0, behavior: "instant" });
    }

    function renderCellSelector() {
      const grid = document.querySelector("#cellGrid");
      grid.innerHTML = "";
      Object.entries(CELL_MACHINES).forEach(([cell, machines]) => {
        const button = document.createElement("button");
        button.className = "cellBtn";
        button.type = "button";
        button.innerHTML = `<div><strong>CÉLULA ${cell}</strong><span>${machines.length} máquinas</span></div><b>›</b>`;
        button.addEventListener("click", () => selectCell(cell));
        grid.appendChild(button);
      });
    }''', 'save and cells')

one('''      node.dataset.id = machine.id;
      node.classList.toggle("collapsed", !!machine.collapsed);''', '''      node.dataset.id = machine.id;
      const isEmpty = !String(machine.timeInput || "").trim() && !String(machine.target || "").trim() && !String(machine.pieceLength || "").trim();
      node.classList.toggle("emptyMachine", isEmpty);
      node.classList.toggle("collapsed", isEmpty || !!machine.collapsed);''', 'compact empty')

one('''      bindField(node, machine, "machine");
      bindField(node, machine, "timeInput");''', '''      bindField(node, machine, "timeInput");''', 'remove machine binding')

one('''      renderTrays(node, machine, calc);
      renderRequest(node, machine, calc);
      bindActions(node, machine);''', '''      renderTrays(node, machine, calc);
      renderRequest(node, machine, calc);
      bindActions(node, machine);
      node.querySelector(".cardHead").addEventListener("click", event => {
        if (event.target.closest("button")) return;
        machine.collapsed = !machine.collapsed;
        render();
      });''', 'head click')

one('''    function addMachine() {
      state.machines.forEach(machine => machine.collapsed = true);
      const newMachine = DEFAULT_MACHINE();
      newMachine.collapsed = false;
      state.machines.push(newMachine);
      render();
      requestAnimationFrame(() => {
        const newCard = document.querySelector(`.machineCard[data-id="${newMachine.id}"]`);
        newCard?.scrollIntoView({ behavior: "smooth", block: "start" });
      });
    }

    document.querySelector("#addMachineBtn").addEventListener("click", addMachine);
    document.querySelector("#addMachineBottomBtn").addEventListener("click", addMachine);''', '''    document.querySelector("#changeCellBtn").addEventListener("click", showCellSelector);''', 'remove add listeners')

one('''    blockIOSZoom();
    render();
    updateLiveClock();''', '''    blockIOSZoom();
    renderCellSelector();
    updateLiveClock();''', 'startup')

# Never allow deletion of predefined machines.
one('''      root.querySelector('[data-action="remove"]').addEventListener("click", () => {
        state.machines = state.machines.filter(item => item.id !== machine.id);
        if (!state.machines.length) state.machines = [DEFAULT_MACHINE()];
        render();
      });''', '''      const removeButton = root.querySelector('[data-action="remove"]');
      if (removeButton) removeButton.style.display = "none";''', 'disable remove')

required = ['CELL_MACHINES', 'CÉLULA 10', 'formatTnl', 'showCellSelector', 'emptyMachine', 'changeCellBtn']
for token in required:
    if token not in text:
        raise RuntimeError(f'ausente: {token}')

path.write_bytes(text.replace('\n', newline).encode('utf-8'))
print('V9 aplicada')
