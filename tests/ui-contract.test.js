import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

const html=await readFile(new URL('../beta/index.html',import.meta.url),'utf8');
const js=await readFile(new URL('../beta/app.js',import.meta.url),'utf8');
const css=await readFile(new URL('../beta/app.css',import.meta.url),'utf8');
const manifest=JSON.parse(await readFile(new URL('../beta/manifest.json',import.meta.url),'utf8'));
const sw=await readFile(new URL('../beta/sw.js',import.meta.url),'utf8');

test('beta possui identidade e entrada modular',()=>{
  assert.match(html,/PULSE CNC 1\.0 Beta/);
  assert.match(html,/type="module"/);
  assert.match(html,/\.\/app\.js/);
});

test('interface usa motor e storage únicos',()=>{
  assert.match(js,/import \{ calculateMachine \}/);
  assert.match(js,/import \{ createDefaultMachine, loadState, saveState \}/);
  assert.match(js,/return calculateMachine\(machineInput\(machine\)/);
  assert.match(js,/state=saveState\(localStorage,state\)/);
});

test('linha inteira abre máquina com um toque',()=>{
  assert.match(js,/data-machine/);
  assert.match(js,/card\.onclick=\(\)=>openMachine/);
  assert.match(css,/touch-action:manipulation/);
});

test('editor mantém ordem operacional',()=>{
  const cycle=js.indexOf("field('Ciclo'");
  const remaining=js.indexOf("field('Peças restantes'");
  const target=js.indexOf("field('Meta da OP'");
  const piece=js.indexOf("field('Peça (mm)'");
  const bars=js.indexOf("field('Barras'");
  const trays=js.indexOf('Gabaritos');
  assert.ok(cycle<remaining&&remaining<target&&target<piece&&piece<bars&&bars<trays);
});

test('resultado exibe cálculos completos vindos do motor',()=>{
  for(const label of [
    'Produção','Matéria-prima','Dados do cálculo','Próxima OP',
    'Meta da OP','Turnos passados','Produção do turno','Total estimado','Faltam','Até a parada',
    'Peças por barra','MP disponível','Ciclo informado','Ciclo em segundos','Fração de minuto',
    'Cálculo iniciado','Previsão fixa','Confiança','Ver memória do cálculo'
  ]) assert.match(js,new RegExp(label));
  assert.match(js,/result\.production\.currentEstimated/);
  assert.match(js,/result\.production\.remainingOrder/);
  assert.match(js,/result\.material\.totalCapacity/);
  assert.match(js,/result\.forecast\.piecesUntilStop/);
  assert.match(js,/result\.cycle\.decimalMinutes/);
});

test('status usa apenas cores e não emojis operacionais',()=>{
  assert.match(css,/--green/);
  assert.match(css,/--orange/);
  assert.match(css,/--red/);
  assert.doesNotMatch(js,/🟢|🟠|🔴/);
});

test('layout é compacto em dashboard, editor, gabaritos e ajustes',()=>{
  for(const selector of ['machineRow','compactEditor','gabaritoPanel','trayRow','settingsCard','orderRow','moveButtons']) assert.match(css,new RegExp(selector));
  assert.match(js,/aria-label="Remover gabarito"/);
  assert.match(js,/aria-label="Mover para cima"/);
  assert.match(js,/aria-label="Mover para baixo"/);
});

test('ajustes possuem bedame, gabaritos e ordem por célula',()=>{
  assert.match(js,/Largura do bedame/);
  assert.match(js,/Campos individuais/);
  assert.match(js,/Soma rápida/);
  assert.match(js,/moveMachine\(currentMachines/);
  assert.match(js,/restoreMachineOrder\(currentMachines/);
});

test('beta está preparada para instalação, atualização e uso offline',()=>{
  assert.match(html,/rel="manifest"/);
  assert.equal(manifest.name,'PULSE CNC');
  assert.equal(manifest.display,'standalone');
  assert.match(js,/serviceWorker\.register/);
  assert.match(sw,/pulse-cnc-beta-1\.0\.2/);
  assert.match(sw,/cache\.addAll/);
  assert.match(sw,/fetch\(event\.request\)/);
  assert.match(sw,/src\/core\/calc-engine\.js/);
});