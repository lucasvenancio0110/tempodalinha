from pathlib import Path

path = Path("index.html")
raw = path.read_bytes()
newline = "\r\n" if b"\r\n" in raw else "\n"
text = raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")

replacements = {
    "<title>Tempo da Linha | VENANC Tools V11.1.02</title>": "<title>PULSE CNC | 1.0 Beta</title>",
    "<h1>Defina a linha</h1>": "<h1>PULSE CNC</h1>",
    "<p>Toque na célula para abrir as máquinas correspondentes.</p>": "<p>Selecione a célula.</p>",
    "<strong>TEMPO DA LINHA</strong>": "<strong>PULSE CNC</strong>",
    "<span>VENANC Tools</span>": "<span>1.0 Beta</span>",
    "TEMPO DA LINHA — VENANC Tools": "PULSE CNC — 1.0 Beta",
}

for old, new in replacements.items():
    if old not in text:
        raise SystemExit(f"Marcador não encontrado: {old}")
    text = text.replace(old, new, 1)

# Marca visual mínima, sem alterar estrutura, eventos ou lógica.
css_marker = """

    /* PULSE CNC 1.0 Beta — identidade aplicada sobre a base monolítica estável */
    .brandTitle strong { letter-spacing:.065em; }
    .brandTitle span { color:var(--primary); }
"""

if "PULSE CNC 1.0 Beta — identidade aplicada" not in text:
    text = text.replace("\n  </style>", css_marker + "\n  </style>", 1)

path.write_text(text.replace("\n", newline), encoding="utf-8", newline="")
