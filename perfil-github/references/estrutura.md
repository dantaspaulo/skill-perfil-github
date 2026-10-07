# Estrutura do design

## Índice
1. A ideia do layout
2. Ordem das seções
3. Os blocos e seus campos (com limites)
4. Temas e tema a partir do site
5. Escrevendo para cartão
6. Mexendo no gerador

## 1. A ideia do layout

O visitante passa de 10 a 30 segundos no perfil. O layout responde três perguntas, nesta ordem:
**quem é** (topo), **o que prova** (números e cases) e **como falar** (convite). Tudo o que é
detalhe fica escondido num bloco que abre.

Princípios que o gerador já segue e que vale manter ao mudar algo:
- **Um número grande por cartão.** O olho lê o número primeiro; o rótulo explica em até 2 linhas.
- **Cartões escuros com borda viva** funcionam nos dois temas do GitHub (claro e escuro), como uma
  peça de vitrine. Por isso o fundo do cartão é sempre escuro, independente do tema do visitante.
- **Animação discreta e com propósito**: a luz que corre na borda e o brilho que passa dizem "vivo";
  o número que sobe direciona o olho; o ponto que percorre o método conta a sequência. Nada pisca.
- **Texto longo não vai em imagem.** Imagem não é pesquisável nem acessível; o texto completo dos
  cases fica no `<details>`, em Markdown.

## 2. Ordem das seções (README gerado)

| # | Seção | Origem no `perfil.json` | Obrigatória |
|---|---|---|---|
| 1 | Cabeçalho em onda com nome e frase | `nome`, `frase`, `tema` | sim |
| 2 | Linha que se digita sozinha | `linhas_digitando` | não |
| 3 | Botões de contato | `contatos` | sim (ao menos um) |
| 4 | Pitch em destaque | `pitch`, `pitch_sub` | recomendado |
| 5 | Papéis atuais (cartões) | `papeis` | recomendado |
| 6 | Números (faixa) | `numeros` | recomendado |
| 7 | Cases (grade de cartões) + detalhes que abrem | `cases`, `fontes` | o coração |
| 8 | Método (linha do tempo animada) | `metodo` | não |
| 9 | Princípios (ícones que acendem em sequência) | `principios` | não |
| 10 | Aberto no GitHub (cartões) | `abertos`, `nota_repos` | se houver |
| 11 | Stack (ícones e badges) | `stack` | recomendado |
| 12 | Convite final e rodapé em onda | `cta` | recomendado |

Títulos das seções mudam em `titulos` (chaves `cases`, `metodo`, `abertos`, `stack`, `cta`,
`detalhes`), por exemplo para escrever em inglês.

## 3. Os blocos e seus campos

Os limites em pixels são os que a conferência usa; o texto em caracteres é só uma referência.

### Topo
- `login`: usuário do GitHub. O repositório precisa se chamar igual.
- `nome`: como a pessoa quer ser chamada.
- `frase`: até ~40 caracteres, aparece embaixo do nome ("automatiza operações com IA").
- `linhas_digitando`: 2 a 4 frases curtas (até ~45 caracteres) que se alternam.
- `contatos`: `site`, `linkedin`, `email`, `agenda`, `local`, e `outros` (lista de
  `{rotulo, url, logo}`; `logo` é um nome do simpleicons.org).
- `pitch`: 1 ou 2 frases; aceita `<br/>` para quebrar. `pitch_sub`: uma linha menor.

### `papeis` (2 a 4)
`{icone, titulo, sub}`. Título até ~22 caracteres (cabe 186 px no celular), sub até ~26.
Ex.: `{"icone": "🧭", "titulo": "Consultora de IA", "sub": "4 clientes ativos"}`.

### `numeros` (2 a 4)
`{valor, rotulo: [linha1, linha2], fonte}`. Valor curto em serifa grande ("1 mi+", "−95%", "8").
O limite vem do celular (dois por linha): **valor até ~190 px, uns 5 a 6 caracteres** ("99,9%" cabe,
"15 min" cabe, "18%→9%" não: símbolos largos como %, → e M contam mais) e **cada linha do rótulo
até ~190 px, uns 26 caracteres**. Número ímpar funciona: o último fica centralizado.
`fonte` não aparece no cartão, mas a conferência avisa quando falta; resuma as fontes em `fontes`.

### `cases` (2 a 10; par fica melhor)
| campo | o que é | limite |
|---|---|---|
| `icone` | um emoji | 1 |
| `nome` | título do cartão | ~18 caracteres (depende do selo) |
| `sub` | setor ou descrição curta | ~34 caracteres |
| `selo` | etiqueta em caixa alta no canto | ~16 caracteres ("PRODUTO PRÓPRIO", "CLIENTE") |
| `numero` | o número grande | ~9 caracteres |
| `rotulo` | 1 ou 2 linhas explicando o número | ~38 caracteres por linha |
| `rodape` | escala, contexto ou tecnologias | ~46 caracteres |
| `anonimo` | `true` se o nome do cliente não aparece | liga a nota "pelo setor" |
| `link` | página pública, se houver | precisa ser https |
| `contexto` | aparece no detalhe ao lado do nome ("fundadora", "pela consultoria X") | |
| `detalhe` | `{problema, solucao, resultado, papel}` em frases completas | sem limite (é Markdown) |

Sem número de verdade? Use um fato curto e verdadeiro que ainda informe: prazo ("2 semanas", "1º
dia"), cobertura ("24 h"), conformidade ("LGPD ✓"), escala ("3 lojas"). Evite contagem fraca ("1
bot") e nunca invente: nesse caso o cartão pode trazer o papel no rótulo ("feito do zero, / sozinho").
Número ímpar de cases funciona (o último fica centralizado), mas par fica mais equilibrado.

### `metodo` (opcional, 3 a 5 passos)
`{passos: [{nome, sub: [linha1, linha2]}], frase}`. No computador é uma linha horizontal com um
ponto que percorre os passos; no celular, vertical.

### `principios` (opcional, 3 a 6)
`{frase, itens: [{icone, linhas: [linha1, linha2]}]}`. Cada item acende na sua vez.

### `abertos` (opcional, até 3)
`{icone, nome, dono, linhas: [linha1, linha2], selo, link}`. Os links também saem em texto embaixo,
porque o bloco inteiro é uma imagem só. Selo honesto: `MEU` para repositório da pessoa,
`CONTRIBUIÇÃO` só para projeto de outros em que ela contribuiu de verdade. Repositório de teste ou
de demonstração não entra.

### `stack`
- `skillicons`: nomes do skillicons.dev (ex.: `python, ts, nextjs, react, postgres, docker, aws`).
  Quebra em linhas de 9.
- `badges`: `{nome, logo}` para o que o skillicons não tem (logo do simpleicons.org).

### `cta`
`{titulo, sub}`. Usa o e-mail e o site de `contatos` nos botões.

## 4. Temas

`"tema"` aceita `champagne`, `esmeralda`, `oceano` ou `grafite`. Para personalizar, passe um objeto
com uma base e só as chaves que mudam:

```json
"tema": { "base": "oceano", "destaque": "#FF8A3D", "claro": "#FFB27A", "escuro": "#B85A1E", "medio": "#D9732F" }
```

Chaves e para que servem:
- `fundo`, `caixa`, `borda`, `borda2`: o cartão (escuros, do mais fundo ao mais claro);
- `tinta`, `corpo`, `suave`, `apagado`: textos, do mais forte ao mais fraco;
- `destaque`: selos, números do método, botão principal;
- `claro` → `escuro`: o degradê dos números grandes, da borda viva e do cabeçalho;
- `medio`: a linha que se digita (precisa ler bem no fundo branco e no escuro);
- `aceso`: fundo do item aceso nas animações;
- `tinta_escura`: texto sobre o cabeçalho claro;
- `brilho`: o reflexo que passa pelo cartão.

**Tema a partir do site da pessoa:** pegue a cor de destaque do site (botão principal, link) para
`destaque`, uma versão mais clara para `claro` e uma mais escura para `escuro`; mantenha o resto da
base. Confira na prévia o cabeçalho (texto escuro sobre o degradê) e a linha que se digita no tema
claro.

## 5. Escrevendo para cartão

- Comece pelo número e escreva o rótulo para ele: "40 h" → "por semana devolvidas / ao time de
  atendimento".
- Rótulo completa a frase do número; não repita o nome do case.
- Rodapé dá escala ou tecnologia ("12 unidades · WhatsApp e e-mail").
- Selo diz a natureza: PRODUTO PRÓPRIO, CLIENTE, EMPREGO, CONSULTORIA, CONTRIBUIÇÃO, ou o nome da
  empresa autorizada.
- Mesma estrutura em todos os cartões: o olho compara melhor.

## 6. Mexendo no gerador

`scripts/perfil.py` tem três partes: as **peças** (`peca_case`, `peca_aberto` e as células dentro de
`gerar_svgs`), a **composição** (`grade` monta a grade e centraliza a última linha incompleta;
`salvar` embrulha com estilo e degradês) e o **README** (`montar_readme`). As classes CSS de texto
ficam em `css_base` com prefixo por tipo de peça (`c*` cartão, `n*` número, `m*` método, `g*`
princípios, `p*` papéis, `a*` abertos). Se mudar tamanho de fonte ou de cartão, atualize os limites
em `conferir()` junto, senão a trava passa a mentir.
