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

### 6.3 Continuidade do batch após falha técnica terminal

Esta regra aplica-se à rodada principal em ordem fixa e a cada EXP/configuração independentemente. Depois da tentativa inicial e de, no máximo, dois retries técnicos permitidos, um EXP sem resposta localmente válida recebe o outcome `TECHNICAL_FAILURE_NO_VALID_RESPONSE`. Suas attempts já preservadas permanecem fatos append-only; não é criado `llm-output.json`, não se carrega Ground Truth, e não se calcula `MATCH` ou `MISMATCH` para esse EXP.

O batch deve então `CONTINUE_TO_NEXT_ELIGIBLE_EXPERIMENT`, preservando a ordem fixa. A falha encerra somente a avaliação daquele EXP/configuração. Não são permitidos quarto attempt, reexecução posterior para completar o dataset, compensação por chamadas extras em outro EXP, alteração de configuração, modelo, prompt, ordem, seed ou timing. A resposta válida máxima continua sendo uma por EXP/configuração; a primeira resposta válida encerra as tentativas e segue para a Phase B normal.

As contagens futuras distinguem `ELIGIBLE_EXPERIMENTS`, `VALID_LLM_RESPONSES`, `TECHNICAL_FAILURES_NO_VALID_RESPONSE`, `MATCHES` e `MISMATCHES`. A regra é independente de Ground Truth, categoria, dificuldade, intenção, pares contrastivos e qualquer resultado observado.

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

### 11.1 Identidade do template e do prompt renderizado

`PROMPT_TEMPLATE_V1` é exclusivamente o arquivo `docs/benchmark/prompts/snapshot-review-v1.md`, congelado no `executionProtocolFreezeCommit` (`2beba4d26d7836c951c1f0601483b96acfd10c8a`). O SHA-256 autoritativo do arquivo-template é `85135355C8C1A22AEE5F693369538BED7C46E27AA106B9B933E3DC5E4B4E9A3C`.

O SHA-256 `013A7EBAC85A7CE3ECFBA871BB2B990BAB6B36516D68CCCCB9FAD21802CD4EE9` registrado acima identifica o `rendered-prompt.txt` específico de EXP-001, obtido pela substituição literal do template pelo `llm-input.json` daquele EXP; ele não identifica o arquivo-template. Portanto, `PROMPT_TEMPLATE_SHA != RENDERED_PROMPT_SHA` quando o prompt contém evidência do EXP. Cada `rendered-prompt.txt` congelado é `BYTE_IMMUTABLE_EVIDENCE` e é a entrada direta da inferência: nenhuma rerenderização em runtime o substitui.

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

## 13. Execução técnica repetida para evidência variável

Esta seção aplica-se exclusivamente a CASEs que exijam explicitamente `repeated technical execution`. Ela regula a coleta técnica anterior à renderização e não altera o protocolo de inferência LLM.

- `REPEATED_TECHNICAL_EXECUTION_COUNT = 3`.
- Os índices fixos são `RUN-01`, `RUN-02` e `RUN-03`.
- As três execuções usam a mesma mutação e o mesmo contexto técnico, sem alteração intermediária de código.
- Cada execução é independente e preservada em `technical-runs/RUN-NN/received.txt` e `technical-runs/RUN-NN/test-output.txt`.
- `technical-runs-manifest.json`, validado por `schemas/technical-runs-manifest.schema.json`, registra versão do protocolo, quantidade planejada, execução selecionada, IDs, status técnico e hashes SHA-256.
- Ground Truth, categoria, dificuldade, interpretação, decisão esperada e dados LLM são proibidos no manifest e nos diretórios de runs.

### 13.1 Seleção definida a priori

`LLM_STIMULUS_RUN = RUN-01`. Somente os bytes de `RUN-01/received.txt` e `RUN-01/test-output.txt` alimentam os artefatos centrais `received.txt`, `test-output.txt`, `llm-input.json` e `rendered-prompt.txt`. A correspondência dos arquivos centrais com RUN-01 deve ser validada byte a byte e por SHA-256.

Uma execução é tecnicamente válida somente quando parte do baseline correto, aplica a mutação prescrita, executa o contexto correto, alcança o mecanismo experimental esperado e produz os artefatos necessários sem falha de infraestrutura ou setup. A validade independe do conteúdo recebido, Ground Truth ou decisão esperada. Se RUN-01 sofrer falha infraestrutural, RUN-02 não é promovida: o EXP passa a `REQUIRES_REVIEW` e a ocorrência é preservada.

RUN-02 e RUN-03 servem somente à caracterização da variabilidade. Não substituem RUN-01, não alteram o estímulo e não produzem inferências adicionais. `LLM_INFERENCES_PER_EXPERIMENT = 1`; execuções técnicas repetidas não são repetições LLM.

`VARIABILITY_OBSERVED = YES` quando pelo menos duas execuções técnicas válidas possuem `received.txt` byte-diferentes, comprovados por SHA-256. A observação não altera `selectedRun`.

### 13.2 Proibição de amostragem adaptativa

São proibidos early stopping, executar até surgir determinada saída, alterar N após resultados, repetir por igualdade ou diferença das três saídas, descartar outliers, majority vote, resultado modal, selecionar proximidade ou distância do approved e qualquer seleção baseada em Ground Truth. A seleção nunca depende do resultado observado.

## 14. Preconditionamento explícito de fixture e janela de observação primária

Esta seção aplica-se quando a execução isolada do teste primário não reproduz o snapshot approved congelado porque o estado baseline depende de fixture, sequence, identity ou outras ações técnicas anteriores. A regra foi definida depois da observação de resultados técnicos de EXP-019 e EXP-020, mas antes de qualquer resultado LLM para esses EXPs.

### 14.1 Definição e seleção

`PRECONDITIONING` é a execução mínima e determinística das ações técnicas necessárias para colocar o sistema no estado em que o snapshot approved congelado é legitimamente reproduzível.

- `PRECONDITIONING_PURPOSE = REPRODUCE_FROZEN_BASELINE_STATE`.
- `PRECONDITIONING_SELECTION_RULE = MINIMUM_BASELINE_STATE_REPRODUCTION`.
- A seleção deve ser demonstrável exclusivamente a partir do setup da suíte, fixtures, sequences, estado do banco, approved congelado e comportamento baseline.
- São proibidos testes ou passos extras por conveniência.
- O preconditionamento não integra a mutação e não altera CASE, Ground Truth ou snapshot approved.
- A seleção não pode usar o received mutado, resultado ou classificação LLM, categoria, dificuldade ou intenção administrativa.
- `PRECONDITIONING_STEPS_FIXED_BEFORE_MUTATION = YES`.
- `PRECONDITIONING_DEPENDS_ON_MUTATED_OUTPUT = NO`.
- `ARTIFICIAL_ID_FORCING_ALLOWED = NO`.
- `SNAPSHOT_EDITING_ALLOWED = NO`.

O objetivo é reproduzir, por consequência do fluxo real, o mesmo estado observável relevante ao teste primário. Quando aplicável, entidades criadas, sequence/identity state, IDs esperados e demais fatos de fixture devem ser registrados no manifest.

### 14.2 Fases e janelas de captura

O fluxo possui duas fases normativas separadas no momento da execução:

```text
PHASE P — PRECONDITIONING
    constrói o estado baseline mínimo
    preserva transcript próprio
    não alimenta o estímulo LLM
              ↓
PHASE O — PRIMARY OBSERVATION
    inicia depois do preconditionamento bem-sucedido
    executa o teste primário oficial
    produz received e test-output centrais
```

- `PRIMARY_LLM_EVIDENCE_SOURCE = PRIMARY_OBSERVATION_ONLY`.
- PHASE P pode executar setup ou testes necessários, mas seu transcript não é `test-output.txt` central.
- PHASE O é a única janela que produz o `testOutput` usado em `llm-input.json` e `rendered-prompt.txt`.
- É proibido fazer uma captura ampla e remover posteriormente trechos de setup ou collateral: `POST_HOC_LOG_FILTERING_ALLOWED = NO`.
- Os transcripts de PHASE P e PHASE O devem ser capturados separadamente desde o início de cada fase.

### 14.3 Preservação e manifest

O preconditionamento deve ser preservado integralmente em:

```text
EXP-NNN/
  precondition/
    manifest.json
    test-output.txt
```

`precondition/manifest.json` deve validar contra `schemas/precondition-manifest.schema.json`. Ele registra somente fatos verificáveis: EXP, versão do protocolo, propósito, passos/comandos, estado baseline esperado, exit code, timestamp, SHA-256 do transcript, teste primário selecionado e confirmação de exclusão do input LLM.

Ground Truth, classificação esperada, categoria, dificuldade, interpretação e dados LLM são proibidos no manifest e no transcript.

### 14.4 Gates baseline e equivalência

- `PRECONDITIONING_SUCCESS_REQUIRED = YES`.
- `PRIMARY_BASELINE_PASS_REQUIRED_AFTER_PRECONDITIONING = YES`.
- O preconditionamento apenas prepara o estado; ele não substitui a observação baseline primária nem autoriza aceitar mismatch.
- Os mesmos passos de PHASE P devem ser usados no baseline e na execução mutada.
- Exceção exige impossibilidade técnica objetiva definida e registrada antes da mutação; nunca pode decorrer do received mutado.

Fluxo normativo futuro:

1. restaurar o baseline congelado;
2. executar PHASE P e preservar seu transcript/manifest;
3. iniciar PHASE O baseline e confirmar que o approved passa;
4. restaurar e preparar novamente estado equivalente;
5. aplicar exclusivamente a mutação do CASE;
6. executar PHASE P mutada com os mesmos passos fixados;
7. iniciar PHASE O mutada e preservar `received.txt` e `test-output.txt` centrais;
8. executar collateral separadamente;
9. preservar collateral fora do estímulo LLM.

### 14.5 Conjuntos de evidência e collateral

`TECHNICAL_EVIDENCE_SET` pode conter evidência de preconditionamento, observação primária e collateral. `LLM_EVIDENCE_SET` contém somente a evidência primária permitida produzida em PHASE O. São conjuntos normativos distintos, produzidos em janelas distintas; essa separação não é truncamento nem edição de log.

Se um passo de preconditionamento também corresponder a um teste collateral, seu output permanece evidência de preconditionamento e/ou collateral, nunca evidência LLM primária.

- `PRECONDITION_METADATA_SENT_TO_LLM = NO`.
- `PRECONDITION_COLLATERAL_OUTPUT_SENT_TO_LLM = NO`.
- `COLLATERAL_EVIDENCE_REQUIRED_IN_LLM_INPUT = NO`.

O `llm-input.json` não inclui transcript, manifest ou comandos de preconditionamento, collateral, indicação de que outro teste ocorreu antes, alcance `MULTIPLE_SNAPSHOTS` ou qualquer informação reservada.

### 14.6 Sucesso da PHASE P e exit code do processo

O sucesso do processo e o sucesso do estado de preconditionamento são fatos distintos. `exitCode == 0` caracteriza `SUCCESS_EXIT` e permite `PRECONDITION_SUCCESS`, desde que os demais requisitos desta seção sejam satisfeitos. Um exit code diferente de zero não constitui sucesso genérico: `NONZERO_EXIT_IS_GENERIC_SUCCESS = NO`.

Uma PHASE P com `exitCode != 0` somente recebe `PRECONDITION_SUCCESS` quando, conjuntamente:

1. o transcript integral demonstra que todas as ações necessárias à construção do estado foram concluídas antes da falha: `PRECONDITION_STATE_CONSTRUCTION_CONFIRMED = YES`;
2. a falha é classificada como `POST_STATE_ASSERTION_FAILURE`, ocorre estritamente depois da construção do estado e não invalida seus efeitos;
3. o transcript integral, sem recorte, edição ou normalização destinada a ocultar a falha, está preservado: `PRECONDITION_TRANSCRIPT_PRESERVED = YES`;
4. em nova invocação, a PHASE O baseline usa o estado produzido, executa o teste primário sem mutação, passa, reproduz o approved congelado e os valores relevantes: `PRIMARY_BASELINE_PASS_AFTER_PRECONDITIONING = REQUIRED`;
5. `PRECONDITIONING_STEPS_FIXED_BEFORE_MUTATION = YES`;
6. `PRECONDITIONING_DEPENDS_ON_MUTATED_OUTPUT = NO`.

Formalmente:

```text
PRECONDITION_SUCCESS =
    (exitCode == 0)
    OR
    (
      exitCode != 0
      AND stateConstructionConfirmed == true
      AND failureClassification == POST_STATE_ASSERTION_FAILURE
      AND preconditionTranscriptPreserved == true
      AND primaryBaselinePassAfterPreconditioning == true
      AND preconditioningStepsFixedBeforeMutation == true
      AND dependsOnMutatedOutput == false
    )
```

A PHASE O baseline aprovada não apaga nem reclassifica o exit code factual; ela comprova independentemente a construção do estado. O manifest sempre preserva o valor real: `PRECONDITION_EXIT_CODE_PRESERVED_FACTUALLY = YES`.

As classificações mínimas de término da PHASE P são:

- `SUCCESS_EXIT`: processo encerrado com exit code zero;
- `POST_STATE_ASSERTION_FAILURE`: depois de o estado estar integralmente construído, uma asserção de snapshot falha sem invalidar seus efeitos;
- `PRE_STATE_FAILURE`: falha anterior ao início da construção necessária;
- `STATE_CONSTRUCTION_FAILURE`: falha durante ou ao persistir a construção, deixando-a incompleta ou incerta;
- `INFRASTRUCTURE_FAILURE`: falha de compilação, startup, conexão, fixture, timeout ou infraestrutura que impeça comprovar a construção.

Somente `POST_STATE_ASSERTION_FAILURE` pode ser compatível com `PRECONDITION_SUCCESS` não-zero e apenas com todos os gates conjuntivos acima. Para `PRE_STATE_FAILURE`, `STATE_CONSTRUCTION_FAILURE` e `INFRASTRUCTURE_FAILURE`, `PRECONDITION_SUCCESS = NO`. A regra é geral para qualquer EXP com preconditionamento explícito e não depende de CASE, Ground Truth, received mutado ou resultado LLM.

## 15. Manifest de evidências collateral

Collateral evidence existe quando a mutação afeta um ou mais snapshots adicionais além do snapshot primário. Ela pertence exclusivamente ao `TECHNICAL_EVIDENCE_SET` e não pertence ao `LLM_EVIDENCE_SET`. Permanece obrigatória a regra `COLLATERAL_EVIDENCE_REQUIRED_IN_LLM_INPUT = NO`.

Quando ao menos um collateral for observado, o EXP deve preservar `collateral-manifest.json`, validado por `schemas/collateral-manifest.schema.json`. Quando nenhum collateral for observado, o manifest não é criado e nenhuma evidência collateral artificial é adicionada. Por isso, um manifest existente contém no mínimo uma entrada.

O manifest registra somente fatos verificáveis: EXP, versão do protocolo, quantidade de collaterals, identificação técnica de cada teste e snapshot, paths relativos dos artefatos approved, received e test-output, seus hashes SHA-256, preservação integral e exclusão do input LLM. `collateralCount` deve ser igual à quantidade de entradas em `collaterals`; essa igualdade é um gate do produtor e da validação metodológica, além das restrições estruturais do schema.

Paths absolutos, travessia por `..`, Ground Truth, categoria, dificuldade, intenção, justificativa semântica, classificação esperada, scoring, `MATCH` e `MISMATCH` são proibidos. O valor de `includedInLlmInput` é sempre `false`.

Antes de um EXP alcançar `VALIDATED` ou ser congelado, seu manifest collateral deve passar no schema, a contagem deve conferir com as entradas, cada path deve resolver dentro do EXP, os três hashes devem corresponder aos bytes preservados e a exclusão do `llm-input.json` e do prompt deve ser confirmada.

## 16. Representação Git no stage e identidade da evidência

Esta seção regula a representação versionada de artefatos durante o stage e freeze. Ela não autoriza alterar artefatos experimentais, `.gitattributes`, schemas, CASEs, Ground Truth ou estímulos para satisfazer um gate.

### 16.1 Classes normativas

`BYTE_IMMUTABLE_EVIDENCE` é evidência cujo valor científico depende dos bytes exatamente capturados e previamente validados. Inclui `patch.diff`, `approved.txt`, `received.txt`, `test-output.txt`, `llm-input.json`, `rendered-prompt.txt`, transcripts de preconditionamento, evidência collateral approved/received/test-output, technical runs e respostas brutas ou outputs de LLM. Para essa classe, `STAGED_BLOB_BYTES == EXPECTED_EVIDENCE_BYTES` é obrigatório. Qualquer alteração produzida por filtro Git bloqueia o freeze.

`CANONICALIZABLE_TEXT_METADATA` é texto estruturado cujo valor normativo é o conteúdo factual e sua estrutura validada, não a escolha física de EOL. Inclui `metadata.json`, `execution.json`, `ground-truth.json`, `precondition/manifest.json`, `collateral-manifest.json` e `technical-runs-manifest.json`. Um arquivo JSON não entra automaticamente nessa classe: deve exercer papel de metadado estruturado e não de estímulo, transcript, snapshot, patch ou output bruto.

`ground-truth.json` é metadata estruturada reservada: a regra não permite que seu conteúdo seja carregado no renderer, chamada LLM ou qualquer decisão sobre classificação experimental. `llm-input.json` permanece `BYTE_IMMUTABLE_EVIDENCE`, porque é o estímulo estruturado que origina o prompt, mesmo contendo JSON.

### 16.2 Canonicalização permitida

Para `CANONICALIZABLE_TEXT_METADATA`, a única canonicalização inicialmente aceita é `EOL_CANONICALIZATION_ONLY`. O commit pode congelar o blob Git canônico produzido por filtros já vigentes antes da tentativa de freeze somente se todos os seguintes gates passarem:

1. a transformação provém exclusivamente de filtros Git preexistentes e versionados/aplicáveis;
2. nenhum byte do worktree foi editado para obter a representação canônica;
3. a diferença é somente CRLF/LF;
4. ambas as representações são JSON válido e possuem estrutura, valores, tipos, propriedades, arrays e ordem de arrays idênticos;
5. nenhuma string interna, encoding lógico ou informação é modificada;
6. ambas passam no schema aplicável;
7. o blob staged é exatamente o resultado esperado do clean filter Git;
8. `.gitattributes` não foi alterado na mesma operação; e
9. a aceitação não depende do EXP, de Ground Truth, de resultado técnico observado ou de resultado LLM.

Não são permitidos trimming, reindentação, reordenação de propriedades, pretty-print, minificação, formatter, normalização Unicode, alteração de BOM, alteração de strings, espaços internos ou remoção de linhas em branco. Qualquer transformação além de EOL bloqueia o freeze.

`GIT_ATTRIBUTES_MUST_PREEXIST_FREEZE_ATTEMPT = YES`. `GIT_ATTRIBUTES_CHANGE_TO_PASS_GATE_ALLOWED = NO`.

### 16.3 Duas identidades verificáveis

Para metadata canonicalizável, a auditoria registra separadamente `WORKTREE_SHA256`, hash dos bytes físicos factuais preservados, e `GIT_BLOB_SHA256`, hash da representação canônica que será versionada. Um não substitui silenciosamente o outro. Para evidência byte-imutável, a identidade congelada é o conteúdo byte-exato já validado; para metadata canonicalizável, a identidade congelada é o blob Git canônico somente após os gates da seção 16.2.

### 16.4 Gate de freeze

O freeze segue cinco gates:

1. **Scope:** stage somente paths autorizados.
2. **Byte immutable:** exigir identidade byte a byte para cada `BYTE_IMMUTABLE_EVIDENCE`.
3. **Text metadata:** exigir proveniência do clean filter, transformação EOL-only, identidade semântica JSON, schema e ausência de edição no worktree para cada `CANONICALIZABLE_TEXT_METADATA` afetado.
4. **Diff:** executar `git diff --cached --check`. Findings exclusivamente de whitespace preservado em `BYTE_IMMUTABLE_EVIDENCE` são diagnósticos e não autorizam alterar bytes; metadata editável continua sujeita ao check normal.
5. **Secrets:** o scan dos blobs staged deve passar.

Falha em qualquer gate bloqueia o freeze. Esta regra é geral para EXPs passados e futuros, não reclassifica evidência retroativamente e não invalida, reescreve ou move freezes/tags anteriores.

## 18. Retomada de sequência técnica incompleta por interrupção do executor

`EXECUTOR_INTERRUPTION` é um evento operacional distinto de falha do provider: o processo ou orquestrador termina depois da preservação completa de uma attempt e antes de obter a primeira resposta válida ou consumir `MAX_TECHNICAL_ATTEMPTS`. A interrupção não conta como attempt, não reinicia o orçamento, não apaga nem sobrescreve evidência e não torna automaticamente o EXP uma falha técnica terminal.

`RESUME_INCOMPLETE_TECHNICAL_ATTEMPT_SEQUENCE` é permitido somente quando não existe `llm-output.json` válido, o número de attempts completas é menor que o máximo congelado, a sequência é contínua desde `attempt-01`, todas as attempts existentes passam integridade e hash linkage, nenhuma Phase B ocorreu, Ground Truth não foi carregado, prompt/config/schema permanecem idênticos e a interrupção ocorreu fora de qualquer decisão semântica da LLM. O próximo índice é determinístico: `NEXT_ATTEMPT_INDEX = EXISTING_ATTEMPT_COUNT + 1`.

Attempts anteriores permanecem append-only: é proibido renomeá-las, apagá-las, reexecutá-las ou sobrescrever seus raws, timestamps e metadados. O máximo de attempts vale globalmente entre invocações; se o orçamento for esgotado sem resposta válida, então — e somente então — o resultado é `TECHNICAL_FAILURE_NO_VALID_RESPONSE`. `FIRST_VALID_RESPONSE` também vale globalmente: uma resposta válida em retomada congela o output e proíbe attempts posteriores.

Somente uma attempt completa pode contar: `attempt.json` válido, raw preservado quando aplicável, hash linkage válido e status técnico determinado. Uma attempt parcial não pode ser recuperada ou sobrescrita automaticamente; o EXP fica `REQUIRES_REVIEW`. Se já houver output válido, retomada de inferência é proibida e a única próxima ação permitida é Phase B pendente.

Após `EXECUTOR_INTERRUPTION`, o batch não pula o EXP incompleto: a próxima invocação deve aplicar a retomada nele antes do próximo EXP da ordem fixa. Interrupções repetidas continuam suportadas dentro do orçamento, sempre pelo próximo índice disponível. A retomada continua sendo a mesma Phase A: Ground Truth permanece proibido até o freeze de um output válido.

## 19. Freeze de evidência de falha técnica terminal

`VALID_EVALUATION` e `TERMINAL_TECHNICAL_FAILURE_EVIDENCE` são conceitos distintos. Uma avaliação válida exige a primeira resposta válida preservada em `llm-output.json`, schema válido e Phase B quando aplicável. Já a evidência de `TECHNICAL_FAILURE_NO_VALID_RESPONSE` registra um outcome técnico terminal e não é avaliação válida, não recebe Phase B, Ground Truth para scoring, MATCH/MISMATCH, nem entra automaticamente no denominador de `VALID_RESPONSE_ACCURACY`.

Uma evidência terminal pode ser congelada em Git somente se: o máximo de attempts autorizado foi atingido sem exceder orçamento; índices são contínuos; todas as attempts e raws estão preservados append-only, com hash linkage; não existe `llm-output.json`, resposta válida, indicação de resposta válida não persistida, segunda observação válida ou colisão de slot pós-call; a política de retry foi respeitada; Ground Truth não foi carregado para scoring; Phase B não ocorreu; não existe retry pós-batch; e o secret scan passou. A ausência de `llm-output.json` é obrigatória e suficiente para esse outcome, não evidência incompleta.

O conjunto congelável contém somente `attempt.json` (`CANONICALIZABLE_TEXT_METADATA`) e `response.raw.json` (`BYTE_IMMUTABLE_EVIDENCE`) de cada attempt. A regra é geral para qualquer falha técnica retryable autorizada, não específica a HTTP 429. O status é derivável das attempts, seus raws, a ausência de output e este protocolo; não exige novo artefato de status.

Um checkpoint de execução pode conter tanto avaliações válidas como evidências técnicas terminais, desde que os outcomes individuais sejam derivados dos artefatos e claramente diferenciados. Falhas terminais podem ser reportadas separadamente como outcomes técnicos, mas nunca como MATCH, MISMATCH ou avaliação válida. Não há retry compensatório ou pós-batch. A regra não reclassifica retroativamente casos com resposta válida não persistida, segunda observação válida, colisão de slot ou orçamento excedido.

## 20. Condições técnicas do provider e reexecução controlada

Resultado classificatório, resultado técnico e conformidade metodológica são dimensões independentes. Falha técnica do provider não é, por si, falha metodológica e não conta como MATCH ou MISMATCH.

`response.raw.json` é obrigatório quando uma resposta do provider foi efetivamente recebida. Para `TIMEOUT` ou falha de transporte antes de qualquer resposta, `attempt.json` com status inequívoco é a evidência completa: raw é `NOT_APPLICABLE`, não pode ser sintetizado ou reconstruído, e a tentativa ainda consome orçamento. Uma primeira resposta válida posterior permanece selecionável sob `FIRST_VALID_RESPONSE`.

HTTP 429, quota exhaustion e rate limit equivalente são `PROVIDER_LIMIT_CONDITION`: condição técnica externa, não observação válida nem falha metodológica. Uma execução com orçamento esgotado, zero resposta válida e todas as attempts em `PROVIDER_LIMIT_CONDITION` é `TERMINAL_PROVIDER_LIMIT_FAILURE`; sua evidência histórica permanece imutável e não é avaliação válida, MATCH ou MISMATCH.

`PROVIDER_LIMIT_REEXECUTION` é permitido apenas para `TERMINAL_PROVIDER_LIMIT_FAILURE` com zero respostas/classificações válidas e sem não conformidade metodológica. A autorização é independente de Ground Truth e scores; usa namespace de execução novo e determinístico, orçamento novo e `FIRST_VALID_RESPONSE` dentro dessa nova execução, sem sobrescrever attempts históricas. É proibido após resposta válida, MATCH, MISMATCH, para melhorar classificação ou como inferência compensatória. Resposta válida não persistida, segunda observação válida, violação de orçamento ou colisão de slot não são curadas por esta regra.

## 17. Recuperação de artefato normativo preexistente ausente

`RECOVERY_OF_MISSING_PREEXISTING_NORMATIVE_ARTIFACT` é uma correção excepcional e geral para materializar um `ground-truth.json` fisicamente ausente. Ela não cria nem redefine Ground Truth: somente cria uma nova representação física de conteúdo normativo que já existia, de modo inequívoco, antes da primeira inferência relevante.

A recuperação só é permitida se todos os gates abaixo forem satisfeitos e registrados no protocolo/change control:

1. `NORMATIVE_CONTENT_PREEXISTED_BEFORE_LLM = YES`;
2. `NORMATIVE_SOURCE_FROZEN = YES`;
3. `SCHEMA_PREEXISTED = YES`;
4. `RECOVERY_DETERMINISTIC = YES`;
5. `HISTORICAL_FILE_BYTES_EXIST = NO`;
6. `LLM_RESULT_USED_FOR_RECOVERY = NO`;
7. `NO_SEMANTIC_DECISION_INTRODUCED = YES`; e
8. `RECOVERY_PROVENANCE_RECORDED = YES`.

A proveniência obrigatoriamente distingue `GROUND_TRUTH_SEMANTIC_PROVENANCE: FROZEN_CATALOG` de `GROUND_TRUTH_FILE_BYTE_PROVENANCE: POST_HOC_DETERMINISTIC_MATERIALIZATION`. Ela também deve registrar `HISTORICAL_GT_FILE_BYTES_EXIST: NO` e `HISTORICAL_GT_SEMANTIC_CONTENT_EXISTED: YES`. Esses dados pertencem ao protocolo e ao change control; não podem ser adicionados ao `ground-truth.json` quando o schema não os autorizar.

É proibido usar resposta, classificação, confidence ou reason de LLM para escolher a classificação, reescrever/simplificar/corrigir a justificativa, reinterpretar a fonte congelada, alterar o schema, comparar Ground Truth com output antes do freeze da recuperação, executar Phase B antes desse freeze ou afirmar que os bytes materializados são históricos.

O arquivo materializado deve conter exclusivamente o objeto permitido pelo schema preexistente. A serialização física nova deve ser registrada como pós-hoc e determinística; a recuperação não autoriza alterar catálogo, fonte normativa, evidência imutável, output LLM ou decisão semântica.

### 17.1 Gate de existência antes de inferência

Antes da primeira chamada real de cada EXP elegível, um preflight independente do caminho de inferência deve confirmar `GROUND_TRUTH_FILE_PRESENT_FOR_FUTURE_PHASE_B: YES`, validade contra o schema e proveniência do arquivo resolvida. O caminho de Phase A continua proibido de ler o Ground Truth ou seus valores; esse gate verifica somente path, existência, schema e proveniência fora do caminho de inferência.

O preflight deve falhar se qualquer uma dessas condições não for satisfeita. O gate é geral, não expõe conteúdo reservado ao modelo e não altera retroativamente uma Phase A já concluída.
