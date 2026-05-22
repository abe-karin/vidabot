# Análise Técnica — Por que escolher RAG em vez de Fine‑Tuning

Para o projeto VidaBot, adotamos uma arquitetura RAG (Retrieval‑Augmented Generation) em vez de treinar ou fine‑tunear um modelo central. A decisão apoia‑se em critérios técnicos, regulatórios e econômicos relevantes para o setor de seguros.

Primeiro, RAG oferece atualizabilidade e rastreabilidade. Em um domínio regulado como seguros de vida (CNSP 294/2013, normas SUSEP), textos normativos, cláusulas e procedimentos mudam com frequência. Com RAG, a base de conhecimento (`faq.txt`) pode ser atualizada imediatamente sem retrain do modelo, preservando histórico de versões e permitindo auditoria das fontes usadas em cada resposta — requisito crítico em avaliações de conformidade.

Segundo, custo e velocidade de implementação. Fine‑tuning exige dataset de qualidade, pipeline de curadoria, custo computacional (treinamento) e tempo até a entrega. Para uma solução acadêmica e de prova de conceito operacional, RAG reduz custo inicial e permite deploy rápido com qualidade controlável por prompt engineering e seleção de chunks. Isso é especialmente relevante quando se compara planos e tarifas de provedores LLM: manter uma base de recuperação é mais barato que múltiplos ciclos de treino e revalidação.

Terceiro, manutenibilidade e granularidade de controle. RAG separa a camada de conhecimento (KB) do gerador, favorecendo intervenções localizadas: corrigir um trecho do `faq.txt` corrige comportamento pontual sem risco de degradar capacidades gerais do gerador. Fine‑tuning, por outro lado, altera pesos do modelo e pode gerar efeitos colaterais (catástrofes de performance em outras capacidades), exigindo testes extensivos.

Quarto, rastreabilidade e explicabilidade — requisitos da banca e do regulador. RAG permite retornar os trechos (chunks) que embasaram a resposta, facilitando justificativas e evidências. Em cenários de sinistro ou disputa, essa trilha de auditoria é valiosa; modelos fine‑tuned não oferecem esse vínculo explícito entre output e fonte sem mecanismos adicionais.

Por fim, o triângulo de esforço (Prompt Engineering → RAG → Fine‑Tuning → Trained Model): RAG ocupa uma posição prática e eficiente entre prompt engineering e fine‑tuning. Para a maioria dos casos de uso de atendimento ao segurado, a combinação de prompts bem elaborados + RAG entrega precisão e atualizabilidade suficiente. O fine‑tuning permanece uma opção para cenários com grande escala, alta necessidade de personalização e orçamento elevado, mas exige governança, avaliação de vieses e ciclo de retraining que fogem ao escopo e restrição temporal deste desafio.

Conclusão: para o VidaBot, RAG equilibra custo, compliance e velocidade de entrega, oferece rastreabilidade das fontes e facilita manutenção operacional — tornando‑o a opção mais adequada para um chatbot regulado de suporte a segurados.
