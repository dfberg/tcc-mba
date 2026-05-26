# POC API - Java REST API com Arquitetura em Camadas

Proof of Concept (POC) de uma API REST em Java com **Spring Boot 3.x**, arquitetura em **3 camadas**, dados em **memória**, e testes com **snapshots** usando ApprovalTests.

## 📋 Stack Tecnológico

| Componente | Framework | Versão |
|-----------|-----------|--------|
| Framework | Spring Boot | 3.4.1 LTS |
| Java | JDK | 21 LTS |
| Build Tool | Maven | 3.9.x |
| Testing | JUnit 5, Mockito | 5.11.x, 5.x |
| Snapshots | ApprovalTests | 24.1.0 |
| Assertions | AssertJ | 3.26.0 |
| ORM | Spring Data JPA | 2.x |

## 🏗️ Arquitetura

Projeto estruturado em **3 camadas** com **5 camadas complementares**:

```
┌────────────────────────────────────┐
│  Controller (REST Endpoints)       │  HTTP requests/responses
├────────────────────────────────────┤
│  Service (Business Logic)          │  Validações, orquestração
├────────────────────────────────────┤
│  Repository (Data Access)          │  In-memory storage (ConcurrentHashMap)
├────────────────────────────────────┤
│  Model/Entity & DTO                │  Data Transfer Objects
├────────────────────────────────────┤
│  Exception Handling                │  @ControllerAdvice global
└────────────────────────────────────┘
```

### Entidades (3+)

- **Author** (1 → N) **Book** (1 → N) **Review**
  - Author: id, name, email
  - Book: id, title, isbn, author_id
  - Review: id, rating (1-5), content, book_id

## 📁 Estrutura do Projeto

```
poc-api/
├── pom.xml
├── README.md
├── src/
│   ├── main/
│   │   ├── java/com/example/pocapi/
│   │   │   ├── PocApiApplication.java
│   │   │   ├── controller/
│   │   │   │   ├── AuthorController.java
│   │   │   │   ├── BookController.java
│   │   │   │   └── ReviewController.java
│   │   │   ├── service/
│   │   │   │   ├── AuthorService.java
│   │   │   │   ├── BookService.java
│   │   │   │   └── ReviewService.java
│   │   │   ├── repository/
│   │   │   │   ├── AuthorRepository.java
│   │   │   │   ├── BookRepository.java
│   │   │   │   └── ReviewRepository.java
│   │   │   ├── model/
│   │   │   │   ├── entity/
│   │   │   │   │   ├── Author.java
│   │   │   │   │   ├── Book.java
│   │   │   │   │   └── Review.java
│   │   │   │   └── dto/
│   │   │   │       ├── AuthorDTO.java
│   │   │   │       ├── BookDTO.java
│   │   │   │       └── ReviewDTO.java
│   │   │   ├── exception/
│   │   │   │   ├── ResourceNotFoundException.java
│   │   │   │   ├── ValidationException.java
│   │   │   │   ├── ErrorResponse.java
│   │   │   │   └── GlobalExceptionHandler.java
│   │   │   └── config/
│   │   └── resources/
│   │       ├── application.properties
│   │       └── application-test.properties
│   └── test/
│       ├── java/com/example/pocapi/
│       │   ├── service/
│       │   │   ├── AuthorServiceTest.java
│       │   │   ├── BookServiceTest.java
│       │   │   └── ReviewServiceTest.java
│       │   └── integration/
│       │       ├── AuthorApiIntegrationTest.java
│       │       └── BookApiIntegrationTest.java
│       └── resources/
│           └── approvals/
```

## 🚀 Como Executar

### Pré-requisitos

- JDK 21+
- Maven 3.9.x+

### 1. Compilar o Projeto

```bash
cd poc-api
mvn clean install
```

### 2. Executar a Aplicação

```bash
mvn spring-boot:run
```

A aplicação estará disponível em: `http://localhost:8080/api`

### 3. Dados Iniciais

A aplicação carrega automaticamente dados de exemplo via `@PostConstruct` no `AuthorService`:
- 2 autores: J.K. Rowling, George R.R. Martin

## 📡 Endpoints da API

### Authors

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/authors` | Listar todos os autores |
| GET | `/api/authors/{id}` | Buscar autor por ID |
| POST | `/api/authors` | Criar novo autor |
| PUT | `/api/authors/{id}` | Atualizar autor |
| DELETE | `/api/authors/{id}` | Deletar autor |

**Exemplo (POST):**
```bash
curl -X POST http://localhost:8080/api/authors \
  -H "Content-Type: application/json" \
  -d '{"name":"Arthur Conan Doyle","email":"doyle@example.com"}'
```

### Books

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/books` | Listar todos os livros |
| GET | `/api/books/{id}` | Buscar livro por ID |
| GET | `/api/books/by-author/{authorId}` | Listar livros de um autor |
| POST | `/api/books` | Criar novo livro |
| PUT | `/api/books/{id}` | Atualizar livro |
| DELETE | `/api/books/{id}` | Deletar livro |

**Exemplo (POST):**
```bash
curl -X POST http://localhost:8080/api/books \
  -H "Content-Type: application/json" \
  -d '{"title":"Harry Potter","isbn":"123456789","authorId":1}'
```

### Reviews

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/reviews` | Listar todos os reviews |
| GET | `/api/reviews/{id}` | Buscar review por ID |
| GET | `/api/reviews/by-book/{bookId}` | Listar reviews de um livro |
| POST | `/api/reviews` | Criar novo review |
| PUT | `/api/reviews/{id}` | Atualizar review |
| DELETE | `/api/reviews/{id}` | Deletar review |

**Exemplo (POST):**
```bash
curl -X POST http://localhost:8080/api/reviews \
  -H "Content-Type: application/json" \
  -d '{"rating":5,"content":"Excelente livro!","bookId":1}'
```

## 🧪 Testes

### Executar Todos os Testes

```bash
mvn test
```

### Executar Testes Específicos

```bash
# Unit tests (Service tests)
mvn test -Dtest=*ServiceTest

# Integration tests (Snapshot tests)
mvn test -Dtest=*IntegrationTest
```

### Testes com Snapshots (ApprovalTests)

Os testes de snapshot comparetem respostas JSON contra arquivos `.approved.txt` na primeira execução:

1. **Primeira execução**: Cria arquivos `.received.txt` e `.approved.txt`
2. **Revisar**: Abra os arquivos `.received.txt` no `target/` e valide os dados
3. **Aprovar**: Rename ou copie `.received.txt` → `.approved.txt` (ou use a IDE)
4. **Próximas execuções**: Compara automaticamente contra `.approved.txt`

**Localização dos aproveals:**
```
target/
  com.example.pocapi.integration/
    AuthorApiIntegrationTest/
      ├── testGetAllAuthors_Snapshot.approved.txt
      ├── testCreateAuthor_Snapshot.approved.txt
      └── ...
```

### Cobertura de Testes

Gerar relatório de cobertura:

```bash
mvn clean test jacoco:report
```

Relatorio disponível em: `target/site/jacoco/index.html`

**Objetivo de cobertura:**
- Unit tests: 60%
- Integration tests: 30%
- Snapshot tests: 10%

## 🛠️ Validações de Negócio

### Author
- ✅ Nome não pode ser vazio
- ✅ Email não pode ser vazio e deve ser válido (conter @)
- ✅ Email deve ser único

### Book
- ✅ Título não pode ser vazio
- ✅ ISBN não pode ser vazio
- ✅ ISBN deve ser único
- ✅ Deve estar associado a um author válido

### Review
- ✅ Rating deve estar entre 1 e 5
- ✅ Deve estar associado a um book válido

## 📝 Tratamento de Erros

Todos os erros retornam uma resposta padronizada via `@ControllerAdvice`:

```json
{
  "status": "404",
  "message": "Author not found with id: 99",
  "timestamp": "2026-04-07T10:30:00",
  "path": "/api/authors/99"
}
```

### Exceções Tratadas

- `ResourceNotFoundException` (404)
- `ValidationException` (400)
- `IllegalArgumentException` (400)
- `Exception` genérica (500)

## 🔄 Inicialização de Dados

Os dados são inicializados automaticamente no startup via `@PostConstruct`:

```java
@PostConstruct
public void initData() {
    // Cria 2 autores de exemplo
}
```

**Nota:** Como os dados são em memória, eles se perdem ao reiniciar a aplicação. A cada reinicialização, os dados são recriados.

## 📦 Dependências Principais

- Spring Boot Starter Web (REST API)
- Spring Boot Starter Data JPA (ORM)
- Spring Boot Starter Validation (validações)
- JUnit 5 (testes)
- Mockito (mocking)
- AssertJ (assertions fluentes)
- ApprovalTests (snapshot testing)
- Lombok (reduz boilerplate)
- H2 Database (para testes)

## 🎯 Decisões Arquiteturais

✅ **Incluído:**
- 3 camadas bem definidas (Controller → Service → Repository)
- Dados em memória (ConcurrentHashMap)
- DTOs para separação de concerns
- Exceções customizadas
- Validações nas 3 camadas
- Testes unitários com Mockito
- Testes de integração com snapshots
- Tratamento centralizado de erros

❌ **Excluído (escopo POC):**
- Autenticação/Autorização (JWT, OAuth)
- Documentação OpenAPI/Swagger
- Logging estruturado
- Cache distribuído
- CI/CD pipeline
- Docker/containerização
- Monitoramento e observabilidade

## 🚀 Próximos Passos (Evolução)

1. **Persistência:** Trocar in-memory por PostgreSQL + Spring Data JPA
2. **Autenticação:** Adicionar Spring Security + JWT
3. **API Docs:** Integrar Springdoc OpenAPI para Swagger automático
4. **Observabilidade:** Spring Boot Actuator + logs estruturados
5. **Cache:** Redis para caching de queries frequentes
6. **CI/CD:** GitHub Actions / GitLab CI

## 📄 Licença

Projeto de demonstração educacional.

---

**Autor:** POC Team  
**Data:** Abril 2026  
**Status:** ✅ Completo
