from pathlib import Path
import re

path = Path('index.html')
raw = path.read_bytes()
nl = '\r\n' if b'\r\n' in raw else '\n'
text = raw.decode('utf-8').replace('\r\n','\n').replace('\r','\n')

text = text.replace('VENANC Tools V11.0.04', 'VENANC Tools V11.1.00')

# Nova preferência de gabaritos.
text = text.replace(
"""      turnMinutes: 480,""",
"""      turnMinutes: 480,
      gabaritoMode: "sum",""",
1)

# Ajustes: modo dos gabaritos e organização da célula.
settings_anchor = '''        <div class="notice">
          O cálculo da matéria-prima considera <strong>comprimento da peça + largura do bedame</strong>. Exemplo: peça de 32 mm com bedame de 1 mm consome 33 mm por unidade.
        </div>'''
settings_new = '''        <div class="grid2 v111SettingsGrid">
          <div class="field">
            <label for="gabaritoMode">Preenchimento dos gabaritos</label>
            <select id="gabaritoMode" class="input">
              <option value="sum">Soma rápida: 60+40+39+22</option>
              <option value="individual">Campos individuais</option>
            </select>
          </div>
          <div class="field">
            <label>Ordem da célula atual</label>
            <div class="fixedRuleText">Mova as TNLs para acompanhar seu percurso.</div>
          </div>
        </div>
        <section class="machineOrderSettings" id="machineOrderSettings">
          <div class="machineOrderHeader"><strong>Organizar máquinas</strong><span>Use as setas para mover</span></div>
          <div class="machineOrderList" id="machineOrderList"></div>
        </section>
        <div class="notice">
          O cálculo da matéria-prima considera <strong>comprimento da peça + largura do bedame</strong>. Exemplo: peça de 32 mm com bedame de 1 mm consome 33 mm por unidade.
        </div>'''
if settings_anchor not in text:
    raise RuntimeError('âncora dos ajustes não encontrada')
text = text.replace(settings_anchor, settings_new, 1)

# Preserva a ordem personalizada que já está salva para cada célula.
old_create = '''    function createCellMachines(cell) {
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
    }'''
new_create = '''    function createCellMachines(cell) {
      const existing = Array.isArray(state.cells[cell]) ? state.cells[cell] : [];
      const defaults = CELL_MACHINES[cell].map(formatTnl);
      const byNumber = new Map(existing.map(machine => [formatTnl(machine.machine), machine]));
      const savedOrder = existing.map(machine => formatTnl(machine.machine)).filter(number => defaults.includes(number));
      const order = [...savedOrder, ...defaults.filter(number => !savedOrder.includes(number))];
      return order.map(key => {
        const saved = byNumber.get(key);
        if (saved) return { ...normalizeMachine(saved), machine: key };
        const machine = DEFAULT_MACHINE();
        machine.machine = key;
        machine.collapsed = true;
        return machine;
      });
    }'''
if old_create not in text:
    raise RuntimeError('createCellMachines não encontrada')
text = text.replace(old_create, new_create, 1)

# Funções de soma rápida, preview e organização.
insert_before_settings = '''    function openSettings() {'''
helpers = r'''    function parseGabaritoExpression(value) {
      const clean = String(value || '').replace(/\s+/g, '');
      if (!clean) return [];
      if (!/^\d+(?:\+\d+)*$/.test(clean)) return null;
      return clean.split('+').map(Number).filter(number => Number.isFinite(number) && number >= 0);
    }

    function gabaritoExpression(machine) {
      if (String(machine.trayExpression || '').trim()) return String(machine.trayExpression);
      return (Array.isArray(machine.trays) ? machine.trays : []).map(value => Math.max(0, parseInteger(value))).filter(Boolean).join('+');
    }

    function syncExpressionToTrays(machine, value) {
      machine.trayExpression = value;
      const parsed = parseGabaritoExpression(value);
      if (parsed) machine.trays = parsed.length ? parsed.map(String) : [''];
      syncPastProductionV11(machine);
      return parsed;
    }

    function moveMachineOrder(index, direction) {
      const next = index + direction;
      if (next < 0 || next >= state.machines.length) return;
      [state.machines[index], state.machines[next]] = [state.machines[next], state.machines[index]];
      state.cells[state.selectedCell] = state.machines;
      saveState();
      renderMachineOrderSettings();
      render();
    }

    function renderMachineOrderSettings() {
      const list = document.querySelector('#machineOrderList');
      const section = document.querySelector('#machineOrderSettings');
      if (!list || !section) return;
      section.hidden = !state.selectedCell || !state.machines.length;
      list.innerHTML = '';
      state.machines.forEach((machine, index) => {
        const row = document.createElement('div');
        row.className = 'machineOrderRow';
        row.innerHTML = `<span><b>${index + 1}</b>TNL ${formatTnl(machine.machine)}</span><div><button type="button" aria-label="Mover para cima" ${index === 0 ? 'disabled' : ''}>↑</button><button type="button" aria-label="Mover para baixo" ${index === state.machines.length - 1 ? 'disabled' : ''}>↓</button></div>`;
        const buttons = row.querySelectorAll('button');
        buttons[0].onclick = () => moveMachineOrder(index, -1);
        buttons[1].onclick = () => moveMachineOrder(index, 1);
        list.appendChild(row);
      });
    }

    function compactEditorPreview(machine) {
      const calc = calcMachine(machine);
      if (!calc.valid) return `<section class="editorLiveResult waiting"><span>RESULTADO</span><strong>Complete Ciclo, Meta e Peça</strong><small>A previsão aparecerá aqui automaticamente.</small></section>`;
      ensureExactStart(machine);
      const parts = formatCountdownParts(calc.restMs);
      const past = syncPastProductionV11(machine);
      const estimate = estimatedShiftProduction(machine, calc, Date.now());
      const target = Math.max(0, parseInteger(machine.target));
      const missing = Math.max(0, target - Math.min(target, past + estimate));
      const progress = target ? Math.min(100, ((past + estimate) / target) * 100) : 0;
      return `<section class="editorLiveResult">
        <div class="editorResultHead"><div><span>RESULTADO AO VIVO</span><strong>${escapeHtml(calc.statusText.toUpperCase())}</strong></div><b>${Math.round(progress)}%</b></div>
        <div class="editorResultClock"><span>Tempo restante</span><strong>${parts.clock}<small>.${parts.milliseconds}</small></strong></div>
        <div class="editorResultBar"><i style="width:${progress}%"></i></div>
        <div class="editorResultMetrics"><div><span>Turnos passados</span><strong>${past}</strong></div><div><span>Estimada do turno</span><strong>${estimate}</strong></div><div><span>Faltam</span><strong>${missing}</strong></div><div><span>MP disponível</span><strong>${calc.capacity}</strong></div></div>
      </section>`;
    }

    function updateCompactEditorPreview(machine) {
      const holder = machineScreenContent.querySelector('[data-v111-preview]');
      if (!holder) return;
      holder.innerHTML = compactEditorPreview(machine);
    }

'''
if insert_before_settings not in text:
    raise RuntimeError('openSettings não encontrada')
text = text.replace(insert_before_settings, helpers + insert_before_settings, 1)

# Ajustes abrem com as novas opções e salvam o modo.
old_open = '''    function openSettings() {
      el.barLength.value = state.settings.barLength;
      el.kerfWidth.value = state.settings.kerfWidth;
      el.turnMinutes.value = state.settings.turnMinutes;
      el.modal.showModal();
    }'''
new_open = '''    function openSettings() {
      el.barLength.value = state.settings.barLength;
      el.kerfWidth.value = state.settings.kerfWidth;
      el.turnMinutes.value = state.settings.turnMinutes;
      const mode = document.querySelector('#gabaritoMode');
      if (mode) mode.value = state.settings.gabaritoMode || 'sum';
      renderMachineOrderSettings();
      el.modal.showModal();
    }'''
text = text.replace(old_open, new_open, 1)
old_save = '''    function saveSettings() {
      state.settings.barLength = Math.max(1, parseNumber(el.barLength.value) || DEFAULT_SETTINGS.barLength);
      state.settings.kerfWidth = Math.max(0, parseNumber(el.kerfWidth.value) || 0);
      state.settings.turnMinutes = Math.max(1, parseInteger(el.turnMinutes.value) || DEFAULT_SETTINGS.turnMinutes);
      el.modal.close();
      render();
    }'''
new_save = '''    function saveSettings() {
      state.settings.barLength = Math.max(1, parseNumber(el.barLength.value) || DEFAULT_SETTINGS.barLength);
      state.settings.kerfWidth = Math.max(0, parseNumber(el.kerfWidth.value) || 0);
      state.settings.turnMinutes = Math.max(1, parseInteger(el.turnMinutes.value) || DEFAULT_SETTINGS.turnMinutes);
      state.settings.gabaritoMode = document.querySelector('#gabaritoMode')?.value || 'sum';
      saveState();
      el.modal.close();
      render();
    }'''
if old_save not in text:
    raise RuntimeError('saveSettings não encontrada')
text = text.replace(old_save, new_save, 1)

# Substitui somente a última versão ativa do editor V11.
pattern = re.compile(r"    function renderMachineEditor\(machine, calc\) \{.*?\n    \}\n\n    function renderMachineResult\(machine, calc\) \{", re.S)
matches = list(pattern.finditer(text))
if not matches:
    raise RuntimeError('editor V11 ativo não encontrado')
new_editor = r'''    function renderMachineEditor(machine, calc) {
      syncPastProductionV11(machine);
      const piecesLabel = machine.barMode === 'partialMm' ? 'Milímetros restantes' : 'Peças restantes';
      const piecesValue = machine.barMode === 'partialMm' ? machine.partialMm : machine.partialPieces;
      const totalTrays = trayTotalV11(machine);
      const useSum = (state.settings.gabaritoMode || 'sum') === 'sum';
      const gabaritos = useSum
        ? `<div class="quickTrayField"><label>Soma dos gabaritos</label><input class="operatorInput" data-v111-tray-expression inputmode="numeric" value="${escapeHtml(gabaritoExpression(machine))}" placeholder="60+40+39+22"><small data-v111-tray-feedback>Use números separados por +</small></div>`
        : `<div class="trayListV11">${traysMarkupV11(machine)}</div><button class="addTrayV11" data-v10-action="add-tray" type="button">Adicionar gabarito</button>`;
      machineScreenContent.innerHTML = `
        <section class="machineView operatorForm compactOperatorV111">
          <div class="operatorIntro"><div><span>Modo operador</span><strong>Preenchimento rápido</strong></div><span class="operatorModePill">ORDEM DA MÁQUINA</span></div>
          <div class="operatorGrid compactGridV111">
            <div class="operatorField cycleField"><label>1. Ciclo</label><input class="operatorInput" data-v10-field="timeInput" inputmode="decimal" value="${escapeHtml(String(machine.timeInput ?? ''))}" placeholder="2,24"></div>
            <div class="operatorField"><label>2. ${piecesLabel}</label><input class="operatorInput" data-v10-field="materialRemaining" inputmode="decimal" value="${escapeHtml(String(piecesValue ?? ''))}" placeholder="0"><div class="mpModeTabs"><button class="mpModeTab ${machine.barMode==='pieces'?'active':''}" data-v10-action="mp-mode" data-value="pieces" type="button">PEÇAS</button><button class="mpModeTab ${machine.barMode==='partialMm'?'active':''}" data-v10-action="mp-mode" data-value="partialMm" type="button">MM</button><button class="mpModeTab ${machine.barMode==='full'?'active':''}" data-v10-action="mp-mode" data-value="full" type="button">CHEIA</button></div></div>
            <div class="operatorField"><label>3. Meta da OP</label><input class="operatorInput" data-v10-field="target" inputmode="numeric" value="${escapeHtml(String(machine.target ?? ''))}" placeholder="1000"></div>
            <div class="operatorField"><label>4. Peça (mm)</label><input class="operatorInput" data-v10-field="pieceLength" inputmode="decimal" value="${escapeHtml(String(machine.pieceLength ?? ''))}" placeholder="32"></div>
            <div class="operatorField compactBarsV111"><label>5. Barras</label><div class="barCounter"><button type="button" data-v10-action="bar-minus">−</button><strong>${parseInteger(machine.fullBars)}</strong><button type="button" data-v10-action="bar-plus">＋</button></div></div>
            <details class="optionalPanel compactOptionalV111" ${machine.traysCollapsed === false ? 'open' : ''}><summary>Gabaritos — opcional <b>${totalTrays}</b></summary><div class="optionalBodyV11"><div class="trayTotalV11"><span>Produção dos turnos passados</span><strong>${totalTrays}</strong></div>${gabaritos}</div></details>
            <div data-v111-preview>${compactEditorPreview(machine)}</div>
            ${renderPresetV11(machine, calcMachine(machine))}
          </div>
        </section>`;
      machineScreenFooter.innerHTML = `<button class="machineFooterBtn" data-v10-action="previous" type="button" ${activeMachineIndex()<=0?'disabled':''}>${svgArrow(-1)} Anterior</button><button class="machineFooterBtn danger" data-v10-action="clear" type="button">Limpar dados</button><button class="machineFooterBtn primary" data-v10-action="save-next" type="button">Salvar e próxima ${svgArrow(1)}</button>`;
      bindMachineScreenEvents(machine);
    }

    function renderMachineResult(machine, calc) {'''
last = matches[-1]
text = text[:last.start()] + new_editor + text[last.end():]

# Substitui a última função ativa de eventos, sem foco artificial.
event_pattern = re.compile(r"    function bindMachineScreenEvents\(machine\) \{.*?\n    \}\n\n    function handleMachineScreenAction", re.S)
event_matches = list(event_pattern.finditer(text))
if not event_matches:
    raise RuntimeError('bindMachineScreenEvents ativo não encontrado')
new_events = r'''    function bindMachineScreenEvents(machine) {
      const mainInputs = [...machineScreenContent.querySelectorAll('[data-v10-field]')];
      mainInputs.forEach((input, index) => {
        input.addEventListener('input', () => {
          const field = input.dataset.v10Field;
          if (field === 'materialRemaining') {
            if (machine.barMode === 'partialMm') machine.partialMm = input.value; else machine.partialPieces = input.value;
          } else machine[field] = input.value;
          saveState();
          updateCompactEditorPreview(machine);
        });
        input.addEventListener('change', () => { ensureExactStart(machine); saveState(); updateCompactEditorPreview(machine); });
        input.addEventListener('keydown', event => {
          if (event.key !== 'Enter') return;
          event.preventDefault();
          const next = mainInputs.slice(index + 1).find(node => !node.readOnly && !node.disabled && node.offsetParent !== null);
          if (next) next.focus(); else input.blur();
        });
      });
      const expression = machineScreenContent.querySelector('[data-v111-tray-expression]');
      expression?.addEventListener('input', () => {
        const parsed = syncExpressionToTrays(machine, expression.value);
        const feedback = machineScreenContent.querySelector('[data-v111-tray-feedback]');
        if (feedback) { feedback.textContent = parsed === null ? 'Use somente números e o sinal +' : `Total: ${trayTotalV11(machine)} peças`; feedback.classList.toggle('error', parsed === null); }
        const totalNode = machineScreenContent.querySelector('.trayTotalV11 strong');
        const summaryNode = machineScreenContent.querySelector('.optionalPanel summary b');
        if (totalNode) totalNode.textContent = String(trayTotalV11(machine));
        if (summaryNode) summaryNode.textContent = String(trayTotalV11(machine));
        saveState();
        updateCompactEditorPreview(machine);
      });
      machineScreen.querySelectorAll('[data-v10-action]').forEach(button => { button.onclick = () => handleMachineScreenAction(button, machine); });
      machineScreenContent.querySelectorAll('[data-v10-tray]').forEach(input => {
        input.addEventListener('input', () => {
          machine.trays[Number(input.dataset.v10Tray)] = input.value;
          machine.trayExpression = '';
          const total = syncPastProductionV11(machine);
          saveState();
          const totalNode = machineScreenContent.querySelector('.trayTotalV11 strong');
          const summaryNode = machineScreenContent.querySelector('.optionalPanel summary b');
          if (totalNode) totalNode.textContent = String(total);
          if (summaryNode) summaryNode.textContent = String(total);
          updateCompactEditorPreview(machine);
        });
      });
      const details = machineScreenContent.querySelector('.optionalPanel');
      details?.addEventListener('toggle', () => { machine.traysCollapsed = !details.open; saveState(); });
    }

    function handleMachineScreenAction'''
last_event = event_matches[-1]
text = text[:last_event.start()] + new_events + text[last_event.end():]

# CSS compacto e ajustes premium.
css = r'''
    /* V11.1.00 — preenchimento compacto, resultado ao vivo e organização */
    .compactOperatorV111 .operatorIntro { margin-bottom:10px; }
    .compactGridV111 { gap:10px; grid-template-columns:repeat(2,minmax(0,1fr)); }
    .compactGridV111 .operatorField { min-height:122px; padding:14px 16px; }
    .compactGridV111 .cycleField { grid-column:auto; }
    .compactGridV111 .operatorField label { margin-bottom:9px; font-size:10px; }
    .compactGridV111 .operatorInput { min-height:44px; font-size:28px; line-height:1; padding:4px 0 8px; }
    .compactGridV111 .mpModeTabs { margin-top:8px; }
    .compactGridV111 .mpModeTab { min-height:34px; }
    .compactBarsV111 .barCounter { min-height:54px; }
    .compactBarsV111 .barCounter button { width:48px; height:48px; }
    .compactBarsV111 .barCounter strong { font-size:32px; }
    .compactOptionalV111 { grid-column:1/-1; }
    .quickTrayField label { display:block; color:#9db0b8; font-size:10px; font-weight:900; letter-spacing:.10em; text-transform:uppercase; }
    .quickTrayField .operatorInput { width:100%; margin-top:7px; border:1px solid rgba(255,255,255,.11); border-radius:12px; padding:11px 12px; color:#f5fbfc; background:rgba(255,255,255,.045); font-size:20px; }
    .quickTrayField small { display:block; margin-top:7px; color:#83a39f; font-weight:750; }
    .quickTrayField small.error { color:#ff9ba3; }
    [data-v111-preview] { grid-column:1/-1; }
    .editorLiveResult { border:1px solid rgba(86,213,199,.22); border-radius:18px; padding:15px; background:linear-gradient(145deg,rgba(86,213,199,.10),rgba(255,255,255,.035)); }
    .editorLiveResult.waiting { min-height:96px; display:flex; flex-direction:column; justify-content:center; }
    .editorLiveResult.waiting span,.editorResultHead span,.editorResultClock span,.editorResultMetrics span { color:#91a8b0; font-size:9px; font-weight:950; letter-spacing:.12em; text-transform:uppercase; }
    .editorLiveResult.waiting strong { margin-top:6px; font-size:18px; }
    .editorLiveResult.waiting small { margin-top:4px; color:#91a8b0; }
    .editorResultHead { display:flex; align-items:flex-start; justify-content:space-between; gap:12px; }
    .editorResultHead strong { display:block; margin-top:5px; color:var(--primary); font-size:15px; }
    .editorResultHead b { font-size:25px; }
    .editorResultClock { margin-top:14px; }
    .editorResultClock strong { display:block; margin-top:5px; font-family:"SFMono-Regular",Consolas,monospace; font-size:clamp(29px,8vw,43px); letter-spacing:-.07em; }
    .editorResultClock strong small { color:var(--primary); font-size:.42em; }
    .editorResultBar { height:7px; margin-top:12px; overflow:hidden; border-radius:999px; background:rgba(255,255,255,.09); }
    .editorResultBar i { display:block; height:100%; border-radius:inherit; background:var(--primary); }
    .editorResultMetrics { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:8px; margin-top:13px; }
    .editorResultMetrics div { min-width:0; border-radius:11px; padding:10px; background:rgba(255,255,255,.045); }
    .editorResultMetrics strong { display:block; margin-top:5px; font-size:20px; }
    .v111SettingsGrid { margin-top:12px; }
    .machineOrderSettings { margin-top:14px; border:1px solid var(--line); border-radius:15px; padding:13px; background:#f5f8f9; }
    .machineOrderHeader { display:flex; align-items:center; justify-content:space-between; gap:10px; color:var(--ink); }
    .machineOrderHeader span { color:var(--muted); font-size:11px; font-weight:750; }
    .machineOrderList { display:grid; gap:7px; margin-top:11px; max-height:310px; overflow:auto; }
    .machineOrderRow { display:flex; align-items:center; justify-content:space-between; gap:10px; border:1px solid var(--line); border-radius:11px; padding:7px 8px 7px 11px; background:#fff; }
    .machineOrderRow span { display:flex; align-items:center; gap:9px; color:var(--ink); font-weight:900; }
    .machineOrderRow span b { width:24px; height:24px; display:grid; place-items:center; border-radius:8px; color:#096f66; background:#e5f7f4; font-size:11px; }
    .machineOrderRow div { display:flex; gap:5px; }
    .machineOrderRow button { width:38px; height:36px; border:1px solid var(--line); border-radius:9px; color:var(--ink); background:#f7fafb; font-size:18px; font-weight:900; }
    @media(max-width:560px){
      .compactGridV111 .operatorField { min-height:108px; padding:12px 13px; }
      .compactGridV111 .operatorInput { font-size:25px; }
      .editorResultMetrics { grid-template-columns:repeat(2,minmax(0,1fr)); }
    }
'''
if '</style>' not in text:
    raise RuntimeError('style final não encontrado')
text = text.replace('</style>', css + '\n  </style>', 1)

required = [
    'VENANC Tools V11.1.00',
    'data-v111-tray-expression',
    'function moveMachineOrder',
    'function compactEditorPreview',
    'machineOrderList',
    'compactGridV111',
    'state.settings.gabaritoMode'
]
for token in required:
    if token not in text:
        raise RuntimeError(f'ausente: {token}')

path.write_bytes(text.replace('\n', nl).encode('utf-8'))
print('V11.1.00 aplicada.')
