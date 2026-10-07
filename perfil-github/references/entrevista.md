# Entrevista: o que perguntar, em que ordem e como

O objetivo é sair com um `perfil.json` completo fazendo a pessoa pensar o mínimo. Ela sabe o que
fez; quase nunca sabe como contar. Seu papel é trazer rascunhos e deixar a pessoa corrigir.

## Antes de perguntar

Junte o que já está público (passo 1 da skill): perfil do GitHub, README atual, site, LinkedIn,
currículo. Daí costumam sair o nome, a frase de posicionamento, os papéis, os contatos e boa parte
dos projetos. Pergunte só o que faltar e diga de onde tirou o resto ("peguei a frase do seu site").

## Regras da conversa

- **Rascunho, não pergunta aberta.** "Qual é seu posicionamento?" trava qualquer um. "Pelo seu
  site, sugiro: *automatiza operações com IA*. Serve, ou prefere outra ênfase?" anda.
- **Rodadas curtas.** Até 4 perguntas por rodada, agrupadas. No máximo 3 rodadas antes da primeira
  prévia; o resto se ajusta vendo o resultado.
- **Escolha fechada quando der.** Tema, seções opcionais e sim ou não vão em `AskUserQuestion` (se
  existir), com a opção recomendada primeiro.
- **"Não sei" é resposta válida.** Número sem fonte fica de fora; case sem resultado medido entra
  com "Meu papel" no lugar de "Resultado". Não invente para preencher.
- **Confirme a interpretação** quando a resposta for vaga ("participei" pode ser liderar ou ter
  feito uma parte; pergunte qual).

## Rodada 1: quem é e para quem fala

1. **Para quem é o perfil?** Recrutador, cliente que contrata, comunidade técnica. Isso decide o
   tom do convite final e quais números aparecem primeiro.
2. **Frase de efeito** (aparece no topo, até ~40 caracteres) e **pitch** (1 ou 2 frases). Traga 2
   ou 3 opções tiradas do que já leu.
3. **Papéis atuais** (2 a 4): onde trabalha, empresa própria, mentoria, comunidade. Cada um com um
   complemento curto ("3 clientes ativos", "time de plataforma").
4. **Contatos**: site, LinkedIn, e-mail, agenda, cidade. Pergunte se quer o e-mail público.

## Rodada 2: as provas

5. **Números do topo** (2 a 4). Para cada um: o valor, o que mede e **de onde vem e de quando**
   (painel, fatura, relatório do cliente, contagem própria). Sem fonte, não entra.
6. **Cases** (2 a 8; par fica melhor na grade). Para cada um, em ordem:
   - **O nome pode aparecer?** Produto próprio, empresa que autorizou, ou cliente sem autorização.
     Sem autorização: combine com a pessoa o setor e o porte que vão aparecer e ponha o nome no
     `nao-citar.txt`. Confira com ela o "teste do concorrente" (ver `o-que-citar.md`).
   - **Problema** em uma frase: o que travava antes, na língua do negócio.
   - **Solução**: o que foi construído, sem jargão desnecessário.
   - **Resultado**: um número com fonte e data. Se não houver, use o papel.
   - **Papel da pessoa**, com o verbo certo.
   - **Link público**, se houver.
   Depois disso, **você** escreve o cartão (número grande, 2 linhas de rótulo, rodapé) e mostra.
7. **Código aberto** (até 3): repositórios próprios ou em que contribuiu. O diagnóstico já lista os
   candidatos; pergunte quais valem e o que dizer de cada um.

## Rodada 3: o visual

8. **Tema**: `champagne` (escuro com dourado), `esmeralda` (verde), `oceano` (azul) ou `grafite`
   (preto e branco). Se a pessoa tiver site com cor própria, ofereça um tema a partir dele (ver
   `estrutura.md`).
9. **Seções opcionais**: método de trabalho (3 a 5 passos) e princípios (3 a 6 ícones). Só entram se
   a pessoa tiver algo a dizer; não são obrigatórias.
10. **Stack**: tecnologias que usa de verdade, em produção. Menos e verdadeiro vale mais.

## Ao fim da entrevista

Mostre o `perfil.json` resumido em texto (não o JSON cru, para quem não é técnico) e confirme os
pontos sensíveis: o que vai pelo setor, os números e as fontes, o papel em cada case. Depois monte
e mostre a prévia. Ajuste fino se faz em cima da prévia, não da entrevista.
