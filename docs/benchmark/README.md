# Benchmark V2 de Snapshot Testing

## Objetivo

Este benchmark avaliará a capacidade de uma LLM de classificar diferenças encontradas em testes de snapshot de APIs REST e decidir se o snapshot aprovado deve ser atualizado.

## Estrutura real do projeto

- O catálogo exploratório está em `docs/snapshot_preliminar_dataset.md`.
- Os testes de snapshot estão em `src/test/java/com/example/pocapi/integration/`.
- Os snapshots aprovados (`*.approved.txt`) estão no mesmo diretório dos testes de integração.
- Quando uma verificação diverge, o ApprovalTests produz o arquivo `*.received.txt` junto ao respectivo `*.approved.txt`. No momento da preparação desta estrutura, não havia arquivos recebidos no repositório.
- O revisor experimental existente está em `scripts/snapshot_ai_review.py`; ele não faz parte desta mudança.

## Princípio experimental

O protocolo separa três papéis:

### Pesquisador

- define o caso experimental;
- define o Ground Truth;
- revisa a validade do caso.

### Agente de código

- implementa uma alteração especificada;
- trabalha sobre o código real;
- não decide o Ground Truth.

### LLM avaliada

- analisa exclusivamente as evidências produzidas pelo experimento;
- decide se o snapshot deve ou não ser atualizado.

## Fluxo

```text
baseline
   ↓
especificação do caso
   ↓
alteração real no código
   ↓
git diff
   ↓
execução dos testes
   ↓
falha real do ApprovalTests
   ↓
coleta de approved/received/test-output
   ↓
montagem do input da LLM
   ↓
classificação da LLM
   ↓
comparação com Ground Truth
```

Snapshots e resultados de testes não podem ser inventados por uma LLM. Eles devem ser obtidos pela execução real da aplicação e dos testes.

## Ground Truth

O Ground Truth admite exatamente dois valores:

- `SHOULD_UPDATE`: a diferença observada corresponde a uma alteração intencional e correta do comportamento esperado; portanto, o snapshot aprovado deveria ser atualizado.
- `SHOULD_NOT_UPDATE`: a diferença observada representa regressão, bug, comportamento indesejado ou outra situação em que atualizar o snapshot ocultaria um problema.

O Ground Truth pertence ao benchmark e nunca deve ser incluído no input enviado à LLM avaliada, direta ou indiretamente.

## Artefatos de um experimento executado

Após a execução, cada experimento deverá seguir aproximadamente esta convenção:

```text
experiments/
└── EXP-001/
    ├── metadata.json
    ├── patch.diff
    ├── approved.txt
    ├── received.txt
    ├── test-output.txt
    ├── llm-input.json
    ├── llm-output.json
    ├── ground-truth.json
    └── execution.json
```

O diretório acima é apenas uma convenção. Nenhum caso experimental é criado nesta etapa.

## Dataset preliminar

`../snapshot_preliminar_dataset.md` pertence à fase exploratória da pesquisa. Seus casos não constituem resultados experimentais finais, podem conter hipóteses ainda não reproduzidas e não devem ser usados automaticamente como Ground Truth do benchmark V2. O material poderá servir apenas como inspiração durante a elaboração manual e a revisão dos novos casos; seu conteúdo não foi copiado para o novo catálogo.
