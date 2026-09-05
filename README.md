# Cálculo de Matrizes

Programa em Python para estudar e realizar operações básicas com matrizes.

## Operações previstas

O programa possui um menu com as seguintes operações:

| Opção | Operação | Descrição |
| --- | --- | --- |
| 1 | Soma | Soma duas matrizes de mesma ordem, elemento por elemento. |
| 2 | Multiplicação escalar | Multiplica todos os elementos de uma matriz por um número. |
| 3 | Multiplicação | Multiplica duas matrizes quando o número de colunas da primeira é igual ao número de linhas da segunda. |
| 4 | Transposta | Troca as linhas pelas colunas de uma matriz. |
| 5 | Inversa | Calcula a matriz inversa quando ela é quadrada e possui determinante diferente de zero. |
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

Ao iniciar, informe as linhas e as colunas das matrizes A e B. Os valores devem ser separados por vírgulas. Por exemplo:

```text
Digite um número para representar as linhas da matriz A: 1,2
Digite um número para representar as colunas da matriz A: 3,4
```

Depois, escolha no menu o número correspondente à operação desejada.

## Regras das operações

### Soma

As duas matrizes precisam ter a mesma quantidade de linhas e colunas:

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

Se `A` tem ordem `m x n`, `B` precisa ter ordem `n x p`. O resultado terá ordem `m x p`.

### Transposta

Na transposta, o elemento que está na posição linha `i`, coluna `j` passa para a posição linha `j`, coluna `i`.

### Inversa

A inversa só existe para matrizes quadradas cujo determinante seja diferente de zero. Quando existe, ela é indicada por `A⁻¹` e satisfaz:

```text
A * A⁻¹ = I
```

em que `I` é a matriz identidade.

## Status do projeto

O menu e as validações iniciais estão estruturados. A implementação dos cálculos e da leitura completa dos elementos das matrizes ainda está em desenvolvimento.

## Tecnologias

- Python
- Git