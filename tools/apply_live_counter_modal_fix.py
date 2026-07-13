from pathlib import Path
import re

path = Path('index.html')
raw = path.read_bytes()
newline = '\r\n' if b'\r\n' in raw else '\n'
text = raw.decode('utf-8').replace('\r\n','\n')

# Atualização passa a ser de 1 segundo.
text = text.replace('setInterval(refreshLiveRemaining, 250);', 'setInterval(refreshLiveRemaining, 1000);', 1)

# Contadores antigos deixam de exigir o nó de milissegundos.
old = '''    function updateCountdownDisplay(root, calc) {
      const wrap = root.querySelector('[data-role="projectionRest"]');
      const clock = root.querySelector('[data-role="countdownClock"]');
      const milliseconds = root.querySelector('[data-role="countdownMs"]');
      if (!wrap || !clock || !milliseconds) return;
      if (!calc.valid || !calc.endDT) {
        clock.textContent = "--:--:--";
        milliseconds.textContent = ".---";
        wrap.setAttribute("aria-label", "Tempo restante indisponível");
        return;
      }
      const parts = formatCountdownParts(calc.restMs);
      clock.textContent = parts.clock;
      milliseconds.textContent = `.${parts.milliseconds}`;
      wrap.setAttribute("aria-label", `${parts.clock}.${parts.milliseconds} restantes`);
    }'''
new = '''    function updateCountdownDisplay(root, calc) {
      const wrap = root.querySelector('[data-role="projectionRest"]');
      const clock = root.querySelector('[data-role="countdownClock"]');
      if (!wrap || !clock) return;
      if (!calc.valid || !calc.endDT) {
        clock.textContent = "--:--:--";
        wrap.setAttribute("aria-label", "Tempo restante indisponível");
        return;
      }
      const parts = formatCountdownParts(calc.restMs);
      clock.textContent = parts.clock;
      wrap.setAttribute("aria-label", `${parts.clock} restantes`);
    }'''
if old not in text:
    raise SystemExit('updateCountdownDisplay não encontrado')
text = text.replace(old, new, 1)

# Resultado ao vivo do preenchimento ganha cor operacional e não exibe milissegundos.
start = text.find('    function compactEditorPreview(machine) {')
end = text.find('\n    function updateCompactEditorPreview(machine) {', start)
if start < 0 or end < 0:
    raise SystemExit('compactEditorPreview não encontrado')
replacement = '''    function compactEditorPreview(machine) {
      const calc = calcMachine(machine);
      if (!calc.valid) return `<section class="editorLiveResult waiting"><span>RESULTADO</span><strong>Complete Ciclo, Meta e Peça</strong><small>A previsão aparecerá aqui automaticamente.</small></section>`;
      ensureExactStart(machine);
      const parts = formatCountdownParts(calc.restMs);
      const past = syncPastProductionV11(machine);
      const estimate = estimatedShiftProduction(machine, calc, Date.now());
      const target = Math.max(0, parseInteger(machine.target));
      const missing = Math.max(0, target - Math.min(target, past + estimate));
      const progress = target ? Math.min(100, ((past + estimate) / target) * 100) : 0;
      const statusClass = calc.badgeClass === 'bad' ? 'bad' : calc.badgeClass === 'warn' ? 'warn' : 'ok';
      return `<section class="editorLiveResult ${statusClass}">
        <div class="editorResultHead"><div><span>RESULTADO AO VIVO</span><strong>${escapeHtml(calc.statusText.toUpperCase())}</strong></div><b>${Math.round(progress)}%</b></div>
        <div class="editorResultClock"><span>Tempo restante</span><strong data-v12-editor-countdown>${parts.clock}</strong></div>
        <div class="editorResultBar"><i style="width:${progress}%"></i></div>
        <div class="editorResultMetrics"><div><span>Total dos gabaritos</span><strong>${past}</strong></div><div><span>Produção ao vivo</span><strong>${estimate}</strong></div><div><span>Faltam</span><strong>${missing}</strong></div><div><span>MP disponível</span><strong>${calc.capacity}</strong></div></div>
      </section>`;
    }
'''
text = text[:start] + replacement + text[end:]

# A rotina ao vivo passa a atender tanto resultado quanto preenchimento.
old_head = '''    function refreshMachineScreenLive() {
      if (!machineScreen?.open || machineScreenMode !== 'result') return;
      const machine = getActiveMachine(); if (!machine) return;'''
new_head = '''    function refreshMachineScreenLive() {
      if (!machineScreen?.open) return;
      const machine = getActiveMachine(); if (!machine) return;
      if (machineScreenMode === 'edit') {
        const holder = machineScreenContent.querySelector('[data-v111-preview]');
        if (holder) holder.innerHTML = compactEditorPreview(machine);
        return;
      }
      if (machineScreenMode !== 'result') return;'''
if old_head not in text:
    raise SystemExit('início de refreshMachineScreenLive não encontrado')
text = text.replace(old_head, new_head, 1)

# Remove atualização textual dos milissegundos da tela de resultado.
text = text.replace("set('[data-v10-live=\"countdown\"]',parts.clock); set('[data-v10-live=\"milliseconds\"]',`.${parts.milliseconds}`);", "set('[data-v10-live=\"countdown\"]',parts.clock);", 1)

# Remove os pequenos blocos de milissegundos dos templates efetivamente usados.
text = re.sub(r'<small[^>]*(?:clockMs|countdownMs|data-v10-live="milliseconds")[^>]*>[^<]*</small>', '', text)

# Ajustes: texto da regra acompanha a lógica atual por turnos reais.
text = text.replace('🟥 menos de 8h · 🟧 menos de 16h', 'Vermelho: turno atual · Laranja: próximo turno', 1)

css = '''

    /* PULSE CNC — contador leve, cores no preenchimento e modal rolável */
    .clockMs, .countdownMs, [data-v10-live="milliseconds"], .mainCountdownV11 > small { display:none !important; }
    .editorLiveResult.bad { border-color:rgba(255,111,130,.52) !important; background:linear-gradient(145deg,rgba(173,48,59,.18),rgba(255,255,255,.025)) !important; }
    .editorLiveResult.warn { border-color:rgba(242,184,100,.48) !important; background:linear-gradient(145deg,rgba(154,90,8,.18),rgba(255,255,255,.025)) !important; }
    .editorLiveResult.ok { border-color:rgba(86,213,199,.42) !important; }
    .editorLiveResult.bad .editorResultHead strong { color:#ff8fa0 !important; }
    .editorLiveResult.warn .editorResultHead strong { color:#f2b864 !important; }
    .editorLiveResult.ok .editorResultHead strong { color:#56d5c7 !important; }

    body:has(#settingsModal[open]) { overflow:hidden !important; }
    #settingsModal {
      width:min(760px,calc(100vw - 20px));
      max-width:760px;
      max-height:calc(100dvh - 20px);
      padding:0 !important;
      overflow:hidden !important;
    }
    #settingsForm {
      width:100%;
      max-height:calc(100dvh - 20px);
      display:flex;
      flex-direction:column;
      overflow:hidden;
    }
    #settingsModal .modalHead { flex:0 0 auto; }
    #settingsModal .modalBody {
      flex:1 1 auto;
      min-height:0;
      overflow-y:auto !important;
      overscroll-behavior:contain;
      -webkit-overflow-scrolling:touch;
      touch-action:pan-y;
      padding-bottom:28px;
    }
    #settingsModal .modalFoot {
      position:sticky;
      bottom:0;
      z-index:5;
      flex:0 0 auto;
      background:#fff;
      box-shadow:0 -12px 28px rgba(0,0,0,.10);
    }
    @media(max-width:620px){
      #settingsModal { width:calc(100vw - 12px); max-height:calc(100dvh - 12px); }
      #settingsForm { max-height:calc(100dvh - 12px); }
    }
'''
if '</style>' not in text:
    raise SystemExit('style final não encontrado')
text = text.replace('</style>', css + '\n  </style>', 1)

# Documentação interna deixa de mencionar milissegundos.
text = text.replace('Tempo restante em HH:MM:SS.mmm com atualização visual contínua.', 'Tempo restante em HH:MM:SS com atualização a cada segundo.', 1)

path.write_bytes(text.replace('\n', newline).encode('utf-8'))
