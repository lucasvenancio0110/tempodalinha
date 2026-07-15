from pathlib import Path

path = Path('index.html')
raw = path.read_bytes()
newline = '\r\n' if b'\r\n' in raw else '\n'
text = raw.decode('utf-8').replace('\r\n', '\n')

old = '''            <div data-v111-preview>${compactEditorPreview(machine)}</div>${renderPresetEditorV13(machine, calc)}
            ${renderPresetV11(machine, calcMachine(machine))}'''
new = '''            <div data-v111-preview>${compactEditorPreview(machine)}</div>
            ${renderPresetEditorV13(machine, calcMachine(machine))}'''
assert old in text, 'duplicação do Preset no editor não encontrada'
text = text.replace(old, new, 1)

editor = text[text.rfind('function renderMachineEditor'):text.rfind('function renderMachineResult')]
result = text[text.rfind('function renderMachineResult'):text.rfind('function bindMachineScreenEvents')]
assert editor.count('renderPresetEditorV13(') == 1
assert 'renderPresetV11(' not in editor
assert result.count('renderPresetDashboardV13(') == 1

path.write_bytes(text.replace('\n', newline).encode('utf-8'))
