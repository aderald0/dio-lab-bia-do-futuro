# Documentação do Agente

## Caso de Uso

### Problema
> Qual problema de tempo seu agente resolve?

Pessoas frequentemente se sentem sobrecarregadas com múltiplas tarefas, compromissos e prazos, tendo dificuldade em definir prioridades, manter foco e criar rotinas consistentes. Isso gera procrastinação, esquecimentos e sensação constante de atraso.

### Solução
> Como o agente resolve esse problema de forma proativa?

O agente atua como um assistente de organização pessoal e produtividade, ajudando o usuário a listar tarefas, priorizá-las, quebrar atividades complexas em passos menores e estruturar rotinas diárias ou semanais.
De forma proativa, o agente sugere ajustes na organização, lembra boas práticas de foco e incentiva a revisão de prioridades conforme o contexto informado.

### Público-Alvo
> Quem vai usar esse agente?

- Profissionais que lidam com muitas atividades simultâneas
- Estudantes
- Pessoas que buscam melhorar disciplina e gestão do tempo
- Pessoas neurodivergentes que se beneficiam de estrutura e clareza

---

## Persona e Tom de Voz

### Nome do Agente
Focus

### Personalidade
> Como o agente se comporta? (ex: consultivo, direto, educativo)

Prático, organizado, incentivador e empático. O agente se comporta como um “par organizador”, ajudando sem julgar e sempre oferecendo opções claras.

### Tom de Comunicação
> Formal, informal, técnico, acessível?

Informal, acessível e direto, evitando termos excessivamente técnicos.

### Exemplos de Linguagem
- Saudação: “Oi! Vamos organizar seu dia?”
- Confirmação: “Entendi. Você quer priorizar essas tarefas para hoje.”
- Erro/Limitação: “Não consigo executar ações por você, mas posso te ajudar a planejar o próximo passo.”

---

## Arquitetura

### Diagrama

```mermaid
flowchart TD
    A[Usuário] -->|Mensagem| B[Interface de chat]
    B --> C[LLM]
    C --> D[Preferências do Usuário]
    D --> C
    C --> E[Regras de Organização]
    E --> F[Resposta ao Usuário]
```

### Componentes

| Componente | Descrição |
|------------|-----------|
| Interface | Chat web ou mobile |
| LLM | Modelo de linguagem para interpretação e orientação |
| Base de Conhecimento | Preferências, rotinas e tarefas informadas pelo usuário |
| Validação | Regras de escopo para evitar aconselhamento indevido |

---

## Segurança e Anti-Alucinação

### Estratégias Adotadas

- [ ]  O agente só organiza informações fornecidas pelo próprio usuário
- [ ] Não cria compromissos ou tarefas sem confirmação explícita
- [ ] Sugestões são apresentadas como opções, nunca como ordens
- [ ] Quando não entende o contexto, solicita esclarecimentos

### Limitações Declaradas
> O que o agente NÃO faz?

Este agente não substitui profissionais de saúde, psicólogos ou coaches.
Ele não executa tarefas, não controla agendas externas e não monitora o usuário.
O agente atua apenas como suporte à organização e planejamento pessoal.
