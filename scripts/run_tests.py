"""Run test questions against the configured LLM provider.

Reads docs/perguntas_teste.md (format: "N. Question | Expected answer | Chunk")
and calls gerar_resposta_llm from app.py for each question. Produces
docs/test_results.md with model responses and a simple match check.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import List

# Ensure project root is on sys.path when running as a script: `python scripts/run_tests.py`
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import SYSTEM_PROMPT, gerar_resposta_llm


TEST_FILE = Path(__file__).resolve().parents[1] / "docs" / "perguntas_teste.md"
OUTPUT_FILE = Path(__file__).resolve().parents[1] / "docs" / "test_results.md"


def parse_tests(path: Path) -> List[dict]:
    lines = path.read_text(encoding="utf-8").splitlines()
    items = []
    pattern = re.compile(r"^\s*\d+\.\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*$")
    for ln in lines:
        m = pattern.match(ln)
        if m:
            q, expected, chunk = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
            items.append({"question": q, "expected": expected, "chunk": chunk})
    return items


def run():
    tests = parse_tests(TEST_FILE)
    if not tests:
        print("Nenhum teste encontrado em", TEST_FILE)
        return

    out_lines = ["# Resultados dos Testes — VidaBot", ""]
    total = 0
    matched = 0

    for t in tests:
        total += 1
        print(f"[{total}/{len(tests)}] Pergunta: {t['question']}")
        mensagens = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": t["question"]},
        ]
        try:
            resposta = gerar_resposta_llm(mensagens)
        except Exception as e:
            resposta = f"[ERRO] {type(e).__name__}: {e}"

        matched_flag = t["expected"].lower() in resposta.lower()
        if matched_flag:
            matched += 1

        out_lines.append(f"## Pergunta {total}")
        out_lines.append(f"**Pergunta:** {t['question']}")
        out_lines.append(f"**Esperado:** {t['expected']}")
        out_lines.append(f"**Chunk RAG:** {t['chunk']}")
        out_lines.append(f"**Resposta do Modelo:**\n\n{resposta}")
        out_lines.append(f"**Match (substring):** {'SIM' if matched_flag else 'NÃO'}")
        out_lines.append("")

    out_lines.append(f"\n**Resumo:** {matched}/{total} respostas contêm a substring esperada")

    OUTPUT_FILE.write_text("\n".join(out_lines), encoding="utf-8")
    print("Resultados salvos em", OUTPUT_FILE)


if __name__ == '__main__':
    run()
