from pathlib import Path

path = Path('index.html')
raw = path.read_bytes()
newline = '\r\n' if b'\r\n' in raw else '\n'
text = raw.decode('utf-8').replace('\r\n', '\n')

# Resultado ao vivo do preenchimento: somente decisão operacional.
start = text.rfind('    function compactEditorPreview(machine) {')
end = text.find('\n    function updateCompactEditorPreview(machine) {', start)
if start < 0 or end < 0:
    raise SystemExit('compactEditorPreview final não encontrado')
preview = '''    function compactEditorPreview(machine) {
      const calc = calcMachine(machine);
      if (!calc.valid) return `<section class="editorLiveResult waiting"><span>RESULTADO</span><strong>Complete Ciclo, Meta e Peça</strong><small>A previsão aparecerá aqui automaticamente.</small></section>`;
      ensureExactStart(machine);
      const parts = formatCountdownParts(calc.restMs);
      const past = syncPastProductionV11(machine);
      const estimate = estimatedShiftProduction(machine, calc, Date.now());
      const shiftEndEstimate = estimatedUntilShiftEndV11(machine, calc, Date.now());
      const target = Math.max(0, parseInteger(machine.target));
      const progress = target ? Math.max(0, Math.min(100, ((past + estimate) / target) * 100)) : 0;
      const statusClass = calc.badgeClass === 'bad' ? 'bad' : calc.badgeClass === 'warn' ? 'warn' : 'ok';
      return `<section class="editorLiveResult editorDecisionV12 ${statusClass}">
        <div class="editorResultHead"><div><span>RESULTADO AO VIVO</span><strong>${escapeHtml(calc.statusText.toUpperCase())}</strong></div><b>${Math.round(progress)}%</b></div>
        <div class="decisionMainV12"><span>Tempo restante</span><strong data-v12-editor-countdown>${parts.clock}</strong></div>
        <div class="decisionFactsV12">
          <div><span>Previsão de encerramento</span><strong>${fmtTime(calc.endDT)}</strong><small>${fmtDate(calc.endDT)} · ${shiftName(getShiftWindowFor(calc.endDT).id)}</small></div>
          <div><span>Até o fim do turno</span><strong>${shiftEndEstimate} peças</strong><small>mantendo o ciclo atual</small></div>
        </div>
        <div class="editorResultBar"><i style="width:${progress}%"></i></div>
        <div class="decisionProgressV12"><span>${past + estimate} / ${target} peças</span><strong>${Math.round(progress)}% da OP</strong></div>
      </section>`;
    }
'''
text = text[:start] + preview + text[end:]

# Preset: mantém os mesmos campos, com apresentação operacional premium.
start = text.rfind('    function renderPresetV11(machine, calc) {')
if start < 0:
    raise SystemExit('renderPresetV11 final não encontrado')
end = text.find('\n    function ', start + 20)
if end < 0:
    raise SystemExit('fim de renderPresetV11 não encontrado')
preset = '''    function renderPresetV11(machine, calc) {
      if (!presetRequiredV11(calc)) return '';
      const received = machine.presetMode === 'yes';
      const requestDate = calc.endDT ? fmtDate(calc.endDT) : '-';
      const requestTime = calc.endDT ? fmtTime(calc.endDT) : '--:--';
      const remainingText = calc.forecastReached ? 'HORÁRIO ATINGIDO' : `Faltam ${formatMinutes(calc.restMin)}`;
      const setupOptions = [
        ['sequencia', 'Sequência'],
        ['verde', 'Setup verde'],
        ['azul', 'Setup azul'],
        ['vermelho', 'Setup vermelho']
      ].map(([value,label]) => `<option value="${value}" ${machine.presetType===value?'selected':''}>${label}</option>`).join('');
      return `<section class="presetMissionV12 ${received ? 'received' : 'pending'}">
        <div class="presetMissionHeadV12">
          <div><span>PRÓXIMA OP</span><strong>Preset da máquina</strong></div>
          <b>${received ? 'PRESET RECEBIDO' : 'PRESET PENDENTE'}</b>
        </div>
        <div class="presetDecisionV12">
          <button type="button" data-v10-action="preset-mode" data-value="yes" class="${received ? 'active' : ''}"><span>✓</span><strong>Já trouxe</strong></button>
          <button type="button" data-v10-action="preset-mode" data-value="no" class="${!received ? 'active' : ''}"><span>⌛</span><strong>Ainda não trouxe</strong></button>
        </div>
        <div class="presetTypeV12"><label>Tipo da próxima OP</label><select data-v10-field="presetType">${setupOptions}</select></div>
        ${received
          ? `<div class="presetReceivedV12"><span>✓</span><div><strong>Preset disponível</strong><small>${escapeHtml(presetLabel(machine))}</small></div></div>`
          : `<div class="presetRequestV12"><span>Solicitar ao Preset</span><strong>${requestDate} · ${requestTime}</strong><small>${remainingText}</small></div><div class="presetItemV12"><label>Item da próxima OP</label><input data-v10-field="itemCode" value="${escapeHtml(String(machine.itemCode || ''))}" placeholder="Ex.: 125.142-1"></div>`}
      </section>`;
    }
'''
text = text[:start] + preset + text[end:]

# Organização por arrastar e soltar, mantendo a mesma matriz e persistência.
start = text.rfind('    function renderMachineOrderSettings() {')
end = text.find('\n    function compactEditorPreview(machine) {', start)
if start < 0 or end < 0:
    raise SystemExit('renderMachineOrderSettings final não encontrado')
order = '''    function commitMachineOrderFromList(list) {
      const ids = [...list.querySelectorAll('.machineOrderRow')].map(row => row.dataset.machineId);
      const byId = new Map(state.machines.map(machine => [String(machine.id), machine]));
      const reordered = ids.map(id => byId.get(id)).filter(Boolean);
      if (reordered.length !== state.machines.length) return;
      state.machines = reordered;
      state.cells[state.selectedCell] = state.machines;
      saveState();
      render();
    }

    function bindMachineOrderDrag(row, list) {
      const handle = row.querySelector('.dragHandleV12');
      let dragging = false;
      const finish = () => {
        if (!dragging) return;
        dragging = false;
        row.classList.remove('dragging');
        document.body.classList.remove('sorting-machines');
        commitMachineOrderFromList(list);
        [...list.children].forEach((item,index) => {
          const number = item.querySelector('.machineOrderPositionV12');
          if (number) number.textContent = index + 1;
        });
      };
      handle.addEventListener('pointerdown', event => {
        if (event.pointerType === 'mouse' && event.button !== 0) return;
        dragging = true;
        row.classList.add('dragging');
        document.body.classList.add('sorting-machines');
        handle.setPointerCapture?.(event.pointerId);
        navigator.vibrate?.(25);
        event.preventDefault();
      });
      handle.addEventListener('pointermove', event => {
        if (!dragging) return;
        const target = document.elementFromPoint(event.clientX, event.clientY)?.closest('.machineOrderRow');
        if (!target || target === row || target.parentElement !== list) return;
        const rect = target.getBoundingClientRect();
        list.insertBefore(row, event.clientY < rect.top + rect.height / 2 ? target : target.nextSibling);
        event.preventDefault();
      });
      handle.addEventListener('pointerup', finish);
      handle.addEventListener('pointercancel', finish);
    }

    function renderMachineOrderSettings() {
      const list = document.querySelector('#machineOrderList');
      const section = document.querySelector('#machineOrderSettings');
      if (!list || !section) return;
      section.hidden = !state.selectedCell || !state.machines.length;
      list.innerHTML = '';
      state.machines.forEach((machine, index) => {
        const row = document.createElement('div');
        row.className = 'machineOrderRow draggableOrderV12';
        row.dataset.machineId = String(machine.id);
        row.innerHTML = `<button class="dragHandleV12" type="button" aria-label="Segure e arraste a TNL ${formatTnl(machine.machine)}"><i></i><i></i><i></i></button><span><b class="machineOrderPositionV12">${index + 1}</b>TNL ${formatTnl(machine.machine)}</span><small>Segure e arraste</small>`;
        list.appendChild(row);
        bindMachineOrderDrag(row, list);
      });
    }
'''
text = text[:start] + order + text[end:]

# CSS isolado da Sprint 1.2.
css = r'''

    /* PULSE CNC Sprint 1.2 — decisão rápida, preset premium e ordem por arraste */
    .editorDecisionV12 { padding:15px !important; }
    .decisionMainV12 { margin-top:12px; padding:12px 0 10px; text-align:center; }
    .decisionMainV12 span { display:block; color:#82979e; font-size:9px; font-weight:950; letter-spacing:.12em; text-transform:uppercase; }
    .decisionMainV12 strong { display:block; margin-top:3px; color:#f3fbfa; font-family:"SFMono-Regular",Consolas,monospace; font-size:clamp(38px,12vw,56px); line-height:1; letter-spacing:-.07em; }
    .decisionFactsV12 { display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-top:8px; }
    .decisionFactsV12 > div { min-height:82px; padding:11px; border:1px solid rgba(255,255,255,.08); border-radius:13px; background:rgba(0,0,0,.13); }
    .decisionFactsV12 span,.decisionFactsV12 small { display:block; color:#82979e; font-size:9px; font-weight:850; }
    .decisionFactsV12 strong { display:block; margin:5px 0 2px; color:#f3fbfa; font-size:21px; }
    .decisionProgressV12 { display:flex; justify-content:space-between; gap:10px; margin-top:7px; color:#91a7ad; font-size:9px; font-weight:900; }

    .presetMissionV12 { margin-top:10px; overflow:hidden; border:1px solid rgba(242,184,100,.35); border-radius:18px; background:linear-gradient(145deg,rgba(91,58,14,.30),rgba(20,29,35,.94)); box-shadow:0 16px 34px rgba(0,0,0,.15); }
    .presetMissionV12.received { border-color:rgba(86,213,199,.40); background:linear-gradient(145deg,rgba(16,93,82,.25),rgba(20,29,35,.94)); }
    .presetMissionHeadV12 { display:flex; align-items:center; justify-content:space-between; gap:12px; padding:14px; border-bottom:1px solid rgba(255,255,255,.08); }
    .presetMissionHeadV12 span { display:block; color:#f2b864; font-size:8px; font-weight:950; letter-spacing:.15em; }
    .presetMissionHeadV12 strong { display:block; margin-top:3px; color:#f6fbfa; font-size:16px; }
    .presetMissionHeadV12 > b { padding:6px 8px; border-radius:999px; color:#f2b864; background:rgba(242,184,100,.12); font-size:8px; letter-spacing:.08em; }
    .presetMissionV12.received .presetMissionHeadV12 > b { color:#70eadc; background:rgba(86,213,199,.13); }
    .presetDecisionV12 { display:grid; grid-template-columns:1fr 1fr; gap:8px; padding:12px 12px 0; }
    .presetDecisionV12 button { min-height:58px; display:flex; align-items:center; justify-content:center; gap:7px; border:1px solid rgba(255,255,255,.10); border-radius:13px; color:#9eb1b6; background:rgba(255,255,255,.04); }
    .presetDecisionV12 button.active { color:#092b27; border-color:transparent; background:#56d5c7; box-shadow:0 8px 20px rgba(86,213,199,.20); }
    .presetDecisionV12 button:nth-child(2).active { color:#3b2405; background:#f2b864; box-shadow:0 8px 20px rgba(242,184,100,.18); }
    .presetDecisionV12 span { font-size:18px; }
    .presetDecisionV12 strong { font-size:12px; }
    .presetTypeV12,.presetItemV12 { padding:12px; }
    .presetTypeV12 label,.presetItemV12 label { display:block; margin-bottom:6px; color:#9eb1b6; font-size:9px; font-weight:950; letter-spacing:.1em; text-transform:uppercase; }
    .presetTypeV12 select,.presetItemV12 input { width:100%; min-height:46px; border:1px solid rgba(255,255,255,.12); border-radius:12px; padding:0 12px; color:#eefafa; background:#16242c; font-size:16px; }
    .presetRequestV12 { margin:0 12px; padding:13px; border:1px solid rgba(242,184,100,.24); border-radius:13px; text-align:center; background:rgba(242,184,100,.08); }
    .presetRequestV12 span,.presetRequestV12 small { display:block; color:#caa66e; font-size:9px; font-weight:900; }
    .presetRequestV12 strong { display:block; margin:5px 0 3px; color:#ffd899; font-size:21px; }
    .presetReceivedV12 { display:flex; align-items:center; gap:10px; margin:0 12px 12px; padding:13px; border-radius:13px; color:#70eadc; background:rgba(86,213,199,.10); }
    .presetReceivedV12 > span { font-size:24px; }
    .presetReceivedV12 strong,.presetReceivedV12 small { display:block; }
    .presetReceivedV12 small { margin-top:2px; color:#8fbab5; }

    .machineOrderHeader span { font-size:0 !important; }
    .machineOrderHeader span::after { content:"Segure a alça e arraste"; font-size:10px; }
    .draggableOrderV12 { display:grid !important; grid-template-columns:42px 1fr auto; align-items:center; gap:10px; min-height:58px; user-select:none; }
    .draggableOrderV12 > span { display:flex; align-items:center; gap:9px; }
    .draggableOrderV12 > small { color:#82979e; font-size:9px; font-weight:850; }
    .dragHandleV12 { width:38px; height:38px; display:grid; align-content:center; gap:4px; border:0; border-radius:10px; padding:0 9px; background:rgba(86,213,199,.10); touch-action:none; }
    .dragHandleV12 i { display:block; height:2px; border-radius:999px; background:#56d5c7; }
    .draggableOrderV12.dragging { position:relative; z-index:20; opacity:.92; transform:scale(1.02); border-color:rgba(86,213,199,.55) !important; box-shadow:0 14px 30px rgba(0,0,0,.18); }
    body.sorting-machines { user-select:none; }
    @media(max-width:430px){
      .decisionFactsV12 { grid-template-columns:1fr 1fr; }
      .draggableOrderV12 { grid-template-columns:42px 1fr; }
      .draggableOrderV12 > small { display:none; }
    }
'''
if '</style>' not in text:
    raise SystemExit('fechamento de style não encontrado')
text = text.replace('</style>', css + '\n  </style>', 1)

path.write_bytes(text.replace('\n', newline).encode('utf-8'))
