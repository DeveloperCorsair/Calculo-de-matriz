from fractions import Fraction


# ---------------------------------------------------------------
# Leitura de dados pelo teclado
# ---------------------------------------------------------------
def ler_numero(msg):
    """Lê um número (inteiro, decimal ou fração, ex.: 2, 1.5, 1/3)."""
    while True:
        txt = input(msg).strip().replace(",", ".")
        try:
            return Fraction(txt)
        except (ValueError, ZeroDivisionError):
            print("  Valor inválido. Use inteiro, decimal ou fração (ex.: 2, 1.5, 1/3).")


def ler_inteiro_positivo(msg):
    while True:
        txt = input(msg).strip()
        if txt.isdigit() and int(txt) > 0:
            return int(txt)
        print("  Digite um número inteiro positivo.")


def ler_matriz(nome, linhas=None, colunas=None):
    """Lê uma matriz. Se linhas/colunas forem dadas, não pergunta a ordem."""
    if linhas is None:
        linhas = ler_inteiro_positivo(f"Número de linhas da matriz {nome}: ")
    if colunas is None:
        colunas = ler_inteiro_positivo(f"Número de colunas da matriz {nome}: ")
    matriz = []
    for i in range(linhas):
        matriz.append([ler_numero(f"  {nome}[{i + 1}][{j + 1}] = ") for j in range(colunas)])
    return matriz


# ---------------------------------------------------------------
# Saída formatada
# ---------------------------------------------------------------
def fmt(x):
    """Mostra inteiro quando possível; senão, fração."""
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def mostrar_matriz(m, titulo=None):
    if titulo:
        print(titulo)
    larg = max(len(fmt(x)) for linha in m for x in linha)
    for linha in m:
        print("  | " + "  ".join(fmt(x).rjust(larg) for x in linha) + " |")


# ---------------------------------------------------------------
# Operações com matrizes
# ---------------------------------------------------------------
def somar(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def multiplicar_escalar(k, a):
    return [[k * x for x in linha] for linha in a]


def multiplicar(a, b):
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def transpor(a):
    return [[a[i][j] for i in range(len(a))] for j in range(len(a[0]))]


# ---------------------------------------------------------------
# Escalonamento (Gauss-Jordan) - usado na inversa e nos sistemas
# ---------------------------------------------------------------
def escalonar(m, n_colunas_pivo):
    """
    Reduz a matriz m à forma escalonada reduzida, procurando pivôs
    apenas nas primeiras n_colunas_pivo colunas.
    Retorna (matriz_reduzida, lista_de_colunas_pivo).
    """
    m = [linha[:] for linha in m]
    linhas = len(m)
    pivos = []
    r = 0
    for c in range(n_colunas_pivo):
        if r >= linhas:
            break
        p = next((i for i in range(r, linhas) if m[i][c] != 0), None)
        if p is None:
            continue
        m[r], m[p] = m[p], m[r]
        piv = m[r][c]
        m[r] = [x / piv for x in m[r]]
        for i in range(linhas):
            if i != r and m[i][c] != 0:
                f = m[i][c]
                m[i] = [m[i][k] - f * m[r][k] for k in range(len(m[i]))]
        pivos.append(c)
        r += 1
    return m, pivos


def inversa(a):
    """Retorna a inversa de a, ou None se a matriz for singular."""
    n = len(a)
    aumentada = [a[i][:] + [Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
    red, pivos = escalonar(aumentada, n)
    if len(pivos) < n:
        return None
    return [linha[n:] for linha in red]


# ---------------------------------------------------------------
# Sistemas lineares: classificação SPD / SPI / SI
# ---------------------------------------------------------------
def formatar_equacao(coeficientes, termo):
    """Ex.: [2, -1, 1] e 0  ->  '2x1 - x2 + x3 = 0'."""
    partes = []
    for j, c in enumerate(coeficientes):
        if c == 0:
            continue
        modulo = abs(c)
        parte_coef = "" if modulo == 1 else f"{fmt(modulo)}"
        if not partes:
            sinal = "-" if c < 0 else ""
        else:
            sinal = "- " if c < 0 else "+ "
        partes.append(f"{sinal}{parte_coef}x{j + 1}")
    esquerda = " ".join(partes) if partes else "0"
    return f"{esquerda} = {fmt(termo)}"


def ler_sistema(eqs, n):
    """Lê o sistema e pede confirmação antes de seguir."""
    while True:
        print("\nDigite cada equação. Para cada uma, informe os coeficientes de x1, x2, ...")
        print("e depois o termo independente (o valor que fica depois do =).")
        aug = []
        for i in range(eqs):
            print(f"\nEquação {i + 1}:")
            linha = [ler_numero(f"  coeficiente de x{j + 1}: ") for j in range(n)]
            linha.append(ler_numero("  termo independente (depois do =): "))
            aug.append(linha)

        print("\nSistema digitado:")
        for i, linha in enumerate(aug):
            print(f"  ({i + 1})  {formatar_equacao(linha[:n], linha[n])}")

        resposta = input("\nO sistema está correto? (s/n): ").strip().lower()
        if resposta.startswith("s"):
            return aug
        print("Ok, vamos digitar o sistema novamente.")


def verificar_solucao(aug, n, solucao):
    """Substitui a solução em cada equação original e mostra se confere."""
    print("\nVerificação (substituindo a solução nas equações originais):")
    for i, linha in enumerate(aug):
        lhs = sum(linha[j] * solucao[j] for j in range(n))
        ok = "OK" if lhs == linha[n] else "ERRO"
        print(f"  ({i + 1})  {fmt(lhs)} = {fmt(linha[n])}   [{ok}]")


def resolver_sistema():
    print("\n=== Resolução de sistema linear ===")
    eqs = ler_inteiro_positivo("Quantas equações o sistema tem? ")
    n = ler_inteiro_positivo("Quantas incógnitas (x1, x2, ...)? ")
    aug = ler_sistema(eqs, n)

    # Passo 1 - matriz aumentada
    print("\nPasso 1 - Matriz aumentada [A | b] (coeficientes à esquerda, termos independentes à direita):")
    mostrar_matriz(aug)

    # Passo 2 - escalonamento
    red, pivos = escalonar(aug, n)
    print("\nPasso 2 - Escalonamento (Gauss-Jordan): zeramos os demais elementos de cada coluna")
    print("de pivô, para que cada variável fique isolada em uma linha.")
    mostrar_matriz(red)

    # Passo 3 - postos
    posto_a = len(pivos)
    impossivel = any(all(x == 0 for x in linha[:n]) and linha[n] != 0 for linha in red)
    posto_aug = posto_a + (1 if impossivel else 0)
    print("\nPasso 3 - Comparação dos postos (quantidade de pivôs, ou seja, de linhas úteis):")
    print(f"  posto(A)     = {posto_a}")
    print(f"  posto([A|b]) = {posto_aug}")
    print(f"  incógnitas   = {n}")

    # Passo 4 - classificação
    print("\nPasso 4 - Classificação:")
    if impossivel:
        print("  SI - Sistema Impossível.")
        print("  Surgiu uma linha do tipo 0 = b, com b diferente de zero.")
        print("  Isso é uma contradição, então o sistema não tem solução.")
        return

    if posto_a == n:
        print("  SPD - Sistema Possível e Determinado.")
        print("  Há um pivô para cada incógnita, então existe exatamente uma solução:")
        solucao = [None] * n
        for k, c in enumerate(pivos):
            solucao[c] = red[k][n]
            print(f"    x{c + 1} = {fmt(red[k][n])}")
        verificar_solucao(aug, n, solucao)
    else:
        livres = [j for j in range(n) if j not in pivos]
        nomes_livres = {j: f"t{k + 1}" for k, j in enumerate(livres)}
        print("  SPI - Sistema Possível e Indeterminado.")
        print(f"  Há menos pivôs que incógnitas: {len(livres)} variável(is) não tem pivô.")
        print("  Ela(s) pode(m) assumir qualquer valor, então há infinitas soluções.")
        print("\n  Solução geral (t1, t2, ... podem ser qualquer número real):")
        for j in livres:
            print(f"    x{j + 1} = {nomes_livres[j]}")
        for k, c in enumerate(pivos):
            expressao = fmt(red[k][n])
            for j in livres:
                coef = -red[k][j]
                if coef == 0:
                    continue
                modulo = abs(coef)
                parte = nomes_livres[j] if modulo == 1 else f"{fmt(modulo)}*{nomes_livres[j]}"
                expressao += f" {'-' if coef < 0 else '+'} {parte}"
            print(f"    x{c + 1} = {expressao}")

        # Exemplo concreto: todas as variáveis livres iguais a zero
        exemplo = {c: red[k][n] for k, c in enumerate(pivos)}
        for j in livres:
            exemplo[j] = Fraction(0)
        texto = ", ".join(f"x{j + 1} = {fmt(exemplo[j])}" for j in range(n))
        print(f"\n  Exemplo de solução (t1 = 0, t2 = 0, ...): {texto}")


# ---------------------------------------------------------------
# Operações do menu
# ---------------------------------------------------------------
def op_soma():
    print("Vou calcular a soma das matrizes")
    a = ler_matriz("A")
    b = ler_matriz("B", len(a), len(a[0]))  # B precisa ter a mesma ordem de A
    mostrar_matriz(somar(a, b), "\nA + B =")


def op_escalar():
    print("Vou calcular a multiplicação de uma matriz por escalar")
    k = ler_numero("Escalar: ")
    a = ler_matriz("A")
    mostrar_matriz(multiplicar_escalar(k, a), f"\n{fmt(k)} * A =")


def op_multiplicacao():
    print("Vou calcular a multiplicação das matrizes")
    a = ler_matriz("A")
    print(f"B precisa ter {len(a[0])} linha(s) para o produto A x B existir.")
    colunas_b = ler_inteiro_positivo("Número de colunas da matriz B: ")
    b = ler_matriz("B", len(a[0]), colunas_b)
    mostrar_matriz(multiplicar(a, b), "\nA x B =")


def op_transposta():
    print("Vou calcular a transposta da matriz")
    a = ler_matriz("A")
    mostrar_matriz(transpor(a), "\nTransposta de A =")


def op_inversa():
    print("Vou calcular a inversa da matriz")
    n = ler_inteiro_positivo("Ordem da matriz quadrada A (n x n): ")
    a = ler_matriz("A", n, n)
    inv = inversa(a)
    if inv is None:
        print("\nA matriz não possui inversa (determinante igual a zero).")
    else:
        mostrar_matriz(inv, "\nInversa de A =")


# ---------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------
def main():
    execucao = True
    while execucao:
        print("\nQual o tipo de operação que você quer fazer: ")
        print("1 - Soma")
        print("2 - Multiplicação escalar")
        print("3 - Multiplicação")
        print("4 - Transposta")
        print("5 - Inversa")
        print("6 - Sistema linear (SPD / SPI / SI)")
        print("0 - Sair")

        entrada = input("Digite o número da operação: ").strip()
        opcao = int(entrada) if entrada.lstrip("-").isdigit() else -1

        match opcao:
            case 1:
                op_soma()
            case 2:
                op_escalar()
            case 3:
                op_multiplicacao()
            case 4:
                op_transposta()
            case 5:
                op_inversa()
            case 6:
                resolver_sistema()
            case 0:
                execucao = False
                print("Até mais!")
            case _:
                print("Opção inválida para calcular a matriz")


if __name__ == "__main__":
    main()