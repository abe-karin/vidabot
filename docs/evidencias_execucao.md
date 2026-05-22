# Evidências de Execução — VidaBot

Este documento descreve 8 telas/momentos do chatbot em funcionamento, pronto para inclusão no relatório de entrega do Desafio II.

1) Tela Inicial do VidaBot
- Descrição: Interface principal com cabeçalho (VidaBot — InsurMinds), área de mensagens, campo de entrada, botão de envio e sidebar com atalhos (Abrir Sinistro, Segunda Via, Atendimento Humano). Logo e cores navy/gold visíveis.
- O que o usuário fez: abriu a aplicação pela URL local/hosted.
- Resultado obtido: mensagem de boas‑vindas exibida pelo bot com ações rápidas sugeridas (ex.: "Como posso ajudar hoje?" e botões rápidos).
- Chunk RAG ativado: nenhum (boa‑vinda padrão).

2) Pergunta sobre sinistro + RAG ativado
- Descrição: o usuário pergunta "Como abro um sinistro por falecimento?"; painel RAG mostra 3 chunks com títulos e trechos; cada chunk possui score numérico.
- O que o usuário fez: digitou a pergunta e clicou em Enviar.
- Resultado obtido: VidaBot exibe passos para abertura (0800/portal), lista de documentos necessários e prazo SUSEP de 30 dias; painel RAG destaca `COMO ABRIR UM SINISTRO` e `DOCUMENTAÇÃO PARA SINISTRO`.
- Chunk RAG ativado: `COMO ABRIR UM SINISTRO`, `DOCUMENTAÇÃO PARA SINISTRO`, `DIREITOS DO SEGURADO`.

3) Pergunta sobre carência com citação SUSEP
- Descrição: usuário pergunta "Qual a carência para morte natural?"; resposta do bot inclui menção a CNSP/SUSEP e trecho da base.
- O que o usuário fez: enviou a pergunta curta.
- Resultado obtido: VidaBot responde "Carência de 180 dias para morte natural (CNSP/Circular SUSEP)" e mostra o trecho do `faq.txt` usado como evidência.
- Chunk RAG ativado: `CARÊNCIAS`, `DIREITOS DO SEGURADO`.

4) Atalho rápido do sidebar sendo usado
- Descrição: sidebar expandida com botões; usuário clica no atalho "Abrir Sinistro"; formulário leve aparece preenchido com instruções.
- O que o usuário fez: clicou no botão de atalho no sidebar.
- Resultado obtido: bot apresenta um fluxo guiado para iniciar sinistro (coleta de apólice, CPF e upload de documentos), com opção de encaminhar para humano.
- Chunk RAG ativado: `COMO ABRIR UM SINISTRO`.

5) Painel RAG expandido mostrando scores de relevância
- Descrição: visão expandida do painel RAG exibindo top_k=3 chunks, scores (ex.: 92, 78, 45), fontes e primeiras 120 chars dos trechos.
- O que o usuário fez: clicou em "Ver detalhes" no painel RAG.
- Resultado obtido: exibição dos trechos e opção de copiar/abrir fonte; usuário pode validar de onde a resposta foi extraída.
- Chunk RAG ativado: lista visível (ex.: `CARÊNCIAS`, `DOCUMENTAÇÃO PARA SINISTRO`, `PRÊMIO E PAGAMENTO`).

6) Fluxo animado RAG (6 etapas visuais)
- Descrição: animação/indicador mostrando as etapas: 1) recebimento pergunta, 2) tokenização/extração keywords, 3) recuperação chunks, 4) scoring, 5) montagem do system prompt com contextos, 6) resposta do LLM.
- O que o usuário fez: observou o indicador de processamento durante a geração da resposta.
- Resultado obtido: usuário ganha transparência do processo e vê o tempo aproximado de cada etapa; resposta final aparece logo após etapa 6.
- Chunk RAG ativado: etapas mostram chunks intermediários conforme consulta (ex.: `DOENÇAS GRAVES`).

7) Pergunta fora do domínio → direcionamento para atendimento humano
- Descrição: usuário pede parecer jurídico complexo (fora do escopo); bot responde com aviso e oferta de abertura de chamado humano; mostra canais de contato.
- O que o usuário fez: solicitou opinião jurídica detalhada sobre contestação de sinistro.
- Resultado obtido: VidaBot não fornece parecer jurídico; recomenda contato humano, apresenta telefone/WhatsApp e oferece abrir um chamado com resumo automático.
- Chunk RAG ativado: `ATENDIMENTO HUMANO` (se aplicável) — caso contrário, nenhum chunk específico.

8) Estatísticas de uso ao final da sessão
- Descrição: tela de resumo de sessão exibindo: número de mensagens trocadas, tópicos mais consultados (carência, sinistro, documentos), tempo médio de resposta e botão para baixar o resumo em PDF.
- O que o usuário fez: encerrou a sessão ou clicou em "Resumo da Sessão".
- Resultado obtido: visualização de métricas e lista de trechos consultados; opção de enviar o resumo por e‑mail.
- Chunk RAG ativado: agregação dos chunks mais acionados durante a sessão (ex.: `CARÊNCIAS`, `DOCUMENTAÇÃO PARA SINISTRO`).

Observação final: os exemplos acima são descrições de telas para documentação; para evidências reais recomenda‑se capturar screenshots locais nos momentos descritos (ou exportar `docs/test_results.md` e logs de RAG para anexar).

Fim do documento
