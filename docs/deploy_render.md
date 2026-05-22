# Guia: Deploy no Render (Web Service) — VidaBot

Este guia descreve, passo a passo, como fazer o deploy do projeto VidaBot no Render como um *Web Service* (gratuito para testes). Use uma conta GitHub vinculada ao Render.

1. Criar conta no Render
   1. Acesse https://render.com e crie uma conta (pode usar GitHub para login).
   2. Confirme seu e-mail e acesse o painel do Render.

2. Preparar o repositório GitHub
   1. Se ainda não estiver no GitHub, crie um repositório público ou privado e faça push do código do projeto.
   2. Garanta que o repositório contenha `app.py`, `requirements.txt` e o diretório `frontend/`.

   Exemplo de comandos locais:

   ```bash
   git init
   git remote add origin git@github.com:SEU_USUARIO/SEU_REPO.git
   git add .
   git commit -m "Initial commit - VidaBot"
   git push -u origin main
   ```

3. Criar um novo Web Service no Render
   1. No painel do Render, clique em "New" → "Web Service".
   2. Conecte o repositório GitHub onde está o projeto e selecione a branch (ex.: `main`).
   3. Configure as opções do serviço:
      - Name: `vidabot` (ou outro nome desejado)
      - Region: escolha a mais próxima (ex.: `Oregon`, `Iowa`, `Frankfurt`)
      - Service type: `Web Service`
      - Environment: `Python`
      - Branch: `main`

4. Build Command e Start Command
   - Build command: leave blank or use the default. Recomendado especificar para garantir reproduzibilidade:

     ```bash
     pip install -r requirements.txt
     ```

   - Start command: use `gunicorn` para rodar o app Flask no ambiente do Render:

     ```bash
     gunicorn app:app --bind 0.0.0.0:$PORT
     ```

   Observação: se `gunicorn` não estiver no `requirements.txt`, adicione-o (`gunicorn>=20`).

5. Variáveis de ambiente / Secrets
   1. No painel do serviço (Settings → Environment), adicione as variáveis necessárias:
      - `ANTHROPIC_API_KEY` (se usar Anthropic)
      - `OPENAI_API_KEY` (se usar OpenAI)
      - `GEMINI_API_KEY` (se usar Gemini / IA Studio)
      - `LLM_PROVIDER` (opcional: `openai`, `anthropic` ou `gemini`)
      - `OPENAI_MODEL`, `ANTHROPIC_MODEL`, `GEMINI_MODEL` (opcionais)

      - Recomendação prática: defina `ANTHROPIC_MODEL=claude-sonnet-4-20250514` quando disponível. O backend tentará
        usar este modelo preferido automaticamente caso `ANTHROPIC_MODEL` não esteja explicitamente definido.
        Se o modelo preferido não estiver acessível, o serviço realizará fallback para uma versão compatível
        (por exemplo `claude-sonnet-4-6`) e anexará uma nota técnica curta à resposta retornada pelo VidaBot
        explicando por que outra versão foi usada.

   2. Nunca comite chaves em arquivos de código. Use o painel do Render para armazenar *secrets*.

6. Health check / Readiness
   1. Render normalmente verifica se o processo está escutando na porta `$PORT`.
   2. Garanta que `app.py` leia `PORT` via Flask (o exemplo padrão do Flask/Render funciona com `gunicorn app:app`).

7. Deploy automático e verificações
   1. Após criar o serviço, o Render fará um build e deploy automático da branch selecionada.
   2. Acompanhe logs no painel (View Logs) para ver erros de build ou runtime.

8. Testar a aplicação
   1. Quando o deployment terminar, acesse a URL fornecida pelo Render (ex.: `https://vidabot.onrender.com`).
   2. Teste o endpoint de chat:

   ```bash
   curl -X POST https://SEU_SERVICE.onrender.com/api/chat \
     -H "Content-Type: application/json" \
     -d '{"mensagem":"Qual a carência do seguro?"}'
   ```

9. Configurações recomendadas / dicas
   - Monitore uso de API e custos no provedor escolhido (OpenAI / Anthropic / IA Studio).
   - Use variáveis de ambiente para alternar `LLM_PROVIDER` sem alterar código.
   - Para produção: configure certificados, limites de CPU/memória e um plano pago conforme necessidade.
   - Ative alertas na conta do provedor para evitar surpresas com gastos.

10. Rollback e atualizações
    - Para atualizar, faça `git push` na branch configurada; o Render iniciará um novo deploy automático.
    - Em caso de falha, use a funcionalidade de Revert ou escolha uma versão estável no painel do Render.

11. Troubleshooting comum
    - Build falhando: verifique `requirements.txt` e a versão do Python selecionada.
    - Variáveis de ambiente não encontradas: confira se foram definidas no Settings do serviço.
    - Erro 502/Timeout: aumente recursos ou revise logs para exceções de inicialização.

12. Referências úteis
    - Render Docs: https://render.com/docs
    - GitHub → Render integration: https://render.com/docs/deploy-from-github

---

Arquivo relacionado: `app.py` (ponto de entrada Flask) — verifique se está em conformidade com `gunicorn app:app`.
