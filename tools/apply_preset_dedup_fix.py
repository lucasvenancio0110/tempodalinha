from pathlib import Path
import re

path = Path('index.html')
raw = path.read_bytes()
newline = '\r\n' if b'\r\n' in raw else '\n'
text = raw.decode('utf-8').replace('\r\n', '\n')

text = text.replace('O setor do Preset já trouxe a nova OP?', 'Preset recebido?')

editor_start = text.rfind('    function renderMachineEditor(machine, calc) {')
editor_end = text.find('\n    function ', editor_start + 20)
if editor_start < 0 or editor_end < 0:
    raise SystemExit('renderMachineEditor não encontrado')
editor = text[editor_start:editor_end]
editor = re.sub(r'\$\{renderPreset(?:EditorV13|V11)\(machine, calc\)\}', '', editor)
preview_marker = '<div data-v111-preview>${compactEditorPreview(machine)}</div>'
if preview_marker not in editor:
    raise SystemExit('prévia do editor não encontrada')
editor = editor.replace(preview_marker, preview_marker + '${renderPresetEditorV13(machine, calc)}', 1)
text = text[:editor_start] + editor + text[editor_end:]

result_start = text.rfind('    function renderMachineResult(machine, calc) {')
result_end = text.find('\n    function ', result_start + 20)
if result_start < 0 or result_end < 0:
    raise SystemExit('renderMachineResult não encontrado')
result = text[result_start:result_end]
result = re.sub(r'\$\{renderPreset(?:DashboardV13|V11)\(machine, calc\)\}', '', result)
close_marker = '        </section>`;'
pos = result.rfind(close_marker)
if pos < 0:
    raise SystemExit('fim do dashboard não encontrado')
result = result[:pos] + '        ${renderPresetDashboardV13(machine, calc)}\n' + result[pos:]
text = text[:result_start] + result + text[result_end:]

css = '''\n\n    /* PULSE CNC - correcao de duplicacao do Preset */\n    .presetMissionHeadV12 strong { max-width:230px; font-size:17px; line-height:1.15; }\n    .presetMissionHeadV12 { align-items:flex-start; }\n    @media (max-width:560px) {\n      .presetMissionHeadV12 strong { max-width:180px; font-size:16px; }\n    }\n'''
if 'correcao de duplicacao do Preset' not in text:
    text = text.replace('</style>', css + '\n  </style>', 1)

path.write_bytes(text.replace('\n', newline).encode('utf-8'))
