---
name: perfil-github
description: Monta ou refaz o README de perfil do GitHub (o repositório USUARIO/USUARIO) com visual animado e organizado, em vez de texto corrido. Gera cartões SVG animados de cases (problema, solução e resultado), números com fonte, papéis atuais, método de trabalho e projetos abertos, com versão própria para celular e tema de cores escolhido. Entrevista a pessoa sobre o que não conseguir descobrir sozinho (posicionamento, cases, números, o que pode e o que não pode ser citado), protege nome de cliente não autorizado com uma trava que recusa, confere se cada texto cabe no cartão e mostra uma prévia antes de publicar. Use sempre que alguém pedir para criar, melhorar, arrumar ou "deixar bonito" o perfil do GitHub, o README do perfil, colocar cases ou portfólio no GitHub, fixar repositórios, ou alinhar o GitHub a um novo posicionamento, site ou LinkedIn, mesmo que a pessoa não fale "README".
---

# Perfil do GitHub com cases animados

Esta skill transforma o perfil do GitHub numa vitrine que se lê em 20 segundos: quem a pessoa é,
o que ela entrega e a prova disso. O resultado é um `README.md` no repositório especial
`USUARIO/USUARIO` mais uma pasta `assets/` com SVGs animados.

**Por que SVG animado.** O README do GitHub não roda JavaScript nem aceita CSS próprio, mas
mostra imagens, e um SVG com `@keyframes` dentro anima mesmo servido como imagem. Por isso cada
bloco visual é um SVG gerado a partir de um arquivo de dados (`perfil.json`). O texto longo dos
cases vai para um bloco `<details>` fechado: quem quer ler abre, quem está passando vê só os
cartões.

**Por que versão de celular.** Cartões lado a lado ficam ilegíveis num celular. Cada bloco sai em
duas versões, e o README usa `<picture><source media="(max-width: 700px)">` para trocar. O GitHub
respeita essa troca.

Tudo é feito pelo script `scripts/perfil.py` (só Python padrão; o `gh` é opcional). O trabalho da
skill é entender a pessoa, escrever um bom `perfil.json` e conferir o resultado.

## Fluxo

### 1. Descobrir o que já existe, antes de perguntar

Pergunte só o que não dá para descobrir. Comece pelo que é público:

```bash
python3 <skill>/scripts/perfil.py diagnostico --login USUARIO
```

Ele mostra campos do perfil, se o repositório de perfil existe, o que está fixado, repositórios
públicos (candidatos a fixar), repositórios de outros em que a pessoa contribuiu e quais
repositórios concentram os commits (sinaliza automação que infla a contagem). Leia também o README
atual, se existir. Se a pessoa tiver site, LinkedIn ou currículo, leia: o posicionamento quase
sempre já está escrito lá.

Resuma para a pessoa em poucas linhas o que encontrou e o que ainda falta.

### 2. Entrevistar sobre o que falta

Leia `references/entrevista.md`. O essencial:
- no máximo 3 rodadas, poucas perguntas por rodada, agrupadas por assunto;
- em vez de pergunta aberta, traga um rascunho para a pessoa aprovar ("sugiro esta frase; serve?");
- para cada case, pergunte se o nome do cliente pode aparecer. Se não puder, o case vai pelo setor
  e o nome entra no `nao-citar.txt`;
- todo número precisa de fonte e data. Se a pessoa não souber de onde vem, o número não entra;
- contato, link e nome de repositório vêm da pessoa ou do que é público dela. Não preencha com
  palpite: se faltar, pergunte.

Se a ferramenta `AskUserQuestion` existir, use para escolhas fechadas (tema, seções, sim ou não).

### 3. Escrever os dados FORA do repositório

Crie uma pasta de trabalho fora do clone, por exemplo `~/perfil-github-trabalho/`, com:
- `perfil.json`: todos os textos e escolhas. Modelo completo em `references/perfil.exemplo.json`;
  o que cada campo faz e os limites de tamanho em `references/estrutura.md`;
- `nao-citar.txt`: um nome por linha (clientes, pessoas, produtos internos) que nunca pode sair.

Fica fora porque o repositório de perfil é público, e o `nao-citar.txt` é, por definição, uma lista
de nomes que não podem ser públicos.

### 4. Montar e conferir

```bash
gh repo clone USUARIO/USUARIO   # ou git clone; se não existir, crie (passo 6)
python3 <skill>/scripts/perfil.py montar --config ~/perfil-github-trabalho/perfil.json --repo ./USUARIO
```

O `montar` gera README e SVGs e já roda a conferência, que **recusa** (sai com erro):
- texto que não cabe no cartão (SVG não quebra linha sozinho);
- nome do `nao-citar.txt` em qualquer arquivo público;
- algo com cara de credencial, IP ou texto provisório;
- SVG inválido, quantidade fora do limite em cada bloco.

Corrija o `perfil.json` e rode de novo até zerar os erros. Leia os avisos: número sem fonte, por
exemplo, não trava, mas precisa de uma decisão.

### 5. Prévia antes de publicar

```bash
python3 <skill>/scripts/perfil.py previa --config ~/perfil-github-trabalho/perfil.json --repo ./USUARIO
```

Gera `previa/index.html` na pasta do `perfil.json` (fora do repositório; mude com `--saida`), com o
README como o GitHub renderiza, lado a lado em 900 px e 390 px.
Mostre à pessoa. Se houver Playwright, capture as duas larguras e olhe você também: texto
encostando na borda, cartão vazio, cor ruim no tema claro.

### 6. Publicar, só com o ok da pessoa

Publicar deixa o conteúdo público e indexado. Peça o ok explícito antes do primeiro push.
- O repositório precisa ser **público** e ter **exatamente o nome do usuário**. Se não existir:
  `gh repo create USUARIO/USUARIO --public` (com o ok).
- Commite só `README.md` e `assets/`. Nunca o `perfil.json` nem o `nao-citar.txt`.
- Depois do push, abra `https://github.com/USUARIO` deslogado (ou numa janela anônima) para ver
  o que um visitante vê.

### 7. Acabamento fora do README

Repositórios fixados, bio, site e empresa ficam fora do README. As regras e os comandos estão em
`references/github.md`. Em resumo: só dá para fixar repositório público seu ou em que você
contribuiu, e não há API para fixar (é pela tela).

## O que citar e o que não citar

Leia `references/o-que-citar.md` antes de escrever qualquer texto de case. As regras que mais
pesam:
- cliente sem autorização aparece pelo setor e pelo porte, e a combinação não pode identificar
  ("rede de academias com 12 unidades", não "a academia da avenida X");
- nada de nome de pessoa, incidente interno, valor de contrato, credencial, servidor ou URL interna;
- número só com fonte e data, separando medido de estimado; promessa do produto não é resultado;
- o papel da pessoa com precisão: "construí", "liderei", "participei do desenvolvimento".

## Design

O desenho, a ordem das seções, os limites de cada campo, os temas e como criar um tema a partir
das cores do site da pessoa estão em `references/estrutura.md`. Leia antes de escrever o
`perfil.json`. A regra de fundo: **um número grande por cartão, no máximo duas linhas de rótulo,
e o resto no bloco que abre**.

## Armadilhas

Antes de mexer no gerador ou de prometer algo à pessoa, leia `references/armadilhas.md`. As que
mais aparecem:
- os cartões de estatística públicos (github-readme-stats) só enxergam repositório público e podem
  mostrar números pífios para quem trabalha em código privado;
- commits automáticos (backup, sincronização) feitos com a identidade da pessoa inflam a contagem
  de contribuições; não cite a contagem sem conferir;
- alguns nomes do skillicons não existem (n8n, qdrant, openai, claude, ollama): use badge do
  shields.io para esses;
- cada bloco é uma imagem só, então os cartões não são clicáveis um a um: os links vão no bloco de
  detalhes e abaixo dos projetos abertos.

## Entrega

Ao terminar, diga à pessoa: o endereço do perfil, o que foi publicado, o que ficou fora e por quê
(nomes protegidos, números sem fonte), e o que só ela pode fazer (fixar, bio, foto).
