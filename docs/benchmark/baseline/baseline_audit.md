# Auditoria do baseline do Benchmark V2

## Identificação

- Data/hora da auditoria: `2026-08-09T16:34:05.8443578-03:00`
- Branch: `main`
- HEAD: `577aeea3901e7dc3e818ce8139bce652480af308`
- Sistema operacional: Windows 11, versão observada pelo Maven `10.0`, arquitetura `amd64` (runtime .NET: `Microsoft Windows NT 10.0.26200.0`)
- Java: OpenJDK `21.0.11` LTS, Microsoft build `21.0.11+10-LTS`
- Maven: Apache Maven `3.9.14`
- Spring Boot: `3.4.1`
- ApprovalTests: `24.3.0`
- Banco de teste: H2, com `ddl-auto=create-drop`
- JUnit: JUnit Jupiter fornecido e gerenciado por `spring-boot-starter-test` `3.4.1`; não há versão do JUnit declarada diretamente no `pom.xml`
- Timezone de teste: UTC, por `Clock.fixed(Instant.parse("2026-05-26T13:25:34.690339900Z"), ZoneOffset.UTC)` em `TestTimeConfig`

## Estado inicial do Git

Não havia arquivos rastreados modificados nem arquivos staged. Os seguintes arquivos já estavam untracked antes dos testes:

```text
docs/benchmark/README.md
docs/benchmark/baseline/README.md
docs/benchmark/experiments/.gitkeep
docs/benchmark/schemas/case.schema.json
docs/benchmark/schemas/execution.schema.json
docs/benchmark/schemas/ground-truth.schema.json
docs/benchmark/schemas/llm-input.schema.json
docs/benchmark/schemas/llm-output.schema.json
docs/benchmark/snapshot_dataset.md
docs/snapshot_preliminar_dataset.md
```

O script `scripts/snapshot_ai_review.py`, os testes de integração e os snapshots aprovados estavam rastreados e sem modificações.

## Estrutura do benchmark

| Item | Status |
|---|---|
| `docs/benchmark/README.md` | PASS |
| `docs/benchmark/snapshot_dataset.md` | PASS |
| `docs/benchmark/baseline/README.md` | PASS |
| `docs/benchmark/experiments/.gitkeep` | PASS |
| `docs/benchmark/schemas/case.schema.json` | PASS |
| `docs/benchmark/schemas/ground-truth.schema.json` | PASS |
| `docs/benchmark/schemas/llm-input.schema.json` | PASS |
| `docs/benchmark/schemas/llm-output.schema.json` | PASS |
| `docs/benchmark/schemas/execution.schema.json` | PASS |
| `docs/snapshot_preliminar_dataset.md` preservado | PASS |

## JSON Schemas

| Schema | Status | Evidência |
|---|---|---|
| `case.schema.json` | PASS | JSON válido, Draft 2020-12, objeto fechado, obrigatórios coerentes e enums de categoria, método, dificuldade e status restritos. |
| `ground-truth.schema.json` | PASS | JSON válido, Draft 2020-12 e classificação restrita a `SHOULD_UPDATE` ou `SHOULD_NOT_UPDATE`. |
| `llm-input.schema.json` | PASS | JSON válido, Draft 2020-12 e campos de evidência obrigatórios. Não contém Ground Truth, classificação esperada, resposta correta, `shouldUpdateSnapshot` ou valores equivalentes que revelem a resposta. |
| `llm-output.schema.json` | PASS | JSON válido, Draft 2020-12; boolean obrigatório, confiança inteira limitada de 0 a 100 e razão obrigatória. |
| `execution.schema.json` | PASS | JSON válido, Draft 2020-12; campos obrigatórios e opcionais de reprodutibilidade possuem tipos coerentes. |

## Snapshots

Arquivos-fonte aprovados:

| Caminho | Teste associado | Recurso/endpoint | HTTP |
|---|---|---|---|
| `src/test/java/com/example/pocapi/integration/AuthorApiIntegrationTest.testCreateAuthor_Snapshot.approved.txt` | `AuthorApiIntegrationTest.testCreateAuthor_Snapshot` | `/authors` | POST |
| `src/test/java/com/example/pocapi/integration/AuthorApiIntegrationTest.testGetAllAuthors_Snapshot.approved.txt` | `AuthorApiIntegrationTest.testGetAllAuthors_Snapshot` | `/authors` | GET |
| `src/test/java/com/example/pocapi/integration/AuthorApiIntegrationTest.testGetAuthorById_Snapshot.approved.txt` | `AuthorApiIntegrationTest.testGetAuthorById_Snapshot` | `/authors/{id}` | GET |
| `src/test/java/com/example/pocapi/integration/AuthorApiIntegrationTest.testGetAuthorNotFound_Snapshot.approved.txt` | `AuthorApiIntegrationTest.testGetAuthorNotFound_Snapshot` | `/authors/99999` | GET |
| `src/test/java/com/example/pocapi/integration/BookApiIntegrationTest.testCreateBook_Snapshot.approved.txt` | `BookApiIntegrationTest.testCreateBook_Snapshot` | `/books` | POST |
| `src/test/java/com/example/pocapi/integration/BookApiIntegrationTest.testGetBooksByAuthor_Snapshot.approved.txt` | `BookApiIntegrationTest.testGetBooksByAuthor_Snapshot` | `/books/by-author/{authorId}` | GET |

Também existiam seis cópias geradas desses arquivos em `target/test-classes/com/example/pocapi/integration/`. Não foi encontrado nenhum `*.received.txt` antes, entre ou depois das execuções.

## Execução 1

- Comando: `mvn test`
- Exit code: `0`
- Total: `18`
- Successes: `18`
- Failures: `0`
- Errors: `0`
- Skipped: `0`
- Tempo total Maven: `32.090 s`
- Resultado: `BUILD SUCCESS`

Uma tentativa inicial dentro do sandbox não iniciou a suíte porque o Maven não pôde criar/acessar `C:\.m2\repository`. O comando foi repetido sem alteração fora do sandbox, usando o repositório local normal do usuário; os números acima correspondem à execução válida.

## Execução 2

- Comando: `mvn test`
- Exit code: `0`
- Total: `18`
- Successes: `18`
- Failures: `0`
- Errors: `0`
- Skipped: `0`
- Tempo total Maven: `31.501 s`
- Resultado: `BUILD SUCCESS`

As duas execuções tiveram o mesmo resultado funcional. Não surgiram arquivos recebidos e os hashes SHA-256 dos seis snapshots aprovados permaneceram idênticos antes, entre e depois das execuções.

## Build

- Comando: `mvn -DskipTests package`
- Exit code: `0`
- Tempo total Maven: `11.951 s`
- Resultado: `BUILD SUCCESS`
- Observação: o Maven informou explicitamente `Tests are skipped.`

## Efeitos colaterais

- Arquivos já untracked antes dos testes: os dez arquivos listados em **Estado inicial do Git**.
- Novos arquivos não ignorados produzidos pelos testes: nenhum.
- Arquivos rastreados modificados pelos testes: nenhum.
- Snapshots aprovados modificados: nenhum; hashes SHA-256 permaneceram estáveis.
- Arquivos `*.received.txt` produzidos: nenhum.
- Saídas de build ficaram em `target/`, que já é ignorado pelo Git.

## Inventário dos testes de snapshot

| Classe | Método de teste | Arquivo aprovado | Endpoint | HTTP |
|---|---|---|---|---|
| `AuthorApiIntegrationTest` | `testGetAllAuthors_Snapshot` | `AuthorApiIntegrationTest.testGetAllAuthors_Snapshot.approved.txt` | `/authors` | GET |
| `AuthorApiIntegrationTest` | `testCreateAuthor_Snapshot` | `AuthorApiIntegrationTest.testCreateAuthor_Snapshot.approved.txt` | `/authors` | POST |
| `AuthorApiIntegrationTest` | `testGetAuthorById_Snapshot` | `AuthorApiIntegrationTest.testGetAuthorById_Snapshot.approved.txt` | `/authors/{id}` | GET |
| `AuthorApiIntegrationTest` | `testGetAuthorNotFound_Snapshot` | `AuthorApiIntegrationTest.testGetAuthorNotFound_Snapshot.approved.txt` | `/authors/99999` | GET |
| `BookApiIntegrationTest` | `testCreateBook_Snapshot` | `BookApiIntegrationTest.testCreateBook_Snapshot.approved.txt` | `/books` | POST |
| `BookApiIntegrationTest` | `testGetBooksByAuthor_Snapshot` | `BookApiIntegrationTest.testGetBooksByAuthor_Snapshot.approved.txt` | `/books/by-author/{authorId}` | GET |

Todos os seis métodos acima chamam diretamente `org.approvaltests.Approvals.verify(responseBody)`. Não foi inferida cobertura além desses métodos.

## Critérios de baseline

| Critério | Status | Evidência |
|---|---|---|
| Projeto compila | PASS | `mvn -DskipTests package`, exit code 0. |
| Primeira execução de `mvn test` passa | PASS | 18 testes, 0 falhas e 0 erros, exit code 0. |
| Segunda execução de `mvn test` passa | PASS | 18 testes, 0 falhas e 0 erros, exit code 0. |
| Nenhum `.received.txt` residual | PASS | Busca antes, entre e depois das execuções sem resultados. |
| Testes não modificam snapshots aprovados | PASS | Seis hashes SHA-256 idênticos nos três pontos de verificação. |
| Testes não modificam arquivos funcionais versionados | PASS | `git diff --name-only` vazio após as execuções e o build. |
| Estrutura do benchmark presente | PASS | Todos os dez itens estruturais verificados. |
| JSON Schemas válidos | PASS | Sintaxe, Draft 2020-12, obrigatórios, tipos, enums e limites auditados. |
| `llm-input` sem vazamento de Ground Truth | PASS | Nenhum campo ou valor de classificação/resultado esperado encontrado. |
| Sem evidência clara de não determinismo prejudicial | PASS | Duas suítes equivalentes, snapshots estáveis e nenhum `.received`. |

## Veredito

`BASELINE_READY`

## Próxima ação recomendada

Revisão humana e posterior congelamento do commit de baseline.
