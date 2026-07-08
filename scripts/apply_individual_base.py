from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')
original = text


def replace_once(old: str, new: str, label: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'{label}: esperado 1 trecho, encontrado {count}')
    text = text.replace(old, new, 1)


def regex_once(pattern: str, replacement: str, label: str, flags: int = re.S) -> None:
    global text
    text, count = re.subn(pattern, replacement, text, count=1, flags=flags)
    if count != 1:
        raise RuntimeError(f'{label}: esperado 1 trecho, encontrado {count}')


replace_once(
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">',
    '<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, minimum-scale=1, user-scalable=no, viewport-fit=cover">',
    'viewport sem zoom'
)

replace_once(
    'html { min-height: 100%; scroll-behavior: smooth; }',
    'html { min-height: 100%; scroll-behavior: smooth; touch-action: manipulation; -webkit-text-size-adjust: 100%; }',
    'css touch action'
)

replace_once(
'''    <section class="compactControl" aria-label="Controle da projeção">
      <div class="compactClockBlock">
        <div>
          <span class="compactLabel">HORÁRIO ATUAL</span>
          <strong id="liveClock">--/--/---- · --:--:--</strong>
        </div>
        <span class="shiftPill" id="baseShift">-</span>
      </div>
      <div class="compactBaseGrid">
        <div class="field">
          <label for="baseDate">Data-base</label>
          <input class="input" id="baseDate" type="date">
        </div>
        <div class="field">
          <label for="baseTime">Hora-base</label>
          <input class="input" id="baseTime" type="time" step="60">
        </div>
      </div>
      <div class="compactActions">
        <button class="btn btnGhost" id="useNowBtn" type="button">Usar agora</button>
        <button class="btn btnPrimary" id="whatsBtn" type="button">↗ Enviar resumo</button>
      </div>
    </section>''',
'''    <section class="compactControl" aria-label="Relógio e ações da linha">
      <div class="compactClockBlock">
        <div>
          <span class="compactLabel">HORÁRIO ATUAL</span>
          <strong id="liveClock">--/--/---- · --:--:--</strong>
        </div>
        <span class="shiftPill" id="baseShift">-</span>
      </div>
      <div class="compactActions">
        <button class="btn btnPrimary" id="whatsBtn" type="button">↗ Enviar resumo</button>
      </div>
    </section>''',
    'remover horario global'
)

replace_once(
'''      V3 — solicitação automática + destaque executivo da projeção
      Revisão visual premium + correções funcionais:''',
'''      V7 — horário-base individual + previsão fixa + remaining time em tempo real
      Revisão visual premium + correções funcionais:''',
    'versao comentario'
)

replace_once(
'''      6. Campo direto de produzidas e relatório WhatsApp mais enxuto.
    */''',
'''      6. Campo direto de produzidas e relatório WhatsApp mais enxuto.
      7. Cada máquina possui horário-base persistente e previsão independente.
      8. O relógio atual reduz somente o tempo restante, sem deslocar a previsão.
      9. Zoom por pinça, duplo toque e foco de campo bloqueado no iPhone.
    */''',
    'notas da versao'
)

replace_once(
'''    const DEFAULT_MACHINE = () => ({
      id: crypto.randomUUID ? crypto.randomUUID() : String(Date.now() + Math.random()),''',
'''    const DEFAULT_MACHINE = (baseTimestamp = Date.now()) => ({
      id: crypto.randomUUID ? crypto.randomUUID() : String(Date.now() + Math.random()),
      baseTimestamp,''',
    'timestamp default machine'
)

replace_once(
'''      empty: document.querySelector("#emptyState"),
      baseDate: document.querySelector("#baseDate"),
      baseTime: document.querySelector("#baseTime"),
      baseShift: document.querySelector("#baseShift"),''',
'''      empty: document.querySelector("#emptyState"),
      baseShift: document.querySelector("#baseShift"),''',
    'remover refs base global'
)

regex_once(
    r'''    function getNowBase\(\) \{.*?\n    \}\n\n    function loadState\(\) \{.*?\n    \}\n\n    function normalizeMachine\(machine\) \{.*?\n    \}''',
'''    function getTimestampFromLegacyBase(base) {
      if (!base || !base.date || !base.time) return NaN;
      const [y, m, d] = String(base.date).split("-").map(Number);
      const [hh, mm] = String(base.time).split(":").map(Number);
      if (!y || !m || !d || !Number.isFinite(hh) || !Number.isFinite(mm)) return NaN;
      const value = new Date(y, m - 1, d, hh, mm, 0, 0).getTime();
      return Number.isFinite(value) ? value : NaN;
    }

    function loadState() {
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
    }

    function normalizeMachine(machine, fallbackTimestamp = Date.now()) {
      const persistedTimestamp = Number(machine && machine.baseTimestamp);
      const baseTimestamp = Number.isFinite(persistedTimestamp) && persistedTimestamp > 0
        ? persistedTimestamp
        : fallbackTimestamp;
      return {
        ...DEFAULT_MACHINE(baseTimestamp),
        ...machine,
        baseTimestamp,
        trays: Array.isArray(machine.trays) && machine.trays.length ? machine.trays : [""],
        traysCollapsed: machine.traysCollapsed !== false
      };
    }''',
    'migracao e carregamento'
)

regex_once(
    r'''    function getBaseDateTime\(\) \{.*?\n    \}''',
'''    function getMachineBaseDateTime(machine) {
      const timestamp = Number(machine && machine.baseTimestamp);
      if (Number.isFinite(timestamp) && timestamp > 0) return new Date(timestamp);
      const fallback = Date.now();
      machine.baseTimestamp = fallback;
      return new Date(fallback);
    }''',
    'base datetime individual'
)

replace_once(
'''    function calcMachine(machine) {
      const baseDT = getBaseDateTime();''',
'''    function calcMachine(machine) {
      const baseDT = getMachineBaseDateTime(machine);
      const nowDT = new Date();''',
    'calculo usa base individual'
)

replace_once(
'''      const restMin = Math.max(0, Math.floor((endDT - baseDT) / 60000));
      const reason = producible < remainingOP ? "mp" : "meta";
      const status = getOperationalStatus(restMin);
      const labels = {
        now: ["Neste turno", "bad", "bad", "Vai encerrar neste turno."],
        next: ["Próximo turno", "warn", "warn", "Vai encerrar no próximo turno."],
        ok: ["Estável", "ok", "ok", "Não encerra no turno atual nem no próximo."]
      };
      const [statusText, badgeClass, noticeClass, noticeTitle] = labels[status];''',
'''      const restMin = Math.max(0, (endDT - nowDT) / 60000);
      const forecastReached = nowDT >= endDT;
      const reason = producible < remainingOP ? "mp" : "meta";
      const status = forecastReached ? "reached" : getOperationalStatus(restMin);
      const labels = {
        reached: ["Previsão atingida", "bad", "bad", "O horário previsto de encerramento foi atingido."],
        now: ["Neste turno", "bad", "bad", "Vai encerrar neste turno."],
        next: ["Próximo turno", "warn", "warn", "Vai encerrar no próximo turno."],
        ok: ["Estável", "ok", "ok", "Não encerra no turno atual nem no próximo."]
      };
      const [statusText, badgeClass, noticeClass, noticeTitle] = labels[status];''',
    'remaining dinamico'
)

replace_once(
'''        restMin,
        showRequest: restMin < 16 * 60,''',
'''        restMin,
        forecastReached,
        showRequest: forecastReached || restMin < 16 * 60,''',
    'request por remaining'
)

replace_once(
'''    function render() {
      el.baseDate.value = state.base.date;
      el.baseTime.value = state.base.time;
      el.baseShift.textContent = shiftName(getShiftWindowFor(getBaseDateTime()).id);''',
'''    function render() {
      el.baseShift.textContent = shiftName(getShiftWindowFor(new Date()).id);''',
    'render sem base global'
)

replace_once(
'''      node.classList.toggle("collapsed", !!machine.collapsed);
      node.classList.toggle("status-ok", calc.badgeClass === "ok");
      node.classList.toggle("status-warn", calc.badgeClass === "warn");
      node.classList.toggle("status-bad", calc.badgeClass === "bad");

      node.querySelector('[data-role="titleMachine"]').textContent = machine.machine || '-';
      node.querySelector('[data-role="machineToken"]').textContent = machine.machine || '--';
      const badge = node.querySelector('[data-role="statusBadge"]');
      badge.textContent = calc.statusText;
      badge.className = `badge ${calc.badgeClass || ""}`.trim();
      node.querySelector('[data-role="miniRest"]').textContent = calc.valid && calc.endDT ? `${formatMinutes(calc.restMin)} restantes` : "Preencha os dados da máquina";
      node.querySelector('[data-role="miniEnd"]').textContent = calc.valid && calc.endDT ? `previsão ${fmtDate(calc.endDT)} às ${fmtTime(calc.endDT)}` : "Sem previsão calculada";''',
'''      node.classList.toggle("collapsed", !!machine.collapsed);

      node.querySelector('[data-role="titleMachine"]').textContent = machine.machine || '-';
      node.querySelector('[data-role="machineToken"]').textContent = machine.machine || '--';
      applyDynamicCard(node, machine, calc);''',
    'card dinamico inicial'
)

replace_once(
'''      renderTrays(node, machine, calc);
      renderNotice(node, calc);
      renderRequest(node, machine, calc);''',
'''      renderTrays(node, machine, calc);
      renderRequest(node, machine, calc);''',
    'evitar notice duplicado'
)

replace_once(
'''      bindActions(node, machine);
      return node;
    }

    let liveRenderTimer = null;''',
'''      bindActions(node, machine);
      return node;
    }

    function applyDynamicCard(root, machine, calc) {
      root.classList.toggle("status-ok", calc.badgeClass === "ok");
      root.classList.toggle("status-warn", calc.badgeClass === "warn");
      root.classList.toggle("status-bad", calc.badgeClass === "bad");

      const badge = root.querySelector('[data-role="statusBadge"]');
      badge.textContent = calc.statusText;
      badge.className = `badge ${calc.badgeClass || ""}`.trim();

      const miniRest = root.querySelector('[data-role="miniRest"]');
      const miniEnd = root.querySelector('[data-role="miniEnd"]');
      if (calc.valid && calc.endDT) {
        miniRest.textContent = calc.status === "reached" ? "Previsão atingida" : `${formatMinutes(calc.restMin)} restantes`;
        miniEnd.textContent = `previsão fixa ${fmtDate(calc.endDT)} às ${fmtTime(calc.endDT)}`;
      } else {
        miniRest.textContent = "Preencha os dados da máquina";
        miniEnd.textContent = "Sem previsão calculada";
      }

      renderNotice(root, calc);
      const requestBox = root.querySelector('[data-role="requestBox"]');
      if (requestBox) requestBox.classList.toggle("visible", !!calc.showRequest);
    }

    function refreshLiveRemaining() {
      const calcs = [];
      state.machines.forEach(machine => {
        const calc = calcMachine(machine);
        calcs.push(calc);
        const root = [...document.querySelectorAll(".machineCard")].find(card => card.dataset.id === machine.id);
        if (root) applyDynamicCard(root, machine, calc);
      });
      updateSummary(calcs);
      el.baseShift.textContent = shiftName(getShiftWindowFor(new Date()).id);
    }

    let liveRenderTimer = null;''',
    'atualizacao live sem rerender'
)

replace_once(
'''    function prioritySquare(calc) {
      return calc.status === "now" ? "\\u{1F7E5}" : "\\u{1F7E7}";
    }''',
'''    function prioritySquare(calc) {
      return calc.status === "now" || calc.status === "reached" ? "\\u{1F7E5}" : "\\u{1F7E7}";
    }''',
    'prioridade atingida'
)

replace_once(
'''      if (!calc.valid) return `\\u2B1C *TNL ${name}* — Ciclo: _${cycle}_ — Dados incompletos`;
      if (calc.status === "done") return `\\u2705 *TNL ${name}* — Ciclo: _${cycle}_ — OP finalizada`;
      if (calc.status === "now") return `\\u{1F7E5} *TNL ${name}* — Ciclo: _${cycle}_ — Encerra neste turno às _${fmtTime(calc.endDT)}_`;''',
'''      if (!calc.valid) return `\\u2B1C *TNL ${name}* — Ciclo: _${cycle}_ — Dados incompletos`;
      if (calc.status === "done") return `\\u2705 *TNL ${name}* — Ciclo: _${cycle}_ — OP finalizada`;
      if (calc.status === "reached") return `\\u{1F7E5} *TNL ${name}* — Ciclo: _${cycle}_ — Previsão atingida às _${fmtTime(calc.endDT)}_`;
      if (calc.status === "now") return `\\u{1F7E5} *TNL ${name}* — Ciclo: _${cycle}_ — Encerra neste turno às _${fmtTime(calc.endDT)}_`;''',
    'whatsapp previsao atingida'
)

replace_once(
'''    function buildWhatsAppReport() {
      const baseDT = getBaseDateTime();''',
'''    function buildWhatsAppReport() {
      const baseDT = new Date();''',
    'relatorio usa horario atual'
)

replace_once(
'''        .filter(item => (item.calc.status === "now" || item.calc.status === "next") && item.calc.status !== "done")''',
'''        .filter(item => item.calc.status === "reached" || item.calc.status === "now" || item.calc.status === "next")''',
    'prioridades inclui atingida'
)

regex_once(
    r'''\n    function useNow\(\) \{.*?\n    \}\n''',
    '\n',
    'remover use now'
)

replace_once(
'''    document.querySelector("#whatsBtn")?.addEventListener("click", sendWhatsApp);
    document.querySelector("#settingsBtn").addEventListener("click", openSettings);
    document.querySelector("#useNowBtn").addEventListener("click", useNow);
    document.querySelector("#saveSettingsBtn").addEventListener("click", saveSettings);

    el.baseDate.addEventListener("input", () => {
      state.base.date = el.baseDate.value;
      saveState();
    });
    el.baseDate.addEventListener("change", () => {
      state.base.date = el.baseDate.value;
      render();
    });
    el.baseTime.addEventListener("input", () => {
      state.base.time = el.baseTime.value;
      saveState();
    });
    el.baseTime.addEventListener("change", () => {
      state.base.time = el.baseTime.value;
      render();
    });

    updateLiveClock();
    setInterval(updateLiveClock, 1000);
    render();''',
'''    document.querySelector("#whatsBtn")?.addEventListener("click", sendWhatsApp);
    document.querySelector("#settingsBtn").addEventListener("click", openSettings);
    document.querySelector("#saveSettingsBtn").addEventListener("click", saveSettings);

    function blockIOSZoom() {
      ["gesturestart", "gesturechange", "gestureend"].forEach(eventName => {
        document.addEventListener(eventName, event => event.preventDefault(), { passive: false });
      });
      document.addEventListener("touchmove", event => {
        if (event.touches && event.touches.length > 1) event.preventDefault();
      }, { passive: false });
      document.addEventListener("dblclick", event => event.preventDefault(), { passive: false });
      let lastTouchEnd = 0;
      document.addEventListener("touchend", event => {
        const now = Date.now();
        if (now - lastTouchEnd <= 300) event.preventDefault();
        lastTouchEnd = now;
      }, { passive: false });
    }

    blockIOSZoom();
    render();
    updateLiveClock();
    setInterval(() => {
      updateLiveClock();
      refreshLiveRemaining();
    }, 1000);''',
    'listeners e timer final'
)

required = [
    'baseTimestamp',
    'getMachineBaseDateTime(machine)',
    'refreshLiveRemaining()',
    'Previsão atingida',
    'user-scalable=no',
    'blockIOSZoom()'
]
for token in required:
    if token not in text:
        raise RuntimeError(f'validação: token obrigatório ausente: {token}')

for forbidden in ['id="baseDate"', 'id="baseTime"', 'id="useNowBtn"', 'getBaseDateTime()', 'state.base.date', 'state.base.time']:
    if forbidden in text:
        raise RuntimeError(f'validação: resíduo do modelo global encontrado: {forbidden}')

if text == original:
    raise RuntimeError('nenhuma alteração aplicada')

path.write_text(text, encoding='utf-8', newline='\n')
print('index.html atualizado com horário-base individual e previsão fixa.')
