# Baseline

O baseline oficial é o commit que introduz e congela a estrutura documental do Benchmark V2, incluindo este arquivo e o relatório de auditoria. Seu SHA autoritativo deve ser obtido diretamente pelo Git no repositório, evitando uma referência circular dentro do próprio commit.

Cada experimento deve registrar esse SHA no campo `baselineCommit` de seu `execution.json` e começar diretamente desse mesmo estado imutável, salvo decisão metodológica explicitamente registrada.

Os experimentos são ramificações independentes do baseline. Nenhum caso pode usar como ponto inicial o estado produzido por outro experimento.
