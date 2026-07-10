from pathlib import Path

path = Path('index.html')
raw = path.read_bytes()
newline = '\r\n' if b'\r\n' in raw else '\n'
text = raw.decode('utf-8').replace('\r\n','\n').replace('\r','\n')

def one(old,new,label):
    global text
    c=text.count(old)
    if c!=1: raise RuntimeError(f'{label}: {c}')
    text=text.replace(old,new,1)

one('<title>Tempo da Linha | VENANC Tools V9.1</title>','<title>Tempo da Linha | VENANC Tools V9.2</title>','title')

one('''    .machineCard.emptyMachine .cardHead { border-bottom:0; }
    .machineCard.emptyMachine .cardMini .dot,
    .machineCard.emptyMachine [data-role="miniEnd"] { display:none; }
    .machineCard.emptyMachine .cardHead { cursor:pointer; }
    .machineCard.emptyMachine .machineToken { min-width:64px; }''','''    .machineCard.emptyMachine .cardHead { border-bottom:0; cursor:pointer; }
    .machineCard.emptyMachine .cardMini { display:none; }
    .machineCard.emptyMachine .machineToken { min-width:64px; }
    .machineCard.emptyMachine .cardIdentity { display:flex; align-items:center; }
    .cardCountdown {
      display:inline-flex;
      align-items:baseline;
      gap:2px;
      color:#294751;
      font-family:"SFMono-Regular",Consolas,"Liberation Mono",monospace;
      font-variant-numeric:tabular-nums;
      white-space:nowrap;
    }
    .cardCountdown .clockMain { font-size:15px; font-weight:950; letter-spacing:-.06em; }
    .cardCountdown .clockMs { color:#6d878f; font-size:10px; font-weight:900; }
    .cardPrediction { color:#768991; font-size:12px; font-weight:800; }
    .machineCard:not(.emptyMachine) .cardMini { margin-top:7px; row-gap:4px; }
    .machineCard:not(.emptyMachine) .cardIdentity { min-width:0; }''','empty css')

one('''            <div class="cardName">
              <strong>TNL <span data-role="titleMachine">-</span></strong>
              <span class="badge" data-role="statusBadge">Aguardando dados</span>
            </div>
            <div class="cardMini">
              <span class="miniText" data-role="miniRest">Preencha os dados</span>
              <span class="dot">•</span>
              <span class="miniText" data-role="miniEnd">Sem previsão</span>
            </div>''','''            <div class="cardName">
              <span class="badge" data-role="statusBadge">Aguardando dados</span>
            </div>
            <div class="cardMini">
              <span class="cardCountdown" data-role="miniRest"><span class="clockMain">--:--:--</span><small class="clockMs">.---</small></span>
              <span class="dot">•</span>
              <span class="cardPrediction" data-role="miniEnd">Sem previsão</span>
            </div>''','template header')

one('''        ok: ["Estável", "ok", "ok", "Não encerra no turno atual nem no próximo."]''','''        ok: ["Não encerra", "ok", "ok", "Não encerra no turno atual nem no próximo."]''','status ok')
one('''        now: ["Neste turno", "bad", "bad", "Vai encerrar neste turno."],
        next: ["Próximo turno", "warn", "warn", "Vai encerrar no próximo turno."],''','''        now: ["Encerra neste turno", "bad", "bad", "Vai encerrar neste turno."],
        next: ["Encerra no próximo turno", "warn", "warn", "Vai encerrar no próximo turno."],''','status labels')

one('''      node.querySelector('[data-role="titleMachine"]').textContent = machine.machine || '-';
      node.querySelector('[data-role="machineToken"]').textContent = machine.machine || '--';''','''      node.querySelector('[data-role="machineToken"]').textContent = machine.machine || '--';''','remove duplicate title')

one('''      if (calc.valid && calc.endDT) {
        miniRest.textContent = calc.status === "reached" ? "Previsão atingida" : `${formatCountdownShort(calc.restMs)} restantes`;
        miniEnd.textContent = `previsão fixa ${fmtDate(calc.endDT)} às ${fmtTime(calc.endDT)}`;
      } else {
        miniRest.textContent = "Preencha os dados da máquina";
        miniEnd.textContent = "Sem previsão calculada";
      }''','''      if (calc.valid && calc.endDT) {
        const parts = formatCountdownParts(calc.restMs);
        miniRest.innerHTML = `<span class="clockMain">${parts.clock}</span><small class="clockMs">.${parts.milliseconds}</small>`;
        miniRest.setAttribute("aria-label", `${parts.clock}.${parts.milliseconds} restantes`);
        miniEnd.textContent = `Previsão ${fmtDate(calc.endDT)} às ${fmtTime(calc.endDT)}`;
      } else {
        miniRest.innerHTML = `<span class="clockMain">--:--:--</span><small class="clockMs">.---</small>`;
        miniEnd.textContent = "";
      }''','dynamic header')

one('''      input.addEventListener("change", () => {
        machine[field] = input.value;
        clearTimeout(liveRenderTimer);
        render();
      });''','''      input.addEventListener("change", () => {
        machine[field] = input.value;
        clearTimeout(liveRenderTimer);
        saveState();
        const calc = calcMachine(machine);
        applyDynamicCard(root, machine, calc);
        const preview = root.querySelector('[data-role="mpPreview"]');
        if (preview) preview.textContent = `Capacidade com MP: ${calc.capacity} ${plural(calc.capacity, "peça", "peças")} · ${calc.perBar} por barra`;
      });''','field focus fix')

one('''        input.addEventListener("change", () => {
          machine.trays[index] = input.value;
          render();
        });''','''        input.addEventListener("change", () => {
          machine.trays[index] = input.value;
          saveState();
          applyDynamicCard(root, machine, calcMachine(machine));
        });''','tray focus fix')

required=['VENANC Tools V9.2','Não encerra','Encerra neste turno','clockMain','applyDynamicCard(root, machine, calc);']
for token in required:
    if token not in text: raise RuntimeError(f'ausente {token}')
path.write_bytes(text.replace('\n',newline).encode('utf-8'))
print('V9.2 aplicada')
