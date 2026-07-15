from pathlib import Path

path = Path('index.html')
raw = path.read_bytes()
newline = '\r\n' if b'\r\n' in raw else '\n'
text = raw.decode('utf-8').replace('\r\n', '\n')

editor_old = '''            <div data-v111-preview>${compactEditorPreview(machine)}</div>${renderPresetEditorV13(machine, calc)}
            ${renderPresetV11(machine, calcMachine(machine))}'''
editor_new = '''            <div data-v111-preview>${compactEditorPreview(machine)}</div>
            ${renderPresetEditorV13(machine, calcMachine(machine))}'''
assert editor_old in text, 'duplicação do editor não encontrada'
text = text.replace(editor_old, editor_new, 1)

result_old = '''          ${renderPresetV11(machine, calc)}
        ${renderPresetDashboardV13(machine, calc)}'''
result_new = '''          ${renderPresetDashboardV13(machine, calc)}'''
assert result_old in text, 'duplicação do dashboard não encontrada'
text = text.replace(result_old, result_new, 1)

text = text.replace('O setor do Preset já trouxe a nova OP?', 'Preset recebido?', 1)

editor_block = text[text.rfind('function renderMachineEditor'):text.rfind('function renderMachineResult')]
result_block = text[text.rfind('function renderMachineResult'):text.rfind('function bindMachineScreenEvents')]
assert editor_block.count('renderPresetEditorV13(') == 1
assert 'renderPresetV11(' not in editor_block
assert result_block.count('renderPresetDashboardV13(') == 1
assert 'renderPresetV11(' not in result_block

path.write_bytes(text.replace('\n', newline).encode('utf-8'))
