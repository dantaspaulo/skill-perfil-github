# Skill perfil-github

Uma skill para o Claude montar o seu perfil do GitHub com cara de portfólio: cartões animados com
os seus cases (problema, solução e resultado), números com fonte, papéis atuais, método de trabalho,
projetos abertos e stack, com versão própria para celular.

O Claude primeiro lê o que já é público (seu perfil, seu site, seu LinkedIn), depois pergunta só o
que falta, em poucas rodadas. Cliente que não autorizou o nome entra pelo setor, e uma trava recusa
publicar se o nome escapar em algum arquivo. Nada vai ao ar sem você ver a prévia e dizer que pode.

## Instalar

**Claude Code:** copie esta pasta para `~/.claude/skills/perfil-github/` (ou para
`.claude/skills/` dentro de um projeto). Abra o Claude Code de novo.

**Claude.ai / app:** em Configurações → Capacidades → Skills, envie o arquivo `.skill` (ou o `.zip`
desta pasta).

## Usar

Peça com as suas palavras, por exemplo:
- "deixa meu perfil do GitHub com cara de portfólio, meu usuário é fulano"
- "quero colocar meus cases no GitHub sem citar os clientes"
- "alinha meu GitHub com meu site novo"

## O que precisa ter na máquina

- `python3` e `git`;
- `gh` (GitHub CLI) logado, opcional: com ele o Claude faz o diagnóstico do perfil e a prévia
  exatamente como o GitHub renderiza;
- Playwright, opcional, para capturar a prévia no tamanho de computador e de celular.

## Onde ficam os seus dados

O `perfil.json` (seus textos) e o `nao-citar.txt` (nomes que não podem sair) ficam numa pasta de
trabalho **fora** do repositório público. No repositório vão só o `README.md` e a pasta `assets/`.
