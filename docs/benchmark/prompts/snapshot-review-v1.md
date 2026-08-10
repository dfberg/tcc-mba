# PROMPT_TEMPLATE_V1

Você está revisando uma falha de snapshot causada por uma alteração de código.

Analise exclusivamente as evidências fornecidas. Não presuma contexto de negócio ou informações que não estejam presentes nelas.

Decida entre estas duas classificações:

- `SHOULD_UPDATE`: a diferença observada parece representar o comportamento esperado que deve substituir o snapshot aprovado.
- `SHOULD_NOT_UPDATE`: a diferença observada parece representar erro, comportamento inadequado ou ruído que não deve ser incorporado ao snapshot aprovado.

## Contexto técnico

Endpoint: `[ENDPOINT]`

Método HTTP: `[HTTP_METHOD]`

Teste: `[TEST_NAME]`

## Git diff

```diff
[GIT_DIFF]
```

## Snapshot aprovado

```text
[APPROVED_SNAPSHOT]
```

## Snapshot recebido

```text
[RECEIVED_SNAPSHOT]
```

## Output do teste

```text
[TEST_OUTPUT]
```

Determine se o snapshot aprovado deve ser atualizado.

Responda somente com um objeto JSON válido, sem Markdown, bloco de código ou texto adicional, contendo exatamente:

- `shouldUpdateSnapshot`: booleano; `true` representa `SHOULD_UPDATE` e `false` representa `SHOULD_NOT_UPDATE`;
- `confidence`: inteiro de 0 a 100 com a confiança autorrelatada;
- `reason`: justificativa textual baseada apenas nas evidências.
