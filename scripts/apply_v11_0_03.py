from pathlib import Path
import re

path = Path('index.html')
raw = path.read_bytes()
newline = '\r\n' if b'\r\n' in raw else '\n'
text = raw.decode('utf-8').replace('\r\n','\n').replace('\r','\n')

text = text.replace('VENANC Tools V11.0.02', 'VENANC Tools V11.0.03')
text = text.replace("        input.addEventListener('pointerdown', event => event.stopPropagation());\n", '')
text = text.replace("        input.addEventListener('click', event => event.stopPropagation());\n", '')

css_marker = '    .operatorInput:focus { border-bottom-color:#56d5c7; box-shadow:0 7px 0 -6px rgba(86,213,199,.55); }'
css_patch = css_marker + '''
    /* V11.0.03 — toque nativo e área inteira focável no iPhone */
    .operatorField { position:relative; touch-action:manipulation; }
    .operatorField label { pointer-events:none; }
    .operatorInput {
      position:relative; z-index:3; pointer-events:auto !important;
      touch-action:manipulation; -webkit-user-select:text; user-select:text;
    }
'''
if 'V11.0.03 — toque nativo' not in text:
    if css_marker not in text: raise RuntimeError('marcador CSS não encontrado')
    text = text.replace(css_marker, css_patch, 1)

bind_marker = "      const mainInputs = [...machineScreenContent.querySelectorAll('[data-v10-field]')];"
field_focus = bind_marker + '''
      machineScreenContent.querySelectorAll('.operatorField').forEach(fieldBox => {
        const editable = fieldBox.querySelector('.operatorInput:not([readonly]):not([disabled])');
        if (!editable) return;
        fieldBox.addEventListener('click', event => {
          if (event.target.closest('button, select, input') && event.target !== editable) return;
          if (document.activeElement !== editable) editable.focus({ preventScroll:false });
        });
      });'''
if "querySelectorAll('.operatorField').forEach" not in text:
    if bind_marker not in text: raise RuntimeError('marcador de eventos não encontrado')
    text = text.replace(bind_marker, field_focus, 1)

# Também remove qualquer bloqueio legado restante de duplo toque.
text = re.sub(r'\s*document\.addEventListener\("dblclick"[^;]+;\n?', '\n', text)
text = re.sub(r'\s*let lastTouchEnd = 0;.*?\}, \{ passive: false \}\);', '', text, flags=re.S)

for token in ['VENANC Tools V11.0.03', 'V11.0.03 — toque nativo', "querySelectorAll('.operatorField').forEach"]:
    if token not in text: raise RuntimeError(f'ausente: {token}')

path.write_bytes(text.replace('\n', newline).encode('utf-8'))
print('V11.0.03 aplicada.')
