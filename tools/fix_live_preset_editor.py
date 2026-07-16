from pathlib import Path
import re

path = Path('index.html')
raw = path.read_bytes()
newline = '\r\n' if b'\r\n' in raw else '\n'
text = raw.decode('utf-8').replace('\r\n','\n')

if 'data-v14-preset-editor' not in text:
    pattern = r'(\s*<div data-v111-preview>\$\{compactEditorPreview\(machine\)\}</div>)\s*\$\{renderPresetEditorV13\(machine, calcMachine\(machine\)\)\}'
    replacement = r'\1\n             <div class="presetEditorSlotV14" data-v14-preset-editor>${renderPresetEditorV13(machine, calcMachine(machine))}</div>'
    text, count = re.subn(pattern, replacement, text, count=1)
    assert count == 1, 'montagem atual do Preset não encontrada'

anchor = "    function renderMachineEditor(machine, calc) {"
helper = '''    function bindPresetEditorV14(machine, slot) {
      slot.querySelectorAll('[data-v10-action]').forEach(button => {
        button.onclick = () => handleMachineScreenAction(button, machine);
      });
      slot.querySelectorAll('[data-v10-field]').forEach(input => {
        const savePresetField = () => {
          machine[input.dataset.v10Field] = input.value;
          saveState();
        };
        input.addEventListener('input', savePresetField);
        input.addEventListener('change', savePresetField);
      });
    }

    function refreshPresetEditorV14(machine) {
      if (machineScreenMode !== 'edit') return;
      const slot = machineScreenContent.querySelector('[data-v14-preset-editor]');
      if (!slot) return;
      const html = renderPresetEditorV13(machine, calcMachine(machine));
      if (slot.innerHTML === html) return;
      slot.innerHTML = html;
      bindPresetEditorV14(machine, slot);
    }

'''
assert anchor in text
if 'function refreshPresetEditorV14(machine)' not in text:
    text = text.replace(anchor, helper + anchor, 1)

assert 'data-v14-preset-editor' in text
assert text.count('function refreshPresetEditorV14(machine)') == 1
assert 'refreshPresetEditorV14(machine);' in text

path.write_bytes(text.replace('\n', newline).encode('utf-8'))
