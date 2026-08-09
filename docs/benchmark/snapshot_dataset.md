# Catálogo planejado de candidatos do Benchmark V2

Este catálogo contém candidatos conceituais ainda não implementados. Cada candidato parte independentemente do baseline `8316d9ffa0c109c0aac68fd181b94fdd9dce368e` (`benchmark-v2-baseline`). Os IDs `CASE-*` identificam propostas; `EXP-*` permanece reservado a execuções futuras.

As fontes de verdade são o código do baseline, os seis testes que chamam `Approvals.verify(responseBody)`, seus arquivos aprovados e `baseline/system_inventory.md`. Nenhum candidato foi copiado automaticamente do dataset exploratório.

## Casos planejados

## CASE-001

**Categoria:** CONTRACT_EVOLUTION
**Snapshot alvo:** `AuthorApiIntegrationTest.testGetAllAuthors_Snapshot.approved.txt`
**Teste alvo:** `AuthorApiIntegrationTest.testGetAllAuthors_Snapshot`
**Endpoint:** `/authors`
**HTTP:** GET
**Mutation Point:** MP-005, MP-007
**Arquivo/região candidata:** `AuthorController.java`, `getAllAuthors`

**Objetivo:** Evoluir deliberadamente a representação da coleção vazia.

**Alteração planejada:** Substituir o array raiz por um objeto de coleção contendo `authors: []` e `count: 0`.

**Intenção:** Adotar um envelope paginável e extensível como novo contrato aprovado.

**Observabilidade no snapshot:** O cenário executa a resposta vazia; o texto passa de `[]` para um objeto JSON mesmo sem elementos.

**Ground Truth:** SHOULD_UPDATE
**Justificativa do Ground Truth:** A quebra de representação é deliberada e constitui o novo contrato esperado.
**Dificuldade:** MEDIUM
**Alcance esperado:** TARGET_ONLY
**Status:** PLANNED
**Riscos de execução:** A alteração pode não alcançar o body se ficar apenas em tipos genéricos ou documentação.

## CASE-002

**Categoria:** BUG
**Snapshot alvo:** `AuthorApiIntegrationTest.testGetAllAuthors_Snapshot.approved.txt`
**Teste alvo:** `AuthorApiIntegrationTest.testGetAllAuthors_Snapshot`
**Endpoint:** `/authors`
**HTTP:** GET
**Mutation Point:** MP-005, MP-007
**Arquivo/região candidata:** `AuthorController.java`, `getAllAuthors`

**Objetivo:** Representar uma regressão que devolve nulo no lugar de coleção vazia.

**Alteração planejada:** Fazer o controller devolver explicitamente um valor JSON nulo serializável quando não existirem autores, sem depender de `ResponseEntity.ok(null)` ou de referência Java nula.

**Intenção:** Simular um tratamento acidentalmente incorreto de ausência de resultados.

**Observabilidade no snapshot:** O teste parte de repositório vazio e compara literalmente `[]`; `null` altera diretamente o body verificado.

**Ground Truth:** SHOULD_NOT_UPDATE
**Justificativa do Ground Truth:** Atualizar o snapshot legitimaria a perda da semântica de coleção.
**Dificuldade:** EASY
**Alcance esperado:** TARGET_ONLY
**Status:** PLANNED
**Riscos de execução:** A implementação futura deve usar representação JSON nula explícita e confirmar que o body textual é `null`, não string vazia nem string `"null"`.

## CASE-003

**Categoria:** NOISE
**Snapshot alvo:** `AuthorApiIntegrationTest.testGetAllAuthors_Snapshot.approved.txt`
**Teste alvo:** `AuthorApiIntegrationTest.testGetAllAuthors_Snapshot`
**Endpoint:** `/authors`
**HTTP:** GET
**Mutation Point:** MP-021
**Arquivo/região candidata:** `src/main/resources/application.properties`, configuração de serialização Jackson

**Objetivo:** Detectar ruído de formatação JSON sem mudança semântica da coleção.

**Alteração planejada:** Habilitar globalmente uma serialização indentada que altere de modo determinístico a representação textual da coleção vazia, preservando seu valor semântico.

**Intenção:** Simular uma mudança de configuração de serialização introduzida durante manutenção, cujo whitespace não deveria exigir nova aprovação sem uma decisão contratual.

**Observabilidade no snapshot:** ApprovalTests compara o texto bruto; a forma compacta `[]` receberá whitespace determinístico mesmo continuando uma coleção vazia.

**Ground Truth:** SHOULD_NOT_UPDATE
**Justificativa do Ground Truth:** Atualizar o snapshot aceitaria ruído de apresentação que deveria ser estabilizado ou normalizado, sem evolução semântica do body.
**Dificuldade:** HARD
**Alcance esperado:** GLOBAL_BEHAVIOR
**Status:** PLANNED
**Riscos de execução:** A opção futura deve ser validada contra a versão real do Jackson para confirmar que o array vazio muda textualmente; a configuração também afetará os outros cinco snapshots.

## CASE-004

**Categoria:** CONTRACT_EVOLUTION
**Snapshot alvo:** `AuthorApiIntegrationTest.testCreateAuthor_Snapshot.approved.txt`
**Teste alvo:** `AuthorApiIntegrationTest.testCreateAuthor_Snapshot`
**Endpoint:** `/authors`
**HTTP:** POST
**Mutation Point:** MP-001, MP-002
**Arquivo/região candidata:** `AuthorDTO.java`, propriedades; `AuthorService.java`, `convertToDTO`

**Objetivo:** Acrescentar uma representação derivada do nome completo.

**Alteração planejada:** Adicionar e preencher `displayName` com `firstName + " " + lastName` na resposta criada.

**Intenção:** Evolução deliberada do contrato para oferecer um valor pronto para exibição.

**Observabilidade no snapshot:** Isaac Asimov está presente e o mapeamento executado produzirá um novo campo não nulo no objeto JSON.

**Ground Truth:** SHOULD_UPDATE
**Justificativa do Ground Truth:** O campo novo é uma extensão intencional e correta do contrato.
**Dificuldade:** MEDIUM
**Alcance esperado:** MULTIPLE_SNAPSHOTS
**Status:** PLANNED
**Riscos de execução:** Declarar o campo sem preenchê-lo o manteria omitido por `NON_NULL`.

## CASE-005

**Categoria:** BREAKING_CHANGE
**Snapshot alvo:** `AuthorApiIntegrationTest.testCreateAuthor_Snapshot.approved.txt`
**Teste alvo:** `AuthorApiIntegrationTest.testCreateAuthor_Snapshot`
**Endpoint:** `/authors`
**HTTP:** POST
**Mutation Point:** MP-001, MP-021
**Arquivo/região candidata:** `AuthorDTO.java`, propriedade/serialização de `firstName`

**Objetivo:** Renomear deliberadamente `firstName` para `givenName` no JSON.

**Alteração planejada:** Adotar `givenName` como nome público aprovado da propriedade, preservando o valor `Isaac`.

**Intenção:** Alinhar o contrato a uma convenção terminológica decidida pela equipe.

**Observabilidade no snapshot:** A chave textual `firstName` existe no body aprovado e será substituída por `givenName`.

**Ground Truth:** SHOULD_UPDATE
**Justificativa do Ground Truth:** Embora incompatível, a mudança é explicitamente aprovada como novo contrato.
**Dificuldade:** EASY
**Alcance esperado:** MULTIPLE_SNAPSHOTS
**Status:** PLANNED
**Riscos de execução:** Alterar apenas a desserialização de entrada pode não mudar a serialização da resposta.

## CASE-006

**Categoria:** BUG
**Snapshot alvo:** `AuthorApiIntegrationTest.testCreateAuthor_Snapshot.approved.txt`
**Teste alvo:** `AuthorApiIntegrationTest.testCreateAuthor_Snapshot`
**Endpoint:** `/authors`
**HTTP:** POST
**Mutation Point:** MP-002
**Arquivo/região candidata:** `AuthorService.java`, `convertToDTO`

**Objetivo:** Capturar troca acidental entre nome e sobrenome.

**Alteração planejada:** Mapear `firstName` a partir de `lastName` e `lastName` a partir de `firstName`.

**Intenção:** Simular erro comum de wiring entre propriedades do mesmo tipo.

**Observabilidade no snapshot:** O body passará de `Isaac`/`Asimov` para `Asimov`/`Isaac` nas chaves existentes.

**Ground Truth:** SHOULD_NOT_UPDATE
**Justificativa do Ground Truth:** Atualizar o snapshot aceitaria valores semanticamente trocados.
**Dificuldade:** EASY
**Alcance esperado:** MULTIPLE_SNAPSHOTS
**Status:** PLANNED
**Riscos de execução:** Nenhum relevante enquanto os valores de entrada continuarem distintos.

## CASE-007

**Categoria:** SERIALIZATION
**Snapshot alvo:** `AuthorApiIntegrationTest.testCreateAuthor_Snapshot.approved.txt`
**Teste alvo:** `AuthorApiIntegrationTest.testCreateAuthor_Snapshot`
**Endpoint:** `/authors`
**HTTP:** POST
**Mutation Point:** MP-002, MP-021
**Arquivo/região candidata:** `AuthorService.java`, `convertToDTO`; `AuthorDTO.java`, inclusão de propriedades

**Objetivo:** Modelar perda acidental do email na resposta.

**Alteração planejada:** Deixar `email` nulo no DTO de saída, fazendo `NON_NULL` omitir a chave.

**Intenção:** Simular regressão de mapeamento combinada com a política de serialização existente.

**Observabilidade no snapshot:** `email:"isaac@example.com"` existe no aprovado e desaparecerá do body.

**Ground Truth:** SHOULD_NOT_UPDATE
**Justificativa do Ground Truth:** A ausência não foi aprovada e representa perda de informação.
**Dificuldade:** EASY
**Alcance esperado:** MULTIPLE_SNAPSHOTS
**Status:** PLANNED
**Riscos de execução:** Preencher o email em outro ponto do fluxo impediria a omissão.

## CASE-008

**Categoria:** BREAKING_CHANGE
**Snapshot alvo:** `AuthorApiIntegrationTest.testCreateAuthor_Snapshot.approved.txt`
**Teste alvo:** `AuthorApiIntegrationTest.testCreateAuthor_Snapshot`
**Endpoint:** `/authors`
**HTTP:** POST
**Mutation Point:** MP-001, MP-002
**Arquivo/região candidata:** `AuthorDTO.java`; `AuthorService.java`, `convertToDTO`

**Objetivo:** Remover deliberadamente o email das respostas públicas de criação.

**Alteração planejada:** Omitir `email` no mapper compartilhado usando a mesma forma mínima de diff prevista em CASE-007, agora como decisão explícita de minimização de dados.

**Intenção:** Aplicar uma política de privacidade aprovada, mesmo com quebra do contrato anterior.

**Observabilidade no snapshot:** A chave e o valor de email presentes no objeto aprovado deixam de ser serializados.

**Ground Truth:** SHOULD_UPDATE
**Justificativa do Ground Truth:** A perda do campo é intencional e constitui o comportamento correto definido para o caso.
**Dificuldade:** HARD
**Alcance esperado:** MULTIPLE_SNAPSHOTS
**Status:** PLANNED
**Riscos de execução:** A omissão também afetará o GET por ID; o efeito múltiplo é aceito e deverá ser coletado sem ampliar artificialmente o patch.

## CASE-009

**Categoria:** CONTRACT_EVOLUTION
**Snapshot alvo:** `AuthorApiIntegrationTest.testGetAuthorById_Snapshot.approved.txt`
**Teste alvo:** `AuthorApiIntegrationTest.testGetAuthorById_Snapshot`
**Endpoint:** `/authors/{id}`
**HTTP:** GET
**Mutation Point:** MP-001, MP-002, MP-007
**Arquivo/região candidata:** `AuthorDTO.java`; `AuthorController.java`, `getAuthorById`

**Objetivo:** Substituir nomes separados por `fullName` na consulta por ID.

**Alteração planejada:** Preencher `fullName:"J.R.R. Tolkien"` e omitir `firstName`/`lastName` somente na resposta do GET por ID; o novo campo permanecerá nulo e omitido nos demais fluxos.

**Intenção:** Adotar uma representação canônica simplificada para leitura individual.

**Observabilidade no snapshot:** Duas chaves existentes serão removidas e uma nova chave não nula aparecerá no body do GET.

**Ground Truth:** SHOULD_UPDATE
**Justificativa do Ground Truth:** A transformação é uma evolução intencional do contrato de leitura.
**Dificuldade:** MEDIUM
**Alcance esperado:** TARGET_ONLY
**Status:** PLANNED
**Riscos de execução:** A localização exige que o controller transforme o DTO após o serviço; preencher o campo no mapper compartilhado afetaria criação e violaria o alcance definido.

## CASE-010

**Categoria:** BUG
**Snapshot alvo:** `AuthorApiIntegrationTest.testGetAuthorById_Snapshot.approved.txt`
**Teste alvo:** `AuthorApiIntegrationTest.testGetAuthorById_Snapshot`
**Endpoint:** `/authors/{id}`
**HTTP:** GET
**Mutation Point:** MP-002, MP-004
**Arquivo/região candidata:** `AuthorService.java`, `getAuthorById`, após `convertToDTO`

**Objetivo:** Detectar identificador incorreto na resposta de consulta.

**Alteração planejada:** Aplicar no DTO do GET uma transformação off-by-one sobre o identificador real recuperado, produzindo de forma determinística um ID incorreto e diferente.

**Intenção:** Simular erro de mapeamento ou transformação de identidade.

**Observabilidade no snapshot:** O aprovado contém `id:4`; o valor numérico enviado ao ApprovalTests será diferente.

**Ground Truth:** SHOULD_NOT_UPDATE
**Justificativa do Ground Truth:** O body deixaria de identificar corretamente o recurso solicitado.
**Dificuldade:** EASY
**Alcance esperado:** TARGET_ONLY
**Status:** PLANNED
**Riscos de execução:** A transformação deve ocorrer depois da busca e manter o GET bem-sucedido; não deve ser movida para o mapper compartilhado.

## CASE-011

**Categoria:** BUSINESS_RULE
**Snapshot alvo:** `AuthorApiIntegrationTest.testGetAuthorById_Snapshot.approved.txt`
**Teste alvo:** `AuthorApiIntegrationTest.testGetAuthorById_Snapshot`
**Endpoint:** `/authors/{id}`
**HTTP:** GET
**Mutation Point:** MP-002, MP-007
**Arquivo/região candidata:** `AuthorController.java`, `getAuthorById`, após retorno do serviço

**Objetivo:** Aplicar mascaramento deliberado do email em consultas públicas.

**Alteração planejada:** Aplicar uma forma mascarada observável ao email somente no DTO devolvido por `AuthorController.getAuthorById`.

**Intenção:** Implementar regra aprovada de proteção de dado pessoal sem remover a propriedade.

**Observabilidade no snapshot:** O valor literal completo do email está no aprovado e será substituído pelo valor mascarado.

**Ground Truth:** SHOULD_UPDATE
**Justificativa do Ground Truth:** A mudança de valor é consequência correta da nova política de exposição.
**Dificuldade:** HARD
**Alcance esperado:** TARGET_ONLY
**Status:** PLANNED
**Riscos de execução:** Uma máscara que gere o mesmo texto não produzirá diff; a regra não deve ser movida para o mapper compartilhado.

## CASE-012

**Categoria:** SERIALIZATION
**Snapshot alvo:** `AuthorApiIntegrationTest.testGetAuthorById_Snapshot.approved.txt`
**Teste alvo:** `AuthorApiIntegrationTest.testGetAuthorById_Snapshot`
**Endpoint:** `/authors/{id}`
**HTTP:** GET
**Mutation Point:** MP-001, MP-002, MP-021
**Arquivo/região candidata:** `AuthorService.java`, `getAuthorById`, após `convertToDTO`; campo `books` existente em `AuthorDTO.java`

**Objetivo:** Detectar exposição acidental de uma coleção vazia antes omitida.

**Alteração planejada:** Preencher inadvertidamente `books` com lista vazia somente no DTO retornado por `getAuthorById`, após o mapper compartilhado.

**Intenção:** Simular inicialização automática que altera o contrato de serialização sem decisão explícita.

**Observabilidade no snapshot:** `books` hoje é nulo e omitido; ao receber lista vazia, aparece como `"books":[]` no body.

**Ground Truth:** SHOULD_NOT_UPDATE
**Justificativa do Ground Truth:** A nova propriedade exposta não foi intencionalmente aprovada.
**Dificuldade:** MEDIUM
**Alcance esperado:** TARGET_ONLY
**Status:** PLANNED
**Riscos de execução:** Se `books` permanecer nulo ou houver política `NON_EMPTY`, não haverá falha; a mutação não deve ser colocada em `convertToDTO`.

## CASE-013

**Categoria:** ERROR_HANDLING
**Snapshot alvo:** `AuthorApiIntegrationTest.testGetAuthorNotFound_Snapshot.approved.txt`
**Teste alvo:** `AuthorApiIntegrationTest.testGetAuthorNotFound_Snapshot`
**Endpoint:** `/authors/99999`
**HTTP:** GET
**Mutation Point:** MP-008, MP-009
**Arquivo/região candidata:** `ResourceNotFoundException.java`, construtor; `GlobalExceptionHandler.java`, `handleResourceNotFound`

**Objetivo:** Padronizar deliberadamente a mensagem de recurso ausente.

**Alteração planejada:** Trocar a mensagem para uma redação aprovada, por exemplo com padrão uniforme de recurso e identificador.

**Intenção:** Alinhar mensagens públicas de erro a uma convenção institucional.

**Observabilidade no snapshot:** O campo `message` contém texto literal e mudará, mantendo os demais campos.

**Ground Truth:** SHOULD_UPDATE
**Justificativa do Ground Truth:** A nova redação é uma decisão correta e intencional do contrato de erro.
**Dificuldade:** EASY
**Alcance esperado:** GLOBAL_BEHAVIOR
**Status:** PLANNED
**Riscos de execução:** Alterar uma sobrecarga de exceção que não é usada nesse fluxo não gerará diff.

## CASE-014

**Categoria:** ERROR_HANDLING
**Snapshot alvo:** `AuthorApiIntegrationTest.testGetAuthorNotFound_Snapshot.approved.txt`
**Teste alvo:** `AuthorApiIntegrationTest.testGetAuthorNotFound_Snapshot`
**Endpoint:** `/authors/99999`
**HTTP:** GET
**Mutation Point:** MP-009
**Arquivo/região candidata:** `ResourceNotFoundException.java`, construtor `(String, Long)`; chamada em `AuthorService.getAuthorById`

**Objetivo:** Detectar mensagem que identifica o tipo de recurso errado.

**Alteração planejada:** Produzir acidentalmente mensagem `Book not found...` no fluxo de autor.

**Intenção:** Simular erro de copiar/colar no argumento do recurso.

**Observabilidade no snapshot:** O campo `message` passará de `Author...` para `Book...`.

**Ground Truth:** SHOULD_NOT_UPDATE
**Justificativa do Ground Truth:** A mensagem contradiz o endpoint e ocultaria um defeito de diagnóstico.
**Dificuldade:** EASY
**Alcance esperado:** TARGET_ONLY
**Status:** PLANNED
**Riscos de execução:** O handler genérico não deve interceptar/reescrever a mensagem antes da serialização.

## CASE-015

**Categoria:** SERIALIZATION
**Snapshot alvo:** `AuthorApiIntegrationTest.testGetAuthorNotFound_Snapshot.approved.txt`
**Teste alvo:** `AuthorApiIntegrationTest.testGetAuthorNotFound_Snapshot`
**Endpoint:** `/authors/99999`
**HTTP:** GET
**Mutation Point:** MP-008, MP-010
**Arquivo/região candidata:** `GlobalExceptionHandler.java`, formatador e `handleResourceNotFound`

**Objetivo:** Adotar deliberadamente timestamp ISO instantâneo com marcador UTC.

**Alteração planejada:** Serializar o instante fixo em formato aprovado que inclua `Z`, em vez do formato local atual.

**Intenção:** Tornar explícito o timezone na representação de erro.

**Observabilidade no snapshot:** O valor textual de `timestamp` está materializado e ganhará representação diferente.

**Ground Truth:** SHOULD_UPDATE
**Justificativa do Ground Truth:** A mudança de formato é intencional e remove ambiguidade temporal.
**Dificuldade:** MEDIUM
**Alcance esperado:** GLOBAL_BEHAVIOR
**Status:** PLANNED
**Riscos de execução:** Usar `LocalDateTime` com o mesmo formatter atual pode preservar exatamente o texto.

## CASE-016

**Categoria:** NON_DETERMINISTIC
**Snapshot alvo:** `AuthorApiIntegrationTest.testGetAuthorNotFound_Snapshot.approved.txt`
**Teste alvo:** `AuthorApiIntegrationTest.testGetAuthorNotFound_Snapshot`
**Endpoint:** `/authors/99999`
**HTTP:** GET
**Mutation Point:** MP-010
**Arquivo/região candidata:** `GlobalExceptionHandler.java`, geração de timestamp; `TestTimeConfig.java`, `Clock`

**Objetivo:** Detectar introdução de horário real variável no snapshot.

**Alteração planejada:** Contornar o `Clock` fixo e usar tempo corrente do sistema no erro.

**Intenção:** Simular regressão que reintroduz valor não determinístico em testes de snapshot.

**Observabilidade no snapshot:** O timestamp aprovado é fixo; cada execução produzirá texto diferente do baseline e, em execuções suficientemente separadas, diferente das demais execuções.

**Ground Truth:** SHOULD_NOT_UPDATE
**Justificativa do Ground Truth:** Aprovar qualquer novo valor apenas esconderia variabilidade recorrente, que deve ser normalizada; o comportamento variável é reproduzível, embora o timestamp exato não seja.
**Dificuldade:** HARD
**Alcance esperado:** GLOBAL_BEHAVIOR
**Status:** PLANNED
**Protocolo especial:** repeated execution; executar ao menos duas vezes, comparando cada body com o baseline e entre execuções.
**Riscos de execução:** O valor exato não é reproduzível; resolução temporal ou execuções próximas podem coincidir, portanto o protocolo deve espaçar/coletar as repetições.

## CASE-017

**Categoria:** CONTRACT_EVOLUTION
**Snapshot alvo:** `AuthorApiIntegrationTest.testGetAuthorNotFound_Snapshot.approved.txt`
**Teste alvo:** `AuthorApiIntegrationTest.testGetAuthorNotFound_Snapshot`
**Endpoint:** `/authors/99999`
**HTTP:** GET
**Mutation Point:** MP-011, MP-021
**Arquivo/região candidata:** `ErrorResponse.java`, propriedade `status`; serialização Jackson

**Objetivo:** Renomear deliberadamente o campo textual `status` para `code`.

**Alteração planejada:** Publicar `code:"404"` como novo contrato do objeto de erro.

**Intenção:** Uniformizar a nomenclatura com outros consumidores da API.

**Observabilidade no snapshot:** A chave `status` está no JSON aprovado e será substituída por `code`.

**Ground Truth:** SHOULD_UPDATE
**Justificativa do Ground Truth:** A alteração de contrato foi deliberadamente aprovada.
**Dificuldade:** MEDIUM
**Alcance esperado:** GLOBAL_BEHAVIOR
**Status:** PLANNED
**Riscos de execução:** Alterações apenas em getters internos, sem efeito no nome Jackson, podem não mudar o body.

## CASE-018

**Categoria:** ERROR_HANDLING
**Snapshot alvo:** `AuthorApiIntegrationTest.testGetAuthorNotFound_Snapshot.approved.txt`
**Teste alvo:** `AuthorApiIntegrationTest.testGetAuthorNotFound_Snapshot`
**Endpoint:** `/authors/99999`
**HTTP:** GET
**Mutation Point:** MP-008
**Arquivo/região candidata:** `GlobalExceptionHandler.java`, `handleResourceNotFound`, derivação de `path`

**Objetivo:** Detectar path de erro incorreto.

**Alteração planejada:** Preencher acidentalmente `path` com outra rota ou valor constante.

**Intenção:** Simular regressão na extração de `WebRequest`.

**Observabilidade no snapshot:** O aprovado contém `/authors/99999`; o valor da chave `path` mudará diretamente.

**Ground Truth:** SHOULD_NOT_UPDATE
**Justificativa do Ground Truth:** O erro deixaria de apontar para a requisição que falhou.
**Dificuldade:** MEDIUM
**Alcance esperado:** GLOBAL_BEHAVIOR
**Status:** PLANNED
**Riscos de execução:** A mutação deve atuar no handler específico de `ResourceNotFoundException`.

## CASE-019

**Categoria:** CONTRACT_EVOLUTION
**Snapshot alvo:** `BookApiIntegrationTest.testCreateBook_Snapshot.approved.txt`
**Teste alvo:** `BookApiIntegrationTest.testCreateBook_Snapshot`
**Endpoint:** `/books`
**HTTP:** POST
**Mutation Point:** MP-012, MP-013, MP-014
**Arquivo/região candidata:** `BookDTO.java`; `BookService.java`, `convertToDTO`

**Objetivo:** Evoluir a representação plana de autor para objeto aninhado.

**Alteração planejada:** Substituir `authorId` e `authorName` por um objeto `author` preenchido com identidade e nome.

**Intenção:** Adotar deliberadamente representação relacional estruturada.

**Observabilidade no snapshot:** Duas propriedades planas existentes desaparecem e um objeto JSON não nulo surge no body.

**Ground Truth:** SHOULD_UPDATE
**Justificativa do Ground Truth:** A nova forma relacional é o contrato intencional do caso.
**Dificuldade:** HARD
**Alcance esperado:** MULTIPLE_SNAPSHOTS
**Status:** PLANNED
**Riscos de execução:** Reutilizar entidades diretamente pode causar ciclos; a implementação futura deve manter body serializável e alcançar ApprovalTests.

## CASE-020

**Categoria:** BUSINESS_RULE
**Snapshot alvo:** `BookApiIntegrationTest.testCreateBook_Snapshot.approved.txt`
**Teste alvo:** `BookApiIntegrationTest.testCreateBook_Snapshot`
**Endpoint:** `/books`
**HTTP:** POST
**Mutation Point:** MP-013, MP-015
**Arquivo/região candidata:** `BookService.java`, `createBook`/`convertToDTO`

**Objetivo:** Normalizar deliberadamente ISBN na representação retornada.

**Alteração planejada:** Persistir/retornar o ISBN canônico sem hífens para a entrada `978-0-14-043926-8`.

**Intenção:** Aplicar regra aprovada de canonicalização para comparação e integração.

**Observabilidade no snapshot:** O campo `isbn` contém hífens e passará a outro texto não vazio.

**Ground Truth:** SHOULD_UPDATE
**Justificativa do Ground Truth:** A diferença é o resultado correto da nova regra explícita.
**Dificuldade:** MEDIUM
**Alcance esperado:** MULTIPLE_SNAPSHOTS
**Status:** PLANNED
**Riscos de execução:** Normalizar apenas na busca de duplicidade, sem alterar o valor retornado, não gera diff.

## CASE-021

**Categoria:** BUG
**Snapshot alvo:** `BookApiIntegrationTest.testCreateBook_Snapshot.approved.txt`
**Teste alvo:** `BookApiIntegrationTest.testCreateBook_Snapshot`
**Endpoint:** `/books`
**HTTP:** POST
**Mutation Point:** MP-014
**Arquivo/região candidata:** `BookService.java`, `convertToDTO`, composição de `authorName`

**Objetivo:** Detectar inversão acidental do nome do autor.

**Alteração planejada:** Compor `authorName` como `lastName + " " + firstName` sem decisão contratual.

**Intenção:** Simular troca de ordem em valor derivado.

**Observabilidade no snapshot:** `Arthur Conan Doyle` passará a `Conan Doyle Arthur`.

**Ground Truth:** SHOULD_NOT_UPDATE
**Justificativa do Ground Truth:** A representação ficaria incorreta segundo o comportamento esperado do caso.
**Dificuldade:** EASY
**Alcance esperado:** MULTIPLE_SNAPSHOTS
**Status:** PLANNED
**Riscos de execução:** Nenhum relevante porque os componentes do nome são distintos.

## CASE-022

**Categoria:** BUG
**Snapshot alvo:** `BookApiIntegrationTest.testCreateBook_Snapshot.approved.txt`
**Teste alvo:** `BookApiIntegrationTest.testCreateBook_Snapshot`
**Endpoint:** `/books`
**HTTP:** POST
**Mutation Point:** MP-013, MP-014, MP-016
**Arquivo/região candidata:** `BookService.java`, `convertToDTO`; `Book.java`, relação `author`

**Objetivo:** Detectar `authorId` mapeado a partir da identidade errada.

**Alteração planejada:** Aplicar uma transformação off-by-one ao ID real do autor no mapper, garantindo de modo determinístico um `authorId` incorreto sem depender dos valores gerados para livro e autor.

**Intenção:** Simular bug de relacionamento entre entidades com IDs do mesmo tipo.

**Observabilidade no snapshot:** O `authorId` publicado será sempre diferente do ID real presente no baseline, enquanto `authorName` continuará derivado do autor correto.

**Ground Truth:** SHOULD_NOT_UPDATE
**Justificativa do Ground Truth:** O relacionamento público se tornaria internamente inconsistente.
**Dificuldade:** MEDIUM
**Alcance esperado:** MULTIPLE_SNAPSHOTS
**Status:** PLANNED
**Riscos de execução:** A transformação deve preservar o fluxo e não alterar a relação persistida; o mapper compartilhado afetará os dois snapshots de livro.

## CASE-023

**Categoria:** SERIALIZATION
**Snapshot alvo:** `BookApiIntegrationTest.testCreateBook_Snapshot.approved.txt`
**Teste alvo:** `BookApiIntegrationTest.testCreateBook_Snapshot`
**Endpoint:** `/books`
**HTTP:** POST
**Mutation Point:** MP-013, MP-021
**Arquivo/região candidata:** `BookService.java`, `convertToDTO`; `BookDTO.java`, `isbn`

**Objetivo:** Detectar omissão acidental do ISBN.

**Alteração planejada:** Deixar `isbn` nulo no DTO de saída, fazendo `NON_NULL` retirar a chave.

**Intenção:** Simular perda de mapeamento de um identificador bibliográfico.

**Observabilidade no snapshot:** A chave `isbn` e seu valor aparecem no aprovado e serão removidos do body.

**Ground Truth:** SHOULD_NOT_UPDATE
**Justificativa do Ground Truth:** Atualizar o snapshot esconderia perda não intencional de informação.
**Dificuldade:** EASY
**Alcance esperado:** MULTIPLE_SNAPSHOTS
**Status:** PLANNED
**Riscos de execução:** A entidade deve continuar válida e o fluxo chegar à serialização.

## CASE-024

**Categoria:** CONTRACT_EVOLUTION
**Snapshot alvo:** `BookApiIntegrationTest.testCreateBook_Snapshot.approved.txt`
**Teste alvo:** `BookApiIntegrationTest.testCreateBook_Snapshot`
**Endpoint:** `/books`
**HTTP:** POST
**Mutation Point:** MP-012, MP-019, MP-021
**Arquivo/região candidata:** `BookController.java`, `createBook`; campo `reviews` já existente em `BookDTO.java`

**Objetivo:** Incluir deliberadamente coleção vazia de avaliações na resposta criada.

**Alteração planejada:** Preencher `reviews` como `[]` somente no DTO devolvido por `BookController.createBook`, em vez de mantê-lo nulo/omitido.

**Intenção:** Tornar explícito que um livro recém-criado ainda não possui avaliações.

**Observabilidade no snapshot:** A política `NON_NULL` serializa lista vazia; surgirá `"reviews":[]` no objeto aprovado.

**Ground Truth:** SHOULD_UPDATE
**Justificativa do Ground Truth:** A presença da coleção é uma extensão intencional do contrato.
**Dificuldade:** MEDIUM
**Alcance esperado:** TARGET_ONLY
**Status:** PLANNED
**Riscos de execução:** Uma configuração Jackson que omita coleções vazias impediria o diff; a alteração não deve ser movida para o mapper compartilhado.

## CASE-025

**Categoria:** COLLECTION
**Snapshot alvo:** `BookApiIntegrationTest.testGetBooksByAuthor_Snapshot.approved.txt`
**Teste alvo:** `BookApiIntegrationTest.testGetBooksByAuthor_Snapshot`
**Endpoint:** `/books/by-author/{authorId}`
**HTTP:** GET
**Mutation Point:** MP-017, MP-018
**Arquivo/região candidata:** `BookRepository.java`, `findByAuthorId`; `BookService.java`, `getBooksByAuthorId`

**Objetivo:** Adotar deliberadamente ordenação “mais recente primeiro”.

**Alteração planejada:** Ordenar a coleção por ID decrescente como nova regra pública.

**Intenção:** Exibir primeiro os livros criados mais recentemente.

**Observabilidade no snapshot:** Os dois objetos atuais aparecem em IDs 1,2; a ordem passará a 2,1 no array textual.

**Ground Truth:** SHOULD_UPDATE
**Justificativa do Ground Truth:** A nova ordenação é uma decisão funcional explícita.
**Dificuldade:** HARD
**Alcance esperado:** TARGET_ONLY
**Status:** PLANNED
**Riscos de execução:** Se os IDs ou o arranjo não forem os esperados, a ordenação pode coincidir com a saída anterior.

## CASE-026

**Categoria:** COLLECTION
**Snapshot alvo:** `BookApiIntegrationTest.testGetBooksByAuthor_Snapshot.approved.txt`
**Teste alvo:** `BookApiIntegrationTest.testGetBooksByAuthor_Snapshot`
**Endpoint:** `/books/by-author/{authorId}`
**HTTP:** GET
**Mutation Point:** MP-017, MP-018
**Arquivo/região candidata:** `BookRepository.java`, consulta derivada; `BookService.java`, `getBooksByAuthorId`

**Objetivo:** Detectar inversão acidental da ordem observada.

**Alteração planejada:** Reverter os itens sem requisito de produto que justifique a mudança.

**Intenção:** Simular regressão de ordenação causada por refatoração de consulta/coleção.

**Observabilidade no snapshot:** O array contém dois objetos distintos; a inversão altera o texto integral mesmo preservando conteúdo.

**Ground Truth:** SHOULD_NOT_UPDATE
**Justificativa do Ground Truth:** Aprovar a ordem esconderia uma mudança acidental sem intenção contratual.
**Dificuldade:** MEDIUM
**Alcance esperado:** TARGET_ONLY
**Status:** PLANNED
**Riscos de execução:** A ordem do baseline não é formalmente garantida; a mutação deverá inverter explicitamente a lista observada para produzir a mesma ordem 2,1 de CASE-025.

## CASE-027

**Categoria:** BUG
**Snapshot alvo:** `BookApiIntegrationTest.testGetBooksByAuthor_Snapshot.approved.txt`
**Teste alvo:** `BookApiIntegrationTest.testGetBooksByAuthor_Snapshot`
**Endpoint:** `/books/by-author/{authorId}`
**HTTP:** GET
**Mutation Point:** MP-017
**Arquivo/região candidata:** `BookService.java`, `getBooksByAuthorId`; `BookRepository.java`, `findByAuthorId`

**Objetivo:** Detectar item duplicado na coleção.

**Alteração planejada:** Fazer uma composição de resultados processar duas vezes o mesmo registro, produzindo um item duplicado sem uma adição manual orientada ao fixture.

**Intenção:** Simular erro de agregação/junção que duplica resultado.

**Observabilidade no snapshot:** O array aprovado tem dois itens; passará a conter um terceiro objeto repetido.

**Ground Truth:** SHOULD_NOT_UPDATE
**Justificativa do Ground Truth:** A duplicação viola o conteúdo esperado e não deve ser aprovada.
**Dificuldade:** MEDIUM
**Alcance esperado:** TARGET_ONLY
**Status:** PLANNED
**Riscos de execução:** A composição precisa continuar plausível e determinística; estruturas que deduplicam automaticamente podem neutralizar a mutação.

## CASE-028

**Categoria:** COLLECTION
**Snapshot alvo:** `BookApiIntegrationTest.testGetBooksByAuthor_Snapshot.approved.txt`
**Teste alvo:** `BookApiIntegrationTest.testGetBooksByAuthor_Snapshot`
**Endpoint:** `/books/by-author/{authorId}`
**HTTP:** GET
**Mutation Point:** MP-017
**Arquivo/região candidata:** `BookRepository.java`, `findByAuthorId`; `BookService.java`, `getBooksByAuthorId`

**Objetivo:** Detectar perda acidental de item.

**Alteração planejada:** Aplicar filtro/limite incorreto que remova um dos dois livros do autor.

**Intenção:** Simular regressão de consulta ou processamento de coleção.

**Observabilidade no snapshot:** O body aprovado possui dois objetos distintos; apenas um permanecerá.

**Ground Truth:** SHOULD_NOT_UPDATE
**Justificativa do Ground Truth:** Atualizar ocultaria conteúdo persistido que deixou de ser retornado.
**Dificuldade:** MEDIUM
**Alcance esperado:** TARGET_ONLY
**Status:** PLANNED
**Riscos de execução:** O filtro deve distinguir os títulos/IDs do fixture e ainda devolver resposta 200.

## CASE-029

**Categoria:** CONTRACT_EVOLUTION
**Snapshot alvo:** `BookApiIntegrationTest.testGetBooksByAuthor_Snapshot.approved.txt`
**Teste alvo:** `BookApiIntegrationTest.testGetBooksByAuthor_Snapshot`
**Endpoint:** `/books/by-author/{authorId}`
**HTTP:** GET
**Mutation Point:** MP-017, MP-019
**Arquivo/região candidata:** `BookController.java`, `getBooksByAuthorId`; `BookService.java`, `getBooksByAuthorId`

**Objetivo:** Evoluir a coleção para envelope com contagem.

**Alteração planejada:** Substituir o array raiz por objeto com `books` contendo os dois itens e `count:2`.

**Intenção:** Preparar contrato extensível para metadados de coleção.

**Observabilidade no snapshot:** O body deixa de começar por array e passa a conter objeto, nova chave e contagem materializada.

**Ground Truth:** SHOULD_UPDATE
**Justificativa do Ground Truth:** A representação envelopada é uma evolução deliberada e correta.
**Dificuldade:** HARD
**Alcance esperado:** TARGET_ONLY
**Status:** PLANNED
**Riscos de execução:** Alterar apenas a assinatura genérica sem modificar o objeto retornado não muda o JSON.

## CASE-030

**Categoria:** CONTRACT_EVOLUTION
**Snapshot alvo:** `BookApiIntegrationTest.testGetBooksByAuthor_Snapshot.approved.txt`
**Teste alvo:** `BookApiIntegrationTest.testGetBooksByAuthor_Snapshot`
**Endpoint:** `/books/by-author/{authorId}`
**HTTP:** GET
**Mutation Point:** MP-013, MP-014
**Arquivo/região candidata:** `BookService.java`, `convertToDTO`, composição de `authorName`

**Objetivo:** Adotar representação bibliográfica deliberada para o nome do autor.

**Alteração planejada:** Representar `authorName` no formato bibliográfico `lastName, firstName` em todas as respostas de livro.

**Intenção:** Alinhar a exibição de autoria a uma convenção de catálogo bibliográfico aplicável ao domínio, sem depender de títulos específicos do fixture.

**Observabilidade no snapshot:** `Arthur Conan Doyle` passará deterministicamente a `Conan Doyle, Arthur` em cada item do array e também na resposta de criação de livro.

**Ground Truth:** SHOULD_UPDATE
**Justificativa do Ground Truth:** A nova representação é uma evolução intencional e semanticamente válida para o domínio bibliográfico.
**Dificuldade:** HARD
**Alcance esperado:** MULTIPLE_SNAPSHOTS
**Status:** PLANNED
**Riscos de execução:** O mapper compartilhado afetará os dois snapshots de livro; o parsing deve respeitar `firstName` e `lastName` existentes, sem tentar decompor a string atual.

## Oportunidades fora do escopo do snapshot atual

As oportunidades abaixo são `OUT_OF_SCOPE_CURRENT_SNAPSHOT` e não originam `CASE-*`, pois `Approvals.verify()` recebe somente `responseBody`:

- mudança isolada de status HTTP (200/201/404/204), inclusive nas regiões de controller;
- adição, remoção ou alteração isolada de headers;
- mudança isolada do response `Content-Type`;
- inclusão ou alteração isolada de header `Location` após criação;
- diferenças de cookies, encoding ou demais metadados de `MockHttpServletResponse`;
- endpoints sem um dos seis snapshots existentes, ainda que tenham potencial factual no inventário;
- propriedades de elementos de `AuthorDTO` no snapshot `testGetAllAuthors`, enquanto seu fixture continuar produzindo `[]`.

## Matriz de cobertura

| Caso | Snapshot | Categoria | Ground Truth | Dificuldade | Mutation Point |
|---|---|---|---|---|---|
| CASE-001 | GetAllAuthors | CONTRACT_EVOLUTION | SHOULD_UPDATE | MEDIUM | MP-005, MP-007 |
| CASE-002 | GetAllAuthors | BUG | SHOULD_NOT_UPDATE | EASY | MP-005, MP-007 |
| CASE-003 | GetAllAuthors | NOISE | SHOULD_NOT_UPDATE | HARD | MP-021 |
| CASE-004 | CreateAuthor | CONTRACT_EVOLUTION | SHOULD_UPDATE | MEDIUM | MP-001, MP-002 |
| CASE-005 | CreateAuthor | BREAKING_CHANGE | SHOULD_UPDATE | EASY | MP-001, MP-021 |
| CASE-006 | CreateAuthor | BUG | SHOULD_NOT_UPDATE | EASY | MP-002 |
| CASE-007 | CreateAuthor | SERIALIZATION | SHOULD_NOT_UPDATE | EASY | MP-002, MP-021 |
| CASE-008 | CreateAuthor | BREAKING_CHANGE | SHOULD_UPDATE | HARD | MP-001, MP-002 |
| CASE-009 | GetAuthorById | CONTRACT_EVOLUTION | SHOULD_UPDATE | MEDIUM | MP-001, MP-002, MP-007 |
| CASE-010 | GetAuthorById | BUG | SHOULD_NOT_UPDATE | EASY | MP-002, MP-004 |
| CASE-011 | GetAuthorById | BUSINESS_RULE | SHOULD_UPDATE | HARD | MP-002, MP-007 |
| CASE-012 | GetAuthorById | SERIALIZATION | SHOULD_NOT_UPDATE | MEDIUM | MP-001, MP-002, MP-021 |
| CASE-013 | AuthorNotFound | ERROR_HANDLING | SHOULD_UPDATE | EASY | MP-008, MP-009 |
| CASE-014 | AuthorNotFound | ERROR_HANDLING | SHOULD_NOT_UPDATE | EASY | MP-009 |
| CASE-015 | AuthorNotFound | SERIALIZATION | SHOULD_UPDATE | MEDIUM | MP-008, MP-010 |
| CASE-016 | AuthorNotFound | NON_DETERMINISTIC | SHOULD_NOT_UPDATE | HARD | MP-010 |
| CASE-017 | AuthorNotFound | CONTRACT_EVOLUTION | SHOULD_UPDATE | MEDIUM | MP-011, MP-021 |
| CASE-018 | AuthorNotFound | ERROR_HANDLING | SHOULD_NOT_UPDATE | MEDIUM | MP-008 |
| CASE-019 | CreateBook | CONTRACT_EVOLUTION | SHOULD_UPDATE | HARD | MP-012, MP-013, MP-014 |
| CASE-020 | CreateBook | BUSINESS_RULE | SHOULD_UPDATE | MEDIUM | MP-013, MP-015 |
| CASE-021 | CreateBook | BUG | SHOULD_NOT_UPDATE | EASY | MP-014 |
| CASE-022 | CreateBook | BUG | SHOULD_NOT_UPDATE | MEDIUM | MP-013, MP-014, MP-016 |
| CASE-023 | CreateBook | SERIALIZATION | SHOULD_NOT_UPDATE | EASY | MP-013, MP-021 |
| CASE-024 | CreateBook | CONTRACT_EVOLUTION | SHOULD_UPDATE | MEDIUM | MP-012, MP-019, MP-021 |
| CASE-025 | GetBooksByAuthor | COLLECTION | SHOULD_UPDATE | HARD | MP-017, MP-018 |
| CASE-026 | GetBooksByAuthor | COLLECTION | SHOULD_NOT_UPDATE | MEDIUM | MP-017, MP-018 |
| CASE-027 | GetBooksByAuthor | BUG | SHOULD_NOT_UPDATE | MEDIUM | MP-017 |
| CASE-028 | GetBooksByAuthor | COLLECTION | SHOULD_NOT_UPDATE | MEDIUM | MP-017 |
| CASE-029 | GetBooksByAuthor | CONTRACT_EVOLUTION | SHOULD_UPDATE | HARD | MP-017, MP-019 |
| CASE-030 | GetBooksByAuthor | CONTRACT_EVOLUTION | SHOULD_UPDATE | HARD | MP-013, MP-014 |

### Contagens por snapshot

| Snapshot | Casos |
|---|---:|
| `AuthorApiIntegrationTest.testGetAllAuthors_Snapshot.approved.txt` | 3 |
| `AuthorApiIntegrationTest.testCreateAuthor_Snapshot.approved.txt` | 5 |
| `AuthorApiIntegrationTest.testGetAuthorById_Snapshot.approved.txt` | 4 |
| `AuthorApiIntegrationTest.testGetAuthorNotFound_Snapshot.approved.txt` | 6 |
| `BookApiIntegrationTest.testCreateBook_Snapshot.approved.txt` | 6 |
| `BookApiIntegrationTest.testGetBooksByAuthor_Snapshot.approved.txt` | 6 |
| **Total** | **30** |

### Contagens por categoria

| Categoria | Casos |
|---|---:|
| CONTRACT_EVOLUTION | 8 |
| BREAKING_CHANGE | 2 |
| BUSINESS_RULE | 2 |
| HTTP | 0 |
| SERIALIZATION | 4 |
| ERROR_HANDLING | 3 |
| COLLECTION | 3 |
| NON_DETERMINISTIC | 1 |
| NOISE | 1 |
| BUG | 6 |
| **Total** | **30** |

Categorias com zero casos foram preservadas na contagem. `HTTP` ficou vazio porque nenhuma proposta puramente HTTP é elegível. `NOISE` passou a representar a alteração textual sem mudança semântica de CASE-003 e permanece distinto do timestamp variável de CASE-016.

### Contagens por Ground Truth

| Ground Truth | Casos |
|---|---:|
| SHOULD_UPDATE | 15 |
| SHOULD_NOT_UPDATE | 15 |
| **Total** | **30** |

### Contagens por dificuldade

| Dificuldade | Casos |
|---|---:|
| EASY | 9 |
| MEDIUM | 13 |
| HARD | 8 |
| **Total** | **30** |

### Contagens por alcance esperado

| Alcance esperado | Casos |
|---|---:|
| TARGET_ONLY | 13 |
| MULTIPLE_SNAPSHOTS | 11 |
| GLOBAL_BEHAVIOR | 6 |
| **Total** | **30** |

## Pares contrastivos planejados

| Par | Snapshot | Diferença observável | GT A | GT B | Requisito de comparabilidade |
|---|---|---|---|---|---|
| CASE-007 / CASE-008 | `AuthorApiIntegrationTest.testCreateAuthor_Snapshot.approved.txt` | Mesma omissão textual de `email` | SHOULD_NOT_UPDATE | SHOULD_UPDATE | Usar o mesmo mapper, quantidade de arquivos e mutação mínima; somente a intenção reservada ao pesquisador deve diferir. |
| CASE-013 / CASE-014 | `AuthorApiIntegrationTest.testGetAuthorNotFound_Snapshot.approved.txt` | Alteração do campo `message` | SHOULD_UPDATE | SHOULD_NOT_UPDATE | Manter mudança pequena de uma mensagem no mesmo body; evitar alterações adicionais no handler. |
| CASE-025 / CASE-026 | `BookApiIntegrationTest.testGetBooksByAuthor_Snapshot.approved.txt` | Mesma inversão do array de IDs 1,2 para 2,1 | SHOULD_UPDATE | SHOULD_NOT_UPDATE | Forçar deterministicamente o mesmo resultado ordenado; diferenciar somente regra “mais recente primeiro” de inversão sem requisito. |

CASE-021 e CASE-030 também formam um contraste secundário sobre `authorName`: inversão sem convenção versus representação bibliográfica deliberada. Eles não substituem os três pares principais porque seus textos finais e snapshots-alvo primários não são idênticos.

## Substituições realizadas

### CASE-003

- Caso anterior: fallback hardcoded de autor seed após uma listagem vazia.
- Motivo: dependia de comportamento artificial, conflitava com a limpeza do `@BeforeEach` e inventava dado para produzir o diff.
- Novo conceito: alteração global de configuração Jackson que introduz whitespace determinístico em `[]` sem mudar a coleção.
- Maior realismo: mudanças de configuração/pretty-print durante manutenção são plausíveis e atravessam a serialização real já executada.
- Equilíbrio preservado: continua `SHOULD_NOT_UPDATE`, `HARD`, no snapshot GetAllAuthors; passa de `COLLECTION` para `NOISE` e explicita `GLOBAL_BEHAVIOR`.

### CASE-030

- Caso anterior: filtro por prefixo literal `Sherlock` na rota por autor.
- Motivo: regra orientada ao fixture e não ao contrato/domínio.
- Novo conceito: convenção bibliográfica intencional `lastName, firstName` para `authorName` no mapper real de livros.
- Maior realismo: a aplicação representa autores e livros; ordenação bibliográfica do nome é evolução natural e não depende dos títulos do fixture.
- Equilíbrio preservado: continua `SHOULD_UPDATE` e `HARD`, usa snapshot real e assume corretamente `MULTIPLE_SNAPSHOTS`.

## Revisão de pistas espúrias

`SPURIOUS_CUE_REVIEW_COMPLETED`

- CASE-007/008 e CASE-025/026 foram ajustados para manter forma e tamanho de diff próximos com Ground Truth oposto.
- CASE-030 oferece mudança intencional pequena no mapper, reduzindo a associação entre `SHOULD_UPDATE` e patches amplos.
- CASE-003 acrescenta um `SHOULD_NOT_UPDATE` global e contextual, reduzindo a associação entre regressão e troca isolada de uma linha de negócio.
- Persistem desequilíbrios: todos os `CONTRACT_EVOLUTION` e `BREAKING_CHANGE` são `SHOULD_UPDATE`; todos os `BUG`, `NON_DETERMINISTIC` e `NOISE` são `SHOULD_NOT_UPDATE`; 6 dos 8 casos `HARD` continuam `SHOULD_UPDATE`.
- Categoria, intenção, dificuldade, ID e Ground Truth permanecem reservados neste catálogo e não podem integrar `llm-input.json`.

## Auditoria interna e candidatos descartados

Cada caso mantido foi revisado quanto à existência do snapshot, chamada real a `Approvals.verify`, uso de código/MP existente, alteração plausível do body, execução do trecho no cenário, intenção, Ground Truth, independência e origem comum no baseline.

Foram descartadas estas classes de candidato:

- mudanças exclusivas de status, headers, Content-Type ou Location: não chegam ao texto snapshotado;
- alterações de campos de autores aplicadas somente aos elementos de `testGetAllAuthors`: o snapshot é `[]`, portanto o mapeamento de item não executa;
- propostas sobre endpoints de reviews, updates, deletes e demais rotas sem snapshot: não pertencem aos seis cenários elegíveis;
- remoções adicionais de campos do mesmo DTO e trocas adicionais de propriedades pelo mesmo mecanismo: redundantes com CASE-006, CASE-007, CASE-021 e CASE-023;
- adições adicionais de campos derivados sem nova exigência contextual: redundantes com CASE-004 e CASE-024;
- ordenações por título/ISBN que preservariam a ordem dos valores atuais: não produziriam falha de snapshot no fixture real;
- deduplicação intencional por ISBN: os dois ISBNs atuais são distintos, logo o body permaneceria igual;
- mudanças que afetariam apenas bodies de requisições de arranjo, mas não o response body finalmente enviado a ApprovalTests.

Nenhum caso foi implementado, executado ou convertido em `EXP-*`.
