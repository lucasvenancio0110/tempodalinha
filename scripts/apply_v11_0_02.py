from pathlib import Path

path = Path('index.html')
raw = path.read_bytes()
newline = '\r\n' if b'\r\n' in raw else '\n'
text = raw.decode('utf-8').replace('\r\n','\n').replace('\r','\n')


def one(old, new, label):
    global text
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'{label}: esperado 1, encontrado {count}')
    text = text.replace(old, new, 1)

one('<title>Tempo da Linha | VENANC Tools V11.0.01</title>', '<title>Tempo da Linha | VENANC Tools V11.0.02</title>', 'versão')

one('''      document.addEventListener("dblclick", event => event.preventDefault(), { passive: false });
      let lastTouchEnd = 0;
      document.addEventListener("touchend", event => {
        const now = Date.now();
        if (now - lastTouchEnd <= 300) event.preventDefault();
        lastTouchEnd = now;
      }, { passive: false });''', '''      // Não bloqueia dblclick/touchend: isso impedia o primeiro toque nos campos do iPhone.
      // O zoom por pinça continua bloqueado pelas gestures e pelo touchmove com múltiplos dedos.''', 'bloqueio agressivo de toque')

one('''             <div class="operatorField cycleField"><label>1. Ciclo</label><input class="operatorInput" data-v10-field="timeInput" inputmode="decimal" value="${escapeHtml(String(machine.timeInput ?? ''))}" placeholder="2,24"></div>''', '''             <div class="operatorField cycleField"><label>1. Ciclo</label><input class="operatorInput" data-v10-field="timeInput" inputmode="decimal" enterkeyhint="next" value="${escapeHtml(String(machine.timeInput ?? ''))}" placeholder="2,24"></div>''', 'enter ciclo')
one('''<input class="operatorInput" data-v10-field="materialRemaining" inputmode="decimal"''', '''<input class="operatorInput" data-v10-field="materialRemaining" inputmode="decimal" enterkeyhint="next"''', 'enter material')
one('''<input class="operatorInput" data-v10-field="target" inputmode="numeric"''', '''<input class="operatorInput" data-v10-field="target" inputmode="numeric" enterkeyhint="next"''', 'enter meta')
one('''<input class="operatorInput" data-v10-field="pieceLength" inputmode="decimal"''', '''<input class="operatorInput" data-v10-field="pieceLength" inputmode="decimal" enterkeyhint="done"''', 'enter peça')

old_bind = '''    function bindMachineScreenEvents(machine) {
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
    }'''
new_bind = '''    function bindMachineScreenEvents(machine) {
      const mainInputs = [...machineScreenContent.querySelectorAll('[data-v10-field]')];
      mainInputs.forEach((input, index) => {
        input.addEventListener('pointerdown', event => event.stopPropagation());
        input.addEventListener('click', event => event.stopPropagation());
        input.addEventListener('input', () => {
          const field = input.dataset.v10Field;
          if (field === 'materialRemaining') {
            if (machine.barMode === 'partialMm') machine.partialMm = input.value; else machine.partialPieces = input.value;
          } else machine[field] = input.value;
          saveState();
        });
        input.addEventListener('change', () => { ensureExactStart(machine); saveState(); });
        input.addEventListener('keydown', event => {
          if (event.key !== 'Enter') return;
          event.preventDefault();
          const next = mainInputs.slice(index + 1).find(node => !node.readOnly && !node.disabled && node.offsetParent !== null);
          if (next) next.focus({ preventScroll: false });
          else input.blur();
        });
      });
      machineScreen.querySelectorAll('[data-v10-action]').forEach(button => { button.onclick = () => handleMachineScreenAction(button, machine); });
      machineScreenContent.querySelectorAll('[data-v10-tray]').forEach(input => {
        input.addEventListener('pointerdown', event => event.stopPropagation());
        input.addEventListener('click', event => event.stopPropagation());
        input.addEventListener('input', () => {
          machine.trays[Number(input.dataset.v10Tray)] = input.value;
          const total = syncPastProductionV11(machine);
          saveState();
          const totalNode = machineScreenContent.querySelector('.trayTotalV11 strong');
          const summaryNode = machineScreenContent.querySelector('.optionalPanel summary b');
          if (totalNode) totalNode.textContent = String(total);
          if (summaryNode) summaryNode.textContent = String(total);
        });
        input.addEventListener('change', () => { syncPastProductionV11(machine); ensureExactStart(machine); saveState(); });
        input.addEventListener('keydown', event => {
          if (event.key !== 'Enter') return;
          event.preventDefault();
          const trayInputs = [...machineScreenContent.querySelectorAll('[data-v10-tray]')];
          const next = trayInputs[trayInputs.indexOf(input) + 1];
          if (next) next.focus(); else input.blur();
        });
      });
      const details = machineScreenContent.querySelector('.optionalPanel');
      details?.addEventListener('toggle', () => { machine.traysCollapsed = !details.open; saveState(); });
    }'''
one(old_bind, new_bind, 'eventos do editor')

one("""      if (action === 'add-tray') { machine.trays.push(''); machine.traysCollapsed=false; saveState(); return renderMachineScreen(); }""", """      if (action === 'add-tray') {
        machine.trays.push(''); machine.traysCollapsed=false; saveState(); renderMachineScreen();
        requestAnimationFrame(() => {
          const inputs = machineScreenContent.querySelectorAll('[data-v10-tray]');
          inputs[inputs.length - 1]?.focus({ preventScroll:false });
        });
        return;
      }""", 'adicionar gabarito com foco')

one('''    /* V11.0.01 — operações, resultados e preset em 16 horas */''', '''    /* V11.0.02 — foco imediato e digitação fluida no iPhone */''', 'comentário versão')

for token in ['VENANC Tools V11.0.02', 'enterkeyhint="next"', "event.key !== 'Enter'", 'Não bloqueia dblclick/touchend', 'inputs[inputs.length - 1]?.focus']:
    if token not in text:
        raise RuntimeError(f'ausente: {token}')

path.write_bytes(text.replace('\n', newline).encode('utf-8'))
print('V11.0.02 aplicada com sucesso.')