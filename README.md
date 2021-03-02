# Utilidades para cálculo de xi(r, mu) e multipólos a partir do nbodykit

Estes scripts são breves wrappers ao redor do nbodykit e do numpy para geração de randoms e cálculo da função de correlação de 2 pontos espacial (tanto como função de r e mu como os seus multipólos). Consulte https://nbodykit.readthedocs.io/en/latest/ para mais informações sobre o nbodykit. Pequenas alterações permitem calcular outros tipos de estatísticas de 2 pontos.

## Dependências
    pyyaml e nbodykit. Para instalação confira https://nbodykit.readthedocs.io/en/latest/getting-started/install.html e https://pyyaml.org/wiki/PyYAMLDocumentation.

## Scripts

### randoms.py

Uso:

`bash
    python make_randoms.py <number of randoms> <Lbox size in Mpc/h> <integer seed to use> <output file name>
`

Onde:
    * <number of randoms>: tamanho do catálogo de randoms a ser gerado
    * <Lbox size in Mpc/h>: tamanho da caixa tridimensional contendo os randoms
    * <integer seed to use>: um inteiro qualquer para semente do gerador de números aleatórios
    * <output file name>: arquivo de saída

### xi.py

`bash
    python xi.py config.yaml
`

Onde config.yaml é o arquivo de configuração (cf. exemplo).

### job.pbs

Exemplo de diretivas para o gerenciador de trabalhos do cluster planck.
