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


one('<title>Tempo da Linha | VENANC Tools V9.4</title>', '<title>Tempo da Linha | VENANC Tools V10</title>', 'versão')

v10_css = r'''

    /* V10 — cockpit de máquina em tela cheia */
    body.machine-screen-open { overflow:hidden; }
    .machineCard .cardBody { display:none !important; }
    .machineCard .cardHead { border-bottom:0; cursor:pointer; }
    .machineScreen {
      width:100vw; height:100dvh; max-width:none; max-height:none;
      margin:0; border:0; padding:0; overflow:hidden;
      color:#edf8f9; background:#091116;
    }
    .machineScreen::backdrop { background:rgba(0,7,11,.72); backdrop-filter:blur(8px); }
    .machineScreen[open] { animation:machineScreenIn .24s cubic-bezier(.2,.8,.2,1); }
    .machineScreenShell {
      height:100dvh; display:grid;
      grid-template-rows:auto auto minmax(0,1fr) auto;
      background:
        radial-gradient(circle at 85% -10%,rgba(86,213,199,.16),transparent 34%),
        linear-gradient(155deg,#0a141b,#101d25 58%,#0b151b);
    }
    .machineScreenTop {
      display:grid; grid-template-columns:auto minmax(0,1fr) auto; align-items:center; gap:12px;
      padding:max(12px,env(safe-area-inset-top)) 14px 10px;
      border-bottom:1px solid rgba(255,255,255,.08);
      background:rgba(8,15,20,.76); backdrop-filter:blur(18px);
    }
    .machineScreenClose,.machineScreenIconBtn {
      width:42px; height:42px; display:grid; place-items:center; border:1px solid rgba(255,255,255,.11);
      border-radius:13px; padding:0; color:#eaf8f8; background:rgba(255,255,255,.055);
    }
    .machineScreenClose svg,.machineScreenIconBtn svg { width:20px; height:20px; stroke:currentColor; fill:none; stroke-width:2; }
    .machineScreenHeading { min-width:0; text-align:center; }
    .machineScreenHeading span { display:block; color:#8ea8af; font-size:10px; font-weight:900; letter-spacing:.14em; }
    .machineScreenHeading strong { display:block; margin-top:2px; color:#f3fbfb; font-size:24px; letter-spacing:-.055em; }
    .machineScreenHeading small { display:block; margin-top:2px; color:#72d9cc; font-size:11px; font-weight:850; }
    .machineQueue {
      display:flex; align-items:center; gap:7px; overflow-x:auto; scrollbar-width:none;
      padding:8px 12px; border-bottom:1px solid rgba(255,255,255,.07); background:rgba(255,255,255,.025);
    }
    .machineQueue::-webkit-scrollbar { display:none; }
    .queueMachine {
      flex:0 0 auto; min-width:45px; height:34px; border:1px solid rgba(255,255,255,.09); border-radius:10px;
      color:#9eb4ba; background:rgba(255,255,255,.035); font-size:11px; font-weight:950;
      transition:transform .18s ease,background .18s ease,border-color .18s ease,color .18s ease;
    }
    .queueMachine.is-filled { color:#91e4d9; border-color:rgba(86,213,199,.24); }
    .queueMachine.is-active { transform:translateY(-1px); color:#062824; background:#56d5c7; border-color:#56d5c7; box-shadow:0 8px 22px rgba(86,213,199,.20); }
    .machineScreenContent { min-height:0; overflow:hidden; padding:10px 12px; }
    .machineView { height:100%; min-height:0; }
    .machineViewSwap { animation:machineViewIn .22s cubic-bezier(.2,.8,.2,1); }

    .operatorForm {
      height:100%; display:grid; grid-template-rows:auto minmax(0,1fr); gap:8px;
    }
    .operatorIntro { display:flex; align-items:center; justify-content:space-between; gap:10px; }
    .operatorIntro div span { display:block; color:#7f9aa2; font-size:9px; font-weight:950; letter-spacing:.13em; text-transform:uppercase; }
    .operatorIntro div strong { display:block; margin-top:3px; color:#e9f7f7; font-size:16px; }
    .operatorModePill { border:1px solid rgba(86,213,199,.22); border-radius:999px; padding:6px 9px; color:#75ded1; background:rgba(86,213,199,.07); font-size:9px; font-weight:950; letter-spacing:.08em; }
    .operatorGrid {
      min-height:0; display:grid; grid-template-columns:repeat(2,minmax(0,1fr));
      grid-template-rows:repeat(3,minmax(72px,1fr)) auto; gap:8px;
    }
    .operatorField {
      min-width:0; display:flex; flex-direction:column; justify-content:center;
      border:1px solid rgba(255,255,255,.09); border-radius:15px; padding:10px 12px;
      background:linear-gradient(145deg,rgba(255,255,255,.065),rgba(255,255,255,.035));
      box-shadow:inset 0 1px 0 rgba(255,255,255,.035);
    }
    .operatorField.cycleField { grid-column:1/-1; }
    .operatorField label { color:#8ea5ac; font-size:9px; font-weight:950; letter-spacing:.12em; text-transform:uppercase; }
    .operatorInput {
      width:100%; min-width:0; border:0; border-bottom:1px solid rgba(255,255,255,.13); border-radius:0;
      padding:7px 0 4px; color:#f4fbfb; outline:none; background:transparent;
      font-size:clamp(24px,6vw,34px); font-weight:950; letter-spacing:-.055em; font-variant-numeric:tabular-nums;
    }
    .operatorInput:focus { border-bottom-color:#56d5c7; box-shadow:0 7px 0 -6px rgba(86,213,199,.55); }
    .mpModeTabs { display:flex; gap:5px; margin-top:7px; }
    .mpModeTab { flex:1; min-height:25px; border:1px solid rgba(255,255,255,.08); border-radius:8px; color:#829ca3; background:rgba(255,255,255,.025); font-size:8px; font-weight:900; }
    .mpModeTab.active { color:#062824; background:#56d5c7; border-color:#56d5c7; }
    .barCounter { display:grid; grid-template-columns:39px 1fr 39px; align-items:center; gap:7px; margin-top:5px; }
    .barCounter button { height:39px; border:1px solid rgba(255,255,255,.10); border-radius:11px; color:#dff5f3; background:rgba(255,255,255,.055); font-size:22px; }
    .barCounter strong { text-align:center; color:#f4fbfb; font-size:28px; }
    .optionalPanel { grid-column:1/-1; min-height:44px; border:1px solid rgba(255,255,255,.08); border-radius:13px; background:rgba(255,255,255,.035); overflow:hidden; }
    .optionalPanel summary { min-height:44px; display:flex; align-items:center; justify-content:space-between; padding:0 12px; color:#b6c9ce; cursor:pointer; list-style:none; font-size:10px; font-weight:950; letter-spacing:.08em; text-transform:uppercase; }
    .optionalPanel summary::-webkit-details-marker { display:none; }
    .optionalPanel summary b { color:#56d5c7; font-size:15px; }
    .optionalBody { max-height:118px; overflow:auto; display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:6px; padding:0 9px 9px; }
    .trayCompactRow { display:grid; grid-template-columns:1fr 32px; gap:5px; }
    .trayCompactRow input { min-width:0; height:36px; border:1px solid rgba(255,255,255,.10); border-radius:9px; padding:0 9px; color:#effafa; background:rgba(255,255,255,.045); font-size:16px; font-weight:850; }
    .trayCompactRow button,.addTrayCompact { height:36px; border:1px solid rgba(255,255,255,.09); border-radius:9px; color:#b7cdcf; background:rgba(255,255,255,.04); font-weight:900; }
    .addTrayCompact { grid-column:1/-1; color:#62d7ca; }

    .cockpit {
      height:100%; min-height:0; display:grid;
      grid-template-columns:minmax(0,1.18fr) minmax(0,.82fr); grid-template-rows:minmax(0,1fr); gap:9px;
    }
    .cockpitHero,.cockpitPanel { border:1px solid rgba(255,255,255,.09); border-radius:18px; background:linear-gradient(145deg,rgba(255,255,255,.07),rgba(255,255,255,.035)); }
    .cockpitHero { min-height:0; display:flex; flex-direction:column; align-items:center; justify-content:center; padding:14px; text-align:center; overflow:hidden; position:relative; }
    .cockpitHero::after { content:""; position:absolute; width:220px; height:220px; border-radius:50%; background:radial-gradient(circle,rgba(86,213,199,.12),transparent 67%); pointer-events:none; }
    .cockpitStatus { position:relative; z-index:1; border:1px solid currentColor; border-radius:999px; padding:6px 10px; color:#77ded2; background:rgba(86,213,199,.07); font-size:9px; font-weight:950; letter-spacing:.09em; }
    .cockpitStatus.warn { color:#f2b864; background:rgba(242,184,100,.07); }
    .cockpitStatus.bad { color:#ff8b94; background:rgba(255,139,148,.07); }
    .cockpitLabel { position:relative; z-index:1; margin-top:14px; color:#839fa6; font-size:9px; font-weight:950; letter-spacing:.14em; text-transform:uppercase; }
    .cockpitCountdown { position:relative; z-index:1; display:flex; align-items:baseline; margin-top:5px; color:#f4fdfc; font-family:"SFMono-Regular",Consolas,monospace; font-variant-numeric:tabular-nums; white-space:nowrap; }
    .cockpitCountdown strong { font-size:clamp(34px,9vw,68px); letter-spacing:-.085em; line-height:.96; }
    .cockpitCountdown small { min-width:45px; color:#72bdb5; font-size:13px; font-weight:900; }
    .progressRing { --progress:0; position:relative; z-index:1; width:92px; aspect-ratio:1; margin-top:13px; display:grid; place-items:center; border-radius:50%; background:conic-gradient(#56d5c7 calc(var(--progress)*1%),rgba(255,255,255,.08) 0); }
    .progressRing::before { content:""; position:absolute; inset:7px; border-radius:50%; background:#101b22; }
    .progressRing strong { position:relative; color:#f0fbfa; font-size:20px; }
    .progressRing span { position:absolute; top:61%; color:#76939a; font-size:7px; font-weight:900; letter-spacing:.09em; }
    .cockpitSide { min-height:0; display:grid; grid-template-rows:repeat(3,minmax(0,1fr)); gap:8px; }
    .cockpitPanel { min-height:0; display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:7px; padding:10px; }
    .cockpitPanel.full { grid-template-columns:1fr; }
    .cockpitMetric { min-width:0; display:flex; flex-direction:column; justify-content:center; border-radius:12px; padding:8px 9px; background:rgba(0,0,0,.12); }
    .cockpitMetric span { color:#7f989f; font-size:8px; font-weight:950; letter-spacing:.09em; text-transform:uppercase; }
    .cockpitMetric strong { margin-top:5px; color:#edf9f8; font-size:clamp(15px,3.8vw,24px); letter-spacing:-.045em; overflow-wrap:anywhere; }
    .cockpitMetric small { margin-top:3px; color:#6fa79f; font-size:9px; font-weight:800; }

    .machineScreenFooter {
      display:grid; grid-template-columns:auto minmax(0,1fr) auto; gap:8px;
      padding:9px 12px max(9px,env(safe-area-inset-bottom)); border-top:1px solid rgba(255,255,255,.08);
      background:rgba(8,15,20,.88); backdrop-filter:blur(18px);
    }
    .machineFooterBtn { min-height:46px; border:1px solid rgba(255,255,255,.10); border-radius:13px; padding:0 13px; color:#dceced; background:rgba(255,255,255,.055); font-size:11px; font-weight:950; }
    .machineFooterBtn.primary { color:#052a25; background:#56d5c7; border-color:#56d5c7; box-shadow:0 10px 24px rgba(86,213,199,.18); }
    .machineFooterBtn.danger { color:#ff9ba3; border-color:rgba(255,120,130,.22); }
    .machineFooterBtn:disabled { opacity:.35; }

    @keyframes machineScreenIn { from { opacity:0; transform:scale(.985); } to { opacity:1; transform:scale(1); } }
    @keyframes machineViewIn { from { opacity:0; transform:translateX(18px); } to { opacity:1; transform:translateX(0); } }
    @keyframes metricPop { 50% { transform:translateY(-2px); color:#56d5c7; } }
    .metricPop { animation:metricPop .22s ease; }
    @media (max-width:680px) {
      .machineScreenTop { padding-left:10px; padding-right:10px; }
      .machineScreenContent { padding:8px; }
      .operatorGrid { gap:6px; grid-template-rows:repeat(3,minmax(64px,1fr)) auto; }
      .operatorField { padding:8px 10px; border-radius:13px; }
      .operatorInput { font-size:26px; }
      .cockpit { grid-template-columns:1fr; grid-template-rows:minmax(0,1.05fr) minmax(0,.95fr); gap:7px; }
      .cockpitSide { grid-template-columns:repeat(3,minmax(0,1fr)); grid-template-rows:1fr; gap:6px; }
      .cockpitPanel { grid-template-columns:1fr; gap:4px; padding:6px; border-radius:13px; }
      .cockpitPanel.full { grid-template-columns:1fr; }
      .cockpitMetric { padding:5px 7px; border-radius:9px; }
      .cockpitMetric span { font-size:7px; }
      .cockpitMetric strong { margin-top:3px; font-size:14px; }
      .cockpitMetric small { font-size:7px; }
      .cockpitCountdown strong { font-size:clamp(30px,10.8vw,48px); }
      .progressRing { width:76px; margin-top:8px; }
      .progressRing strong { font-size:17px; }
      .cockpitLabel { margin-top:9px; }
      .machineFooterBtn { min-height:43px; padding:0 9px; font-size:10px; }
    }
    @media (max-height:690px) {
      .machineQueue { padding-top:5px; padding-bottom:5px; }
      .queueMachine { height:29px; }
      .machineScreenContent { padding-top:6px; padding-bottom:6px; }
      .operatorGrid { grid-template-rows:repeat(3,minmax(55px,1fr)) auto; }
      .operatorIntro { display:none; }
      .cockpitLabel { margin-top:7px; }
      .progressRing { width:66px; }
    }
    @media (prefers-reduced-motion:reduce) {
      .machineScreen[open],.machineViewSwap,.metricPop { animation:none !important; }
      *,*::before,*::after { scroll-behavior:auto !important; transition-duration:.01ms !important; }
    }
'''
one('  </style>', v10_css + '\n  </style>', 'CSS V10')

v10_dialog = r'''
  <dialog id="machineScreen" class="machineScreen" aria-label="Máquina em tela cheia">
    <div class="machineScreenShell">
      <header class="machineScreenTop">
        <button class="machineScreenClose" id="machineScreenClose" type="button" aria-label="Fechar">
          <svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></svg>
        </button>
        <div class="machineScreenHeading">
          <span id="machineScreenCell">CÉLULA --</span>
          <strong id="machineScreenTitle">TNL ---</strong>
          <small id="machineScreenPosition">0 de 0</small>
        </div>
        <button class="machineScreenIconBtn" id="machineScreenMode" type="button" aria-label="Alternar edição e resultado">
          <svg viewBox="0 0 24 24"><path d="M4 20h4l11-11-4-4L4 16v4zM13.5 6.5l4 4"/></svg>
        </button>
      </header>
      <nav class="machineQueue" id="machineQueue" aria-label="Máquinas da célula"></nav>
      <div class="machineScreenContent" id="machineScreenContent"></div>
      <footer class="machineScreenFooter" id="machineScreenFooter"></footer>
    </div>
  </dialog>

'''
one('  <dialog id="settingsModal">', v10_dialog + '  <dialog id="settingsModal">', 'dialog V10')

one(
'''      node.querySelector(".cardHead").addEventListener("click", event => {
        if (event.target.closest("button")) return;
        machine.collapsed = !machine.collapsed;
        render();
      });''',
'''      node.querySelector(".cardHead").addEventListener("click", event => {
        if (event.target.closest("button")) return;
        openMachineScreen(machine.id);
      });''',
'abrir card em tela cheia'
)

one(
'''      root.querySelector('[data-action="toggle"]').addEventListener("click", () => {
        machine.collapsed = !machine.collapsed;
        render();
      });''',
'''      root.querySelector('[data-action="toggle"]').addEventListener("click", () => {
        openMachineScreen(machine.id);
      });''',
'botão abrir tela cheia'
)

one(
'''      updateSummary(calcs);
      el.baseShift.textContent = shiftName(getShiftWindowFor(new Date()).id);
    }

    let liveRenderTimer = null;''',
'''      updateSummary(calcs);
      el.baseShift.textContent = shiftName(getShiftWindowFor(new Date()).id);
      refreshMachineScreenLive();
    }

    let liveRenderTimer = null;''',
'atualização do cockpit'
)

v10_js = r'''

    /* V10 — tela de operador e cockpit */
    const machineScreen = document.querySelector("#machineScreen");
    const machineScreenContent = document.querySelector("#machineScreenContent");
    const machineScreenFooter = document.querySelector("#machineScreenFooter");
    const machineQueue = document.querySelector("#machineQueue");
    let activeMachineId = null;
    let machineScreenMode = "edit";

    function machineHasPrimaryData(machine) {
      return !!String(machine.timeInput || "").trim()
        || !!String(machine.target || "").trim()
        || !!String(machine.pieceLength || "").trim()
        || !!String(machine.partialPieces || "").trim()
        || parseInteger(machine.fullBars) > 0;
    }

    function getActiveMachine() {
      return state.machines.find(machine => machine.id === activeMachineId) || null;
    }

    function activeMachineIndex() {
      return state.machines.findIndex(machine => machine.id === activeMachineId);
    }

    function svgArrow(direction) {
      return direction < 0
        ? '<svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 18l-6-6 6-6"/></svg>'
        : '<svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg>';
    }

    function openMachineScreen(machineId, requestedMode = null) {
      const machine = state.machines.find(item => item.id === machineId);
      if (!machine) return;
      activeMachineId = machineId;
      const calc = calcMachine(machine);
      machineScreenMode = requestedMode || (calc.valid ? "result" : "edit");
      renderMachineScreen();
      if (!machineScreen.open) machineScreen.showModal();
      document.body.classList.add("machine-screen-open");
      requestAnimationFrame(() => {
        machineQueue.querySelector('.queueMachine.is-active')?.scrollIntoView({ behavior:"smooth", inline:"center", block:"nearest" });
        if (machineScreenMode === "edit") machineScreenContent.querySelector('[data-v10-field="timeInput"]')?.focus({ preventScroll:true });
      });
    }

    function closeMachineScreen() {
      if (machineScreen.open) machineScreen.close();
      document.body.classList.remove("machine-screen-open");
      activeMachineId = null;
      render();
    }

    function renderMachineQueue() {
      machineQueue.innerHTML = "";
      state.machines.forEach(machine => {
        const button = document.createElement("button");
        const calc = calcMachine(machine);
        button.type = "button";
        button.className = `queueMachine${machine.id === activeMachineId ? " is-active" : ""}${calc.valid ? " is-filled" : ""}`;
        button.textContent = formatTnl(machine.machine);
        button.addEventListener("click", () => switchMachineScreen(machine.id));
        machineQueue.appendChild(button);
      });
    }

    function renderMachineScreen() {
      const machine = getActiveMachine();
      if (!machine) return closeMachineScreen();
      const index = activeMachineIndex();
      const calc = calcMachine(machine);
      document.querySelector("#machineScreenCell").textContent = `CÉLULA ${state.selectedCell || "--"}`;
      document.querySelector("#machineScreenTitle").textContent = `TNL ${formatTnl(machine.machine)}`;
      document.querySelector("#machineScreenPosition").textContent = `${index + 1} de ${state.machines.length}`;
      document.querySelector("#machineScreenMode").style.visibility = calc.valid ? "visible" : "hidden";
      renderMachineQueue();
      if (machineScreenMode === "result" && calc.valid) renderMachineResult(machine, calc);
      else {
        machineScreenMode = "edit";
        renderMachineEditor(machine, calc);
      }
      machineScreenContent.firstElementChild?.classList.add("machineViewSwap");
    }

    function renderMachineEditor(machine, calc) {
      const piecesLabel = machine.barMode === "partialMm" ? "Milímetros restantes" : "Peças restantes";
      const piecesValue = machine.barMode === "partialMm" ? machine.partialMm : machine.partialPieces;
      const trayCount = machine.trays.filter(value => String(value || "").trim()).length;
      const trays = machine.trays.map((value, index) => `
        <div class="trayCompactRow">
          <input type="number" min="0" step="1" inputmode="numeric" data-v10-tray="${index}" value="${escapeHtml(String(value ?? ""))}" placeholder="Quantidade">
          <button type="button" data-v10-action="remove-tray" data-index="${index}" aria-label="Remover">×</button>
        </div>`).join("");

      machineScreenContent.innerHTML = `
        <section class="machineView operatorForm">
          <div class="operatorIntro"><div><span>Modo operador</span><strong>Preenchimento rápido</strong></div><span class="operatorModePill">ORDEM DA MÁQUINA</span></div>
          <div class="operatorGrid">
            <div class="operatorField cycleField"><label>1. Ciclo</label><input class="operatorInput" data-v10-field="timeInput" inputmode="decimal" value="${escapeHtml(String(machine.timeInput ?? ""))}" placeholder="2,24"></div>
            <div class="operatorField"><label>2. ${piecesLabel}</label><input class="operatorInput" data-v10-field="materialRemaining" inputmode="decimal" value="${escapeHtml(String(piecesValue ?? ""))}" placeholder="0">
              <div class="mpModeTabs">
                <button class="mpModeTab ${machine.barMode === "pieces" ? "active" : ""}" data-v10-action="mp-mode" data-value="pieces" type="button">PEÇAS</button>
                <button class="mpModeTab ${machine.barMode === "partialMm" ? "active" : ""}" data-v10-action="mp-mode" data-value="partialMm" type="button">MM</button>
                <button class="mpModeTab ${machine.barMode === "full" ? "active" : ""}" data-v10-action="mp-mode" data-value="full" type="button">CHEIA</button>
              </div>
            </div>
            <div class="operatorField"><label>3. Meta da OP</label><input class="operatorInput" data-v10-field="target" inputmode="numeric" value="${escapeHtml(String(machine.target ?? ""))}" placeholder="1000"></div>
            <div class="operatorField"><label>4. Peça (mm)</label><input class="operatorInput" data-v10-field="pieceLength" inputmode="decimal" value="${escapeHtml(String(machine.pieceLength ?? ""))}" placeholder="32"></div>
            <div class="operatorField"><label>5. Barras</label><div class="barCounter"><button type="button" data-v10-action="bar-minus">−</button><strong data-v10-role="bar-count">${parseInteger(machine.fullBars)}</strong><button type="button" data-v10-action="bar-plus">＋</button></div></div>
            <details class="optionalPanel" ${machine.traysCollapsed === false ? "open" : ""}><summary>Gabaritos — opcional <b>${trayCount}</b></summary><div class="optionalBody">${trays}<button class="addTrayCompact" data-v10-action="add-tray" type="button">Adicionar gabarito</button></div></details>
          </div>
        </section>`;

      machineScreenFooter.innerHTML = `
        <button class="machineFooterBtn" data-v10-action="previous" type="button" ${activeMachineIndex() <= 0 ? "disabled" : ""}>${svgArrow(-1)} Anterior</button>
        <button class="machineFooterBtn danger" data-v10-action="clear" type="button">Limpar dados</button>
        <button class="machineFooterBtn primary" data-v10-action="save-next" type="button">Salvar e próxima ${svgArrow(1)}</button>`;
      bindMachineScreenEvents(machine);
    }

    function estimatedShiftProduction(machine, calc, now = Date.now()) {
      const cycleSeconds = parseTempoToSeconds(machine.timeInput);
      const started = Number(machine.calculationStartedAt);
      if (!Number.isFinite(cycleSeconds) || cycleSeconds <= 0 || !Number.isFinite(started) || started <= 0) return 0;
      const raw = Math.max(0, Math.floor((now - started) / (cycleSeconds * 1000)));
      const limit = calc && calc.valid ? Math.max(0, Math.min(calc.remainingOP, calc.capacity)) : raw;
      return Math.min(raw, limit);
    }

    function formatElapsed(ms) {
      const parts = formatCountdownParts(Math.max(0, ms));
      return `${parts.clock}.${parts.milliseconds}`;
    }

    function cycleConverted(machine) {
      const seconds = parseTempoToSeconds(machine.timeInput);
      if (!Number.isFinite(seconds)) return "--:--:--.---";
      return formatElapsed(seconds * 1000);
    }

    function resultProgress(machine, calc, estimate) {
      const target = Math.max(0, parseInteger(machine.target));
      const past = Math.max(0, parseInteger(machine.producedManual));
      if (!target) return 0;
      return Math.max(0, Math.min(100, ((past + estimate) / target) * 100));
    }

    function renderMachineResult(machine, calc) {
      const now = Date.now();
      const estimate = estimatedShiftProduction(machine, calc, now);
      const progress = resultProgress(machine, calc, estimate);
      const countdown = formatCountdownParts(calc.restMs);
      const elapsed = formatElapsed(now - Number(machine.calculationStartedAt || now));
      const statusClass = calc.badgeClass === "bad" ? "bad" : calc.badgeClass === "warn" ? "warn" : "";

      machineScreenContent.innerHTML = `
        <section class="machineView cockpit">
          <div class="cockpitHero">
            <span class="cockpitStatus ${statusClass}" data-v10-live="status">${escapeHtml(calc.statusText.toUpperCase())}</span>
            <span class="cockpitLabel">Tempo restante</span>
            <div class="cockpitCountdown"><strong data-v10-live="countdown">${countdown.clock}</strong><small data-v10-live="milliseconds">.${countdown.milliseconds}</small></div>
            <div class="progressRing" data-v10-live="progress-ring" style="--progress:${progress.toFixed(2)}"><strong data-v10-live="progress">${Math.round(progress)}%</strong><span>DA OP</span></div>
          </div>
          <div class="cockpitSide">
            <div class="cockpitPanel">
              <div class="cockpitMetric"><span>Turnos passados</span><strong>${Math.max(0,parseInteger(machine.producedManual))}</strong></div>
              <div class="cockpitMetric"><span>Estimada do turno</span><strong data-v10-live="estimated">${estimate}</strong><small>desde o cálculo</small></div>
            </div>
            <div class="cockpitPanel">
              <div class="cockpitMetric"><span>Meta da OP</span><strong>${Math.max(0,parseInteger(machine.target))}</strong></div>
              <div class="cockpitMetric"><span>Produção por turno</span><strong>${calc.metaTurno || 0}</strong><small>peças em 8 horas</small></div>
            </div>
            <div class="cockpitPanel">
              <div class="cockpitMetric"><span>Tempo de ciclo</span><strong>${escapeHtml(String(machine.timeInput || "-"))}</strong></div>
              <div class="cockpitMetric"><span>Ciclo convertido</span><strong>${cycleConverted(machine)}</strong></div>
              <div class="cockpitMetric"><span>Rodando há</span><strong data-v10-live="elapsed">${elapsed}</strong></div>
              <div class="cockpitMetric"><span>Previsão</span><strong>${fmtDate(calc.endDT)}</strong><small>${fmtTime(calc.endDT)} · ${shiftName(getShiftWindowFor(calc.endDT).id)}</small></div>
              <div class="cockpitMetric" style="grid-column:1/-1"><span>Cálculo iniciado</span><strong>${fmtExactDateTime(machine.calculationStartedAt)}</strong></div>
            </div>
          </div>
        </section>`;

      machineScreenFooter.innerHTML = `
        <button class="machineFooterBtn" data-v10-action="previous" type="button" ${activeMachineIndex() <= 0 ? "disabled" : ""}>${svgArrow(-1)} Anterior</button>
        <button class="machineFooterBtn" data-v10-action="edit" type="button">Editar dados</button>
        <button class="machineFooterBtn primary" data-v10-action="next" type="button">Próxima máquina ${svgArrow(1)}</button>`;
      bindMachineScreenEvents(machine);
    }

    function escapeHtml(value) {
      return String(value).replace(/[&<>'"]/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;","'":"&#39;",'"':"&quot;"}[char]));
    }

    function ensureExactStart(machine) {
      let calc = calcMachine(machine);
      if (calc.valid && !machine.calculationStartedAt) {
        const exactStart = Date.now();
        machine.calculationStartedAt = exactStart;
        machine.baseTimestamp = exactStart;
        calc = calcMachine(machine);
      }
      return calc;
    }

    function bindMachineScreenEvents(machine) {
      machineScreenContent.querySelectorAll("[data-v10-field]").forEach(input => {
        input.addEventListener("input", () => {
          const field = input.dataset.v10Field;
          if (field === "materialRemaining") {
            if (machine.barMode === "partialMm") machine.partialMm = input.value;
            else machine.partialPieces = input.value;
          } else machine[field] = input.value;
          saveState();
        });
        input.addEventListener("change", () => {
          ensureExactStart(machine);
          saveState();
        });
      });
      machineScreen.querySelectorAll("[data-v10-action]").forEach(button => {
        button.onclick = () => handleMachineScreenAction(button, machine);
      });
      machineScreenContent.querySelectorAll("[data-v10-tray]").forEach(input => {
        input.addEventListener("input", () => {
          machine.trays[Number(input.dataset.v10Tray)] = input.value;
          saveState();
        });
      });
      const details = machineScreenContent.querySelector(".optionalPanel");
      details?.addEventListener("toggle", () => {
        machine.traysCollapsed = !details.open;
        saveState();
      });
    }

    function handleMachineScreenAction(button, machine) {
      const action = button.dataset.v10Action;
      if (action === "previous") return navigateMachine(-1);
      if (action === "next") return navigateMachine(1);
      if (action === "edit") { machineScreenMode = "edit"; return renderMachineScreen(); }
      if (action === "save-next") {
        ensureExactStart(machine); saveState(); render(); return navigateMachine(1, true);
      }
      if (action === "clear") {
        if (!window.confirm(`Limpar os dados da TNL ${formatTnl(machine.machine)}?\n\nA máquina continuará na célula.`)) return;
        clearMachineData(machine); saveState(); render(); machineScreenMode = "edit"; return renderMachineScreen();
      }
      if (action === "bar-minus" || action === "bar-plus") {
        machine.fullBars = Math.max(0, parseInteger(machine.fullBars) + (action === "bar-plus" ? 1 : -1));
        saveState(); return renderMachineScreen();
      }
      if (action === "mp-mode") {
        machine.barMode = button.dataset.value;
        saveState(); return renderMachineScreen();
      }
      if (action === "add-tray") {
        machine.trays.push(""); machine.traysCollapsed = false; saveState(); return renderMachineScreen();
      }
      if (action === "remove-tray") {
        machine.trays.splice(Number(button.dataset.index),1);
        if (!machine.trays.length) machine.trays = [""];
        saveState(); return renderMachineScreen();
      }
    }

    function navigateMachine(direction, forceEdit = false) {
      const current = activeMachineIndex();
      const nextIndex = current + direction;
      if (nextIndex < 0 || nextIndex >= state.machines.length) {
        if (direction > 0) return closeMachineScreen();
        return;
      }
      const nextMachine = state.machines[nextIndex];
      activeMachineId = nextMachine.id;
      const calc = calcMachine(nextMachine);
      machineScreenMode = forceEdit ? (calc.valid ? "result" : "edit") : (calc.valid ? "result" : "edit");
      animateMachineSwap(direction, renderMachineScreen);
      requestAnimationFrame(() => machineQueue.querySelector('.queueMachine.is-active')?.scrollIntoView({ behavior:"smooth", inline:"center", block:"nearest" }));
    }

    function switchMachineScreen(machineId) {
      const oldIndex = activeMachineIndex();
      const newIndex = state.machines.findIndex(machine => machine.id === machineId);
      if (newIndex < 0 || newIndex === oldIndex) return;
      activeMachineId = machineId;
      machineScreenMode = calcMachine(state.machines[newIndex]).valid ? "result" : "edit";
      animateMachineSwap(newIndex > oldIndex ? 1 : -1, renderMachineScreen);
    }

    function animateMachineSwap(direction, update) {
      const current = machineScreenContent.firstElementChild;
      if (!current || typeof current.animate !== "function" || matchMedia('(prefers-reduced-motion: reduce)').matches) return update();
      current.animate([{opacity:1,transform:"translateX(0)"},{opacity:0,transform:`translateX(${direction < 0 ? 20 : -20}px)`}],{duration:120,easing:"ease-in",fill:"forwards"}).finished
        .then(() => update()).catch(() => update());
    }

    function animateNumber(element, value) {
      if (!element || element.textContent === String(value)) return;
      element.textContent = String(value);
      element.classList.remove("metricPop");
      void element.offsetWidth;
      element.classList.add("metricPop");
    }

    function refreshMachineScreenLive() {
      if (!machineScreen?.open || machineScreenMode !== "result") return;
      const machine = getActiveMachine();
      if (!machine) return;
      const calc = calcMachine(machine);
      if (!calc.valid) { machineScreenMode = "edit"; return renderMachineScreen(); }
      const now = Date.now();
      const parts = formatCountdownParts(calc.restMs);
      const estimate = estimatedShiftProduction(machine, calc, now);
      const progress = resultProgress(machine, calc, estimate);
      const clock = machineScreenContent.querySelector('[data-v10-live="countdown"]');
      const ms = machineScreenContent.querySelector('[data-v10-live="milliseconds"]');
      if (clock) clock.textContent = parts.clock;
      if (ms) ms.textContent = `.${parts.milliseconds}`;
      animateNumber(machineScreenContent.querySelector('[data-v10-live="estimated"]'), estimate);
      const elapsed = machineScreenContent.querySelector('[data-v10-live="elapsed"]');
      if (elapsed) elapsed.textContent = formatElapsed(now - Number(machine.calculationStartedAt || now));
      const progressText = machineScreenContent.querySelector('[data-v10-live="progress"]');
      if (progressText) progressText.textContent = `${Math.round(progress)}%`;
      const ring = machineScreenContent.querySelector('[data-v10-live="progress-ring"]');
      if (ring) ring.style.setProperty("--progress", progress.toFixed(2));
      const status = machineScreenContent.querySelector('[data-v10-live="status"]');
      if (status && status.textContent !== calc.statusText.toUpperCase()) {
        status.textContent = calc.statusText.toUpperCase();
        status.className = `cockpitStatus ${calc.badgeClass === "bad" ? "bad" : calc.badgeClass === "warn" ? "warn" : ""}`.trim();
      }
    }

    document.querySelector("#machineScreenClose").addEventListener("click", closeMachineScreen);
    document.querySelector("#machineScreenMode").addEventListener("click", () => {
      const machine = getActiveMachine();
      if (!machine) return;
      const calc = calcMachine(machine);
      machineScreenMode = machineScreenMode === "result" ? "edit" : (calc.valid ? "result" : "edit");
      renderMachineScreen();
    });
    machineScreen.addEventListener("cancel", event => { event.preventDefault(); closeMachineScreen(); });
    machineScreen.addEventListener("close", () => document.body.classList.remove("machine-screen-open"));
'''
one('    function openSettings() {', v10_js + '\n\n    function openSettings() {', 'JavaScript V10')

required = [
    '<title>Tempo da Linha | VENANC Tools V10</title>',
    'id="machineScreen"',
    'function openMachineScreen(machineId',
    'function estimatedShiftProduction(machine, calc',
    'Produção por turno',
    'Turnos passados',
    'Estimada do turno',
    'Salvar e próxima',
    'Gabaritos — opcional',
    'openMachineScreen(machine.id)',
    'refreshMachineScreenLive()'
]
for token in required:
    if token not in text:
        raise RuntimeError(f'ausente: {token}')

path.write_bytes(text.replace('\n', newline).encode('utf-8'))
print('V10 aplicada com sucesso.')
