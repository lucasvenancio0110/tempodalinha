import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

const html=await readFile(new URL('../beta/index.html',import.meta.url),'utf8');
const js=await readFile(new URL('../beta/app.js',import.meta.url),'utf8');
const css=await readFile(new URL('../beta/app.css',import.meta.url),'utf8');

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

test('card inteiro abre máquina com um toque',()=>{
  assert.match(js,/data-machine/);
  assert.match(js,/card\.onclick=\(\)=>openMachine/);
});

test('editor mantém ordem operacional',()=>{
  const cycle=js.indexOf("field('Ciclo'");
  const remaining=js.indexOf("field('Peças restantes'");
  const target=js.indexOf("field('Meta da OP'");
  const piece=js.indexOf("field('Peça (mm)'");
  const bars=js.indexOf("field('Barras'");
  const trays=js.indexOf('<label>Gabaritos</label>');
  assert.ok(cycle<remaining&&remaining<target&&target<piece&&piece<bars&&bars<trays);
});

test('dashboard contém categorias operacionais',()=>{
  for(const label of ['Produção','Matéria-prima','Dados do cálculo','Próxima OP'])assert.match(js,new RegExp(label));
  assert.match(js,/Produção atual estimada/);
  assert.match(js,/Turnos passados/);
  assert.match(js,/Preset já trouxe/);
});

test('status usa apenas cores e não emojis operacionais',()=>{
  assert.match(css,/--green/);
  assert.match(css,/--orange/);
  assert.match(css,/--red/);
  assert.doesNotMatch(js,/🟢|🟠|🔴/);
});
