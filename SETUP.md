# 🚀 Guia de Setup - POC API

Este guia descreve como configurar o ambiente e executar a POC API.

## 📋 Pré-requisitos

### 1. Java Development Kit (JDK) 21+

**Windows:**
1. Download JDK 21+ de: https://www.oracle.com/java/technologies/downloads/
2. Instale o JDK (exemplo: `C:\Program Files\Java\jdk-21`)
3. Configure a variável de ambiente `JAVA_HOME`:
   - Clique em "Editar as variáveis de ambiente do sistema"
   - Crie nova variável: `JAVA_HOME` = `C:\Program Files\Java\jdk-21`
   - Edite `PATH` e adicione: `%JAVA_HOME%\bin`
4. Verifique:
   ```bash
   java -version
   javac -version
   ```

**Linux/Mac:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install openjdk-21-jdk

# macOS (Homebrew)
brew install openjdk@21

# Verificar
java -version
```

### 2. Apache Maven 3.9.x+

**Windows:**
1. Download Maven de: https://maven.apache.org/download.cgi
2. Extraia para um diretório (exemplo: `C:\Apache\maven-3.9.6`)
3. Configure variável de ambiente `MAVEN_HOME`:
   - Crie variável: `MAVEN_HOME` = `C:\Apache\maven-3.9.6`
   - Edite `PATH` e adicione: `%MAVEN_HOME%\bin`
4. Verifique:
   ```bash
   mvn --version
   ```

**Linux/Mac:**
```bash
# Homebrew
brew install maven

# Ou download manualmente
wget https://archive.apache.org/dist/maven/maven-3/3.9.6/binaries/apache-maven-3.9.6-bin.tar.gz
tar -xzf apache-maven-3.9.6-bin.tar.gz
sudo mv apache-maven-3.9.6 /opt/maven

# Adicione ao PATH (~/.bashrc ou ~/.zshrc):
export PATH=$PATH:/opt/maven/bin

# Verifique
mvn --version
```

**Alternativa: Docker**
Se preferir não instalar localmente, use Docker:
```bash
docker run -it --rm -v $(pwd):/app -w /app maven:3.9-eclipse-temurin-21 mvn clean install
```

---

## 🏃 Como Executar

### 1. Compilar o Projeto

```bash
cd poc-api
mvn clean install
```

### 2. Executar a Aplicação

```bash
mvn spring-boot:run
```

Ou se já compilou:
```bash
java -jar target/poc-api-0.0.1-SNAPSHOT.jar
```

A aplicação estará em: **http://localhost:8080/api**

### 3. Testar a API

Abra outro terminal e teste um endpoint:

```bash
# Listar autores
curl http://localhost:8080/api/authors

# Criar autor
curl -X POST http://localhost:8080/api/authors \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane Austen","email":"jane@example.com"}'

# Listar livros
curl http://localhost:8080/api/books

# Listar reviews
curl http://localhost:8080/api/reviews
```

---

## 🧪 Como Executar Testes

### Todos os testes

```bash
mvn test
```

### Apenas testes unitários (Services)

```bash
mvn test -Dtest=*ServiceTest
```

### Apenas testes de integração (Snapshots)

```bash
mvn test -Dtest=*IntegrationTest
```

### Testes com saída detalhada

```bash
mvn test -e
```

### Cobertura de testes

```bash
mvn clean test jacoco:report
# Relatório em: target/site/jacoco/index.html
```

---

## 📁 Estrutura de Diretórios

```
poc-api/
├── pom.xml                          # Configuração Maven e dependências
├── setup.bat / setup.sh            # Scripts de setup
├── README.md                        # Documentação da API
├── SETUP.md                         # Este arquivo
│
├── .mvn/
│   └── wrapper/                     # Maven Wrapper config
│
├── src/
│   ├── main/
│   │   ├── java/com/example/pocapi/
│   │   │   ├── controller/          # REST Controllers
│   │   │   ├── service/             # Business logic
│   │   │   ├── repository/          # Data access (in-memory)
│   │   │   ├── model/
│   │   │   │   ├── entity/          # JPA Entities
│   │   │   │   └── dto/             # Data Transfer Objects
│   │   │   ├── exception/           # Exception handling
│   │   │   └── PocApiApplication.java
│   │   └── resources/
│   │       ├── application.properties
│   │       └── application-test.properties
│   │
│   └── test/
│       ├── java/com/example/pocapi/
│       │   ├── service/             # Unit tests (Mockito)
│       │   └── integration/         # Integration tests (Snapshots)
│       └── resources/
│           └── approvals/           # Snapshot files
```

---

## 🛠️ Troubleshooting

### "mvn: command not found"
- **Causa:** Maven não está no PATH
- **Solução:** Instale Maven e adicione ao PATH conforme instruções acima

### "JAVA_HOME is not set"
- **Causa:** Variável JAVA_HOME não configurada
- **Solução:** Configure `JAVA_HOME` apontando para seu JDK

### "OutOfMemoryError" durante build
- **Solução:** Aumentar heap memory
```bash
export MAVEN_OPTS="-Xmx1024m -XX:MaxPermSize=512m"
mvn clean install
```

### Erro ao compilar: "Symbol not found"
- **Causa:** Possível problema com cache Maven
- **Solução:** Limpar cache
```bash
rm -rf ~/.m2/repository
mvn clean install
```

### Porta 8080 já em uso
- **Solução:** Alterar porta em `application.properties`
```properties
server.port=8081
```

---

## 🐳 Executar com Docker (Opcional)

### Criar imagem Docker

```bash
docker build -t poc-api:latest .
docker run -p 8080:8080 poc-api:latest
```

### Ou usar a imagem Maven do Docker

```bash
docker run -it --rm -v $(pwd):/app -w /app \
  maven:3.9-eclipse-temurin-21 \
  mvn spring-boot:run
```

---

## 📚 Recursos Úteis

- **Java 21 Documentation:** https://docs.oracle.com/en/java/javase/21/
- **Spring Boot 3.4:** https://spring.io/projects/spring-boot
- **Maven Guide:** https://maven.apache.org/guides/
- **JUnit 5:** https://junit.org/junit5/docs/current/user-guide/
- **ApprovalTests:** https://approvaltests.com/

---

## ✅ Checklist de Setup

- [ ] JDK 21+ instalado (`java -version`)
- [ ] Maven 3.9+ instalado (`mvn --version`)
- [ ] Clonar/baixar projeto
- [ ] `cd poc-api`
- [ ] `mvn clean install`
- [ ] `mvn spring-boot:run`
- [ ] Acessar http://localhost:8080/api/authors
- [ ] `mvn test` (executar testes)

---

**Pronto!** 🎉 Agora você pode:
- ✅ Executar a aplicação
- ✅ Testar os endpoints via curl/Postman
- ✅ Executar testes unitários e de integração
- ✅ Explorar o código-fonte

**Próximas etapas sugeridas:**
1. Revisar arquitetura em 3 camadas
2. Adicionar mais testes
3. Evoluir para usar banco de dados (PostgreSQL)
4. Adicionar autenticação JWT
5. Integrar com Swagger/OpenAPI
