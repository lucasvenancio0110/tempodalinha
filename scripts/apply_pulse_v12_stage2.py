from pathlib import Path
import re

path = Path('index.html')
raw = path.read_bytes()
newline = '\r\n' if b'\r\n' in raw else '\n'
text = raw.decode('utf-8').replace('\r\n', '\n').replace('\r', '\n')
text = text.replace('<title>PULSE CNC | V12.0.0</title>', '<title>PULSE CNC | V12.1.0</title>', 1)

css = r'''

    /* PULSE CNC V12.1.0 — Etapa 2 */
    .machineScreenContent{overflow-x:hidden;overflow-y:auto}
    .pulseEditorV12,.pulseDashboardV12{display:block;min-height:100%;padding-bottom:16px}
    .pulseEditorGridV12{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
    .pulseFieldV12{min-width:0;min-height:92px;display:flex;flex-direction:column;justify-content:center;padding:12px 13px;border:1px solid rgba(255,255,255,.09);border-radius:17px;background:linear-gradient(145deg,rgba(255,255,255,.06),rgba(255,255,255,.026));box-shadow:inset 0 1px 0 rgba(255,255,255,.035)}
    .pulseFieldV12 label{margin:0 0 7px;color:#8fa6ad;font-size:9px;font-weight:900;letter-spacing:.10em;text-transform:uppercase}
    .pulseFieldV12 .operatorInput{height:40px!important;min-height:40px!important;padding:2px 0 6px!important;font-size:27px!important}
    .pulseFieldV12.wide{grid-column:1/-1;min-height:78px}
    .pulseFieldV12 .mpModeTabs{margin-top:8px!important}
    .pulseEditorOptionalV12,.pulseEditorPreviewV12{grid-column:1/-1}
    .pulseEditorOptionalV12{margin:0!important;border-radius:16px}
    .pulseEditorPreviewV12 .editorLiveResult{margin:0}
    .pulseSectionV12{margin-top:12px;padding:14px;border:1px solid rgba(255,255,255,.085);border-radius:20px;background:rgba(255,255,255,.032)}
    .pulseSectionV12:first-child{margin-top:0}
    .pulseSectionHeadV12{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:12px}
    .pulseSectionHeadV12 h3{margin:0;color:#eff9f9;font-size:12px;font-weight:950;letter-spacing:.11em;text-transform:uppercase}
    .pulseSectionHeadV12 small{color:#789198;font-size:10px;font-weight:800}
    .pulseHeroV12{--pulse-status:var(--pulse-green);position:relative;overflow:hidden;padding:18px 16px}
    .pulseHeroV12.status-now{--pulse-status:var(--pulse-red)}
    .pulseHeroV12.status-next{--pulse-status:var(--pulse-orange)}
    .pulseHeroV12.status-ok{--pulse-status:var(--pulse-green)}
    .pulseHeroV12:before{content:"";position:absolute;inset:0 auto 0 0;width:4px;background:var(--pulse-status)}
    .pulseStatusV12{color:var(--pulse-status);font-size:12px;font-weight:950;letter-spacing:.08em;text-transform:uppercase}
    .pulseCountdownV12{display:flex;align-items:baseline;margin-top:10px;color:#f7ffff;font-family:"SFMono-Regular",Consolas,monospace;font-variant-numeric:tabular-nums;white-space:nowrap}
    .pulseCountdownV12 strong{font-size:clamp(39px,11vw,64px);line-height:.95;letter-spacing:-.09em}
    .pulseCountdownV12 small{color:var(--pulse-status);font-size:13px;font-weight:900}
    .pulseProgressLabelsV12{display:flex;justify-content:space-between;gap:10px;margin-top:17px;color:#91a8ae;font-size:10px;font-weight:850}
    .pulseProgressLabelsV12 strong{color:#effafa}
    .pulseTrackV12,.materialTrackV12{overflow:hidden;border-radius:999px;background:rgba(255,255,255,.075)}
    .pulseTrackV12{height:8px;margin-top:7px}.pulseTrackV12 i{display:block;height:100%;border-radius:inherit;background:var(--pulse-status)}
    .pulseMetricsV12{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
    .pulseMetricV12{min-width:0;padding:11px 12px;border-radius:14px;background:rgba(0,0,0,.13)}
    .pulseMetricV12 span{display:block;color:#81999f;font-size:8px;font-weight:950;letter-spacing:.09em;text-transform:uppercase}
    .pulseMetricV12 strong{display:block;margin-top:5px;color:#f1fbfb;font-size:23px;letter-spacing:-.05em;overflow-wrap:anywhere}
    .pulseMetricV12 small{display:block;margin-top:3px;color:#6f8a90;font-size:9px;font-weight:750}
    .materialBarV12{padding:13px;border-radius:15px;background:rgba(0,0,0,.14)}
    .materialBarTopV12{display:flex;justify-content:space-between;align-items:flex-end;gap:12px}
    .materialBarTopV12 span{color:#8ca4aa;font-size:9px;font-weight:950;letter-spacing:.09em;text-transform:uppercase}
    .materialBarTopV12 strong{color:#f2fbfb;font-size:20px}
    .materialTrackV12{height:12px;margin-top:10px}.materialTrackV12 i{display:block;height:100%;border-radius:inherit;background:linear-gradient(90deg,#2ebd7b,#70dec0)}
    .materialBarFootV12{display:flex;justify-content:space-between;gap:12px;margin-top:8px;color:#789198;font-size:10px;font-weight:800}
    .pulsePresetWrapV12 .presetPanelV11{margin:0;border:0;padding:0;background:transparent}.pulsePresetWrapV12 .presetTitleV11{display:none}
    .cockpitV11{height:auto!important;min-height:100%!important;overflow:visible!important}
    @media(max-width:390px){.pulseEditorGridV12{gap:8px}.pulseFieldV12{min-height:86px;padding:10px 11px}.pulseFieldV12 .operatorInput{font-size:24px!important}.pulseMetricsV12{gap:7px}.pulseMetricV12 strong{font-size:20px}}
'''
text = text.replace('</style>', css + '\n  </style>', 1)

helper = r'''
    function currentBarInfoV12(machine, calc) {
      const perBar = Math.max(0, parseInteger(calc && calc.perBar));
      let remaining = 0;
      if (machine.barMode === 'partialMm') {
        const piece = parseNumber(machine.pieceLength);
        const kerf = Math.max(0, parseNumber(state.settings.kerfWidth) || 0);
        const consumption = piece + kerf;
        remaining = consumption > 0 ? Math.max(0, Math.floor((parseNumber(machine.partialMm) || 0) / consumption)) : 0;
      } else if (machine.barMode === 'full') remaining = perBar;
      else remaining = Math.max(0, parseInteger(machine.partialPieces));
      remaining = perBar ? Math.min(perBar, remaining) : remaining;
      const percent = perBar ? Math.max(0, Math.min(100, remaining / perBar * 100)) : 0;
      const cycleSeconds = parseTempoToSeconds(machine.timeInput);
      return { perBar, remaining, percent, changeSeconds:Number.isFinite(cycleSeconds)?remaining*cycleSeconds:NaN };
    }
    function formatDurationShortV12(seconds) {
      if (!Number.isFinite(seconds)) return 'sem estimativa';
      const total=Math.max(0,Math.round(seconds)), hours=Math.floor(total/3600), minutes=Math.floor((total%3600)/60);
      return hours ? `${hours}h ${pad2(minutes)}min` : `${minutes} min`;
    }
    function operationalStatusV12(calc) {
      if (calc.status === 'now' || calc.status === 'reached') return {key:'now',text:'Encerra neste turno'};
      if (calc.status === 'next') return {key:'next',text:'Encerra no próximo turno'};
      return {key:'ok',text:'Produção normal'};
    }
'''
anchor='    function renderMachineEditor(machine, calc) {'
if anchor not in text: raise RuntimeError('renderMachineEditor não encontrada')
text=text.replace(anchor,helper+'\n'+anchor,1)

editor=r'''    function renderMachineEditor(machine, calc) {
      syncPastProductionV11(machine);
      const piecesLabel=machine.barMode==='partialMm'?'Milímetros restantes':'Peças restantes';
      const piecesValue=machine.barMode==='partialMm'?machine.partialMm:machine.partialPieces;
      const totalTrays=trayTotalV11(machine);
      const useSum=(state.settings.gabaritoMode||'individual')==='sum';
      const gabaritos=useSum?`<div class="quickTrayField"><label>Soma dos gabaritos</label><input class="operatorInput" data-v111-tray-expression inputmode="numeric" value="${escapeHtml(gabaritoExpression(machine))}" placeholder="60+40+39+22"><small data-v111-tray-feedback>Use números separados por +</small></div>`:`<div class="trayListV11">${traysMarkupV11(machine)}</div><button class="addTrayV11" data-v10-action="add-tray" type="button">Adicionar gabarito</button>`;
      machineScreenContent.innerHTML=`<section class="machineView pulseEditorV12"><div class="pulseEditorGridV12">
        <div class="pulseFieldV12"><label>Ciclo</label><input class="operatorInput" data-v10-field="timeInput" inputmode="decimal" value="${escapeHtml(String(machine.timeInput??''))}" placeholder="2,24"></div>
        <div class="pulseFieldV12"><label>${piecesLabel}</label><input class="operatorInput" data-v10-field="materialRemaining" inputmode="decimal" value="${escapeHtml(String(piecesValue??''))}" placeholder="0"><div class="mpModeTabs"><button class="mpModeTab ${machine.barMode==='pieces'?'active':''}" data-v10-action="mp-mode" data-value="pieces" type="button">PEÇAS</button><button class="mpModeTab ${machine.barMode==='partialMm'?'active':''}" data-v10-action="mp-mode" data-value="partialMm" type="button">MM</button><button class="mpModeTab ${machine.barMode==='full'?'active':''}" data-v10-action="mp-mode" data-value="full" type="button">CHEIA</button></div></div>
        <div class="pulseFieldV12"><label>Meta da OP</label><input class="operatorInput" data-v10-field="target" inputmode="numeric" value="${escapeHtml(String(machine.target??''))}" placeholder="1000"></div>
        <div class="pulseFieldV12"><label>Peça (mm)</label><input class="operatorInput" data-v10-field="pieceLength" inputmode="decimal" value="${escapeHtml(String(machine.pieceLength??''))}" placeholder="32"></div>
        <div class="pulseFieldV12 wide"><label>Barras</label><div class="barCounter"><button type="button" data-v10-action="bar-minus">−</button><strong>${parseInteger(machine.fullBars)}</strong><button type="button" data-v10-action="bar-plus">＋</button></div></div>
        <details class="optionalPanel pulseEditorOptionalV12" ${machine.traysCollapsed===false?'open':''}><summary>Gabaritos <b>${totalTrays}</b></summary><div class="optionalBodyV11"><div class="trayTotalV11"><span>Turnos passados</span><strong>${totalTrays}</strong></div>${gabaritos}</div></details>
        <div class="pulseEditorPreviewV12" data-v111-preview>${compactEditorPreview(machine)}</div>${renderPresetV11(machine,calcMachine(machine))}
      </div></section>`;
      machineScreenFooter.innerHTML=`<button class="machineFooterBtn" data-v10-action="previous" type="button" ${activeMachineIndex()<=0?'disabled':''}>${svgArrow(-1)} Anterior</button><button class="machineFooterBtn danger" data-v10-action="clear" type="button">Limpar dados</button><button class="machineFooterBtn primary" data-v10-action="save-next" type="button">Salvar e próxima ${svgArrow(1)}</button>`;
      bindMachineScreenEvents(machine);
    }
'''
text,count=re.subn(r'    function renderMachineEditor\(machine, calc\) \{.*?\n    \}\n\n    function renderMachineResult',editor+'\n    function renderMachineResult',text,count=1,flags=re.S)
if count!=1: raise RuntimeError('falha ao substituir editor')

result=r'''    function renderMachineResult(machine, calc) {
      const now=Date.now(),past=syncPastProductionV11(machine),estimate=estimatedShiftProduction(machine,calc,now);
      const target=Math.max(0,parseInteger(machine.target)),currentTotal=Math.min(target||Infinity,past+estimate),missing=Math.max(0,target-currentTotal),progress=target?Math.max(0,Math.min(100,currentTotal/target*100)):0;
      const countdown=formatCountdownParts(calc.restMs),cycleSeconds=parseTempoToSeconds(machine.timeInput),decimalMinutes=Number.isFinite(cycleSeconds)?cycleSeconds/60:NaN,status=operationalStatusV12(calc),bar=currentBarInfoV12(machine,calc);
      const started=Number.isFinite(Number(machine.calculationStartedAt))?new Date(Number(machine.calculationStartedAt)):null,preset=renderPresetV11(machine,calc);
      machineScreenContent.innerHTML=`<section class="machineView pulseDashboardV12">
        <section class="pulseSectionV12 pulseHeroV12 status-${status.key}"><div class="pulseStatusV12" data-v10-live="status">${status.text}</div><div class="pulseCountdownV12"><strong data-v10-live="countdown">${countdown.clock}</strong><small data-v10-live="milliseconds">.${countdown.milliseconds}</small></div><div class="pulseProgressLabelsV12"><span>Progresso da OP</span><strong data-v10-live="progress">${Math.round(progress)}%</strong></div><div class="pulseTrackV12"><i data-v10-live="progress-bar" style="width:${progress}%"></i></div></section>
        <section class="pulseSectionV12"><div class="pulseSectionHeadV12"><h3>Produção</h3></div><div class="pulseMetricsV12"><div class="pulseMetricV12"><span>Meta da OP</span><strong>${target}</strong></div><div class="pulseMetricV12"><span>Faltam</span><strong data-v10-live="missing">${missing}</strong></div><div class="pulseMetricV12"><span>Estimada no turno</span><strong data-v10-live="estimated">${estimate}</strong></div><div class="pulseMetricV12"><span>Turnos passados</span><strong>${past}</strong><small>soma dos gabaritos</small></div></div></section>
        <section class="pulseSectionV12"><div class="pulseSectionHeadV12"><h3>Matéria-prima</h3><small>${calc.capacity} peças disponíveis</small></div><div class="materialBarV12"><div class="materialBarTopV12"><span>Barra atual</span><strong>${bar.remaining} / ${bar.perBar||0} peças</strong></div><div class="materialTrackV12"><i style="width:${bar.percent}%"></i></div><div class="materialBarFootV12"><span>${Math.round(bar.percent)}% restante</span><span>Troca em ${formatDurationShortV12(bar.changeSeconds)}</span></div></div><div class="pulseMetricsV12" style="margin-top:8px"><div class="pulseMetricV12"><span>MP disponível</span><strong>${calc.capacity}</strong><small>peças possíveis</small></div><div class="pulseMetricV12"><span>Barras inteiras</span><strong>${Math.max(0,parseInteger(machine.fullBars))}</strong></div></div></section>
        <section class="pulseSectionV12"><div class="pulseSectionHeadV12"><h3>Dados do cálculo</h3></div><div class="pulseMetricsV12"><div class="pulseMetricV12"><span>Tempo informado</span><strong>${escapeHtml(String(machine.timeInput||'-'))}</strong></div><div class="pulseMetricV12"><span>Tempo em minutos</span><strong>${Number.isFinite(decimalMinutes)?decimalMinutes.toFixed(4):'-'}</strong><small>fração decimal</small></div><div class="pulseMetricV12" style="grid-column:1/-1"><span>Cálculo iniciado</span><strong>${started?fmtTime(started):'-'}</strong><small>${started?fmtDate(started):'Ainda não iniciado'}</small></div></div></section>
        ${preset?`<section class="pulseSectionV12 pulsePresetWrapV12"><div class="pulseSectionHeadV12"><h3>Próxima OP</h3></div>${preset}</section>`:''}
      </section>`;
      machineScreenFooter.innerHTML=`<button class="machineFooterBtn" data-v10-action="previous" type="button" ${activeMachineIndex()<=0?'disabled':''}>${svgArrow(-1)} Anterior</button><button class="machineFooterBtn" data-v10-action="edit" type="button">Editar dados</button><button class="machineFooterBtn primary" data-v10-action="next" type="button">Próxima máquina ${svgArrow(1)}</button>`;
      bindMachineScreenEvents(machine);
    }
'''
text,count=re.subn(r'    function renderMachineResult\(machine, calc\) \{.*?\n    \}\n\n    function bindMachineScreenEvents',result+'\n    function bindMachineScreenEvents',text,count=1,flags=re.S)
if count!=1: raise RuntimeError('falha ao substituir resultado')
old="status.textContent=calc.statusText.toUpperCase(); status.className=`resultStatusV11 ${calc.badgeClass==='bad'?'bad':calc.badgeClass==='warn'?'warn':''}`.trim();"
new="const liveStatus=operationalStatusV12(calc); status.textContent=liveStatus.text; const hero=status.closest('.pulseHeroV12'); if(hero) hero.className=`pulseSectionV12 pulseHeroV12 status-${liveStatus.key}`;"
text=text.replace(old,new,1)
for marker in ['<title>PULSE CNC | V12.1.0</title>','PULSE CNC V12.1.0 — Etapa 2','function currentBarInfoV12','class="machineView pulseDashboardV12"','<h3>Produção</h3>','<h3>Matéria-prima</h3>','<h3>Dados do cálculo</h3>']:
    if marker not in text: raise RuntimeError('marcador ausente: '+marker)
path.write_bytes(text.replace('\n',newline).encode('utf-8'))
print('PULSE CNC V12 etapa 2 aplicada com sucesso.')
