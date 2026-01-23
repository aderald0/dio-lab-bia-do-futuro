# Base de Conhecimento

## Dados Utilizados

Objetivo: dar ao agente contexto suficiente para organizar tarefas, priorizar, sugerir rotinas e acompanhar progresso—sempre com consentimento explícito do usuário.

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `tarefas.csv` | CSV | Backlog de tarefas com prioridade, contexto, status e estimativa |
| `rotinas.json` | JSON | Blocos de rotina (manhã, tarde, noite), hábitos e frequência |
| `preferencias_usuario.json` | JSON | Preferências de comunicação, horários ideais de foco, estilo de lembrete |
| `calendario_eventos.csv` | CSV | Compromissos fixos (reuniões, prazos, consultas) |
| `bloqueios_log.csv` | CSV | Registro de bloqueios (procrastinação, interrupções) e possíveis causas |
| `progresso_semanal.csv` | CSV | Métricas de conclusão, tempo investido, streaks de hábitos |
| `contexto_trabalho.json` | JSON | Ambiente de trabalho (ex.: Service Desk), softwares, restrições de horário |

> [!TIP]
> **Quer um dataset mais robusto?** Você pode utilizar datasets públicos do [Hugging Face](https://huggingface.co/datasets) relacionados a finanças, desde que sejam adequados ao contexto do desafio.

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

- Normalização de campos: mapeamento de prioridades (Alta/Média/Baixa) e status (pendente/em_andamento/concluida).
- Deduplicação de tarefas: merge por titulo + contexto quando difere só em descrição.
- Criação de subtarefas: para tarefas longas (> 60 min), gerar automaticamente passos (ex.: “abrir arquivo”, “validar colunas”, “lançar alterações”, “checagem final”).
- Enriquecimento de contexto: adicionar tags e estimativa_min se ausentes (estimativa inicial padrão: 25 min).
- Privacidade: remover PII desnecessária de eventos (ex.: links de reunião, nomes de terceiros).
- Timezone: alinhar tudo para America/Sao_Paulo.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

- Carregamento inicial: ao iniciar a sessão, o agente tenta ler data/*.csv|json.
- Cache de sessão: dados estruturados em memória do agente para respostas rápidas.
- Atualizações incrementais: quando o usuário cria/edita tarefas, o agente atualiza a estrutura em memória e marca para persistir ao final da sessão.

   Ex.: “Os JSON/CSV são carregados no início da sessão e incluídos no contexto do prompt, com consultas dinâmicas conforme as intenções (priorizar, planejar, revisar).”

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

- System prompt (regras fixas): princípios do agente (não executar ações sem autorização, sugerir opções, respeitar janelas de foco, evitar overbooking).
- Contexto dinâmico do usuário: recortes dos dados relevantes à intenção atual:
  - Se a intenção for planejar o dia, incluir tarefas pendentes + eventos de hoje + preferências de janelas de foco.
  - Se for quebrar uma tarefa grande, incluir detalhes da tarefa + bloqueios anteriores + contexto_trabalho.
  - Se for retrospectiva semanal, incluir progresso_semanal.csv + tarefas concluídas/pendentes.
- Memória leve: preferências do Aderaldo para tom, número máximo de tarefas/dia, janelas de foco.

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```

[Persona]
Usuário: ADERALDO DE JESUS AMARAL (Analista Service Desk Jr)
Preferências: tom direto e positivo; sugestões em passos; blocos 25/5; janelas de foco 09:00–11:00, 14:00–16:00; evitar interrupções 12:00–13:00 e 18:00–07:00.

[Agenda de Hoje - 2026-01-23]
- 10:00–11:00 — Reunião SD (alinhamento semanal) [Obrigatório]
- 15:00–15:30 — Checagem PJE (verificar acessos e prazos) [Obrigatório]

[Tarefas Pendentes Relevantes]
- (T-001) Atualizar planilha Escala_Central — Pri: Alta; Urg: Alta; Est: 45min; Status: em_andamento; Deadline: 2026-01-23; Tags: planilha;ti;service_desk
- (T-002) Revisar checklist do PJE — Pri: Média; Urg: Média; Est: 30min; Status: pendente; Deadline: 2026-01-24; Tags: judiciario;software
- (T-004) Organizar e-mail (inbox zero) — Pri: Baixa; Urg: Baixa; Est: 25min; Status: pendente

[Bloqueios Recentes]
- T-001: interrupções por mensagens de chat às 10:40; Ação sugerida: modo não perturbe 25min
- T-004: procrastinação por falta de clareza; Ação sugerida: quebrar em subtarefas

[Regras do Agente]
- Não criar compromissos ou alterar dados sem confirmação explícita.
- Sugerir no máximo 5 tarefas para o dia (limitador de carga).
- Propor blocos concentrados nas janelas de foco; usar pomodoro 25/5.
- Quando o contexto for insuficiente, perguntar de forma objetiva.

[Pedido do Usuário]
"Ajudar a montar um plano para hoje priorizando tarefas mais urgentes."

[Resposta Esperada - Diretrizes]
- Propor agenda enxuta (<= 5 itens), encaixando tarefas entre 09:00–11:00 e 14:00–16:00,
  respeitando reuniões às 10:00–11:00 e 15:00–15:30.
- Começar por T-001 (deadline hoje), sugerindo um bloco de 45min + buffers.
- Quebrar T-004 em subtarefas para reduzir atrito.
- Oferecer duas opções de agenda (A/B) e pedir confirmação única.

```
