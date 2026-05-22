"""
InsurMinds — VidaBot Backend
Flask API com RAG simulado e integração OpenAI GPT
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from anthropic import Anthropic
from openai import OpenAI, RateLimitError, AuthenticationError
import google.genai as genai
from dotenv import load_dotenv
from typing import cast, Any
import os
import re

load_dotenv()

app = Flask(__name__, static_folder="frontend")
CORS(app)

# ============================================================
# CARREGAR BASE RAG DO ARQUIVO
# ============================================================
def carregar_faq(caminho="faq.txt"):
    chunks = []
    if not os.path.exists(caminho):
        return chunks
    with open(caminho, "r", encoding="utf-8") as f:
        conteudo = f.read()
    blocos = conteudo.strip().split("\n\n---")
    for bloco in blocos:
        bloco = bloco.strip().lstrip("- ")
        if not bloco:
            continue
        linhas = bloco.strip().split("\n")
        source = "Base de Conhecimento"
        texto = bloco
        for linha in linhas:
            if linha.startswith("FONTE:"):
                source = linha.replace("FONTE:", "").strip()
            elif linha.startswith("---"):
                source = linha.strip("- \n").replace("FONTE:", "").strip()
        keywords = re.findall(r'\b\w{4,}\b', texto.lower())
        chunks.append({
            "source": source,
            "texto": texto[:500],
            "keywords": list(set(keywords))
        })
    return chunks

BASE_RAG = carregar_faq()

# ============================================================
# BUSCA RAG
# ============================================================
def buscar_rag(pergunta: str, top_k: int = 3):
    q = pergunta.lower()
    scored = []
    for chunk in BASE_RAG:
        score = 0
        for kw in chunk["keywords"]:
            if kw in q:
                score += 10
        palavras = [p for p in q.split() if len(p) > 3]
        for p in palavras:
            if p in chunk["texto"].lower():
                score += 3
        if score > 0:
            scored.append({**chunk, "score": score})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]

# ============================================================
# SYSTEM PROMPT
# ============================================================
SYSTEM_PROMPT = """Você é o VidaBot, assistente virtual especializado em Seguros de Vida da InsurMinds.

IDENTIDADE:
- Nome: VidaBot
- Empresa: InsurMinds Seguros
- Especialidade: Seguros de Vida (individual, em grupo, VGBL, PGBL)
- Tom: empático, claro, profissional, acessível

SUAS RESPONSABILIDADES:
- Responder dúvidas sobre coberturas, carências, sinistros e documentos
- Orientar o segurado sobre próximos passos
- Explicar termos técnicos de forma simples
- Indicar canais de atendimento humano quando necessário
- Basear respostas APENAS no contexto fornecido abaixo + conhecimento regulatório

REGULAÇÃO (SUSEP):
- Prazo máximo de pagamento de sinistro: 30 dias após documentação completa
- Carência morte natural: 180 dias
- Carência suicídio: 2 anos
- Direito de arrependimento: 7 dias após contratação

LIMITES:
- NÃO confirme valores de indenização específicos sem dados da apólice
- NÃO tome decisão de aceitação ou recusa de sinistro
- Para casos jurídicos ou complexos, direcione para atendimento humano

FORMATO DAS RESPOSTAS:
- Máximo 3 parágrafos
- Use listas quando houver múltiplos itens
- Seja direto e objetivo
- Finalize sempre perguntando se o usuário precisa de mais informações"""


def gerar_resposta_llm(mensagens: list[dict[str, Any]], provider_override: str | None = None) -> str:
    provider_env = os.environ.get("LLM_PROVIDER")
    openai_api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    gemini_api_key = os.environ.get("GEMINI_API_KEY", "").strip()

    tem_openai = bool(openai_api_key) and not openai_api_key.startswith("sk-ant-")
    tem_anthropic = bool(anthropic_api_key)
    tem_gemini = bool(gemini_api_key)

    if provider_override:
        provider = provider_override.strip().lower()
    elif provider_env:
        provider = provider_env.strip().lower()
    elif tem_openai:
        provider = "openai"
    elif tem_anthropic:
        provider = "anthropic"
    elif tem_gemini:
        provider = "gemini"
    else:
        provider = "openai"

    if provider == "gemini":
        if not gemini_api_key:
            raise ValueError("GEMINI_API_KEY não configurada")

        gemini_model = os.environ.get("GEMINI_MODEL", "models/gemini-2.5-flash-lite")
        client = genai.Client(api_key=gemini_api_key)
        
        system_message = next((m["content"] for m in mensagens if m.get("role") == "system"), SYSTEM_PROMPT)
        mensagens_gemini = []
        for m in mensagens:
            role = m.get("role")
            content = m.get("content")
            if role not in ("user", "assistant") or not content:
                continue

            gemini_role = "model" if role == "assistant" else "user"
            mensagens_gemini.append(
                genai.types.Content(
                    role=gemini_role,
                    parts=[genai.types.Part(text=str(content))],
                )
            )
        
        resposta = client.models.generate_content(
            model=gemini_model,
            contents=mensagens_gemini,
            config=genai.types.GenerateContentConfig(
                system_instruction=system_message,
                max_output_tokens=1000,
            )
        )
        return resposta.text if resposta.text else "Desculpe, ocorreu um erro."

    if provider == "anthropic":
        anthropic_api_key = anthropic_api_key or openai_api_key
        if not anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY não configurada")

            # Preferência por uma versão específica do Claude quando disponível.
            preferred_model = "claude-sonnet-4-20250514"
            anthropic_model = os.environ.get("ANTHROPIC_MODEL")
            note = None

            system_message = next((m["content"] for m in mensagens if m.get("role") == "system"), SYSTEM_PROMPT)
            mensagens_anthropic = [
                {"role": m["role"], "content": m["content"]}
                for m in mensagens
                if m.get("role") in ("user", "assistant") and m.get("content")
            ]

            client = Anthropic(api_key=anthropic_api_key)

            # Se não foi especificado via env, tentamos detectar se o modelo preferido está disponível.
            if not anthropic_model:
                try:
                    models_list = None
                    if hasattr(client, "models") and hasattr(client.models, "list"):
                        models_list = client.models.list()

                    if models_list:
                        names = []
                        for m in models_list:
                            if isinstance(m, str):
                                names.append(m)
                            elif isinstance(m, dict):
                                names.append(m.get("id") or m.get("name"))
                            else:
                                names.append(getattr(m, "id", str(m)))

                        if preferred_model in names:
                            anthropic_model = preferred_model
                        else:
                            anthropic_model = "claude-sonnet-4-6"
                            note = f"modelo preferido {preferred_model} não listado; usando {anthropic_model}."
                    else:
                        # Não foi possível listar modelos: optar pelo preferido e confiar que a API aceita.
                        anthropic_model = preferred_model
                except Exception as e:
                    anthropic_model = "claude-sonnet-4-6"
                    note = f"falha ao verificar modelos Anthropic ({type(e).__name__}): usando {anthropic_model}."

            # Se env especificou outro modelo, usaremos o que foi informado.
            anthropic_model = anthropic_model or os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6")

            resposta = client.messages.create(
                model=anthropic_model,
                max_tokens=1000,
                system=system_message,
                messages=cast(Any, mensagens_anthropic),
            )

            texto = "".join(
                bloco.text for bloco in resposta.content if getattr(bloco, "type", None) == "text"
            )

            if not texto:
                return "Desculpe, ocorreu um erro."

            if note:
                texto = f"{texto}\n\n[Nota técnica: {note}]"

            return texto

    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY não configurada")

    if openai_api_key.startswith("sk-ant-"):
        raise ValueError("OPENAI_API_KEY parece ser uma chave da Anthropic. Use ANTHROPIC_API_KEY ou defina LLM_PROVIDER=anthropic.")

    openai_model = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
    client = OpenAI(api_key=openai_api_key)
    resposta = client.chat.completions.create(
        model=openai_model,
        max_tokens=1000,
        messages=cast(Any, mensagens),
    )
    return resposta.choices[0].message.content or "Desculpe, ocorreu um erro."

# ============================================================
# ROTAS
# ============================================================

@app.route("/")
def index():
    return send_from_directory("frontend", "index.html")

@app.route("/api/chat", methods=["GET", "POST"])
def chat():
    # Suporte informativo via GET para evitar 405 ao abrir a URL no navegador.
    if request.method == "GET":
        return jsonify({
            "info": "Use POST /api/chat com JSON: {'mensagem':'sua pergunta'}. Exemplo: curl -X POST http://localhost:5000/api/chat -H 'Content-Type: application/json' -d '{\"mensagem\":\"Qual a carência do seguro?\"}'"
        }), 200

    data = request.get_json(silent=True) or {}
    mensagem = data.get("mensagem", "")
    historico = data.get("historico", [])

    if not mensagem:
        return jsonify({"erro": "Mensagem vazia"}), 400

    # Busca RAG
    chunks = buscar_rag(mensagem)
    contexto = "\n\n".join(
        [f"[{c['source']}]: {c['texto']}" for c in chunks]
    ) if chunks else "Sem contexto específico. Responda com base em conhecimento geral de seguros de vida."

    system_com_rag = f"{SYSTEM_PROMPT}\n\n===== CONTEXTO RAG =====\n{contexto}\n========================"

    # Prepara mensagens para OpenAI (inclui system no array de mensagens)
    mensagens_openai: list[dict[str, Any]] = [{"role": "system", "content": system_com_rag}]
    
    # Adiciona histórico
    for m in historico:
        if m.get("role") in ("user", "assistant") and m.get("content"):
            mensagens_openai.append({"role": m["role"], "content": m["content"]})
    
    # Adiciona mensagem atual
    mensagens_openai.append({"role": "user", "content": mensagem})

    # Chama o provedor configurado
    try:
        provider_req = data.get("provider")
        texto_resposta = gerar_resposta_llm(mensagens_openai, provider_override=provider_req)
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400
    except Exception as erro:
        return jsonify({"erro": f"Falha ao consultar o modelo: {type(erro).__name__}: {erro}"}), 502

    return jsonify({
        "resposta": texto_resposta,
        "chunks": [
            {"source": c["source"], "texto": c["texto"][:200], "score": c["score"]}
            for c in chunks
        ]
    })


@app.route("/api/rag", methods=["GET"])
def info_rag():
    return jsonify({
        "total_chunks": len(BASE_RAG),
        "fontes": list(set(c["source"] for c in BASE_RAG))
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
