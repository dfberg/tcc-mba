# Inventário técnico da aplicação

## Visão geral
- Aplicação REST em Spring Boot 3.4.1 com Java 21.
- Arquitetura em camadas: controller, service, repository, model/entity e exception.
- Persistência em memória com H2.
- Contexto HTTP configurado com prefixo /api e porta 8080.
- Testes unitários com JUnit 5 e Mockito, além de testes de integração com MockMvc e ApprovalTests.

## Estrutura funcional

### Recursos principais
- Autores
  - Controlador: [src/main/java/com/example/pocapi/controller/AuthorController.java](src/main/java/com/example/pocapi/controller/AuthorController.java)
  - Serviço: [src/main/java/com/example/pocapi/service/AuthorService.java](src/main/java/com/example/pocapi/service/AuthorService.java)
  - DTO: [src/main/java/com/example/pocapi/model/dto/AuthorDTO.java](src/main/java/com/example/pocapi/model/dto/AuthorDTO.java)
  - Entidade: [src/main/java/com/example/pocapi/model/entity/Author.java](src/main/java/com/example/pocapi/model/entity/Author.java)

- Books
  - Controlador: [src/main/java/com/example/pocapi/controller/BookController.java](src/main/java/com/example/pocapi/controller/BookController.java)
  - Serviço: [src/main/java/com/example/pocapi/service/BookService.java](src/main/java/com/example/pocapi/service/BookService.java)
  - DTO: [src/main/java/com/example/pocapi/model/dto/BookDTO.java](src/main/java/com/example/pocapi/model/dto/BookDTO.java)
  - Entidade: [src/main/java/com/example/pocapi/model/entity/Book.java](src/main/java/com/example/pocapi/model/entity/Book.java)

- Reviews
  - Controlador: [src/main/java/com/example/pocapi/controller/ReviewController.java](src/main/java/com/example/pocapi/controller/ReviewController.java)
  - Serviço: [src/main/java/com/example/pocapi/service/ReviewService.java](src/main/java/com/example/pocapi/service/ReviewService.java)
  - DTO: [src/main/java/com/example/pocapi/model/dto/ReviewDTO.java](src/main/java/com/example/pocapi/model/dto/ReviewDTO.java)
  - Entidade: [src/main/java/com/example/pocapi/model/entity/Review.java](src/main/java/com/example/pocapi/model/entity/Review.java)

## Endpoints disponíveis

### Autores
- GET /api/authors
- GET /api/authors/{id}
- POST /api/authors
- PUT /api/authors/{id}
- DELETE /api/authors/{id}

### Books
- GET /api/books
- GET /api/books/{id}
- GET /api/books/by-author/{authorId}
- POST /api/books
- PUT /api/books/{id}
- DELETE /api/books/{id}

### Reviews
- GET /api/reviews
- GET /api/reviews/{id}
- GET /api/reviews/by-book/{bookId}
- POST /api/reviews
- PUT /api/reviews/{id}
- DELETE /api/reviews/{id}

## Regras de negócio principais
- Autores: valida nome, sobrenome e e-mail; evita e-mails duplicados.
- Books: valida título, ISBN e vínculo com autor; evita ISBN duplicado.
- Reviews: valida rating entre 1 e 5 e exige associação com um livro.

## Tratamento de exceções
- Exceções específicas para recurso não encontrado e validação.
- Handler global em [src/main/java/com/example/pocapi/exception/GlobalExceptionHandler.java](src/main/java/com/example/pocapi/exception/GlobalExceptionHandler.java).
- Respostas padronizadas com status, mensagem, timestamp e path.

## Persistência e relacionamentos
- Author possui muitos Books.
- Book pertence a um Author e possui muitas Reviews.
- Review pertence a um Book.
- Repositórios JPA: [src/main/java/com/example/pocapi/repository/AuthorRepository.java](src/main/java/com/example/pocapi/repository/AuthorRepository.java), [src/main/java/com/example/pocapi/repository/BookRepository.java](src/main/java/com/example/pocapi/repository/BookRepository.java) e [src/main/java/com/example/pocapi/repository/ReviewRepository.java](src/main/java/com/example/pocapi/repository/ReviewRepository.java).

## Testes e snapshots
- Testes unitários: [src/test/java/com/example/pocapi/service/AuthorServiceTest.java](src/test/java/com/example/pocapi/service/AuthorServiceTest.java), [src/test/java/com/example/pocapi/service/BookServiceTest.java](src/test/java/com/example/pocapi/service/BookServiceTest.java) e [src/test/java/com/example/pocapi/service/ReviewServiceTest.java](src/test/java/com/example/pocapi/service/ReviewServiceTest.java).
- Testes de integração com snapshots: [src/test/java/com/example/pocapi/integration/AuthorApiIntegrationTest.java](src/test/java/com/example/pocapi/integration/AuthorApiIntegrationTest.java) e [src/test/java/com/example/pocapi/integration/BookApiIntegrationTest.java](src/test/java/com/example/pocapi/integration/BookApiIntegrationTest.java).
- Snapshots aprovados já existentes em: [src/test/java/com/example/pocapi/integration/AuthorApiIntegrationTest.testGetAllAuthors_Snapshot.approved.txt](src/test/java/com/example/pocapi/integration/AuthorApiIntegrationTest.testGetAllAuthors_Snapshot.approved.txt), [src/test/java/com/example/pocapi/integration/AuthorApiIntegrationTest.testCreateAuthor_Snapshot.approved.txt](src/test/java/com/example/pocapi/integration/AuthorApiIntegrationTest.testCreateAuthor_Snapshot.approved.txt), [src/test/java/com/example/pocapi/integration/AuthorApiIntegrationTest.testGetAuthorById_Snapshot.approved.txt](src/test/java/com/example/pocapi/integration/AuthorApiIntegrationTest.testGetAuthorById_Snapshot.approved.txt), [src/test/java/com/example/pocapi/integration/AuthorApiIntegrationTest.testGetAuthorNotFound_Snapshot.approved.txt](src/test/java/com/example/pocapi/integration/AuthorApiIntegrationTest.testGetAuthorNotFound_Snapshot.approved.txt), [src/test/java/com/example/pocapi/integration/BookApiIntegrationTest.testCreateBook_Snapshot.approved.txt](src/test/java/com/example/pocapi/integration/BookApiIntegrationTest.testCreateBook_Snapshot.approved.txt) e [src/test/java/com/example/pocapi/integration/BookApiIntegrationTest.testGetBooksByAuthor_Snapshot.approved.txt](src/test/java/com/example/pocapi/integration/BookApiIntegrationTest.testGetBooksByAuthor_Snapshot.approved.txt).

## Pontos de atenção
- Há cobertura de integração para autores e livros, mas não para o fluxo completo de reviews.
- A API é adequada para um POC, mas ainda não possui paginação, filtros avançados ou autenticação.

### Remoções e correções após auditoria
Os seguintes casos foram removidos ou marcados como inválidos porque já estão implementados no código-fonte atual, ou porque a especificação do snapshot estava inconsistente com o estado real do repositório de testes:

- `C01-006` (GET /reviews): removido — o campo `bookTitle` já é populado em `ReviewService.convertToDTO` no código atual, portanto não constitui uma alteração a ser avaliada.
- `C01-007` (POST /reviews): removido — o payload de criação já inclui `bookTitle` no estado atual do código.
- `C01-008` (GET /books/by-author/{authorId}): removido — `authorName` já é incluído em `BookService.convertToDTO`; o snapshot aprovado no repositório já contém esse campo.
- `C01-011` (GET /reviews/{id}): removido — duplicado conceitual de C01-006 e já implementado.

As razões para remoção incluem inconsistências entre o "snapshot esperado" documentado e o comportamento real do código, e a impossibilidade prática de reproduzir a suposta regressão sem modificar os testes de integração existentes.

### Especificações de casos mantidos
As especificações seguintes descrevem os casos mantidos após auditoria. Não incluem snapshots nem resultados — apenas condições, passos reprodutíveis e observáveis esperados.

---

Caso: C01-005
Category: Evolução de contrato
Endpoint: POST /api/books

1. Objetivo
- Fazer com que a resposta à criação de um livro inclua o campo `reviews` inicializado como lista vazia.

2. Justificativa técnica
- O `BookDTO` já contém o campo `reviews`. Preencher esse campo no retorno da criação torna o contrato de criação mais explícito e evita que clientes façam chamadas adicionais para descobrir estado inicial de avaliações.

3. Arquivos envolvidos
- src/main/java/com/example/pocapi/service/BookService.java

4. Preconditions (estado necessário)
- Deve existir um `Author` válido com o `id` informado no payload de criação.
- Ambiente de teste deve permitir persistência e leitura imediata (H2 in-memory padrão de testes é aceitável).

5. Passos de reprodução
- Enviar `POST /api/books` com um `BookDTO` válido contendo `title`, `isbn` e `authorId`.

6. Observáveis (o que verificar)
- Código de resposta HTTP: 201 Created.
- Corpo JSON da resposta contém os campos do `BookDTO` e um campo `reviews` presente e igual a `[]`.

7. Complexidade estimada
- Baixa a média (modificação localizada no mapeamento de entidade→DTO).

8. Impacto esperado
- Médio: adiciona campo ao payload de criação; clientes que deserializam estritamente podem precisar se adaptar.

9. Breaking change?
- Não — alteração aditiva.

---

Caso: C01-009
Category: Evolução de contrato
Endpoint: PUT /api/authors/{id}

1. Objetivo
- Normalizar valores textuais (`firstName`, `lastName`) recebidos para remover espaços em excesso antes de persistir e retornar o recurso atualizado.

2. Justificativa técnica
- Padronização de dados melhora consistência do repositório e da API, evitando diferenças triviais que afetam comparações e snapshots.

3. Arquivos envolvidos
- src/main/java/com/example/pocapi/service/AuthorService.java

4. Preconditions (estado necessário)
- Deve existir um `Author` com o `{id}` alvo.

5. Passos de reprodução
- Enviar `PUT /api/authors/{id}` com payload onde `firstName` e/ou `lastName` contenham espaços antes/depois ou múltiplos espaços internos.

6. Observáveis (o que verificar)
- Código HTTP: 200 OK.
- No corpo de resposta, `firstName` e `lastName` estão com espaços externos removidos (trim). Internamente, decisões sobre colapso de múltiplos espaços devem ser especificadas se aplicáveis.

7. Complexidade estimada
- Baixa.

8. Impacto esperado
- Baixo a médio: alteração textual nos valores retornados; pode afetar comparações exatas em snapshots.

9. Breaking change?
- Não — alteração aditiva/normalizadora; entretanto, clientes que dependem de espaços específicos podem ser impactados.

---

Caso: C01-010
Category: Evolução de contrato
Endpoint: PUT /api/books/{id}

1. Objetivo
- Padronizar o campo `isbn` removendo hífens na representação persistida e retornada pela API.

2. Justificativa técnica
- Fornecer ISBN em formato canônico facilita búsquedas, indexação e comparações; elimina variações de formatação.

3. Arquivos envolvidos
- src/main/java/com/example/pocapi/service/BookService.java

4. Preconditions (estado necessário)
- Deve existir um `Book` com o `{id}` alvo.

5. Passos de reprodução
- Enviar `PUT /api/books/{id}` com `isbn` contendo hífens (por exemplo, `978-0-14-043925-1`).

6. Observáveis (o que verificar)
- Código HTTP: 200 OK.
- No corpo de resposta, o campo `isbn` aparece sem hífens (por exemplo, `9780140439251`).

7. Complexidade estimada
- Baixa.

8. Impacto esperado
- Médio: alteração de representação do identificador do recurso; pode afetar clientes que exibem o valor textual ou que usam comparações literais.

9. Breaking change?
- Não estrito; é aditivo/transformacional, mas pode ser percebido como breaking por consumidores que esperam o formato com hífens.

---

### Observações finais
- Removi casos do catálogo que já estavam implementados no código ou que não eram reproduzíveis sem alterar testes — detalhes listados na seção "Remoções e correções" acima.
- Se desejar que eu torne os casos mantidos reproduzíveis automaticamente, eu posso (A) ajustar testes de integração para criar os dados precondition necessários, ou (B) fornecer comandos cURL/requests passo-a-passo para execução manual.

Caso: C01-012

Categoria:
Evolução de contrato

Endpoint:
DELETE /authors/{id}

Arquivos alterados:
AuthorController.java, AuthorService.java

Objetivo da alteração:
Retornar um corpo JSON simples após a remoção bem-sucedida.

Descrição:
A equipe decidiu deixar explícito o resultado da operação em vez de um corpo vazio.

Git Diff:
```diff
@@
- return ResponseEntity.noContent().build();
+ return ResponseEntity.ok(Map.of("deleted", true, "id", id));
```

Snapshot esperado:
```json
""
```

Snapshot recebido:
```json
{"deleted":true,"id":7}
```

Impacto:
Mudança de contrato em resposta ao DELETE.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A API passou a devolver um payload explícito por decisão de produto.

--------------------------------------------------------

Caso: C01-013

Categoria:
Evolução de contrato

Endpoint:
GET /books/{id}

Arquivos alterados:
BookService.java

Objetivo da alteração:
Adicionar uma descrição resumida do livro no retorno.

Descrição:
A equipe quer disponibilizar um resumo curto junto com os dados principais do livro.

Git Diff:
```diff
@@
- .authorName(book.getAuthor().getFirstName() + " " + book.getAuthor().getLastName())
+ .authorName(book.getAuthor().getFirstName() + " " + book.getAuthor().getLastName())
+ .reviews(book.getReviews().stream().map(Review::getId).collect(Collectors.toList()))
```

Snapshot esperado:
```json
{"id":1,"title":"The Hobbit","isbn":"123456789","authorId":1,"authorName":"J.K. Rowling"}
```

Snapshot recebido:
```json
{"id":1,"title":"The Hobbit","isbn":"123456789","authorId":1,"authorName":"J.K. Rowling","reviews":[1,2]}
```

Impacto:
Evolução do contrato de detalhe do livro.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A expansão do payload é intencional e compatível.

--------------------------------------------------------

Caso: C01-014

Categoria:
Evolução de contrato

Endpoint:
GET /authors

Arquivos alterados:
AuthorService.java

Objetivo da alteração:
Ordenar a lista de autores por sobrenome na resposta.

Descrição:
A API passou a devolver os autores em ordem alfabética para facilitar a navegação.

Git Diff:
```diff
@@
- .findAll()
+ .findAll().stream().sorted(Comparator.comparing(Author::getLastName))
```

Snapshot esperado:
```json
[{"id":1,"firstName":"J.K.","lastName":"Rowling","email":"jk@example.com"}]
```

Snapshot recebido:
```json
[{"id":2,"firstName":"George R.R.","lastName":"Martin","email":"grrm@example.com"},{"id":1,"firstName":"J.K.","lastName":"Rowling","email":"jk@example.com"}]
```

Impacto:
Mudança de ordem na coleção.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A mudança é deliberada e altera a saída observável.

--------------------------------------------------------

Caso: C01-015

Categoria:
Evolução de contrato

Endpoint:
GET /reviews/by-book/{bookId}

Arquivos alterados:
ReviewService.java

Objetivo da alteração:
Ordenar reviews por rating decrescente.

Descrição:
A API passou a priorizar as avaliações mais positivas nas respostas de coleção.

Git Diff:
```diff
@@
- .findByBookId(bookId)
+ .findByBookId(bookId).stream().sorted(Comparator.comparing(Review::getRating).reversed())
```

Snapshot esperado:
```json
[{"id":1,"rating":3,"content":"Okay"},{"id":2,"rating":5,"content":"Great"}]
```

Snapshot recebido:
```json
[{"id":2,"rating":5,"content":"Great"},{"id":1,"rating":3,"content":"Okay"}]
```

Impacto:
Mudança de ordem na coleção.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A ordem da coleção passou a ser parte do contrato explícito da operação.

--------------------------------------------------------

Caso: C01-016

Categoria:
Evolução de contrato

Endpoint:
POST /authors

Arquivos alterados:
AuthorService.java

Objetivo da alteração:
Normalizar o e-mail para minúsculas ao criar o autor.

Descrição:
A equipe decidiu padronizar o valor armazenado e devolvido para evitar variações de caixa.

Git Diff:
```diff
@@
- author.setEmail(authorDTO.getEmail());
+ author.setEmail(authorDTO.getEmail().toLowerCase());
```

Snapshot esperado:
```json
{"id":3,"firstName":"Isaac","lastName":"Asimov","email":"isaac@example.com"}
```

Snapshot recebido:
```json
{"id":3,"firstName":"Isaac","lastName":"Asimov","email":"isaac@example.com"}
```

Impacto:
Mudança de representação do campo de e-mail.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
Apesar de parecer trivial, a saída passou a ser diferente e o snapshot deve refletir isso.

--------------------------------------------------------

Caso: C01-017

Categoria:
Evolução de contrato

Endpoint:
POST /books

Arquivos alterados:
BookService.java

Objetivo da alteração:
Normalizar o título do livro para capitalização padrão.

Descrição:
A equipe decidiu ajustar o título para um formato canônico antes da resposta.

Git Diff:
```diff
@@
- book.setTitle(bookDTO.getTitle());
+ book.setTitle(bookDTO.getTitle().trim());
```

Snapshot esperado:
```json
{"id":3,"title":"The Hound of the Baskervilles","isbn":"978-0-14-043926-8","authorId":6,"authorName":"Arthur Conan Doyle"}
```

Snapshot recebido:
```json
{"id":3,"title":"The Hound of the Baskervilles","isbn":"978-0-14-043926-8","authorId":6,"authorName":"Arthur Conan Doyle"}
```

Impacto:
Mudança textual de saída.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A normalização altera o valor retornado e justifica a atualização do snapshot.

--------------------------------------------------------

Caso: C01-018

Categoria:
Evolução de contrato

Endpoint:
GET /books/by-author/{authorId}

Arquivos alterados:
BookService.java

Objetivo da alteração:
Incluir o `authorName` em cada item de coleção.

Descrição:
O time passou a devolver o nome do autor junto a cada livro para reduzir a necessidade de joins no cliente.

Git Diff:
```diff
@@
- .authorId(book.getAuthor().getId())
+ .authorId(book.getAuthor().getId())
+ .authorName(book.getAuthor().getFirstName() + " " + book.getAuthor().getLastName())
```

Snapshot esperado:
```json
[{"id":1,"title":"Sherlock Holmes","isbn":"978-0-14-043924-4","authorId":5}]
```

Snapshot recebido:
```json
[{"id":1,"title":"Sherlock Holmes","isbn":"978-0-14-043924-4","authorId":5,"authorName":"Arthur Conan Doyle"}]
```

Impacto:
Ampliação do payload de coleção.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
É uma evolução de contrato e não uma quebra.

--------------------------------------------------------

Caso: C01-019

Categoria:
Evolução de contrato

Endpoint:
GET /reviews

Arquivos alterados:
ReviewService.java

Objetivo da alteração:
Retornar `bookId` e `bookTitle` de forma consistente nas respostas de coleção.

Descrição:
A equipe decidiu uniformizar o formato das reviews retornadas pela coleção.

Git Diff:
```diff
@@
- .bookTitle(review.getBook().getTitle())
+ .bookId(review.getBook().getId())
+ .bookTitle(review.getBook().getTitle())
```

Snapshot esperado:
```json
[{"id":1,"rating":5,"content":"Great book!"}]
```

Snapshot recebido:
```json
[{"id":1,"rating":5,"content":"Great book!","bookId":1,"bookTitle":"The Hobbit"}]
```

Impacto:
Mudança aditiva nas coleções.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
O consumidor passa a receber dados adicionais que foram planejados.

--------------------------------------------------------

Caso: C01-020

Categoria:
Evolução de contrato

Endpoint:
GET /authors/{id}

Arquivos alterados:
AuthorService.java

Objetivo da alteração:
Retornar um campo `books` sempre presente, mesmo quando vazio.

Descrição:
A API passou a padronizar o contrato para sempre devolver uma coleção de livros, mesmo quando vazia.

Git Diff:
```diff
@@
- .books(author.getBooks().stream().map(...))
+ .books(author.getBooks().stream().map(...).collect(Collectors.toList()))
```

Snapshot esperado:
```json
{"id":4,"firstName":"J.R.R.","lastName":"Tolkien","email":"tolkien@example.com"}
```

Snapshot recebido:
```json
{"id":4,"firstName":"J.R.R.","lastName":"Tolkien","email":"tolkien@example.com","books":[]}
```

Impacto:
Padronização do contrato de resposta.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A mudança é intencional e altera a estrutura observável da resposta.

--------------------------------------------------------

### Categoria 2 — Breaking Change

--------------------------------------------------------

Caso: C02-001

Categoria:
Breaking Change

Endpoint:
POST /authors

Arquivos alterados:
AuthorDTO.java, AuthorController.java

Objetivo da alteração:
Substituir o campo `email` por `contactEmail`.

Descrição:
A API passou por uma refatoração de nomenclatura de um campo público.

Git Diff:
```diff
@@
- private String email;
+ private String contactEmail;
```

Snapshot esperado:
```json
{"id":3,"firstName":"Isaac","lastName":"Asimov","email":"isaac@example.com"}
```

Snapshot recebido:
```json
{"id":3,"firstName":"Isaac","lastName":"Asimov","contactEmail":"isaac@example.com"}
```

Impacto:
Quebra do contrato público da API.

Classificação Humana:
SHOULD_NOT_UPDATE

Justificativa:
Clientes existentes deixarão de encontrar o campo `email`. A mudança caracteriza regressão de contrato.

--------------------------------------------------------

Caso: C02-002

Categoria:
Breaking Change

Endpoint:
GET /authors/{id}

Arquivos alterados:
AuthorService.java, AuthorDTO.java

Objetivo da alteração:
Remover o campo `firstName` do payload de resposta.

Descrição:
A equipe decidiu reduzir o payload, mas isso inviabiliza o consumo de clientes que dependem dessa propriedade.

Git Diff:
```diff
@@
- private String firstName;
+ // removed
```

Snapshot esperado:
```json
{"id":4,"firstName":"J.R.R.","lastName":"Tolkien","email":"tolkien@example.com"}
```

Snapshot recebido:
```json
{"id":4,"lastName":"Tolkien","email":"tolkien@example.com"}
```

Impacto:
Remoção de um atributo público.

Classificação Humana:
SHOULD_NOT_UPDATE

Justificativa:
A mudança desmonta um campo já consumido e não deve ser encoberta por um snapshot atualizado.

--------------------------------------------------------

Caso: C02-003

Categoria:
Breaking Change

Endpoint:
POST /books

Arquivos alterados:
BookDTO.java, BookController.java

Objetivo da alteração:
Trocar `authorId` por `author` em uma estrutura aninhada.

Descrição:
A API passou a reutilizar uma representação de autor aninhada, alterando completamente o contrato.

Git Diff:
```diff
@@
- private Long authorId;
+ private AuthorDTO author;
```

Snapshot esperado:
```json
{"id":3,"title":"The Hound of the Baskervilles","isbn":"978-0-14-043926-8","authorId":6,"authorName":"Arthur Conan Doyle"}
```

Snapshot recebido:
```json
{"id":3,"title":"The Hound of the Baskervilles","isbn":"978-0-14-043926-8","author":{"id":6,"firstName":"Arthur","lastName":"Conan Doyle"}}
```

Impacto:
Quebra da forma de representação do relacionamento.

Classificação Humana:
SHOULD_NOT_UPDATE

Justificativa:
O formato do payload mudou radicalmente e isso representa uma regressão de contrato.

--------------------------------------------------------

Caso: C02-004

Categoria:
Breaking Change

Endpoint:
GET /books/{id}

Arquivos alterados:
BookService.java, BookDTO.java

Objetivo da alteração:
Remover o campo `authorName` do livro.

Descrição:
O time decidiu remover informação que já vinha sendo entregue aos clientes.

Git Diff:
```diff
@@
- private String authorName;
+ // removed
```

Snapshot esperado:
```json
{"id":1,"title":"The Hobbit","isbn":"123456789","authorId":1,"authorName":"J.K. Rowling"}
```

Snapshot recebido:
```json
{"id":1,"title":"The Hobbit","isbn":"123456789","authorId":1}
```

Impacto:
Remoção de campo público.

Classificação Humana:
SHOULD_NOT_UPDATE

Justificativa:
Isso quebra um contrato que já existia e não deve ser tratado como uma mudança de snapshot aceitável.

--------------------------------------------------------

Caso: C02-005

Categoria:
Breaking Change

Endpoint:
GET /reviews/{id}

Arquivos alterados:
ReviewDTO.java

Objetivo da alteração:
Substituir `bookId` por `book` aninhado.

Descrição:
A mudança de modelo de relacionamento alterou o formato de referência do livro.

Git Diff:
```diff
@@
- private Long bookId;
+ private BookDTO book;
```

Snapshot esperado:
```json
{"id":1,"rating":5,"content":"Great book!","bookId":1}
```

Snapshot recebido:
```json
{"id":1,"rating":5,"content":"Great book!","book":{"id":1,"title":"The Hobbit"}}
```

Impacto:
Quebra do contrato de referência do livro.

Classificação Humana:
SHOULD_NOT_UPDATE

Justificativa:
Clientes existentes dependem de `bookId`; a alteração não é compatível.

--------------------------------------------------------

Caso: C02-006

Categoria:
Breaking Change

Endpoint:
POST /reviews

Arquivos alterados:
ReviewController.java

Objetivo da alteração:
Alterar o status de criação de `201 Created` para `200 OK`.

Descrição:
A equipe decidiu simplificar o contrato HTTP, mas isso muda o comportamento observable para clientes.

Git Diff:
```diff
@@
- return ResponseEntity.status(HttpStatus.CREATED).body(createdReview);
+ return ResponseEntity.ok(createdReview);
```

Snapshot esperado:
```json
{"id":2,"rating":4,"content":"Good read","bookId":1}
```

Snapshot recebido:
```json
{"id":2,"rating":4,"content":"Good read","bookId":1}
```

Impacto:
Mudança de semântica HTTP.

Classificação Humana:
SHOULD_NOT_UPDATE

Justificativa:
O payload pode permanecer igual, mas o código de status muda e isso é uma regressão de contrato.

--------------------------------------------------------

Caso: C02-007

Categoria:
Breaking Change

Endpoint:
DELETE /books/{id}

Arquivos alterados:
BookController.java

Objetivo da alteração:
Mudar o DELETE de `204 No Content` para `200 OK` com corpo JSON.

Descrição:
A API começou a devolver um resumo do resultado da operação.

Git Diff:
```diff
@@
- return ResponseEntity.noContent().build();
+ return ResponseEntity.ok(Map.of("deleted", true));
```

Snapshot esperado:
```json
""
```

Snapshot recebido:
```json
{"deleted":true}
```

Impacto:
Quebra do contrato de remoção.

Classificação Humana:
SHOULD_NOT_UPDATE

Justificativa:
A resposta deixou de ser vazia, o que é um ajuste de contrato incompatível.

--------------------------------------------------------

Caso: C02-008

Categoria:
Breaking Change

Endpoint:
GET /authors/{id}

Arquivos alterados:
AuthorController.java

Objetivo da alteração:
Mudar o corpo de sucesso de um objeto para um objeto encapsulado.

Descrição:
A equipe decidiu introduzir um envelope de resposta para padronização.

Git Diff:
```diff
@@
- return ResponseEntity.ok(author);
+ return ResponseEntity.ok(Map.of("data", author));
```

Snapshot esperado:
```json
{"id":4,"firstName":"J.R.R.","lastName":"Tolkien","email":"tolkien@example.com"}
```

Snapshot recebido:
```json
{"data":{"id":4,"firstName":"J.R.R.","lastName":"Tolkien","email":"tolkien@example.com"}}
```

Impacto:
Quebra estrutural do contrato.

Classificação Humana:
SHOULD_NOT_UPDATE

Justificativa:
A alteração muda a estrutura de resposta e não deve ser tratada como um ajuste de snapshot.

--------------------------------------------------------

Caso: C02-009

Categoria:
Breaking Change

Endpoint:
GET /books/by-author/{authorId}

Arquivos alterados:
BookController.java

Objetivo da alteração:
Retornar `400 Bad Request` quando o `authorId` não é numérico.

Descrição:
A camada de controle passou a validar a presença de um identificador numérico antes de qualquer processamento.

Git Diff:
```diff
@@
- public ResponseEntity<List<BookDTO>> getBooksByAuthorId(@PathVariable Long authorId)
+ public ResponseEntity<List<BookDTO>> getBooksByAuthorId(@PathVariable String authorId)
```

Snapshot esperado:
```json
[{"id":1,"title":"Sherlock Holmes","isbn":"978-0-14-043924-4","authorId":5,"authorName":"Arthur Conan Doyle"}]
```

Snapshot recebido:
```json
{"status":"400","message":"Invalid authorId"}
```

Impacto:
Mudança de formato e status HTTP.

Classificação Humana:
SHOULD_NOT_UPDATE

Justificativa:
A mudança altera o contrato e o comportamento da API para cenários anteriores.

--------------------------------------------------------

Caso: C02-010

Categoria:
Breaking Change

Endpoint:
POST /authors

Arquivos alterados:
AuthorService.java

Objetivo da alteração:
Exigir `lastName` e remover `firstName` do contrato.

Descrição:
A equipe simplificou o modelo, mas isso quebra consumidores que ainda enviam `firstName`.

Git Diff:
```diff
@@
- if (authorDTO.getFirstName() == null || authorDTO.getFirstName().isBlank())
+ if (authorDTO.getLastName() == null || authorDTO.getLastName().isBlank())
```

Snapshot esperado:
```json
{"id":3,"firstName":"Isaac","lastName":"Asimov","email":"isaac@example.com"}
```

Snapshot recebido:
```json
{"status":"400","message":"Author last name cannot be empty"}
```

Impacto:
Alteração de validação e contrato de entrada.

Classificação Humana:
SHOULD_NOT_UPDATE

Justificativa:
A resposta de erro passou a indicar uma entrada inválida para um campo que antes era aceito.

--------------------------------------------------------

Caso: C02-011

Categoria:
Breaking Change

Endpoint:
POST /books

Arquivos alterados:
BookService.java

Objetivo da alteração:
Exigir `authorId` como inteiro positivo e rejeitar zero.

Descrição:
A validação de entrada passou a ser mais rigorosa.

Git Diff:
```diff
@@
- if (bookDTO.getAuthorId() == null)
+ if (bookDTO.getAuthorId() == null || bookDTO.getAuthorId() <= 0)
```

Snapshot esperado:
```json
{"id":3,"title":"The Hound of the Baskervilles","isbn":"978-0-14-043926-8","authorId":6,"authorName":"Arthur Conan Doyle"}
```

Snapshot recebido:
```json
{"status":"400","message":"Book must have a valid author"}
```

Impacto:
Mudança de contrato de entrada que passa a falhar em cenários anteriores.

Classificação Humana:
SHOULD_NOT_UPDATE

Justificativa:
Isso representa uma quebra de compatibilidade de uso do endpoint.

--------------------------------------------------------

Caso: C02-012

Categoria:
Breaking Change

Endpoint:
PUT /reviews/{id}

Arquivos alterados:
ReviewService.java

Objetivo da alteração:
Passar a exigir `content` não vazio.

Descrição:
A validação de review tornou-se mais restritiva.

Git Diff:
```diff
@@
- if (reviewDTO.getBookId() == null)
+ if (reviewDTO.getContent() == null || reviewDTO.getContent().isBlank())
```

Snapshot esperado:
```json
{"id":1,"rating":5,"content":"Great book!","bookId":1}
```

Snapshot recebido:
```json
{"status":"400","message":"Review content cannot be empty"}
```

Impacto:
Quebra de compatibilidade para payloads que antes eram aceitos.

Classificação Humana:
SHOULD_NOT_UPDATE

Justificativa:
A mudança altera a resposta de sucesso para erro em cenários já válidos.

--------------------------------------------------------

Caso: C02-013

Categoria:
Breaking Change

Endpoint:
GET /authors

Arquivos alterados:
AuthorService.java

Objetivo da alteração:
Remover e-mails da coleção retornada.

Descrição:
A equipe decidiu reduzir a exposição de dados pessoais na API.

Git Diff:
```diff
@@
- .email(author.getEmail())
+ // removed
```

Snapshot esperado:
```json
[{"id":1,"firstName":"J.K.","lastName":"Rowling","email":"jk@example.com"}]
```

Snapshot recebido:
```json
[{"id":1,"firstName":"J.K.","lastName":"Rowling"}]
```

Impacto:
Remoção de um atributo público.

Classificação Humana:
SHOULD_NOT_UPDATE

Justificativa:
Aliar o snapshot com essa mudança esconderia uma quebra de compatibilidade.

--------------------------------------------------------

Caso: C02-014

Categoria:
Breaking Change

Endpoint:
GET /books

Arquivos alterados:
BookDTO.java, BookService.java

Objetivo da alteração:
Remover o `isbn` do payload.

Descrição:
A equipe decidiu esconder o identificador do livro em uma mudança de desenho de API.

Git Diff:
```diff
@@
- private String isbn;
+ // removed
```

Snapshot esperado:
```json
[{"id":1,"title":"The Hobbit","isbn":"123456789","authorId":1,"authorName":"J.K. Rowling"}]
```

Snapshot recebido:
```json
[{"id":1,"title":"The Hobbit","authorId":1,"authorName":"J.K. Rowling"}]
```

Impacto:
Quebra do contrato de leitura de livros.

Classificação Humana:
SHOULD_NOT_UPDATE

Justificativa:
A mudança remove um campo público já conhecido por clientes.

--------------------------------------------------------

Caso: C02-015

Categoria:
Breaking Change

Endpoint:
GET /reviews

Arquivos alterados:
ReviewDTO.java

Objetivo da alteração:
Remover o campo `content` das respostas.

Descrição:
A equipe decidiu reduzir o payload de reviews ao mínimo.

Git Diff:
```diff
@@
- private String content;
+ // removed
```

Snapshot esperado:
```json
[{"id":1,"rating":5,"content":"Great book!","bookId":1}]
```

Snapshot recebido:
```json
[{"id":1,"rating":5,"bookId":1}]
```

Impacto:
Remoção de um campo público.

Classificação Humana:
SHOULD_NOT_UPDATE

Justificativa:
Isso muda o contrato sem compatibilidade e não deve ser tratado como um snapshot benigno.

--------------------------------------------------------

Caso: C02-016

Categoria:
Breaking Change

Endpoint:
POST /authors

Arquivos alterados:
AuthorController.java

Objetivo da alteração:
Trocar a resposta de `201 Created` para `202 Accepted`.

Descrição:
A API passou a usar um status diferente para processamentos assíncronos.

Git Diff:
```diff
@@
- ResponseEntity.status(HttpStatus.CREATED)
+ ResponseEntity.status(HttpStatus.ACCEPTED)
```

Snapshot esperado:
```json
{"id":3,"firstName":"Isaac","lastName":"Asimov","email":"isaac@example.com"}
```

Snapshot recebido:
```json
{"id":3,"firstName":"Isaac","lastName":"Asimov","email":"isaac@example.com"}
```

Impacto:
Mudança semântica de status HTTP.

Classificação Humana:
SHOULD_NOT_UPDATE

Justificativa:
O corpo pode permanecer igual, mas o status mudou e isso deve ser tratado como regressão de contrato.

--------------------------------------------------------

Caso: C02-017

Categoria:
Breaking Change

Endpoint:
GET /authors/{id}

Arquivos alterados:
AuthorController.java

Objetivo da alteração:
Trocar `200 OK` por `204 No Content` em caso de sucesso.

Descrição:
O endpoint passou a não devolver body em resposta de sucesso.

Git Diff:
```diff
@@
- return ResponseEntity.ok(author);
+ return ResponseEntity.noContent().build();
```

Snapshot esperado:
```json
{"id":4,"firstName":"J.R.R.","lastName":"Tolkien","email":"tolkien@example.com"}
```

Snapshot recebido:
```json
""
```

Impacto:
Quebra estrutural da operação de leitura.

Classificação Humana:
SHOULD_NOT_UPDATE

Justificativa:
A API deixou de retornar o payload esperado, o que não é um ajuste de snapshot.

--------------------------------------------------------

Caso: C02-018

Categoria:
Breaking Change

Endpoint:
GET /books/{id}

Arquivos alterados:
BookController.java

Objetivo da alteração:
Trocar o `id` do livro por `bookId` no payload.

Descrição:
A equipe decidiu renomear as chaves públicas para se alinhar a um novo padrão interno.

Git Diff:
```diff
@@
- private Long id;
+ private Long bookId;
```

Snapshot esperado:
```json
{"id":1,"title":"The Hobbit","isbn":"123456789","authorId":1,"authorName":"J.K. Rowling"}
```

Snapshot recebido:
```json
{"bookId":1,"title":"The Hobbit","isbn":"123456789","authorId":1,"authorName":"J.K. Rowling"}
```

Impacto:
Mudança de forma pública do identificador do recurso.

Classificação Humana:
SHOULD_NOT_UPDATE

Justificativa:
Essa troca quebra compatibilidade com consumidores atuais e não representa uma evolução aceitável.

--------------------------------------------------------

Caso: C02-019

Categoria:
Breaking Change

Endpoint:
GET /reviews/{id}

Arquivos alterados:
ReviewService.java

Objetivo da alteração:
Remover o campo `rating` do detalhe da review.

Descrição:
A equipe decidiu reduzir o payload de detalhe.

Git Diff:
```diff
@@
- .rating(review.getRating())
+ // removed
```

Snapshot esperado:
```json
{"id":1,"rating":5,"content":"Great book!","bookId":1}
```

Snapshot recebido:
```json
{"id":1,"content":"Great book!","bookId":1}
```

Impacto:
Remoção de campo relevante do contrato.

Classificação Humana:
SHOULD_NOT_UPDATE

Justificativa:
A perda de um campo central não é um ajuste de snapshot, e sim uma quebra.

--------------------------------------------------------

Caso: C02-020

Categoria:
Breaking Change

Endpoint:
GET /authors

Arquivos alterados:
AuthorDTO.java

Objetivo da alteração:
Trocar `lastName` por `surname`.

Descrição:
O time adotou um novo nome de campo para se alinhar a um padrão interno.

Git Diff:
```diff
@@
- private String lastName;
+ private String surname;
```

Snapshot esperado:
```json
[{"id":1,"firstName":"J.K.","lastName":"Rowling","email":"jk@example.com"}]
```

Snapshot recebido:
```json
[{"id":1,"firstName":"J.K.","surname":"Rowling","email":"jk@example.com"}]
```

Impacto:
Quebra de nomenclatura do contrato.

Classificação Humana:
SHOULD_NOT_UPDATE

Justificativa:
A API deixou de expor um campo antigo e isso não é uma atualização legítima do snapshot.

--------------------------------------------------------

### Categoria 3 — Regras de negócio

--------------------------------------------------------

Caso: C03-001

Categoria:
Regras de negócio

Endpoint:
POST /authors

Arquivos alterados:
AuthorService.java

Objetivo da alteração:
Passar a rejeitar autores com `firstName` menor do que 2 caracteres.

Descrição:
A regra de validação foi reforçada para evitar nomes muito curtos.

Git Diff:
```diff
@@
- if (authorDTO.getFirstName() == null || authorDTO.getFirstName().isBlank())
+ if (authorDTO.getFirstName() == null || authorDTO.getFirstName().length() < 2)
```

Snapshot esperado:
```json
{"id":3,"firstName":"Isaac","lastName":"Asimov","email":"isaac@example.com"}
```

Snapshot recebido:
```json
{"status":"400","message":"Author first name must be at least 2 characters"}
```

Impacto:
Mudança de comportamento em validação de entrada.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A regra é intencional e o snapshot deve refletir o novo comportamento de erro.

--------------------------------------------------------

Caso: C03-002

Categoria:
Regras de negócio

Endpoint:
POST /books

Arquivos alterados:
BookService.java

Objetivo da alteração:
Passar a aceitar somente ISBN-13 válidos.

Descrição:
A validação e o formato do ISBN foram ajustados para cumprir uma política interna.

Git Diff:
```diff
@@
- if (bookDTO.getIsbn() == null || bookDTO.getIsbn().isBlank())
+ if (bookDTO.getIsbn() == null || bookDTO.getIsbn().isBlank() || !bookDTO.getIsbn().matches("\\d{13}"))
```

Snapshot esperado:
```json
{"id":3,"title":"The Hound of the Baskervilles","isbn":"978-0-14-043926-8","authorId":6,"authorName":"Arthur Conan Doyle"}
```

Snapshot recebido:
```json
{"status":"400","message":"Book ISBN must be a valid 13-digit number"}
```

Impacto:
Uma nova regra de negócio afeta o resultado do endpoint.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A alteração é planejada e o snapshot precisa refletir a nova resposta.

--------------------------------------------------------

Caso: C03-003

Categoria:
Regras de negócio

Endpoint:
POST /reviews

Arquivos alterados:
ReviewService.java

Objetivo da alteração:
Passar a rejeitar avaliações com conteúdo vazio.

Descrição:
Depois de uma análise do produto, a regra passou a exigir conteúdo textual na review.

Git Diff:
```diff
@@
- if (reviewDTO.getBookId() == null)
+ if (reviewDTO.getContent() == null || reviewDTO.getContent().isBlank())
```

Snapshot esperado:
```json
{"id":2,"rating":4,"content":"Good read","bookId":1}
```

Snapshot recebido:
```json
{"status":"400","message":"Review content cannot be empty"}
```

Impacto:
Mudança na validação do recurso.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A regra nova muda o comportamento observado da API e o snapshot deve ser atualizado.

--------------------------------------------------------

Caso: C03-004

Categoria:
Regras de negócio

Endpoint:
POST /authors

Arquivos alterados:
AuthorService.java

Objetivo da alteração:
Permitir apenas um autor por e-mail, inclusive em case-insensitive.

Descrição:
A regra de unicidade passou a ser case-insensitive para evitar duplicações por variações de caixa.

Git Diff:
```diff
@@
- if (authorRepository.findByEmail(authorDTO.getEmail()).isPresent())
+ if (authorRepository.findByEmail(authorDTO.getEmail().toLowerCase()).isPresent())
```

Snapshot esperado:
```json
{"id":3,"firstName":"Isaac","lastName":"Asimov","email":"isaac@example.com"}
```

Snapshot recebido:
```json
{"status":"400","message":"Author with email isaac@example.com already exists"}
```

Impacto:
Mudança na resposta para um cenário de duplicidade.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A regra foi reforçada e a resposta mudou intencionalmente.

--------------------------------------------------------

Caso: C03-005

Categoria:
Regras de negócio

Endpoint:
POST /books

Arquivos alterados:
BookService.java

Objetivo da alteração:
Restringir a criação de livros duplicados por ISBN, mesmo com hífens.

Descrição:
A regra de unicidade passou a normalizar o ISBN antes da comparação.

Git Diff:
```diff
@@
- if (bookRepository.findByIsbn(bookDTO.getIsbn()).isPresent())
+ if (bookRepository.findByIsbn(bookDTO.getIsbn().replace("-", "")).isPresent())
```

Snapshot esperado:
```json
{"id":3,"title":"The Hound of the Baskervilles","isbn":"978-0-14-043926-8","authorId":6,"authorName":"Arthur Conan Doyle"}
```

Snapshot recebido:
```json
{"status":"400","message":"Book with ISBN 9780140439268 already exists"}
```

Impacto:
Mudança na resposta para um cenário de duplicidade.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A regra é nova e altera o comportamento do endpoint de forma explícita.

--------------------------------------------------------

Caso: C03-006

Categoria:
Regras de negócio

Endpoint:
POST /reviews

Arquivos alterados:
ReviewService.java

Objetivo da alteração:
Passar a aceitar somente notas entre 1 e 4.

Descrição:
A política de negócio reduziu o limite superior de 5 para 4.

Git Diff:
```diff
@@
- if (reviewDTO.getRating() < 1 || reviewDTO.getRating() > 5)
+ if (reviewDTO.getRating() < 1 || reviewDTO.getRating() > 4)
```

Snapshot esperado:
```json
{"id":2,"rating":5,"content":"Great read","bookId":1}
```

Snapshot recebido:
```json
{"status":"400","message":"Review rating must be between 1 and 4"}
```

Impacto:
Regra de validação mais restritiva.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
O cenário passou de sucesso para erro e o snapshot deve refletir isso.

--------------------------------------------------------

Caso: C03-007

Categoria:
Regras de negócio

Endpoint:
PUT /authors/{id}

Arquivos alterados:
AuthorService.java

Objetivo da alteração:
Impedir que o e-mail seja alterado para um valor já existente.

Descrição:
A regra de negócio passou a ser aplicada também no update, não só na criação.

Git Diff:
```diff
@@
- if (!author.getEmail().equals(authorDTO.getEmail()) && authorRepository.findByEmail(authorDTO.getEmail()).isPresent())
+ if (!author.getEmail().equalsIgnoreCase(authorDTO.getEmail()) && authorRepository.findByEmail(authorDTO.getEmail().toLowerCase()).isPresent())
```

Snapshot esperado:
```json
{"id":2,"firstName":"George","lastName":"Martin","email":"grrm@example.com"}
```

Snapshot recebido:
```json
{"status":"400","message":"Author with email grrm@example.com already exists"}
```

Impacto:
Mudança de comportamento em update de autores.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A regra nova mudou a resposta observável e deve ser refletida no snapshot.

--------------------------------------------------------

Caso: C03-008

Categoria:
Regras de negócio

Endpoint:
PUT /books/{id}

Arquivos alterados:
BookService.java

Objetivo da alteração:
Passar a rejeitar alteração de ISBN para um valor duplicado.

Descrição:
A validação de atualização passou a impedir conflitos de ISBN.

Git Diff:
```diff
@@
- if (!book.getIsbn().equals(bookDTO.getIsbn()) && bookRepository.findByIsbn(bookDTO.getIsbn()).isPresent())
+ if (!book.getIsbn().equals(bookDTO.getIsbn()) && bookRepository.findByIsbn(bookDTO.getIsbn().replace("-", "")).isPresent())
```

Snapshot esperado:
```json
{"id":2,"title":"The Sign of the Four","isbn":"978-0-14-043925-1","authorId":5,"authorName":"Arthur Conan Doyle"}
```

Snapshot recebido:
```json
{"status":"400","message":"Book with ISBN 9780140439251 already exists"}
```

Impacto:
Mudança de comportamento em atualização de livros.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A regra alterou a saída do endpoint e o snapshot precisa ser atualizado.

--------------------------------------------------------

Caso: C03-009

Categoria:
Regras de negócio

Endpoint:
POST /reviews

Arquivos alterados:
ReviewService.java

Objetivo da alteração:
Bloquear reviews para livros inexistentes de forma mais explícita.

Descrição:
Um erro de negócio passou a ser convertido em uma mensagem mais informativa.

Git Diff:
```diff
@@
- throw new ResourceNotFoundException("Book", reviewDTO.getBookId());
+ throw new ValidationException("Review must be associated with a valid book");
```

Snapshot esperado:
```json
{"id":2,"rating":4,"content":"Good read","bookId":999}
```

Snapshot recebido:
```json
{"status":"400","message":"Review must be associated with a valid book"}
```

Impacto:
Mudança de semântica da operação.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A regra do negócio mudou e a resposta passou a ser diferente.

--------------------------------------------------------

Caso: C03-010

Categoria:
Regras de negócio

Endpoint:
GET /books/by-author/{authorId}

Arquivos alterados:
BookService.java

Objetivo da alteração:
Retornar uma lista vazia quando o autor existe, mas não possui livros.

Descrição:
A regra passou a ser explícita para cenários de autor sem obras associadas.

Git Diff:
```diff
@@
- authorRepository.findById(authorId)
+ authorRepository.findById(authorId)
+ return Collections.emptyList();
```

Snapshot esperado:
```json
[{"id":1,"title":"The Hobbit","isbn":"123456789","authorId":1,"authorName":"J.K. Rowling"}]
```

Snapshot recebido:
```json
[]
```

Impacto:
Mudança de comportamento de coleção vazia.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A resposta da API em um cenário legítimo agora é outra e merece atualização do snapshot.

--------------------------------------------------------

Caso: C03-011

Categoria:
Regras de negócio

Endpoint:
GET /reviews/by-book/{bookId}

Arquivos alterados:
ReviewService.java

Objetivo da alteração:
Filtrar reviews de rating menor que 3.

Descrição:
A política passou a exibir somente avaliações mais relevantes.

Git Diff:
```diff
@@
- return reviewRepository.findByBookId(bookId)
+ return reviewRepository.findByBookId(bookId).stream().filter(r -> r.getRating() >= 3)
```

Snapshot esperado:
```json
[{"id":1,"rating":2,"content":"Not great"},{"id":2,"rating":5,"content":"Excellent"}]
```

Snapshot recebido:
```json
[{"id":2,"rating":5,"content":"Excellent"}]
```

Impacto:
Mudança da coleção retornada.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A regra alterou o conjunto de dados entregue pela API e o snapshot deve mudar.

--------------------------------------------------------

Caso: C03-012

Categoria:
Regras de negócio

Endpoint:
GET /authors

Arquivos alterados:
AuthorService.java

Objetivo da alteração:
Filtrar autores com e-mail inválido.

Descrição:
A API passou a omitir dados inválidos de sua listagem pública.

Git Diff:
```diff
@@
- .findAll()
+ .findAll().stream().filter(a -> a.getEmail().contains("@"))
```

Snapshot esperado:
```json
[{"id":1,"firstName":"J.K.","lastName":"Rowling","email":"jk@example.com"}]
```

Snapshot recebido:
```json
[]
```

Impacto:
Mudança de conjunto retornado.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A regra faz sentido e a saída observável mudou de forma intencional.

--------------------------------------------------------

Caso: C03-013

Categoria:
Regras de negócio

Endpoint:
PUT /authors/{id}

Arquivos alterados:
AuthorService.java

Objetivo da alteração:
Remover espaços em volta do e-mail ao atualizar.

Descrição:
A regra passou a normalizar o valor do e-mail para evitar inconsistências.

Git Diff:
```diff
@@
- author.setEmail(authorDTO.getEmail());
+ author.setEmail(authorDTO.getEmail().trim());
```

Snapshot esperado:
```json
{"id":2,"firstName":"George","lastName":"Martin","email":"grrm@example.com"}
```

Snapshot recebido:
```json
{"id":2,"firstName":"George","lastName":"Martin","email":"grrm@example.com"}
```

Impacto:
Mudança mínima de valor retornado.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
Mesmo que pareça sutil, a regra altera o valor final retornado e é intencional.

--------------------------------------------------------

Caso: C03-014

Categoria:
Regras de negócio

Endpoint:
POST /books

Arquivos alterados:
BookService.java

Objetivo da alteração:
Exigir que o título tenha ao menos 3 caracteres.

Descrição:
A validação de título foi reforçada para evitar cadastros muito curtos.

Git Diff:
```diff
@@
- if (bookDTO.getTitle() == null || bookDTO.getTitle().isBlank())
+ if (bookDTO.getTitle() == null || bookDTO.getTitle().trim().length() < 3)
```

Snapshot esperado:
```json
{"id":3,"title":"The Hound of the Baskervilles","isbn":"978-0-14-043926-8","authorId":6,"authorName":"Arthur Conan Doyle"}
```

Snapshot recebido:
```json
{"status":"400","message":"Book title must be at least 3 characters"}
```

Impacto:
Mudança de validação de entrada.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A nova regra alterou o comportamento do endpoint e exige um novo snapshot.

--------------------------------------------------------

Caso: C03-015

Categoria:
Regras de negócio

Endpoint:
POST /reviews

Arquivos alterados:
ReviewService.java

Objetivo da alteração:
Restringir reviews a livros com `authorId` associado a um autor válido.

Descrição:
A regra passou a verificar a existência do autor em vez de apenas do livro.

Git Diff:
```diff
@@
- Book book = bookRepository.findById(reviewDTO.getBookId())
+ Book book = bookRepository.findById(reviewDTO.getBookId())
+ authorRepository.findById(book.getAuthor().getId())
```

Snapshot esperado:
```json
{"id":2,"rating":4,"content":"Good read","bookId":1}
```

Snapshot recebido:
```json
{"status":"400","message":"Review must be associated with a valid author"}
```

Impacto:
Mudança de regra de negócio para validação de relação.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A resposta do endpoint passou a ser diferente por uma decisão explícita do produto.

--------------------------------------------------------

### Categoria 4 — Serialização

--------------------------------------------------------

Caso: C04-001

Categoria:
Serialização

Endpoint:
GET /authors/{id}

Arquivos alterados:
AuthorDTO.java

Objetivo da alteração:
Passar a omitir campos nulos em vez de devolver `null`.

Descrição:
A política de serialização foi alterada para reduzir ruído no JSON.

Git Diff:
```diff
@@
- @JsonInclude(JsonInclude.Include.NON_NULL)
+ @JsonInclude(JsonInclude.Include.NON_EMPTY)
```

Snapshot esperado:
```json
{"id":4,"firstName":"J.R.R.","lastName":"Tolkien","email":"tolkien@example.com","books":null}
```

Snapshot recebido:
```json
{"id":4,"firstName":"J.R.R.","lastName":"Tolkien","email":"tolkien@example.com"}
```

Impacto:
Mudança na forma de serialização do payload.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A mudança é intencional e muda a representação do JSON produzido.

--------------------------------------------------------

Caso: C04-002

Categoria:
Serialização

Endpoint:
GET /books/{id}

Arquivos alterados:
BookDTO.java

Objetivo da alteração:
Excluir o campo `reviews` quando a coleção está vazia.

Descrição:
A serialização passou a ficar mais limpa quando a coleção não tem conteúdo.

Git Diff:
```diff
@@
- @JsonInclude(JsonInclude.Include.NON_NULL)
+ @JsonInclude(JsonInclude.Include.NON_EMPTY)
```

Snapshot esperado:
```json
{"id":1,"title":"The Hobbit","isbn":"123456789","authorId":1,"authorName":"J.K. Rowling","reviews":[]}
```

Snapshot recebido:
```json
{"id":1,"title":"The Hobbit","isbn":"123456789","authorId":1,"authorName":"J.K. Rowling"}
```

Impacto:
Mudança de serialização de coleções vazias.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A resposta muda de forma deliberada e deveria ser capturada pelo snapshot.

--------------------------------------------------------

Caso: C04-003

Categoria:
Serialização

Endpoint:
GET /reviews/{id}

Arquivos alterados:
ReviewDTO.java

Objetivo da alteração:
Remover o campo `content` quando ele estiver vazio.

Descrição:
A serialização passou a omitir conteúdo vazio para simplificar o JSON.

Git Diff:
```diff
@@
- @JsonInclude(JsonInclude.Include.NON_NULL)
+ @JsonInclude(JsonInclude.Include.NON_EMPTY)
```

Snapshot esperado:
```json
{"id":1,"rating":5,"content":"Great book!","bookId":1}
```

Snapshot recebido:
```json
{"id":1,"rating":5,"bookId":1}
```

Impacto:
Mudança na representação do payload.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
O JSON produzido mudou e o snapshot precisa refletir isso.

--------------------------------------------------------

Caso: C04-004

Categoria:
Serialização

Endpoint:
GET /authors

Arquivos alterados:
AuthorDTO.java

Objetivo da alteração:
Alterar a ordem das propriedades do JSON para fins de consistência.

Descrição:
A equipe passou a usar `@JsonPropertyOrder` para deixar o payload mais previsível.

Git Diff:
```diff
@@
+ @JsonPropertyOrder({"id","firstName","lastName","email","books"})
```

Snapshot esperado:
```json
[{"firstName":"J.K.","lastName":"Rowling","email":"jk@example.com","id":1}]
```

Snapshot recebido:
```json
[{"id":1,"firstName":"J.K.","lastName":"Rowling","email":"jk@example.com"}]
```

Impacto:
Mudança de ordem de campos no JSON.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A ordem textual do objeto mudou e o snapshot deve ser atualizado.

--------------------------------------------------------

Caso: C04-005

Categoria:
Serialização

Endpoint:
GET /books

Arquivos alterados:
BookDTO.java

Objetivo da alteração:
Adicionar um alias para `authorName` com `@JsonProperty("author")`.

Descrição:
A API passou a se alinhar com um padrão de consumo mais comum.

Git Diff:
```diff
@@
- private String authorName;
+ @JsonProperty("author")
+ private String authorName;
```

Snapshot esperado:
```json
[{"id":1,"title":"The Hobbit","isbn":"123456789","authorId":1,"authorName":"J.K. Rowling"}]
```

Snapshot recebido:
```json
[{"id":1,"title":"The Hobbit","isbn":"123456789","authorId":1,"author":"J.K. Rowling"}]
```

Impacto:
Mudança de nome da propriedade serializada.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A API passou a expor um nome diferente para o mesmo dado.

--------------------------------------------------------

Caso: C04-006

Categoria:
Serialização

Endpoint:
GET /reviews

Arquivos alterados:
ReviewDTO.java

Objetivo da alteração:
Serializar `rating` como string em vez de número.

Descrição:
A equipe alterou a representação do campo para atender a um consumidor legado.

Git Diff:
```diff
@@
- private Integer rating;
+ private String rating;
```

Snapshot esperado:
```json
[{"id":1,"rating":5,"content":"Great book!","bookId":1}]
```

Snapshot recebido:
```json
[{"id":1,"rating":"5","content":"Great book!","bookId":1}]
```

Impacto:
Mudança de tipo no JSON.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
O tipo do campo mudou e isso é claramente observável no snapshot.

--------------------------------------------------------

Caso: C04-007

Categoria:
Serialização

Endpoint:
GET /authors/{id}

Arquivos alterados:
AuthorDTO.java

Objetivo da alteração:
Serializar `books` como objeto vazio em vez de array vazio.

Descrição:
A equipe pensou em padronizar o valor para coleções de relacionamento.

Git Diff:
```diff
@@
- .books(new ArrayList<>())
+ .books(new LinkedHashMap<>())
```

Snapshot esperado:
```json
{"id":4,"firstName":"J.R.R.","lastName":"Tolkien","email":"tolkien@example.com","books":[]}
```

Snapshot recebido:
```json
{"id":4,"firstName":"J.R.R.","lastName":"Tolkien","email":"tolkien@example.com","books":{}}
```

Impacto:
Mudança de estrutura de serialização.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A alteração de tipo e estrutura do valor serializado é visível e intencional.

--------------------------------------------------------

Caso: C04-008

Categoria:
Serialização

Endpoint:
GET /books/{id}

Arquivos alterados:
BookDTO.java

Objetivo da alteração:
Usar `@JsonInclude(Include.ALWAYS)` para sempre incluir `reviews`.

Descrição:
O time decidiu não omitir coleções vazias em respostas de detalhe.

Git Diff:
```diff
@@
- @JsonInclude(JsonInclude.Include.NON_EMPTY)
+ @JsonInclude(JsonInclude.Include.ALWAYS)
```

Snapshot esperado:
```json
{"id":1,"title":"The Hobbit","isbn":"123456789","authorId":1,"authorName":"J.K. Rowling"}
```

Snapshot recebido:
```json
{"id":1,"title":"The Hobbit","isbn":"123456789","authorId":1,"authorName":"J.K. Rowling","reviews":[]}
```

Impacto:
Mudança de serialização de campos vazios.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A serialização agora inclui um campo que antes era omitido.

--------------------------------------------------------

Caso: C04-009

Categoria:
Serialização

Endpoint:
GET /reviews/{id}

Arquivos alterados:
ReviewDTO.java

Objetivo da alteração:
Incluir `content` mesmo quando for vazio.

Descrição:
A equipe decidiu remover a omissão de conteúdo vazio em detalhe.

Git Diff:
```diff
@@
- @JsonInclude(JsonInclude.Include.NON_EMPTY)
+ @JsonInclude(JsonInclude.Include.ALWAYS)
```

Snapshot esperado:
```json
{"id":1,"rating":5,"bookId":1}
```

Snapshot recebido:
```json
{"id":1,"rating":5,"content":"","bookId":1}
```

Impacto:
Mudança na representação de conteúdo vazio.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A representação do JSON alterou de forma deliberada.

--------------------------------------------------------

Caso: C04-010

Categoria:
Serialização

Endpoint:
GET /authors/{id}

Arquivos alterados:
AuthorDTO.java

Objetivo da alteração:
Serializar `email` como `contactEmail` no DTO.

Descrição:
A equipe adaptou o DTO para um padrão de serialização mais legível.

Git Diff:
```diff
@@
- private String email;
+ @JsonProperty("contactEmail")
+ private String email;
```

Snapshot esperado:
```json
{"id":4,"firstName":"J.R.R.","lastName":"Tolkien","email":"tolkien@example.com"}
```

Snapshot recebido:
```json
{"id":4,"firstName":"J.R.R.","lastName":"Tolkien","contactEmail":"tolkien@example.com"}
```

Impacto:
Mudança de nome de propriedade serializada.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A mudança altera claramente o contrato serializado e justifica atualização do snapshot.

--------------------------------------------------------

### Categoria 5 — HTTP

--------------------------------------------------------

Caso: C05-001

Categoria:
HTTP

Endpoint:
POST /authors

Arquivos alterados:
AuthorController.java

Objetivo da alteração:
Retornar `200 OK` em vez de `201 Created` em criação bem-sucedida.

Descrição:
O time decidiu simplificar a semântica de criação para o cliente consumidor.

Git Diff:
```diff
@@
- ResponseEntity.status(HttpStatus.CREATED).body(createdAuthor)
+ ResponseEntity.ok(createdAuthor)
```

Snapshot esperado:
```json
{"id":3,"firstName":"Isaac","lastName":"Asimov","email":"isaac@example.com"}
```

Snapshot recebido:
```json
{"id":3,"firstName":"Isaac","lastName":"Asimov","email":"isaac@example.com"}
```

Impacto:
Mudança de status HTTP.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
O comportamento observable mudou e o snapshot precisa refletir a resposta de contrato, embora o body continue igual.

--------------------------------------------------------

Caso: C05-002

Categoria:
HTTP

Endpoint:
POST /books

Arquivos alterados:
BookController.java

Objetivo da alteração:
Retornar `202 Accepted` para criação de livros.

Descrição:
A equipe decidiu tratar a criação como assíncrona no nível HTTP.

Git Diff:
```diff
@@
- ResponseEntity.status(HttpStatus.CREATED).body(createdBook)
+ ResponseEntity.status(HttpStatus.ACCEPTED).body(createdBook)
```

Snapshot esperado:
```json
{"id":3,"title":"The Hound of the Baskervilles","isbn":"978-0-14-043926-8","authorId":6,"authorName":"Arthur Conan Doyle"}
```

Snapshot recebido:
```json
{"id":3,"title":"The Hound of the Baskervilles","isbn":"978-0-14-043926-8","authorId":6,"authorName":"Arthur Conan Doyle"}
```

Impacto:
Mudança de status HTTP.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
O payload é igual, mas o status HTTP passa a ser parte do contrato do endpoint.

--------------------------------------------------------

Caso: C05-003

Categoria:
HTTP

Endpoint:
DELETE /authors/{id}

Arquivos alterados:
AuthorController.java

Objetivo da alteração:
Alterar de `204 No Content` para `200 OK` com corpo indicando sucesso.

Descrição:
A equipe decidiu devolver um corpo resumindo o resultado da remoção.

Git Diff:
```diff
@@
- return ResponseEntity.noContent().build();
+ return ResponseEntity.ok(Map.of("deleted", true));
```

Snapshot esperado:
```json
""
```

Snapshot recebido:
```json
{"deleted":true}
```

Impacto:
Mudança de status e payload.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A operação passou a ter um contrato explícito de resposta, diferente do anterior.

--------------------------------------------------------

Caso: C05-004

Categoria:
HTTP

Endpoint:
GET /authors/99999

Arquivos alterados:
AuthorController.java, GlobalExceptionHandler.java

Objetivo da alteração:
Mudar o status de `404 Not Found` para `410 Gone` para recursos removidos.

Descrição:
A camada de exceção passou a usar um código mais específico para o cenário não encontrado.

Git Diff:
```diff
@@
- return new ResponseEntity<>(errorResponse, HttpStatus.NOT_FOUND);
+ return new ResponseEntity<>(errorResponse, HttpStatus.GONE);
```

Snapshot esperado:
```json
{"status":"404","message":"Author not found with id: 99999","timestamp":"2026-05-26T13:25:34.6903399","path":"/authors/99999"}
```

Snapshot recebido:
```json
{"status":"410","message":"Author not found with id: 99999","timestamp":"2026-05-26T13:25:34.6903399","path":"/authors/99999"}
```

Impacto:
Mudança de status de erro.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
É uma alteração intencional de contrato de erro e o snapshot precisa ser atualizado.

--------------------------------------------------------

Caso: C05-005

Categoria:
HTTP

Endpoint:
GET /books/by-author/{authorId}

Arquivos alterados:
BookController.java

Objetivo da alteração:
Retornar `404 Not Found` para autores inexistentes em vez de `400 Bad Request`.

Descrição:
A API passou a informar de forma mais clara casos de autor inexistente.

Git Diff:
```diff
@@
- throw new ValidationException("Book must have an author")
+ throw new ResourceNotFoundException("Author", authorId)
```

Snapshot esperado:
```json
{"status":"400","message":"Book must have an author"}
```

Snapshot recebido:
```json
{"status":"404","message":"Author not found with id: 999"}
```

Impacto:
Mudança de status e mensagem de erro.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A alteração de contrato é intencional e deve ser refletida no snapshot.

--------------------------------------------------------

Caso: C05-006

Categoria:
HTTP

Endpoint:
POST /reviews

Arquivos alterados:
ReviewController.java

Objetivo da alteração:
Retornar `422 Unprocessable Entity` para reviews com dados inválidos.

Descrição:
A camada de controle passou a traduzir erros de validação para um status mais específico.

Git Diff:
```diff
@@
- ResponseEntity.status(HttpStatus.CREATED).body(createdReview)
+ ResponseEntity.status(HttpStatus.UNPROCESSABLE_ENTITY).body(errorResponse)
```

Snapshot esperado:
```json
{"id":2,"rating":4,"content":"Good read","bookId":1}
```

Snapshot recebido:
```json
{"status":"422","message":"Review rating must be between 1 and 5"}
```

Impacto:
Mudança de status HTTP para erro de validação.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A resposta observável mudou e o snapshot precisa refletir esse novo contrato.

--------------------------------------------------------

Caso: C05-007

Categoria:
HTTP

Endpoint:
GET /reviews/{id}

Arquivos alterados:
ReviewController.java

Objetivo da alteração:
Retornar `404 Not Found` para review inexistente com payload de erro padronizado.

Descrição:
A API passou a usar o mesmo padrão de erro para erro de recurso ausente em todas as rotas.

Git Diff:
```diff
@@
- return ResponseEntity.ok(review)
+ return ResponseEntity.status(HttpStatus.NOT_FOUND).body(errorResponse)
```

Snapshot esperado:
```json
{"id":1,"rating":5,"content":"Great book!","bookId":1}
```

Snapshot recebido:
```json
{"status":"404","message":"Review not found with id: 999","timestamp":"2026-05-26T13:25:34.6903399","path":"/reviews/999"}
```

Impacto:
Mudança de status e resposta em erro.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A regressão de contrato foi corrigida e a saída mudou por design.

--------------------------------------------------------

Caso: C05-008

Categoria:
HTTP

Endpoint:
PUT /books/{id}

Arquivos alterados:
BookController.java

Objetivo da alteração:
Retornar `201 Created` para atualizações bem-sucedidas.

Descrição:
A equipe decidiu tratar as atualizações como uma criação de nova versão do recurso.

Git Diff:
```diff
@@
- return ResponseEntity.ok(updatedBook)
+ return ResponseEntity.status(HttpStatus.CREATED).body(updatedBook)
```

Snapshot esperado:
```json
{"id":2,"title":"The Sign of the Four","isbn":"978-0-14-043925-1","authorId":5,"authorName":"Arthur Conan Doyle"}
```

Snapshot recebido:
```json
{"id":2,"title":"The Sign of the Four","isbn":"978-0-14-043925-1","authorId":5,"authorName":"Arthur Conan Doyle"}
```

Impacto:
Mudança de status HTTP em update.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
É uma mudança de contrato explícita, mesmo com body idêntico.

--------------------------------------------------------

Caso: C05-009

Categoria:
HTTP

Endpoint:
DELETE /reviews/{id}

Arquivos alterados:
ReviewController.java

Objetivo da alteração:
Retornar `200 OK` com mensagem simples em vez de `204 No Content`.

Descrição:
A equipe decidiu oferecer uma confirmação textual após a remoção.

Git Diff:
```diff
@@
- return ResponseEntity.noContent().build();
+ return ResponseEntity.ok(Map.of("message", "Review deleted"));
```

Snapshot esperado:
```json
""
```

Snapshot recebido:
```json
{"message":"Review deleted"}
```

Impacto:
Mudança de resposta de delete.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A API passou a devolver um contrato explícito após a remoção e o snapshot deve mudar.

--------------------------------------------------------

Caso: C05-010

Categoria:
HTTP

Endpoint:
POST /books

Arquivos alterados:
BookController.java

Objetivo da alteração:
Retornar `415 Unsupported Media Type` para payloads sem JSON.

Descrição:
A camada de controle passou a validar o tipo de mídia recebido para garantir maior consistência.

Git Diff:
```diff
@@
- contentType(MediaType.APPLICATION_JSON)
+ contentType(MediaType.APPLICATION_XML)
```

Snapshot esperado:
```json
{"id":3,"title":"The Hound of the Baskervilles","isbn":"978-0-14-043926-8","authorId":6,"authorName":"Arthur Conan Doyle"}
```

Snapshot recebido:
```json
{"status":"415","message":"Unsupported media type"}
```

Impacto:
Mudança de status e erro de conteúdo.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
Essa mudança afeta o contrato observable e deve refletir no snapshot.

--------------------------------------------------------

### Categoria 6 — Tratamento de erros

--------------------------------------------------------

Caso: C06-001

Categoria:
Tratamento de erros

Endpoint:
GET /authors/99999

Arquivos alterados:
GlobalExceptionHandler.java

Objetivo da alteração:
Padronizar o formato do payload de erro de recurso inexistente.

Descrição:
A equipe decidiu adicionar o campo `path` e `timestamp` no mesmo formato que já era usado para outros endpoints.

Git Diff:
```diff
@@
- .message(ex.getMessage())
+ .message(ex.getMessage())
+ .timestamp(LocalDateTime.now(clock).format(dateTimeFormatter))
+ .path(request.getDescription(false).replace("uri=", ""))
```

Snapshot esperado:
```json
{"status":"404","message":"Author not found with id: 99999"}
```

Snapshot recebido:
```json
{"status":"404","message":"Author not found with id: 99999","timestamp":"2026-05-26T13:25:34.6903399","path":"/authors/99999"}
```

Impacto:
Mudança na forma do erro retornado.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A resposta de erro foi enriquecida de forma intencional.

--------------------------------------------------------

Caso: C06-002

Categoria:
Tratamento de erros

Endpoint:
POST /books

Arquivos alterados:
GlobalExceptionHandler.java

Objetivo da alteração:
Uniformizar mensagens de validação com prefixo `Validation error:`.

Descrição:
A equipe decidiu deixar todas as mensagens de erro com um padrão comum.

Git Diff:
```diff
@@
- .message(ex.getMessage())
+ .message("Validation error: " + ex.getMessage())
```

Snapshot esperado:
```json
{"status":"400","message":"Book title cannot be empty"}
```

Snapshot recebido:
```json
{"status":"400","message":"Validation error: Book title cannot be empty"}
```

Impacto:
Mudança na mensagem de erro.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A interface do erro mudou por design e o snapshot deve refletir isso.

--------------------------------------------------------

Caso: C06-003

Categoria:
Tratamento de erros

Endpoint:
POST /reviews

Arquivos alterados:
GlobalExceptionHandler.java

Objetivo da alteração:
Adicionar o campo `error` no payload de erro de validação.

Descrição:
A equipe passou a usar um envelope mais explícito para erros de validação.

Git Diff:
```diff
@@
- .message(ex.getMessage())
+ .message(ex.getMessage())
+ .error("validation")
```

Snapshot esperado:
```json
{"status":"400","message":"Review rating must be between 1 and 5"}
```

Snapshot recebido:
```json
{"status":"400","message":"Review rating must be between 1 and 5","error":"validation"}
```

Impacto:
Mudança na estrutura de erro.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A resposta passou a ter um campo adicional e é uma mudança intencional.

--------------------------------------------------------

Caso: C06-004

Categoria:
Tratamento de erros

Endpoint:
GET /books/{id}

Arquivos alterados:
GlobalExceptionHandler.java

Objetivo da alteração:
Trocar `message` por `detail` em erros de recurso não encontrado.

Descrição:
A equipe passou a usar um nome mais semântico para a descrição do erro.

Git Diff:
```diff
@@
- .message(ex.getMessage())
+ .detail(ex.getMessage())
```

Snapshot esperado:
```json
{"status":"404","message":"Book not found with id: 999"}
```

Snapshot recebido:
```json
{"status":"404","detail":"Book not found with id: 999"}
```

Impacto:
Mudança de nome de propriedade do erro.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A estrutura do erro mudou e isso é observado no snapshot.

--------------------------------------------------------

Caso: C06-005

Categoria:
Tratamento de erros

Endpoint:
GET /authors/{id}

Arquivos alterados:
GlobalExceptionHandler.java

Objetivo da alteração:
Adicionar um código de erro associado ao payload.

Descrição:
A camada de exceção passou a incluir o código da categoria do erro para facilitar a integração.

Git Diff:
```diff
@@
- .message(ex.getMessage())
+ .message(ex.getMessage())
+ .code("NOT_FOUND")
```

Snapshot esperado:
```json
{"status":"404","message":"Author not found with id: 999"}
```

Snapshot recebido:
```json
{"status":"404","message":"Author not found with id: 999","code":"NOT_FOUND"}
```

Impacto:
Mudança de estrutura de erro.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
O contrato de erro foi expandido de forma planejada.

--------------------------------------------------------

Caso: C06-006

Categoria:
Tratamento de erros

Endpoint:
POST /authors

Arquivos alterados:
AuthorService.java, GlobalExceptionHandler.java

Objetivo da alteração:
Substituir mensagens de validação genéricas por mensagens específicas por campo.

Descrição:
A equipe decidiu melhorar a clareza das respostas quando o payload é inválido.

Git Diff:
```diff
@@
- throw new ValidationException("Author name cannot be empty")
+ throw new ValidationException("firstName: Author name cannot be empty")
```

Snapshot esperado:
```json
{"status":"400","message":"Author name cannot be empty"}
```

Snapshot recebido:
```json
{"status":"400","message":"firstName: Author name cannot be empty"}
```

Impacto:
Mudança na mensagem de erro.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A resposta passou a ser mais informativa e deve ser refletida no snapshot.

--------------------------------------------------------

Caso: C06-007

Categoria:
Tratamento de erros

Endpoint:
POST /books

Arquivos alterados:
BookService.java, GlobalExceptionHandler.java

Objetivo da alteração:
Adicionar `requestId` ao payload de erro para rastreio.

Descrição:
A equipe decidiu incluir um identificador de rastreio para facilitar suporte operacional.

Git Diff:
```diff
@@
+ .requestId(UUID.randomUUID().toString())
```

Snapshot esperado:
```json
{"status":"400","message":"Book title cannot be empty"}
```

Snapshot recebido:
```json
{"status":"400","message":"Book title cannot be empty","requestId":"<UUID>"}
```

Impacto:
Mudança em erros de validação.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A resposta passou a ter um campo adicional com propósito operacional.

--------------------------------------------------------

Caso: C06-008

Categoria:
Tratamento de erros

Endpoint:
GET /reviews/99999

Arquivos alterados:
ReviewService.java, GlobalExceptionHandler.java

Objetivo da alteração:
Trocar a mensagem de recurso não encontrado por uma descrição mais amigável.

Descrição:
A equipe racionalizou a mensagem para clientes de API.

Git Diff:
```diff
@@
- throw new ResourceNotFoundException("Review", id)
+ throw new ResourceNotFoundException("Review resource", id)
```

Snapshot esperado:
```json
{"status":"404","message":"Review not found with id: 999"}
```

Snapshot recebido:
```json
{"status":"404","message":"Review resource not found with id: 999"}
```

Impacto:
Mudança na mensagem de erro.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A mensagem de erro mudou e isso deve ser refletido no snapshot.

--------------------------------------------------------

Caso: C06-009

Categoria:
Tratamento de erros

Endpoint:
POST /reviews

Arquivos alterados:
ReviewService.java

Objetivo da alteração:
Retornar `400 Bad Request` para reviews associadas a livros inexistentes.

Descrição:
A equipe decidiu tratar esse cenário como invalidação de entrada em vez de not found.

Git Diff:
```diff
@@
- throw new ResourceNotFoundException("Book", reviewDTO.getBookId())
+ throw new ValidationException("Review must be associated with a book")
```

Snapshot esperado:
```json
{"status":"404","message":"Book not found with id: 999"}
```

Snapshot recebido:
```json
{"status":"400","message":"Review must be associated with a book"}
```

Impacto:
Mudança de status e mensagem de erro.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
Esse é um ajuste explícito de comportamento de erro da API.

--------------------------------------------------------

Caso: C06-010

Categoria:
Tratamento de erros

Endpoint:
GET /authors/{id}

Arquivos alterados:
GlobalExceptionHandler.java

Objetivo da alteração:
Enviar `500 Internal Server Error` para exceções inesperadas com envelope padrão.

Descrição:
A equipe passou a padronizar o tratamento de falhas imprevistas.

Git Diff:
```diff
@@
- .message("An unexpected error occurred")
+ .message("An unexpected error occurred")
+ .code("INTERNAL_ERROR")
```

Snapshot esperado:
```json
{"status":"500","message":"An unexpected error occurred"}
```

Snapshot recebido:
```json
{"status":"500","message":"An unexpected error occurred","code":"INTERNAL_ERROR"}
```

Impacto:
Mudança estrutural de erro interno.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A resposta passou a ter um campo de contrato novo e de objetivo operacional.

--------------------------------------------------------

### Categoria 7 — Coleções

--------------------------------------------------------

Caso: C07-001

Categoria:
Coleções

Endpoint:
GET /authors

Arquivos alterados:
AuthorService.java

Objetivo da alteração:
Ordenar autores alfabeticamente por `lastName`.

Descrição:
A equipe decidiu padronizar a ordem de exibição na listagem pública.

Git Diff:
```diff
@@
- .findAll()
+ .findAll().stream().sorted(Comparator.comparing(Author::getLastName))
```

Snapshot esperado:
```json
[{"id":1,"firstName":"J.K.","lastName":"Rowling","email":"jk@example.com"},{"id":2,"firstName":"George R.R.","lastName":"Martin","email":"grrm@example.com"}]
```

Snapshot recebido:
```json
[{"id":2,"firstName":"George R.R.","lastName":"Martin","email":"grrm@example.com"},{"id":1,"firstName":"J.K.","lastName":"Rowling","email":"jk@example.com"}]
```

Impacto:
Mudança de ordem da coleção.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A ordem da lista passou a ser parte da saída observável da API.

--------------------------------------------------------

Caso: C07-002

Categoria:
Coleções

Endpoint:
GET /books/by-author/{authorId}

Arquivos alterados:
BookService.java

Objetivo da alteração:
Ordenar livros por título na coleção retornada.

Descrição:
A equipe optou por uma ordenação mais amigável para clientes.

Git Diff:
```diff
@@
- .findByAuthorId(authorId)
+ .findByAuthorId(authorId).stream().sorted(Comparator.comparing(Book::getTitle))
```

Snapshot esperado:
```json
[{"id":1,"title":"The Hobbit","isbn":"123456789","authorId":1,"authorName":"J.K. Rowling"},{"id":2,"title":"The Lord of the Rings","isbn":"987654321","authorId":1,"authorName":"J.K. Rowling"}]
```

Snapshot recebido:
```json
[{"id":2,"title":"The Lord of the Rings","isbn":"987654321","authorId":1,"authorName":"J.K. Rowling"},{"id":1,"title":"The Hobbit","isbn":"123456789","authorId":1,"authorName":"J.K. Rowling"}]
```

Impacto:
Mudança de ordem na coleção.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
O conjunto retornado mudou de ordem e isso altera o snapshot.

--------------------------------------------------------

Caso: C07-003

Categoria:
Coleções

Endpoint:
GET /reviews/by-book/{bookId}

Arquivos alterados:
ReviewService.java

Objetivo da alteração:
Ordenar reviews por data de criação; como o modelo atual não tem data, a ordem é mantida por id crescente.

Descrição:
A equipe decidiu estabilizar a coleção para leitura consistente.

Git Diff:
```diff
@@
- .findByBookId(bookId)
+ .findByBookId(bookId).stream().sorted(Comparator.comparing(Review::getId))
```

Snapshot esperado:
```json
[{"id":2,"rating":5,"content":"Excellent"},{"id":1,"rating":3,"content":"Okay"}]
```

Snapshot recebido:
```json
[{"id":1,"rating":3,"content":"Okay"},{"id":2,"rating":5,"content":"Excellent"}]
```

Impacto:
Mudança de ordernação da coleção.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
Mesmo sem um campo de data, a ordem da coleção mudou intencionalmente.

--------------------------------------------------------

Caso: C07-004

Categoria:
Coleções

Endpoint:
GET /books

Arquivos alterados:
BookService.java

Objetivo da alteração:
Filtrar livros com `isbn` vazio das respostas de coleção.

Descrição:
A equipe decidiu remover itens inválidos da listagem pública.

Git Diff:
```diff
@@
- .findAll()
+ .findAll().stream().filter(b -> b.getIsbn() != null && !b.getIsbn().isBlank())
```

Snapshot esperado:
```json
[{"id":1,"title":"The Hobbit","isbn":"123456789","authorId":1,"authorName":"J.K. Rowling"}]
```

Snapshot recebido:
```json
[]
```

Impacto:
Mudança de conteúdo da coleção.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A regra alterou a coleção devolvida e o snapshot precisa refletir isso.

--------------------------------------------------------

Caso: C07-005

Categoria:
Coleções

Endpoint:
GET /authors

Arquivos alterados:
AuthorService.java

Objetivo da alteração:
Filtrar autores sem e-mail da listagem.

Descrição:
A API passou a esconder usuários incompletos na listagem pública.

Git Diff:
```diff
@@
- .findAll()
+ .findAll().stream().filter(a -> a.getEmail() != null && a.getEmail().contains("@"))
```

Snapshot esperado:
```json
[{"id":1,"firstName":"J.K.","lastName":"Rowling","email":"jk@example.com"}]
```

Snapshot recebido:
```json
[]
```

Impacto:
Mudança de coleção resultado.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A regra de filtragem alterou a saída observável e o snapshot deve mudar.

--------------------------------------------------------

Caso: C07-006

Categoria:
Coleções

Endpoint:
GET /reviews

Arquivos alterados:
ReviewService.java

Objetivo da alteração:
Exibir somente reviews com rating maior ou igual a 4.

Descrição:
A equipe passou a priorizar avaliações positivas na listagem.

Git Diff:
```diff
@@
- .findAll()
+ .findAll().stream().filter(r -> r.getRating() >= 4)
```

Snapshot esperado:
```json
[{"id":1,"rating":3,"content":"Okay"},{"id":2,"rating":5,"content":"Excellent"}]
```

Snapshot recebido:
```json
[{"id":2,"rating":5,"content":"Excellent"}]
```

Impacto:
Mudança de conteúdo da coleção.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A regra alterou a composição da coleção e o snapshot precisa ser atualizado.

--------------------------------------------------------

Caso: C07-007

Categoria:
Coleções

Endpoint:
GET /books/by-author/{authorId}

Arquivos alterados:
BookService.java

Objetivo da alteração:
Limitar a coleção a até 10 livros por autor.

Descrição:
A equipe decidiu introduzir um limite operacional para respostas de coleção.

Git Diff:
```diff
@@
- .findByAuthorId(authorId)
+ .findByAuthorId(authorId).stream().limit(10)
```

Snapshot esperado:
```json
[{"id":1,"title":"Book A"},{"id":2,"title":"Book B"}]
```

Snapshot recebido:
```json
[{"id":1,"title":"Book A"},{"id":2,"title":"Book B"}]
```

Impacto:
Mudança de tamanho da coleção.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A coleção passou a ter um limite explícito e o snapshot precisa refletir isso.

--------------------------------------------------------

Caso: C07-008

Categoria:
Coleções

Endpoint:
GET /reviews/by-book/{bookId}

Arquivos alterados:
ReviewService.java

Objetivo da alteração:
Excluir reviews sem conteúdo textual da coleção.

Descrição:
A equipe decidiu não expor avaliações sem texto da listagem.

Git Diff:
```diff
@@
- .findByBookId(bookId)
+ .findByBookId(bookId).stream().filter(r -> r.getContent() != null && !r.getContent().isBlank())
```

Snapshot esperado:
```json
[{"id":1,"rating":3,"content":"Okay"},{"id":2,"rating":5,"content":"Great"}]
```

Snapshot recebido:
```json
[{"id":1,"rating":3,"content":"Okay"},{"id":2,"rating":5,"content":"Great"}]
```

Impacto:
Mudança na composição da coleção.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A lógica de filtragem alterou a coleção observável.

--------------------------------------------------------

Caso: C07-009

Categoria:
Coleções

Endpoint:
GET /books

Arquivos alterados:
BookService.java

Objetivo da alteração:
Retornar apenas livros com `authorId` maior que zero.

Descrição:
A equipe decidiu filtrar relacionamentos inválidos da listagem.

Git Diff:
```diff
@@
- .findAll()
+ .findAll().stream().filter(b -> b.getAuthor() != null && b.getAuthor().getId() > 0)
```

Snapshot esperado:
```json
[{"id":1,"title":"The Hobbit","isbn":"123456789","authorId":1,"authorName":"J.K. Rowling"}]
```

Snapshot recebido:
```json
[{"id":1,"title":"The Hobbit","isbn":"123456789","authorId":1,"authorName":"J.K. Rowling"}]
```

Impacto:
Mudança de conteúdo da coleção.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A regra de filtragem impacta a lista retornada e o snapshot deve mudar.

--------------------------------------------------------

Caso: C07-010

Categoria:
Coleções

Endpoint:
GET /authors

Arquivos alterados:
AuthorService.java

Objetivo da alteração:
Remover duplicatas de autores na listagem.

Descrição:
A equipe decidiu garantir que a listagem não repita recursos por problemas de integração.

Git Diff:
```diff
@@
- .findAll()
+ .findAll().stream().distinct()
```

Snapshot esperado:
```json
[{"id":1,"firstName":"J.K.","lastName":"Rowling","email":"jk@example.com"},{"id":2,"firstName":"George R.R.","lastName":"Martin","email":"grrm@example.com"}]
```

Snapshot recebido:
```json
[{"id":1,"firstName":"J.K.","lastName":"Rowling","email":"jk@example.com"},{"id":2,"firstName":"George R.R.","lastName":"Martin","email":"grrm@example.com"}]
```

Impacto:
Mudança na composição da coleção.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A coleção passou a ser deduplicada, alterando o resultado observado.

--------------------------------------------------------

### Categoria 8 — Campos não determinísticos

--------------------------------------------------------

Caso: C08-001

Categoria:
Campos não determinísticos

Endpoint:
GET /authors/99999

Arquivos alterados:
GlobalExceptionHandler.java

Objetivo da alteração:
Adicionar um timestamp de erro com hora atual.

Descrição:
A equipe decidiu registrar a hora exata do erro na resposta.

Git Diff:
```diff
@@
- .timestamp("2026-05-26T13:25:34.6903399")
+ .timestamp(LocalDateTime.now(clock).format(dateTimeFormatter))
```

Snapshot esperado:
```json
{"status":"404","message":"Author not found with id: 99999","timestamp":"2026-05-26T13:25:34.6903399","path":"/authors/99999"}
```

Snapshot recebido:
```json
{"status":"404","message":"Author not found with id: 99999","timestamp":"2026-08-04T10:00:00","path":"/authors/99999"}
```

Impacto:
Variação temporal na resposta.

Classificação Humana:
SHOULD_NOT_UPDATE

Justificativa:
O campo é intrinsicamente não determinístico; o snapshot não deveria ser atualizado por esse motivo.

--------------------------------------------------------

Caso: C08-002

Categoria:
Campos não determinísticos

Endpoint:
POST /authors

Arquivos alterados:
AuthorService.java

Objetivo da alteração:
Usar um `id` gerado automaticamente pela base em vez de um valor estático.

Descrição:
A camada de persistência passou a delegar a geração do identificador ao banco.

Git Diff:
```diff
@@
- author.setId(3L)
+ // relies on database identity
```

Snapshot esperado:
```json
{"id":3,"firstName":"Isaac","lastName":"Asimov","email":"isaac@example.com"}
```

Snapshot recebido:
```json
{"id":12,"firstName":"Isaac","lastName":"Asimov","email":"isaac@example.com"}
```

Impacto:
Variação do identificador retornado.

Classificação Humana:
SHOULD_NOT_UPDATE

Justificativa:
A mudança não representa um comportamento intencional do contrato; ela depende do ambiente de execução.

--------------------------------------------------------

Caso: C08-003

Categoria:
Campos não determinísticos

Endpoint:
POST /books

Arquivos alterados:
BookService.java

Objetivo da alteração:
Adicionar um `requestId` gerado por UUID à resposta de erro.

Descrição:
A equipe decidiu incluir um identificador de correlação em erros de validação.

Git Diff:
```diff
@@
+ .requestId(UUID.randomUUID().toString())
```

Snapshot esperado:
```json
{"status":"400","message":"Book title cannot be empty"}
```

Snapshot recebido:
```json
{"status":"400","message":"Book title cannot be empty","requestId":"87b4d7b5-3f90-4a0a-b0a7-1ab8b7d2e4f8"}
```

Impacto:
Campo aleatório na resposta.

Classificação Humana:
SHOULD_NOT_UPDATE

Justificativa:
Quando o campo é aleatório, a atualização do snapshot seria espúria e não refletiria uma mudança de contrato.

--------------------------------------------------------

Caso: C08-004

Categoria:
Campos não determinísticos

Endpoint:
GET /authors

Arquivos alterados:
AuthorService.java

Objetivo da alteração:
Adicionar um campo com o horário atual da serialização.

Descrição:
A API passou a anexar um timestamp de composição em cada resposta para observabilidade.

Git Diff:
```diff
@@
+ .generatedAt(LocalDateTime.now())
```

Snapshot esperado:
```json
[{"id":1,"firstName":"J.K.","lastName":"Rowling","email":"jk@example.com"}]
```

Snapshot recebido:
```json
[{"id":1,"firstName":"J.K.","lastName":"Rowling","email":"jk@example.com","generatedAt":"2026-08-04T10:00:00"}]
```

Impacto:
Campo temporal não determinístico.

Classificação Humana:
SHOULD_NOT_UPDATE

Justificativa:
O snapshot não deve ser atualizado para um valor que muda a cada execução.

--------------------------------------------------------

Caso: C08-005

Categoria:
Campos não determinísticos

Endpoint:
GET /reviews

Arquivos alterados:
ReviewService.java

Objetivo da alteração:
Adicionar um `traceId` para cada resposta de coleção.

Descrição:
A equipe decidiu incluir uma identidade temporal única para observabilidade distribuída.

Git Diff:
```diff
@@
+ .traceId(UUID.randomUUID().toString())
```

Snapshot esperado:
```json
[{"id":1,"rating":5,"content":"Great book!","bookId":1}]
```

Snapshot recebido:
```json
[{"id":1,"rating":5,"content":"Great book!","bookId":1,"traceId":"3f654e52-21ea-4168-8e30-798ebbf1458d"}]
```

Impacto:
Campo não determinístico na resposta.

Classificação Humana:
SHOULD_NOT_UPDATE

Justificativa:
O valor é sempre diferente e não representa uma alteração de comportamento estável do contrato.

--------------------------------------------------------

### Categoria 9 — Ruído

--------------------------------------------------------

Caso: C09-001

Categoria:
Ruído

Endpoint:
GET /authors

Arquivos alterados:
AuthorService.java

Objetivo da alteração:
Trocar a indentação do JSON produzido por um formatter que não altera o conteúdo semântico.

Descrição:
A mudança é puramente estética e não deveria impactar o contrato.

Git Diff:
```diff
@@
- ObjectMapper mapper = new ObjectMapper();
+ ObjectMapper mapper = new ObjectMapper().enable(SerializationFeature.INDENT_OUTPUT);
```

Snapshot esperado:
```json
[{"id":1,"firstName":"J.K.","lastName":"Rowling","email":"jk@example.com"}]
```

Snapshot recebido:
```json
[
  {"id":1,"firstName":"J.K.","lastName":"Rowling","email":"jk@example.com"}
]
```

Impacto:
Mudança visual no corpo da resposta.

Classificação Humana:
SHOULD_NOT_UPDATE

Justificativa:
A diferença é cosmética e não representa uma mudança semântica no contrato.

--------------------------------------------------------

Caso: C09-002

Categoria:
Ruído

Endpoint:
GET /books

Arquivos alterados:
BookController.java

Objetivo da alteração:
Adicionar espaços extras em torno de campos em um corpo de resposta já estável.

Descrição:
A mudança reflete apenas um ajuste de formatting e não altera a semântica do JSON.

Git Diff:
```diff
@@
- return ResponseEntity.ok(books);
+ return ResponseEntity.ok(books);
```

Snapshot esperado:
```json
[{"id":1,"title":"The Hobbit","isbn":"123456789","authorId":1,"authorName":"J.K. Rowling"}]
```

Snapshot recebido:
```json
[{"id":1,"title":"The Hobbit","isbn":"123456789","authorId":1,"authorName":"J.K. Rowling"}]
```

Impacto:
Nenhum impacto semântico.

Classificação Humana:
SHOULD_NOT_UPDATE

Justificativa:
Não há mudança material no payload; o snapshot não deve ser alterado.

--------------------------------------------------------

Caso: C09-003

Categoria:
Ruído

Endpoint:
GET /reviews

Arquivos alterados:
ReviewService.java

Objetivo da alteração:
Mudar a ordem de importações e comentários de código sem alterar a resposta.

Descrição:
Essa mudança é estritamente cosmética na implementação.

Git Diff:
```diff
@@
- import java.util.List;
+ import java.util.List;
+ import java.util.Collections;
```

Snapshot esperado:
```json
[{"id":1,"rating":5,"content":"Great book!","bookId":1}]
```

Snapshot recebido:
```json
[{"id":1,"rating":5,"content":"Great book!","bookId":1}]
```

Impacto:
Nenhum impacto na resposta.

Classificação Humana:
SHOULD_NOT_UPDATE

Justificativa:
A mudança não afeta a saída da API e não deve mudar o snapshot.

--------------------------------------------------------

Caso: C09-004

Categoria:
Ruído

Endpoint:
GET /books/{id}

Arquivos alterados:
BookService.java

Objetivo da alteração:
Trocar o nome local de uma variável sem alterar o comportamento.

Descrição:
A alteração é puramente interna e não afeta a resposta serializada.

Git Diff:
```diff
@@
- Book book = bookRepository.findById(id)
+ Book currentBook = bookRepository.findById(id)
```

Snapshot esperado:
```json
{"id":1,"title":"The Hobbit","isbn":"123456789","authorId":1,"authorName":"J.K. Rowling"}
```

Snapshot recebido:
```json
{"id":1,"title":"The Hobbit","isbn":"123456789","authorId":1,"authorName":"J.K. Rowling"}
```

Impacto:
Nenhum impacto observável.

Classificação Humana:
SHOULD_NOT_UPDATE

Justificativa:
A saída é exatamente a mesma e o snapshot não precisa mudar.

--------------------------------------------------------

Caso: C09-005

Categoria:
Ruído

Endpoint:
GET /authors/{id}

Arquivos alterados:
AuthorController.java

Objetivo da alteração:
Mover uma instrução de retorno para outra linha sem impactar a resposta.

Descrição:
A mudança é estritamente cosmética na forma de implementar o endpoint.

Git Diff:
```diff
@@
- return ResponseEntity.ok(author);
+ return
+     ResponseEntity.ok(author);
```

Snapshot esperado:
```json
{"id":4,"firstName":"J.R.R.","lastName":"Tolkien","email":"tolkien@example.com"}
```

Snapshot recebido:
```json
{"id":4,"firstName":"J.R.R.","lastName":"Tolkien","email":"tolkien@example.com"}
```

Impacto:
Nenhum impacto observável.

Classificação Humana:
SHOULD_NOT_UPDATE

Justificativa:
O comportamento da API é idêntico e o snapshot não deve ser alterado.

--------------------------------------------------------

### Categoria 10 — Bugs reais

--------------------------------------------------------

Caso: C10-001

Categoria:
Bugs reais

Endpoint:
POST /authors

Arquivos alterados:
AuthorService.java

Objetivo da alteração:
Corrigir a criação de autores com `firstName` e `lastName` trocados na persistência.

Descrição:
Um bug real fazia o sistema gravar o sobrenome no primeiro nome e vice-versa.

Git Diff:
```diff
@@
- author.setFirstName(authorDTO.getLastName());
- author.setLastName(authorDTO.getFirstName());
+ author.setFirstName(authorDTO.getFirstName());
+ author.setLastName(authorDTO.getLastName());
```

Snapshot esperado:
```json
{"id":3,"firstName":"Isaac","lastName":"Asimov","email":"isaac@example.com"}
```

Snapshot recebido:
```json
{"id":3,"firstName":"Isaac","lastName":"Asimov","email":"isaac@example.com"}
```

Impacto:
Correção de bug de persistência.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
O comportamento foi corrigido de forma intencional; o snapshot deve refletir a saída correta.

--------------------------------------------------------

Caso: C10-002

Categoria:
Bugs reais

Endpoint:
POST /books

Arquivos alterados:
BookService.java

Objetivo da alteração:
Corrigir o relacionamento entre livro e autor na criação.

Descrição:
Um bug fazia o livro ser criado com um autor inválido ou nulo.

Git Diff:
```diff
@@
- book.setAuthor(null);
+ book.setAuthor(author);
```

Snapshot esperado:
```json
{"id":3,"title":"The Hound of the Baskervilles","isbn":"978-0-14-043926-8","authorId":6,"authorName":"Arthur Conan Doyle"}
```

Snapshot recebido:
```json
{"id":3,"title":"The Hound of the Baskervilles","isbn":"978-0-14-043926-8","authorId":6,"authorName":"Arthur Conan Doyle"}
```

Impacto:
Correção de bug de relacionamento.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A correção altera o valor real retornado pelo endpoint e deve ser refletida no snapshot.

--------------------------------------------------------

Caso: C10-003

Categoria:
Bugs reais

Endpoint:
POST /reviews

Arquivos alterados:
ReviewService.java

Objetivo da alteração:
Corrigir a validação de rating para aceitar valores válidos.

Descrição:
Um bug fazia o sistema rejeitar reviews legítimas com rating 5.

Git Diff:
```diff
@@
- if (rating < 1 || rating > 4)
+ if (rating < 1 || rating > 5)
```

Snapshot esperado:
```json
{"status":"400","message":"Review rating must be between 1 and 4"}
```

Snapshot recebido:
```json
{"id":2,"rating":5,"content":"Great read","bookId":1}
```

Impacto:
Correção de bug de validação.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A correção faz o fluxo de sucesso voltar a funcionar e o snapshot deve mudar.

--------------------------------------------------------

Caso: C10-004

Categoria:
Bugs reais

Endpoint:
GET /authors/{id}

Arquivos alterados:
AuthorService.java

Objetivo da alteração:
Corrigir a recuperação de autores por id com `Optional.empty()` mal tratado.

Descrição:
Um bug fazia o endpoint retornar um autor vazio em vez de gerar `404` quando o recurso não existia.

Git Diff:
```diff
@@
- return convertToDTO(author)
+ throw new ResourceNotFoundException("Author", id)
```

Snapshot esperado:
```json
{"id":4,"firstName":"J.R.R.","lastName":"Tolkien","email":"tolkien@example.com"}
```

Snapshot recebido:
```json
{"status":"404","message":"Author not found with id: 999"}
```

Impacto:
Correção de bug de resposta de erro.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A saída de erro corrigida é um novo comportamento intencional do endpoint.

--------------------------------------------------------

Caso: C10-005

Categoria:
Bugs reais

Endpoint:
GET /books/by-author/{authorId}

Arquivos alterados:
BookService.java

Objetivo da alteração:
Corrigir o retorno de uma lista vazia quando o autor existe e possui livros.

Descrição:
Um bug fazia a operação ignorar os livros do autor e retornar `[]` indevidamente.

Git Diff:
```diff
@@
- return Collections.emptyList();
+ return bookRepository.findByAuthorId(authorId)
```

Snapshot esperado:
```json
[]
```

Snapshot recebido:
```json
[{"id":1,"title":"The Hobbit","isbn":"123456789","authorId":1,"authorName":"J.K. Rowling"}]
```

Impacto:
Correção de bug de coleção.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A resposta correta mudou e o snapshot deve ser atualizado.

--------------------------------------------------------

Caso: C10-006

Categoria:
Bugs reais

Endpoint:
GET /reviews/by-book/{bookId}

Arquivos alterados:
ReviewService.java

Objetivo da alteração:
Corrigir a listagem de reviews para incluir todas as avaliações do livro.

Descrição:
Um bug fazia a coleção retornar apenas a primeira review associada ao livro.

Git Diff:
```diff
@@
- .findFirst()
+ .findAll()
```

Snapshot esperado:
```json
[{"id":1,"rating":3,"content":"Okay"}]
```

Snapshot recebido:
```json
[{"id":1,"rating":3,"content":"Okay"},{"id":2,"rating":5,"content":"Excellent"}]
```

Impacto:
Correção de bug de coleção.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A coleção retornada passou a ser completa e a alteração é intencional.

--------------------------------------------------------

Caso: C10-007

Categoria:
Bugs reais

Endpoint:
POST /authors

Arquivos alterados:
AuthorService.java

Objetivo da alteração:
Corrigir o armazenamento de `email` em caixa alta.

Descrição:
Um bug fazia o sistema salvar e retornar o e-mail em maiúsculas mesmo quando o cliente enviava minúsculas.

Git Diff:
```diff
@@
- author.setEmail(authorDTO.getEmail().toUpperCase())
+ author.setEmail(authorDTO.getEmail().toLowerCase())
```

Snapshot esperado:
```json
{"id":3,"firstName":"Isaac","lastName":"Asimov","email":"ISAAC@EXAMPLE.COM"}
```

Snapshot recebido:
```json
{"id":3,"firstName":"Isaac","lastName":"Asimov","email":"isaac@example.com"}
```

Impacto:
Correção de bug de normalização.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A resposta correta agora é consistente com a regra esperada.

--------------------------------------------------------

Caso: C10-008

Categoria:
Bugs reais

Endpoint:
POST /books

Arquivos alterados:
BookService.java

Objetivo da alteração:
Corrigir a persistência do título sem espaços extras.

Descrição:
Um bug deixava o sistema salvar o título com espaços no início e fim.

Git Diff:
```diff
@@
- book.setTitle(bookDTO.getTitle())
+ book.setTitle(bookDTO.getTitle().trim())
```

Snapshot esperado:
```json
{"id":3,"title":"The Hound of the Baskervilles","isbn":"978-0-14-043926-8","authorId":6,"authorName":"Arthur Conan Doyle"}
```

Snapshot recebido:
```json
{"id":3,"title":"The Hound of the Baskervilles","isbn":"978-0-14-043926-8","authorId":6,"authorName":"Arthur Conan Doyle"}
```

Impacto:
Correção de bug de formatação.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A correção altera o valor salvo e retornado e deve ser refletida no snapshot.

--------------------------------------------------------

Caso: C10-009

Categoria:
Bugs reais

Endpoint:
GET /books/{id}

Arquivos alterados:
BookService.java

Objetivo da alteração:
Corrigir o cálculo do `authorName` para usar o nome do autor real.

Descrição:
Um bug fazia o endpoint usar o título do livro em vez do nome do autor.

Git Diff:
```diff
@@
- .authorName(book.getTitle())
+ .authorName(book.getAuthor().getFirstName() + " " + book.getAuthor().getLastName())
```

Snapshot esperado:
```json
{"id":1,"title":"The Hobbit","isbn":"123456789","authorId":1,"authorName":"The Hobbit"}
```

Snapshot recebido:
```json
{"id":1,"title":"The Hobbit","isbn":"123456789","authorId":1,"authorName":"J.K. Rowling"}
```

Impacto:
Correção de bug de serialização de relacionamento.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A resposta correta mudou de forma obviamente intencional.

--------------------------------------------------------

Caso: C10-010

Categoria:
Bugs reais

Endpoint:
GET /reviews/{id}

Arquivos alterados:
ReviewService.java

Objetivo da alteração:
Corrigir o nome do livro associado na review.

Descrição:
Um bug fazia a review carregar o título de um livro diferente do realmente associado.

Git Diff:
```diff
@@
- .bookTitle(review.getBook().getTitle())
+ .bookTitle(review.getBook().getTitle())
```

Snapshot esperado:
```json
{"id":1,"rating":5,"content":"Great book!","bookId":1,"bookTitle":"Wrong title"}
```

Snapshot recebido:
```json
{"id":1,"rating":5,"content":"Great book!","bookId":1,"bookTitle":"The Hobbit"}
```

Impacto:
Correção de bug de relacionamento.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A resposta correta agora corresponde ao relacionamento real.

--------------------------------------------------------

Caso: C10-011

Categoria:
Bugs reais

Endpoint:
POST /books

Arquivos alterados:
BookService.java

Objetivo da alteração:
Corrigir o uso do `authorId` recebido no payload ao criar o livro.

Descrição:
Um bug fazia a criação ignorar o `authorId` fornecido pelo cliente.

Git Diff:
```diff
@@
- book.setAuthor(authorRepository.findById(1L).orElseThrow(...))
+ book.setAuthor(authorRepository.findById(bookDTO.getAuthorId()).orElseThrow(...))
```

Snapshot esperado:
```json
{"id":3,"title":"The Hound of the Baskervilles","isbn":"978-0-14-043926-8","authorId":6,"authorName":"Arthur Conan Doyle"}
```

Snapshot recebido:
```json
{"id":3,"title":"The Hound of the Baskervilles","isbn":"978-0-14-043926-8","authorId":6,"authorName":"Arthur Conan Doyle"}
```

Impacto:
Correção de bug de associação ao autor.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A correção faz o endpoint devolver o relacionamento correto.

--------------------------------------------------------

Caso: C10-012

Categoria:
Bugs reais

Endpoint:
GET /books/{id}

Arquivos alterados:
BookService.java

Objetivo da alteração:
Corrigir a resposta para retornar `404` ao tentar acessar um livro inexistente.

Descrição:
Um bug fazia a API retornar um objeto vazio ao invés de um erro de recurso inexistente.

Git Diff:
```diff
@@
- return BookDTO.builder().build();
+ throw new ResourceNotFoundException("Book", id);
```

Snapshot esperado:
```json
{"id":1,"title":"The Hobbit","isbn":"123456789","authorId":1}
```

Snapshot recebido:
```json
{"status":"404","message":"Book not found with id: 999"}
```

Impacto:
Correção de bug de erro de recurso.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A resposta correta muda de sucesso para erro e o snapshot deve ser atualizado.

--------------------------------------------------------

Caso: C10-013

Categoria:
Bugs reais

Endpoint:
GET /reviews/{id}

Arquivos alterados:
ReviewService.java

Objetivo da alteração:
Corrigir a resposta de review para retornar o conteúdo real.

Descrição:
Um bug fazia a API retornar um `content` vazio para reviews que possuíam texto.

Git Diff:
```diff
@@
- .content("")
+ .content(review.getContent())
```

Snapshot esperado:
```json
{"id":1,"rating":5,"content":"","bookId":1}
```

Snapshot recebido:
```json
{"id":1,"rating":5,"content":"Great book!","bookId":1}
```

Impacto:
Correção de bug de serialização de conteúdo.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A saída corrigida representa um comportamento novo e legítimo da API.

--------------------------------------------------------

Caso: C10-014

Categoria:
Bugs reais

Endpoint:
GET /authors

Arquivos alterados:
AuthorService.java

Objetivo da alteração:
Corrigir a listagem para incluir autores criados recentemente.

Descrição:
Um bug fazia a listagem ignorar autores recém-criados por causa de uma consulta incompleta.

Git Diff:
```diff
@@
- return authorRepository.findByEmail(email)
+ return authorRepository.findAll()
```

Snapshot esperado:
```json
[]
```

Snapshot recebido:
```json
[{"id":3,"firstName":"Isaac","lastName":"Asimov","email":"isaac@example.com"}]
```

Impacto:
Correção de bug de coleção.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A lista corrigida passou a refletir o estado real do repositório.

--------------------------------------------------------

Caso: C10-015

Categoria:
Bugs reais

Endpoint:
POST /reviews

Arquivos alterados:
ReviewService.java

Objetivo da alteração:
Corrigir a criação de reviews para persistir o livro correto.

Descrição:
Um bug fazia a review ser associada ao livro errado na persistência.

Git Diff:
```diff
@@
- review.setBook(previousBook)
+ review.setBook(book)
```

Snapshot esperado:
```json
{"id":2,"rating":4,"content":"Good read","bookId":1}
```

Snapshot recebido:
```json
{"id":2,"rating":4,"content":"Good read","bookId":2}
```

Impacto:
Correção de bug de relacionamento de review.

Classificação Humana:
SHOULD_UPDATE

Justificativa:
A resposta passou a refletir o relacionamento correto e o snapshot deve ser atualizado.

--------------------------------------------------------

## 3. Resumo de casos por categoria

| ID | Categoria | Endpoint | Dificuldade | Classificação Esperada |
|---|---|---|---|---|
| C01-001 | Evolução de contrato | GET /authors | Fácil | SHOULD_UPDATE |
| C01-002 | Evolução de contrato | GET /authors/{id} | Fácil | SHOULD_UPDATE |
| C01-003 | Evolução de contrato | POST /authors | Fácil | SHOULD_UPDATE |
| C01-004 | Evolução de contrato | GET /books | Fácil | SHOULD_UPDATE |
| C01-005 | Evolução de contrato | POST /books | Fácil | SHOULD_UPDATE |
| C01-006 | Evolução de contrato | GET /reviews | Fácil | SHOULD_UPDATE |
| C01-007 | Evolução de contrato | POST /reviews | Fácil | SHOULD_UPDATE |
| C01-008 | Evolução de contrato | GET /books/by-author/{authorId} | Fácil | SHOULD_UPDATE |
| C01-009 | Evolução de contrato | PUT /authors/{id} | Médio | SHOULD_UPDATE |
| C01-010 | Evolução de contrato | PUT /books/{id} | Médio | SHOULD_UPDATE |
| C01-011 | Evolução de contrato | GET /reviews/{id} | Fácil | SHOULD_UPDATE |
| C01-012 | Evolução de contrato | DELETE /authors/{id} | Médio | SHOULD_UPDATE |
| C01-013 | Evolução de contrato | GET /books/{id} | Fácil | SHOULD_UPDATE |
| C01-014 | Evolução de contrato | GET /authors | Médio | SHOULD_UPDATE |
| C01-015 | Evolução de contrato | GET /reviews/by-book/{bookId} | Médio | SHOULD_UPDATE |
| C01-016 | Evolução de contrato | POST /authors | Fácil | SHOULD_UPDATE |
| C01-017 | Evolução de contrato | POST /books | Fácil | SHOULD_UPDATE |
| C01-018 | Evolução de contrato | GET /books/by-author/{authorId} | Fácil | SHOULD_UPDATE |
| C01-019 | Evolução de contrato | GET /reviews | Fácil | SHOULD_UPDATE |
| C01-020 | Evolução de contrato | GET /authors/{id} | Fácil | SHOULD_UPDATE |
| C02-001 | Breaking Change | POST /authors | Fácil | SHOULD_NOT_UPDATE |
| C02-002 | Breaking Change | GET /authors/{id} | Fácil | SHOULD_NOT_UPDATE |
| C02-003 | Breaking Change | POST /books | Fácil | SHOULD_NOT_UPDATE |
| C02-004 | Breaking Change | GET /books/{id} | Fácil | SHOULD_NOT_UPDATE |
| C02-005 | Breaking Change | GET /reviews/{id} | Fácil | SHOULD_NOT_UPDATE |
| C02-006 | Breaking Change | POST /reviews | Fácil | SHOULD_NOT_UPDATE |
| C02-007 | Breaking Change | DELETE /books/{id} | Fácil | SHOULD_NOT_UPDATE |
| C02-008 | Breaking Change | GET /authors/{id} | Médio | SHOULD_NOT_UPDATE |
| C02-009 | Breaking Change | GET /books/by-author/{authorId} | Médio | SHOULD_NOT_UPDATE |
| C02-010 | Breaking Change | POST /authors | Médio | SHOULD_NOT_UPDATE |
| C02-011 | Breaking Change | POST /books | Médio | SHOULD_NOT_UPDATE |
| C02-012 | Breaking Change | PUT /reviews/{id} | Médio | SHOULD_NOT_UPDATE |
| C02-013 | Breaking Change | GET /authors | Fácil | SHOULD_NOT_UPDATE |
| C02-014 | Breaking Change | GET /books | Fácil | SHOULD_NOT_UPDATE |
| C02-015 | Breaking Change | GET /reviews | Fácil | SHOULD_NOT_UPDATE |
| C02-016 | Breaking Change | POST /authors | Fácil | SHOULD_NOT_UPDATE |
| C02-017 | Breaking Change | GET /authors/{id} | Fácil | SHOULD_NOT_UPDATE |
| C02-018 | Breaking Change | GET /books/{id} | Fácil | SHOULD_NOT_UPDATE |
| C02-019 | Breaking Change | GET /reviews/{id} | Fácil | SHOULD_NOT_UPDATE |
| C02-020 | Breaking Change | GET /authors | Fácil | SHOULD_NOT_UPDATE |
| C03-001 | Regras de negócio | POST /authors | Fácil | SHOULD_UPDATE |
| C03-002 | Regras de negócio | POST /books | Fácil | SHOULD_UPDATE |
| C03-003 | Regras de negócio | POST /reviews | Fácil | SHOULD_UPDATE |
| C03-004 | Regras de negócio | POST /authors | Médio | SHOULD_UPDATE |
| C03-005 | Regras de negócio | POST /books | Médio | SHOULD_UPDATE |
| C03-006 | Regras de negócio | POST /reviews | Médio | SHOULD_UPDATE |
| C03-007 | Regras de negócio | PUT /authors/{id} | Médio | SHOULD_UPDATE |
| C03-008 | Regras de negócio | PUT /books/{id} | Médio | SHOULD_UPDATE |
| C03-009 | Regras de negócio | POST /reviews | Médio | SHOULD_UPDATE |
| C03-010 | Regras de negócio | GET /books/by-author/{authorId} | Médio | SHOULD_UPDATE |
| C03-011 | Regras de negócio | GET /reviews/by-book/{bookId} | Médio | SHOULD_UPDATE |
| C03-012 | Regras de negócio | GET /authors | Médio | SHOULD_UPDATE |
| C03-013 | Regras de negócio | PUT /authors/{id} | Médio | SHOULD_UPDATE |
| C03-014 | Regras de negócio | POST /books | Médio | SHOULD_UPDATE |
| C03-015 | Regras de negócio | POST /reviews | Difícil | SHOULD_UPDATE |
| C04-001 | Serialização | GET /authors/{id} | Fácil | SHOULD_UPDATE |
| C04-002 | Serialização | GET /books/{id} | Fácil | SHOULD_UPDATE |
| C04-003 | Serialização | GET /reviews/{id} | Fácil | SHOULD_UPDATE |
| C04-004 | Serialização | GET /authors | Fácil | SHOULD_UPDATE |
| C04-005 | Serialização | GET /books | Fácil | SHOULD_UPDATE |
| C04-006 | Serialização | GET /reviews | Fácil | SHOULD_UPDATE |
| C04-007 | Serialização | GET /authors/{id} | Médio | SHOULD_UPDATE |
| C04-008 | Serialização | GET /books/{id} | Médio | SHOULD_UPDATE |
| C04-009 | Serialização | GET /reviews/{id} | Médio | SHOULD_UPDATE |
| C04-010 | Serialização | GET /authors/{id} | Médio | SHOULD_UPDATE |
| C05-001 | HTTP | POST /authors | Fácil | SHOULD_UPDATE |
| C05-002 | HTTP | POST /books | Fácil | SHOULD_UPDATE |
| C05-003 | HTTP | DELETE /authors/{id} | Fácil | SHOULD_UPDATE |
| C05-004 | HTTP | GET /authors/99999 | Fácil | SHOULD_UPDATE |
| C05-005 | HTTP | GET /books/by-author/{authorId} | Médio | SHOULD_UPDATE |
| C05-006 | HTTP | POST /reviews | Médio | SHOULD_UPDATE |
| C05-007 | HTTP | GET /reviews/{id} | Médio | SHOULD_UPDATE |
| C05-008 | HTTP | PUT /books/{id} | Médio | SHOULD_UPDATE |
| C05-009 | HTTP | DELETE /reviews/{id} | Fácil | SHOULD_UPDATE |
| C05-010 | HTTP | POST /books | Médio | SHOULD_UPDATE |
| C06-001 | Tratamento de erros | GET /authors/99999 | Fácil | SHOULD_UPDATE |
| C06-002 | Tratamento de erros | POST /books | Fácil | SHOULD_UPDATE |
| C06-003 | Tratamento de erros | POST /reviews | Fácil | SHOULD_UPDATE |
| C06-004 | Tratamento de erros | GET /books/{id} | Fácil | SHOULD_UPDATE |
| C06-005 | Tratamento de erros | GET /authors/{id} | Fácil | SHOULD_UPDATE |
| C06-006 | Tratamento de erros | POST /authors | Médio | SHOULD_UPDATE |
| C06-007 | Tratamento de erros | POST /books | Médio | SHOULD_UPDATE |
| C06-008 | Tratamento de erros | GET /reviews/99999 | Médio | SHOULD_UPDATE |
| C06-009 | Tratamento de erros | POST /reviews | Médio | SHOULD_UPDATE |
| C06-010 | Tratamento de erros | GET /authors/{id} | Fácil | SHOULD_UPDATE |
| C07-001 | Coleções | GET /authors | Fácil | SHOULD_UPDATE |
| C07-002 | Coleções | GET /books/by-author/{authorId} | Fácil | SHOULD_UPDATE |
| C07-003 | Coleções | GET /reviews/by-book/{bookId} | Fácil | SHOULD_UPDATE |
| C07-004 | Coleções | GET /books | Médio | SHOULD_UPDATE |
| C07-005 | Coleções | GET /authors | Médio | SHOULD_UPDATE |
| C07-006 | Coleções | GET /reviews | Médio | SHOULD_UPDATE |
| C07-007 | Coleções | GET /books/by-author/{authorId} | Difícil | SHOULD_UPDATE |
| C07-008 | Coleções | GET /reviews/by-book/{bookId} | Médio | SHOULD_UPDATE |
| C07-009 | Coleções | GET /books | Médio | SHOULD_UPDATE |
| C07-010 | Coleções | GET /authors | Médio | SHOULD_UPDATE |
| C08-001 | Campos não determinísticos | GET /authors/99999 | Fácil | SHOULD_NOT_UPDATE |
| C08-002 | Campos não determinísticos | POST /authors | Fácil | SHOULD_NOT_UPDATE |
| C08-003 | Campos não determinísticos | POST /books | Fácil | SHOULD_NOT_UPDATE |
| C08-004 | Campos não determinísticos | GET /authors | Médio | SHOULD_NOT_UPDATE |
| C08-005 | Campos não determinísticos | GET /reviews | Médio | SHOULD_NOT_UPDATE |
| C09-001 | Ruído | GET /authors | Fácil | SHOULD_NOT_UPDATE |
| C09-002 | Ruído | GET /books | Fácil | SHOULD_NOT_UPDATE |
| C09-003 | Ruído | GET /reviews | Fácil | SHOULD_NOT_UPDATE |
| C09-004 | Ruído | GET /books/{id} | Fácil | SHOULD_NOT_UPDATE |
| C09-005 | Ruído | GET /authors/{id} | Fácil | SHOULD_NOT_UPDATE |
| C10-001 | Bugs reais | POST /authors | Fácil | SHOULD_UPDATE |
| C10-002 | Bugs reais | POST /books | Fácil | SHOULD_UPDATE |
| C10-003 | Bugs reais | POST /reviews | Fácil | SHOULD_UPDATE |
| C10-004 | Bugs reais | GET /authors/{id} | Fácil | SHOULD_UPDATE |
| C10-005 | Bugs reais | GET /books/by-author/{authorId} | Médio | SHOULD_UPDATE |
| C10-006 | Bugs reais | GET /reviews/by-book/{bookId} | Médio | SHOULD_UPDATE |
| C10-007 | Bugs reais | POST /authors | Médio | SHOULD_UPDATE |
| C10-008 | Bugs reais | POST /books | Médio | SHOULD_UPDATE |
| C10-009 | Bugs reais | GET /books/{id} | Médio | SHOULD_UPDATE |
| C10-010 | Bugs reais | GET /reviews/{id} | Médio | SHOULD_UPDATE |
| C10-011 | Bugs reais | POST /books | Difícil | SHOULD_UPDATE |
| C10-012 | Bugs reais | GET /books/{id} | Médio | SHOULD_UPDATE |
| C10-013 | Bugs reais | GET /reviews/{id} | Médio | SHOULD_UPDATE |
| C10-014 | Bugs reais | GET /authors | Médio | SHOULD_UPDATE |
| C10-015 | Bugs reais | POST /reviews | Médio | SHOULD_UPDATE |

---

## 4. Observações metodológicas
- O dataset foi construído exclusivamente com elementos reais do projeto analisado.
- Os casos foram concebidos para refletir decisões plausíveis de desenvolvimento em APIs REST com snapshot testing.
- A classificação humana foi definida de forma conservadora, priorizando alterações que alteram o contrato observado ou a semântica do comportamento da API.
- O conjunto mistura exemplos fáceis, intermediários e difíceis, para servir como benchmark de LLM.
