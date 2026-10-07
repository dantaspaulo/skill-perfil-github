# O que fica fora do README: fixados, perfil e contagem

## O repositório de perfil
- Precisa ter **exatamente o nome do usuário** (`ana-exemplo/ana-exemplo`) e ser **público**.
- O GitHub mostra o `README.md` da raiz no topo do perfil. A pasta `assets/` pode ficar no mesmo
  repositório; caminhos relativos funcionam.
- Criar: `gh repo create USUARIO/USUARIO --public` (só com o ok da pessoa).

## Repositórios fixados (até 6)
- **Não há API** para fixar: é pela tela, em "Customize your pins", no próprio perfil.
- Só aparecem para escolher: repositórios **públicos** que a pessoa tem, ou em que **contribuiu**
  (commit no branch principal, pull request ou issue aberta). Repositório de outra pessoa sem
  contribuição não aparece, mesmo sendo público.
- Fixar repositório privado é possível, mas o visitante não vê. Não conte com isso.
- Fork aparece "forked from", e um fork sem mudança repete o original: prefira fixar o original
  quando houver contribuição nele.
- O `diagnostico` lista os candidatos: públicos próprios e públicos de terceiros com contribuição.
- Quer fixar o projeto de um amigo ou do empregador? A forma honesta é contribuir de verdade (um PR
  útil), não abrir issue vazia.

## Bio, site, empresa e local
- Bio: até 160 caracteres. Uma frase do posicionamento mais os papéis.
- Empresa: `@organizacao` vira link para a organização no GitHub.
- Editar: `github.com/settings/profile`, ou pelo `gh`:
  `gh api -X PATCH user -f bio='...' -f blog='https://...' -f company='...' -f location='...'`.
  Esse comando exige o escopo `user` no token (`gh auth refresh -h github.com -s user`, que abre o
  navegador). Sem o escopo, a API responde 404.

## Contribuições e o gráfico verde
- Visitante deslogado vê o total e "N contributions in private repositories", **sem o nome** dos
  repositórios privados. Quem tem acesso ao repositório vê o nome.
- Só conta commit cujo e-mail de autor está ligado à conta. Por isso **automação com a identidade
  da pessoa** (backup que commita a cada execução, sincronização, bot de dependências rodando com o
  token dela) infla a contagem, às vezes para centenas de milhares por ano.
- Antes de citar "N contribuições", rode o `diagnostico`: ele mostra quais repositórios concentram
  os commits e marca os que parecem automação. Se for o caso, não cite a contagem, e sugira à
  pessoa trocar o autor da automação para uma identidade própria (por exemplo
  `Robô de Backup <backup@dominio>`, e-mail que não esteja na conta). Isso para de contar daí para
  frente; o passado só sai reescrevendo histórico, o que não vale o risco.
- "Private contributions" pode ser desligado nas configurações do perfil, mas aí some também o
  trabalho real em privado. Raramente vale.

## Cartões de estatística de terceiros
- A instância pública do github-readme-stats só enxerga repositório **público**. Para quem trabalha
  em código privado, ela mostra "Total commits 50, stars 0", que diz o contrário do perfil. Só use
  se a pessoa tiver bastante código público, ou hospede a própria instância com um token.
- O mesmo vale para "top languages": reflete só o público.
