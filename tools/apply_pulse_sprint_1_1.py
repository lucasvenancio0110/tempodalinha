from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')

old_status = '''    function getOperationalStatus(restMin) {
      if (!Number.isFinite(restMin)) return "idle";
      if (restMin < 8 * 60) return "now";
      if (restMin < 16 * 60) return "next";
      return "ok";
    }'''
new_status = '''    function getOperationalStatus(nowDT, endDT) {
      if (!(nowDT instanceof Date) || !(endDT instanceof Date) || !Number.isFinite(nowDT.getTime()) || !Number.isFinite(endDT.getTime())) return "idle";
      const currentShift = getShiftWindowFor(nowDT);
      if (endDT <= currentShift.endDT) return "now";
      const followingShift = nextShiftWindow(currentShift.endDT, currentShift.id);
      if (endDT <= followingShift.endDT) return "next";
      return "ok";
    }'''
if old_status not in text:
    raise SystemExit('Bloco getOperationalStatus não encontrado')
text = text.replace(old_status, new_status, 1)
text = text.replace('const status = forecastReached ? "reached" : getOperationalStatus(restMin);', 'const status = forecastReached ? "reached" : getOperationalStatus(nowDT, endDT);', 1)

# Memoriza e prioriza a última célula utilizada.
text = text.replace('''      state.selectedCell = cell;
      state.machines = createCellMachines(cell);''', '''      state.selectedCell = cell;
      state.settings.lastCell = cell;
      state.machines = createCellMachines(cell);''', 1)

start = text.find('    function renderCellSelector() {')
end = text.find('\n    function fmtDate(', start)
if start < 0 or end < 0:
    raise SystemExit('renderCellSelector não encontrado')
new_cell_selector = '''    function renderCellSelector() {
      const grid = document.querySelector("#cellGrid");
      grid.innerHTML = "";
      const lastCell = String(state.settings.lastCell || "");
      const entries = Object.entries(CELL_MACHINES).sort(([a], [b]) => {
        if (a === lastCell) return -1;
        if (b === lastCell) return 1;
        return Number(a) - Number(b);
      });
      entries.forEach(([cell, machines]) => {
        const button = document.createElement("button");
        button.className = `cellBtn${cell === lastCell ? " lastUsed" : ""}`;
        button.type = "button";
        button.innerHTML = `<div>${cell === lastCell ? '<small>ÚLTIMA UTILIZADA</small>' : ''}<strong>CÉLULA ${cell}</strong><span>${machines.length} máquinas</span></div><b>›</b>`;
        button.addEventListener("click", () => selectCell(cell));
        grid.appendChild(button);
      });
    }
'''
text = text[:start] + new_cell_selector + text[end:]

# Substitui somente a última função de resultado (a versão efetivamente utilizada).
start = text.rfind('    function renderMachineResult(machine, calc) {')
end = text.find('\n    function bindMachineScreenEvents(machine) {', start)
if start < 0 or end < 0:
    raise SystemExit('renderMachineResult final não encontrado')
new_result = '''    function renderMachineResult(machine, calc) {
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
      const pieceLength = Math.max(0, parseNumber(machine.pieceLength) || 0);
      const kerf = Math.max(0, parseNumber(state.settings.kerfWidth) || 0);
      const step = pieceLength + kerf;
      let currentBarPieces = 0;
      if (machine.barMode === 'full') currentBarPieces = calc.perBar || 0;
      else if (machine.barMode === 'partialMm' && step > 0) currentBarPieces = Math.floor(Math.max(0, parseNumber(machine.partialMm) || 0) / step);
      else currentBarPieces = Math.max(0, parseInteger(machine.partialPieces));
      const barPercent = calc.perBar ? Math.max(0, Math.min(100, currentBarPieces / calc.perBar * 100)) : 0;
      const reason = calc.reason === 'mp' ? 'Matéria-prima disponível' : 'Meta da OP';

      machineScreenContent.innerHTML = `
        <section class="machineView cockpitV11 pulseResultV12">
          <div class="resultHeroV11 pulseHeroV12">
            <div class="resultHeroTopV11"><span class="resultStatusV11 ${statusClass}" data-v10-live="status">${escapeHtml(calc.statusText.toUpperCase())}</span><small>Tempo restante</small></div>
            <div class="mainCountdownV11"><strong data-v10-live="countdown">${countdown.clock}</strong><small data-v10-live="milliseconds">.${countdown.milliseconds}</small></div>
            <div class="pulseForecastV12"><span>Previsão fixa</span><strong>${fmtTime(calc.endDT)}</strong><small>${fmtDate(calc.endDT)} · ${shiftName(getShiftWindowFor(calc.endDT).id)}</small></div>
            <div class="opProgressV11"><div class="opProgressLabelsV11"><span>${currentTotal} / ${target} peças</span><strong data-v10-live="progress">${Math.round(progress)}%</strong></div><div class="opProgressTrackV11"><i data-v10-live="progress-bar" style="width:${progress}%"></i></div></div>
          </div>

          <div class="primaryMetricsV11 pulsePrimaryV12">
            <div class="metricV11"><span>Total dos gabaritos</span><strong>${past}</strong></div>
            <div class="metricV11"><span>Produção ao vivo</span><strong data-v10-live="estimated">${estimate}</strong><small>desde o início do cálculo</small></div>
            <div class="metricV11"><span>Produção até o fim do turno</span><strong data-v10-live="shift-end-estimated">${shiftEndEstimate}</strong><small>mantendo o ciclo</small></div>
            <div class="metricV11"><span>Faltam para a meta</span><strong data-v10-live="missing">${missing}</strong></div>
          </div>

          <section class="resultCategoryV12">
            <h3>Produção</h3>
            <div class="resultCategoryGridV12">
              <div class="metricV11"><span>Meta da OP</span><strong>${target}</strong></div>
              <div class="metricV11"><span>Capacidade por turno</span><strong>${calc.metaTurno || 0}</strong><small>peças em 8 horas</small></div>
              <div class="metricV11"><span>Encerramento por</span><strong>${reason}</strong></div>
            </div>
          </section>

          <section class="resultCategoryV12">
            <h3>Matéria-prima</h3>
            <div class="materialBarV12"><div><span>Barra atual</span><strong>${currentBarPieces} / ${calc.perBar || 0} peças</strong></div><div class="materialTrackV12"><i style="width:${barPercent}%"></i></div><small>${Math.round(barPercent)}% disponível na barra atual</small></div>
            <div class="resultCategoryGridV12">
              <div class="metricV11"><span>MP disponível</span><strong>${calc.capacity}</strong><small>peças possíveis</small></div>
              <div class="metricV11"><span>Barras inteiras</span><strong>${bars}</strong></div>
              <div class="metricV11"><span>Peças por barra</span><strong>${calc.perBar || 0}</strong></div>
              <div class="metricV11"><span>Consumo por peça</span><strong>${step ? step.toFixed(2).replace('.', ',') : '-'} mm</strong><small>peça + bedame</small></div>
            </div>
          </section>

          <details class="calculationDetailsV12">
            <summary>Detalhes do cálculo</summary>
            <div class="resultCategoryGridV12">
              <div class="metricV11"><span>Ciclo informado</span><strong>${escapeHtml(String(machine.timeInput || '-'))}</strong></div>
              <div class="metricV11"><span>Ciclo em segundos</span><strong>${Number.isFinite(cycleSeconds) ? cycleSeconds.toFixed(0) : '-'} s</strong></div>
              <div class="metricV11"><span>Ciclo em minutos</span><strong>${Number.isFinite(decimalMinutes) ? decimalMinutes.toFixed(4) : '-'}</strong><small>fração decimal</small></div>
              <div class="metricV11"><span>Cálculo iniciado</span><strong>${fmtTime(new Date(machine.calculationStartedAt))}</strong><small>${fmtDate(new Date(machine.calculationStartedAt))}</small></div>
            </div>
          </details>
          ${renderPresetV11(machine, calc)}
        </section>`;
      machineScreenFooter.innerHTML = `<button class="machineFooterBtn" data-v10-action="previous" type="button" ${activeMachineIndex()<=0?'disabled':''}>${svgArrow(-1)} Anterior</button><button class="machineFooterBtn" data-v10-action="edit" type="button">Editar dados</button><button class="machineFooterBtn primary" data-v10-action="next" type="button">Próxima máquina ${svgArrow(1)}</button>`;
      bindMachineScreenEvents(machine);
    }
'''
text = text[:start] + new_result + text[end:]

# Textos restantes no resultado/editor e relatório.
replacements = {
    'Turnos passados': 'Total dos gabaritos',
    'Estimada até agora': 'Produção ao vivo',
    'Estimada do turno': 'Produção ao vivo',
    'Até o fim do turno': 'Produção até o fim do turno',
    'Produção por turno': 'Capacidade por turno',
    '*TEMPO DA LINHA —': '*PULSE CNC —',
    '· VENANC Tools_': '· PULSE CNC_'
}
for old, new in replacements.items():
    text = text.replace(old, new)

text = text.replace('<div class="mark" aria-hidden="true">TL</div>', '<div class="mark pulseLetterMark" aria-hidden="true">P</div>', 1)

css = r'''

    /* PULSE CNC Sprint 1.1 — leitura operacional e segurança visual */
    .cellSelectorPanel { padding:16px !important; }
    .cellSelectorBrand { margin-bottom:12px !important; }
    .cellSelectorBrand .mark { width:42px; height:42px; }
    .cellSelectorTitle h1 { font-size:24px !important; }
    .cellSelectorTitle p { margin-top:3px !important; }
    .cellGrid { grid-template-columns:repeat(2,minmax(0,1fr)) !important; gap:8px !important; }
    .cellBtn { min-height:62px !important; padding:10px 12px !important; border-radius:14px !important; }
    .cellBtn strong { font-size:16px !important; }
    .cellBtn span { margin-top:2px !important; font-size:10px !important; }
    .cellBtn small { display:block; margin-bottom:3px; color:#f2b864; font-size:7px; font-weight:950; letter-spacing:.1em; }
    .cellBtn.lastUsed { grid-column:1/-1; border-color:rgba(86,213,199,.42); background:rgba(86,213,199,.10); }
    .pulseLetterMark { color:#062824 !important; background:linear-gradient(145deg,#70eadc,#42cbbb) !important; font-size:22px !important; }

    .machineScreenContent { scroll-padding-bottom:120px; }
    .pulseResultV12 { display:block !important; height:auto !important; min-height:100%; padding-bottom:28px; }
    .pulseHeroV12 { min-height:0 !important; padding:15px 17px !important; }
    .pulseHeroV12 .mainCountdownV11 { margin-top:7px; }
    .pulseForecastV12 { display:grid; grid-template-columns:1fr auto; align-items:end; gap:2px 12px; margin-top:10px; padding:9px 11px; border:1px solid rgba(255,255,255,.08); border-radius:12px; background:rgba(0,0,0,.12); }
    .pulseForecastV12 span { color:#829aa1; font-size:8px; font-weight:950; letter-spacing:.1em; text-transform:uppercase; }
    .pulseForecastV12 strong { grid-row:1/3; grid-column:2; color:#f0fbfa; font-size:24px; }
    .pulseForecastV12 small { color:#6fa79f; font-size:9px; font-weight:800; }
    .pulsePrimaryV12 { margin-top:9px; }
    .pulsePrimaryV12 .metricV11 { min-height:92px; }
    .resultCategoryV12 { margin-top:10px; padding:12px; border:1px solid rgba(255,255,255,.09); border-radius:17px; background:rgba(255,255,255,.028); }
    .resultCategoryV12 h3 { margin:0 0 9px; color:#99afb5; font-size:10px; font-weight:950; letter-spacing:.14em; text-transform:uppercase; }
    .resultCategoryGridV12 { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:8px; }
    .resultCategoryGridV12 .metricV11 { min-height:88px; }
    .materialBarV12 { margin-bottom:9px; padding:11px; border-radius:13px; background:rgba(0,0,0,.14); }
    .materialBarV12 > div:first-child { display:flex; align-items:center; justify-content:space-between; gap:10px; }
    .materialBarV12 span { color:#839ca3; font-size:9px; font-weight:950; letter-spacing:.09em; text-transform:uppercase; }
    .materialBarV12 strong { color:#f1fbfa; font-size:15px; }
    .materialTrackV12 { height:10px; margin-top:9px; overflow:hidden; border-radius:999px; background:rgba(255,255,255,.08); }
    .materialTrackV12 i { display:block; height:100%; border-radius:inherit; background:linear-gradient(90deg,#18a999,#56d5c7); }
    .materialBarV12 small { display:block; margin-top:6px; color:#6fa79f; font-size:9px; font-weight:800; }
    .calculationDetailsV12 { margin-top:10px; border:1px solid rgba(255,255,255,.09); border-radius:16px; background:rgba(255,255,255,.025); overflow:hidden; }
    .calculationDetailsV12 summary { min-height:48px; display:flex; align-items:center; padding:0 13px; color:#b5c8cc; cursor:pointer; font-size:11px; font-weight:950; }
    .calculationDetailsV12[open] summary { border-bottom:1px solid rgba(255,255,255,.08); }
    .calculationDetailsV12 .resultCategoryGridV12 { padding:10px; }
    .pulseResultV12 > .presetPanelV11 { margin-top:10px; }
    .machineScreenFooter { position:relative; z-index:5; }
    .machineScreenContent::-webkit-scrollbar { width:3px; }
    .machineScreenContent::-webkit-scrollbar-thumb { background:rgba(181,206,211,.25); border-radius:999px; }
    @media(max-width:430px){
      .cellSelector { padding:12px 10px !important; }
      .cellGrid { gap:7px !important; }
      .cellBtn { min-height:58px !important; }
      .pulsePrimaryV12, .resultCategoryGridV12 { grid-template-columns:repeat(2,minmax(0,1fr)) !important; }
      .pulsePrimaryV12 .metricV11, .resultCategoryGridV12 .metricV11 { min-height:82px; }
      .pulseHeroV12 .mainCountdownV11 strong { font-size:clamp(38px,12vw,55px) !important; }
    }
'''
text = text.replace('\n  </style>', css + '\n  </style>', 1)

path.write_text(text, encoding='utf-8', newline='')
print('Sprint 1.1 aplicada com sucesso')
