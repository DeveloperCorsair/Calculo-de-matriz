# Cálculo de Matrizes

Programa em Python para realizar operações com matrizes e resolver sistemas lineares, com todos os dados digitados pelo teclado.

## Operações

O programa possui um menu com as seguintes operações:

| Opção | Operação | Descrição |
| --- | --- | --- |
| 1 | Soma | Soma duas matrizes de mesma ordem, elemento por elemento. |
| 2 | Multiplicação escalar | Multiplica todos os elementos de uma matriz por um número. |
| 3 | Multiplicação | Multiplica duas matrizes quando o número de colunas da primeira é igual ao número de linhas da segunda. |
| 4 | Transposta | Troca as linhas pelas colunas de uma matriz. |
| 5 | Inversa | Calcula a matriz inversa quando ela é quadrada e possui determinante diferente de zero. |
| 6 | Sistema linear | Resolve um sistema linear e o classifica em SPD, SPI ou SI. |
| 0 | Sair | Encerra o programa. |

## Requisitos

- Python 3.10 ou superior, por causa da utilização de `match/case`.
- Terminal ou prompt de comando.

## Como executar

1. Clone este repositório ou baixe os arquivos.
2. Abra o terminal na pasta do projeto.
3. Execute:

```bash
python calc.py
```

No Windows, também pode ser necessário usar:

```bash
py calc.py
```

Escolha no menu o número da operação. Em seguida, o programa pede a ordem da(s) matriz(es) e cada elemento, um por vez. Os números podem ser inteiros, decimais ou frações (`2`, `1.5`, `1/3`). Os cálculos usam frações exatas, então não há erro de arredondamento.

## Regras das operações

### Soma

As duas matrizes precisam ter a mesma quantidade de linhas e colunas (o programa pede a ordem só de A e usa a mesma em B):

```text
A = [1 2]       B = [5 6]
    [3 4]           [7 8]

A + B = [6  8]
        [10 12]
```

### Multiplicação escalar

Cada elemento da matriz é multiplicado pelo escalar informado:

```text
2 * [1 3] = [2 6]
    [2 4]   [4 8]
```

### Multiplicação de matrizes

Se `A` tem ordem `m x n`, `B` precisa ter ordem `n x p`. O resultado terá ordem `m x p`. O programa já define o número de linhas de `B` e pergunta apenas as colunas.

### Transposta

Na transposta, o elemento que está na posição linha `i`, coluna `j` passa para a posição linha `j`, coluna `i`.

### Inversa

A inversa só existe para matrizes quadradas cujo determinante seja diferente de zero. Quando existe, ela é indicada por `A⁻¹` e satisfaz:

```text
A * A⁻¹ = I
```

em que `I` é a matriz identidade. O cálculo é feito escalonando a matriz `[A | I]` (método de Gauss-Jordan). Se não for possível obter a identidade do lado esquerdo, a matriz não tem inversa e o programa avisa.

### Sistema linear

Informe o número de equações, o número de incógnitas e, para cada equação, os coeficientes e o termo independente. O programa escalona a matriz aumentada `[A | b]` (Gauss-Jordan) e compara o posto de `A` com o posto de `[A | b]`:

| Classificação | Condição | Resultado mostrado |
| --- | --- | --- |
| SPD (possível e determinado) | posto(A) = posto([A\|b]) = número de incógnitas | Solução única. |
| SPI (possível e indeterminado) | posto(A) = posto([A\|b]) < número de incógnitas | Solução geral, com as variáveis livres. |
| SI (impossível) | posto(A) < posto([A\|b]) | Não há solução. |

Exemplo (SPI): `x + y = 2` e `2x + 2y = 4` resultam em `x2 = livre` e `x1 = 2 - 1*x2`.

## Tecnologias

- Python
- Git