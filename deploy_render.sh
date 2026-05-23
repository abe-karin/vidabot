#!/usr/bin/env bash
set -euo pipefail

# deploy_render.sh — script auxiliar para preparar o repositório e gerar
# um arquivo `render.yaml` de exemplo para uso no Render (Web Service).
# Uso: bash deploy_render.sh

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
RENDER_YAML="$REPO_ROOT/render.yaml"

echo "[deploy_render] Iniciando preparação para deploy no Render..."

check_command() {
  command -v "$1" >/dev/null 2>&1 || { echo "Erro: comando '$1' não encontrado. Instale-o e tente novamente."; exit 1; }
}

check_command git
check_command python

echo "Verificando branch atual..."
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD || echo "")
echo "Branch atual: ${CURRENT_BRANCH:-(desconhecida)}"

if [ -z "${CURRENT_BRANCH}" ]; then
  echo "Aviso: não foi possível detectar a branch git. Certifique-se de estar em um repositório git e em uma branch (ex.: main)."
fi

echo "Verificando requirements.txt..."
if [ ! -f "$REPO_ROOT/requirements.txt" ]; then
  echo "Atenção: requirements.txt não encontrado. Crie um antes do deploy ou atualize este script." 
else
  if ! grep -q "gunicorn" "$REPO_ROOT/requirements.txt"; then
    echo "Recomendação: adicionar 'gunicorn' ao requirements.txt para execução em produção (Render)."
    echo "  echo 'gunicorn>=20' >> requirements.txt    # (opcional)" 
  fi
fi

echo "Gerando render.yaml de exemplo em: $RENDER_YAML"
cat > "$RENDER_YAML" << 'YAML'
services:
  - type: web
    name: vidabot
    env: python
    branch: main
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app --bind 0.0.0.0:$PORT
    autoDeploy: true
    envVars:
      - key: LLM_PROVIDER
        value: openai
      - key: OPENAI_MODEL
        value: gpt-3.5-turbo
      - key: ANTHROPIC_MODEL
        value: claude-sonnet-4-20250514
      - key: GEMINI_API_KEY
        value: ""
      - key: GEMINI_MODEL
        value: models/gemini-2.5-flash-lite
YAML

echo "Arquivo render.yaml criado. Conteúdo (resumo):"
sed -n '1,120p' "$RENDER_YAML"

echo
echo "Próximos passos (manuais / verifique antes de executar):"
echo "1) Verifique que seu repositório está com todos os arquivos prontos: app.py, requirements.txt, frontend/, faq.txt, docs/."
echo "2) Faça commit das mudanças locais e confirme remote:"
echo "   git add ."
echo "   git commit -m 'Prepare render.yaml for deploy'"
echo "   git remote -v  # confirme remote origin apontando para seu repositório GitHub"
echo "3) Push para a branch configurada (ex.: main):"
echo "   git push origin \$(git rev-parse --abbrev-ref HEAD)"
echo "4) No painel do Render: New -> Web Service -> Connect Repository -> selecione a branch 'main' e, se desejar, carregue este render.yaml ou deixe o Render detectar o arquivo."
echo "5) No painel do serviço, configure as Environment Variables / Secrets: OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY, LLM_PROVIDER, etc."
echo
echo "Observações de segurança: NÃO comite chaves de API. Use o painel do Render para adicionar secrets."

echo "Concluído. "

exit 0
