from pathlib import Path

path = Path('index.html')
raw = path.read_bytes()
newline = '\r\n' if b'\r\n' in raw else '\n'
text = raw.decode('utf-8').replace('\r\n','\n')

start = text.rfind('    function renderPresetV11(machine, calc) {')
if start < 0:
    raise SystemExit('renderPresetV11 não encontrado')
end = text.find('\n    function ', start + 20)
if end < 0:
    raise SystemExit('fim renderPresetV11 não encontrado')
replacement = '''    function renderPresetEditorV13(machine, calc) {
      if (!presetRequiredV11(calc)) return '';
      const received = machine.presetMode === 'yes';
      const requestDate = calc.endDT ? fmtDate(calc.endDT) : '-';
      const requestTime = calc.endDT ? fmtTime(calc.endDT) : '--:--';
      const remainingText = calc.forecastReached ? 'HORÁRIO ATINGIDO' : `Faltam ${formatMinutes(calc.restMin)}`;
      const setupOptions = [
        ['sequencia', 'Sequência'],
        ['verde', 'Setup verde'],
        ['azul', 'Setup azul'],
        ['vermelho', 'Setup vermelho']
      ].map(([value,label]) => `<option value="${value}" ${machine.presetType===value?'selected':''}>${label}</option>`).join('');
      return `<section class="presetMissionV12 ${received ? 'received' : 'pending'}">
        <div class="presetMissionHeadV12">
          <div><span>PRÓXIMA OP</span><strong>O setor do Preset já trouxe a nova OP?</strong></div>
          <b>${received ? 'PRESET RECEBIDO' : 'PRESET PENDENTE'}</b>
        </div>
        <div class="presetDecisionV12">
          <button type="button" data-v10-action="preset-mode" data-value="yes" class="${received ? 'active' : ''}"><span>✓</span><strong>Já trouxe</strong></button>
          <button type="button" data-v10-action="preset-mode" data-value="no" class="${!received ? 'active' : ''}"><span>⌛</span><strong>Ainda não trouxe</strong></button>
        </div>
        ${received
          ? `<div class="presetTypeV12 presetTypeConfirmedV13"><label>TIPO DA PRÓXIMA OP</label><div class="presetNextOpLeadV13"><span>✓</span><div><small>A próxima OP será</small><strong>${escapeHtml(presetLabel(machine))}</strong></div></div><select data-v10-field="presetType">${setupOptions}</select></div>`
          : `<div class="presetRequestV12"><span>Solicitar ao Preset</span><strong>${requestDate} · ${requestTime}</strong><small>${remainingText}</small></div><div class="presetItemV12"><label>Item da próxima OP</label><input data-v10-field="itemCode" value="${escapeHtml(String(machine.itemCode || ''))}" placeholder="Ex.: 125.142-1"></div>`}
      </section>`;
    }

    function renderPresetDashboardV13(machine, calc) {
      if (!presetRequiredV11(calc)) return '';
      const received = machine.presetMode === 'yes';
      if (received) {
        return `<section class="presetSummaryV13 received"><span>PRÓXIMA OP</span><strong>Preset recebido</strong><div><small>A próxima OP será</small><b>${escapeHtml(presetLabel(machine))}</b></div></section>`;
      }
      const requestDate = calc.endDT ? fmtDate(calc.endDT) : '-';
      const requestTime = calc.endDT ? fmtTime(calc.endDT) : '--:--';
      const item = String(machine.itemCode || '').trim() || 'Item não informado';
      return `<section class="presetSummaryV13 pending"><span>PRÓXIMA OP</span><strong>Preset pendente</strong><div><small>Item solicitado</small><b>${escapeHtml(item)}</b></div><div><small>Solicitar ao Preset</small><b>${requestDate} · ${requestTime}</b></div></section>`;
    }

    function renderPresetV11(machine, calc) {
      return machineScreenMode === 'edit' ? renderPresetEditorV13(machine, calc) : renderPresetDashboardV13(machine, calc);
    }
'''
text = text[:start] + replacement + text[end:]

needle = '<div data-v111-preview>${compactEditorPreview(machine)}</div>'
if needle in text:
    text = text.replace(needle, needle + '${renderPresetEditorV13(machine, calc)}', 1)
else:
    marker = '          </div>\n        </section>`;'
    idx = text.find(marker, text.rfind('    function renderMachineEditor(machine, calc) {'))
    if idx < 0:
        raise SystemExit('ponto de inserção no editor não encontrado')
    text = text[:idx] + '          ${renderPresetEditorV13(machine, calc)}\n' + text[idx:]

result_start = text.rfind('    function renderMachineResult(machine, calc) {')
result_end = text.find('\n    function ', result_start + 20)
block = text[result_start:result_end]
if '${renderPresetDashboardV13(machine, calc)}' not in block:
    marker = '        </section>`;'
    pos = block.rfind(marker)
    if pos < 0:
        raise SystemExit('ponto de inserção no dashboard não encontrado')
    block = block[:pos] + '        ${renderPresetDashboardV13(machine, calc)}\n' + block[pos:]
    text = text[:result_start] + block + text[result_end:]

css = '''

    /* PULSE CNC — fluxo correto do Preset */
    .presetNextOpLeadV13 { display:flex; align-items:center; gap:10px; margin-bottom:10px; padding:12px; border-radius:13px; color:#70eadc; background:rgba(86,213,199,.10); }
    .presetNextOpLeadV13 > span { font-size:22px; }
    .presetNextOpLeadV13 small,.presetNextOpLeadV13 strong { display:block; }
    .presetNextOpLeadV13 small { color:#8fbab5; font-size:10px; }
    .presetNextOpLeadV13 strong { margin-top:2px; color:#eafffb; font-size:18px; }
    .presetSummaryV13 { margin-top:12px; padding:16px; border:1px solid rgba(255,255,255,.10); border-radius:18px; background:rgba(255,255,255,.035); }
    .presetSummaryV13.pending { border-color:rgba(242,184,100,.35); background:linear-gradient(145deg,rgba(91,58,14,.22),rgba(20,29,35,.94)); }
    .presetSummaryV13.received { border-color:rgba(86,213,199,.38); background:linear-gradient(145deg,rgba(16,93,82,.20),rgba(20,29,35,.94)); }
    .presetSummaryV13 > span { color:#f2b864; font-size:9px; font-weight:950; letter-spacing:.14em; }
    .presetSummaryV13.received > span { color:#70eadc; }
    .presetSummaryV13 > strong { display:block; margin:4px 0 12px; color:#f6fbfa; font-size:20px; }
    .presetSummaryV13 > div { padding:10px 0; border-top:1px solid rgba(255,255,255,.08); }
    .presetSummaryV13 small,.presetSummaryV13 b { display:block; }
    .presetSummaryV13 small { color:#8da1a7; font-size:9px; font-weight:850; text-transform:uppercase; letter-spacing:.08em; }
    .presetSummaryV13 b { margin-top:4px; color:#f4fbfa; font-size:16px; }
'''
text = text.replace('</style>', css + '\n  </style>', 1)
path.write_bytes(text.replace('\n', newline).encode('utf-8'))
