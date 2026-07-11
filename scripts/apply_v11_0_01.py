from pathlib import Path

path = Path('index.html')
raw = path.read_bytes()
newline = '\r\n' if b'\r\n' in raw else '\n'
text = raw.decode('utf-8').replace('\r\n', '\n').replace('\r', '\n')

if '<title>Tempo da Linha | VENANC Tools V11.0.01</title>' in text:
    print('V11.0.01 já aplicada.')
    raise SystemExit(0)

text = text.replace('<title>Tempo da Linha | VENANC Tools V10</title>', '<title>Tempo da Linha | VENANC Tools V11.0.01</title>', 1)

anchor = '    <section class="summaryGrid" aria-label="Resumo da célula">'
overview = '''    <section class="cellOverviewV11" id="cellOverviewV11" aria-label="Painel geral da célula">
      <div class="cellOverviewTop">
        <div><span>Andamento da célula</span><strong id="v11CellProgressText">0 de 0 calculadas</strong></div>
        <span class="cellHealthV11" id="v11CellHealth">SEM DADOS</span>
      </div>
      <div class="cellProgressTrackV11"><i id="v11CellProgressBar"></i></div>
      <div class="cellStatsV11">
        <div><span>Calculadas</span><strong id="v11Calculated">0</strong></div>
        <div><span>Pendentes</span><strong id="v11Pending">0</strong></div>
        <div><span>Neste turno</span><strong id="v11ThisShift">0</strong></div>
        <div><span>Próximo turno</span><strong id="v11NextShift">0</strong></div>
        <div><span>Preset pendente</span><strong id="v11PresetPending">0</strong></div>
        <div><span>Média restante</span><strong id="v11AverageRest">--:--</strong></div>
      </div>
      <div class="cellMachineProgressV11" id="v11MachineProgress"></div>
    </section>

'''
if anchor not in text:
    raise RuntimeError('Resumo da célula não encontrado')
text = text.replace(anchor, overview + anchor, 1)

css = r'''

    /* V11.0.01 — painel operacional simples e premium */
    .cellOverviewV11 {
      margin-bottom:10px; border:1px solid rgba(255,255,255,.08); border-radius:18px; padding:14px;
      background:linear-gradient(145deg,rgba(255,255,255,.07),rgba(255,255,255,.035));
      box-shadow:0 16px 42px rgba(0,0,0,.14); backdrop-filter:blur(16px);
    }
    .cellOverviewTop { display:flex; align-items:center; justify-content:space-between; gap:12px; }
    .cellOverviewTop span { color:#88a1a8; font-size:9px; font-weight:950; letter-spacing:.11em; text-transform:uppercase; }
    .cellOverviewTop strong { display:block; margin-top:4px; color:#effafa; font-size:18px; letter-spacing:-.035em; }
    .cellHealthV11 { flex:0 0 auto; border:1px solid rgba(86,213,199,.25); border-radius:999px; padding:7px 10px; color:#75ded1 !important; background:rgba(86,213,199,.08); }
    .cellHealthV11.warn { color:#f2ba6b !important; border-color:rgba(242,186,107,.25); background:rgba(242,186,107,.08); }
    .cellHealthV11.bad { color:#ff949d !important; border-color:rgba(255,148,157,.25); background:rgba(255,148,157,.08); }
    .cellProgressTrackV11 { height:7px; margin-top:12px; overflow:hidden; border-radius:999px; background:rgba(255,255,255,.07); }
    .cellProgressTrackV11 i { display:block; width:0; height:100%; border-radius:inherit; background:linear-gradient(90deg,#25aa9b,#67e2d3); transition:width .24s ease; }
    .cellStatsV11 { display:grid; grid-template-columns:repeat(6,minmax(0,1fr)); gap:7px; margin-top:11px; }
    .cellStatsV11 div { min-width:0; border-radius:12px; padding:9px 10px; background:rgba(0,0,0,.13); }
    .cellStatsV11 span { display:block; color:#789098; font-size:8px; font-weight:900; letter-spacing:.07em; text-transform:uppercase; }
    .cellStatsV11 strong { display:block; margin-top:5px; color:#edf8f8; font-size:18px; letter-spacing:-.04em; }
    .cellMachineProgressV11 { display:flex; gap:6px; overflow-x:auto; margin-top:10px; padding-bottom:2px; scrollbar-width:none; }
    .cellMachineProgressV11::-webkit-scrollbar { display:none; }
    .cellMachineDotV11 { flex:0 0 auto; min-width:39px; height:29px; display:grid; place-items:center; border:1px solid rgba(255,255,255,.08); border-radius:9px; color:#7d969d; background:rgba(255,255,255,.025); font-size:10px; font-weight:950; }
    .cellMachineDotV11.done { color:#082d28; background:#56d5c7; border-color:#56d5c7; }
    .cellMachineDotV11.attention { color:#ffc16f; border-color:rgba(255,193,111,.32); background:rgba(255,193,111,.07); }

    .operatorGrid { grid-template-rows:repeat(3,minmax(54px,1fr)) auto !important; gap:6px !important; }
    .operatorField { padding:7px 10px !important; border-radius:12px !important; }
    .operatorInput { padding:4px 0 2px !important; font-size:clamp(20px,5vw,27px) !important; }
    .operatorIntro { min-height:30px; }
    .operatorIntro div strong { font-size:14px; }
    .barCounter { grid-template-columns:34px 1fr 34px !important; }
    .barCounter button { height:34px !important; }
    .barCounter strong { font-size:23px !important; }

    .optionalBodyV11 { max-height:190px; overflow:auto; padding:0 9px 9px; }
    .trayTotalV11 { display:flex; align-items:center; justify-content:space-between; gap:10px; margin-bottom:7px; border-radius:10px; padding:9px 10px; color:#9fb4b9; background:rgba(0,0,0,.12); font-size:9px; font-weight:900; text-transform:uppercase; }
    .trayTotalV11 strong { color:#66dacc; font-size:18px; }
    .trayListV11 { display:grid; gap:7px; }
    .trayRowV11 { display:grid; grid-template-columns:auto minmax(0,1fr) 38px; align-items:center; gap:7px; }
    .trayRowV11 label { color:#88a0a7; font-size:10px; font-weight:900; }
    .trayRowV11 input { width:100%; height:42px; border:1px solid rgba(255,255,255,.11); border-radius:11px; padding:0 11px; color:#f1fbfa; background:rgba(255,255,255,.05); font-size:19px; font-weight:900; }
    .trayRowV11 button,.addTrayV11 { height:42px; border:1px solid rgba(255,255,255,.10); border-radius:11px; color:#b9cecf; background:rgba(255,255,255,.04); font-weight:900; }
    .addTrayV11 { width:100%; margin-top:7px; color:#66dacc; }

    .cockpitV11 { height:100%; min-height:0; display:grid; grid-template-rows:auto auto minmax(0,1fr); gap:8px; }
    .resultHeroV11 { border:1px solid rgba(255,255,255,.08); border-radius:17px; padding:12px 14px; background:linear-gradient(145deg,rgba(255,255,255,.07),rgba(255,255,255,.035)); }
    .resultHeroTopV11 { display:flex; align-items:center; justify-content:space-between; gap:10px; }
    .resultStatusV11 { border:1px solid currentColor; border-radius:999px; padding:6px 9px; color:#72ddd0; background:rgba(86,213,199,.07); font-size:9px; font-weight:950; letter-spacing:.08em; }
    .resultStatusV11.warn { color:#f1b75f; background:rgba(241,183,95,.07); }
    .resultStatusV11.bad { color:#ff9099; background:rgba(255,144,153,.07); }
    .resultHeroTopV11 small { color:#80999f; font-size:9px; font-weight:900; }
    .mainCountdownV11 { display:flex; align-items:baseline; margin-top:7px; color:#f4fdfc; font-family:"SFMono-Regular",Consolas,monospace; white-space:nowrap; }
    .mainCountdownV11 strong { font-size:clamp(31px,8vw,55px); line-height:.95; letter-spacing:-.08em; }
    .mainCountdownV11 small { color:#6ebdb4; font-size:12px; font-weight:900; }
    .opProgressV11 { margin-top:11px; }
    .opProgressLabelsV11 { display:flex; justify-content:space-between; color:#81999f; font-size:9px; font-weight:900; }
    .opProgressLabelsV11 strong { color:#eaf7f6; font-size:11px; }
    .opProgressTrackV11 { height:9px; margin-top:6px; overflow:hidden; border-radius:999px; background:rgba(255,255,255,.07); }
    .opProgressTrackV11 i { display:block; height:100%; border-radius:inherit; background:linear-gradient(90deg,#20a899,#66e0d1); transition:width .25s ease; }
    .primaryMetricsV11 { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:7px; }
    .metricV11 { min-width:0; border:1px solid rgba(255,255,255,.07); border-radius:13px; padding:9px 10px; background:rgba(255,255,255,.035); }
    .metricV11 span { display:block; color:#7e989f; font-size:8px; font-weight:950; letter-spacing:.08em; text-transform:uppercase; }
    .metricV11 strong { display:block; margin-top:5px; color:#eefafa; font-size:clamp(16px,4vw,23px); letter-spacing:-.045em; }
    .metricV11 small { display:block; margin-top:2px; color:#70a49e; font-size:8px; font-weight:800; }
    .resultDetailsV11 { min-height:0; overflow:auto; display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:7px; padding-bottom:2px; }
    .presetPanelV11 { grid-column:1/-1; border:1px solid rgba(242,184,100,.20); border-radius:14px; padding:10px; background:rgba(242,184,100,.055); }
    .presetTitleV11 { display:flex; align-items:center; justify-content:space-between; color:#efc27d; font-size:9px; font-weight:950; letter-spacing:.09em; text-transform:uppercase; }
    .presetChoicesV11 { display:flex; gap:6px; margin-top:8px; }
    .presetChoicesV11 button { flex:1; min-height:37px; border:1px solid rgba(255,255,255,.10); border-radius:10px; color:#b8cbce; background:rgba(255,255,255,.035); font-size:10px; font-weight:900; }
    .presetChoicesV11 button.active { color:#062824; background:#56d5c7; border-color:#56d5c7; }
    .presetFieldsV11 { display:grid; grid-template-columns:1fr 1fr; gap:7px; margin-top:7px; }
    .presetFieldsV11 input,.presetFieldsV11 select { width:100%; height:40px; border:1px solid rgba(255,255,255,.10); border-radius:10px; padding:0 10px; color:#effafa; background:#16242c; font-size:12px; font-weight:800; }

    @media(max-width:680px){
      .cellStatsV11 { grid-template-columns:repeat(3,minmax(0,1fr)); }
      .summaryGrid { display:none; }
      .primaryMetricsV11 { grid-template-columns:repeat(2,minmax(0,1fr)); }
      .resultDetailsV11 { grid-template-columns:repeat(2,minmax(0,1fr)); }
      .presetFieldsV11 { grid-template-columns:1fr; }
    }
    @media(max-height:690px){
      .resultHeroV11 { padding:8px 11px; }
      .mainCountdownV11 strong { font-size:34px; }
      .metricV11 { padding:7px 8px; }
      .operatorGrid { grid-template-rows:repeat(3,minmax(47px,1fr)) auto !important; }
    }
'''
text = text.replace('\n  </style>', css + '\n  </style>', 1)

js = r'''

    /* V11.0.01 — operações, resultados e preset em 16 horas */
    function trayTotalV11(machine) {
      return (Array.isArray(machine.trays) ? machine.trays : []).reduce((sum, value) => sum + Math.max(0, parseInteger(value)), 0);
    }

    function syncPastProductionV11(machine) {
      machine.producedManual = trayTotalV11(machine);
      return machine.producedManual;
    }

    function estimatedUntilShiftEndV11(machine, calc, now = Date.now()) {
      const cycleSeconds = parseTempoToSeconds(machine.timeInput);
      if (!Number.isFinite(cycleSeconds) || cycleSeconds <= 0) return 0;
      const currentEstimate = estimatedShiftProduction(machine, calc, now);
      const shift = getShiftWindowFor(new Date(now));
      const extra = Math.max(0, Math.floor((shift.endDT.getTime() - now) / (cycleSeconds * 1000)));
      const maximum = calc && calc.valid ? Math.max(0, Math.min(calc.remainingOP, calc.capacity)) : currentEstimate + extra;
      return Math.min(maximum, currentEstimate + extra);
    }

    function presetRequiredV11(calc) {
      return !!(calc && calc.valid && calc.restMin < 16 * 60);
    }

    function presetPendingV11(machine, calc) {
      if (!presetRequiredV11(calc)) return false;
      if (machine.presetMode === 'yes') return false;
      return !String(machine.itemCode || '').trim();
    }

    function formatAverageRestV11(minutes) {
      if (!Number.isFinite(minutes)) return '--:--';
      const total = Math.max(0, Math.round(minutes));
      return `${pad2(Math.floor(total / 60))}:${pad2(total % 60)}`;
    }

    function updateCellOverviewV11(calcs) {
      const total = state.machines.length;
      const calculated = calcs.filter(calc => calc.valid).length;
      const pending = total - calculated;
      const thisShift = calcs.filter(calc => calc.status === 'now' || calc.status === 'reached').length;
      const nextShift = calcs.filter(calc => calc.status === 'next').length;
      const presetPending = state.machines.reduce((sum, machine, index) => sum + (presetPendingV11(machine, calcs[index]) ? 1 : 0), 0);
      const validRests = calcs.filter(calc => calc.valid && Number.isFinite(calc.restMin)).map(calc => calc.restMin);
      const average = validRests.length ? validRests.reduce((a,b) => a+b, 0) / validRests.length : NaN;
      const progress = total ? (calculated / total) * 100 : 0;

      const set = (id, value) => { const node = document.querySelector(id); if (node) node.textContent = String(value); };
      set('#v11CellProgressText', `${calculated} de ${total} calculadas`);
      set('#v11Calculated', calculated);
      set('#v11Pending', pending);
      set('#v11ThisShift', thisShift);
      set('#v11NextShift', nextShift);
      set('#v11PresetPending', presetPending);
      set('#v11AverageRest', formatAverageRestV11(average));
      const bar = document.querySelector('#v11CellProgressBar'); if (bar) bar.style.width = `${progress}%`;
      const health = document.querySelector('#v11CellHealth');
      if (health) {
        health.className = `cellHealthV11 ${presetPending || thisShift ? 'bad' : pending ? 'warn' : ''}`.trim();
        health.textContent = presetPending || thisShift ? 'ATENÇÃO' : pending ? 'EM ANDAMENTO' : total ? 'SOB CONTROLE' : 'SEM DADOS';
      }
      const row = document.querySelector('#v11MachineProgress');
      if (row) {
        row.innerHTML = '';
        state.machines.forEach((machine, index) => {
          const button = document.createElement('button');
          const calc = calcs[index];
          button.type = 'button';
          button.className = `cellMachineDotV11 ${calc.valid ? 'done' : ''} ${presetPendingV11(machine, calc) ? 'attention' : ''}`.trim();
          button.textContent = formatTnl(machine.machine);
          button.addEventListener('click', () => openMachineScreen(machine.id));
          row.appendChild(button);
        });
      }
    }

    function updateSummary(calcs) {
      el.summaryTotal.textContent = String(state.machines.length);
      el.summaryBad.textContent = String(calcs.filter(calc => calc.status === 'now' || calc.status === 'reached').length);
      el.summaryWarn.textContent = String(calcs.filter(calc => calc.status === 'next').length);
      el.summaryOk.textContent = String(calcs.filter(calc => calc.status === 'ok' || calc.status === 'done').length);
      updateCellOverviewV11(calcs);
    }

    function renderMachineQueue() {
      machineQueue.innerHTML = '';
      state.machines.forEach(machine => {
        const button = document.createElement('button');
        const calc = calcMachine(machine);
        button.type = 'button';
        button.className = `queueMachine${machine.id === activeMachineId ? ' is-active' : ''}${calc.valid ? ' is-filled' : ''}${presetPendingV11(machine, calc) ? ' needs-preset' : ''}`;
        button.textContent = formatTnl(machine.machine);
        button.addEventListener('click', () => switchMachineScreen(machine.id));
        machineQueue.appendChild(button);
      });
    }

    function traysMarkupV11(machine) {
      return (Array.isArray(machine.trays) ? machine.trays : ['']).map((value,index) => `
        <div class="trayRowV11">
          <label>G${index + 1}</label>
          <input type="number" min="0" step="1" inputmode="numeric" data-v10-tray="${index}" value="${escapeHtml(String(value ?? ''))}" placeholder="Quantidade">
          <button type="button" data-v10-action="remove-tray" data-index="${index}" aria-label="Remover gabarito">×</button>
        </div>`).join('');
    }

    function renderPresetV11(machine, calc) {
      if (!presetRequiredV11(calc)) return '';
      const yes = machine.presetMode === 'yes';
      const request = calc.endDT ? `${fmtDate(calc.endDT)} às ${fmtTime(calc.endDT)}` : '-';
      return `<section class="presetPanelV11">
        <div class="presetTitleV11"><span>Próxima OP / preset</span><b>MENOS DE 16H</b></div>
        <div class="presetChoicesV11">
          <button type="button" data-v10-action="preset-mode" data-value="yes" class="${yes ? 'active' : ''}">Já trouxe</button>
          <button type="button" data-v10-action="preset-mode" data-value="no" class="${!yes ? 'active' : ''}">Ainda não trouxe</button>
        </div>
        ${yes ? `<div class="presetFieldsV11"><select data-v10-field="presetType"><option value="sequencia" ${machine.presetType==='sequencia'?'selected':''}>Sequência</option><option value="azul" ${machine.presetType==='azul'?'selected':''}>Setup azul</option><option value="verde" ${machine.presetType==='verde'?'selected':''}>Setup verde</option><option value="vermelho" ${machine.presetType==='vermelho'?'selected':''}>Setup vermelho</option></select></div>` : `<div class="presetFieldsV11"><input data-v10-field="itemCode" value="${escapeHtml(String(machine.itemCode || ''))}" placeholder="Item da próxima OP"><input value="Solicitar: ${request}" readonly></div>`}
      </section>`;
    }

    function renderMachineEditor(machine, calc) {
      syncPastProductionV11(machine);
      const piecesLabel = machine.barMode === 'partialMm' ? 'Milímetros restantes' : 'Peças restantes';
      const piecesValue = machine.barMode === 'partialMm' ? machine.partialMm : machine.partialPieces;
      const totalTrays = trayTotalV11(machine);
      machineScreenContent.innerHTML = `
        <section class="machineView operatorForm">
          <div class="operatorIntro"><div><span>Modo operador</span><strong>Preenchimento rápido</strong></div><span class="operatorModePill">ORDEM DA MÁQUINA</span></div>
          <div class="operatorGrid">
            <div class="operatorField cycleField"><label>1. Ciclo</label><input class="operatorInput" data-v10-field="timeInput" inputmode="decimal" value="${escapeHtml(String(machine.timeInput ?? ''))}" placeholder="2,24"></div>
            <div class="operatorField"><label>2. ${piecesLabel}</label><input class="operatorInput" data-v10-field="materialRemaining" inputmode="decimal" value="${escapeHtml(String(piecesValue ?? ''))}" placeholder="0"><div class="mpModeTabs"><button class="mpModeTab ${machine.barMode==='pieces'?'active':''}" data-v10-action="mp-mode" data-value="pieces" type="button">PEÇAS</button><button class="mpModeTab ${machine.barMode==='partialMm'?'active':''}" data-v10-action="mp-mode" data-value="partialMm" type="button">MM</button><button class="mpModeTab ${machine.barMode==='full'?'active':''}" data-v10-action="mp-mode" data-value="full" type="button">CHEIA</button></div></div>
            <div class="operatorField"><label>3. Meta da OP</label><input class="operatorInput" data-v10-field="target" inputmode="numeric" value="${escapeHtml(String(machine.target ?? ''))}" placeholder="1000"></div>
            <div class="operatorField"><label>4. Peça (mm)</label><input class="operatorInput" data-v10-field="pieceLength" inputmode="decimal" value="${escapeHtml(String(machine.pieceLength ?? ''))}" placeholder="32"></div>
            <div class="operatorField"><label>5. Barras</label><div class="barCounter"><button type="button" data-v10-action="bar-minus">−</button><strong>${parseInteger(machine.fullBars)}</strong><button type="button" data-v10-action="bar-plus">＋</button></div></div>
            <details class="optionalPanel" ${machine.traysCollapsed === false ? 'open' : ''}><summary>Gabaritos — opcional <b>${totalTrays}</b></summary><div class="optionalBodyV11"><div class="trayTotalV11"><span>Produção dos turnos passados</span><strong>${totalTrays}</strong></div><div class="trayListV11">${traysMarkupV11(machine)}</div><button class="addTrayV11" data-v10-action="add-tray" type="button">Adicionar gabarito</button></div></details>
            ${renderPresetV11(machine, calc)}
          </div>
        </section>`;
      machineScreenFooter.innerHTML = `<button class="machineFooterBtn" data-v10-action="previous" type="button" ${activeMachineIndex()<=0?'disabled':''}>${svgArrow(-1)} Anterior</button><button class="machineFooterBtn danger" data-v10-action="clear" type="button">Limpar dados</button><button class="machineFooterBtn primary" data-v10-action="save-next" type="button">Salvar e próxima ${svgArrow(1)}</button>`;
      bindMachineScreenEvents(machine);
    }

    function renderMachineResult(machine, calc) {
      const now = Date.now();
      const past = syncPastProductionV11(machine);
      const estimate = estimatedShiftProduction(machine, calc, now);
      const shiftEndEstimate = estimatedUntilShiftEndV11(machine, calc, now);
      const target = Math.max(0, parseInteger(machine.target));
      const currentTotal = Math.min(target || Infinity, past + estimate);
      const missing = Math.max(0, target - currentTotal);
      const progress = target ? Math.max(0, Math.min(100, currentTotal / target * 100)) : 0;
      const countdown = formatCountdownParts(calc.restMs);
      const cycleSeconds = parseTempoToSeconds(machine.timeInput);
      const decimalMinutes = Number.isFinite(cycleSeconds) ? cycleSeconds / 60 : NaN;
      const statusClass = calc.badgeClass === 'bad' ? 'bad' : calc.badgeClass === 'warn' ? 'warn' : '';
      const bars = Math.max(0, parseInteger(machine.fullBars));
      machineScreenContent.innerHTML = `
        <section class="machineView cockpitV11">
          <div class="resultHeroV11"><div class="resultHeroTopV11"><span class="resultStatusV11 ${statusClass}" data-v10-live="status">${escapeHtml(calc.statusText.toUpperCase())}</span><small>Tempo restante</small></div><div class="mainCountdownV11"><strong data-v10-live="countdown">${countdown.clock}</strong><small data-v10-live="milliseconds">.${countdown.milliseconds}</small></div><div class="opProgressV11"><div class="opProgressLabelsV11"><span>Progresso estimado da OP</span><strong data-v10-live="progress">${Math.round(progress)}%</strong></div><div class="opProgressTrackV11"><i data-v10-live="progress-bar" style="width:${progress}%"></i></div></div></div>
          <div class="primaryMetricsV11"><div class="metricV11"><span>Turnos passados</span><strong>${past}</strong><small>soma dos gabaritos</small></div><div class="metricV11"><span>Estimada até agora</span><strong data-v10-live="estimated">${estimate}</strong><small>nosso turno</small></div><div class="metricV11"><span>Até o fim do turno</span><strong data-v10-live="shift-end-estimated">${shiftEndEstimate}</strong><small>mantendo o ciclo</small></div><div class="metricV11"><span>Faltam</span><strong data-v10-live="missing">${missing}</strong><small>para a meta</small></div></div>
          <div class="resultDetailsV11"><div class="metricV11"><span>Meta da OP</span><strong>${target}</strong></div><div class="metricV11"><span>MP disponível</span><strong>${calc.capacity}</strong><small>peças possíveis</small></div><div class="metricV11"><span>Barras / peças por barra</span><strong>${bars} / ${calc.perBar || 0}</strong></div><div class="metricV11"><span>Ciclo informado</span><strong>${escapeHtml(String(machine.timeInput || '-'))}</strong></div><div class="metricV11"><span>Ciclo em segundos</span><strong>${Number.isFinite(cycleSeconds)?cycleSeconds.toFixed(0):'-'} s</strong></div><div class="metricV11"><span>Ciclo em minutos</span><strong>${Number.isFinite(decimalMinutes)?decimalMinutes.toFixed(4):'-'}</strong><small>fração decimal</small></div><div class="metricV11"><span>Produção por turno</span><strong>${calc.metaTurno || 0}</strong></div><div class="metricV11"><span>Previsão</span><strong>${fmtTime(calc.endDT)}</strong><small>${fmtDate(calc.endDT)} · ${shiftName(getShiftWindowFor(calc.endDT).id)}</small></div><div class="metricV11"><span>Cálculo iniciado</span><strong>${fmtTime(new Date(machine.calculationStartedAt))}</strong><small>${fmtDate(new Date(machine.calculationStartedAt))}</small></div>${renderPresetV11(machine, calc)}</div>
        </section>`;
      machineScreenFooter.innerHTML = `<button class="machineFooterBtn" data-v10-action="previous" type="button" ${activeMachineIndex()<=0?'disabled':''}>${svgArrow(-1)} Anterior</button><button class="machineFooterBtn" data-v10-action="edit" type="button">Editar dados</button><button class="machineFooterBtn primary" data-v10-action="next" type="button">Próxima máquina ${svgArrow(1)}</button>`;
      bindMachineScreenEvents(machine);
    }

    function bindMachineScreenEvents(machine) {
      machineScreenContent.querySelectorAll('[data-v10-field]').forEach(input => {
        input.addEventListener('input', () => {
          const field = input.dataset.v10Field;
          if (field === 'materialRemaining') {
            if (machine.barMode === 'partialMm') machine.partialMm = input.value; else machine.partialPieces = input.value;
          } else machine[field] = input.value;
          saveState();
        });
        input.addEventListener('change', () => { ensureExactStart(machine); saveState(); });
      });
      machineScreen.querySelectorAll('[data-v10-action]').forEach(button => { button.onclick = () => handleMachineScreenAction(button, machine); });
      machineScreenContent.querySelectorAll('[data-v10-tray]').forEach(input => {
        input.addEventListener('input', () => { machine.trays[Number(input.dataset.v10Tray)] = input.value; syncPastProductionV11(machine); saveState(); });
        input.addEventListener('change', () => { syncPastProductionV11(machine); saveState(); renderMachineScreen(); });
      });
      const details = machineScreenContent.querySelector('.optionalPanel');
      details?.addEventListener('toggle', () => { machine.traysCollapsed = !details.open; saveState(); });
    }

    function handleMachineScreenAction(button, machine) {
      const action = button.dataset.v10Action;
      if (action === 'previous') return navigateMachine(-1);
      if (action === 'next') return navigateMachine(1);
      if (action === 'edit') { machineScreenMode = 'edit'; return renderMachineScreen(); }
      if (action === 'save-next') { syncPastProductionV11(machine); ensureExactStart(machine); saveState(); render(); return navigateMachine(1, true); }
      if (action === 'clear') { if (!window.confirm(`Limpar os dados da TNL ${formatTnl(machine.machine)}?\n\nA máquina continuará na célula.`)) return; clearMachineData(machine); saveState(); render(); machineScreenMode='edit'; return renderMachineScreen(); }
      if (action === 'bar-minus' || action === 'bar-plus') { machine.fullBars = Math.max(0, parseInteger(machine.fullBars) + (action === 'bar-plus' ? 1 : -1)); saveState(); return renderMachineScreen(); }
      if (action === 'mp-mode') { machine.barMode = button.dataset.value; saveState(); return renderMachineScreen(); }
      if (action === 'add-tray') { machine.trays.push(''); machine.traysCollapsed=false; saveState(); return renderMachineScreen(); }
      if (action === 'remove-tray') { machine.trays.splice(Number(button.dataset.index),1); if(!machine.trays.length) machine.trays=['']; syncPastProductionV11(machine); saveState(); return renderMachineScreen(); }
      if (action === 'preset-mode') { machine.presetMode = button.dataset.value; saveState(); return renderMachineScreen(); }
    }

    function refreshMachineScreenLive() {
      if (!machineScreen?.open || machineScreenMode !== 'result') return;
      const machine = getActiveMachine(); if (!machine) return;
      syncPastProductionV11(machine);
      const calc = calcMachine(machine); if (!calc.valid) { machineScreenMode='edit'; return renderMachineScreen(); }
      const now = Date.now();
      const parts = formatCountdownParts(calc.restMs);
      const estimate = estimatedShiftProduction(machine, calc, now);
      const shiftEnd = estimatedUntilShiftEndV11(machine, calc, now);
      const target = Math.max(0, parseInteger(machine.target));
      const past = trayTotalV11(machine);
      const missing = Math.max(0, target - Math.min(target || Infinity, past + estimate));
      const progress = target ? Math.max(0, Math.min(100, (past + estimate) / target * 100)) : 0;
      const set = (selector,value) => { const node=machineScreenContent.querySelector(selector); if(node) node.textContent=String(value); };
      set('[data-v10-live="countdown"]',parts.clock); set('[data-v10-live="milliseconds"]',`.${parts.milliseconds}`); set('[data-v10-live="estimated"]',estimate); set('[data-v10-live="shift-end-estimated"]',shiftEnd); set('[data-v10-live="missing"]',missing); set('[data-v10-live="progress"]',`${Math.round(progress)}%`);
      const bar=machineScreenContent.querySelector('[data-v10-live="progress-bar"]'); if(bar) bar.style.width=`${progress}%`;
      const status=machineScreenContent.querySelector('[data-v10-live="status"]'); if(status){ status.textContent=calc.statusText.toUpperCase(); status.className=`resultStatusV11 ${calc.badgeClass==='bad'?'bad':calc.badgeClass==='warn'?'warn':''}`.trim(); }
    }
'''

last_script = text.rfind('</script>')
if last_script < 0:
    raise RuntimeError('Script final não encontrado')
text = text[:last_script] + js + '\n  ' + text[last_script:]

required = [
  'VENANC Tools V11.0.01', 'cellOverviewV11', 'function trayTotalV11',
  'Gabaritos — opcional', 'Produção dos turnos passados', 'Até o fim do turno',
  'function renderPresetV11', "calc.restMin < 16 * 60", 'Ciclo em minutos',
  'fração decimal', 'Preset pendente'
]
for token in required:
    if token not in text:
        raise RuntimeError(f'Ausente após aplicação: {token}')

path.write_bytes(text.replace('\n', newline).encode('utf-8'))
print('V11.0.01 aplicada com sucesso.')
