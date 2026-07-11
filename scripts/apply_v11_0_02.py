from pathlib import Path
import re

path = Path('index.html')
raw = path.read_bytes()
newline = '\r\n' if b'\r\n' in raw else '\n'
text = raw.decode('utf-8').replace('\r\n','\n').replace('\r','\n')

text, n = re.subn(r'<title>Tempo da Linha \| VENANC Tools V11\.0\.01</title>', '<title>Tempo da Linha | VENANC Tools V11.0.02</title>', text, count=1)
if n != 1: raise RuntimeError(f'versão: {n}')

pattern_touch = r'''\n\s*document\.addEventListener\("dblclick", event => event\.preventDefault\(\), \{ passive: false \}\);\n\s*let lastTouchEnd = 0;\n\s*document\.addEventListener\("touchend", event => \{\n\s*const now = Date\.now\(\);\n\s*if \(now - lastTouchEnd <= 300\) event\.preventDefault\(\);\n\s*lastTouchEnd = now;\n\s*\}, \{ passive: false \}\);'''
replacement_touch = '''\n      // Não bloqueia dblclick/touchend: isso impedia o primeiro toque nos campos do iPhone.\n      // O zoom por pinça continua bloqueado pelas gestures e pelo touchmove com múltiplos dedos.'''
text, n = re.subn(pattern_touch, replacement_touch, text, count=1)
if n != 1: raise RuntimeError(f'bloqueio de toque: {n}')

for field, hint in [('timeInput','next'),('materialRemaining','next'),('target','next'),('pieceLength','done')]:
    pattern = rf'(<input class="operatorInput" data-v10-field="{field}"[^>]*?)(>)'
    match = re.search(pattern, text)
    if not match: raise RuntimeError(f'input ausente: {field}')
    if 'enterkeyhint=' not in match.group(1):
        replacement = match.group(1) + f' enterkeyhint="{hint}"' + match.group(2)
        text = text[:match.start()] + replacement + text[match.end():]

start = text.rfind("    function bindMachineScreenEvents(machine) {")
end = text.find("\n    function handleMachineScreenAction(button, machine) {", start)
if start < 0 or end < 0: raise RuntimeError('bloco bind não encontrado')
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
          if (next) next.focus({ preventScroll:false }); else input.blur();
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
          if (next) next.focus({ preventScroll:false }); else input.blur();
        });
      });
      const details = machineScreenContent.querySelector('.optionalPanel');
      details?.addEventListener('toggle', () => { machine.traysCollapsed = !details.open; saveState(); });
    }
'''
text = text[:start] + new_bind + text[end:]

old_add = "      if (action === 'add-tray') { machine.trays.push(''); machine.traysCollapsed=false; saveState(); return renderMachineScreen(); }"
new_add = '''      if (action === 'add-tray') {
        machine.trays.push(''); machine.traysCollapsed=false; saveState(); renderMachineScreen();
        requestAnimationFrame(() => {
          const inputs = machineScreenContent.querySelectorAll('[data-v10-tray]');
          inputs[inputs.length - 1]?.focus({ preventScroll:false });
        });
        return;
      }'''
if old_add not in text: raise RuntimeError('ação adicionar gabarito ausente')
text = text.replace(old_add, new_add, 1)

text = text.replace('/* V11.0.01 — operações, resultados e preset em 16 horas */', '/* V11.0.02 — foco imediato e digitação fluida no iPhone */', 1)

for token in ['VENANC Tools V11.0.02','enterkeyhint="next"',"event.key !== 'Enter'",'Não bloqueia dblclick/touchend','inputs[inputs.length - 1]?.focus']:
    if token not in text: raise RuntimeError(f'ausente: {token}')

path.write_bytes(text.replace('\n', newline).encode('utf-8'))
print('V11.0.02 aplicada com sucesso.')