#!/usr/bin/env python3
"""Monta o README de perfil do GitHub com cartões animados em SVG.

Só biblioteca padrão. O `gh` (GitHub CLI) é opcional: usado no diagnóstico
e na prévia renderizada.

  python3 perfil.py diagnostico --login USUARIO
  python3 perfil.py montar   --config perfil.json --repo ./USUARIO
  python3 perfil.py conferir --config perfil.json --repo ./USUARIO [--nao-citar nao-citar.txt]
  python3 perfil.py previa   --config perfil.json --repo ./USUARIO

`montar` escreve README.md e assets/*.svg dentro do clone do repositório
USUARIO/USUARIO. O perfil.json e a lista de nomes proibidos ficam FORA do
repositório: o que é público é só o que sai do montar.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote
from xml.sax.saxutils import escape

# ── temas ────────────────────────────────────────────────────────────────

TEMAS = {
    "champagne": dict(fundo="#151310", caixa="#1F1C18", borda="#2A2723", borda2="#3A352E", tinta="#F1ECE3",
                      corpo="#CFC6B6", suave="#A39A8A", apagado="#8F8778", destaque="#D6BD8F", claro="#E2CDA4",
                      escuro="#8C7148", aceso="#211C15", medio="#B08D57", tinta_escura="#14110C", brilho="#F1E3C4"),
    "esmeralda": dict(fundo="#0F1512", caixa="#16201B", borda="#22302A", borda2="#2E4038", tinta="#EAF4EE",
                      corpo="#C3D6CB", suave="#93A99D", apagado="#7E9488", destaque="#3DDC97", claro="#7FF0BE",
                      escuro="#1E8C5E", aceso="#13261D", medio="#1FA36B", tinta_escura="#06140D", brilho="#D9FBEA"),
    "oceano": dict(fundo="#0F1420", caixa="#161D2C", borda="#232D40", borda2="#2F3B52", tinta="#EAF0FA",
                   corpo="#C4CFE0", suave="#95A3BA", apagado="#7F8CA3", destaque="#6CB6FF", claro="#A5D3FF",
                   escuro="#2F6FB8", aceso="#142238", medio="#3D8BDA", tinta_escura="#07111F", brilho="#DCEEFF"),
    "grafite": dict(fundo="#141414", caixa="#1C1C1C", borda="#2A2A2A", borda2="#3A3A3A", tinta="#F2F2F2",
                    corpo="#CFCFCF", suave="#A0A0A0", apagado="#8A8A8A", destaque="#E6E6E6", claro="#FFFFFF",
                    escuro="#8A8A8A", aceso="#232323", medio="#7A7A7A", tinta_escura="#111111", brilho="#FFFFFF"),
}

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
SERIF = "Georgia,'Times New Roman',serif"
EMOJI = "'Apple Color Emoji','Segoe UI Emoji','Noto Color Emoji',sans-serif"

TITULOS = {
    "cases": "💼 Cases",
    "metodo": "🧠 Como eu trabalho",
    "abertos": "📦 Aberto no GitHub",
    "stack": "🛠️ Stack",
    "cta": "📫 Vamos conversar",
    "detalhes": "📖 Problema, solução e resultado de cada case",
}


def tema(cfg):
    t = cfg.get("tema", "champagne")
    if isinstance(t, str):
        return dict(TEMAS[t])
    base = dict(TEMAS[t.get("base", "champagne")])
    base.update({k: v for k, v in t.items() if k != "base"})
    return base


# ── medida de texto (estimativa; SVG não quebra linha sozinho) ───────────

def largura(texto, tamanho, estilo="sans", espaco=0.0):
    fator = {"sans": 0.55, "negrito": 0.6, "serif": 0.52, "caixa-alta": 0.68}[estilo]
    n = 0.0
    for ch in texto:
        if ord(ch) > 0x2600:
            n += 1.25
        elif ch in "iIl.,:;'!|j ":
            n += 0.55
        elif ch in "mwMW":
            n += 1.35
        else:
            n += 1.0
    return n * tamanho * fator + len(texto) * espaco


# ── SVG: base comum ──────────────────────────────────────────────────────

def css_base(c):
    return f"""
.up{{opacity:0;animation:up .9s cubic-bezier(.2,.7,.2,1) forwards}}
@keyframes up{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}
.run{{stroke-dasharray:9 91;animation:run 7s linear infinite}}
@keyframes run{{to{{stroke-dashoffset:-100}}}}
.shine{{animation:shine 8s ease-in-out infinite}}
@keyframes shine{{0%,72%{{transform:translateX(-420px)}}100%{{transform:translateX(1300px)}}}}
.ln{{stroke-dasharray:100;stroke-dashoffset:100;animation:ln 1.4s ease forwards}}
@keyframes ln{{to{{stroke-dashoffset:0}}}}
.emo{{font:22px {EMOJI}}}
.ct{{font:700 21px {SANS};fill:{c['tinta']}}}
.cs{{font:500 13px {SANS};fill:{c['suave']}}}
.cp{{font:700 10.5px {SANS};letter-spacing:1.3px;fill:{c['destaque']}}}
.cn{{font:400 50px {SERIF};fill:url(#g)}}
.cl{{font:500 14px {SANS};fill:{c['corpo']}}}
.cf{{font:500 12.5px {SANS};fill:{c['apagado']}}}
.nn{{font:400 46px {SERIF};fill:url(#g)}}
.nl{{font:500 13.5px {SANS};fill:{c['corpo']}}}
.mk{{font:400 20px {SERIF};fill:{c['destaque']}}}
.mt{{font:700 16px {SANS};fill:{c['tinta']}}}
.ms{{font:500 12.5px {SANS};fill:{c['suave']}}}
.gt{{font:700 13.5px {SANS};fill:{c['tinta']}}}
.pt{{font:700 14.5px {SANS};fill:{c['tinta']}}}
.ps{{font:500 12.5px {SANS};fill:{c['suave']}}}
.at{{font:700 16px {SANS};fill:{c['tinta']}}}
.as{{font:500 12px {SANS};fill:{c['suave']}}}
.ap{{font:700 9.5px {SANS};letter-spacing:1.2px;fill:{c['destaque']}}}
.al{{font:500 12.5px {SANS};fill:{c['corpo']}}}
"""


def defs(c):
    return f"""<defs>
<linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c['claro']}"/><stop offset="1" stop-color="{c['escuro']}"/></linearGradient>
<linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="{c['brilho']}" stop-opacity="0"/><stop offset=".5" stop-color="{c['brilho']}" stop-opacity=".09"/><stop offset="1" stop-color="{c['brilho']}" stop-opacity="0"/></linearGradient>
</defs>"""


def attr(texto):
    """Escapa texto para dentro de atributo (aspas incluídas)."""
    return escape(texto, {'"': "&quot;"})


def atraso(s):
    return f'style="animation-delay:{s:.2f}s"'


def moldura(c, pfx, w, h, rx=16):
    return f"""<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{rx}" fill="{c['fundo']}" stroke="{c['borda']}"/>
<clipPath id="c{pfx}"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{rx}"/></clipPath>
<g clip-path="url(#c{pfx})"><g class="shine"><rect x="0" y="-20" width="150" height="{h+40}" fill="url(#sh)" transform="skewX(-18)"/></g></g>
<rect class="run" x="1" y="1" width="{w-2}" height="{h-2}" rx="{rx}" fill="none" stroke="url(#g)" stroke-width="1.6" pathLength="100"/>"""


def selo(c, x_dir, y, texto, cls="cp", passo=7.4, altura=22):
    larg = len(texto) * passo + 22
    return (
        f'<rect x="{x_dir - larg:.1f}" y="{y}" width="{larg:.1f}" height="{altura}" rx="{altura / 2}" fill="{c["caixa"]}" stroke="{c["borda2"]}"/>'
        f'<text class="{cls}" x="{x_dir - larg / 2:.1f}" y="{y + altura / 2 + 4}" text-anchor="middle">{escape(texto)}</text>'
    )


def linhas(cls, x, y0, passo, textos, anchor="start"):
    return "".join(f'<text class="{cls}" x="{x}" y="{y0 + i * passo}" text-anchor="{anchor}">{escape(t)}</text>' for i, t in enumerate(textos))


def salvar(destino, c, w, h, titulo, corpo, css_extra=""):
    destino.write_text(
        f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{attr(titulo)}">
<title>{escape(titulo)}</title>
<style>{css_base(c)}{css_extra}</style>
{defs(c)}
{corpo}
</svg>
""",
        encoding="utf-8",
    )


def grade(pecas, colunas, gap):
    """Peças (w, h, svg) em grade; a última linha incompleta fica centralizada."""
    pw, ph = pecas[0][0], pecas[0][1]
    n = len(pecas)
    nlin = -(-n // colunas)
    w = colunas * pw + (colunas - 1) * gap
    h = nlin * ph + (nlin - 1) * gap
    corpo = []
    for i, p in enumerate(pecas):
        lin, col = divmod(i, colunas)
        na_linha = colunas if lin < nlin - 1 else n - lin * colunas
        sobra = (colunas - na_linha) * (pw + gap) / 2
        corpo.append(f'<g transform="translate({sobra + col * (pw + gap):.1f},{lin * (ph + gap)})">{p[2]}</g>')
    return w, h, "".join(corpo)


# ── peças ────────────────────────────────────────────────────────────────

def peca_case(c, pfx, d, k):
    w, h = 420, 236
    return w, h, f"""{moldura(c, pfx, w, h)}
<rect x="22" y="22" width="40" height="40" rx="11" fill="{c['caixa']}" stroke="{c['borda']}"/>
<text class="emo" x="42" y="50" text-anchor="middle">{k['icone']}</text>
<text class="ct" x="76" y="40">{escape(k['nome'])}</text>
<text class="cs" x="76" y="59">{escape(k.get('sub', ''))}</text>
{selo(c, w - 22, 22, k['selo']) if k.get('selo') else ''}
<g class="up" {atraso(d + .1)}><text class="cn" x="22" y="138">{escape(k['numero'])}</text></g>
<g class="up" {atraso(d + .35)}>{linhas("cl", 24, 166, 19, k['rotulo'])}</g>
<line class="ln" x1="24" y1="{h - 40}" x2="{w - 24}" y2="{h - 40}" stroke="{c['borda']}" pathLength="100" {atraso(d + .5)}/>
<g class="up" {atraso(d + .6)}><text class="cf" x="24" y="{h - 17}">{escape(k.get('rodape', ''))}</text></g>"""


def peca_aberto(c, pfx, d, a):
    w, h = 280, 168
    return w, h, f"""{moldura(c, pfx, w, h, 14)}
<rect x="18" y="18" width="34" height="34" rx="9" fill="{c['caixa']}" stroke="{c['borda']}"/>
<text class="emo" x="35" y="43" text-anchor="middle" style="font-size:18px">{a['icone']}</text>
{selo(c, w - 18, 24, a['selo'], "ap", 6.9, 20) if a.get('selo') else ''}
<g class="up" {atraso(d)}><text class="at" x="18" y="82">{escape(a['nome'])}</text><text class="as" x="18" y="100">{escape(a.get('dono', ''))}</text></g>
<g class="up" {atraso(d + .2)}>{linhas("al", 18, 128, 18, a['linhas'])}</g>"""


def gerar_svgs(cfg, pasta):
    c = tema(cfg)
    pasta.mkdir(parents=True, exist_ok=True)
    for velho in pasta.glob("*.svg"):
        velho.unlink()
    feitos = []

    if cfg.get("papeis"):
        P = cfg["papeis"]
        tit = ", ".join(f"{p['titulo']} ({p.get('sub', '')})" for p in P)

        def cel(d, x, y, w, h, p):
            cx = x + w / 2
            return (f'<g class="up" {atraso(d)}><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{c["fundo"]}" stroke="{c["borda"]}" stroke-width="1.2"/>'
                    f'<text class="emo" x="{cx}" y="{y + 36}" text-anchor="middle" style="font-size:20px">{p["icone"]}</text>'
                    f'<text class="pt" x="{cx}" y="{y + 64}" text-anchor="middle">{escape(p["titulo"])}</text>'
                    f'<text class="ps" x="{cx}" y="{y + 83}" text-anchor="middle">{escape(p.get("sub", ""))}</text></g>')
        n, gap, ch = len(P), 16, 100
        cw = (860 - (n - 1) * gap) / n
        salvar(pasta / "papeis.svg", c, 862, ch + 2, tit, "".join(cel(.1 + i * .12, 1 + i * (cw + gap), 1, cw, ch, p) for i, p in enumerate(P)))
        cw, col = 202, 2
        nlin = -(-n // col)
        corpo = []
        for i, p in enumerate(P):
            lin, k = divmod(i, col)
            sobra = (cw + gap) / 2 if (lin == nlin - 1 and n % col) else 0
            corpo.append(cel(.1 + i * .12, 1 + sobra + k * (cw + gap), 1 + lin * (ch + gap), cw, ch, p))
        salvar(pasta / "papeis-celular.svg", c, col * cw + gap + 2, nlin * ch + (nlin - 1) * gap + 2, tit, "".join(corpo))
        feitos.append("papeis")

    if cfg.get("numeros"):
        N = cfg["numeros"]
        tit = ", ".join(f"{x['valor']} {' '.join(x['rotulo'])}" for x in N)

        def cel(d, cx, x):
            return (f'<g class="up" {atraso(d)}><text class="nn" x="{cx}" y="0" text-anchor="middle">{escape(x["valor"])}</text></g>'
                    f'<g class="up" {atraso(d + .2)}>{linhas("nl", cx, 30, 19, x["rotulo"], "middle")}</g>')
        n = len(N)
        w, h, colw = 840, 156, 840 / n
        corpo = [moldura(c, "n", w, h, 18)]
        for i, x in enumerate(N):
            cx = colw / 2 + i * colw
            corpo.append(f'<g transform="translate(0,74)">{cel(.15 + i * .18, cx, x)}</g>')
            if i:
                corpo.append(f'<line class="ln" x1="{i * colw:.1f}" y1="34" x2="{i * colw:.1f}" y2="{h - 34}" stroke="{c["borda"]}" pathLength="100" {atraso(.15 + i * .18)}/>')
        salvar(pasta / "numeros.svg", c, w, h, tit, "\n".join(corpo))
        nlin = -(-n // 2)
        w, h = 420, 20 + nlin * 125
        corpo = [moldura(c, "m", w, h, 18)]
        for i, x in enumerate(N):
            lin, k = divmod(i, 2)
            cx = 210 if (lin == nlin - 1 and n % 2) else 105 + k * 210
            corpo.append(f'<g transform="translate(0,{72 + lin * 125})">{cel(.15 + i * .15, cx, x)}</g>')
        for lin in range(1, nlin):
            corpo.append(f'<line class="ln" x1="28" y1="{10 + lin * 125}" x2="{w - 28}" y2="{10 + lin * 125}" stroke="{c["borda"]}" pathLength="100"/>')
        salvar(pasta / "numeros-celular.svg", c, w, h, tit, "\n".join(corpo))
        feitos.append("numeros")

    if cfg.get("cases"):
        K = cfg["cases"]
        tit = "Cases: " + "; ".join(f"{k['nome']}, {k['numero']} {' '.join(k['rotulo'])}" for k in K)
        for nome, col, gap in (("cases", 2, 20), ("cases-celular", 1, 14)):
            pecas = [peca_case(c, f"{nome[0]}{i}", (i % col) * .25 + (i // col) * .1, k) for i, k in enumerate(K)]
            w, h, corpo = grade(pecas, col, gap)
            salvar(pasta / f"{nome}.svg", c, w, h, tit, corpo)
        feitos.append("cases")

    met = cfg.get("metodo")
    if met and met.get("passos"):
        S = met["passos"]
        n, ciclo = len(S), 9
        tit = ", ".join(p["nome"] for p in S)
        trecho = 75 / max(n - 1, 1)

        def nos(pfx):
            return "".join(
                f"@keyframes {pfx}{i}{{0%,{max(trecho * i - 1, 0):.0f}%{{fill:{c['fundo']};stroke:{c['borda2']}}}{trecho * i + 3:.0f}%,90%{{fill:{c['aceso']};stroke:{c['destaque']}}}100%{{fill:{c['fundo']};stroke:{c['borda2']}}}}}"
                f".{pfx}{i}{{animation:{pfx}{i} {ciclo}s ease infinite}}" for i in range(n))

        def trilho(eixo, dist):
            return (f".trilho{{stroke-dasharray:100;stroke-dashoffset:100;animation:trilho {ciclo}s ease-in-out infinite}}"
                    f"@keyframes trilho{{0%{{stroke-dashoffset:100;opacity:1}}75%,92%{{stroke-dashoffset:0;opacity:1}}100%{{stroke-dashoffset:0;opacity:0}}}}"
                    f".ponto{{animation:ponto {ciclo}s ease-in-out infinite}}"
                    f"@keyframes ponto{{0%{{transform:translate{eixo}(0);opacity:1}}75%{{transform:translate{eixo}({dist:.1f}px);opacity:1}}92%{{opacity:0}}100%{{transform:translate{eixo}(0);opacity:0}}}}")
        w, h = 840, 196
        colw = 840 / n
        xs = [colw / 2 + i * colw for i in range(n)]
        corpo = [moldura(c, "d", w, h, 18),
                 f'<line x1="{xs[0]:.1f}" y1="62" x2="{xs[-1]:.1f}" y2="62" stroke="{c["borda"]}" stroke-width="2"/>',
                 f'<line class="trilho" x1="{xs[0]:.1f}" y1="62" x2="{xs[-1]:.1f}" y2="62" stroke="{c["destaque"]}" stroke-width="2.4" pathLength="100"/>']
        for i, (p, x) in enumerate(zip(S, xs)):
            corpo.append(f'<circle class="md{i}" cx="{x:.1f}" cy="62" r="22" fill="{c["fundo"]}" stroke="{c["borda2"]}" stroke-width="1.6"/><text class="mk" x="{x:.1f}" y="69" text-anchor="middle">{i + 1}</text>')
            corpo.append(f'<g class="up" {atraso(.15 + i * .15)}><text class="mt" x="{x:.1f}" y="120" text-anchor="middle">{escape(p["nome"])}</text>{linhas("ms", round(x, 1), 143, 18, p.get("sub", []), "middle")}</g>')
        corpo.append(f'<circle class="ponto" cx="{xs[0]:.1f}" cy="62" r="5" fill="{c["claro"]}"/>')
        salvar(pasta / "metodo.svg", c, w, h, tit, "\n".join(corpo), nos("md") + trilho("X", xs[-1] - xs[0]))
        ys = [62 + i * 92 for i in range(n)]
        w, h = 420, ys[-1] + 62
        corpo = [moldura(c, "e", w, h, 18),
                 f'<line x1="56" y1="{ys[0]}" x2="56" y2="{ys[-1]}" stroke="{c["borda"]}" stroke-width="2"/>',
                 f'<line class="trilho" x1="56" y1="{ys[0]}" x2="56" y2="{ys[-1]}" stroke="{c["destaque"]}" stroke-width="2.4" pathLength="100"/>']
        for i, (p, y) in enumerate(zip(S, ys)):
            corpo.append(f'<circle class="me{i}" cx="56" cy="{y}" r="22" fill="{c["fundo"]}" stroke="{c["borda2"]}" stroke-width="1.6"/><text class="mk" x="56" y="{y + 7}" text-anchor="middle">{i + 1}</text>')
            corpo.append(f'<g class="up" {atraso(.15 + i * .15)}><text class="mt" x="96" y="{y - 4}">{escape(p["nome"])}</text><text class="ms" x="96" y="{y + 16}">{escape(" ".join(p.get("sub", [])))}</text></g>')
        corpo.append(f'<circle class="ponto" cx="56" cy="{ys[0]}" r="5" fill="{c["claro"]}"/>')
        salvar(pasta / "metodo-celular.svg", c, w, h, tit, "\n".join(corpo), nos("me") + trilho("Y", ys[-1] - ys[0]))
        feitos.append("metodo")

    pri = cfg.get("principios")
    if pri and pri.get("itens"):
        I = pri["itens"]
        n, ciclo = len(I), 2 * len(I)
        fatia = 100 / n
        tit = ", ".join(" ".join(x["linhas"]) for x in I)

        def kf(pfx):
            return "".join(
                f"@keyframes {pfx}{i}{{0%,{fatia * i:.0f}%{{stroke:{c['borda']};fill:{c['fundo']}}}{fatia * i + 4:.0f}%,{fatia * (i + 1) - 2:.0f}%{{stroke:{c['destaque']};fill:{c['aceso']}}}{min(fatia * (i + 1) + 2, 100):.0f}%,100%{{stroke:{c['borda']};fill:{c['fundo']}}}}}"
                f".{pfx}{i}{{animation:{pfx}{i} {ciclo}s ease infinite}}" for i in range(n))
        gap = 15
        cw = (838 - (n - 1) * gap) / n
        corpo = []
        for i, x in enumerate(I):
            px = 1 + i * (cw + gap)
            corpo.append(f'<g class="up" {atraso(.1 + i * .12)}><rect class="gd{i}" x="{px:.1f}" y="1" width="{cw:.1f}" height="110" rx="14" fill="{c["fundo"]}" stroke="{c["borda"]}" stroke-width="1.4"/>'
                         f'<text class="emo" x="{px + cw / 2:.1f}" y="44" text-anchor="middle">{x["icone"]}</text>'
                         + linhas("gt", round(px + cw / 2, 1), 72, 18, x["linhas"], "middle") + "</g>")
        salvar(pasta / "principios.svg", c, 840, 112, tit, "\n".join(corpo), kf("gd"))
        rw, rh, gap = 418, 50, 10
        corpo = []
        for i, x in enumerate(I):
            y = 1 + i * (rh + gap)
            corpo.append(f'<g class="up" {atraso(.1 + i * .1)}><rect class="ge{i}" x="1" y="{y}" width="{rw}" height="{rh}" rx="12" fill="{c["fundo"]}" stroke="{c["borda"]}" stroke-width="1.4"/>'
                         f'<text class="emo" x="36" y="{y + 33}" text-anchor="middle" style="font-size:20px">{x["icone"]}</text>'
                         f'<text class="gt" x="66" y="{y + 30}" style="font-size:15px">{escape(" ".join(x["linhas"]))}</text></g>')
        salvar(pasta / "principios-celular.svg", c, rw + 2, n * rh + (n - 1) * gap + 2, tit, "\n".join(corpo), kf("ge"))
        feitos.append("principios")

    if cfg.get("abertos"):
        A = cfg["abertos"]
        tit = "Aberto no GitHub: " + ", ".join(a["nome"] for a in A)
        for nome, col, gap in (("abertos", min(3, len(A)), 14), ("abertos-celular", 1, 12)):
            pecas = [peca_aberto(c, f"{nome[0]}{i}", i * .15, a) for i, a in enumerate(A)]
            w, h, corpo = grade(pecas, col, gap)
            salvar(pasta / f"{nome}.svg", c, w, h, tit, corpo)
        feitos.append("abertos")
    return feitos


# ── README ───────────────────────────────────────────────────────────────

def escudo(texto):
    return quote(texto.replace("-", "--").replace("_", "__"))


def badge(rotulo, cor, logo, logo_cor, url=None, alt=None):
    img = f'<img src="https://img.shields.io/badge/{escudo(rotulo)}-{cor.lstrip("#")}?style=for-the-badge&logo={logo}&logoColor={logo_cor.lstrip("#")}" alt="{attr(alt or rotulo)}" />'
    return f'<a href="{url}">{img}</a>' if url else img


def picture(nome, alt, largura_desktop="100%"):
    return (f'<picture>\n  <source media="(max-width: 700px)" srcset="assets/{nome}-celular.svg" />\n'
            f'  <img src="assets/{nome}.svg" width="{largura_desktop}" alt="{attr(alt)}" />\n</picture>')


def montar_readme(cfg, feitos):
    c = tema(cfg)
    T = {**TITULOS, **cfg.get("titulos", {})}
    ct = cfg.get("contatos", {})
    claro, escuro, tinta_escura = c["claro"].lstrip("#"), c["escuro"].lstrip("#"), c["tinta_escura"].lstrip("#")
    if c["escuro"] == TEMAS["grafite"]["escuro"]:
        escuro = "BDBDBD"
    caixa, destaque = "1B1B1B" if cfg.get("tema") == "grafite" else c["caixa"].lstrip("#"), c["destaque"].lstrip("#")
    out = [f"<!-- Perfil de {escape(cfg['nome'])} · cartões em assets/ gerados pela skill perfil-github -->", "", '<div align="center">', ""]
    out.append(
        f'<img src="https://capsule-render.vercel.app/api?type=waving&color=0:{claro},100:{escuro}&height=200&section=header'
        f'&text={quote(cfg["nome"])}&fontColor={tinta_escura}&fontSize=44&fontAlignY=36&desc={quote(cfg.get("frase", ""))}'
        f'&descAlignY=58&descColor={tinta_escura}&descSize=19&animation=fadeIn" width="100%" alt="{attr(cfg["nome"])}" />')
    out.append("")
    if cfg.get("linhas_digitando"):
        ls = ";".join(quote(l).replace("%20", "+") for l in cfg["linhas_digitando"])
        site = ct.get("site") or f"https://github.com/{cfg['login']}"
        out += [f'<a href="{site}">',
                f'  <img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=600&size=20&pause=1300&color={c["medio"].lstrip("#")}&center=true&vCenter=true&width=700&lines={ls}" alt="" />',
                "</a>", "", "<br/>", ""]
    bs = []
    if ct.get("site"):
        bs.append(badge(re.sub(r"^https?://(www\.)?", "", ct["site"]).rstrip("/"), destaque, "googlechrome", tinta_escura, ct["site"], "Site"))
    if ct.get("linkedin"):
        bs.append(badge("LinkedIn", caixa, "linkedin", destaque, ct["linkedin"]))
    if ct.get("email"):
        bs.append(badge("E-mail", caixa, "gmail", destaque, f"mailto:{ct['email']}"))
    if ct.get("agenda"):
        bs.append(badge("Agendar conversa", caixa, "googlemeet", destaque, ct["agenda"]))
    for o in ct.get("outros", []):
        bs.append(badge(o["rotulo"], caixa, o.get("logo", "googlechrome"), destaque, o.get("url")))
    if ct.get("local"):
        bs.append(badge(ct["local"], caixa, "googlemaps", destaque))
    out += bs + ["", "<br/><br/>", ""]
    if cfg.get("pitch"):
        out.append(f"**{cfg['pitch']}**")
        out.append("")
    if cfg.get("pitch_sub"):
        out += [f"<sub>{cfg['pitch_sub']}</sub>", ""]
    out += ["<br/>", ""]
    if "papeis" in feitos:
        out += [picture("papeis", ", ".join(p["titulo"] for p in cfg["papeis"])), "", "<br/>", ""]
    if "numeros" in feitos:
        out += [picture("numeros", ", ".join(f"{x['valor']} {' '.join(x['rotulo'])}" for x in cfg["numeros"])), ""]
    out += ["</div>", "", "<br/>", ""]

    if "cases" in feitos:
        K = cfg["cases"]
        out += ['<div align="center">', "", f"## {T['cases']}", ""]
        if any(k.get("anonimo") for k in K):
            out += ["<sub>Cliente que não autorizou o nome aparece pelo setor.</sub>", "", "<br/>", ""]
        out += [picture("cases", "Cases: " + ", ".join(k["nome"] for k in K)), "", "</div>", ""]
        out += ["<details>", f"<summary><b>{T['detalhes']}</b></summary>", "", "<br/>", ""]
        for k in K:
            nome = f"[{k['nome']}]({k['link']})" if k.get("link") else k["nome"]
            cab = f"**{k['icone']} {nome}**"
            if k.get("contexto"):
                cab += f" · {k['contexto']}"
            out.append(cab)
            dt = k.get("detalhe", {})
            for chave, rot in (("problema", "Problema"), ("solucao", "Solução"), ("resultado", "Resultado"), ("papel", "Meu papel")):
                if dt.get(chave):
                    out.append(f"- **{rot}:** {dt[chave]}")
            out.append("")
        if cfg.get("fontes"):
            out += [f"<sub>Fontes: {cfg['fontes']}</sub>", ""]
        out += ["</details>", "", "<br/>", ""]

    if "metodo" in feitos or "principios" in feitos:
        out += ['<div align="center">', "", f"## {T['metodo']}", ""]
        if "metodo" in feitos:
            out += [picture("metodo", ", ".join(p["nome"] for p in cfg["metodo"]["passos"])), ""]
            if cfg["metodo"].get("frase"):
                out += [cfg["metodo"]["frase"], ""]
        if "principios" in feitos:
            if cfg["principios"].get("frase"):
                out += [cfg["principios"]["frase"], ""]
            out += [picture("principios", ", ".join(" ".join(x["linhas"]) for x in cfg["principios"]["itens"])), ""]
        out += ["</div>", "", "<br/>", ""]

    if "abertos" in feitos:
        A = cfg["abertos"]
        out += ['<div align="center">', "", f"## {T['abertos']}", "", picture("abertos", ", ".join(a["nome"] for a in A)), ""]
        links = " · ".join(f'<a href="{a["link"]}">{escape(a["nome"])}</a>' for a in A if a.get("link"))
        if links:
            out += [f"<sub>{links}</sub>", ""]
        if cfg.get("nota_repos"):
            out += [f"<sub>{cfg['nota_repos']}</sub>", ""]
        out += ["</div>", "", "<br/>", ""]

    st = cfg.get("stack", {})
    if st.get("skillicons") or st.get("badges"):
        out += ['<div align="center">', "", f"## {T['stack']}", ""]
        ic = st.get("skillicons", [])
        for i in range(0, len(ic), 9):
            out += [f'<img src="https://skillicons.dev/icons?i={",".join(ic[i:i + 9])}&perline=9" alt="{", ".join(ic[i:i + 9])}" />', "<br/>"]
        if st.get("badges"):
            out += ["<br/>", ""]
            out += [f'![{b["nome"]}](https://img.shields.io/badge/{escudo(b["nome"])}-{caixa}?style=for-the-badge&logo={b.get("logo", "")}&logoColor={destaque})' for b in st["badges"]]
        out += ["", "</div>", "", "<br/>", ""]

    cta = cfg.get("cta", {})
    if cta:
        out += ['<div align="center">', "", f"## {T['cta']}", ""]
        if cta.get("titulo"):
            out += [f"**{cta['titulo']}**", ""]
        if cta.get("sub"):
            out += [f"<sub>{cta['sub']}</sub>", ""]
        out += ["<br/>", ""]
        bs = []
        if ct.get("email"):
            bs.append(badge(ct["email"], destaque, "gmail", tinta_escura, f"mailto:{ct['email']}", "E-mail"))
        if ct.get("site"):
            bs.append(badge("Site", caixa, "googlechrome", destaque, ct["site"]))
        out += bs + ["", "</div>", ""]
    out += ['<div align="center">',
            f'<img src="https://capsule-render.vercel.app/api?type=waving&color=0:{escuro},100:{claro}&height=110&section=footer&animation=twinkling" width="100%" alt="" />',
            "</div>", ""]
    return "\n".join(out)


# ── conferência ──────────────────────────────────────────────────────────

def conferir(cfg, repo, nao_citar):
    erros, avisos = [], []

    def cabe(caminho, texto, tamanho, estilo, limite, espaco=0.0):
        lw = largura(texto, tamanho, estilo, espaco)
        if lw > limite:
            erros.append(f"{caminho}: \"{texto}\" mede ~{lw:.0f}px e cabe {limite:.0f}px. Encurte ou quebre em duas linhas.")

    for campo in ("login", "nome"):
        if not cfg.get(campo):
            erros.append(f"falta o campo '{campo}'")
    ct = cfg.get("contatos", {})
    if not any(ct.get(k) for k in ("site", "linkedin", "email", "agenda")):
        erros.append("contatos: informe ao menos um entre site, linkedin, email e agenda (pergunte à pessoa; não invente)")
    if repo.name != cfg.get("login"):
        avisos.append(f"a pasta do repositório se chama '{repo.name}', mas o perfil só aparece no repositório {cfg.get('login')}/{cfg.get('login')}")

    P = cfg.get("papeis", [])
    if P and not 2 <= len(P) <= 4:
        erros.append(f"papeis: use de 2 a 4 (há {len(P)})")
    for i, p in enumerate(P):
        cabe(f"papeis[{i}].titulo", p["titulo"], 14.5, "negrito", 186)
        cabe(f"papeis[{i}].sub", p.get("sub", ""), 12.5, "sans", 186)

    N = cfg.get("numeros", [])
    if N and not 2 <= len(N) <= 4:
        erros.append(f"numeros: use de 2 a 4 (há {len(N)})")
    for i, x in enumerate(N):
        lim = min(840 / max(len(N), 1), 210) - 20
        cabe(f"numeros[{i}].valor", x["valor"], 46, "serif", lim)
        if len(x["rotulo"]) > 2:
            erros.append(f"numeros[{i}].rotulo: no máximo 2 linhas")
        for j, l in enumerate(x["rotulo"]):
            cabe(f"numeros[{i}].rotulo[{j}]", l, 13.5, "sans", lim)
        if not x.get("fonte"):
            avisos.append(f"numeros[{i}] ({x['valor']}): sem 'fonte'. Número sem origem e data não se sustenta numa conversa.")

    K = cfg.get("cases", [])
    if K and not 2 <= len(K) <= 10:
        erros.append(f"cases: use de 2 a 10 (há {len(K)})")
    if len(K) % 2:
        avisos.append("cases: número ímpar; o último cartão fica centralizado sozinho na grade")
    for i, k in enumerate(K):
        lim_selo = largura(k.get("selo", ""), 10.5, "caixa-alta", 1.3) + 22 if k.get("selo") else 0
        cabe(f"cases[{i}].nome", k["nome"], 21, "negrito", 420 - 76 - 22 - lim_selo - 10)
        cabe(f"cases[{i}].sub", k.get("sub", ""), 13, "sans", 322)
        cabe(f"cases[{i}].numero", k["numero"], 50, "serif", 376)
        if len(k["rotulo"]) > 2:
            erros.append(f"cases[{i}].rotulo: no máximo 2 linhas")
        for j, l in enumerate(k["rotulo"]):
            cabe(f"cases[{i}].rotulo[{j}]", l, 14, "sans", 372)
        cabe(f"cases[{i}].rodape", k.get("rodape", ""), 12.5, "sans", 372)
        if k.get("selo") and k["selo"] != k["selo"].upper():
            avisos.append(f"cases[{i}].selo: o selo foi desenhado para caixa alta")
        if not k.get("detalhe", {}).get("problema"):
            avisos.append(f"cases[{i}] ({k['nome']}): sem 'detalhe.problema'; o bloco que abre fica raso")
        if k.get("link") and not k["link"].startswith("https://"):
            erros.append(f"cases[{i}].link precisa começar com https://")

    S = (cfg.get("metodo") or {}).get("passos", [])
    if S and not 3 <= len(S) <= 5:
        erros.append(f"metodo.passos: use de 3 a 5 (há {len(S)})")
    for i, p in enumerate(S):
        lim = 840 / max(len(S), 1) - 16
        cabe(f"metodo.passos[{i}].nome", p["nome"], 16, "negrito", lim)
        for j, l in enumerate(p.get("sub", [])):
            cabe(f"metodo.passos[{i}].sub[{j}]", l, 12.5, "sans", lim)
        cabe(f"metodo.passos[{i}].sub (celular)", " ".join(p.get("sub", [])), 12.5, "sans", 304)

    I = (cfg.get("principios") or {}).get("itens", [])
    if I and not 3 <= len(I) <= 6:
        erros.append(f"principios.itens: use de 3 a 6 (há {len(I)})")
    for i, x in enumerate(I):
        cw = (838 - (len(I) - 1) * 15) / max(len(I), 1)
        for j, l in enumerate(x["linhas"]):
            cabe(f"principios.itens[{i}].linhas[{j}]", l, 13.5, "negrito", cw - 16)
        cabe(f"principios.itens[{i}] (celular)", " ".join(x["linhas"]), 15, "negrito", 330)

    A = cfg.get("abertos", [])
    if len(A) > 3:
        erros.append("abertos: no máximo 3")
    for i, a in enumerate(A):
        cabe(f"abertos[{i}].nome", a["nome"], 16, "negrito", 244)
        for j, l in enumerate(a["linhas"]):
            cabe(f"abertos[{i}].linhas[{j}]", l, 12.5, "sans", 244)

    readme = repo / "README.md"
    publicos = [readme] + sorted((repo / "assets").glob("*.svg"))
    for termo in nao_citar:
        for arq in publicos:
            if arq.exists() and termo.lower() in arq.read_text(encoding="utf-8").lower():
                erros.append(f"NÃO CITAR: '{termo}' aparece em {arq.relative_to(repo)}")
    for arq in publicos:
        if arq.exists():
            txt = arq.read_text(encoding="utf-8")
            for padrao, nome in ((r"(?i)(api[_-]?key|token|senha|password)\s*[:=]", "credencial"),
                                 (r"\b(?:\d{1,3}\.){3}\d{1,3}\b", "endereço IP"),
                                 (r"(?i)\bTODO\b|PREENCHER", "texto provisório")):
                if re.search(padrao, txt):
                    erros.append(f"{arq.relative_to(repo)}: parece ter {nome}")
    if shutil.which("xmllint"):
        for svg in (repo / "assets").glob("*.svg"):
            r = subprocess.run(["xmllint", "--noout", str(svg)], capture_output=True, text=True)
            if r.returncode:
                erros.append(f"{svg.name}: XML inválido: {r.stderr.strip()[:200]}")
    return erros, avisos


# ── diagnóstico (gh) ─────────────────────────────────────────────────────

def gh(*args):
    r = subprocess.run(["gh", *args], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def diagnostico(login):
    if not shutil.which("gh"):
        print("gh (GitHub CLI) não está instalado: o diagnóstico fica para o navegador, em github.com/" + login)
        return
    u = gh("api", f"users/{login}")
    if not u:
        print(f"não achei o usuário {login}")
        return
    u = json.loads(u)
    print("== Perfil público")
    for k in ("name", "bio", "company", "blog", "location", "public_repos", "followers"):
        print(f"  {k}: {u.get(k)}")
    existe = gh("api", f"repos/{login}/{login}", "--jq", ".visibility")
    print(f"== Repositório de perfil {login}/{login}: {existe or 'NÃO existe (criar, público, com o mesmo nome do usuário)'}")
    q = """query($l:String!){user(login:$l){pinnedItems(first:6){nodes{... on Repository{nameWithOwner isPrivate}}}
      repositoriesContributedTo(first:50,includeUserRepositories:true,contributionTypes:[COMMIT,PULL_REQUEST,ISSUE,REPOSITORY]){nodes{nameWithOwner isPrivate isFork stargazerCount description}}
      repositories(first:50,ownerAffiliations:OWNER,privacy:PUBLIC,orderBy:{field:STARGAZERS,direction:DESC}){nodes{nameWithOwner isFork stargazerCount description}}
      contributionsCollection{totalCommitContributions restrictedContributionsCount commitContributionsByRepository(maxRepositories:8){repository{nameWithOwner isPrivate}contributions{totalCount}}}}}"""
    r = gh("api", "graphql", "-f", f"query={q}", "-f", f"l={login}")
    if not r:
        print("  (consulta GraphQL falhou; confira `gh auth status`)")
        return
    d = json.loads(r)["data"]["user"]
    print("== Fixados hoje:", ", ".join(n["nameWithOwner"] for n in d["pinnedItems"]["nodes"] if n) or "nenhum")
    print("== Repositórios públicos seus (candidatos a fixar):")
    for n in d["repositories"]["nodes"]:
        print(f"  {n['nameWithOwner']}{' (fork)' if n['isFork'] else ''} ★{n['stargazerCount']} {n['description'] or ''}")
    print("== Públicos de outros em que você contribuiu (também podem ser fixados):")
    for n in d["repositoriesContributedTo"]["nodes"]:
        if not n["isPrivate"] and not n["nameWithOwner"].lower().startswith(login.lower() + "/"):
            print(f"  {n['nameWithOwner']} ★{n['stargazerCount']} {n['description'] or ''}")
    cc = d["contributionsCollection"]
    tot = cc["totalCommitContributions"]
    print(f"== Commits no último ano que a API mostra: {tot} (privados sem detalhe: {cc['restrictedContributionsCount']})")
    for item in cc["commitContributionsByRepository"]:
        n = item["contributions"]["totalCount"]
        nome = item["repository"]["nameWithOwner"]
        share = n / tot if tot else 0
        alerta = "  ⚠️ parece automação: confira antes de citar a contagem" if share > .4 or re.search(r"(?i)backup|bkp|sync|autocommit|bot", nome) else ""
        print(f"  {nome}: {n} ({share:.0%}){alerta}")
    escopos = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True)
    if "'user'" not in (escopos.stdout + escopos.stderr):
        print("== O token do gh não tem o escopo 'user': bio, site e empresa se editam em github.com/settings/profile "
              "ou depois de `gh auth refresh -h github.com -s user`.")


# ── prévia ───────────────────────────────────────────────────────────────

def previa(cfg, repo, saida):
    saida.mkdir(parents=True, exist_ok=True)
    readme = (repo / "README.md").read_text(encoding="utf-8")
    html = None
    if shutil.which("gh"):
        r = subprocess.run(["gh", "api", "markdown", "-f", "mode=markdown", "-f", f"context={cfg['login']}/{cfg['login']}", "-f", f"text={readme}"],
                           capture_output=True, text=True)
        if r.returncode == 0:
            html = r.stdout
    if html is None:
        html = "<p>(sem o gh, a prévia mostra só os cartões)</p>" + "".join(
            f'<p><img src="assets/{p.name}" width="100%"></p>' for p in sorted((repo / "assets").glob("*.svg")) if "celular" not in p.name)
    base = repo.resolve().as_uri() + "/"
    (saida / "readme.html").write_text(
        f"""<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><base href="{base}">
<style>body{{margin:0;padding:16px;background:#0d1117;color:#e6edf3;font:14px/1.5 -apple-system,Segoe UI,Helvetica,Arial,sans-serif}}
a{{color:#4493f8}}img{{max-width:100%}}table{{border-collapse:collapse}}td,th{{border:1px solid #30363d;padding:6px 13px}}
h2{{border-bottom:1px solid #30363d;padding-bottom:.3em}}details{{margin:1em 0}}</style>
<div style="max-width:880px;margin:auto">{html}</div>""", encoding="utf-8")
    (saida / "index.html").write_text(
        """<!doctype html><meta charset="utf-8"><title>Prévia do perfil</title>
<body style="margin:0;background:#010409;color:#8b949e;font:13px sans-serif;display:flex;gap:24px;padding:16px;align-items:flex-start">
<div><p>Computador (900 px)</p><iframe src="readme.html" style="width:900px;height:92vh;border:1px solid #30363d"></iframe></div>
<div><p>Celular (390 px)</p><iframe src="readme.html" style="width:390px;height:92vh;border:1px solid #30363d"></iframe></div>""", encoding="utf-8")
    return saida / "index.html"


# ── linha de comando ─────────────────────────────────────────────────────

def ler_nao_citar(caminho):
    if not caminho or not Path(caminho).exists():
        return []
    return [l.strip() for l in Path(caminho).read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("diagnostico")
    d.add_argument("--login", required=True)
    for nome in ("montar", "conferir", "previa"):
        p = sub.add_parser(nome)
        p.add_argument("--config", required=True)
        p.add_argument("--repo", required=True)
        p.add_argument("--nao-citar", help="arquivo com um nome por linha que nunca pode sair no perfil")
        p.add_argument("--saida", help="pasta da prévia (padrão: previa/ ao lado do perfil.json)")
    a = ap.parse_args()

    if a.cmd == "diagnostico":
        diagnostico(a.login)
        return
    cfg = json.loads(Path(a.config).read_text(encoding="utf-8"))
    repo = Path(a.repo)
    nao = ler_nao_citar(a.nao_citar or (Path(a.config).parent / "nao-citar.txt"))
    if a.cmd == "montar":
        if (repo / "perfil.json").resolve() == Path(a.config).resolve():
            sys.exit("o perfil.json está dentro do repositório público; mova para fora antes de montar")
        feitos = gerar_svgs(cfg, repo / "assets")
        (repo / "README.md").write_text(montar_readme(cfg, feitos), encoding="utf-8")
        print("montado:", ", ".join(feitos) or "nenhum bloco de cartões", f"→ {repo}/README.md e {repo}/assets/")
        a.cmd = "conferir"
    if a.cmd == "conferir":
        erros, avisos = conferir(cfg, repo, nao)
        for x in avisos:
            print("aviso:", x)
        for x in erros:
            print("ERRO:", x)
        print(f"conferência: {len(erros)} erro(s), {len(avisos)} aviso(s)" + ("" if nao else " · sem lista de nomes proibidos (nao-citar.txt)"))
        sys.exit(1 if erros else 0)
    if a.cmd == "previa":
        saida = Path(a.saida) if a.saida else Path(a.config).parent / "previa"
        print("prévia:", previa(cfg, repo, saida))


if __name__ == "__main__":
    main()
