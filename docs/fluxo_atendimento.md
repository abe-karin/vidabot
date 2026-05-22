# Fluxo de Atendimento — VidaBot (Árvore Conversacional)

Documento: árvore de decisão em texto para os 5 tipos principais de consulta definidos no desafio.

Formato: cada nó indica "Entrada do usuário → RAG → Resposta do bot → Pergunta de follow‑up / Ação".

--------------------------------------------------------------------------------
Tipo A — Abertura de Sinistro

- Usuário: "Quero abrir um sinistro" / "Houve um falecimento / acidente"
  - RAG: busca por chunks: `COMO ABRIR UM SINISTRO`, `DOCUMENTAÇÃO PARA SINISTRO` → retorna top chunks
  - Bot (resposta): explica passos iniciais (ligações, portal, documentos necessários) e prazo SUSEP (30 dias)
  - Follow-up 1: "Você já tem número da apólice?" → se não
    - Ação: pedir número da apólice, CPF do segurado e instruções sobre como enviar documentos (upload ou e‑mail)
  - Follow-up 2: "Deseja que eu gere a lista de documentos para sinistro?" → se sim
    - Ação: bot lista documentos (certidão, RG/CPF, BO, laudo, dados bancários)
  - Escalação: se usuário solicitar acompanhamento humano ou caso de urgência, fornecer contato 0800/WhatsApp e oferecer abertura de chamado humano

--------------------------------------------------------------------------------
Tipo B — Dúvidas sobre Cobertura

- Usuário: "Esta situação está coberta?" / "Cobertura X inclui Y?"
  - RAG: busca `COBERTURA BÁSICA DE MORTE`, `INVALIDEZ POR ACIDENTE`, `DOENÇAS GRAVES`, `EXCLUSÕES`
  - Bot (resposta): apresenta interpretação embasada (ex.: cobertura por morte natural após carência 180 dias; exclusões listadas)
  - Follow-up 1: "Qual é a carência aplicável neste caso?" → mostrar trecho relevante (SUSEP/CNSP)
  - Follow-up 2: "Deseja ver a cláusula completa da apólice?" → indicar opção de solicitar segunda via da apólice
  - Escalação: se dúvida jurídica/complexa, recomendar atendimento humano especializado e registrar protocolo

--------------------------------------------------------------------------------
Tipo C — Cancelamento / Portabilidade

- Usuário: "Quero cancelar" / "Posso portar minha apólice?"
  - RAG: busca `CANCELAMENTO E PORTABILIDADE`, `PRÊMIO E PAGAMENTO`
  - Bot (resposta): explica direitos (direito de arrependimento 7 dias, portabilidade sem perda de carências já cumpridas, prazos de inadimplência)
  - Follow-up 1: "Deseja iniciar o cancelamento agora?" → se sim
    - Ação: instruir formulário/portal e possíveis consequências (taxas, reabilitação)
  - Follow-up 2: "Quer gerar instruções para portabilidade?" → fornecer passos e documentos necessários
  - Escalação: processos que requerem análise documental são encaminhados ao time humano com checklist gerado pelo bot

--------------------------------------------------------------------------------
Tipo D — Segunda Via / Documentos

- Usuário: "Preciso da segunda via da apólice" / "Como enviar documentos?"
  - RAG: busca `SEGUNDA VIA DA APÓLICE`, `DOCUMENTAÇÃO PARA SINISTRO`, `ATUALIZAÇÃO DE DADOS CADASTRAIS`
  - Bot (resposta): informa prazos (ex.: até 5 dias úteis), canais (portal, e‑mail, WhatsApp) e lista de documentos aceitos
  - Follow-up 1: "Quer que eu envie instruções por e‑mail?" → solicitar endereço e confirmar envio (simulação)
  - Follow-up 2: "Deseja instruções passo a passo para upload no portal?" → fornecer passo a passo resumido
  - Escalação: se documento exigir validação humana (certidões autenticadas), instruir encaminhamento ao back‑office

--------------------------------------------------------------------------------
Tipo E — Solicitação de Atendimento Humano

- Usuário: "Quero falar com um atendente" / "Meu caso é urgente / complexo"
  - RAG: busca `ATENDIMENTO HUMANO`, `GUIA DE SINISTROS`
  - Bot (resposta): fornece canais (0800, WhatsApp, horário) e oferece abertura de chamado com resumo automático (coleção de dados básicos)
  - Follow-up 1: "Deseja abrir um chamado agora?" → se sim
    - Ação: coletar nome, telefone, número da apólice, breve descrição e criar resumo para o humano (template)
  - Follow-up 2: "Prefere contato por e‑mail ou telefone?" → agendamento/confirmar preferência
  - Escalação imediata: situações de risco/urgência são instruídas a ligar para a linha 24h e são marcadas como prioridade

--------------------------------------------------------------------------------
Notas operacionais (comportamento do bot)
- Em todas as rotas, o bot tenta recuperar até `top_k=3` chunks relevantes e injeta o contexto no `system prompt` antes de gerar a resposta.
- O bot limita respostas a 3 parágrafos e finaliza com uma pergunta de confirmação (ex.: "Posso ajudar em mais alguma coisa?").
- Para perguntas fora do domínio (baixa similaridade com `faq.txt`), o bot sugere atendimento humano e registra o diálogo como "fora do escopo".
- Em casos sensíveis (jurídicos, litígios, fraudes), o bot sempre recomenda contato humano e não fornece parecer jurídico.

--------------------------------------------------------------------------------
Exemplo de template de follow‑up (para escalação humana):

```
Resumo para back‑office:
- Nome: [NOME]
- Telefone: [TEL]
- Apólice: [NÚMERO]
- Tipo de solicitação: [SINISTRO / CANCELAMENTO / DOCUMENTO]
- Descrição: [TEXTO RESUMIDO]
- Chunks ativados: [FONTE 1 — trecho; FONTE 2 — trecho]
```

--------------------------------------------------------------------------------
Arquivo relacionado: `app.py` (lógica RAG, construção do `system prompt` e seleção de provedor).

Fim do documento
