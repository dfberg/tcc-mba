# Auditoria de implementabilidade dos casos do Benchmark V2

## 1. Identificação

- Baseline tag: `benchmark-v2-baseline`
- Baseline SHA: `8316d9ffa0c109c0aac68fd181b94fdd9dce368e`
- Data: `2026-08-09T17:53:03.3569596-03:00`
- Casos auditados: 30 (`CASE-001` a `CASE-030`)
- Fontes: código do baseline, catálogo planejado, inventário factual, seis testes com `Approvals.verify(responseBody)` e seis snapshots aprovados.

Nenhum experimento foi executado. As estimativas abaixo avaliam mutações futuras, não resultados observados.

## 2. Resumo executivo

| Classificação | Quantidade |
|---|---:|
| IMPLEMENTABLE | 19 |
| IMPLEMENTABLE_WITH_RISK | 9 |
| QUESTIONABLE_REALISM | 2 |
| NOT_IMPLEMENTABLE | 0 |
| **Total** | **30** |

O catálogo é majoritariamente implementável. Os riscos recorrentes são: mapeadores compartilhados afetando mais de um snapshot; dependência de IDs gerados; representação de `null` pelo Spring; não determinismo deliberado; e alterações contratuais que exigem dois arquivos. CASE-003 e CASE-030 são tecnicamente possíveis, mas precisam ser substituídos ou reformulados para aumentar o realismo.

## 3. Auditoria por caso

## CASE-001

- Ground Truth atual: `SHOULD_UPDATE`
- Snapshot alvo: `AuthorApiIntegrationTest.testGetAllAuthors_Snapshot.approved.txt`
- Implementabilidade: `IMPLEMENTABLE`
- Arquivos mínimos: `src/main/java/com/example/pocapi/controller/AuthorController.java`
- Tamanho: `SMALL`
- Alcance: `TARGET_ONLY`; o envelope pode ser construído apenas em `getAllAuthors`.
- Observabilidade: `HIGH`; `[]` se torna objeto com `authors` e `count`.
- Determinismo: `HIGH`; o fixture é vazio e a contagem é zero.
- Realismo: `HIGH`; envelopes são evolução comum de coleções.
- Spurious Cue Risk: `MEDIUM`; envelope intencional tende a gerar diff estrutural maior que bugs simples.
- Risco principal: alterar somente a assinatura genérica, sem mudar o objeto retornado, não modifica o JSON.
- Recomendação: `KEEP`
- Ground Truth Review Required: `NÃO`
- Justificativa: uma resposta localizada com `Map` ou DTO de envelope é pequena, reproduzível e alcança o body.

## CASE-002

- Ground Truth atual: `SHOULD_NOT_UPDATE`
- Snapshot alvo: `AuthorApiIntegrationTest.testGetAllAuthors_Snapshot.approved.txt`
- Implementabilidade: `IMPLEMENTABLE_WITH_RISK`
- Arquivos mínimos: `src/main/java/com/example/pocapi/controller/AuthorController.java`
- Tamanho: `SMALL`
- Alcance: `TARGET_ONLY`
- Observabilidade: `MEDIUM`; `ResponseEntity.ok(null)` pode produzir body vazio, não o token JSON `null`.
- Determinismo: `HIGH` se a representação nula for explicitamente serializada.
- Realismo: `MEDIUM`; confundir coleção vazia e ausência é plausível.
- Spurious Cue Risk: `LOW`
- Risco principal: comportamento de serialização do Spring pode fazer o teste comparar string vazia ou nem chegar à evidência esperada.
- Recomendação: `KEEP_WITH_ADJUSTMENT`
- Ground Truth Review Required: `NÃO`
- Justificativa: especificar conceitualmente um valor JSON nulo explícito (`NullNode`, por exemplo), sem depender de retorno Java nulo.

## CASE-003

- Ground Truth atual: `SHOULD_NOT_UPDATE`
- Snapshot alvo: `AuthorApiIntegrationTest.testGetAllAuthors_Snapshot.approved.txt`
- Implementabilidade: `QUESTIONABLE_REALISM`
- Arquivos mínimos: `src/main/java/com/example/pocapi/service/AuthorService.java`
- Tamanho: `MEDIUM`
- Alcance: `TARGET_ONLY` no conjunto atual, mas altera globalmente a semântica de listagem vazia.
- Observabilidade: `HIGH`; o fixture vazio passaria a devolver item.
- Determinismo: `HIGH` se o autor fallback for fixo.
- Realismo: `LOW`; devolver seed hardcoded como fallback de consulta é artificial neste domínio.
- Spurious Cue Risk: `MEDIUM`; código hardcoded pode denunciar que se trata de bug fabricado.
- Risco principal: modificar apenas `initData` não funciona porque `@BeforeEach` apaga os registros; a alternativa no serviço parece pouco natural.
- Recomendação: `REPLACE`
- Ground Truth Review Required: `NÃO`
- Justificativa: substituir por regressão plausível de filtro/isolamento que use dados reais, caso o fixture venha a conter itens; no fixture atual, não há versão pequena e realista equivalente.

## CASE-004

- Ground Truth atual: `SHOULD_UPDATE`
- Snapshot alvo: `AuthorApiIntegrationTest.testCreateAuthor_Snapshot.approved.txt`
- Implementabilidade: `IMPLEMENTABLE`
- Arquivos mínimos: `src/main/java/com/example/pocapi/model/dto/AuthorDTO.java`; `src/main/java/com/example/pocapi/service/AuthorService.java`
- Tamanho: `MEDIUM`
- Alcance: `MULTIPLE_SNAPSHOTS`; `convertToDTO` também atende GET por ID.
- Observabilidade: `HIGH`; `displayName` fica não nulo para Isaac e Tolkien.
- Determinismo: `HIGH`
- Realismo: `HIGH`
- Spurious Cue Risk: `HIGH`; adição intencional exige campo mais mapeamento, criando assinatura de diff de dois arquivos.
- Risco principal: se o campo não for preenchido, `NON_NULL` o omite; além disso, falharão criação e GET por ID.
- Recomendação: `KEEP_WITH_ADJUSTMENT`
- Ground Truth Review Required: `NÃO`
- Justificativa: registrar explicitamente o alcance múltiplo ou localizar a representação somente no endpoint alvo.

## CASE-005

- Ground Truth atual: `SHOULD_UPDATE`
- Snapshot alvo: `AuthorApiIntegrationTest.testCreateAuthor_Snapshot.approved.txt`
- Implementabilidade: `IMPLEMENTABLE`
- Arquivos mínimos: `src/main/java/com/example/pocapi/model/dto/AuthorDTO.java`
- Tamanho: `SMALL`
- Alcance: `MULTIPLE_SNAPSHOTS`; a serialização do DTO muda em POST e GET por ID, e também a entrada serializada pelo teste.
- Observabilidade: `HIGH`
- Determinismo: `HIGH`
- Realismo: `HIGH`
- Spurious Cue Risk: `MEDIUM`; anotação/rename pode sugerir evolução intencional.
- Risco principal: configurar apenas desserialização, e não serialização, preservaria a chave de saída.
- Recomendação: `KEEP_WITH_ADJUSTMENT`
- Ground Truth Review Required: `NÃO`
- Justificativa: é uma mudança pequena, mas a execução deve registrar todos os snapshots atingidos ou usar uma resposta específica.

## CASE-006

- Ground Truth atual: `SHOULD_NOT_UPDATE`
- Snapshot alvo: `AuthorApiIntegrationTest.testCreateAuthor_Snapshot.approved.txt`
- Implementabilidade: `IMPLEMENTABLE`
- Arquivos mínimos: `src/main/java/com/example/pocapi/service/AuthorService.java`
- Tamanho: `SMALL`
- Alcance: `MULTIPLE_SNAPSHOTS`; o mesmo mapper produz o GET por ID.
- Observabilidade: `HIGH`; os nomes dos fixtures são distintos.
- Determinismo: `HIGH`
- Realismo: `HIGH`; troca de propriedades `String` é erro plausível.
- Spurious Cue Risk: `LOW`
- Risco principal: o caso gera duas falhas se a suíte completa for executada.
- Recomendação: `KEEP_WITH_ADJUSTMENT`
- Ground Truth Review Required: `NÃO`
- Justificativa: manter o caso, mas decidir metodologicamente entre execução do teste alvo e registro do efeito múltiplo.

## CASE-007

- Ground Truth atual: `SHOULD_NOT_UPDATE`
- Snapshot alvo: `AuthorApiIntegrationTest.testCreateAuthor_Snapshot.approved.txt`
- Implementabilidade: `IMPLEMENTABLE`
- Arquivos mínimos: `src/main/java/com/example/pocapi/service/AuthorService.java`
- Tamanho: `SMALL`
- Alcance: `MULTIPLE_SNAPSHOTS`; o email some também no GET por ID.
- Observabilidade: `HIGH`; `NON_NULL` está confirmado em `AuthorDTO`.
- Determinismo: `HIGH`
- Realismo: `HIGH`
- Spurious Cue Risk: `LOW`
- Risco principal: alcance além do alvo, não falta de observabilidade.
- Recomendação: `KEEP_WITH_ADJUSTMENT`
- Ground Truth Review Required: `NÃO`
- Justificativa: forma par contrastivo forte com CASE-008 se ambos preservarem a mesma remoção textual.

## CASE-008

- Ground Truth atual: `SHOULD_UPDATE`
- Snapshot alvo: `AuthorApiIntegrationTest.testCreateAuthor_Snapshot.approved.txt`
- Implementabilidade: `IMPLEMENTABLE_WITH_RISK`
- Arquivos mínimos: `src/main/java/com/example/pocapi/service/AuthorService.java`
- Tamanho: `SMALL`
- Alcance: `MULTIPLE_SNAPSHOTS` na forma catalogada; remover do mapper afeta GET por ID.
- Observabilidade: `HIGH`
- Determinismo: `HIGH`
- Realismo: `HIGH`; minimização de dados é intenção plausível.
- Spurious Cue Risk: `HIGH`; se implementado por remoção de campo do DTO, pode parecer muito mais amplo que CASE-007.
- Risco principal: uma implementação estrutural ampla prejudica a comparabilidade e atinge outros snapshots.
- Recomendação: `KEEP_WITH_ADJUSTMENT`
- Ground Truth Review Required: `NÃO`
- Justificativa: usar a mesma forma mínima de omissão de CASE-007 e diferenciar os casos pela especificação de intenção, preservando o par contrastivo.

## CASE-009

- Ground Truth atual: `SHOULD_UPDATE`
- Snapshot alvo: `AuthorApiIntegrationTest.testGetAuthorById_Snapshot.approved.txt`
- Implementabilidade: `IMPLEMENTABLE_WITH_RISK`
- Arquivos mínimos: `src/main/java/com/example/pocapi/model/dto/AuthorDTO.java`; `src/main/java/com/example/pocapi/controller/AuthorController.java`
- Tamanho: `MEDIUM`
- Alcance: `TARGET_ONLY` se o novo campo for preenchido e os campos antigos anulados apenas em `getAuthorById`; caso contrário, `MULTIPLE_SNAPSHOTS`.
- Observabilidade: `HIGH`
- Determinismo: `HIGH`
- Realismo: `MEDIUM`; contratos diferentes de criação/leitura são possíveis, mas um DTO compartilhado torna a solução menos limpa.
- Spurious Cue Risk: `HIGH`; evolução de dois arquivos e nova propriedade pode sinalizar intenção.
- Risco principal: localizar a mudança exige manipular o DTO compartilhado ou criar representação específica.
- Recomendação: `KEEP_WITH_ADJUSTMENT`
- Ground Truth Review Required: `NÃO`
- Justificativa: explicitar que a implementação deve ser endpoint-specific e não alterar o snapshot de criação.

## CASE-010

- Ground Truth atual: `SHOULD_NOT_UPDATE`
- Snapshot alvo: `AuthorApiIntegrationTest.testGetAuthorById_Snapshot.approved.txt`
- Implementabilidade: `IMPLEMENTABLE_WITH_RISK`
- Arquivos mínimos: `src/main/java/com/example/pocapi/service/AuthorService.java`
- Tamanho: `SMALL`
- Alcance: `TARGET_ONLY` se o ID for corrompido após `convertToDTO` dentro de `getAuthorById`; `MULTIPLE_SNAPSHOTS` se o mapper for alterado.
- Observabilidade: `HIGH`
- Determinismo: `HIGH` com valor explicitamente errado.
- Realismo: `MEDIUM`
- Spurious Cue Risk: `LOW`
- Risco principal: usar outro ID gerado pode coincidir; alterar o mapper compartilhado atinge criação.
- Recomendação: `KEEP_WITH_ADJUSTMENT`
- Ground Truth Review Required: `NÃO`
- Justificativa: localizar em `getAuthorById` e escolher transformação determinística que não dependa de coincidência de sequências.

## CASE-011

- Ground Truth atual: `SHOULD_UPDATE`
- Snapshot alvo: `AuthorApiIntegrationTest.testGetAuthorById_Snapshot.approved.txt`
- Implementabilidade: `IMPLEMENTABLE`
- Arquivos mínimos: `src/main/java/com/example/pocapi/controller/AuthorController.java`
- Tamanho: `SMALL`
- Alcance: `TARGET_ONLY`; mascaramento pode ocorrer após retorno do serviço.
- Observabilidade: `HIGH`; o email do fixture contém caracteres suficientes e `@`.
- Determinismo: `HIGH`
- Realismo: `HIGH`
- Spurious Cue Risk: `MEDIUM`; utilitário/expressão de máscara pode revelar política intencional.
- Risco principal: uma máscara mal definida pode coincidir com o texto ou afetar também criação se colocada no mapper.
- Recomendação: `KEEP`
- Ground Truth Review Required: `NÃO`
- Justificativa: há implementação localizada, pequena e sustentada pelo fixture.

## CASE-012

- Ground Truth atual: `SHOULD_NOT_UPDATE`
- Snapshot alvo: `AuthorApiIntegrationTest.testGetAuthorById_Snapshot.approved.txt`
- Implementabilidade: `IMPLEMENTABLE`
- Arquivos mínimos: `src/main/java/com/example/pocapi/service/AuthorService.java`
- Tamanho: `SMALL`
- Alcance: `TARGET_ONLY` se `books` for inicializado em `getAuthorById` após o mapper.
- Observabilidade: `HIGH`; `NON_NULL` inclui listas vazias, pois não há `NON_EMPTY` configurado.
- Determinismo: `HIGH`
- Realismo: `HIGH`; inicialização automática de coleção é plausível.
- Spurious Cue Risk: `MEDIUM`; adição de `Collections.emptyList()` pode parecer deliberada.
- Risco principal: inserir a mudança no mapper compartilhado também afetaria criação.
- Recomendação: `KEEP`
- Ground Truth Review Required: `NÃO`
- Justificativa: o campo já existe e o fixture alcança a serialização.

## CASE-013

- Ground Truth atual: `SHOULD_UPDATE`
- Snapshot alvo: `AuthorApiIntegrationTest.testGetAuthorNotFound_Snapshot.approved.txt`
- Implementabilidade: `IMPLEMENTABLE`
- Arquivos mínimos: `src/main/java/com/example/pocapi/exception/ResourceNotFoundException.java`
- Tamanho: `SMALL`
- Alcance: `GLOBAL_BEHAVIOR` para mensagens de recursos ausentes, mas somente o erro de autor possui snapshot.
- Observabilidade: `HIGH`
- Determinismo: `HIGH`
- Realismo: `HIGH`
- Spurious Cue Risk: `MEDIUM`; padronização textual pode parecer intencional pelo escopo global.
- Risco principal: alterar a sobrecarga de construtor não utilizada não teria efeito; deve ser a `(String, Long)`.
- Recomendação: `KEEP`
- Ground Truth Review Required: `NÃO`
- Justificativa: fluxo e texto são diretos e reproduzíveis.

## CASE-014

- Ground Truth atual: `SHOULD_NOT_UPDATE`
- Snapshot alvo: `AuthorApiIntegrationTest.testGetAuthorNotFound_Snapshot.approved.txt`
- Implementabilidade: `IMPLEMENTABLE`
- Arquivos mínimos: `src/main/java/com/example/pocapi/service/AuthorService.java`
- Tamanho: `SMALL`
- Alcance: `TARGET_ONLY` no conjunto de snapshots.
- Observabilidade: `HIGH`; `Author` e `Book` são textos distintos.
- Determinismo: `HIGH`
- Realismo: `HIGH`; erro de copiar/colar é plausível.
- Spurious Cue Risk: `LOW`
- Risco principal: nenhum relevante além de garantir que a exceção específica continue sendo tratada.
- Recomendação: `KEEP`
- Ground Truth Review Required: `NÃO`
- Justificativa: par contrastivo válido com CASE-013 em torno do campo `message`.

## CASE-015

- Ground Truth atual: `SHOULD_UPDATE`
- Snapshot alvo: `AuthorApiIntegrationTest.testGetAuthorNotFound_Snapshot.approved.txt`
- Implementabilidade: `IMPLEMENTABLE`
- Arquivos mínimos: `src/main/java/com/example/pocapi/exception/GlobalExceptionHandler.java`
- Tamanho: `SMALL`
- Alcance: `GLOBAL_BEHAVIOR`; o formatador é usado por todos os handlers, embora só um erro seja snapshotado.
- Observabilidade: `HIGH`; o fixture temporal é fixo e a presença de `Z` muda o texto.
- Determinismo: `HIGH`
- Realismo: `HIGH`
- Spurious Cue Risk: `MEDIUM`; troca explícita de formatter/Instant sugere padronização.
- Risco principal: continuar usando `LocalDateTime` com formatter equivalente pode não acrescentar offset.
- Recomendação: `KEEP`
- Ground Truth Review Required: `NÃO`
- Justificativa: usar o `Clock` injetado preserva reprodutibilidade.

## CASE-016

- Ground Truth atual: `SHOULD_NOT_UPDATE`
- Snapshot alvo: `AuthorApiIntegrationTest.testGetAuthorNotFound_Snapshot.approved.txt`
- Implementabilidade: `IMPLEMENTABLE_WITH_RISK`
- Arquivos mínimos: `src/main/java/com/example/pocapi/exception/GlobalExceptionHandler.java`
- Tamanho: `SMALL`
- Alcance: `GLOBAL_BEHAVIOR`; todos os erros passam a usar tempo real.
- Observabilidade: `HIGH`; qualquer instante corrente difere do fixo de 2026-05-26.
- Determinismo: `LOW`; o texto recebido varia a cada execução.
- Realismo: `HIGH`; contornar um `Clock` injetado é regressão comum.
- Spurious Cue Risk: `LOW`
- Risco principal: o artefato exato não é reproduzível, apesar de a existência da falha ser reproduzível.
- Recomendação: `KEEP_WITH_ADJUSTMENT`
- Ground Truth Review Required: `NÃO`
- Justificativa: definir protocolo de duas execuções e registrar que a propriedade avaliada é a variabilidade indevida, não um timestamp específico.

## CASE-017

- Ground Truth atual: `SHOULD_UPDATE`
- Snapshot alvo: `AuthorApiIntegrationTest.testGetAuthorNotFound_Snapshot.approved.txt`
- Implementabilidade: `IMPLEMENTABLE`
- Arquivos mínimos: `src/main/java/com/example/pocapi/exception/ErrorResponse.java`
- Tamanho: `SMALL`
- Alcance: `GLOBAL_BEHAVIOR`; todos os erros serializados mudam, mas apenas um possui snapshot.
- Observabilidade: `HIGH`
- Determinismo: `HIGH`
- Realismo: `HIGH`
- Spurious Cue Risk: `MEDIUM`; rename/anotação é pista comum de evolução contratual.
- Risco principal: configurar somente alias de entrada não muda a chave de saída.
- Recomendação: `KEEP`
- Ground Truth Review Required: `NÃO`
- Justificativa: mutação pequena e diretamente verificável.

## CASE-018

- Ground Truth atual: `SHOULD_NOT_UPDATE`
- Snapshot alvo: `AuthorApiIntegrationTest.testGetAuthorNotFound_Snapshot.approved.txt`
- Implementabilidade: `IMPLEMENTABLE`
- Arquivos mínimos: `src/main/java/com/example/pocapi/exception/GlobalExceptionHandler.java`
- Tamanho: `SMALL`
- Alcance: `GLOBAL_BEHAVIOR` se o handler comum for alterado; somente um erro é snapshotado.
- Observabilidade: `HIGH`
- Determinismo: `HIGH` com path constante incorreto.
- Realismo: `HIGH`
- Spurious Cue Risk: `LOW`
- Risco principal: hardcode excessivamente óbvio reduziria realismo; preferir erro plausível de extração/normalização.
- Recomendação: `KEEP`
- Ground Truth Review Required: `NÃO`
- Justificativa: o campo está materializado e o request path é fixo.

## CASE-019

- Ground Truth atual: `SHOULD_UPDATE`
- Snapshot alvo: `BookApiIntegrationTest.testCreateBook_Snapshot.approved.txt`
- Implementabilidade: `IMPLEMENTABLE_WITH_RISK`
- Arquivos mínimos: `src/main/java/com/example/pocapi/model/dto/BookDTO.java`; `src/main/java/com/example/pocapi/service/BookService.java`
- Tamanho: `MEDIUM`
- Alcance: `MULTIPLE_SNAPSHOTS`; ambos os snapshots de livro usam `convertToDTO`.
- Observabilidade: `HIGH`
- Determinismo: `HIGH`
- Realismo: `HIGH`
- Spurious Cue Risk: `HIGH`; mudança intencional aninhada exige diff estrutural em dois arquivos.
- Risco principal: reutilizar entidade `Author` pode introduzir ciclo/Lazy state; deve ser representação DTO controlada.
- Recomendação: `KEEP_WITH_ADJUSTMENT`
- Ground Truth Review Required: `NÃO`
- Justificativa: especificar DTO aninhado mínimo e aceitar/registrar o efeito nos dois snapshots de livro.

## CASE-020

- Ground Truth atual: `SHOULD_UPDATE`
- Snapshot alvo: `BookApiIntegrationTest.testCreateBook_Snapshot.approved.txt`
- Implementabilidade: `IMPLEMENTABLE_WITH_RISK`
- Arquivos mínimos: `src/main/java/com/example/pocapi/service/BookService.java`
- Tamanho: `SMALL`
- Alcance: `MULTIPLE_SNAPSHOTS`; os livros do teste de coleção também são criados por `createBook` e contêm hífens.
- Observabilidade: `HIGH`; todos os ISBNs do fixture têm hífens.
- Determinismo: `HIGH`
- Realismo: `HIGH`
- Spurious Cue Risk: `MEDIUM`; função de normalização pode sinalizar intenção.
- Risco principal: normalizar somente para consulta de duplicidade não altera o retorno; persistir normalizado altera dois snapshots.
- Recomendação: `KEEP_WITH_ADJUSTMENT`
- Ground Truth Review Required: `NÃO`
- Justificativa: documentar alcance múltiplo ou restringir a mudança à representação de criação, se isso ainda respeitar a intenção revisada.

## CASE-021

- Ground Truth atual: `SHOULD_NOT_UPDATE`
- Snapshot alvo: `BookApiIntegrationTest.testCreateBook_Snapshot.approved.txt`
- Implementabilidade: `IMPLEMENTABLE`
- Arquivos mínimos: `src/main/java/com/example/pocapi/service/BookService.java`
- Tamanho: `SMALL`
- Alcance: `MULTIPLE_SNAPSHOTS`; `authorName` muda nos dois snapshots de livro.
- Observabilidade: `HIGH`; `Arthur` e `Conan Doyle` são distintos.
- Determinismo: `HIGH`
- Realismo: `HIGH`
- Spurious Cue Risk: `LOW`
- Risco principal: a suíte completa produzirá mais de uma falha.
- Recomendação: `KEEP_WITH_ADJUSTMENT`
- Ground Truth Review Required: `NÃO`
- Justificativa: a mutação é clara; o protocolo deve registrar o alcance ou localizar o caso.

## CASE-022

- Ground Truth atual: `SHOULD_NOT_UPDATE`
- Snapshot alvo: `BookApiIntegrationTest.testCreateBook_Snapshot.approved.txt`
- Implementabilidade: `IMPLEMENTABLE_WITH_RISK`
- Arquivos mínimos: `src/main/java/com/example/pocapi/service/BookService.java`
- Tamanho: `SMALL`
- Alcance: `MULTIPLE_SNAPSHOTS`; o mapper é compartilhado.
- Observabilidade: `MEDIUM`; no baseline `book.id=3` e `author.id=6`, mas ambos são IDs gerados.
- Determinismo: `MEDIUM`; a auditoria mostrou estabilidade, não garantia semântica de não coincidência.
- Realismo: `HIGH`; confusão de identificadores do mesmo tipo é plausível.
- Spurious Cue Risk: `LOW`
- Risco principal: IDs podem coincidir em outro estado, eliminando o diff; também afeta a coleção.
- Recomendação: `KEEP_WITH_ADJUSTMENT`
- Ground Truth Review Required: `NÃO`
- Justificativa: usar transformação errada determinística ou validar previamente que os valores continuam distintos na execução isolada.

## CASE-023

- Ground Truth atual: `SHOULD_NOT_UPDATE`
- Snapshot alvo: `BookApiIntegrationTest.testCreateBook_Snapshot.approved.txt`
- Implementabilidade: `IMPLEMENTABLE`
- Arquivos mínimos: `src/main/java/com/example/pocapi/service/BookService.java`
- Tamanho: `SMALL`
- Alcance: `MULTIPLE_SNAPSHOTS`; ISBN some de todos os `BookDTO` mapeados.
- Observabilidade: `HIGH`; `NON_NULL` e ISBNs não nulos estão confirmados.
- Determinismo: `HIGH`
- Realismo: `HIGH`
- Spurious Cue Risk: `LOW`
- Risco principal: múltiplas falhas de snapshot, não fragilidade do diff.
- Recomendação: `KEEP_WITH_ADJUSTMENT`
- Ground Truth Review Required: `NÃO`
- Justificativa: mutação representativa, mas o alcance deve ser explícito.

## CASE-024

- Ground Truth atual: `SHOULD_UPDATE`
- Snapshot alvo: `BookApiIntegrationTest.testCreateBook_Snapshot.approved.txt`
- Implementabilidade: `IMPLEMENTABLE_WITH_RISK`
- Arquivos mínimos: `src/main/java/com/example/pocapi/service/BookService.java`
- Tamanho: `SMALL`
- Alcance: `MULTIPLE_SNAPSHOTS`; o mapper compartilhado adiciona `reviews:[]` em cada item da coleção.
- Observabilidade: `HIGH`; `@JsonInclude(NON_NULL)` inclui coleção vazia e não há configuração contrária.
- Determinismo: `HIGH`
- Realismo: `HIGH`
- Spurious Cue Risk: `HIGH`; adição deliberada e efeito repetido no array podem tornar a intenção superficialmente evidente.
- Risco principal: o caso alvo não é isolado; o diff da coleção fica maior que o da criação.
- Recomendação: `KEEP_WITH_ADJUSTMENT`
- Ground Truth Review Required: `NÃO`
- Justificativa: preencher `reviews` somente na resposta de criação ou assumir formalmente o efeito múltiplo.

## CASE-025

- Ground Truth atual: `SHOULD_UPDATE`
- Snapshot alvo: `BookApiIntegrationTest.testGetBooksByAuthor_Snapshot.approved.txt`
- Implementabilidade: `IMPLEMENTABLE`
- Arquivos mínimos: `src/main/java/com/example/pocapi/repository/BookRepository.java`
- Tamanho: `SMALL`
- Alcance: `TARGET_ONLY`; somente o endpoint por autor usa `findByAuthorId`.
- Observabilidade: `HIGH`; IDs 1 e 2 são distintos e a ordem aprovada é ascendente.
- Determinismo: `HIGH` com ordenação explícita descendente.
- Realismo: `HIGH`
- Spurious Cue Risk: `MEDIUM`; nome de consulta `OrderBy...Desc` revela ordenação deliberada.
- Risco principal: depende da identidade representar recência; ainda assim, o fixture atual é reproduzível no baseline.
- Recomendação: `KEEP`
- Ground Truth Review Required: `NÃO`
- Justificativa: alteração pequena, localizada e par contrastivo forte com CASE-026.

## CASE-026

- Ground Truth atual: `SHOULD_NOT_UPDATE`
- Snapshot alvo: `BookApiIntegrationTest.testGetBooksByAuthor_Snapshot.approved.txt`
- Implementabilidade: `IMPLEMENTABLE`
- Arquivos mínimos: `src/main/java/com/example/pocapi/service/BookService.java`
- Tamanho: `SMALL`
- Alcance: `TARGET_ONLY`
- Observabilidade: `HIGH`; há dois objetos diferentes.
- Determinismo: `HIGH` se a reversão for explícita após a consulta.
- Realismo: `HIGH`; refatoração que inverte ordem é plausível.
- Spurious Cue Risk: `LOW`
- Risco principal: a ordem original da consulta não é contratualmente garantida; a mutação deve forçar reversão do resultado observado, não depender do banco.
- Recomendação: `KEEP_WITH_ADJUSTMENT`
- Ground Truth Review Required: `NÃO`
- Justificativa: implementar diferença equivalente à de CASE-025 para preservar comparabilidade, mas sem regra intencional.

## CASE-027

- Ground Truth atual: `SHOULD_NOT_UPDATE`
- Snapshot alvo: `BookApiIntegrationTest.testGetBooksByAuthor_Snapshot.approved.txt`
- Implementabilidade: `IMPLEMENTABLE`
- Arquivos mínimos: `src/main/java/com/example/pocapi/service/BookService.java`
- Tamanho: `SMALL`
- Alcance: `TARGET_ONLY`
- Observabilidade: `HIGH`; um terceiro item repetido altera o array.
- Determinismo: `HIGH`
- Realismo: `MEDIUM`; duplicação por agregação/junção é plausível, mas duplicação manual seria artificial.
- Spurious Cue Risk: `LOW`
- Risco principal: uma implementação com `distinct` ou coleção de conjunto neutralizaria o bug.
- Recomendação: `KEEP_WITH_ADJUSTMENT`
- Ground Truth Review Required: `NÃO`
- Justificativa: formular como duplicação de processamento/consulta, evitando `list.add(list.get(0))` excessivamente óbvio.

## CASE-028

- Ground Truth atual: `SHOULD_NOT_UPDATE`
- Snapshot alvo: `BookApiIntegrationTest.testGetBooksByAuthor_Snapshot.approved.txt`
- Implementabilidade: `IMPLEMENTABLE`
- Arquivos mínimos: `src/main/java/com/example/pocapi/service/BookService.java`
- Tamanho: `SMALL`
- Alcance: `TARGET_ONLY`
- Observabilidade: `HIGH`; o fixture tem dois itens distintos.
- Determinismo: `HIGH`
- Realismo: `HIGH`; limite/paginação/filtro incorreto é comum.
- Spurious Cue Risk: `LOW`
- Risco principal: o filtro deve remover exatamente um item e preservar resposta 200.
- Recomendação: `KEEP`
- Ground Truth Review Required: `NÃO`
- Justificativa: há várias implementações pequenas e plausíveis sobre a lista real.

## CASE-029

- Ground Truth atual: `SHOULD_UPDATE`
- Snapshot alvo: `BookApiIntegrationTest.testGetBooksByAuthor_Snapshot.approved.txt`
- Implementabilidade: `IMPLEMENTABLE`
- Arquivos mínimos: `src/main/java/com/example/pocapi/controller/BookController.java`
- Tamanho: `SMALL`
- Alcance: `TARGET_ONLY`
- Observabilidade: `HIGH`; array raiz se torna objeto com `books` e `count`.
- Determinismo: `HIGH`
- Realismo: `HIGH`
- Spurious Cue Risk: `MEDIUM`; envelope e contagem são sinais de evolução intencional.
- Risco principal: mudar somente o tipo declarado não altera o objeto serializado.
- Recomendação: `KEEP`
- Ground Truth Review Required: `NÃO`
- Justificativa: evolução localizada e sustentada pelos dois itens do fixture.

## CASE-030

- Ground Truth atual: `SHOULD_UPDATE`
- Snapshot alvo: `BookApiIntegrationTest.testGetBooksByAuthor_Snapshot.approved.txt`
- Implementabilidade: `QUESTIONABLE_REALISM`
- Arquivos mínimos: `src/main/java/com/example/pocapi/service/BookService.java`
- Tamanho: `SMALL`
- Alcance: `TARGET_ONLY`
- Observabilidade: `HIGH`; somente o primeiro título começa com `Sherlock`.
- Determinismo: `HIGH`
- Realismo: `LOW`; filtrar implicitamente uma rota “by-author” por prefixo fixo não é suportado pelo contrato nem por parâmetro.
- Spurious Cue Risk: `MEDIUM`; literal `Sherlock` no diff denuncia adequação ao fixture.
- Risco principal: caso excessivamente fixture-specific e artificial, embora tecnicamente simples.
- Recomendação: `REPLACE`
- Ground Truth Review Required: `NÃO`
- Justificativa: substituir por regra de domínio apoiada em campo/parâmetro real; no baseline atual, não há tal critério na rota, portanto a substituição pode exigir revisão do catálogo.

Nenhum Ground Truth mostrou incoerência com a intenção descrita; não há marcação `GROUND_TRUTH_REVIEW_REQUIRED`.

## 4. Pares contrastivos

| Par | Diferença semelhante | GT A | GT B | Validade |
|---|---|---|---|---|
| CASE-007 / CASE-008 | Omissão de `email` no JSON de autor | SHOULD_NOT_UPDATE: perda acidental | SHOULD_UPDATE: minimização deliberada | `CONTRASTIVE_PAIR`; alta validade se ambos usarem a mesma mutação mínima e o mesmo snapshot |
| CASE-013 / CASE-014 | Mudança no campo `message` do erro 404 | SHOULD_UPDATE: padronização aprovada | SHOULD_NOT_UPDATE: recurso incorreto | `CONTRASTIVE_PAIR`; comparável no campo, embora os textos finais sejam diferentes |
| CASE-025 / CASE-026 | Inversão da ordem dos mesmos dois livros | SHOULD_UPDATE: “mais recente primeiro” aprovada | SHOULD_NOT_UPDATE: inversão acidental | `CONTRASTIVE_PAIR`; validade alta se o diff final for exatamente a mesma ordem 2,1 |
| CASE-012 / CASE-024 | Surgimento de propriedade com coleção vazia sob `NON_NULL` | SHOULD_NOT_UPDATE: exposição acidental de `books` | SHOULD_UPDATE: exposição deliberada de `reviews` | `CONTRASTIVE_PAIR`; validade média por usar DTOs e snapshots diferentes |
| CASE-001 / CASE-029 | Envelope JSON com coleção e contagem | SHOULD_UPDATE | SHOULD_UPDATE | Não é contrastivo; é redundância de mecanismo e deve ser balanceada no conjunto executado |

Os três primeiros pares devem ter prioridade. A comparabilidade só será preservada se tamanho, número de arquivos e forma observável do diff forem mantidos próximos; intenção e Ground Truth ficam no artefato reservado do benchmark, não no input da LLM.

## 5. Casos com efeito em múltiplos snapshots

| Casos | Motivo | Snapshots adicionais prováveis |
|---|---|---|
| CASE-004 a CASE-008 | `AuthorDTO`/`AuthorService.convertToDTO` são compartilhados | CreateAuthor e GetAuthorById; GetAllAuthors somente se tiver itens, o que não ocorre no fixture atual |
| CASE-009 | Campo novo no DTO é global, embora possa ficar nulo fora do GET | CreateAuthor se o campo for preenchido globalmente |
| CASE-010 | Alteração no mapper seria global; localização em `getAuthorById` evita isso | CreateAuthor se implementado em `convertToDTO` |
| CASE-013, CASE-015, CASE-017, CASE-018 | Exceção/handler/ErrorResponse atendem erros globais | Não há outro snapshot de erro atual, mas o comportamento da aplicação muda globalmente |
| CASE-019 a CASE-024 | `BookService.convertToDTO` e criação de livros são usados pelos dois testes | CreateBook e GetBooksByAuthor |
| CASE-025 a CASE-030 | Consulta/serviço/controller da rota por autor | Normalmente somente GetBooksByAuthor |

Os casos de mapper compartilhado não devem ser descartados, mas o protocolo precisa escolher entre mutação localizada e coleta explícita de todas as falhas geradas.

## 6. Casos dependentes de fixture

- CASE-002 depende da forma como Spring serializa ausência/nulo; deve usar JSON nulo explícito.
- CASE-003 depende de reintroduzir item depois da limpeza; o caminho proposto é artificial.
- CASE-004 depende de preencher o novo campo; `NON_NULL` omite campo declarado e nulo.
- CASE-006 e CASE-021 dependem de valores distintos; os fixtures atuais satisfazem essa condição.
- CASE-010 e CASE-022 dependem de IDs não coincidirem se usarem outro ID gerado; devem evitar essa coincidência.
- CASE-011 depende de email mascarável; `tolkien@example.com` é adequado.
- CASE-012 e CASE-024 dependem de `NON_NULL` incluir listas vazias; o código usa `NON_NULL`, não `NON_EMPTY`, e não há override configurado.
- CASE-016 depende de tempo real; a falha é certa, mas o valor exato é variável.
- CASE-020 depende de hífens; os três ISBNs usados pelos testes de livros possuem hífens.
- CASE-025 e CASE-026 dependem de dois itens/IDs distintos; o snapshot possui IDs 1 e 2.
- CASE-027 e CASE-028 dependem de dois itens; o fixture cria exatamente dois.
- CASE-030 depende literalmente de `Sherlock` versus `The Sign of the Four`, o que reduz realismo.

## 7. Casos que precisam de ajuste

| Caso | Correção conceitual recomendada |
|---|---|
| CASE-002 | Exigir serialização explícita de JSON `null`, sem confiar em `ResponseEntity` com referência Java nula. |
| CASE-004 a CASE-008 | Declarar alcance múltiplo ou localizar a mutação; para CASE-007/008, usar a mesma forma de diff. |
| CASE-009 | Tornar a representação específica do GET por ID, evitando alterar criação. |
| CASE-010 | Corromper o ID após o mapper, somente no GET, com valor deterministicamente diferente. |
| CASE-016 | Executar repetidamente e avaliar a variabilidade, não o timestamp literal. |
| CASE-019 | Usar DTO aninhado mínimo, nunca entidade JPA direta. |
| CASE-020 | Assumir efeito nos dois snapshots ou redefinir a intenção como transformação apenas da resposta criada. |
| CASE-021, CASE-023, CASE-024 | Localizar ou registrar explicitamente as duas falhas de livro. |
| CASE-022 | Evitar depender de IDs gerados coincidirem ou não. |
| CASE-026 | Forçar reversão sobre uma ordem de entrada conhecida para reproduzir o par com CASE-025. |
| CASE-027 | Modelar duplicação por processamento/consulta plausível, não por adição manual óbvia. |

## 8. Casos recomendados para remoção/substituição

- CASE-003: substituir. O fallback de autor seed em listagem vazia é pouco plausível e exige comportamento artificial depois da limpeza.
- CASE-030: substituir. O filtro hardcoded por prefixo `Sherlock` é orientado ao fixture e não ao contrato `/books/by-author/{authorId}`.

Nenhum caso precisa ser removido por impossibilidade técnica. As duas substituições devem preservar o balanço atual de Ground Truth e dificuldade, se isso puder ser feito sem artificialidade.

## 9. Risco de pistas espúrias

Há desequilíbrios evidentes:

- Categoria versus Ground Truth: todos os 7 `CONTRACT_EVOLUTION`, 2 `BREAKING_CHANGE` e 3 `BUSINESS_RULE` são `SHOULD_UPDATE`; todos os 6 `BUG` e o único `NON_DETERMINISTIC` são `SHOULD_NOT_UPDATE`. Se categoria ou descrição equivalente chegar à LLM, torna-se pista quase direta. O schema atual de `llm-input` não inclui categoria, o que reduz, mas não elimina inferência pelo diff.
- Tamanho/arquivos: várias evoluções intencionais (CASE-004, CASE-009, CASE-019) exigem dois arquivos, enquanto muitos bugs são troca/omissão de uma linha. Isso pode correlacionar diff maior com `SHOULD_UPDATE`.
- Tipo de mutação: adições de DTO, envelopes e annotations concentram-se em `SHOULD_UPDATE`; trocas de valor, null e filtros acidentais concentram-se em `SHOULD_NOT_UPDATE`.
- Dificuldade: dos 8 casos `HARD`, 6 são `SHOULD_UPDATE` e 2 são `SHOULD_NOT_UPDATE`; casos `EASY` concentram bugs simples. A distribuição pode virar pista indireta se complexidade do diff for visível.
- Quantidade de arquivos: os pares CASE-007/008 e CASE-025/026 podem reduzir esse viés se implementados com diffs mecanicamente comparáveis.

Recomendação global: antes de selecionar o conjunto executado, balancear formas de diff dentro de cada Ground Truth, não apenas as contagens 15/15. Incluir evoluções intencionais de uma linha e regressões realistas de dois arquivos, sem inflar artificialmente patches. Não enviar categoria, intenção, dificuldade, ID de caso ou Ground Truth no `llm-input`.

## 10. Catálogo recomendado

| CASE | Recomendação | Implementabilidade | GT | Dificuldade |
|---|---|---|---|---|
| CASE-001 | KEEP | IMPLEMENTABLE | SHOULD_UPDATE | MEDIUM |
| CASE-002 | KEEP_WITH_ADJUSTMENT | IMPLEMENTABLE_WITH_RISK | SHOULD_NOT_UPDATE | EASY |
| CASE-003 | REPLACE | QUESTIONABLE_REALISM | SHOULD_NOT_UPDATE | HARD |
| CASE-004 | KEEP_WITH_ADJUSTMENT | IMPLEMENTABLE | SHOULD_UPDATE | MEDIUM |
| CASE-005 | KEEP_WITH_ADJUSTMENT | IMPLEMENTABLE | SHOULD_UPDATE | EASY |
| CASE-006 | KEEP_WITH_ADJUSTMENT | IMPLEMENTABLE | SHOULD_NOT_UPDATE | EASY |
| CASE-007 | KEEP_WITH_ADJUSTMENT | IMPLEMENTABLE | SHOULD_NOT_UPDATE | EASY |
| CASE-008 | KEEP_WITH_ADJUSTMENT | IMPLEMENTABLE_WITH_RISK | SHOULD_UPDATE | HARD |
| CASE-009 | KEEP_WITH_ADJUSTMENT | IMPLEMENTABLE_WITH_RISK | SHOULD_UPDATE | MEDIUM |
| CASE-010 | KEEP_WITH_ADJUSTMENT | IMPLEMENTABLE_WITH_RISK | SHOULD_NOT_UPDATE | EASY |
| CASE-011 | KEEP | IMPLEMENTABLE | SHOULD_UPDATE | HARD |
| CASE-012 | KEEP | IMPLEMENTABLE | SHOULD_NOT_UPDATE | MEDIUM |
| CASE-013 | KEEP | IMPLEMENTABLE | SHOULD_UPDATE | EASY |
| CASE-014 | KEEP | IMPLEMENTABLE | SHOULD_NOT_UPDATE | EASY |
| CASE-015 | KEEP | IMPLEMENTABLE | SHOULD_UPDATE | MEDIUM |
| CASE-016 | KEEP_WITH_ADJUSTMENT | IMPLEMENTABLE_WITH_RISK | SHOULD_NOT_UPDATE | HARD |
| CASE-017 | KEEP | IMPLEMENTABLE | SHOULD_UPDATE | MEDIUM |
| CASE-018 | KEEP | IMPLEMENTABLE | SHOULD_NOT_UPDATE | MEDIUM |
| CASE-019 | KEEP_WITH_ADJUSTMENT | IMPLEMENTABLE_WITH_RISK | SHOULD_UPDATE | HARD |
| CASE-020 | KEEP_WITH_ADJUSTMENT | IMPLEMENTABLE_WITH_RISK | SHOULD_UPDATE | MEDIUM |
| CASE-021 | KEEP_WITH_ADJUSTMENT | IMPLEMENTABLE | SHOULD_NOT_UPDATE | EASY |
| CASE-022 | KEEP_WITH_ADJUSTMENT | IMPLEMENTABLE_WITH_RISK | SHOULD_NOT_UPDATE | MEDIUM |
| CASE-023 | KEEP_WITH_ADJUSTMENT | IMPLEMENTABLE | SHOULD_NOT_UPDATE | EASY |
| CASE-024 | KEEP_WITH_ADJUSTMENT | IMPLEMENTABLE_WITH_RISK | SHOULD_UPDATE | MEDIUM |
| CASE-025 | KEEP | IMPLEMENTABLE | SHOULD_UPDATE | HARD |
| CASE-026 | KEEP_WITH_ADJUSTMENT | IMPLEMENTABLE | SHOULD_NOT_UPDATE | MEDIUM |
| CASE-027 | KEEP_WITH_ADJUSTMENT | IMPLEMENTABLE | SHOULD_NOT_UPDATE | MEDIUM |
| CASE-028 | KEEP | IMPLEMENTABLE | SHOULD_NOT_UPDATE | MEDIUM |
| CASE-029 | KEEP | IMPLEMENTABLE | SHOULD_UPDATE | HARD |
| CASE-030 | REPLACE | QUESTIONABLE_REALISM | SHOULD_UPDATE | HARD |

## 11. Veredito

`CATALOG_READY_FOR_REVIEW`

O catálogo pode seguir para revisão humana, mas CASE-003 e CASE-030 devem ser substituídos, e os casos marcados `KEEP_WITH_ADJUSTMENT` precisam ter alcance/fixture definidos antes de qualquer implementação.
