# Protocolo de controle de mudanças do Benchmark V2

## 1. Objetivo e escopo

Este protocolo governa alterações em casos, implementações, execuções, evidências e Ground Truth do Benchmark V2. Seu objetivo é preservar rastreabilidade, reprodutibilidade e independência científica, impedindo mudanças oportunistas após a observação de respostas de LLMs.

O baseline oficial é `8316d9ffa0c109c0aac68fd181b94fdd9dce368e`, identificado pela tag `benchmark-v2-baseline`. Cada implementação deve partir diretamente desse baseline e nunca do estado deixado por outro caso.

## 2. Estados do caso

### PLANNED

O caso está definido conceitualmente no catálogo, mas ainda não foi implementado. Pode receber ajustes metodológicos documentados, desde que preservados o histórico e a justificativa.

### IMPLEMENTED

A mutação foi aplicada ao baseline e o código está compilável, mas a execução experimental ainda não foi validada. Ajustes podem somente adequar a implementação ao conceito registrado.

### EXECUTED

O teste foi executado e evidências reais foram coletadas. A existência de uma execução não comprova, por si só, que o caso representa corretamente o conceito planejado.

### VALIDATED

Foi confirmado que:

- a mutação corresponde ao CASE;
- existe diferença real no body enviado a `Approvals.verify(responseBody)`;
- os artefatos approved, received, test-output e patch foram coletados da execução real;
- o caso é reproduzível;
- o Ground Truth continua coerente com a intenção original;
- o input da LLM não contém informação reservada.

### EVALUATED

A evidência foi enviada a pelo menos uma LLM sob avaliação. A partir desse estado, conceito, implementação, evidências e Ground Truth ficam congelados para aquela versão. Nada pode ser alterado ou sobrescrito silenciosamente.

### REJECTED

O caso foi descartado por falha factual, metodológica ou técnica. Seu registro e a justificativa devem permanecer no histórico; o identificador não pode ser reutilizado como se a rejeição não tivesse ocorrido.

### INVALIDATED

`INVALIDATED` é um estado terminal de uma versão ou execução previamente avaliada, não um substituto silencioso para o estado do CASE no catálogo. Indica que seus resultados não podem compor métricas válidas. Todos os artefatos são preservados e uma correção exige nova versão.

## 3. Regras de alteração por estado

| Estado | Alteração conceitual | Ground Truth | Implementação/evidência | Regra |
|---|---|---|---|---|
| PLANNED | Permitida com registro | Permitida somente para corrigir erro identificado antes da avaliação | N/A | Revisão pré-experimental rastreável |
| IMPLEMENTED | Limitada ao conceito original; mudança de conceito cria revisão | Não alterar sem erro metodológico demonstrável | Pode ser corrigida para corresponder ao conceito | Registrar mudança e repetir validações |
| EXECUTED | Muito limitada; mudança conceitual cria revisão | Não alterar por resultado técnico inesperado | Somente correção para reproduzir o conceito original | Preservar execução anterior e reexecutar |
| VALIDATED | Congelada | Congelado | Congelada | Qualquer mudança substantiva cria nova versão |
| EVALUATED | Proibida silenciosamente | Congelado | Congelada; artefatos imutáveis | Invalidar a versão, preservar tudo e criar revisão |
| REJECTED | N/A | N/A | Não reativar silenciosamente | Manter histórico; substituição recebe registro próprio |

Correções exclusivamente documentais podem ocorrer em qualquer estado somente quando não alterarem conceito, intenção, evidência, Ground Truth, interpretação ou estímulo enviado à LLM. Elas também devem constar no log.

## 4. Regra contra viés retrospectivo

O Ground Truth nunca poderá ser alterado com base em:

- desempenho, resposta ou confiança da LLM;
- número de acertos ou erros;
- desejo de melhorar Accuracy, Precision, Recall, F1 ou outra métrica;
- discordância da LLM com o pesquisador;
- conveniência para análise ou publicação.

Se o Ground Truth for `SHOULD_UPDATE` e a LLM retornar `SHOULD_NOT_UPDATE`, a divergência é um resultado experimental. Ela não constitui evidência de que o Ground Truth deva mudar. A mesma regra vale para a divergência inversa.

Uma revisão de Ground Truth exige erro metodológico documentado, evidência independente da resposta da LLM, revisão humana e registro explícito. Depois de `EVALUATED`, a versão original deve ser invalidada; seu Ground Truth e sua resposta não são reescritos.

## 5. Erro metodológico documentado

Erro metodológico documentado é uma falha demonstrável no desenho, implementação, coleta ou isolamento do caso, sustentada por evidência verificável. Exemplos:

- a mutação não altera o body snapshotado;
- o fixture não executa o trecho planejado;
- o caso depende de comportamento inexistente no baseline;
- o caso não parte diretamente do baseline ou depende de outro CASE;
- a implementação produz comportamento diferente da intenção original;
- o Ground Truth foi atribuído a partir de interpretação factual incorreta;
- informação reservada aparece no `llm-input.json`;
- o caso é duplicata material de outro sem justificativa contrastiva;
- a implementação necessária contradiz o conceito registrado;
- evidência foi inventada, truncada, misturada entre execuções ou coletada de versão errada;
- a execução não é reproduzível quando a reprodutibilidade é requisito do caso.

Não são erros metodológicos:

- a LLM errar ou discordar;
- a LLM apresentar baixa confiança;
- o caso ser difícil;
- o resultado reduzir métricas;
- a resposta contrariar a expectativa informal de um pesquisador;
- um modelo ter desempenho diferente de outro.

## 6. Mudanças antes de EVALUATED

Problemas descobertos em `PLANNED`, `IMPLEMENTED`, `EXECUTED` ou `VALIDATED` podem permitir correção, substituição, ajuste de implementação e reexecução. O registro é obrigatório e deve conter:

- CASE e versão afetada;
- estado em que o problema foi descoberto;
- versão anterior;
- problema encontrado;
- evidência independente de resultados de LLM;
- mudança realizada;
- artefatos invalidados ou substituídos;
- responsável e revisor;
- data/hora;
- necessidade e resultado da reexecução.

Uma correção de implementação que preserve integralmente o conceito pode manter a revisão conceitual, mas deve gerar nova execução. Uma mudança de intenção, Ground Truth, estímulo ou comportamento esperado exige nova versão do caso, mesmo antes de `EVALUATED`, se já houver artefatos executados que precisem ser preservados.

## 7. Mudanças depois de EVALUATED

Depois de `EVALUATED`, é proibido sobrescrever a versão original. Ao confirmar erro metodológico:

1. marcar a versão e suas execuções afetadas como `INVALIDATED`;
2. preservar catálogo, especificação, patch, snapshots, outputs, input e output da LLM, Ground Truth e metadados originais;
3. registrar problema, evidência, impacto nas métricas e responsável;
4. excluir os resultados inválidos das métricas principais sem apagá-los do histórico;
5. criar nova revisão, como `CASE-010-v2`;
6. implementar a nova revisão diretamente a partir do baseline;
7. executar, validar e avaliar a nova revisão como novo estímulo experimental.

Resultados de uma versão invalidada não podem ser atribuídos, transferidos ou reutilizados pela versão corrigida. Se já tiverem sido publicados em análise intermediária, a correção deve ser registrada de forma auditável.

## 8. Versionamento e identidade

| Artefato | Convenção | Exemplo |
|---|---|---|
| Caso conceitual no catálogo | `CASE-NNN` | `CASE-001` |
| Revisão implementável do caso | `CASE-NNN-vN` | `CASE-001-v1`, `CASE-001-v2` |
| Execução experimental | `EXP-NNN` | `EXP-001` |
| Repetição da mesma versão/condição | `EXP-NNN-RN` | `EXP-001-R1`, `EXP-001-R2` |

`CASE-001-v1` e `CASE-001-v2` são estímulos experimentais distintos quando qualquer diferença altera conceito, implementação observável, evidência ou input da LLM. Uma repetição `R1/R2` não pode ocultar mudança de versão: repetições usam a mesma revisão, baseline, patch e parâmetros, salvo campos naturalmente variáveis documentados.

Cada `execution.json` deve registrar, além dos campos do schema aplicável, o `baselineCommit`, o identificador do CASE, sua revisão e o identificador da execução. Se o schema ainda não comportar algum campo, a necessidade deve ser tratada em revisão metodológica separada antes das execuções; este protocolo não altera schemas.

## 9. Log obrigatório de mudanças

O log será mantido neste arquivo até eventual migração formal para artefato próprio. A migração deve preservar todas as entradas e ser registrada como `DOCUMENTATION_ONLY`.

Tipos permitidos:

- `CORRECTION`
- `REPLACEMENT`
- `INVALIDATION`
- `IMPLEMENTATION_FIX`
- `GROUND_TRUTH_CORRECTION`
- `DOCUMENTATION_ONLY`

| Data | Caso/versão | Estado | Tipo | Antes | Depois | Motivo | Evidência | Responsável/revisor |
|---|---|---|---|---|---|---|---|---|
| — | — | — | — | — | — | Log inicial sem mudanças registradas | — | — |
| 2026-08-09 | CASE-001-v1 / EXP-001 | EXECUTED | CORRECTION | `metadata.json` validado indevidamente contra `case.schema.json`; hash original `4316C4A26780CDF3366F9C45C3D5BD086FD6C42F7D88408DCB495807CD0DA72D` | Criado `experiment-metadata.schema.json`; `caseVersion` normalizada e estado factual separado em `state` | Separar a definição conceitual de CASE dos metadados factuais de EXP | Falha estrutural independente de resultado de LLM; Ground Truth alterado: NÃO; CASE conceitual alterado: NÃO; resultado de LLM observado: NÃO; impacto experimental: nenhum; reexecução: desnecessária | Codex / revisão humana pendente |
| 2026-08-09 | CASE-001-v1 / EXP-001 | EXECUTED | CORRECTION | `execution.schema.json` exigia modelo/provider/parâmetros antes de EVALUATED; `execution.json` usava sentinelas; hash original `D4396F99AECA4A2A06E2A251A68F06FC86352761E340AA759245F7E4BCE89E21` | Campos de LLM tornados opcionais e sentinelas removidos da execução técnica | Não inventar dados de modelo quando nenhuma LLM foi executada | Artefatos e histórico da execução comprovam ausência de chamada a LLM; Ground Truth alterado: NÃO; CASE conceitual alterado: NÃO; resultado de LLM observado: NÃO; impacto experimental: nenhum; reexecução: desnecessária | Codex / revisão humana pendente |
| 2026-08-10 | Benchmark V2 / PROMPT_TEMPLATE_V1 | VALIDATED, pré-EVALUATED | DOCUMENTATION_ONLY | Não havia protocolo operacional, template congelável nem renderer explícito para avaliação por LLM | Criados `evaluation_protocol.md`, `snapshot-review-v1.md` e renderer determinístico; `caseId` administrativo permanece no artefato interno e é excluído do prompt | Fixar estímulo, formato de resposta, isolamento, configuração, repetição e retry antes da primeira inferência | `LLM_EVALUATIONS_FOUND: 0`; duas renderizações locais idênticas; leakage ausente; schemas, CASE, Ground Truth e evidências reais não alterados; resultado de LLM observado: NÃO | Codex / revisão humana pendente |
| 2026-08-10 | Benchmark V2 / EXP artifacts | VALIDATED, pré-EVALUATED | CORRECTION | A normalização automática de fim de linha alteraria os bytes staged de `test-output.txt` e `rendered-prompt.txt`, divergindo dos hashes registrados | Criado `.gitattributes` para desabilitar normalização dos artefatos experimentais com integridade byte a byte | Preservar no commit exatamente os bytes auditados e seus SHA-256 | Comparação entre blobs working/staged detectou divergência antes do commit; conteúdo dos artefatos não foi alterado; CASE e Ground Truth alterados: NÃO; resultado de LLM observado: NÃO; impacto experimental: nenhum | Codex / revisão humana pendente |
| 2026-08-10 | Benchmark V2 / CONFIG-GEMINI-01 | VALIDATED, pré-EVALUATED | CORRECTION | `snapshot_ai_review.py` usava prompt legado, reconstruía/resumia evidências, não aplicava structured output/schema/retry e continha credencial hardcoded; o commit congelado referenciava modelo anterior, já alterado no working tree para `gemini-3.6-flash` antes desta auditoria | Adaptador passou a consumir `rendered-prompt.txt`, configuração externa sem segredo, chave via `GEMINI_API_KEY`, SHA-256 do estímulo, structured output, validação estrita e até 3 tentativas técnicas; criada `CONFIG-GEMINI-01.json` | Adequar a infraestrutura específica do provider ao protocolo congelado antes da primeira inferência | `LLM_EVALUATIONS_FOUND: 0`; nenhuma API chamada; nenhuma evidência do EXP-001, CASE ou Ground Truth alterada; resultado de LLM observado: NÃO; a credencial histórica deve ser revogada/rotacionada fora do repositório | Codex / revisão humana pendente |
| 2026-08-11 | Benchmark V2 / CONFIG-GEMINI-01 | VALIDATED, pré-EVALUATED | DOCUMENTATION_ONLY | Confirmação humana de segurança pendente | The Gemini credential previously exposed in repository history was revoked/rotated before the first experimental inference. No credential material is recorded. | Registrar a confirmação externa sem persistir chave, prefixo, hash ou identificador de credencial | Nenhuma API chamada; CASE, Ground Truth e evidências alterados: NÃO; resultado de LLM observado: NÃO | Pesquisador / confirmação explícita |
| 2026-08-22 | Benchmark V2 / CONFIG-GEMINI-01 → CONFIG-GEMINI-02 | VALIDATED, pré-EVALUATED | CORRECTION | O contrato `generationConfig.responseFormat` foi rejeitado por `models.generateContent` com HTTP 400 `INVALID_ARGUMENT`, antes de qualquer resposta do modelo | CONFIG-GEMINI-01 e sua tentativa foram preservadas; criada CONFIG-GEMINI-02 usando `generationConfig.responseMimeType` e `generationConfig.responseJsonSchema`; o schema completo continua sendo aplicado na validação local | Corrigir exclusivamente o mapeamento provider-specific após falha técnica sem observação experimental válida | Ground Truth acessado: NÃO; classificação observada: NÃO; CASE, prompt e evidências originais do EXP alterados: NÃO; `$schema` e `minLength`, não listados no subset oficial do provider, são omitidos apenas do request | Codex / revisão humana pendente |

Uma entrada nunca é apagada. Correções no próprio log são novas entradas `DOCUMENTATION_ONLY`, com referência à entrada corrigida.

| 2026-08-22 | Benchmark V2 / EXP-002–EXP-005 freeze | VALIDATED | DOCUMENTATION_ONLY | `git diff --cached --check` era aplicado como gate absoluto e reportava CRLF em `llm-input.json` e blank line final em `patch.diff`, ambos pertencentes à evidência capturada e protegidos contra normalização | Para `EVIDENCE_IMMUTABLE`, integridade SHA-256, preservação de conteúdo, secret scan, schema quando aplicável e escopo substituem o whitespace check; `git diff --cached --check` permanece obrigatório para `EDITABLE_METADATA` | Permitir o freeze técnico sem alterar bytes ou hashes de evidências e sem enfraquecer o gate de arquivos editáveis | Nenhuma evidência, CASE, Ground Truth, prompt ou `llm-input.json` foi alterado; resultado de LLM observado durante a mudança: NÃO; nenhuma LLM/API executada; impacto experimental: nenhum | Codex / revisão humana pendente |

## 10. Ground Truth e informações reservadas

Ground Truth e intenção ficam em artefatos reservados do pesquisador. Não podem aparecer direta ou indiretamente em `llm-input.json`. Categoria, dificuldade, CASE ID e outros metadados também devem ser omitidos quando puderem funcionar como pistas.

O input da LLM contém somente as evidências autorizadas pelo protocolo experimental, como diff, snapshots approved/received, output do teste, nome técnico do teste, endpoint e método HTTP quando previstos. A separação entre artefatos reservados e input deve ser verificada antes de `EVALUATED`.

Outputs da LLM nunca podem ser usados para completar, reformular ou reinterpretar retroativamente o artefato reservado.

## 11. Proteção de pares contrastivos

Os pares atuais sob proteção especial são:

- CASE-007 / CASE-008;
- CASE-013 / CASE-014;
- CASE-025 / CASE-026.

Uma mudança em qualquer membro deve desencadear revisão do par inteiro. A revisão deve verificar se permanecem comparáveis:

- snapshot e fixture;
- forma observável da diferença;
- quantidade de arquivos e tamanho aproximado do patch;
- evidências fornecidas à LLM;
- ausência de pistas superficiais que revelem a intenção;
- oposição justificada dos Ground Truths.

Se a comparabilidade for quebrada, ambos os membros devem ser reavaliados antes de qualquer nova avaliação. Depois de `EVALUATED`, a correção segue versionamento: não se altera um membro original para fazê-lo combinar retroativamente com o outro.

## 12. Critério de congelamento

Um CASE pode ser declarado congelado quando:

- conceito e intenção foram revisados;
- Ground Truth foi revisado independentemente de qualquer resposta de LLM;
- implementabilidade foi aceita;
- alcance e riscos conhecidos estão documentados;
- fixture e observabilidade foram confirmados contra o baseline;
- pares contrastivos relacionados foram revisados;
- nenhuma avaliação por LLM ocorreu para aquela versão.

O congelamento deve ser identificado por commit e registrado no log. Depois dele, mudança conceitual, de Ground Truth ou de estímulo exige versionamento. A versão torna-se estritamente imutável ao alcançar `EVALUATED`.

## 13. Integração com o fluxo experimental

Fluxo principal:

```text
PLANNED
   ↓
IMPLEMENTED
   ↓
EXECUTED
   ↓
VALIDATED
   ↓
EVALUATED
```

Problema antes da avaliação:

```text
PLANNED / IMPLEMENTED / EXECUTED / VALIDATED
   ↓
erro metodológico documentado
   ↓
CORRECTION + revalidação/reexecução
   ou
REJECTED
```

Problema depois da avaliação:

```text
EVALUATED
   ↓
erro metodológico documentado
   ↓
INVALIDATED (artefatos preservados)
   ↓
nova versão do CASE
   ↓
IMPLEMENTED → EXECUTED → VALIDATED → EVALUATED
```

## 14. Checklist operacional

Antes de mudar qualquer artefato do benchmark:

1. identificar CASE, revisão, execução e estado atuais;
2. verificar se alguma LLM já recebeu a evidência;
3. reunir evidência independente da resposta da LLM;
4. classificar o tipo de mudança;
5. decidir entre correção, nova versão, invalidação ou rejeição;
6. preservar os artefatos existentes;
7. registrar a mudança no log;
8. revisar casos contrastivos afetados;
9. reexecutar e revalidar quando aplicável;
10. confirmar que métricas não reutilizam versões inválidas.

## Correção pré-EVALUATED de EXP-011 e EXP-012

EXP-011 e EXP-012 ainda não haviam sido avaliados e nenhuma resposta LLM havia sido observada. Uma auditoria detectou a diferença espúria `id:4 -> id:3`, tornando a evidência anterior inadequada para freeze. A causa foi a execução isolada do teste-alvo: os dois registros criados na inicialização consumiam os IDs 1 e 2 e, embora o `deleteAll()` removesse os registros, a sequência não era reiniciada; assim, a execução isolada criava o autor com ID 3. O contexto legítimo do baseline executa primeiro `testCreateAuthor_Snapshot`, que consome o ID 3, e depois `testGetAuthorById_Snapshot`, que reproduz naturalmente o approved com ID 4. A rematerialização ocorreu somente após esse baseline passar. Os CASEs, o Ground Truth e os objetivos experimentais não foram alterados.

| 2026-08-23 | CASE-016-v1 / protocolo de evidência técnica | PLANNED, pré-EVALUATED | CORRECTION | `repeated technical execution` não definia quantidade, preservação individual, seleção do estímulo nem artefato normativo | Fixados três runs independentes (`RUN-01`–`RUN-03`), seleção a priori de `RUN-01`, comparação byte/SHA-256, manifest factual e proibição de amostragem adaptativa | Eliminar escolha pós-resultado antes de qualquer execução de CASE-016 | EXP-016 não executado; resultados técnicos observados: zero; inferências LLM: zero; CASE e Ground Truth alterados: NÃO; impacto retroativo em EXP-001–015: nenhum; novo commit/tag específico do protocolo | Codex / revisão humana pendente |
| 2026-08-24 | EXP-019 / EXP-020 — protocolo de preconditionamento | VALIDATED, pré-EVALUATED; POST-TECHNICAL-DATA | CORRECTION | O collateral real estava preservado, mas a execução ampla também colocou seu output no `test-output.txt` primário, `llm-input.json` e prompt; a execução primária isolada não reproduziu o approved dependente de estado acumulado | Definidas PHASE P de preconditionamento e PHASE O de observação primária, transcripts separados no momento da execução, manifest factual e exclusão de setup/collateral do estímulo LLM | Reproduzir o baseline congelado com setup mínimo auditável sem filtragem pós-hoc nem leakage de collateral | Correção definida após resultados técnicos de EXP-019/020, mas antes de qualquer resultado LLM; CASE e Ground Truth alterados: NÃO; template, provider e modelo alterados: NÃO; EXP-019/020 requerem rematerialização futura; impacto retroativo em EXP-001–018: nenhum; EXP-016 permanece `REQUIRES_REVIEW` | Codex / revisão humana pendente |
| 2026-08-24 | CASE-019-v1 / EXP-019 e CASE-020-v1 / EXP-020 | VALIDATED, pré-EVALUATED | CORRECTION | Materializações anteriores tinham output collateral no `test-output.txt` central e no futuro estímulo LLM | Rematerializadas sob `EXPLICIT_PRECONDITIONING_V1`: PHASE P e PHASE O capturadas em invocações separadas, preconditionamento preservado com manifest, observação primária isolada e collateral preservado fora do input LLM | Remover leakage por nova execução controlada, sem editar ou filtrar transcripts | Resultados técnicos anteriores preservados por hashes no relatório de correção; resultados LLM observados: NÃO; chamadas LLM/API: zero; CASE, Ground Truth, approved, template, configuração e protocolo alterados: NÃO; baseline funcional restaurado | Codex / revisão humana pendente |
| 2026-08-24 | Benchmark V2 / sucesso da PHASE P | VALIDATED, PRE-EVALUATED; POST-TECHNICAL-DATA | CORRECTION | O protocolo exigia `PRECONDITIONING_SUCCESS`, mas não definia se nem quando uma PHASE P com exit code não-zero poderia satisfazê-lo; os resultados técnicos de EXP-019/020 já existiam, sem qualquer resultado LLM | Separados sucesso do processo e sucesso do estado; exit code zero é sucesso normal, enquanto não-zero exige conjuntamente construção confirmada antes da falha, `POST_STATE_ASSERTION_FAILURE`, transcript integral, PHASE O baseline aprovada, passos fixados antes da mutação e independência do output mutado; manifest ampliado com fatos e determinação auditável | Corrigir a lacuna normativa com regra geral aplicável a qualquer preconditionamento explícito, não para aceitar resultados específicos | Nenhuma LLM/API executada; Ground Truth usado na decisão: NÃO; CASE, Ground Truth e evidências EXP-001–020 alterados: NÃO; EXP-001–018 sem impacto retroativo; EXP-016 permanece `REQUIRES_REVIEW`; EXP-019/020 requerem atualização futura dos manifests e revalidação sob a regra congelada | Codex / revisão humana pendente |
| 2026-08-27 | CASE-019-v1 / EXP-019 e CASE-020-v1 / EXP-020 | VALIDATED, PRE-EVALUATED; revalidação pós-protocolo | CORRECTION | Os manifests de preconditionamento preservavam os fatos originais, mas não continham os cinco campos tornados obrigatórios pelo protocolo de sucesso da PHASE P | Acrescentados somente `stateConstructionConfirmed`, `failureClassification`, `preconditionTranscriptPreserved`, `primaryBaselinePassAfterPreconditioning` e `successDetermination`, derivados dos transcripts e gates técnicos já preservados | Adequar administrativamente os manifests ao schema congelado sem nova execução ou rematerialização | Nenhuma execução, LLM ou API realizada; evidência factual imutável inalterada; exit code 1 preservado; nenhuma informação de Ground Truth registrada; EXP-019/020 revalidados sob `benchmark-v2-precondition-success-protocol` | Codex / revisão humana pendente |
| 2026-08-29 | Benchmark V2 / collateral evidence manifest | VALIDATED, PRE-EVALUATED; POST-TECHNICAL-DATA | CORRECTION | A auditoria de EXP-021–025 encontrou collateral tecnicamente observado em EXP-021–023 e manifests estruturalmente coerentes, mas nenhum schema normativo congelado para `collateral-manifest.json`; nenhum resultado LLM havia sido observado | Criado schema geral `collateral-manifest.schema.json` e formalizados cardinalidade, paths relativos, hashes de approved/received/test-output, preservação integral e exclusão do input LLM | Corrigir a lacuna protocolar antes da avaliação, sem desenhar o contrato para resultados específicos | Correção POST-TECHNICAL-DATA / PRE-EVALUATED; nenhuma evidência experimental ou manifest existente alterado; manifests históricos serão revalidados e, se necessário, migrados em tarefa posterior; Ground Truth não participou do desenho; resultados LLM observados: NÃO | Codex / revisão humana pendente |
| 2026-08-29 | EXP-004–008, EXP-019–023 / collateral manifests | VALIDATED, PRE-EVALUATED; migração administrativa pós-freeze | CORRECTION | Os dez manifests históricos precediam o schema congelado de collateral e não continham sua estrutura normativa nem hashes por artefato | Migrados somente os dez `collateral-manifest.json` existentes para `COLLATERAL_EVIDENCE_V1`, com fatos e SHA-256 derivados da evidência já preservada | Adequar e revalidar os manifests contra o schema congelado sem nova execução ou alteração da evidência | Nenhum teste, Maven, LLM ou API executado; bytes de approved/received/test-output, evidência central e preconditionamento inalterados; Ground Truth não consultado; EXP-024/025 continuam sem manifest; commits e tags congelados não foram movidos | Codex / revisão humana pendente |
| 2026-08-30 | Benchmark V2 / Git staging representation | VALIDATED, PRE-EVALUATED; POST-TECHNICAL-DATA | CORRECTION | O freeze técnico de EXP-026 foi bloqueado antes de commit/tag porque filtros Git preexistentes canonicalizaram CRLF→LF em `metadata.json`, `execution.json`, `ground-truth.json` e `precondition/manifest.json`, enquanto o gate exigia igualdade raw worktree/index para todo arquivo | Definida regra geral que separa `BYTE_IMMUTABLE_EVIDENCE` de `CANONICALIZABLE_TEXT_METADATA`; aceita somente canonicalização EOL por filtros preexistentes para metadata estruturada, com hashes dual worktree/blob, identidade JSON completa, schema e proibição de alterar `.gitattributes` para passar | Corrigir lacuna do gate sem normalizar bytes, alterar EXP-026 ou enfraquecer a imutabilidade de estímulos, snapshots, patches, transcripts e outputs | Nenhum commit/tag de EXP-026 foi criado na tentativa bloqueada; EXP-026 permaneceu íntegro; nenhum experimento, CASE, Ground Truth, prompt, llm-input, precondition ou schema foi alterado; Ground Truth não foi usado para desenhar a regra; resultados técnicos já existiam, resultados LLM observados: NÃO; nova tentativa de freeze ocorrerá em tarefa posterior | Codex / revisão humana pendente |
| 2026-08-30 | Benchmark V2 / prompt identity and batch inference continuation | VALIDATED, PRE-EVALUATED; POST-TECHNICAL-DATA | CORRECTION | O preflight da rodada principal identificou ambiguidade entre o SHA do arquivo-template e o SHA do prompt renderizado de EXP-001, e ausência de regra batch após esgotamento técnico de um EXP | Explicitada a identidade de `PROMPT_TEMPLATE_V1` (arquivo, commit e SHA), a distinção de SHA de template versus prompt renderizado, e a continuação fixa após `TECHNICAL_FAILURE_NO_VALID_RESPONSE` | Eliminar ambiguidades operacionais antes da rodada LLM sem alterar estímulos, evidências ou configuração | A regra é geral para os 28 EXPs elegíveis; Ground Truth não foi usado; EXP-001 não foi reexecutado nem usado para decidir a continuidade; nenhuma LLM/API, teste ou execução técnica ocorreu; EXP-001–030, CONFIG-GEMINI-02, template e adapter inalterados; tags anteriores não foram movidas | Codex / revisão humana pendente |
