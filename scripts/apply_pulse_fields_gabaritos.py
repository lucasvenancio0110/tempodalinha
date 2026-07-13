from pathlib import Path

path = Path("index.html")
raw = path.read_bytes()
newline = "\r\n" if b"\r\n" in raw else "\n"
text = raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")


def replace_once(old: str, new: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"Esperado 1 marcador, encontrado {count}: {old[:100]}")
    text = text.replace(old, new, 1)


replace_once(
    "      turnMinutes: 480\n    };",
    "      turnMinutes: 480,\n      gabaritoMode: \"individual\"\n    };",
)

replace_once(
    "      trays: [\"\"],\n      traysLocked: false,",
    "      trays: [\"\"],\n      gabaritoMode: \"individual\",\n      traysLocked: false,",
)

replace_once(
    "      const useSum = (state.settings.gabaritoMode || 'sum') === 'sum';",
    "      const useSum = (machine.gabaritoMode || 'individual') === 'sum';",
)

old_optional = """<details class="optionalPanel compactOptionalV111" ${machine.traysCollapsed === false ? 'open' : ''}><summary>Gabaritos — opcional <b>${totalTrays}</b></summary><div class="optionalBodyV11"><div class="trayTotalV11"><span>Produção dos turnos passados</span><strong>${totalTrays}</strong></div>${gabaritos}</div></details>"""
new_optional = """<details class="optionalPanel compactOptionalV111" ${machine.traysCollapsed === false ? 'open' : ''}><summary>Gabaritos — turnos passados <b>${totalTrays}</b></summary><div class="optionalBodyV11"><div class="trayModeTabsV12"><button type="button" data-v10-action="gabarito-mode" data-value="individual" class="${!useSum ? 'active' : ''}">Individual</button><button type="button" data-v10-action="gabarito-mode" data-value="sum" class="${useSum ? 'active' : ''}">Soma rápida</button></div><div class="trayTotalV11"><span>Total produzido nos turnos passados</span><strong>${totalTrays}</strong></div>${gabaritos}</div></details>"""
replace_once(old_optional, new_optional)

replace_once(
    "      if (mode) mode.value = state.settings.gabaritoMode || 'sum';",
    "      if (mode) mode.value = state.settings.gabaritoMode || 'individual';",
)
replace_once(
    "      state.settings.gabaritoMode = document.querySelector('#gabaritoMode')?.value || 'sum';",
    "      state.settings.gabaritoMode = document.querySelector('#gabaritoMode')?.value || 'individual';",
)

old_action = """      if (action === 'mp-mode') { machine.barMode = button.dataset.value; saveState(); return renderMachineScreen(); }
      if (action === 'add-tray') {"""
new_action = """      if (action === 'mp-mode') { machine.barMode = button.dataset.value; saveState(); return renderMachineScreen(); }
      if (action === 'gabarito-mode') {
        machine.gabaritoMode = button.dataset.value === 'sum' ? 'sum' : 'individual';
        machine.traysCollapsed = false;
        if (machine.gabaritoMode === 'sum') machine.trayExpression = gabaritoExpression(machine);
        syncPastProductionV11(machine);
        saveState();
        return renderMachineScreen();
      }
      if (action === 'add-tray') {"""
replace_once(old_action, new_action)

# Deixa explícito no resultado que o valor vem exatamente da soma dos gabaritos.
replace_once(
    "<span>Turnos passados</span><strong>${past}</strong><small>soma dos gabaritos</small>",
    "<span>Turnos passados</span><strong>${past}</strong><small>total dos gabaritos</small>",
)

css = r'''

    /* PULSE CNC 1.0 Beta — campos compactos e gabaritos fáceis */
    .compactOperatorV111 .operatorIntro { display:none !important; }
    .compactOperatorV111.operatorForm { display:block !important; height:auto !important; min-height:100%; }
    .compactOperatorV111 .compactGridV111 {
      grid-template-columns:repeat(2,minmax(0,1fr)) !important;
      grid-template-rows:none !important;
      grid-auto-rows:max-content !important;
      align-content:start !important;
      gap:9px !important;
      height:auto !important;
      overflow:visible !important;
    }
    .compactOperatorV111 .operatorField {
      min-height:92px !important;
      height:auto !important;
      padding:11px 13px !important;
      justify-content:center !important;
    }
    .compactOperatorV111 .operatorField.cycleField { grid-column:auto !important; }
    .compactOperatorV111 .compactBarsV111 {
      grid-column:1/-1 !important;
      min-height:76px !important;
    }
    .compactOperatorV111 .operatorInput {
      min-height:44px !important;
      height:44px !important;
      padding:4px 0 7px !important;
      font-size:clamp(25px,7vw,31px) !important;
    }
    .compactOperatorV111 .compactOptionalV111,
    .compactOperatorV111 [data-v111-preview],
    .compactOperatorV111 .presetPanelV11 { grid-column:1/-1 !important; }
    .compactOperatorV111 .optionalBodyV11 {
      max-height:none !important;
      overflow:visible !important;
      display:block !important;
      padding:10px !important;
    }
    .trayModeTabsV12 {
      display:grid;
      grid-template-columns:repeat(2,minmax(0,1fr));
      gap:7px;
      margin-bottom:9px;
      padding:4px;
      border:1px solid rgba(255,255,255,.08);
      border-radius:12px;
      background:rgba(0,0,0,.12);
    }
    .trayModeTabsV12 button {
      min-height:42px;
      border:1px solid transparent;
      border-radius:10px;
      color:#91a8ae;
      background:transparent;
      font-size:11px;
      font-weight:950;
    }
    .trayModeTabsV12 button.active {
      color:#062824;
      border-color:#56d5c7;
      background:#56d5c7;
      box-shadow:0 8px 20px rgba(86,213,199,.16);
    }
    .compactOperatorV111 .trayTotalV11 {
      margin-bottom:9px;
      padding:10px 12px;
      border-radius:12px;
      background:rgba(86,213,199,.07);
    }
    .compactOperatorV111 .trayListV11 { display:grid; gap:7px; }
    .compactOperatorV111 .trayRowV11 {
      display:grid;
      grid-template-columns:34px minmax(0,1fr) 42px;
      align-items:center;
      gap:7px;
    }
    .compactOperatorV111 .trayRowV11 input,
    .compactOperatorV111 .quickTrayField input {
      min-height:46px !important;
      font-size:18px !important;
    }
    .compactOperatorV111 .trayRowV11 button { width:42px; min-height:42px; }
    .compactOperatorV111 .addTrayV11 { min-height:46px; margin-top:8px; }
    .compactOperatorV111 .editorLiveResult { padding:16px !important; border-radius:20px !important; }
    .compactOperatorV111 .editorResultClock strong { font-size:clamp(36px,10vw,54px) !important; }
    .compactOperatorV111 .editorResultMetrics { gap:7px !important; }
    .compactOperatorV111 .editorResultMetrics > div { padding:10px !important; }
    @media(max-width:380px){
      .compactOperatorV111 .compactGridV111 { gap:7px !important; }
      .compactOperatorV111 .operatorField { min-height:86px !important; padding:9px 11px !important; }
      .compactOperatorV111 .operatorInput { font-size:24px !important; }
    }
'''

marker = "PULSE CNC 1.0 Beta — campos compactos e gabaritos fáceis"
if marker not in text:
    replace_once("\n  </style>", css + "\n  </style>")

path.write_text(text.replace("\n", newline), encoding="utf-8", newline="")
