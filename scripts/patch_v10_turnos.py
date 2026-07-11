from pathlib import Path

path = Path('index.html')
raw = path.read_bytes()
newline = '\r\n' if b'\r\n' in raw else '\n'
text = raw.decode('utf-8').replace('\r\n', '\n').replace('\r', '\n')

if 'class="pastProductionCompact"' in text:
    print('Campo de turnos passados já aplicado.')
    raise SystemExit(0)


def one(old: str, new: str, label: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'{label}: esperado 1, encontrado {count}')
    text = text.replace(old, new, 1)

one(
'''    .trayCompactRow { display:grid; grid-template-columns:1fr 32px; gap:5px; }''',
'''    .pastProductionCompact {
      grid-column:1/-1; display:grid; grid-template-columns:minmax(0,1fr) minmax(90px,.55fr); align-items:center; gap:8px;
      border:1px solid rgba(255,255,255,.08); border-radius:10px; padding:7px 9px; background:rgba(0,0,0,.10);
    }
    .pastProductionCompact label { color:#9eb3b8; font-size:8px; font-weight:950; letter-spacing:.08em; text-transform:uppercase; }
    .pastProductionCompact input { min-width:0; height:34px; border:1px solid rgba(255,255,255,.10); border-radius:9px; padding:0 9px; color:#effafa; background:rgba(255,255,255,.045); font-size:18px; font-weight:900; text-align:right; }
    .trayCompactRow { display:grid; grid-template-columns:1fr 32px; gap:5px; }''',
'estilo turnos passados'
)

one(
'''            <details class="optionalPanel" ${machine.traysCollapsed === false ? "open" : ""}><summary>Gabaritos — opcional <b>${trayCount}</b></summary><div class="optionalBody">${trays}<button class="addTrayCompact" data-v10-action="add-tray" type="button">Adicionar gabarito</button></div></details>''',
'''            <details class="optionalPanel" ${machine.traysCollapsed === false ? "open" : ""}><summary>Opcionais — turnos passados e gabaritos <b>${trayCount}</b></summary><div class="optionalBody"><div class="pastProductionCompact"><label>Produção dos turnos passados</label><input type="number" min="0" step="1" inputmode="numeric" data-v10-field="producedManual" value="${escapeHtml(String(machine.producedManual ?? ""))}" placeholder="0"></div>${trays}<button class="addTrayCompact" data-v10-action="add-tray" type="button">Adicionar gabarito</button></div></details>''',
'campo turnos passados'
)

for token in ['class="pastProductionCompact"', 'data-v10-field="producedManual"', 'Produção dos turnos passados', 'Adicionar gabarito']:
    if token not in text:
        raise RuntimeError(f'ausente: {token}')

path.write_bytes(text.replace('\n', newline).encode('utf-8'))
print('Campo de produção dos turnos passados aplicado.')
