# Catálogo de casos do benchmark V2

Este arquivo define a estrutura do catálogo. Ainda não contém casos experimentais.

Cada caso planejado possuirá:

- ID;
- categoria;
- objetivo;
- endpoint alvo;
- método HTTP;
- arquivos candidatos;
- descrição da alteração;
- dificuldade;
- Ground Truth;
- justificativa do Ground Truth;
- status de implementação;
- status de validação.

## Categorias iniciais

- `CONTRACT_EVOLUTION`
- `BREAKING_CHANGE`
- `BUSINESS_RULE`
- `HTTP`
- `SERIALIZATION`
- `ERROR_HANDLING`
- `COLLECTION`
- `NON_DETERMINISTIC`
- `NOISE`
- `BUG`

## Status

Os únicos valores de status são:

- `PLANNED`
- `IMPLEMENTED`
- `EXECUTED`
- `VALIDATED`
- `REJECTED`

## Ground Truth

O Ground Truth aceita somente:

- `SHOULD_UPDATE`: a diferença observada corresponde a uma alteração intencional e correta do comportamento esperado; o snapshot aprovado deveria ser atualizado.
- `SHOULD_NOT_UPDATE`: a diferença representa regressão, bug, comportamento indesejado ou outra situação em que atualizar o snapshot ocultaria um problema.

Não existem valores intermediários. O Ground Truth é definido e justificado pelo pesquisador, pertence ao benchmark e não pode aparecer no input fornecido à LLM avaliada.

O catálogo exploratório `../snapshot_preliminar_dataset.md` não é fonte de verdade deste dataset. Seus casos não são resultados finais, podem conter hipóteses ainda não reproduzidas e não podem ser convertidos automaticamente em casos ou Ground Truth. Eles poderão apenas inspirar a elaboração manual e a revisão futura.

## Casos

Nenhum caso definido nesta etapa.
