from pathlib import Path

path = Path('index.html')
raw = path.read_bytes()
newline = '\r\n' if b'\r\n' in raw else '\n'
text = raw.decode('utf-8').replace('\r\n','\n')

old_render = '''            <div data-v111-preview>${compactEditorPreview(machine)}</div>
             ${renderPresetEditorV13(machine, calcMachine(machine))}'''
new_render = '''            <div data-v111-preview>${compactEditorPreview(machine)}</div>
             <div class="presetEditorSlotV14" data-v14-preset-editor>${renderPresetEditorV13(machine, calcMachine(machine))}</div>'''
assert old_render in text, 'montagem atual do Preset não encontrada'
text = text.replace(old_render, new_render, 1)

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
assert 'function refreshPresetEditorV14(machine)' not in text
text = text.replace(anchor, helper + anchor, 1)

assert 'data-v14-preset-editor' in text
assert 'function refreshPresetEditorV14(machine)' in text
assert 'refreshPresetEditorV14(machine);' in text

path.write_bytes(text.replace('\n', newline).encode('utf-8'))
