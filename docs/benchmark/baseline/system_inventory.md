# Inventário factual do sistema no baseline

## 1. Identificação do baseline

- Tag: `benchmark-v2-baseline`
- SHA: `8316d9ffa0c109c0aac68fd181b94fdd9dce368e`
- Branch observada: `main`
- Data da análise: `2026-08-09T17:07:36.8162639-03:00`
- Estado inicial: working tree limpo; a tag aponta para o HEAD analisado.

## 2. Resumo

| Medida | Quantidade | Critério factual |
|---|---:|---|
| Testes totais | 18 | Métodos anotados com `@Test` em `src/test/java` |
| Testes de snapshot | 6 | Chamadas diretas a `Approvals.verify(responseBody)` |
| Snapshots aprovados | 6 | Arquivos-fonte `*.approved.txt` em `src/test` |
| Recursos cobertos | 2 | `authors` e `books` |
| Combinações rota + método cobertas | 5 | GET/POST de autores e GET/POST de livros; GET `/authors/{id}` tem dois cenários |
| Cenários HTTP snapshotados | 6 | Cinco sucessos/coleções e um erro 404 |

Há 17 combinações rota + método declaradas pelos três controllers. Doze não possuem snapshot. Somente os seis testes listados abaixo foram considerados testes de snapshot; nomes de testes sem `Approvals.verify(...)` não foram usados como evidência.

## 3. Inventário dos snapshots

| Classe e método | Teste | Arquivo aprovado | Endpoint | HTTP | Payload de entrada | Status validado | Produção do snapshot |
|---|---|---|---|---|---|---|---|
| `AuthorApiIntegrationTest.testGetAllAuthors_Snapshot` | `src/test/java/com/example/pocapi/integration/AuthorApiIntegrationTest.java:53-66` | `AuthorApiIntegrationTest.testGetAllAuthors_Snapshot.approved.txt` | `/authors` | GET | Nenhum body; request define `Content-Type: application/json` | 200 (`isOk`) | `getContentAsString()` do response body, seguido de `Approvals.verify(responseBody)` |
| `AuthorApiIntegrationTest.testCreateAuthor_Snapshot` | mesmo arquivo, linhas 68-89 | `AuthorApiIntegrationTest.testCreateAuthor_Snapshot.approved.txt` | `/authors` | POST | JSON de `AuthorDTO`: `firstName=Isaac`, `lastName=Asimov`, `email=isaac@example.com`; nulos omitidos | 201 (`isCreated`) | Mesma sequência: somente response body convertido em `String` |
| `AuthorApiIntegrationTest.testGetAuthorById_Snapshot` | mesmo arquivo, linhas 91-120 | `AuthorApiIntegrationTest.testGetAuthorById_Snapshot.approved.txt` | `/authors/{id}` | GET | O arranjo faz POST de J.R.R. Tolkien; o GET não possui body | 201 no POST de arranjo e 200 (`isOk`) no GET | Somente o response body do GET é enviado ao ApprovalTests |
| `AuthorApiIntegrationTest.testGetAuthorNotFound_Snapshot` | mesmo arquivo, linhas 122-135 | `AuthorApiIntegrationTest.testGetAuthorNotFound_Snapshot.approved.txt` | `/authors/99999` | GET | Nenhum body | 404 (`isNotFound`) | Somente o response body de erro é enviado ao ApprovalTests |
| `BookApiIntegrationTest.testCreateBook_Snapshot` | `src/test/java/com/example/pocapi/integration/BookApiIntegrationTest.java:73-94` | `BookApiIntegrationTest.testCreateBook_Snapshot.approved.txt` | `/books` | POST | JSON de `BookDTO`: título `The Hound of the Baskervilles`, ISBN `978-0-14-043926-8`, `authorId` criado no `setUp` | 201 (`isCreated`) | Somente o response body convertido em `String` |
| `BookApiIntegrationTest.testGetBooksByAuthor_Snapshot` | mesmo arquivo, linhas 96-132 | `BookApiIntegrationTest.testGetBooksByAuthor_Snapshot.approved.txt` | `/books/by-author/{authorId}` | GET | O arranjo faz dois POSTs de livros; o GET não possui body | 201 nos dois POSTs de arranjo e 200 (`isOk`) no GET | Somente o response body do GET é enviado ao ApprovalTests |

Ambas as classes executam `reviewRepository.deleteAll()`, `bookRepository.deleteAll()` e `authorRepository.deleteAll()` antes de cada teste. O `setUp` de livros também cria um autor por `POST /authors`.

## 4. Rastreamento ponta a ponta

### `AuthorApiIntegrationTest.testGetAllAuthors_Snapshot`

```text
AuthorApiIntegrationTest.testGetAllAuthors_Snapshot (linhas 53-65)
  -> GET /authors via MockMvc
  -> AuthorController.getAllAuthors() (linhas 19-23)
  -> AuthorService.getAllAuthors() (linhas 45-50)
  -> AuthorRepository.findAll() [JpaRepository<Author, Long>]
  -> List<Author>
  -> AuthorService.convertToDTO(Author) (linhas 122-129), se houver itens
  -> List<AuthorDTO>
  -> Jackson/Spring MVC serializa o body
  -> result.getResponse().getContentAsString()
  -> Approvals.verify(responseBody)
```

No baseline, o `setUp` remove todos os autores e o snapshot é `[]`; portanto, `convertToDTO` não é invocado para item algum nessa execução observada.

### `AuthorApiIntegrationTest.testCreateAuthor_Snapshot`

```text
AuthorDTO de entrada -> Jackson (ObjectMapper) -> POST /authors
  -> AuthorController.createAuthor(AuthorDTO) (linhas 31-35)
  -> AuthorService.createAuthor(AuthorDTO) (linhas 58-75)
  -> validateAuthorDTO(...)
  -> AuthorRepository.findByEmail(...)
  -> Author [firstName, lastName, email]
  -> AuthorRepository.save(...)
  -> AuthorService.convertToDTO(...) (linhas 122-129)
  -> AuthorDTO -> Jackson/Spring MVC -> JSON response body
  -> getContentAsString() -> Approvals.verify(responseBody)
```

### `AuthorApiIntegrationTest.testGetAuthorById_Snapshot`

```text
POST /authors de arranjo
  -> mesmo fluxo de criação de autor acima
  -> ObjectMapper.readValue(..., AuthorDTO.class) obtém o id
GET /authors/{id}
  -> AuthorController.getAuthorById(Long) (linhas 25-29)
  -> AuthorService.getAuthorById(Long) (linhas 52-56)
  -> AuthorRepository.findById(...)
  -> Author
  -> AuthorService.convertToDTO(...)
  -> AuthorDTO -> Jackson/Spring MVC -> JSON response body
  -> getContentAsString() -> Approvals.verify(responseBody)
```

### `AuthorApiIntegrationTest.testGetAuthorNotFound_Snapshot`

```text
GET /authors/99999
  -> AuthorController.getAuthorById(99999)
  -> AuthorService.getAuthorById(99999)
  -> AuthorRepository.findById(99999) retorna vazio
  -> ResourceNotFoundException("Author", 99999)
  -> GlobalExceptionHandler.handleResourceNotFound(...), linhas 23-33
  -> ErrorResponse [status, message, timestamp, path]
  -> timestamp usa Clock fixo de TestTimeConfig, em UTC
  -> Jackson/Spring MVC -> JSON response body
  -> getContentAsString() -> Approvals.verify(responseBody)
```

### `BookApiIntegrationTest.testCreateBook_Snapshot`

```text
setUp: POST /authors -> fluxo AuthorController/AuthorService/AuthorRepository
BookDTO de entrada -> Jackson -> POST /books
  -> BookController.createBook(BookDTO) (linhas 37-41)
  -> BookService.createBook(BookDTO) (linhas 49-69)
  -> validateBookDTO(...)
  -> AuthorRepository.findById(authorId)
  -> BookRepository.findByIsbn(...)
  -> Book [title, isbn, relação Author]
  -> BookRepository.save(...)
  -> BookService.convertToDTO(...) (linhas 116-123)
  -> BookDTO [id, title, isbn, authorId, authorName]
  -> Jackson/Spring MVC -> JSON response body
  -> getContentAsString() -> Approvals.verify(responseBody)
```

### `BookApiIntegrationTest.testGetBooksByAuthor_Snapshot`

```text
setUp: POST /authors -> autor persistido
dois POST /books de arranjo
  -> BookController.createBook -> BookService.createBook -> repositórios -> Book
GET /books/by-author/{authorId}
  -> BookController.getBooksByAuthorId(Long) (linhas 31-35)
  -> BookService.getBooksByAuthorId(Long) (linhas 38-47)
  -> AuthorRepository.findById(authorId) valida a existência
  -> BookRepository.findByAuthorId(authorId)
  -> List<Book>
  -> BookService.convertToDTO(...) para cada item
  -> List<BookDTO> -> Jackson/Spring MVC -> JSON array
  -> getContentAsString() -> Approvals.verify(responseBody)
```

## 5. Estrutura dos snapshots

### `AuthorApiIntegrationTest.testGetAllAuthors_Snapshot.approved.txt`

- JSON: array vazio `[]`.
- Objetos/campos/tipos: nenhum item presente; a estrutura de um item não é capturada neste arquivo.
- Ordem: não observável com zero itens. `findAll()` não recebe `Sort`, e não há ordenação explícita no serviço.
- Valores potencialmente não determinísticos: nenhum valor materializado no snapshot atual.

### `AuthorApiIntegrationTest.testCreateAuthor_Snapshot.approved.txt`

- JSON: objeto plano.
- Campos, na ordem observada: `id` (número), `firstName`, `lastName`, `email` (strings).
- Valores: `3`, `Isaac`, `Asimov`, `isaac@example.com`.
- `books` não aparece porque `AuthorService.convertToDTO` não o preenche e `AuthorDTO` usa `@JsonInclude(NON_NULL)`.
- `id` é gerado por persistência com `GenerationType.IDENTITY`; foi estável nas validações do baseline, mas depende do estado/sequência do banco no contexto de teste.
- Não há timestamp nem objeto aninhado.

### `AuthorApiIntegrationTest.testGetAuthorById_Snapshot.approved.txt`

- JSON: objeto plano com os mesmos quatro campos e tipos do snapshot de criação.
- Valores: `id=4`, `firstName="J.R.R."`, `lastName="Tolkien"`, `email="tolkien@example.com"`.
- Mesmas observações sobre `books`, identidade persistida e ordem de propriedades sem anotação explícita `@JsonPropertyOrder`.

### `AuthorApiIntegrationTest.testGetAuthorNotFound_Snapshot.approved.txt`

- JSON: objeto plano de erro.
- Campos: `status` (string `"404"`), `message` (string), `timestamp` (string) e `path` (string).
- Mensagem: `Author not found with id: 99999`.
- Timestamp: `2026-05-26T13:25:34.6903399`; em testes vem do `Clock.fixed` UTC definido por `TestTimeConfig`. Fora do perfil de teste, `TimeConfig.clock()` fornece `Clock.systemDefaultZone()`; isso não altera a evidência do baseline de teste.
- Path: `/authors/99999`, derivado de `WebRequest.getDescription(false)` após remoção de `uri=`.
- O status dentro do JSON é string e é distinto do status HTTP 404 validado pelo teste.

### `BookApiIntegrationTest.testCreateBook_Snapshot.approved.txt`

- JSON: objeto plano.
- Campos: `id` (número), `title` (string), `isbn` (string), `authorId` (número), `authorName` (string).
- Valores: `id=3`, título `The Hound of the Baskervilles`, ISBN `978-0-14-043926-8`, `authorId=6`, `authorName="Arthur Conan Doyle"`.
- `reviews` não aparece porque `BookService.convertToDTO` não o preenche e `BookDTO` usa `@JsonInclude(NON_NULL)`.
- `authorName` é calculado por concatenação de `firstName + " " + lastName`; não é um objeto aninhado.
- `id` e `authorId` vêm de identidades persistidas e dependem do estado/sequência do banco, embora tenham sido estáveis na auditoria.

### `BookApiIntegrationTest.testGetBooksByAuthor_Snapshot.approved.txt`

- JSON: array com dois objetos planos `BookDTO`.
- Cada item contém `id`, `title`, `isbn`, `authorId` e `authorName`, com os tipos descritos acima.
- Primeiro item: `id=1`, `Sherlock Holmes: A Study in Scarlet`, ISBN `978-0-14-043924-4`.
- Segundo item: `id=2`, `The Sign of the Four`, ISBN `978-0-14-043925-1`.
- Ambos possuem `authorId=5` e `authorName="Arthur Conan Doyle"`.
- A ordem observada coincide com a ordem de inserção, mas `BookRepository.findByAuthorId` não declara `OrderBy` nem recebe `Sort`; a garantia formal dessa ordem é `NOT_DETERMINED`.
- Identidades persistidas e ordem da coleção são os pontos potencialmente sensíveis a estado/implementação. Não há timestamp.

Em todos os DTOs, a ordem de propriedades é a observada nos arquivos; não existe anotação explícita de ordenação de propriedades no código examinado.

## 6. O que é validado vs. o que é snapshotado

| Teste | Validado pelo teste fora do snapshot | Incluído no snapshot | Não incluído no snapshot |
|---|---|---|---|
| `testGetAllAuthors_Snapshot` | Status HTTP 200 | Body `[]` | Status HTTP, headers, response Content-Type, Location e demais metadados |
| `testCreateAuthor_Snapshot` | Status HTTP 201 | Body completo retornado (`id`, nomes, email) | Status HTTP, headers, response Content-Type, Location e demais metadados |
| `testGetAuthorById_Snapshot` | Status 201 do arranjo e status 200 do GET | Body do GET | Body/headers do POST de arranjo, status HTTP do GET, headers e metadados |
| `testGetAuthorNotFound_Snapshot` | Status HTTP 404 | Body com status textual, mensagem, timestamp e path | Status HTTP como metadado, headers, response Content-Type e demais metadados |
| `testCreateBook_Snapshot` | Status 201 do autor no `setUp` e status 201 do livro | Body do livro retornado | Bodies do arranjo, status HTTP, headers, response Content-Type, Location e demais metadados |
| `testGetBooksByAuthor_Snapshot` | Status 201 do autor, status 201 dos dois livros e status 200 do GET | Body array do GET | Bodies dos arranjos, status HTTP do GET, headers, response Content-Type e demais metadados |

Os requests definem `contentType(MediaType.APPLICATION_JSON)`, mas nenhum teste aplica matcher ao Content-Type da resposta. Nenhum teste chama matcher de header ou snapshot de `MockHttpServletResponse` completo.

## 7. Pontos de mutação

Os IDs abaixo identificam superfícies reais de impacto; não são casos experimentais e não prescrevem uma alteração.

| ID | Snapshot(s) | Categoria | Arquivo/região | Classe e método | Campo/comportamento afetado | Impacto | Direto/Indireto |
|---|---|---|---|---|---|---|---|
| MP-001 | quatro de autor | DTO_STRUCTURE | `model/dto/AuthorDTO.java:15-22` | `AuthorDTO` | Conjunto de propriedades e omissão de nulos | Forma JSON de autores | DIRECT |
| MP-002 | criação e GET por ID de autor; potencialmente lista não vazia | SERVICE_MAPPING | `service/AuthorService.java:122-129` | `AuthorService.convertToDTO` | `id`, `firstName`, `lastName`, `email` | Valores/campos do body | DIRECT |
| MP-003 | criação de autor | BUSINESS_RULE | `service/AuthorService.java:58-75,107-120` | `createAuthor`, `validateAuthorDTO` | Validação e unicidade antes da resposta | Sucesso pode tornar-se erro, ou vice-versa | INDIRECT |
| MP-004 | criação e GET por ID de autor | PERSISTENCE_EFFECT | `model/entity/Author.java:17-28` | `Author` | Identidade e persistência dos campos | IDs/valores recuperados | INDIRECT |
| MP-005 | lista de autores | COLLECTION_CONTENT | `service/AuthorService.java:45-50` | `getAllAuthors` | Fonte e transformação dos itens | Conteúdo do array | DIRECT |
| MP-006 | lista de autores | COLLECTION_ORDER | `AuthorRepository` + `getAllAuthors` | `findAll()` sem `Sort` | Ordem de itens quando não vazio | Ordem do array | INDIRECT |
| MP-007 | respostas de autor | CONTROLLER_RESPONSE | `controller/AuthorController.java:19-35` | `getAllAuthors`, `getAuthorById`, `createAuthor` | Body entregue ao Spring MVC | Corpo serializado | DIRECT |
| MP-008 | erro de autor | ERROR_RESPONSE | `exception/GlobalExceptionHandler.java:23-33` | `handleResourceNotFound` | status textual, mensagem, timestamp, path | Todo o objeto de erro | DIRECT |
| MP-009 | erro de autor | ERROR_RESPONSE | `exception/ResourceNotFoundException.java:9-11` | construtor `(resourceName, id)` | Texto da mensagem | Campo `message` | DIRECT |
| MP-010 | erro de autor | NON_DETERMINISTIC_VALUE | `GlobalExceptionHandler.java:16-29`; `TestTimeConfig` | formatação e `Clock` | Timestamp | Campo `timestamp`; fixo no perfil de teste | DIRECT |
| MP-011 | erro de autor | DTO_STRUCTURE | `exception/ErrorResponse.java:12-16` | `ErrorResponse` | Estrutura do objeto de erro | Campos do JSON de erro | DIRECT |
| MP-012 | dois de livros | DTO_STRUCTURE | `model/dto/BookDTO.java:15-23` | `BookDTO` | Propriedades e omissão de nulos | Forma JSON de livros | DIRECT |
| MP-013 | dois de livros | SERVICE_MAPPING | `service/BookService.java:116-123` | `BookService.convertToDTO` | id, título, ISBN, autor e nome calculado | Valores/campos dos bodies | DIRECT |
| MP-014 | dois de livros | DTO_VALUE | `service/BookService.java:121-122` | `convertToDTO` | `authorId` e concatenação de `authorName` | Representação do autor | DIRECT |
| MP-015 | criação de livro | BUSINESS_RULE | `service/BookService.java:49-69,104-114` | `createBook`, `validateBookDTO` | Validação, autor existente e ISBN único | Sucesso/erro e conteúdo persistido | INDIRECT |
| MP-016 | dois de livros | PERSISTENCE_EFFECT | `model/entity/Book.java:17-33` | `Book` | Identidade, ISBN e relação EAGER com `Author` | IDs e dados derivados do autor | INDIRECT |
| MP-017 | coleção de livros | COLLECTION_CONTENT | `repository/BookRepository.java:13`; `BookService.java:38-47` | `findByAuthorId`, `getBooksByAuthorId` | Filtro por autor e conjunto retornado | Itens presentes/ausentes/duplicados | INDIRECT |
| MP-018 | coleção de livros | COLLECTION_ORDER | mesmas regiões de MP-017 | consulta sem ordenação explícita | Ordem dos dois itens | Ordem do array | INDIRECT |
| MP-019 | dois de livros | CONTROLLER_RESPONSE | `controller/BookController.java:31-41` | `getBooksByAuthorId`, `createBook` | Body entregue ao Spring MVC | Corpo serializado | DIRECT |
| MP-020 | snapshots de criação e GETs dependentes de dados | PERSISTENCE_EFFECT | `service/AuthorService.java:25-43`; `@BeforeEach` dos testes | `initData` e limpeza de repositórios | Sequências de identidade observadas | IDs de autor/livro nos snapshots | INDIRECT |
| MP-021 | todos os snapshots de DTO/erro | SERIALIZATION | anotações `@JsonInclude(NON_NULL)` nos DTOs e serialização Spring/Jackson | `AuthorDTO`, `BookDTO`, `ErrorResponse` | Inclusão, nomes e ordem observada de propriedades | Texto JSON aprovado | DIRECT |

Alterações apenas de status HTTP não são pontos de diferença do arquivo aprovado, pois o status não é enviado ao ApprovalTests; elas podem fazer o matcher falhar antes da captura do body. Por isso `HTTP_STATUS` é uma dimensão validada, mas não uma superfície direta do snapshot atual.

## 8. Oportunidades de evolução intencional

Sem definir classificações ou casos, o código real permite futuramente estudar tipos de evolução como:

- evolução deliberada da representação de `AuthorDTO`, `BookDTO` ou `ErrorResponse` (MP-001, MP-011, MP-012, MP-021);
- mudança intencional no mapeamento entidade/DTO, inclusive na representação calculada de autor em livros (MP-002, MP-013, MP-014);
- alteração deliberada de mensagens e formato uniforme de erro (MP-008 a MP-011);
- mudança consciente de conteúdo ou ordenação de coleções (MP-005, MP-006, MP-017, MP-018);
- evolução de regras de validação, unicidade ou relacionamento que altere o caminho observado entre sucesso e erro (MP-003 e MP-015);
- padronização intencional de serialização e inclusão de campos nulos (MP-021).

Essas são classes de oportunidade sustentadas pelas superfícies existentes; nenhuma alteração concreta ou Ground Truth é estabelecido aqui.

## 9. Oportunidades de regressão

As mesmas superfícies permitem futuramente construir regressões realistas, sem que nenhuma seja introduzida nesta tarefa:

- omissão, renomeação ou valor incorreto de campo nos mapeamentos de autores/livros (MP-001, MP-002, MP-012 a MP-014);
- associação de livro ao autor incorreto ou cálculo incorreto de `authorName` (MP-014 a MP-016);
- filtro incorreto, item ausente/extra/duplicado ou ordem instável nas coleções (MP-005, MP-006, MP-017, MP-018);
- mensagem, path, status textual ou timestamp incorreto na resposta 404 (MP-008 a MP-011);
- efeito persistente/identificador inesperado que vaze para respostas (MP-004, MP-016, MP-020);
- serialização que exponha nulos, suprima campos preenchidos ou altere nomes/representação (MP-021);
- regra de validação ou unicidade que aceite/rejeite indevidamente a entrada (MP-003, MP-015).

Nenhum desses itens é uma classificação de uma mudança específica.

## 10. Redundâncias

- `testCreateAuthor_Snapshot` e `testGetAuthorById_Snapshot` convergem para o mesmo `AuthorService.convertToDTO` e a mesma forma `AuthorDTO`; variam principalmente no caminho anterior (save versus find). Casos centrados apenas na estrutura/mapeamento de DTO tenderiam a ser redundantes.
- `testCreateBook_Snapshot` e `testGetBooksByAuthor_Snapshot` compartilham `BookService.convertToDTO` e a mesma forma de item. O segundo agrega filtro, coleção e ordem; mudanças apenas nos campos de `BookDTO` podem afetar ambos de modo redundante.
- O POST `/authors` é usado como arranjo por `testGetAuthorById_Snapshot` e pelos dois testes de livros, mas seu body só é snapshotado em `testCreateAuthor_Snapshot`. Alterações nesse fluxo podem impedir testes dependentes antes da verificação, sem necessariamente produzir um segundo snapshot comparável.
- Os dois cenários de GET `/authors/{id}` compartilham controller e consulta, mas divergem após `findById`: um mapeia `AuthorDTO`; o outro passa por `GlobalExceptionHandler`. Eles não são redundantes quanto à forma do body.

## 11. Lacunas de cobertura

Somente endpoints declarados nos controllers do baseline são listados. “Teste existente” refere-se a teste de serviço relacionado, não a teste HTTP do endpoint, salvo indicação; nenhum dos itens abaixo possui snapshot.

| HTTP | Endpoint | Método do controller | Teste existente relacionado | Snapshot | Potencial experimental factual |
|---|---|---|---|---|---|
| PUT | `/authors/{id}` | `AuthorController.updateAuthor` | Nenhum teste de update localizado | NÃO | Reutiliza validação, unicidade, persistência e mapeamento de `AuthorDTO` |
| DELETE | `/authors/{id}` | `AuthorController.deleteAuthor` | Nenhum teste de delete localizado | NÃO | Resposta 204 sem body; potencial de snapshot do body atual é limitado |
| GET | `/books` | `BookController.getAllBooks` | Nenhum teste de `getAllBooks` localizado | NÃO | Coleção de `BookDTO`, conteúdo e ordem |
| GET | `/books/{id}` | `BookController.getBookById` | Nenhum teste de `getBookById` localizado | NÃO | Mapeamento de livro e erro por ID |
| PUT | `/books/{id}` | `BookController.updateBook` | Nenhum teste de update localizado | NÃO | Validação, relação com autor, ISBN e mapeamento |
| DELETE | `/books/{id}` | `BookController.deleteBook` | Nenhum teste de delete localizado | NÃO | Resposta 204 sem body; potencial de snapshot do body atual é limitado |
| GET | `/reviews` | `ReviewController.getAllReviews` | Nenhum teste de listagem localizado | NÃO | Coleção de `ReviewDTO` e ordem |
| GET | `/reviews/{id}` | `ReviewController.getReviewById` | Nenhum teste de busca por ID localizado | NÃO | Mapeamento de review e erro por ID |
| GET | `/reviews/by-book/{bookId}` | `ReviewController.getReviewsByBookId` | Nenhum teste desse método localizado | NÃO | Filtro por livro, coleção e mapeamento |
| POST | `/reviews` | `ReviewController.createReview` | `ReviewServiceTest`: sucesso, rating inválido e livro inválido | NÃO | Rating, conteúdo, relação com livro e título derivado |
| PUT | `/reviews/{id}` | `ReviewController.updateReview` | Nenhum teste de update localizado | NÃO | Validação, relacionamento e mapeamento |
| DELETE | `/reviews/{id}` | `ReviewController.deleteReview` | Nenhum teste de delete localizado | NÃO | Resposta 204 sem body; potencial de snapshot do body atual é limitado |

`POST /authors`, `GET /authors`, `GET /authors/{id}`, `POST /books` e `GET /books/by-author/{authorId}` não aparecem como lacunas porque possuem ao menos um snapshot. Os testes unitários relacionados encontrados incluem criação e busca de autor, criação de livro e criação de review; eles não exercitam HTTP nem ApprovalTests.

## 12. Avaliação experimental

| Snapshot | Variabilidade | Complexidade contextual | Potencial de benchmark | Justificativa |
|---|---|---|---|---|
| `testGetAllAuthors` | LOW | LOW | LOW | O baseline captura apenas `[]`; mudanças de item/mapeamento não são observáveis enquanto a coleção permanecer vazia. |
| `testCreateAuthor` | MEDIUM | LOW | MEDIUM | Objeto plano e fluxo direto; expõe estrutura, valores, validação, persistência e ID, mas pouco contexto relacional. |
| `testGetAuthorById` | MEDIUM | MEDIUM | MEDIUM | Mesma representação de autor, porém depende de criação prévia e leitura persistida; parte das mutações é redundante com criação. |
| `testGetAuthorNotFound` | HIGH | MEDIUM | HIGH | Combina exceção, handler, mensagem, path, status textual, relógio e serialização; separa status validado de body snapshotado. |
| `testCreateBook` | HIGH | MEDIUM | HIGH | Inclui persistência, relação com autor e valor derivado `authorName`, além de estrutura e validações. |
| `testGetBooksByAuthor` | HIGH | HIGH | HIGH | Exige compreender arranjo com autor/dois livros, filtro, relação, mapeamento, conteúdo e ordem de coleção. |

As classificações são relativas aos seis snapshots existentes e descrevem capacidade, não dificuldade ou Ground Truth de casos ainda inexistentes.

## 13. Recomendações para construção do catálogo

- Priorizar diversidade entre o erro 404, o objeto relacional de livro e a coleção filtrada; eles exercitam superfícies contextuais distintas.
- Usar snapshots de autor para cenários de menor complexidade, evitando repetir a mesma mutação em `createAuthor` e `getAuthorById` quando ambos apenas refletem `convertToDTO`.
- Em livros, distinguir casos de estrutura/mapeamento (comuns aos dois snapshots) de casos de filtro, conteúdo ou ordem (específicos da coleção).
- Tratar o array vazio de autores como superfície limitada: ele é útil para contrato de coleção vazia, mas não evidencia campos de `AuthorDTO`.
- Separar alterações de status HTTP de alterações do body, pois os arquivos aprovados não capturam status nem headers.
- Controlar explicitamente, na futura especificação dos casos, dependências de IDs gerados, relógio e ordem de repositório, registrando a evidência real de execução.
- Distribuir futuras dificuldades de forma estrutural: objetos planos para baixa complexidade; persistência/relação para média; handler de erro e coleção filtrada/ordenada para alta.
- Não inflar o catálogo repetindo a mesma superfície de DTO em endpoints diferentes sem uma diferença contextual verificável.
- Endpoints sem snapshot são lacunas factuais, mas não devem ser tratados como fontes de casos do benchmark atual sem uma decisão metodológica posterior sobre cobertura.

Nenhum caso `EXP-*`, classificação de Ground Truth ou patch experimental foi produzido neste inventário.
