from pathlib import Path
import re

path=Path('index.html')
raw=path.read_bytes()
newline='\r\n' if b'\r\n' in raw else '\n'
text=raw.decode('utf-8').replace('\r\n','\n').replace('\r','\n')
text=text.replace('<title>PULSE CNC | V12.1.0</title>','<title>PULSE CNC | V12.1.1</title>',1)

old='''    function openMachineScreen(machineId, requestedMode = null) {
      const machine = state.machines.find(item => item.id === machineId);
      if (!machine) return;
      activeMachineId = machineId;
      const calc = calcMachine(machine);
      machineScreenMode = requestedMode || (calc.valid ? "result" : "edit");
      renderMachineScreen();
      if (!machineScreen.open) machineScreen.showModal();
      document.body.classList.add("machine-screen-open");
      requestAnimationFrame(() => {
        machineQueue.querySelector('.queueMachine.is-active')?.scrollIntoView({ behavior:"smooth", inline:"center", block:"nearest" });
      });
    }'''
new='''    function openMachineScreen(machineId, requestedMode = null) {
      const machine = state.machines.find(item => item.id === machineId);
      if (!machine) return;
      activeMachineId = machineId;
      const calc = calcMachine(machine);
      machineScreenMode = requestedMode || (calc.valid ? "result" : "edit");
      try {
        if (!machineScreen.open) machineScreen.showModal();
        document.body.classList.add("machine-screen-open");
        renderMachineScreen();
      } catch (error) {
        console.error("Falha ao abrir máquina", error);
        machineScreenMode = "edit";
        if (!machineScreen.open) machineScreen.showModal();
        document.body.classList.add("machine-screen-open");
        renderMachineScreen();
      }
      requestAnimationFrame(() => {
        machineQueue.querySelector('.queueMachine.is-active')?.scrollIntoView({ behavior:"smooth", inline:"center", block:"nearest" });
      });
    }'''
if old not in text: raise RuntimeError('openMachineScreen original não encontrada')
text=text.replace(old,new,1)

anchor='''    function bindActions(root, machine) {
      root.querySelector('[data-action="toggle"]').addEventListener("click", () => {
        openMachineScreen(machine.id);
      });'''
replacement='''    function bindActions(root, machine) {
      const openFromCard = event => {
        if (event.target.closest('button, input, select, textarea, label, a')) return;
        openMachineScreen(machine.id);
      };
      root.addEventListener("click", openFromCard);
      root.style.cursor = "pointer";
      root.setAttribute("role", "button");
      root.setAttribute("tabindex", "0");
      root.addEventListener("keydown", event => {
        if (event.key !== "Enter" && event.key !== " ") return;
        event.preventDefault();
        openMachineScreen(machine.id);
      });
      root.querySelector('[data-action="toggle"]').addEventListener("click", event => {
        event.stopPropagation();
        openMachineScreen(machine.id);
      });'''
if anchor not in text: raise RuntimeError('bindActions original não encontrada')
text=text.replace(anchor,replacement,1)

css='''
    /* PULSE CNC V12.1.1 — área inteira do card abre a máquina */
    .machineCard{cursor:pointer;-webkit-tap-highlight-color:transparent;touch-action:manipulation}
    .machineCard:active{transform:scale(.995)}
'''
text=text.replace('</style>',css+'\n  </style>',1)

for marker in ['<title>PULSE CNC | V12.1.1</title>','const openFromCard = event =>','Falha ao abrir máquina','PULSE CNC V12.1.1']:
    if marker not in text: raise RuntimeError('marcador ausente: '+marker)
path.write_bytes(text.replace('\n',newline).encode('utf-8'))
print('correção aplicada')
