# Autoavaliação Técnica — VidaBot

Documento de autoavaliação elaborado para a entrega do Desafio II (InsurMinds — VidaBot). Este arquivo responde aos itens solicitados no enunciado e registra decisões técnicas, critérios de avaliação e propostas de melhoria.

## 1. O que foi implementado vs o que foi proposto

- Implementado:
  - Backend Flask com endpoint `/api/chat` e lógica RAG (`app.py`).
  - Frontend funcional em `frontend/index.html` com chat multi‑turno.
  - Base de conhecimento `faq.txt` com 15+ chunks.
  - Integração configurável com provedores LLM: OpenAI, Anthropic e Google Gemini (variáveis em `.env.example`).
  - Documentação técnica parcial: `README.md`, `docs/relatorio_insurminds_vidabot.pdf`, `docs/arquitetura_rag.svg`, `docs/deploy_render.md`.
  - Scripts auxiliares: `scripts/list_llm_models.py`, `scripts/run_tests.py` e `deploy_render.sh` (+ `render.yaml` de exemplo).
  - Artefatos produzidos para entrega: `docs/evidencias_execucao.md`, `docs/fluxo_atendimento.md`, `docs/analise_tecnica.md`, `docs/perguntas_teste.md`.

- Não implementado / parcialmente implementado (conforme proposta):
  - Geração de screenshots reais (capturas) — o documento `docs/evidencias_execucao.md` descreve os prints, mas as imagens não foram incluídas.
  - Automatização de deploy com push automático — o script gera `render.yaml` e instrui o deploy, mas não executa push por segurança.
  - Testes automatizados end‑to‑end com ambientes de CI — há `scripts/run_tests.py`, mas execução depende de chaves de API e ambiente seguro.

## 2. Quais critérios do Ciclo de Vida GenAI foram atendidos

- **Definição de propósito**: objetivo claro (atendimento ao segurado) e limitações explícitas (não emitir parecer jurídico; escalonar casos complexos).
- **Dados / Conhecimento**: KB (`faq.txt`) separada do modelo — permite atualizações sem retraining.
- **Modelagem e prompt design**: `SYSTEM_PROMPT` padronizado e injeção de contexto RAG no prompt; controles de comprimento e formato de resposta.
- **Avaliação**: perguntas de teste (`docs/perguntas_teste.md`) e `scripts/run_tests.py` fornecem mecanismo inicial de verificação de respostas.
- **Monitoramento e manutenção**: logs e `docs/test_results.md` (quando gerado) servem como artefatos para avaliação; `deploy_render.sh` facilita deploy e gestão de variáveis.
- **Governança e compliance**: rastreabilidade de fontes (chunks retornados) e menção a SUSEP/CNSP para evidência regulatória.

## 3. Melhorias que seriam implementadas com mais tempo

| Melhoria | Estimativa |
|---|---:|
| Incluir imagens reais (screenshots) e gravar vídeos demonstrativos | 2 a 4 horas |
| Implementar testes E2E automatizados (Selenium/Playwright) integrados a CI | 8 a 12 horas |
| Adotar armazenamento de KB versionado e interface admin para editar chunks | 12 a 20 horas |
| Implementar métricas e monitoramento em produção | 6 a 10 horas |
| Formalizar avaliação de qualidade com dataset de validação | 6 a 8 horas |
| Avaliar Fine‑Tuning ou Retrieval+Rerank, se necessário | 16 a 30 horas |

## 4. Lições aprendidas sobre RAG aplicado a seguros

- RAG oferece controle e auditabilidade essenciais em domínios regulados — permite apontar trechos de KB que embasaram cada resposta.
- Separar KB do gerador reduz o risco de 'vazar' políticas internas ou de desatualizar conhecimento crítico sem processo de governança.
- Prompt engineering e curadoria de chunks são atividades contínuas: qualidade da KB impacta diretamente a confiança do usuário.
- Integração com múltiplos provedores exige estratégias de fallback e testes de compatibilidade (por exemplo, preferir `claude-sonnet-4-20250514` quando disponível, conforme `README.md` e `.env.example`).

## 5. Referências técnicas usadas

- Material do curso I²A² — Aula 04 (RAG) — Prof. Celso Azevedo.  
- CNSP 294/2013 e regulação SUSEP (citadas no `faq.txt` e nas respostas).  
- Documentação Anthropic, OpenAI e Google Gemini para integração via SDK/API.
- Código do repositório: `app.py`, `faq.txt`, `frontend/index.html`, `scripts/run_tests.py`.

## 6. Checklist final (status)

- frontend/index.html — ✅ (presente)
- app.py — ✅ (presente; aceita POST; adicionada rota GET informativa)
- faq.txt — ✅ (15+ chunks)
- requirements.txt — ✅ (presente; verifique inclusão de `gunicorn` se necessário)
- .env.example — ✅ (presente; inclui `ANTHROPIC_MODEL` recomendado)
- docs/relatorio_insurminds_vidabot.pdf — ✅ (presente)
- docs/arquitetura_rag.svg — ✅ (presente)
- docs/evidencias_execucao.md — ✅ (presente; sem imagens)
- docs/fluxo_atendimento.md — ✅ (presente)
- docs/analise_tecnica.md — ✅ (presente)
- docs/email_entrega_template.txt — ✅ (presente)
- deploy_render.sh + render.yaml — ✅ (presente; render.yaml de exemplo gerado)

