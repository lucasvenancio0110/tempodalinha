import { calculateMachine } from '../src/core/calc-engine.js';
import { createDefaultMachine, loadState, saveState } from '../src/storage/storage-engine.js';
import { moveMachine, restoreMachineOrder, sanitizeSettings } from '../src/settings/settings-engine.js';
import { buildCellReport } from '../src/share/share-engine.js';

const CELL_MACHINES={
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

const app=document.querySelector('#app');
const loaded=loadState(localStorage);
let state=loaded.state;
let activeMachineId=null;
let machineMode='edit';
let timer=null;

function esc(value=''){return String(value).replace(/[&<>'"]/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[char]));}
function pad(value){return String(value).padStart(2,'0');}
function machineLabel(value){return String(parseInt(value,10)||0).padStart(3,'0');}
function formatClock(ms){const total=Math.max(0,Math.ceil(ms/1000));return `${pad(Math.floor(total/3600))}:${pad(Math.floor(total%3600/60))}:${pad(total%60)}`;}
function formatDateTime(value){if(!value)return '-';const date=new Date(value);return `${pad(date.getDate())}/${pad(date.getMonth()+1)} ${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`;}
function trayTotal(machine){return (machine.trays||[]).reduce((sum,value)=>sum+Math.max(0,parseInt(value,10)||0),0);}

function ensureCell(cellId){
  if(!Array.isArray(state.cells[cellId])||!state.cells[cellId].length){
    state.cells[cellId]=(CELL_MACHINES[cellId]||[]).map((number,index)=>createDefaultMachine({machine:number,id:`cell-${cellId}-${number}`,index}));
  }
  state.selectedCell=cellId;
  persist();
}

function persist(){state=saveState(localStorage,state);}
function currentMachines(){return state.selectedCell?state.cells[state.selectedCell]||[]:[];}
function getMachine(id){return currentMachines().find(machine=>machine.id===id)||null;}
function machineInput(machine){return {cycle:machine.cycle,target:machine.target,trays:machine.trays,pieceLength:machine.pieceLength,fullBars:machine.fullBars,currentBarMode:machine.currentBarMode,currentBarValue:machine.currentBarValue,barLength:state.settings.barLength,kerfWidth:state.settings.kerfWidth,presetLimitHours:state.settings.presetLimitHours};}
function calculate(machine,now=Date.now()){return calculateMachine(machineInput(machine),{now,calculationStartedAt:machine.calculationStartedAt||now});}
function ensureStarted(machine){const result=calculate(machine);if(result.valid&&!machine.calculationStartedAt){const started=Date.now();machine.calculationStartedAt=started;machine.baseTimestamp=started;persist();return calculate(machine,started);}return result;}

function render(){clearInterval(timer);if(!state.selectedCell)return renderCells();renderDashboard();timer=setInterval(refreshVisible,1000);}

function renderCells(){
  app.innerHTML=`<main class="shell"><header class="topbar"><div class="brand"><div class="brandMark">P</div><div><strong>PULSE CNC</strong><small>1.0 Beta</small></div></div></header><h1 class="screenTitle">Selecione a célula</h1><div class="cellGrid">${Object.keys(CELL_MACHINES).map(cell=>`<button class="cellButton" data-cell="${cell}">Célula ${cell}</button>`).join('')}</div></main>`;
  app.querySelectorAll('[data-cell]').forEach(button=>button.onclick=()=>{ensureCell(button.dataset.cell);render();});
}

function renderDashboard(){
  const machines=currentMachines();
  const results=machines.map(machine=>calculate(machine));
  const calculated=results.filter(result=>result.valid).length;
  const red=results.filter(result=>result.valid&&result.status.key==='red').length;
  const orange=results.filter(result=>result.valid&&result.status.key==='orange').length;
  app.innerHTML=`<main class="shell"><header class="topbar"><div class="brand"><div class="brandMark">P</div><div><strong>PULSE CNC</strong><small>Célula ${state.selectedCell} · Beta 1.0</small></div></div><div class="headerActions"><button class="button" id="shareCell">Compartilhar</button><button class="button" id="settings">Ajustes</button><button class="button" id="changeCell">Trocar</button></div></header><section class="summary"><div class="summaryCard"><span>Calculadas</span><strong>${calculated}/${machines.length}</strong></div><div class="summaryCard"><span>Neste turno</span><strong>${red}</strong></div><div class="summaryCard"><span>Próximo</span><strong>${orange}</strong></div></section><section class="machineGrid">${machines.map(machine=>{const result=calculate(machine),status=result.valid?result.status:{key:'neutral',label:'Sem cálculo'};return `<button class="machineCard status-${status.key}" data-machine="${esc(machine.id)}"><strong>${machineLabel(machine.machine)}</strong><span>${result.valid?formatClock(result.forecast.remainingMs):'Preencher dados'}</span><small>${status.label}</small></button>`;}).join('')}</section><div class="toast" id="toast" role="status" aria-live="polite"></div></main>`;
  app.querySelector('#changeCell').onclick=()=>{state.selectedCell=null;persist();render();};
  app.querySelector('#settings').onclick=renderSettings;
  app.querySelector('#shareCell').onclick=shareCurrentCell;
  app.querySelectorAll('[data-machine]').forEach(card=>card.onclick=()=>openMachine(card.dataset.machine));
}

async function shareCurrentCell(){
  const report=buildCellReport({cellId:state.selectedCell,machines:currentMachines(),calculate});
  try{
    if(navigator.share){await navigator.share({title:`PULSE CNC · Célula ${state.selectedCell}`,text:report.text});showToast('Resumo compartilhado');return;}
    await navigator.clipboard.writeText(report.text);showToast('Resumo copiado');
  }catch(error){
    if(error?.name==='AbortError')return;
    const area=document.createElement('textarea');area.value=report.text;area.style.position='fixed';area.style.opacity='0';document.body.append(area);area.select();document.execCommand('copy');area.remove();showToast('Resumo copiado');
  }
}
function showToast(message){const toast=app.querySelector('#toast');if(!toast)return;toast.textContent=message;toast.classList.add('visible');setTimeout(()=>toast.classList.remove('visible'),2200);}

function openMachine(id,requestedMode=null){activeMachineId=id;const machine=getMachine(id);if(!machine)return;const result=calculate(machine);machineMode=requestedMode||(result.valid?'result':'edit');renderMachine();}
function closeMachine(){activeMachineId=null;machineMode='edit';renderDashboard();}
function activeIndex(){return currentMachines().findIndex(machine=>machine.id===activeMachineId);}
function navigate(delta){const machines=currentMachines(),next=Math.max(0,Math.min(machines.length-1,activeIndex()+delta));openMachine(machines[next].id);}

function renderMachine(){
  const machine=getMachine(activeMachineId);if(!machine)return closeMachine();
  const result=calculate(machine);
  app.innerHTML=`<div class="modal"><header class="modalHeader"><button class="button" id="closeMachine">Fechar</button><div class="machineName">${machineLabel(machine.machine)}</div><button class="button" id="toggleMode">${machineMode==='edit'?'Resultado':'Editar'}</button></header><div class="modalBody" id="machineBody"></div><footer class="footer"><button id="previous" ${activeIndex()<=0?'disabled':''}>Anterior</button><button class="danger" id="clear">Limpar</button><button class="primary" id="next">Próxima</button></footer></div>`;
  app.querySelector('#closeMachine').onclick=closeMachine;
  app.querySelector('#toggleMode').onclick=()=>{machineMode=machineMode==='edit'?'result':'edit';renderMachine();};
  app.querySelector('#previous').onclick=()=>navigate(-1);
  app.querySelector('#next').onclick=()=>navigate(1);
  app.querySelector('#clear').onclick=()=>{if(!confirm(`Limpar os dados da máquina ${machineLabel(machine.machine)}?`))return;const clean=createDefaultMachine({machine:machine.machine,id:machine.id});Object.assign(machine,clean);persist();machineMode='edit';renderMachine();};
  if(machineMode==='result'&&result.valid)renderResult(machine,result);else renderEditor(machine,result);
}

function renderEditor(machine,result){
  const body=app.querySelector('#machineBody');
  const useSum=state.settings.gabaritoMode==='sum';
  body.innerHTML=`<div class="editorGrid">${field('Ciclo','cycle',machine.cycle,'2,24','decimal')}${field('Peças restantes','currentBarValue',machine.currentBarValue,'0','decimal',`<select data-field="currentBarMode"><option value="pieces" ${machine.currentBarMode==='pieces'?'selected':''}>Peças</option><option value="partialMm" ${machine.currentBarMode==='partialMm'?'selected':''}>Milímetros</option><option value="full" ${machine.currentBarMode==='full'?'selected':''}>Barra cheia</option></select>`)}${field('Meta da OP','target',machine.target,'1000','numeric')}${field('Peça (mm)','pieceLength',machine.pieceLength,'32','decimal')}${field('Barras','fullBars',machine.fullBars,'0','numeric','',true)}<section class="field wide"><label>Gabaritos</label>${useSum?`<input id="trayExpression" value="${esc((machine.trays||[]).filter(Boolean).join('+'))}" inputmode="numeric" placeholder="60+40+39+22">`:`<div id="trayList">${trayRows(machine)}</div><button class="button" id="addTray" type="button">Adicionar gabarito</button>`}<small>Turnos passados: <strong id="trayTotal">${trayTotal(machine)}</strong></small></section></div><div id="validation">${validationMarkup(result)}</div>`;
  body.querySelectorAll('[data-field]').forEach(input=>{input.addEventListener('input',()=>{machine[input.dataset.field]=input.value;persist();updateEditorPreview(machine);});input.addEventListener('change',()=>{machine[input.dataset.field]=input.value;const current=ensureStarted(machine);persist();updateEditorPreview(machine,current);});});
  if(useSum){const expression=body.querySelector('#trayExpression');expression.oninput=()=>{const valid=/^\s*\d*(?:\s*\+\s*\d+)*\s*$/.test(expression.value);if(valid){machine.trays=expression.value.split('+').map(value=>value.trim()).filter(Boolean);persist();body.querySelector('#trayTotal').textContent=trayTotal(machine);updateEditorPreview(machine);}};}else{bindTrayEvents(machine);body.querySelector('#addTray').onclick=()=>{machine.trays.push('');persist();renderEditor(machine,calculate(machine));requestAnimationFrame(()=>body.querySelectorAll('[data-tray]')[machine.trays.length-1]?.focus());};}
}
function field(label,name,value,placeholder,inputmode,extra='',wide=false){return `<div class="field ${wide?'wide':''}"><label>${label}</label><input data-field="${name}" inputmode="${inputmode}" value="${esc(value)}" placeholder="${placeholder}">${extra}</div>`;}
function trayRows(machine){return machine.trays.map((value,index)=>`<div class="trayRow"><input data-tray="${index}" inputmode="numeric" value="${esc(value)}" placeholder="Quantidade"><button data-remove-tray="${index}" type="button">Remover</button></div>`).join('');}
function bindTrayEvents(machine){app.querySelectorAll('[data-tray]').forEach(input=>input.oninput=()=>{machine.trays[Number(input.dataset.tray)]=input.value;persist();app.querySelector('#trayTotal').textContent=trayTotal(machine);updateEditorPreview(machine);});app.querySelectorAll('[data-remove-tray]').forEach(button=>button.onclick=()=>{machine.trays.splice(Number(button.dataset.removeTray),1);if(!machine.trays.length)machine.trays=[''];persist();renderEditor(machine,calculate(machine));});}
function validationMarkup(result){if(result.valid)return '<div class="section"><strong>Cálculo válido</strong><small> Salvo automaticamente.</small></div>';return `<div class="validation">${(result.validation?.errors||[]).map(error=>`<div>${esc(error.message||error)}</div>`).join('')||'Preencha os dados principais.'}</div>`;}
function updateEditorPreview(machine,result=calculate(machine)){const node=app.querySelector('#validation');if(node)node.innerHTML=validationMarkup(result);}

function renderResult(machine,result){
  const body=app.querySelector('#machineBody');const progress=result.production.target?Math.min(100,(result.production.completedEstimated/result.production.target)*100):0;const materialPercent=result.material.perBar?Math.min(100,(result.material.currentPieces/result.material.perBar)*100):0;
  body.innerHTML=`<section class="section hero status-${result.status.key}"><div class="statusText">${result.status.label}</div><div class="countdown" data-live-countdown>${formatClock(result.forecast.remainingMs)}</div><div class="progress"><i style="width:${progress}%"></i></div></section><section class="section"><h2>Produção</h2><div class="metricGrid">${metric('Meta da OP',result.production.target)}${metric('Faltam',result.production.remainingOrder,'data-live-remaining')}${metric('Produção atual estimada',result.production.currentEstimated,'data-live-current')}${metric('Turnos passados',result.production.previousShifts)}</div></section><section class="section"><h2>Matéria-prima</h2><strong>${result.material.currentPieces} / ${result.material.perBar} peças na barra atual</strong><div class="materialBar"><i style="width:${materialPercent}%"></i></div><div class="metricGrid">${metric('MP disponível',result.material.totalCapacity)}${metric('Barras inteiras',result.material.fullBars)}${metric('Peças por barra',result.material.perBar)}${metric('Motivo do fim',result.forecast.reason==='order'?'Meta da OP':'Falta de MP')}</div></section><section class="section"><h2>Dados do cálculo</h2><div class="metricGrid">${metric('Tempo informado',result.cycle.informed)}${metric('Tempo convertido',result.cycle.decimalMinutes.toFixed(4)+' min')}${metric('Cálculo iniciado',formatDateTime(machine.calculationStartedAt))}${metric('Previsão',formatDateTime(result.forecast.endAt))}</div><details><summary>Ver cálculo</summary><pre>${esc(JSON.stringify(result.audit,null,2))}</pre></details></section>${result.preset.required?renderPreset(machine):''}`;
  bindPreset(machine);
}
function metric(label,value,attr=''){return `<div class="metric"><span>${label}</span><strong ${attr}>${esc(value)}</strong></div>`;}
function renderPreset(machine){return `<section class="section"><h2>Próxima OP</h2><div class="editorGrid"><div class="field"><label>Preset já trouxe?</label><select data-preset="brought"><option value="false" ${!machine.preset.brought?'selected':''}>Não</option><option value="true" ${machine.preset.brought?'selected':''}>Sim</option></select></div>${machine.preset.brought?`<div class="field"><label>Tipo</label><select data-preset="type"><option value="sequencia" ${machine.preset.type==='sequencia'?'selected':''}>Sequência</option><option value="azul" ${machine.preset.type==='azul'?'selected':''}>Setup azul</option><option value="verde" ${machine.preset.type==='verde'?'selected':''}>Setup verde</option><option value="vermelho" ${machine.preset.type==='vermelho'?'selected':''}>Setup vermelho</option></select></div>`:''}</div></section>`;}
function bindPreset(machine){app.querySelectorAll('[data-preset]').forEach(input=>input.onchange=()=>{machine.preset[input.dataset.preset]=input.dataset.preset==='brought'?input.value==='true':input.value;persist();renderMachine();});}

function renderSettings(){
  const machines=currentMachines();
  app.innerHTML=`<div class="settingsScreen"><header class="modalHeader"><button class="button" id="closeSettings">Voltar</button><div><strong>Ajustes</strong><small>Célula ${state.selectedCell}</small></div><button class="primary" id="saveSettings">Salvar</button></header><main class="settingsBody"><section class="section"><h2>Cálculo</h2><div class="editorGrid">${field('Comprimento da barra (mm)','setting-barLength',state.settings.barLength,'3600','decimal')}${field('Largura do bedame (mm)','setting-kerfWidth',state.settings.kerfWidth,'1','decimal')}${field('Janela do preset (h)','setting-presetLimitHours',state.settings.presetLimitHours,'16','decimal')}<div class="field"><label>Gabaritos</label><select id="setting-gabaritoMode"><option value="individual" ${state.settings.gabaritoMode==='individual'?'selected':''}>Campos individuais</option><option value="sum" ${state.settings.gabaritoMode==='sum'?'selected':''}>Soma rápida</option></select></div></div></section><section class="section"><div class="sectionHeader"><h2>Ordem das máquinas</h2><button class="button" id="restoreOrder">Restaurar</button></div><div class="orderList">${machines.map((machine,index)=>`<div class="orderRow"><strong>${machineLabel(machine.machine)}</strong><div><button data-move="-1" data-id="${esc(machine.id)}" ${index===0?'disabled':''}>Subir</button><button data-move="1" data-id="${esc(machine.id)}" ${index===machines.length-1?'disabled':''}>Descer</button></div></div>`).join('')}</div></section><section class="section"><h2>Dados</h2><p class="muted">As alterações são salvas apenas neste aparelho. A ordem é independente para cada célula.</p></section></main></div>`;
  app.querySelector('#closeSettings').onclick=renderDashboard;
  app.querySelector('#saveSettings').onclick=()=>{const next=sanitizeSettings({barLength:app.querySelector('[data-field="setting-barLength"]').value,kerfWidth:app.querySelector('[data-field="setting-kerfWidth"]').value,presetLimitHours:app.querySelector('[data-field="setting-presetLimitHours"]').value,gabaritoMode:app.querySelector('#setting-gabaritoMode').value},state.settings);state.settings=next;persist();renderDashboard();};
  app.querySelectorAll('[data-move]').forEach(button=>button.onclick=()=>{state.cells[state.selectedCell]=moveMachine(currentMachines(),button.dataset.id,Number(button.dataset.move));persist();renderSettings();});
  app.querySelector('#restoreOrder').onclick=()=>{state.cells[state.selectedCell]=restoreMachineOrder(currentMachines(),CELL_MACHINES[state.selectedCell]||[]);persist();renderSettings();};
}

function refreshVisible(){if(!activeMachineId||machineMode!=='result')return;const machine=getMachine(activeMachineId),result=calculate(machine);if(!result.valid)return;const countdown=app.querySelector('[data-live-countdown]');if(countdown)countdown.textContent=formatClock(result.forecast.remainingMs);const remaining=app.querySelector('[data-live-remaining]');if(remaining)remaining.textContent=result.production.remainingOrder;const current=app.querySelector('[data-live-current]');if(current)current.textContent=result.production.currentEstimated;}

if('serviceWorker' in navigator){window.addEventListener('load',()=>navigator.serviceWorker.register('./sw.js').catch(error=>console.warn('Service worker não registrado',error)));}
render();
