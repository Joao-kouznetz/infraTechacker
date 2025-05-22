# Configurando as informações importantes do repositório

## Permissão de codigo em produção

Como A branch main estará concetada com servidor de produção não é interessante que seja possível dar commits diretamente na branch main e a unica forma possível é quando se faz um pull request e ele seja aprovado. Então para isso alteraremos a seguinte configuração do repositório no Github:

Settings -> Rules -> Rulessets -> New rule set

nesse rul set selecione branch targeting criteria -> add target -> include by patter  e escreva main

em seguinda colocoque "require a pull request before merging"

## Confirando Branch Docs para documentação

- Criar branch Docs
- No settings -> pages colocar Deploy from branch selecione a Docs e coloque para ser no root e salve a alteração. Agora toda a vez que voce rodar os comandos abaixo sera salvo a nova forma de documentação.

```bash
mkdocs build
```

## Publicando no git hub -pages

```zsh
mkdocs gh-deploy --remote-branch Docs
```
