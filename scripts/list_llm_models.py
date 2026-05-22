"""List LLM models available from the configured providers.

This script loads environment variables from .env and tries to list
models from OpenAI, Anthropic, and Google Gemini when credentials are present.
"""

from __future__ import annotations

import os
from typing import Iterable, Any

from anthropic import Anthropic
from dotenv import load_dotenv
from openai import OpenAI
import google.genai as genai


def _print_section(title: str) -> None:
    print(f"\n=== {title} ===")


def _field(item: Any, name: str, default: Any = None) -> Any:
    if isinstance(item, dict):
        return item.get(name, default)
    return getattr(item, name, default)


def _format_items(items: Iterable[Any]) -> None:
    any_item = False
    for item in items:
        any_item = True
        model_id = _field(item, "id") or _field(item, "name") or "<unknown>"
        display_name = _field(item, "display_name") or _field(item, "name") or ""
        extra = []
        if display_name and display_name != model_id:
            extra.append(f"display_name={display_name}")
        owned_by = _field(item, "owned_by")
        if owned_by:
            extra.append(f"owned_by={owned_by}")
        item_type = _field(item, "type")
        if item_type:
            extra.append(f"type={item_type}")
        suffix = f" ({', '.join(extra)})" if extra else ""
        print(f"- {model_id}{suffix}")

    if not any_item:
        print("- Nenhum modelo retornado pela API.")


def list_openai_models() -> None:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        print("- OPENAI_API_KEY ausente; pulando OpenAI.")
        return
    if api_key.startswith("sk-ant-"):
        print("- OPENAI_API_KEY parece ser uma chave da Anthropic; pulando OpenAI.")
        return

    _print_section("OpenAI")
    client = OpenAI(api_key=api_key)
    response = client.models.list()
    _format_items(getattr(response, "data", []))


def list_anthropic_models() -> None:
    api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        print("- ANTHROPIC_API_KEY ausente; pulando Anthropic.")
        return

    _print_section("Anthropic")
    client = Anthropic(api_key=api_key)
    response = client.models.list()
    _format_items(getattr(response, "data", []))


def list_gemini_models() -> None:
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        print("- GEMINI_API_KEY ausente; pulando Google Gemini.")
        return

    _print_section("Google Gemini")
    client = genai.Client(api_key=api_key)
    response = client.models.list()
    models = []
    for model in response:
        models.append({
            "name": model.name,
            "display_name": model.display_name or "",
        })
    _format_items(models)


def main() -> None:
    load_dotenv()

    print("Modelos de LLM detectados no ambiente do projeto")
    print(f"LLM_PROVIDER={os.getenv('LLM_PROVIDER', 'openai')}")
    print(f"OPENAI_API_KEY={'configurada' if os.getenv('OPENAI_API_KEY') else 'não configurada'}")
    print(f"OPENAI_MODEL={os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')}")
    print(f"ANTHROPIC_API_KEY={'configurada' if os.getenv('ANTHROPIC_API_KEY') else 'não configurada'}")
    print(f"ANTHROPIC_MODEL={os.getenv('ANTHROPIC_MODEL', 'claude-sonnet-4-6')}")
    print(f"GEMINI_API_KEY={'configurada' if os.getenv('GEMINI_API_KEY') else 'não configurada'}")
    print(f"GEMINI_MODEL={os.getenv('GEMINI_MODEL', 'gemini-2.0-flash')}")

    try:
        list_openai_models()
    except Exception as exc:
        print(f"OpenAI: erro ao listar modelos -> {type(exc).__name__}: {exc}")

    try:
        list_anthropic_models()
    except Exception as exc:
        print(f"Anthropic: erro ao listar modelos -> {type(exc).__name__}: {exc}")

    try:
        list_gemini_models()
    except Exception as exc:
        print(f"Google Gemini: erro ao listar modelos -> {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main()
