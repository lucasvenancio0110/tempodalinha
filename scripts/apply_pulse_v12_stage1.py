from pathlib import Path
import re

path = Path('index.html')
raw = path.read_bytes()
newline = '\r\n' if b'\r\n' in raw else '\n'
text = raw.decode('utf-8').replace('\r\n', '\n').replace('\r', '\n')

# Identidade principal.
text = re.sub(r'<title>.*?</title>', '<title>PULSE CNC | V12.0.0</title>', text, count=1)
text = text.replace('TEMPO DA LINHA — VENANC Tools', 'PULSE CNC')
text = text.replace('<div class="mark" aria-hidden="true">TL</div>', '<div class="mark pulseMark" aria-hidden="true">P</div>', 1)
text = text.replace('<h1>Defina a linha</h1>\n          <p>Toque na célula para abrir as máquinas correspondentes.</p>', '<h1>PULSE CNC</h1>\n          <p>Selecione a célula.</p>', 1)
text = text.replace('<strong>TEMPO DA LINHA</strong>\n          <span>VENANC Tools</span>', '<strong>PULSE CNC</strong>', 1)
text = text.replace('id="settingsBtn" type="button">⚙ Ajustes', 'id="settingsBtn" type="button">Ajustes')
text = text.replace('id="whatsBtn" type="button">↗ Enviar resumo', 'id="whatsBtn" type="button">Enviar resumo')

# Configurações padrão solicitadas.
text = text.replace('kerfWidth: 2,', 'kerfWidth: 1,', 1)
settings_anchor = '''      requestLimit: 16,\n      turnMinutes: 480'''
if settings_anchor in text:
    text = text.replace(settings_anchor, '''      requestLimit: 16,\n      turnMinutes: 480,\n      gabaritoMode: "individual"''', 1)
elif 'gabaritoMode: "individual"' not in text:
    raise RuntimeError('Não foi possível adicionar o modo padrão individual')

text = text.replace('''              <option value="sum">Soma rápida: 60+40+39+22</option>\n              <option value="individual">Campos individuais</option>''', '''              <option value="individual">Campos individuais</option>\n              <option value="sum">Soma rápida: 60+40+39+22</option>''', 1)
text = text.replace("state.settings.gabaritoMode || 'sum'", "state.settings.gabaritoMode || 'individual'")
text = text.replace('''            <label>Regra de encerramento</label>\n            <div class="fixedRuleText">🟥 menos de 8h · 🟧 menos de 16h</div>''', '''            <label>Regra de encerramento</label>\n            <div class="fixedRuleText">Vermelho: neste turno · Laranja: próximo turno · Verde: produção normal</div>''', 1)

# Nome em textos de relatório e interface, sem alterar a chave de armazenamento.
text = text.replace('Tempo da Linha', 'PULSE CNC')
text = text.replace('VENANC Tools', '')
text = re.sub(r'PULSE CNC\s*[|—-]\s*PULSE CNC', 'PULSE CNC', text)

# Camada visual da primeira etapa: cabeçalho compacto, identidade e cores sem emojis.
css = r'''

    /* PULSE CNC V12.0.0 — Etapa 1: identidade e visão da célula */
    :root {
      --pulse-green:#29b877;
      --pulse-green-soft:rgba(41,184,119,.12);
      --pulse-orange:#f1a43b;
      --pulse-orange-soft:rgba(241,164,59,.13);
      --pulse-red:#ef5b66;
      --pulse-red-soft:rgba(239,91,102,.13);
      --pulse-action:#5e8df7;
    }
    .pulseMark,
    .brandRow .mark {
      border-radius:14px;
      color:#07151a;
      background:linear-gradient(145deg,#72e6d8,#36bcae);
      border-color:rgba(114,230,216,.55);
      box-shadow:0 10px 26px rgba(54,188,174,.20);
      font-size:20px;
      letter-spacing:-.08em;
    }
    .brandRow .mark svg { display:none; }
    .brandTitle strong { font-size:19px; letter-spacing:.065em; }
    .brandTitle span { display:none; }
    .appHeader { background:rgba(8,14,19,.95); }
    .headerInner { padding:10px 14px; gap:10px; }
    .brandRow { gap:9px; }
    .brandRow .mark { width:40px; height:40px; }
    .toolbar { flex-wrap:nowrap; gap:6px; }
    .toolbar .btn { min-height:38px; padding:0 10px; font-size:11px; }
    .cellIndicator { max-width:92px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
    main { padding-top:13px; }
    .compactControl {
      min-height:0; padding:10px 12px; border-radius:15px; margin-bottom:10px;
      background:linear-gradient(145deg,rgba(255,255,255,.055),rgba(255,255,255,.025));
    }
    .compactClockBlock strong { font-size:14px; }
    .compactLabel { font-size:8px; }
    .cellOverviewV11 { padding:12px; border-radius:16px; }
    .cellStatsV11 { gap:6px; }
    .cellStatsV11 div { padding:8px; }
    .cellMachineProgressV11 { margin-top:8px; }
    .machineCard { border-radius:15px; overflow:hidden; }
    .machineCard .cardHead { min-height:68px; padding:10px 12px; }
    .machineToken { min-width:52px; height:44px; border-radius:12px; font-size:18px; }
    .machineCard:not(.emptyMachine) .cardMini { margin-top:4px; }
    .cardCountdown .clockMain { font-size:16px; }
    .cardPrediction { font-size:10px; }
    .machineCard.status-ok,
    .machineCard[data-status="ok"] { border-left:4px solid var(--pulse-green); }
    .machineCard.status-warn,
    .machineCard[data-status="warn"] { border-left:4px solid var(--pulse-orange); }
    .machineCard.status-bad,
    .machineCard[data-status="bad"] { border-left:4px solid var(--pulse-red); }
    .badge.ok { color:var(--pulse-green); background:var(--pulse-green-soft); }
    .badge.warn { color:var(--pulse-orange); background:var(--pulse-orange-soft); }
    .badge.bad { color:var(--pulse-red); background:var(--pulse-red-soft); }
    .queueMachine.is-filled.status-ok { color:var(--pulse-green); border-color:rgba(41,184,119,.36); }
    .queueMachine.is-filled.status-warn { color:var(--pulse-orange); border-color:rgba(241,164,59,.40); }
    .queueMachine.is-filled.status-bad { color:var(--pulse-red); border-color:rgba(239,91,102,.40); }
    @media(max-width:620px){
      .headerInner { align-items:center; }
      .brandTitle strong { font-size:16px; }
      .brandRow .mark { width:36px; height:36px; font-size:18px; }
      .toolbar .btn { min-height:35px; padding:0 8px; font-size:10px; }
      #activeCellLabel { display:none; }
      main { padding:10px 10px 90px; }
      .compactControl { padding:9px 10px; }
      .cellOverviewTop strong { font-size:16px; }
      .cellStatsV11 strong { font-size:16px; }
    }
'''
if '</style>' not in text:
    raise RuntimeError('Fechamento de style não encontrado')
text = text.replace('</style>', css + '\n  </style>', 1)

# Manifesto PWA embutido quando ainda não existe um manifest externo.
if 'rel="manifest"' not in text:
    manifest_script = r'''
  <script>
    (() => {
      const manifest = {
        name: 'PULSE CNC',
        short_name: 'PULSE CNC',
        start_url: './',
        display: 'standalone',
        background_color: '#0b1117',
        theme_color: '#07141c'
      };
      const blob = new Blob([JSON.stringify(manifest)], { type: 'application/manifest+json' });
      const link = document.createElement('link');
      link.rel = 'manifest';
      link.href = URL.createObjectURL(blob);
      document.head.appendChild(link);
    })();
  </script>
'''
    text = text.replace('</body>', manifest_script + '\n</body>', 1)

required = [
    '<title>PULSE CNC | V12.0.0</title>',
    '<strong>PULSE CNC</strong>',
    'kerfWidth: 1',
    'gabaritoMode: "individual"',
    '<option value="individual">Campos individuais</option>',
    'PULSE CNC V12.0.0 — Etapa 1'
]
for marker in required:
    if marker not in text:
        raise RuntimeError(f'Marcador ausente: {marker}')

path.write_bytes(text.replace('\n', newline).encode('utf-8'))
print('PULSE CNC V12 etapa 1 aplicada com sucesso.')
