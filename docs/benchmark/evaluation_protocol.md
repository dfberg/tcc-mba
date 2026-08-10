# Protocolo operacional de avaliação por LLM — Benchmark V2

## 1. Identidade e escopo

Este documento é normativo para a rodada principal do Benchmark V2 identificada por `PROMPT_TEMPLATE_V1`. Ele governa a transformação de um EXP `VALIDATED` em estímulo, a chamada futura à LLM, a preservação das tentativas e a transição para `EVALUATED`.

Este protocolo foi definido antes da primeira avaliação por LLM. Ele não autoriza chamadas por si só e não contém credenciais, respostas experimentais ou Ground Truth.

O template normativo é `docs/benchmark/prompts/snapshot-review-v1.md`.

- Identificador: `PROMPT_TEMPLATE_V1`
- SHA-256: `85135355C8C1A22AEE5F693369538BED7C46E27AA106B9B933E3DC5E4B4E9A3C`
- Renderer: `scripts/render_snapshot_review_prompt.ps1`

Depois da primeira avaliação desta rodada, template, renderer, schemas aplicáveis e políticas deste documento ficam imutáveis. Qualquer alteração de estímulo ou execução exige `PROMPT_TEMPLATE_V2` e uma nova configuração/rodada, sem sobrescrever V1.

## 2. Separação de informações

### 2.1 Evidência experimental permitida

O renderer pode consumir exclusivamente:

- `gitDiff` integral;
- `expectedSnapshot` integral;
- `receivedSnapshot` integral;
- `testOutput` integral;
- `testName`;
- `endpoint`;
- `httpMethod`.

Esses valores são inseridos sem resumo, interpretação, reordenação interna ou enriquecimento.

### 2.2 Metadados administrativos

Identificadores de EXP/CASE, revisão, commits, timestamps internos, hashes, categoria, dificuldade, alcance e estado permanecem nos artefatos de rastreabilidade. Eles não fazem parte do estímulo consumido pela LLM.

O campo obrigatório `caseId` de `llm-input.schema.json` contém atualmente um identificador de execução no formato `EXP-NNN`; apesar do nome, seu valor é administrativo. O schema descreve o artefato interno completo, não o payload textual. O renderer não lê nem renderiza esse campo.

`ADMINISTRATIVE_IDS_SENT_TO_LLM: NO`

### 2.3 Informação reservada

Nunca enviar Ground Truth, justificativa do pesquisador, categoria, dificuldade, intenção, classificação esperada, indicação de mudança deliberada/correta/regressiva, outputs de outras LLMs ou métricas acumuladas.

Os tokens `SHOULD_UPDATE` e `SHOULD_NOT_UPDATE` aparecem apenas para definir neutralmente as duas alternativas possíveis; nenhuma delas é indicada como resposta esperada.

## 3. Renderer determinístico

O fluxo obrigatório é:

```text
llm-input.json
        ↓
render_snapshot_review_prompt.ps1
        ↓
rendered-prompt.txt
        ↓
LLM avaliada
```

O renderer carrega somente os sete campos permitidos, aplica substituição literal dos placeholders, rejeita evidência vazia e falha se restar placeholder. Ele exclui metadados administrativos, não interpreta o diff e não acessa Ground Truth.

Comando local de referência:

```powershell
./scripts/render_snapshot_review_prompt.ps1 `
  -InputPath docs/benchmark/experiments/EXP-001/llm-input.json `
  -TemplatePath docs/benchmark/prompts/snapshot-review-v1.md `
  -OutputPath docs/benchmark/experiments/EXP-001/rendered-prompt.txt
```

Cada avaliação deve preservar `rendered-prompt.txt` exatamente como enviado. Se a API separar mensagens system/developer/user, a estrutura e o conteúdo exato de cada mensagem devem ser preservados em forma reproduzível, sem segredos; nenhuma instrução adicional não congelada pode ser inserida.

## 4. Contrato da resposta

A resposta deve ser JSON estrito compatível com `docs/benchmark/schemas/llm-output.schema.json`, sem Markdown ou texto antes/depois:

- `shouldUpdateSnapshot`: booleano (`true` = `SHOULD_UPDATE`; `false` = `SHOULD_NOT_UPDATE`);
- `confidence`: inteiro de 0 a 100;
- `reason`: texto não vazio baseado nas evidências.

Não são permitidos campos adicionais. A confiança é autorrelatada, não modifica a classificação, não determina Ground Truth e será tratada apenas como medida secundária. A justificativa pode apoiar análise qualitativa futura, mas nunca revisão retrospectiva do Ground Truth.

## 5. Modelo e configuração

Nenhum modelo é escolhido implicitamente. Antes da primeira chamada de uma configuração, registrar em `execution.json`:

- `modelProvider` e `model`;
- versão/identificador retornado pelo provider, quando disponível;
- endpoint/API usada, sem credenciais;
- data/hora da avaliação;
- número da repetição e da tentativa;
- parâmetros explicitamente enviados;
- `temperature`, `top_p`, `seed`, limite de output, response format/structured output e configuração de reasoning, quando suportados;
- `PROVIDER_DEFAULT` para parâmetros relevantes omitidos ou não configuráveis;
- identificação `NOT_SUPPORTED` somente quando a API comprovadamente não oferecer o parâmetro.

Os dados específicos da avaliação ficam em `modelParameters`, incluindo `modelVersionIdentifier`, `apiEndpoint`, `evaluationTimestamp`, `repetition`, parâmetros de inferência e `technicalAttempts`. Os campos top-level `inputTokens` e `outputTokens` são registrados quando retornados. `execution.json` é a fonte de verdade para configuração e tentativa selecionada; respostas brutas e erros são evidências auxiliares referenciadas por ele.

Nunca persistir API keys, headers de autorização, tokens secretos, credenciais, cookies ou valores equivalentes.

## 6. Repetição e retry

### 6.1 Rodada principal

A análise principal usa exatamente `1 execução válida por EXP por configuração de modelo`. Essa quantidade não pode mudar após observar resultados individuais.

Estudos com 3, 5 ou N repetições constituem outra rodada/protocolo e não podem ser adicionados seletivamente a casos difíceis da rodada principal.

### 6.2 Retry técnico

Uma tentativa inicial admite no máximo 2 retries técnicos, totalizando 3 tentativas. Retry só é permitido para:

- `TIMEOUT`;
- `API_ERROR` transitório;
- `RATE_LIMIT`;
- falha de conexão;
- `EMPTY_RESPONSE`;
- `INVALID_JSON`;
- `SCHEMA_INVALID`.

Uma resposta JSON válida e compatível com o schema recebe `VALID_RESPONSE` e encerra as tentativas. É proibido repetir por classificação aparentemente errada, baixa confiança, razão fraca ou divergência do Ground Truth.

Estados normativos de tentativa: `VALID_RESPONSE`, `INVALID_JSON`, `SCHEMA_INVALID`, `API_ERROR`, `TIMEOUT`, `RATE_LIMIT`, `EMPTY_RESPONSE`.

Todas as tentativas são preservadas em ordem. Para cada tentativa, registrar timestamp, estado, código HTTP quando houver, erro técnico e referência à resposta bruta. A primeira resposta válida é a única observação experimental; nenhuma tentativa posterior pode ocorrer.

## 7. Artefatos e integridade

Para cada EXP avaliado, preservar:

- `llm-input.json`;
- `rendered-prompt.txt`;
- `llm-output.json` após resposta válida;
- `execution.json` atualizado como fonte normativa da execução técnica e da avaliação;
- respostas brutas/erros por tentativa, quando existirem, em diretório append-only `attempts/attempt-NN/`.

Structured output que já retorne exatamente o JSON final pode dispensar duplicação entre resposta bruta e parseada, desde que isso seja documentado em `execution.json`. Normalização nunca pode alterar classificação, confiança ou razão.

Calcular e registrar SHA-256 de `llm-input.json`, `rendered-prompt.txt`, `llm-output.json`, `patch.diff`, `approved.txt` e `received.txt`. Não editar esses artefatos depois de seus hashes serem associados à avaliação.

## 8. Transição VALIDATED → EVALUATED

Um EXP só entra em `EVALUATED` quando todos forem verdadeiros:

1. estado anterior `VALIDATED`;
2. `llm-input.json` válido no schema;
3. auditoria de leakage aprovada;
4. prompt renderizado com `PROMPT_TEMPLATE_V1` e hash conferido;
5. provider, model, identificação e configuração registrados;
6. resposta válida obtida sob a política de retry;
7. primeira resposta válida e tentativas anteriores preservadas;
8. `llm-output.json` válido no schema;
9. hashes críticos registrados.

A transição ocorre imediatamente após persistir e validar a primeira resposta experimental válida. Falhar todas as três tentativas técnicas não produz `EVALUATED`; o EXP permanece `VALIDATED` com tentativas preservadas.

## 9. Isolamento do Ground Truth e análise posterior

Ordem obrigatória:

```text
evidência → renderizar → LLM → persistir resposta → validar → congelar output
          → carregar Ground Truth → calcular análise
```

Ground Truth não pode ser carregado pelo renderer nem pelo componente de chamada. Métricas só podem ser calculadas sobre outputs congelados. A análise futura pode incluir accuracy, precision/recall/F1 por classe, matriz de confusão, categoria, dificuldade, confiança e pares contrastivos.

Os pares CASE-007/CASE-008, CASE-013/CASE-014 e CASE-025/CASE-026 devem usar exatamente o mesmo template, renderer, modelo/configuração e política; não recebem prompts especiais.

## 10. Checklist por EXP

```text
[ ] EXP está VALIDATED
[ ] llm-input válido
[ ] leakage audit passou
[ ] template = PROMPT_TEMPLATE_V1
[ ] prompt hash conferido
[ ] rendered prompt preservado
[ ] provider/model registrados
[ ] parâmetros registrados
[ ] nenhuma informação reservada enviada
[ ] chamada executada
[ ] tentativa registrada
[ ] primeira resposta válida preservada
[ ] llm-output validado
[ ] output hash calculado
[ ] somente depois Ground Truth carregado
[ ] EXP marcado EVALUATED
```

## 11. Ensaio local pré-avaliação

O EXP-001 foi renderizado localmente duas vezes, sem chamada de rede ou LLM.

- SHA-256 de `rendered-prompt.txt`: `013A7EBAC85A7CE3ECFBA871BB2B990BAB6B36516D68CCCCB9FAD21802CD4EE9`
- `PROMPT_RENDERING_DETERMINISTIC: YES`
- `RENDERED_PROMPT_LEAKAGE: NO`
- IDs administrativos enviados: NÃO

Os rótulos `SHOULD_UPDATE` e `SHOULD_NOT_UPDATE` aparecem apenas nas instruções fixas como alternativas neutras.

## 12. Candidatos ao congelamento

O futuro `executionProtocolFreezeCommit` deve incluir, no mínimo:

- este protocolo;
- `snapshot-review-v1.md`;
- o renderer local;
- `llm-input.schema.json`;
- `llm-output.schema.json`;
- `execution.schema.json`;
- `experiment-metadata.schema.json`;
- `change_control.md` com o registro pré-avaliação;
- `.gitattributes` com preservação byte a byte das evidências experimentais;
- o ensaio renderizado de EXP-001 e seus artefatos já validados.

O commit e eventual tag só podem ser criados após revisão humana. Esta tarefa não cria commit nem executa LLM.
