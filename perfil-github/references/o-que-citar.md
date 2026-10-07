# O que citar e o que não citar

Um perfil público fica indexado, em cache e copiado por terceiros. Apagar depois não desfaz. Por
isso a regra de fundo é: na dúvida, não sai, ou sai mais genérico, e pergunte.

## Pode citar

- Produto ou empresa da própria pessoa.
- Marca de cliente ou empregador **que autorizou** (por escrito, de preferência). Se o nome já está
  publicado com autorização em outro lugar (site da pessoa, case no site do cliente), vale.
- Contribuição em código aberto: é pública por natureza.
- Números com fonte e data.
- Tecnologias usadas de verdade.

## Não cite

- Nome de cliente sem autorização, nem nome de pessoa (cliente, colega, vendedor, usuário).
- Incidente, falha, vazamento, problema interno, mesmo que resolvido.
- Valor de contrato, preço cobrado, faturamento de cliente.
- Credencial, token, nome de servidor, IP, URL interna, nome de repositório privado.
- Detalhe de segurança do sistema do cliente (onde fica o servidor, que porta, que proteção).
- Número que a pessoa não consegue mostrar de onde veio.

## Anonimizar sem identificar: o teste do concorrente

Descreva o cliente por **setor + porte + abrangência**: "rede de academias com 12 unidades",
"SaaS B2B da área de RH", "escritório contábil de médio porte".

Depois aplique o teste: *alguém do mesmo mercado reconheceria o cliente por esta descrição?*
Combinações raras identificam ("a única rede de pet shops 24 horas da capital"). Se reconheceria,
generalize mais (tire a região, arredonde o número) ou peça autorização.

O nome real vai para o `nao-citar.txt`, e a conferência recusa a publicação se ele aparecer em
qualquer arquivo. Ponha também variações (sigla, nome fantasia, nome do produto do cliente, nome
do agente ou do robô que você criou para ele, se ele tiver nome próprio).

## Números: a regra da procedência

Todo número precisa de três coisas: **o que mede, de onde vem, de quando**. Guarde no campo
`fonte` do `perfil.json`; o resumo das fontes aparece no bloco de detalhes.

- **Medido ≠ estimado.** "Caiu de 40 para 8 minutos em ensaio" é honesto; "caiu 80%" sem dizer que
  foi ensaio não é.
- **Estimativa da própria pessoa** ("acho que economizei 2 mil horas") não vai no número grande nem
  na faixa de números. Se ela quiser muito, entra no texto do case que a sustenta, dita como
  estimativa ("estimamos cerca de..."), ou fica de fora. Pergunte qual das duas ela prefere.
- **Promessa do produto não é resultado.** "Relatório pronto em um clique" é o que o produto promete;
  vai na solução, não no número grande.
- **Contagem de vaidade** (contribuições, commits, linhas de código) só depois de conferir que não
  é inflada por automação. Ver `github.md`.
- **Arredonde para baixo** e use "+" ("1 mi+"). Número exato demais parece inventado; inflado
  demais derruba a credibilidade na primeira pergunta.
- Conferiu e o número não se sustenta? Tire. Um case sem número com um papel bem descrito vale mais
  que um número que não aguenta uma pergunta.

## O papel, com o verbo certo

Recrutador e cliente leem o verbo. Use o que aconteceu:
- **fundei / construí do zero**: a pessoa fez o todo;
- **liderei**: conduziu o time ou o projeto;
- **participei do desenvolvimento / atuei em**: fez parte;
- **pela empresa X**: o trabalho foi feito por meio de um empregador ou parceiro.

Quando o trabalho foi por uma empresa, diga qual ("pela consultoria X") se ela autorizou; se não,
"por uma consultoria parceira".

## Tom

Frases curtas, voz ativa, sem adjetivo vazio ("inovador", "revolucionário", "de ponta"). O número e
o problema fazem o trabalho. Problema na língua do negócio ("o lead esperava horas"), não da
tecnologia ("faltava um pipeline").
