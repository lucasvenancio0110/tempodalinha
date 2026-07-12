from pathlib import Path

path = Path('index.html')
raw = path.read_bytes()
newline = '\r\n' if b'\r\n' in raw else '\n'
text = raw.decode('utf-8').replace('\r\n', '\n').replace('\r', '\n')

text = text.replace('VENANC Tools V11.1.00', 'VENANC Tools V11.1.01', 1)

anchor = '''    @media(max-width:560px){
      .compactGridV111 .operatorField { min-height:108px; padding:12px 13px; }
      .compactGridV111 .operatorInput { font-size:25px; }
      .editorResultMetrics { grid-template-columns:repeat(2,minmax(0,1fr)); }
    }
'''

replacement = '''    @media(max-width:560px){
      .compactGridV111 .operatorField { min-height:0; padding:10px 11px; }
      .compactGridV111 .operatorInput { font-size:24px; }
      .editorResultMetrics { grid-template-columns:repeat(2,minmax(0,1fr)); }
    }

    /* V11.1.01 — correção estrutural do formulário compacto */
    .compactOperatorV111 .compactGridV111 {
      display:grid;
      grid-template-columns:repeat(2,minmax(0,1fr));
      grid-template-rows:none !important;
      grid-auto-flow:row;
      grid-auto-rows:auto;
      align-items:stretch;
      gap:8px !important;
    }
    .compactOperatorV111 .compactGridV111 > * {
      min-width:0;
      position:relative;
      inset:auto;
    }
    .compactOperatorV111 .compactGridV111 .operatorField {
      min-height:0 !important;
      height:auto !important;
      padding:10px 12px !important;
      overflow:visible;
      align-self:stretch;
    }
    .compactOperatorV111 .compactGridV111 .operatorField label {
      display:block;
      min-height:14px;
      margin:0 0 5px;
      line-height:1.2;
    }
    .compactOperatorV111 .compactGridV111 .operatorInput {
      width:100%;
      min-width:0;
      min-height:36px;
      height:auto;
      padding:3px 0 6px !important;
      line-height:1.05;
    }
    .compactOperatorV111 .compactGridV111 .mpModeTabs {
      display:grid;
      grid-template-columns:repeat(3,minmax(0,1fr));
      gap:5px;
      margin-top:6px;
    }
    .compactOperatorV111 .compactGridV111 .mpModeTab {
      min-width:0;
      min-height:32px;
      padding:0 5px;
      font-size:9px;
    }
    .compactOperatorV111 .compactBarsV111 {
      grid-column:1/-1;
      min-height:70px !important;
    }
    .compactOperatorV111 .compactBarsV111 .barCounter {
      min-height:42px;
      grid-template-columns:42px minmax(0,1fr) 42px !important;
    }
    .compactOperatorV111 .compactBarsV111 .barCounter button {
      width:42px;
      height:42px !important;
    }
    .compactOperatorV111 .compactBarsV111 .barCounter strong {
      font-size:27px !important;
    }
    .compactOperatorV111 .compactOptionalV111,
    .compactOperatorV111 [data-v111-preview],
    .compactOperatorV111 .presetPanelV11 {
      grid-column:1/-1;
    }
    @media(max-width:380px){
      .compactOperatorV111 .compactGridV111 { gap:7px !important; }
      .compactOperatorV111 .compactGridV111 .operatorField { padding:9px 10px !important; }
      .compactOperatorV111 .compactGridV111 .operatorInput { font-size:22px !important; }
    }
'''

if anchor not in text:
    raise RuntimeError('âncora CSS V11.1.00 não encontrada')
text = text.replace(anchor, replacement, 1)

required = [
    'VENANC Tools V11.1.01',
    'grid-template-rows:none !important',
    'grid-auto-rows:auto',
    '.compactOperatorV111 .compactBarsV111',
    'grid-column:1/-1'
]
for marker in required:
    if marker not in text:
        raise RuntimeError(f'marcador ausente: {marker}')

path.write_bytes(text.replace('\n', newline).encode('utf-8'))
print('V11.1.01 aplicada com sucesso.')
