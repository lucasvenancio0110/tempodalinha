from pathlib import Path
import re

path = Path('index.html')
raw = path.read_bytes()
newline = '\r\n' if b'\r\n' in raw else '\n'
text = raw.decode('utf-8').replace('\r\n','\n').replace('\r','\n')

text = text.replace('VENANC Tools V11.0.03', 'VENANC Tools V11.0.04')

old_focus = '''      requestAnimationFrame(() => {
        machineQueue.querySelector('.queueMachine.is-active')?.scrollIntoView({ behavior:"smooth", inline:"center", block:"nearest" });
        if (machineScreenMode === "edit") machineScreenContent.querySelector('[data-v10-field="timeInput"]')?.focus({ preventScroll:true });
      });'''
new_focus = '''      requestAnimationFrame(() => {
        machineQueue.querySelector('.queueMachine.is-active')?.scrollIntoView({ behavior:"smooth", inline:"center", block:"nearest" });
      });'''
if old_focus not in text:
    raise RuntimeError('bloco de foco automático não encontrado')
text = text.replace(old_focus, new_focus, 1)

old_field_focus = '''      machineScreenContent.querySelectorAll('.operatorField').forEach(fieldBox => {
        const editable = fieldBox.querySelector('.operatorInput:not([readonly]):not([disabled])');
        if (!editable) return;
        fieldBox.addEventListener('click', event => {
          if (event.target.closest('button, select, input') && event.target !== editable) return;
          if (document.activeElement !== editable) editable.focus({ preventScroll:false });
        });
      });
'''
if old_field_focus not in text:
    raise RuntimeError('foco artificial dos blocos não encontrado')
text = text.replace(old_field_focus, '', 1)

old_refresh = '''    function refreshLiveRemaining() {
      const calcs = [];'''
new_refresh = '''    function refreshLiveRemaining() {
      // Durante o preenchimento não atualiza a página atrás do popup.
      // Isso evita reconstruções e cálculos concorrendo com o toque nos inputs.
      if (typeof machineScreen !== "undefined" && machineScreen?.open && machineScreenMode === "edit") return;
      const calcs = [];'''
if old_refresh not in text:
    raise RuntimeError('refreshLiveRemaining não encontrado')
text = text.replace(old_refresh, new_refresh, 1)

if 'setInterval(refreshLiveRemaining, 50);' not in text:
    raise RuntimeError('intervalo de 50 ms não encontrado')
text = text.replace('setInterval(refreshLiveRemaining, 50);', 'setInterval(refreshLiveRemaining, 250);', 1)

# Evita reconstruir a fila de máquinas quando o estado visual não mudou.
old_row = '''      const row = document.querySelector('#v11MachineProgress');
      if (row) {
        row.innerHTML = '';
        state.machines.forEach((machine, index) => {
          const button = document.createElement('button');
          const calc = calcs[index];
          button.type = 'button';
          button.className = `cellMachineDotV11 ${calc.valid ? 'done' : ''} ${presetPendingV11(machine, calc) ? 'attention' : ''}`.trim();
          button.textContent = formatTnl(machine.machine);
          button.addEventListener('click', () => openMachineScreen(machine.id));
          row.appendChild(button);
        });
      }'''
new_row = '''      const row = document.querySelector('#v11MachineProgress');
      if (row) {
        const signature = state.machines.map((machine, index) => {
          const calc = calcs[index];
          return `${machine.id}:${calc.valid ? 1 : 0}:${presetPendingV11(machine, calc) ? 1 : 0}`;
        }).join('|');
        if (row.dataset.signature !== signature) {
          row.dataset.signature = signature;
          row.innerHTML = '';
          state.machines.forEach((machine, index) => {
            const button = document.createElement('button');
            const calc = calcs[index];
            button.type = 'button';
            button.className = `cellMachineDotV11 ${calc.valid ? 'done' : ''} ${presetPendingV11(machine, calc) ? 'attention' : ''}`.trim();
            button.textContent = formatTnl(machine.machine);
            button.addEventListener('click', () => openMachineScreen(machine.id));
            row.appendChild(button);
          });
        }
      }'''
if old_row not in text:
    raise RuntimeError('recriação da fila não encontrada')
text = text.replace(old_row, new_row, 1)

markers = [
    'VENANC Tools V11.0.04',
    'setInterval(refreshLiveRemaining, 250);',
    'machineScreenMode === "edit") return;',
    'row.dataset.signature !== signature'
]
for marker in markers:
    if marker not in text:
        raise RuntimeError(f'marcador ausente: {marker}')
if 'data-v10-field="timeInput"]\')?.focus' in text:
    raise RuntimeError('foco automático ainda presente')
if "querySelectorAll('.operatorField').forEach" in text:
    raise RuntimeError('foco artificial ainda presente')

path.write_bytes(text.replace('\n', newline).encode('utf-8'))
print('V11.0.04 aplicada com sucesso.')
