import { calculateMachine } from '../src/core/calc-engine.js';
import { createDefaultMachine, loadState, saveState } from '../src/storage/storage-engine.js';
import { moveMachine, restoreMachineOrder, sanitizeSettings } from '../src/settings/settings-engine.js';
import { buildCellReport } from '../src/share/share-engine.js';

const CELL_MACHINES = {
  '01':[2,5,15,19,23,24,25,26,27,29,30,35,46,47,48],
  '02':[3,4,7,8,13,16,17,18,28,31,32,49,50,51,143],
  '03':[9,10,33,34,36,37,39,40,41,43,44],
  '04':[42,52,53,57,58,59,60,61,64,65,66],
  '05':[95,94,93,92,91,90,89,88,87,85,83,72,69],
  '06':[67,68,73,74,75,76,77,79,81,82,84,86],
  '07':[45,54,55,56,62,63,70,71,78,80,102,103,110,111],
  '08':[96,98,104,107,112,113,115,116,118,119,121,122],
  '09':[97,99,100,101,105,106,108,109,114,117,120,123],
  '10':[124,125,126,127,128,129,130,134,135,136,137,138,139,140,141,142]
};

const app = document.querySelector('#app');
const loaded = loadState(localStorage);
let state = loaded.state;
let activeMachineId = null;
let machineMode = 'edit';
let timer = null;

const esc = (value='') => String(value).replace(/[&<>'"]/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[char]));
const pad = value => String(value).padStart(2,'0');
const machineLabel = value => String(parseInt(value,10)||0).padStart(3,'0');
const formatClock = ms => { const total=Math.max(0,Math.ceil(ms/1000)); return `${pad(Math.floor(total/3600))}:${pad(Math.floor(total%3600/60))}:${pad(total%60)}`; };
const formatDateTime = value => { if(!value) return '-'; const date=new Date(value); return `${pad(date.getDate())}/${pad(date.getMonth()+1)}/${date.getFullYear()} ${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`; };
const trayTotal = machine => (machine.trays||[]).reduce((sum,value)=>sum+Math.max(0,parseInt(value,10)||0),0);

function ensureCell(cellId){
  if(!Array.isArray(state.cells[cellId]) || !state.cells[cellId].length){
    state.cells[cellId]=(CELL_MACHINES[cellId]||[]).map((number,index)=>createDefaultMachine({machine:number,id:`cell-${cellId}-${number}`,index}));
  }
  state.selectedCell=cellId;
  persist();
}

function persist(){ state=saveState(localStorage,state); }
function currentMachines(){ return state.selectedCell ? state.cells[state.selectedCell]||[] : []; }
function getMachine(id){ return currentMachines().find(machine=>machine.id===id)||null; }
function machineInput(machine){
  return {
    cycle:machine.cycle,
    target:machine.target,
    trays:machine.trays,
    pieceLength:machine.pieceLength,
    fullBars:machine.fullBars,
    currentBarMode:machine.currentBarMode,
    currentBarValue:machine.currentBarValue,
    barLength:state.settings.barLength,
    kerfWidth:state.settings.kerfWidth,
    presetLimitHours:state.settings.presetLimitHours
  };
}
function calculate(machine,now=Date.now()){
  return calculateMachine(machineInput(machine),{now,calculationStartedAt:machine.calculationStartedAt||now});
}
function ensureStarted(machine){
  const result=calculate(machine);
  if(result.valid && !machine.calculationStartedAt){
    const started=Date.now();
    machine.calculationStartedAt=started;
    machine.baseTimestamp=started;
    persist();
    return calculate(machine,started);
  }
  return result;
}

function render(){
  clearInterval(timer);
  if(!state.selectedCell) return renderCells();
  renderDashboard();
  timer=setInterval(refreshVisible,1000);
}

function renderCells(){
  app.innerHTML=`<main class="shell cellScreen"><div class="brandHero"><div class="brandMark">P</div><div><strong>PULSE CNC</strong><small>1.0 Beta</small></div></div><h1>Selecione a célula</h1><div class="cellGrid">${Object.keys(CELL_MACHINES).map(cell=>`<button class="cellButton" data-cell="${cell}"><span>${cell}</span><small>Célula</small></button>`).join('')}</div></main>`;
  app.querySelectorAll('[data-cell]').forEach(button=>button.onclick=()=>{ensureCell(button.dataset.cell);render();});
}

function renderDashboard(){
  const machines=currentMachines();
  const results=machines.map(machine=>calculate(machine));
  const calculated=results.filter(result=>result.valid).length;
  const red=results.filter(result=>result.valid&&result.status.key==='red').length;
  const orange=results.filter(result=>result.valid&&result.status.key==='orange').length;
  const green=results.filter(result=>result.valid&&result.status.key==='green').length;
  app.innerHTML=`<main class="shell dashboardScreen">
    <header class="topbar compactTopbar">
      <div class="brand"><div class="brandMark">P</div><div><strong>PULSE CNC</strong><small>Célula ${state.selectedCell} · Beta</small></div></div>
      <div class="headerActions"><button class="iconButton" id="shareCell" aria-label="Compartilhar">Compartilhar</button><button class="iconButton" id="settings">Ajustes</button><button class="iconButton" id="changeCell">Trocar</button></div>
    </header>
    <section class="summary compactSummary">
      <div class="summaryCard"><span>Calculadas</span><strong>${calculated}/${machines.length}</strong></div>
      <div class="summaryCard redMetric"><span>Neste turno</span><strong>${red}</strong></div>
      <div class="summaryCard orangeMetric"><span>Próximo</span><strong>${orange}</strong></div>
      <div class="summaryCard greenMetric"><span>Normal</span><strong>${green}</strong></div>
    </section>
    <section class="machineList">${machines.map(machine=>{
      const result=calculate(machine);
      const status=result.valid?result.status:{key:'neutral',label:'Sem cálculo'};
      return `<button class="machineRow status-${status.key}" data-machine="${esc(machine.id)}"><div class="machineNumber">${machineLabel(machine.machine)}</div><div class="machineSummary"><strong>${status.label}</strong><span>${result.valid?`${formatClock(result.forecast.remainingMs)} restantes`:'Toque para preencher'}</span></div><div class="rowArrow">›</div></button>`;
    }).join('')}</section>
    <div class="toast" id="toast" role="status" aria-live="polite"></div>
  </main>`;
  app.querySelector('#changeCell').onclick=()=>{state.selectedCell=null;persist();render();};
  app.querySelector('#settings').onclick=renderSettings;
  app.querySelector('#shareCell').onclick=shareCurrentCell;
  app.querySelectorAll('[data-machine]').forEach(card=>card.onclick=()=>openMachine(card.dataset.machine));
}

async function shareCurrentCell(){
  const report=buildCellReport({cellId:state.selectedCell,machines:currentMachines(),calculate});
  try{
    if(navigator.share){ await navigator.share({title:`PULSE CNC · Célula ${state.selectedCell}`,text:report.text}); showToast('Resumo compartilhado'); return; }
    await navigator.clipboard.writeText(report.text); showToast('Resumo copiado');
  }catch(error){
    if(error?.name==='AbortError') return;
    const area=document.createElement('textarea'); area.value=report.text; area.style.position='fixed'; area.style.opacity='0'; document.body.append(area); area.select(); document.execCommand('copy'); area.remove(); showToast('Resumo copiado');
  }
}
function showToast(message){ const toast=app.querySelector('#toast'); if(!toast)return; toast.textContent=message; toast.classList.add('visible'); setTimeout(()=>toast.classList.remove('visible'),2200); }

function openMachine(id,requestedMode=null){
  activeMachineId=id;
  const machine=getMachine(id); if(!machine)return;
  const result=calculate(machine);
  machineMode=requestedMode||(result.valid?'result':'edit');
  renderMachine();
}
function closeMachine(){ activeMachineId=null; machineMode='edit'; renderDashboard(); }
function activeIndex(){ return currentMachines().findIndex(machine=>machine.id===activeMachineId); }
function navigate(delta){ const machines=currentMachines(); const next=Math.max(0,Math.min(machines.length-1,activeIndex()+delta)); openMachine(machines[next].id); }

function renderMachine(){
  const machine=getMachine(activeMachineId); if(!machine) return closeMachine();
  const result=calculate(machine);
  app.innerHTML=`<div class="modal machineModal"><header class="modalHeader"><button class="button ghost" id="closeMachine">Fechar</button><div class="machineTitle"><small>TNL</small><strong>${machineLabel(machine.machine)}</strong></div><button class="button" id="toggleMode">${machineMode==='edit'?'Resultado':'Editar'}</button></header><div class="modalBody" id="machineBody"></div><footer class="footer"><button id="previous" ${activeIndex()<=0?'disabled':''}>Anterior</button><button class="danger" id="clear">Limpar</button><button class="primary" id="next">Próxima</button></footer></div>`;
  app.querySelector('#closeMachine').onclick=closeMachine;
  app.querySelector('#toggleMode').onclick=()=>{machineMode=machineMode==='edit'?'result':'edit';renderMachine();};
  app.querySelector('#previous').onclick=()=>navigate(-1);
  app.querySelector('#next').onclick=()=>navigate(1);
  app.querySelector('#clear').onclick=()=>{if(!confirm(`Limpar os dados da máquina ${machineLabel(machine.machine)}?`))return; const clean=createDefaultMachine({machine:machine.machine,id:machine.id}); Object.assign(machine,clean); persist(); machineMode='edit'; renderMachine();};
  if(machineMode==='result'&&result.valid) renderResult(machine,result); else renderEditor(machine,result);
}

function renderEditor(machine,result){
  const body=app.querySelector('#machineBody');
  const useSum=state.settings.gabaritoMode==='sum';
  body.innerHTML=`<section class="editorPanel"><div class="editorGrid compactEditor">
    ${field('Ciclo','cycle',machine.cycle,'2,24','decimal')}
    ${field('Peças restantes','currentBarValue',machine.currentBarValue,'0','decimal',`<select data-field="currentBarMode"><option value="pieces" ${machine.currentBarMode==='pieces'?'selected':''}>Peças</option><option value="partialMm" ${machine.currentBarMode==='partialMm'?'selected':''}>Milímetros</option><option value="full" ${machine.currentBarMode==='full'?'selected':''}>Barra cheia</option></select>`)}
    ${field('Meta da OP','target',machine.target,'1000','numeric')}
    ${field('Peça (mm)','pieceLength',machine.pieceLength,'32','decimal')}
    ${field('Barras','fullBars',machine.fullBars,'0','numeric','',true)}
  </div>
  <section class="gabaritoPanel"><div class="sectionHeader"><div><span class="eyebrow">Gabaritos</span><strong>Turnos passados: <b id="trayTotal">${trayTotal(machine)}</b></strong></div></div>${useSum?`<div class="sumInput"><input id="trayExpression" value="${esc((machine.trays||[]).filter(Boolean).join('+'))}" inputmode="numeric" placeholder="60+40+39+22"></div>`:`<div id="trayList" class="trayList">${trayRows(machine)}</div><button class="button addTray" id="addTray" type="button">Adicionar gabarito</button>`}</section>
  <div id="validation">${validationMarkup(result)}</div></section>`;
  body.querySelectorAll('[data-field]').forEach(input=>{
    input.addEventListener('input',()=>{machine[input.dataset.field]=input.value;persist();updateEditorPreview(machine);});
    input.addEventListener('change',()=>{machine[input.dataset.field]=input.value;const current=ensureStarted(machine);persist();updateEditorPreview(machine,current);});
  });
  if(useSum){
    const expression=body.querySelector('#trayExpression');
    expression.oninput=()=>{const valid=/^\s*\d*(?:\s*\+\s*\d+)*\s*$/.test(expression.value);if(valid){machine.trays=expression.value.split('+').map(value=>value.trim()).filter(Boolean);persist();body.querySelector('#trayTotal').textContent=trayTotal(machine);updateEditorPreview(machine);}};
  }else{
    bindTrayEvents(machine);
    body.querySelector('#addTray').onclick=()=>{machine.trays.push('');persist();renderEditor(machine,calculate(machine));requestAnimationFrame(()=>body.querySelectorAll('[data-tray]')[machine.trays.length-1]?.focus());};
  }
}
function field(label,name,value,placeholder,inputmode,extra='',wide=false){ return `<div class="field ${wide?'wide':''}"><label>${label}</label><input data-field="${name}" inputmode="${inputmode}" value="${esc(value)}" placeholder="${placeholder}">${extra}</div>`; }
function trayRows(machine){ return machine.trays.map((value,index)=>`<div class="trayRow"><input data-tray="${index}" inputmode="numeric" value="${esc(value)}" placeholder="Quantidade"><button data-remove-tray="${index}" type="button" aria-label="Remover gabarito">×</button></div>`).join(''); }
function bindTrayEvents(machine){
  app.querySelectorAll('[data-tray]').forEach(input=>input.oninput=()=>{machine.trays[Number(input.dataset.tray)]=input.value;persist();app.querySelector('#trayTotal').textContent=trayTotal(machine);updateEditorPreview(machine);});
  app.querySelectorAll('[data-remove-tray]').forEach(button=>button.onclick=()=>{machine.trays.splice(Number(button.dataset.removeTray),1);if(!machine.trays.length)machine.trays=[''];persist();renderEditor(machine,calculate(machine));});
}
function validationMarkup(result){
  if(result.valid) return '<div class="validState"><strong>Cálculo pronto</strong><span>Salvo automaticamente.</span></div>';
  return `<div class="validation">${(result.validation?.errors||[]).map(error=>`<div>${esc(error.message||error)}</div>`).join('')||'Preencha os dados principais.'}</div>`;
}
function updateEditorPreview(machine,result=calculate(machine)){ const node=app.querySelector('#validation'); if(node) node.innerHTML=validationMarkup(result); }

function renderResult(machine,result){
  const body=app.querySelector('#machineBody');
  const progress=result.production.target?Math.min(100,(result.production.completedEstimated/result.production.target)*100):0;
  const materialPercent=result.material.perBar?Math.min(100,(result.material.currentPieces/result.material.perBar)*100):0;
  const reason=result.forecast.reason==='order'?'Meta da OP':'Falta de matéria-prima';
  const totalEstimated=result.production.completedEstimated;
  body.innerHTML=`
    <section class="resultHero status-${result.status.key}"><div class="heroTop"><span class="statusBadge">${result.status.label}</span><span class="heroLabel">Tempo restante</span></div><div class="countdown" data-live-countdown>${formatClock(result.forecast.remainingMs)}</div><div class="heroMeta"><span>Previsão ${formatDateTime(result.forecast.endAt)}</span><strong>${reason}</strong></div><div class="progress"><i style="width:${progress}%"></i></div></section>

    <section class="resultSection"><div class="sectionTitle"><span>Produção</span><small>situação da OP</small></div><div class="metricGrid importantMetrics">${metric('Meta da OP',result.production.target)}${metric('Turnos passados',result.production.previousShifts)}${metric('Produção do turno',result.production.currentEstimated,'data-live-current')}${metric('Total estimado',totalEstimated)}${metric('Faltam',result.production.remainingOrder,'data-live-remaining')}${metric('Até a parada',result.forecast.piecesUntilStop)}</div></section>

    <section class="resultSection"><div class="sectionTitle"><span>Matéria-prima</span><small>capacidade disponível</small></div><div class="barHeadline"><strong>${result.material.currentPieces}</strong><span>de ${result.material.perBar} peças na barra atual</span></div><div class="materialBar"><i style="width:${materialPercent}%"></i></div><div class="metricGrid">${metric('Peças por barra',result.material.perBar)}${metric('Barras inteiras',result.material.fullBars)}${metric('MP disponível',result.material.totalCapacity)}${metric('Consumo por peça',(Number(machine.pieceLength)+Number(state.settings.kerfWidth)).toFixed(2)+' mm')}</div></section>

    <section class="resultSection"><div class="sectionTitle"><span>Dados do cálculo</span><small>valores usados pelo motor</small></div><div class="metricGrid">${metric('Ciclo informado',result.cycle.informed)}${metric('Ciclo em segundos',result.cycle.seconds+' s')}${metric('Fração de minuto',result.cycle.decimalMinutes.toFixed(4)+' min')}${metric('Cálculo iniciado',formatDateTime(machine.calculationStartedAt))}${metric('Previsão fixa',formatDateTime(result.forecast.endAt))}${metric('Confiança',result.confidence+'%')}</div><details class="audit"><summary>Ver memória do cálculo</summary><div class="auditGrid"><div><span>Produção</span><p>${esc(result.audit.production.formula)}</p></div><div><span>Matéria-prima</span><p>${esc(result.audit.material.formula)}</p></div><div><span>Previsão</span><p>${esc(result.audit.forecast.formula)}</p></div></div></details></section>

    ${result.preset.required?renderPreset(machine):''}`;
  bindPreset(machine);
}
function metric(label,value,attr=''){ return `<div class="metric"><span>${label}</span><strong ${attr}>${esc(value)}</strong></div>`; }
function renderPreset(machine){ return `<section class="resultSection presetSection"><div class="sectionTitle"><span>Próxima OP</span><small>janela abaixo de ${state.settings.presetLimitHours}h</small></div><div class="editorGrid compactEditor"><div class="field"><label>Preset já trouxe?</label><select data-preset="brought"><option value="false" ${!machine.preset.brought?'selected':''}>Não</option><option value="true" ${machine.preset.brought?'selected':''}>Sim</option></select></div>${machine.preset.brought?`<div class="field"><label>Tipo</label><select data-preset="type"><option value="sequencia" ${machine.preset.type==='sequencia'?'selected':''}>Sequência</option><option value="azul" ${machine.preset.type==='azul'?'selected':''}>Setup azul</option><option value="verde" ${machine.preset.type==='verde'?'selected':''}>Setup verde</option><option value="vermelho" ${machine.preset.type==='vermelho'?'selected':''}>Setup vermelho</option></select></div>`:''}</div></section>`; }
function bindPreset(machine){ app.querySelectorAll('[data-preset]').forEach(input=>input.onchange=()=>{machine.preset[input.dataset.preset]=input.dataset.preset==='brought'?input.value==='true':input.value;persist();renderMachine();}); }

function renderSettings(){
  const machines=currentMachines();
  app.innerHTML=`<div class="settingsScreen"><header class="modalHeader"><button class="button ghost" id="closeSettings">Voltar</button><div class="machineTitle"><small>Célula ${state.selectedCell}</small><strong>Ajustes</strong></div><button class="button primary" id="saveSettings">Salvar</button></header><main class="settingsBody"><section class="settingsCard"><div class="sectionTitle"><span>Cálculo</span><small>padrões da célula</small></div><div class="editorGrid compactEditor">${field('Comprimento da barra (mm)','setting-barLength',state.settings.barLength,'3600','decimal')}${field('Largura do bedame (mm)','setting-kerfWidth',state.settings.kerfWidth,'1','decimal')}${field('Janela do preset (h)','setting-presetLimitHours',state.settings.presetLimitHours,'16','decimal')}<div class="field"><label>Gabaritos</label><select id="setting-gabaritoMode"><option value="individual" ${state.settings.gabaritoMode==='individual'?'selected':''}>Campos individuais</option><option value="sum" ${state.settings.gabaritoMode==='sum'?'selected':''}>Soma rápida</option></select></div></div></section><section class="settingsCard"><div class="sectionHeader"><div class="sectionTitle"><span>Ordem das máquinas</span><small>define o percurso</small></div><button class="button" id="restoreOrder">Restaurar</button></div><div class="orderList">${machines.map((machine,index)=>`<div class="orderRow"><div><small>${index+1}</small><strong>${machineLabel(machine.machine)}</strong></div><div class="moveButtons"><button data-move="-1" data-id="${esc(machine.id)}" ${index===0?'disabled':''} aria-label="Mover para cima">↑</button><button data-move="1" data-id="${esc(machine.id)}" ${index===machines.length-1?'disabled':''} aria-label="Mover para baixo">↓</button></div></div>`).join('')}</div></section></main></div>`;
  app.querySelector('#closeSettings').onclick=renderDashboard;
  app.querySelector('#saveSettings').onclick=()=>{const next=sanitizeSettings({barLength:app.querySelector('[data-field="setting-barLength"]').value,kerfWidth:app.querySelector('[data-field="setting-kerfWidth"]').value,presetLimitHours:app.querySelector('[data-field="setting-presetLimitHours"]').value,gabaritoMode:app.querySelector('#setting-gabaritoMode').value},state.settings);state.settings=next;persist();renderDashboard();};
  app.querySelectorAll('[data-move]').forEach(button=>button.onclick=()=>{state.cells[state.selectedCell]=moveMachine(currentMachines(),button.dataset.id,Number(button.dataset.move));persist();renderSettings();});
  app.querySelector('#restoreOrder').onclick=()=>{state.cells[state.selectedCell]=restoreMachineOrder(currentMachines(),CELL_MACHINES[state.selectedCell]||[]);persist();renderSettings();};
}

function refreshVisible(){
  if(!activeMachineId||machineMode!=='result')return;
  const machine=getMachine(activeMachineId),result=calculate(machine); if(!result.valid)return;
  const countdown=app.querySelector('[data-live-countdown]'); if(countdown)countdown.textContent=formatClock(result.forecast.remainingMs);
  const remaining=app.querySelector('[data-live-remaining]'); if(remaining)remaining.textContent=result.production.remainingOrder;
  const current=app.querySelector('[data-live-current]'); if(current)current.textContent=result.production.currentEstimated;
}

if('serviceWorker' in navigator){ window.addEventListener('load',()=>navigator.serviceWorker.register('./sw.js').catch(error=>console.warn('Service worker não registrado',error))); }
render();