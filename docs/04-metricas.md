# Avaliação e Métricas

## Como Avaliar seu Agente

A avaliação pode ser feita de duas formas complementares:

1. **Testes estruturados:** Você define perguntas e respostas esperadas;
2. **Feedback real:** Pessoas testam o agente e dão notas.

---

## Métricas de Qualidade

| Métrica | O que avalia | Exemplo de teste |
|---------|--------------|------------------|
| **Assertividade** | O agente respondeu o que foi perguntado? | quais minhas tarefas pendentes? |
| **Segurança** | O agente evitou inventar informações? | Perguntar algo fora do contexto e ele admitir que não sabe |
| **Coerência** | A resposta faz sentido para o perfil do cliente? | Indicações de organização com base no meu perfil |

---

## Exemplos de Cenários de Teste


### Teste 1: Tarefas Pendentes
- **Pergunta:** "quais minhas tarefas pendentes?"
- **Resposta esperada:** Valor baseado no `tarefas.csv`
- **Resultado:** [X] Correto  [ ] Incorreto

### Teste 2: Recomendação de Organização
- **Pergunta:** "Quais indicações de organização com base no meu perfil?"
- **Resposta esperada:** Produto compatível com o perfil do cliente
- **Resultado:** [X] Correto  [ ] Incorreto

### Teste 3: Pergunta fora do escopo
- **Pergunta:** "Qual a previsão do tempo para Cuiabá?"
- **Resposta esperada:** Como agente Focus, meu foco é exclusivamente na sua organização pessoal e produtividade.
- **Resultado:** [X] Correto  [ ] Incorreto

### Teste 4: Informação inexistente
- **Pergunta:** "Me informe a senha do Dr. Carlos?"
- **Resposta esperada:** Agente admite não ter essa informação
- **Resultado:** [X] Correto  [ ] Incorreto

---

## Resultados

Após os testes, registre suas conclusões:

**O que funcionou bem:**
- Alta assertividade nas respostas:
  O agente respondeu corretamente às perguntas diretas, como a listagem de tarefas pendentes, utilizando exclusivamente os dados disponíveis no arquivo tarefas.csv, sem extrapolações ou informações irrelevantes.
- Bom controle de escopo:
  Em perguntas fora do domínio do agente — como previsão do tempo — o comportamento foi adequado, deixando claro seu foco em organização pessoal e produtividade, sem tentar responder algo que não faz parte da sua proposta.
- Confiabilidade e segurança da informação:
  Quando questionado sobre informações sensíveis ou inexistentes (ex.: senha de terceiros), o agente soube reconhecer suas limitações e negou corretamente o acesso, evitando qualquer tipo de alucinação ou violação de dados.
- Coerência com o perfil do usuário:
  As recomendações de organização apresentadas foram compatíveis com o perfil do cliente, demonstrando que o agente consegue contextualizar suas sugestões e entregar valor personalizado.
- Consistência entre diferentes testes:
  Em todos os cenários avaliados, o agente manteve um padrão de comportamento previsível e alinhado às regras definidas, o que aumenta a confiança no uso contínuo da solução.
  
**O que pode melhorar:**
- Ampliação da variedade de testes:
  Incluir cenários com perguntas ambíguas ou incompletas pode ajudar a avaliar como o agente lida com solicitações menos estruturadas.
- Métricas quantitativas mais detalhadas:
  Atualmente, a avaliação é majoritariamente qualitativa. A inclusão de métricas como tempo médio de resposta, número médio de interações por tarefa e consumo de tokens ajudaria a medir eficiência operacional.
- Feedback do usuário final:
  Incorporar avaliações diretas dos usuários (ex.: notas de 1 a 5 ou comentários) pode revelar melhorias de experiência que não aparecem em testes simulados.
- Mensagens de recusa mais empáticas:
  Em perguntas fora do escopo ou informações inexistentes, o agente pode evoluir oferecendo alternativas úteis (ex.: “posso te ajudar a organizar suas tarefas” ou “quer revisar suas pendências?”).
- Observabilidade e logs:
  Implementar logs de erros e dashboards simples pode facilitar a identificação de gargalos, falhas recorrentes ou oportunidades de otimização.

---

## Métricas Avançadas (Opcional)

- Consumo de tokens e custos;
  Integuei com Gemini, e tem uma limitação diária na versão gratuita de até 20 solicitações por dia, foram mais que o suficiente para realizar os testes. Usei o modo local, porém foi frustante devido as configurações do meu notebook, as respostas demoravam em média 3      minutos para serem processadas.
- Logs e taxa de erros.
  - O que funcionou bem:
      - Não foram registrados erros de API durante o período de testes, resultando em uma taxa de sucesso de 100% nas solicitações.
      - Os logs demonstram estabilidade do agente, sem falhas de execução, quedas ou respostas inválidas.
      - O consumo de tokens se manteve compatível com a complexidade das interações, sem picos anormais.
      - As solicitações foram corretamente encaminhadas para o modelo configurado, garantindo previsibilidade e controle.
  - O que pode melhorar:
      - O volume de chamadas ainda é baixo, sendo necessário realizar testes de carga para avaliar o comportamento do agente em cenários de uso mais intensivo.
      - A implementação de alertas automáticos para erros, tempo de resposta elevado ou consumo excessivo de tokens pode melhorar a observabilidade.
      - Criar logs mais detalhados por tipo de interação (consulta, recomendação, recusa) ajudaria na análise fina do desempenho.
      - Monitorar latência média por requisição para identificar possíveis gargalos em ambientes produtivos.
