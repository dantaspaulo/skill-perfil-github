#!/usr/bin/env python3
"""Gera as imagens do README deste repositório com o próprio gerador da skill.

Uso: python3 docs/gerar_docs.py
"""
import importlib.util
import json
import re
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "docs" / "assets"
spec = importlib.util.spec_from_file_location("perfil", RAIZ / "perfil-github" / "scripts" / "perfil.py")
perfil = importlib.util.module_from_spec(spec)
spec.loader.exec_module(perfil)

DOCS = {
    "login": "skill-perfil-github",
    "nome": "perfil-github",
    "tema": "champagne",
    "numeros": [
        {"valor": "6", "rotulo": ["blocos animados", "prontos"], "fonte": "o gerador"},
        {"valor": "4", "rotulo": ["temas, ou o seu", "a partir do site"], "fonte": "o gerador"},
        {"valor": "2", "rotulo": ["versões de cada bloco:", "computador e celular"], "fonte": "o gerador"},
        {"valor": "0", "rotulo": ["dependências além", "do Python"], "fonte": "o gerador"},
    ],
    "metodo": {"passos": [
        {"nome": "Descobrir", "sub": ["lê perfil, site", "e LinkedIn"]},
        {"nome": "Perguntar", "sub": ["só o que falta,", "com rascunho"]},
        {"nome": "Montar", "sub": ["cartões e README", "a partir de um JSON"]},
        {"nome": "Conferir", "sub": ["trava de nome,", "texto que cabe"]},
        {"nome": "Publicar", "sub": ["depois da prévia", "e do seu ok"]},
    ]},
    "principios": {"itens": [
        {"icone": "🔒", "linhas": ["Nome do cliente", "protegido"]},
        {"icone": "📏", "linhas": ["Número com", "fonte e data"]},
        {"icone": "✂️", "linhas": ["Texto que", "cabe no cartão"]},
        {"icone": "👀", "linhas": ["Prévia antes", "de publicar"]},
        {"icone": "📱", "linhas": ["Celular", "também"]},
    ]},
}


def gerar_blocos():
    with tempfile.TemporaryDirectory() as tmp:
        perfil.gerar_svgs(DOCS, Path(tmp))
        for svg in Path(tmp).glob("*.svg"):
            (SAIDA / svg.name).write_text(svg.read_text(encoding="utf-8"), encoding="utf-8")


def galeria_de_temas():
    """Um cartão de case por tema, todos no mesmo SVG (classes e degradês com escopo por tema)."""
    exemplo = json.loads((RAIZ / "perfil-github" / "references" / "perfil.exemplo.json").read_text(encoding="utf-8"))
    case = exemplo["cases"][0]
    pecas, estilos, defs = [], [], []
    for i, nome in enumerate(perfil.TEMAS):
        c = perfil.tema({"tema": nome})
        k = dict(case, selo=nome.upper())
        w, h, corpo = perfil.peca_case(c, f"t{i}", 0.15 * i, k)
        corpo = corpo.replace('url(#g)', f'url(#g{i})').replace('url(#sh)', f'url(#sh{i})')
        css = perfil.css_base(c)
        css = re.sub(r"(?m)^\.([a-z]{2,5})\{", lambda m: f".t{i} .{m.group(1)}{{", css)
        estilos.append(css)
        d = perfil.defs(c).replace('id="g"', f'id="g{i}"').replace('id="sh"', f'id="sh{i}"')
        defs.append(d)
        pecas.append((w, h, f'<g class="t{i}">{corpo}</g>'))
    for arquivo, col, gap in (("temas.svg", 2, 20), ("temas-celular.svg", 1, 14)):
        w, h, corpo = perfil.grade(pecas, col, gap)
        titulo = "Os quatro temas: " + ", ".join(perfil.TEMAS)
        (SAIDA / arquivo).write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{titulo}">\n'
            f"<title>{titulo}</title>\n<style>{''.join(estilos)}</style>\n{''.join(defs)}\n{corpo}\n</svg>\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    SAIDA.mkdir(parents=True, exist_ok=True)
    for velho in SAIDA.glob("*.svg"):
        velho.unlink()
    gerar_blocos()
    galeria_de_temas()
    print("ok:", ", ".join(sorted(p.name for p in SAIDA.glob("*.svg"))))
