from pathlib import Path

path = Path("index.html")
raw = path.read_bytes()
newline = "\r\n" if b"\r\n" in raw else "\n"
text = raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")

if "VENANC Tools V8" in text and 'id="addMachineBottomBtn"' in text:
    print("V8 já aplicada.")
    raise SystemExit(0)


def one(old: str, new: str, label: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: esperado 1, encontrado {count}")
    text = text.replace(old, new, 1)


one(
    "<title>Tempo da Linha | VENANC Tools V7</title>",
    "<title>Tempo da Linha | VENANC Tools V8</title>",
    "título",
)

one(
    "    .cards { display: flex; flex-direction: column; gap: 13px; }",
    """    .cards { display: flex; flex-direction: column; gap: 13px; }
    .bottomAddWrap { display:flex; justify-content:center; padding:18px 0 4px; }
    .bottomAddWrap .bottomAddBtn {
      width:min(100%, 330px);
      min-height:54px;
      border-radius:16px;
      border-color:rgba(112,237,219,.42);
      box-shadow:0 15px 32px rgba(24,169,153,.24);
      font-size:14px;
      letter-spacing:.01em;
    }
    .bottomAddBtn .addButtonIcon {
      width:30px;
      height:30px;
      display:inline-grid;
      place-items:center;
      border-radius:10px;
      color:#effffc;
      background:rgba(6,40,36,.22);
      font-size:21px;
      line-height:1;
    }
    .bottomAddBtn:hover { box-shadow:0 18px 38px rgba(24,169,153,.30); }""",
    "css botão inferior",
)

one(
    "    .compactProjectionMetric strong { display:block; margin-top:8px; color:#1b3741; font-size:18px; line-height:1.08; letter-spacing:-.04em; overflow-wrap:anywhere; }",
    """    .compactProjectionMetric strong { display:block; margin-top:8px; color:#1b3741; font-size:18px; line-height:1.08; letter-spacing:-.04em; overflow-wrap:anywhere; }
    .compactProjectionMetric.remainingMetric {
      position:relative;
      overflow:hidden;
      background:linear-gradient(145deg, rgba(86,213,199,.15), rgba(255,255,255,.78));
    }
    .compactProjectionMetric.remainingMetric::after {
      content:"";
      position:absolute;
      right:-34px;
      bottom:-44px;
      width:96px;
      height:96px;
      border-radius:50%;
      background:radial-gradient(circle, rgba(86,213,199,.20), transparent 68%);
      pointer-events:none;
    }
    .remainingLabel { display:flex !important; align-items:center; gap:7px; }
    .remainingLabel::before {
      content:"";
      width:7px;
      height:7px;
      flex:0 0 7px;
      border-radius:50%;
      background:var(--primary-2);
      box-shadow:0 0 0 4px rgba(24,169,153,.12);
      animation:countdownPulse 1.2s ease-in-out infinite;
    }
    .liveCountdown {
      position:relative;
      z-index:1;
      display:flex !important;
      align-items:baseline;
      gap:2px;
      white-space:nowrap;
      color:#095f58 !important;
      font-family:"SFMono-Regular", Consolas, "Liberation Mono", monospace;
      font-variant-numeric:tabular-nums;
      overflow-wrap:normal !important;
    }
    .liveCountdown .countdownClock {
      font-size:clamp(18px,2.7vw,25px);
      font-weight:950;
      line-height:1;
      letter-spacing:-.075em;
    }
    .liveCountdown .countdownMs {
      min-width:31px;
      color:#3f7f79;
      font-size:11px;
      font-weight:900;
      letter-spacing:-.045em;
      opacity:.84;
    }
    @keyframes countdownPulse {
      0%,100% { transform:scale(.86); opacity:.58; }
      50% { transform:scale(1); opacity:1; }
    }""",
    "css cronômetro",
)

one(
    "      .compactProjectionMetric strong { font-size:16px; }",
    """      .compactProjectionMetric strong { font-size:16px; }
      .liveCountdown .countdownClock { font-size:18px; }
      .liveCountdown .countdownMs { min-width:28px; font-size:10px; }""",
    "css cronômetro mobile",
)

one(
    """    <div class="cards" id="cards"></div>
    <div class="empty" id="emptyState">Nenhuma máquina cadastrada.</div>""",
    """    <div class="cards" id="cards"></div>
    <div class="empty" id="emptyState">Nenhuma máquina cadastrada.</div>
    <div class="bottomAddWrap">
      <button class="btn btnPrimary bottomAddBtn" id="addMachineBottomBtn" type="button">
        <span class="addButtonIcon" aria-hidden="true">＋</span>
        <span>Adicionar máquina</span>
      </button>
    </div>""",
    "html botão inferior",
)

one(
    """            <div class="compactProjectionMetric">
              <span>Restante</span>
              <strong data-role="projectionRest">-</strong>
            </div>""",
    """            <div class="compactProjectionMetric remainingMetric">
              <span class="remainingLabel">Restante</span>
              <strong class="liveCountdown" data-role="projectionRest" aria-label="Tempo restante">
                <span class="countdownClock" data-role="countdownClock">--:--:--</span>
                <small class="countdownMs" data-role="countdownMs">.---</small>
              </strong>
            </div>""",
    "html cronômetro",
)

one(
    "      V7 — horário-base individual + previsão fixa + remaining time em tempo real",
    "      V8 — botão inferior + cronômetro detalhado em tempo real",
    "comentário versão",
)

one(
    """      9. Zoom por pinça, duplo toque e foco de campo bloqueado no iPhone.
    */""",
    """      9. Zoom por pinça, duplo toque e foco de campo bloqueado no iPhone.
      10. Botão para adicionar máquina também abaixo do último card.
      11. Tempo restante em HH:MM:SS.mmm com atualização visual contínua.
    */""",
    "comentário melhorias",
)

one(
    """    function formatMinutes(totalMin) {
      if (totalMin == null || !Number.isFinite(totalMin)) return "-";
      const min = totalMin > 0 ? Math.ceil(totalMin) : 0;
      return `${Math.floor(min / 60)}h ${pad2(min % 60)}min`;
    }

    function formatCycle(minutes) {""",
    """    function formatMinutes(totalMin) {
      if (totalMin == null || !Number.isFinite(totalMin)) return "-";
      const min = totalMin > 0 ? Math.ceil(totalMin) : 0;
      return `${Math.floor(min / 60)}h ${pad2(min % 60)}min`;
    }

    function formatCountdownParts(totalMs) {
      const safeMs = Number.isFinite(totalMs) ? Math.max(0, Math.floor(totalMs)) : 0;
      const hours = Math.floor(safeMs / 3600000);
      const minutes = Math.floor((safeMs % 3600000) / 60000);
      const seconds = Math.floor((safeMs % 60000) / 1000);
      const milliseconds = safeMs % 1000;
      return {
        clock: `${String(hours).padStart(2, "0")}:${pad2(minutes)}:${pad2(seconds)}`,
        milliseconds: String(milliseconds).padStart(3, "0")
      };
    }

    function formatCountdownShort(totalMs) {
      return formatCountdownParts(totalMs).clock;
    }

    function formatCycle(minutes) {""",
    "formatador cronômetro",
)

count = text.count("          restMin: 0,")
if count != 2:
    raise RuntimeError(f"restMin imediato: esperado 2, encontrado {count}")
text = text.replace("          restMin: 0,", "          restMin: 0,\n          restMs: 0,")

one(
    "      const restMin = Math.max(0, (endDT - nowDT) / 60000);",
    """      const restMs = Math.max(0, endDT.getTime() - nowDT.getTime());
      const restMin = restMs / 60000;""",
    "cálculo restMs",
)

one(
    """        endDT,
        restMin,
        forecastReached,""",
    """        endDT,
        restMin,
        restMs,
        forecastReached,""",
    "retorno restMs",
)

one(
    '        miniRest.textContent = calc.status === "reached" ? "Previsão atingida" : `${formatMinutes(calc.restMin)} restantes`;',
    '        miniRest.textContent = calc.status === "reached" ? "Previsão atingida" : `${formatCountdownShort(calc.restMs)} restantes`;',
    "mini contador",
)

one(
    """      renderNotice(root, calc);
      const requestBox = root.querySelector('[data-role="requestBox"]');""",
    """      updateCountdownDisplay(root, calc);
      renderNotice(root, calc);
      const requestBox = root.querySelector('[data-role="requestBox"]');""",
    "chamada cronômetro",
)

one(
    """    function refreshLiveRemaining() {
      const calcs = [];
      state.machines.forEach(machine => {
        const calc = calcMachine(machine);
        calcs.push(calc);
        const root = [...document.querySelectorAll(".machineCard")].find(card => card.dataset.id === machine.id);
        if (root) applyDynamicCard(root, machine, calc);
      });
      updateSummary(calcs);
      el.baseShift.textContent = shiftName(getShiftWindowFor(new Date()).id);
    }""",
    """    function refreshLiveRemaining() {
      const calcs = [];
      const cardsById = new Map(
        [...document.querySelectorAll(".machineCard")].map(card => [card.dataset.id, card])
      );
      state.machines.forEach(machine => {
        const calc = calcMachine(machine);
        calcs.push(calc);
        const root = cardsById.get(machine.id);
        if (root) applyDynamicCard(root, machine, calc);
      });
      updateSummary(calcs);
      el.baseShift.textContent = shiftName(getShiftWindowFor(new Date()).id);
    }""",
    "refresh otimizado",
)

one(
    """    function renderNotice(root, calc) {
      const card = root.querySelector('[data-role="projectionCard"]');""",
    """    function updateCountdownDisplay(root, calc) {
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
    }

    function renderNotice(root, calc) {
      const card = root.querySelector('[data-role="projectionCard"]');""",
    "função display cronômetro",
)

one("      const rest = root.querySelector('[data-role=\"projectionRest\"]');\n", "", "remover rest antigo")
one('        rest.textContent = "-";\n', "", "remover rest inválido")
one("      rest.textContent = formatMinutes(calc.restMin);\n", "", "remover rest minutos")

one(
    """    document.querySelector("#addMachineBtn").addEventListener("click", () => {
      state.machines.forEach(machine => machine.collapsed = true);
      const newMachine = DEFAULT_MACHINE();
      newMachine.collapsed = false;
      state.machines.push(newMachine);
      render();
    });""",
    """    function addMachine() {
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
    document.querySelector("#addMachineBottomBtn").addEventListener("click", addMachine);""",
    "botões add compartilhados",
)

one(
    """    blockIOSZoom();
    render();
    updateLiveClock();
    setInterval(() => {
      updateLiveClock();
      refreshLiveRemaining();
    }, 1000);""",
    """    blockIOSZoom();
    render();
    updateLiveClock();
    setInterval(updateLiveClock, 1000);
    setInterval(refreshLiveRemaining, 50);""",
    "intervalos",
)

required = [
    'id="addMachineBottomBtn"',
    "formatCountdownParts",
    "restMs",
    "countdownClock",
    "countdownMs",
    "setInterval(refreshLiveRemaining, 50)",
]
for token in required:
    if token not in text:
        raise RuntimeError(f"ausente: {token}")

path.write_bytes(text.replace("\n", newline).encode("utf-8"))
print("V8 aplicada com sucesso.")
