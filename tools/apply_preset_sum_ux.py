from pathlib import Path

path = Path('index.html')
raw = path.read_bytes()
newline = '\r\n' if b'\r\n' in raw else '\n'
text = raw.decode('utf-8').replace('\r\n','\n')

# Preset deve depender do status real: encerra neste ou no próximo turno.
text = text.replace("    function presetRequiredV11(calc) {\n      return !!(calc && calc.valid && calc.restMin < 16 * 60);\n    }", "    function presetRequiredV11(calc) {\n      return !!(calc && calc.valid && ['now','next','reached'].includes(calc.status));\n    }")

# Soma rápida precisa abrir teclado com + disponível.
text = text.replace('input class="operatorInput" data-v111-tray-expression inputmode="numeric"', 'input class="operatorInput" data-v111-tray-expression type="text" inputmode="text" autocapitalize="off" autocomplete="off" spellcheck="false"')

# Preset do editor fica em contêiner próprio e usa cálculo atualizado.
text = text.replace('<div data-v111-preview>${compactEditorPreview(machine)}</div>\n             ${renderPresetEditorV13(machine, calcMachine(machine))}', '<div data-v111-preview>${compactEditorPreview(machine)}</div>\n             <div class="presetEditorSlotV14" data-v14-preset-editor>${renderPresetEditorV13(machine, calcMachine(machine))}</div>')

# Atualização segura do Preset ao preencher dados, sem duplicar o card.
anchor = "    function renderMachineEditor(machine, calc) {"
helper = '''    function refreshPresetEditorV14(machine) {\n      const slot = machineScreenContent.querySelector('[data-v14-preset-editor]');\n      if (!slot) return;\n      const html = renderPresetEditorV13(machine, calcMachine(machine));\n      if (slot.innerHTML !== html) {\n        slot.innerHTML = html;\n        slot.querySelectorAll('[data-v10-action]').forEach(button => { button.onclick = () => handleMachineScreenAction(button, machine); });\n        slot.querySelectorAll('[data-v10-field]').forEach(input => {\n          input.addEventListener('input', () => { machine[input.dataset.v10Field] = input.value; saveState(); });\n          input.addEventListener('change', () => { machine[input.dataset.v10Field] = input.value; saveState(); });\n        });\n      }\n    }\n\n'''
if helper.strip() not in text:
    text = text.replace(anchor, helper + anchor, 1)

# Atualiza o Preset junto com o preview durante o preenchimento.
text = text.replace('          updateCompactEditorPreview(machine);\n        });', '          updateCompactEditorPreview(machine);\n          refreshPresetEditorV14(machine);\n        });')
text = text.replace("        input.addEventListener('change', () => { ensureExactStart(machine); saveState(); updateCompactEditorPreview(machine); });", "        input.addEventListener('change', () => { ensureExactStart(machine); saveState(); updateCompactEditorPreview(machine); refreshPresetEditorV14(machine); });")

# Atualização ao vivo do editor também mantém o Preset coerente.
text = text.replace("        if (holder) holder.innerHTML = compactEditorPreview(machine);\n        return;", "        if (holder) holder.innerHTML = compactEditorPreview(machine);\n        refreshPresetEditorV14(machine);\n        return;")

css = '''\n\n    /* PULSE CNC — Preset e soma rápida V14 */\n    .compactOperatorV111 [data-v111-preview],\n    .compactOperatorV111 .presetEditorSlotV14,\n    .compactOperatorV111 .presetMissionV12 { grid-column: 1 / -1; width: 100%; min-width: 0; }\n    .presetEditorSlotV14:empty { display:none; }\n    .quickTrayField input[data-v111-tray-expression] { font-variant-numeric: tabular-nums; }\n'''
text = text.replace('</style>', css + '\n  </style>', 1)

assert "['now','next','reached'].includes(calc.status)" in text
assert 'data-v111-tray-expression type="text" inputmode="text"' in text
assert 'data-v14-preset-editor' in text
assert 'refreshPresetEditorV14(machine)' in text

path.write_bytes(text.replace('\n', newline).encode('utf-8'))
