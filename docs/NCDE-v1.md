# NCDE v1.0 — Neo CNC Decision Engine

## Objetivo

O NCDE é o motor responsável por analisar o turno inteiro antes de recomendar qualquer jantar, revezamento ou próximo setup.

Ele não pode escolher apenas quem está livre naquele momento. Cada decisão deve ser simulada até o fim do turno para verificar o impacto sobre:

- jantares;
- revezamentos;
- setups em andamento;
- próximos setups;
- disponibilidade futura;
- pessoas de reserva;
- conflitos de horário.

O sistema só pode exibir **Plano validado** quando todos os requisitos obrigatórios forem atendidos.

---

## 1. Entidades principais

### Preparador

```js
{
  id: "lucas-v",
  nome: "Lucas V.",
  aliases: ["Lucas", "Lucas V", "Lucas V."],
  presente: true,
  statusAtual: "AJUSTE",
  maquinaAtual: "TNL093",
  livreEm: null,
  jantar: null,
  tarefaFutura: null,
  indisponibilidades: []
}
```

### Tarefa

```js
{
  id: "setup-tnl005-2030",
  tipo: "SETUP_FUTURO",
  maquina: "TNL005",
  inicio: "20:30",
  fimEstimado: "22:40",
  responsavel: null,
  prioridade: 100,
  obrigatoria: true
}
```

Tipos iniciais:

- `SETUP_ATUAL`
- `AJUSTE`
- `REVEZAMENTO`
- `JANTAR`
- `SETUP_FUTURO`
- `RESERVA`

### Plano

```js
{
  atribuicoes: [],
  conflitos: [],
  alertas: [],
  pontuacao: 0,
  validado: false,
  explicacao: []
}
```

---

## 2. Regras obrigatórias

Um plano é inválido quando qualquer uma destas condições ocorrer:

1. Um preparador aparece em duas tarefas sobrepostas.
2. Um preparador janta e trabalha no mesmo intervalo.
3. Um próximo setup obrigatório fica sem responsável.
4. Um preparador fica sem jantar dentro da janela permitida.
5. Um preparador assume um setup antes de estar livre.
6. Uma pessoa cobre duas máquinas incompatíveis no mesmo intervalo.
7. A mesma tarefa é atribuída mais de uma vez.
8. Um alias é tratado como uma pessoa diferente.
9. O sistema marca o plano como validado contendo `SEM RESPONSÁVEL`.
10. Uma troca resolve um conflito, mas cria outro conflito não informado.

---

## 3. Critério de validação

```js
function validarPlano(plano) {
  const conflitosCriticos = plano.conflitos.filter(c => c.severidade === "CRITICA");
  const tarefasObrigatoriasAbertas = plano.atribuicoes.filter(
    a => a.obrigatoria && !a.responsavel
  );

  return conflitosCriticos.length === 0 && tarefasObrigatoriasAbertas.length === 0;
}
```

A mensagem **Plano validado** depende exclusivamente desse resultado.

---

## 4. Pontuação

A pontuação serve para escolher o melhor entre planos válidos. Ela nunca deve transformar um plano inválido em aceitável.

### Recompensas

- +1000 por plano totalmente válido;
- +120 por próximo setup obrigatório atendido;
- +80 por jantar realizado;
- +40 por manter uma pessoa de reserva;
- +25 por usar alguém sem tarefa futura crítica;
- +15 por reduzir trocas desnecessárias;
- +10 por distribuir os jantares de forma equilibrada.

### Penalidades

- −10000 por próximo setup obrigatório sem responsável;
- −8000 por alguém sem jantar;
- −7000 por conflito de horário;
- −500 por utilizar a última pessoa de reserva;
- −250 por criar sequência frágil dependente de horário exato;
- −100 por troca desnecessária;
- −50 por atrasar jantar sem necessidade.

---

## 5. Busca de cenários

A primeira versão deve usar busca em feixe (`beam search`).

Fluxo:

```text
Estado inicial
    ↓
Gerar ações possíveis
    ↓
Aplicar cada ação
    ↓
Descartar estados inválidos
    ↓
Pontuar estados restantes
    ↓
Manter os melhores estados
    ↓
Avançar para o próximo evento
    ↓
Repetir até o fim do turno
```

Eventos devem ser processados em ordem cronológica.

Ações possíveis:

- iniciar jantar;
- terminar jantar;
- assumir revezamento;
- liberar revezamento;
- assumir setup futuro;
- trocar responsáveis;
- antecipar jantar;
- adiar jantar dentro da janela;
- manter pessoa como reserva.

Parâmetros iniciais sugeridos:

```js
const SEARCH_CONFIG = {
  beamWidth: 250,
  maxStates: 30000,
  maxRuntimeMs: 1500,
  alternatives: 3
};
```

O limite de tempo evita travar celulares mais fracos.

---

## 6. Busca de reparo

Quando um próximo setup ficar sem responsável, o motor não pode parar imediatamente.

Ele deve executar uma busca de reparo:

1. identificar o conflito;
2. localizar todos os preparadores que poderiam assumir o setup;
3. simular a retirada de cada candidato de sua tarefa atual;
4. procurar quem pode substituir esse candidato;
5. continuar a cadeia de trocas;
6. validar novamente todos os jantares e setups;
7. escolher a cadeia válida de menor custo.

Exemplo de resposta:

```text
TNL027 estava sem responsável.

Solução encontrada:
1. Lucas cobre Alan das 18:30 às 19:30.
2. Alan assume a TNL027.
3. Everson permanece disponível para a TNL005.

Nenhum outro setup ou jantar foi prejudicado.
```

Somente depois de esgotar a busca o sistema pode afirmar que não existe solução.

---

## 7. Explicações

Toda recomendação deve responder:

- quem foi escolhido;
- por que foi escolhido;
- qual problema foi evitado;
- quais alternativas foram descartadas;
- qual é o risco do plano;
- o que muda se houver atraso.

Exemplo:

```text
Sugestão: Marlon cobre Clayton às 19:30.

Motivos:
- Marlon está livre nesse intervalo;
- não possui setup futuro crítico;
- Lucas permanece disponível para a TNL005;
- Everson continua como reserva;
- todos os jantares permanecem dentro da janela.
```

---

## 8. Confiança

A confiança não deve ser inventada. Ela deve ser calculada pela robustez do plano.

Fatores:

- quantidade de alternativas válidas;
- quantidade de pessoas de reserva;
- folga entre tarefas;
- dependência de horários exatos;
- impacto de atrasos de 5, 10 e 15 minutos.

Exemplo:

```js
confianca = 100
  - riscoSemReserva
  - riscoDeAtraso
  - riscoDeDependencia
  + bonusAlternativas;
```

Faixas:

- 90–100: robusto;
- 75–89: seguro;
- 60–74: atenção;
- abaixo de 60: frágil.

---

## 9. Simulação de atraso

Após encontrar o melhor plano, o motor deve testar automaticamente:

- atraso de 5 minutos;
- atraso de 10 minutos;
- atraso de 15 minutos.

Se um atraso pequeno quebrar o plano, a interface deve informar:

```text
Plano válido, porém frágil.
Um atraso de 5 minutos na TNL093 deixa a TNL005 descoberta.
```

---

## 10. Saída do motor

```js
{
  status: "VALIDADO",
  score: 96,
  confidence: 91,
  scenariosTested: 12438,
  bestPlan: {},
  alternatives: [],
  conflicts: [],
  opportunities: [],
  explanations: [],
  whatsappReport: ""
}
```

Status possíveis:

- `VALIDADO`
- `VALIDO_FRAGIL`
- `REPARO_SUGERIDO`
- `SEM_SOLUCAO`
- `DADOS_INCOMPLETOS`

---

## 11. Relatório para WhatsApp

O relatório deve ser organizado por preparador, e não apenas por evento.

```text
*REVEZAMENTO — 2º TURNO*

*ALAN*
TNL116
Janta: 18:30–19:30
Cobertura: Everson
Próximo setup: TNL027

*LUCAS V.*
Ajuste TNL093
Janta: 20:30–21:30
Cobertura: Marlon
Próximo setup: TNL005
```

Ao final:

```text
*VALIDAÇÃO DO PLANO*
✅ Todos os jantares definidos
✅ Todos os próximos setups com responsável
✅ Nenhum conflito de horário
🟢 Reserva operacional: 1 preparador
```

Se houver conflito, o relatório não deve usar a palavra `validado`.

---

## 12. Plano de implementação

### Fase 1 — Modelo e validação

- normalização definitiva de nomes e aliases;
- criação das entidades;
- detecção de sobreposição;
- validação obrigatória;
- bloqueio de falso `Plano validado`.

### Fase 2 — Otimizador global

- linha do tempo completa;
- geração de ações;
- beam search;
- pontuação;
- três melhores planos.

### Fase 3 — Reparo automático

- busca por cadeias de troca;
- antecipação e adiamento de jantares;
- sugestão concreta para setups descobertos.

### Fase 4 — Explicação e robustez

- motivos da escolha;
- comparação com alternativas;
- simulação de atrasos;
- confiança calculada.

### Fase 5 — Interface

- tela “Analisando cenários...”;
- painel de conflitos;
- botão “Aplicar sequência”;
- comparação entre planos;
- relatório final por preparador.

---

## Regra central do NCDE

> O motor deve pensar na fábrica inteira até o fim do turno antes de recomendar qualquer decisão local.
