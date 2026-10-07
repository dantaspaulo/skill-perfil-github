# Armadilhas já pisadas

Cada item diz o sintoma, a causa e o que fazer.

## SVG no README
- **Fonte web não carrega.** SVG servido como `<img>` não busca nada de fora. Use pilha de sistema
  (`-apple-system, Segoe UI, Helvetica, Arial`) e Georgia para a serifada.
- **Texto não quebra linha.** `<text>` vai até onde precisar e sai do cartão. Quebre à mão (campos
  em lista) e deixe a conferência medir.
- **Degradê em linha horizontal some.** Com `gradientUnits` padrão (objectBoundingBox), uma linha
  reta tem altura zero e o traço não é desenhado. Use cor sólida em linhas retas.
- **Ids repetidos entre peças** fazem uma peça usar o recorte da outra. Prefixe ids por peça
  (`c` + prefixo).
- **Animação fora da tela não roda até aparecer.** Na captura de página inteira, o que está abaixo
  da dobra pode sair "vazio" (opacidade 0). Capture com janela alta ou role antes. No navegador do
  visitante isso é bom: a animação toca quando ele chega lá.
- **`transform` no CSS sobrescreve o atributo `transform`.** Para animar algo que já tem
  `transform` (como o brilho inclinado), anime um `<g>` em volta.
- **Emoji muda de desenho por sistema.** Apple, Windows e Android desenham diferente; escolha emoji
  que funcione nos três (evite os muito novos).

## Layout no GitHub
- **Cartões lado a lado com `width="49%"` ficam ilegíveis no celular.** Use um SVG por bloco e
  `<picture><source media="(max-width: 700px)" srcset="...-celular.svg">`. O GitHub respeita.
- **Uma imagem por bloco = sem link por cartão.** Ponha os links no bloco de detalhes e abaixo dos
  projetos abertos.
- **A API de Markdown no modo `gfm` transforma quebra de linha em `<br>`** (é o modo de
  comentários). Para prévia fiel ao README, use `mode=markdown`.
- **Badges em linhas separadas no código** aparecem lado a lado no README. Linha em branco entre
  eles quebra o grupo.
- **Tabelas HTML** ganham borda no tema do GitHub e vazam da tela no celular; os blocos em SVG
  evitam as duas coisas.

## Serviços de imagem
- **skillicons.dev** não tem todos os nomes. Sem ícone: `n8n`, `qdrant`, `openai`, `claude`,
  `ollama` (em 2026). Teste com `curl -s -o /dev/null -w '%{size_download}' 'https://skillicons.dev/icons?i=NOME'`:
  resposta muito pequena (~256 bytes) é erro. Para esses, badge do shields.io com `logo=` do
  simpleicons.
- **shields.io**: hífen e sublinhado no texto do badge se escrevem `--` e `__`. O script já faz.
  Alguns logos saíram do simpleicons (LinkedIn, por exemplo): o badge aparece sem ícone, o que é
  aceitável.
- **capsule-render e readme-typing-svg** são serviços de terceiros. Se caírem, o cabeçalho some; o
  resto do perfil (SVGs no repositório) continua.

## Conteúdo
- **Repetir número do site sem conferir.** Antes de copiar um número que já está publicado em outro
  lugar, confira a fonte de novo; erro replicado em dois lugares vira dois erros.
- **Somar casos diferentes num número só** ("agentes entregues com 600 testes", quando os 600 são de
  um cliente) é o tipo de exagero que cai numa pergunta. Diga de qual case é.
- **Link quebrado** para página de produto ou cliente: confira com
  `curl -s -o /dev/null -w '%{http_code}' -L URL` antes de publicar.
