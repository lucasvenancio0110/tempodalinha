from pathlib import Path

path = Path('index.html')
raw = path.read_bytes()
newline = '\r\n' if b'\r\n' in raw else '\n'
text = raw.decode('utf-8').replace('\r\n', '\n').replace('\r', '\n')

text = text.replace('VENANC Tools V11.1.01', 'VENANC Tools V11.1.02', 1)

css = r'''

    /* V11.1.02 — editor reorganizado, separado e rolável */
    .machineScreenContent {
      overflow-x:hidden;
      overflow-y:auto;
      -webkit-overflow-scrolling:touch;
      overscroll-behavior:contain;
    }
    .compactOperatorV111.operatorForm {
      height:auto !important;
      min-height:100%;
      display:block !important;
    }
    .compactOperatorV111 .operatorIntro {
      position:relative;
      z-index:1;
      margin:0 0 14px;
      padding:0 2px;
    }
    .compactOperatorV111 .compactGridV111 {
      display:grid !important;
      grid-template-columns:repeat(2,minmax(0,1fr)) !important;
      grid-template-rows:none !important;
      grid-auto-rows:max-content !important;
      align-content:start !important;
      gap:12px !important;
      height:auto !important;
      min-height:0 !important;
      overflow:visible !important;
      padding-bottom:18px;
    }
    .compactOperatorV111 .compactGridV111 > * {
      position:static !important;
      inset:auto !important;
      transform:none !important;
      min-width:0;
      margin:0 !important;
      align-self:auto !important;
    }
    .compactOperatorV111 .compactGridV111 .operatorField {
      min-height:104px !important;
      height:auto !important;
      display:flex !important;
      flex-direction:column;
      justify-content:center !important;
      overflow:hidden !important;
      padding:13px 14px !important;
      border:1px solid rgba(255,255,255,.09) !important;
      border-radius:18px !important;
      background:linear-gradient(145deg,rgba(255,255,255,.065),rgba(255,255,255,.028)) !important;
      box-shadow:inset 0 1px 0 rgba(255,255,255,.035),0 10px 26px rgba(0,0,0,.10);
    }
    .compactOperatorV111 .compactGridV111 .operatorField label {
      position:static !important;
      display:block !important;
      min-height:0 !important;
      margin:0 0 8px !important;
      padding:0 !important;
      line-height:1.15 !important;
      color:#8fa6ad;
      font-size:10px !important;
      letter-spacing:.11em;
      white-space:normal;
    }
    .compactOperatorV111 .compactGridV111 .operatorInput {
      position:relative !important;
      display:block;
      width:100% !important;
      min-width:0 !important;
      min-height:42px !important;
      height:42px !important;
      margin:0 !important;
      padding:2px 0 7px !important;
      font-size:clamp(25px,7vw,31px) !important;
      line-height:1 !important;
    }
    .compactOperatorV111 .compactGridV111 .mpModeTabs {
      position:static !important;
      display:grid !important;
      grid-template-columns:repeat(3,minmax(0,1fr));
      gap:6px;
      margin:9px 0 0 !important;
    }
    .compactOperatorV111 .compactGridV111 .mpModeTab {
      min-width:0;
      min-height:34px;
      height:34px;
      padding:0 5px;
      font-size:9px;
    }
    .compactOperatorV111 .compactBarsV111 {
      grid-column:1/-1 !important;
      min-height:88px !important;
    }
    .compactOperatorV111 .compactBarsV111 .barCounter {
      position:static !important;
      display:grid !important;
      grid-template-columns:48px minmax(0,1fr) 48px !important;
      align-items:center;
      gap:12px;
      min-height:48px;
      margin:0 !important;
    }
    .compactOperatorV111 .compactBarsV111 .barCounter button {
      position:static !important;
      width:48px !important;
      height:48px !important;
      border-radius:14px;
    }
    .compactOperatorV111 .compactBarsV111 .barCounter strong {
      position:static !important;
      font-size:31px !important;
      line-height:1;
    }
    .compactOperatorV111 .compactOptionalV111,
    .compactOperatorV111 [data-v111-preview],
    .compactOperatorV111 .presetPanelV11 {
      grid-column:1/-1 !important;
      position:static !important;
      width:100%;
      clear:both;
    }
    .compactOperatorV111 .compactOptionalV111 {
      margin-top:2px !important;
      border-radius:16px;
    }
    .compactOperatorV111 [data-v111-preview] {
      margin-top:2px !important;
    }
    .compactOperatorV111 .editorLiveResult {
      position:relative !important;
      min-height:0;
      padding:18px;
      border-radius:22px;
      box-shadow:0 18px 42px rgba(0,0,0,.13);
    }
    @media(max-width:420px){
      .compactOperatorV111 .compactGridV111 { gap:10px !important; }
      .compactOperatorV111 .compactGridV111 .operatorField {
        min-height:98px !important;
        padding:12px !important;
      }
      .compactOperatorV111 .compactGridV111 .operatorInput {
        font-size:25px !important;
      }
    }
    @media(max-width:350px){
      .compactOperatorV111 .compactGridV111 {
        grid-template-columns:1fr !important;
      }
      .compactOperatorV111 .compactBarsV111,
      .compactOperatorV111 .compactOptionalV111,
      .compactOperatorV111 [data-v111-preview],
      .compactOperatorV111 .presetPanelV11 {
        grid-column:1 !important;
      }
    }
'''

if '</style>' not in text:
    raise RuntimeError('fechamento de style não encontrado')
text = text.replace('</style>', css + '\n  </style>', 1)

required = [
    'VENANC Tools V11.1.02',
    'overflow-y:auto',
    'grid-auto-rows:max-content',
    '.compactOperatorV111 .compactBarsV111',
    'grid-column:1/-1 !important'
]
for marker in required:
    if marker not in text:
        raise RuntimeError(f'marcador ausente: {marker}')

path.write_bytes(text.replace('\n', newline).encode('utf-8'))
print('V11.1.02 aplicada com sucesso.')
