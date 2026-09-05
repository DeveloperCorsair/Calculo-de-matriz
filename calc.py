listaLinhaA = [int(i) for i in input("Digite um número para representar as linhas da matriz A: ").split(",")]
listaColunaA = [int(i) for i in input("Digite um número para representar as colunas da matriz A: ").split(",")]
listaLinhaB = [int(i) for i in input("Agora, outro número para representar as linhas da matriz B: ").split(",")]
listaColunaB = [int(i) for i in input("Agora, outro número para representar as colunas da matriz B: ").split(",")]

execucao = True

while execucao:
    print("\nQual o tipo de operação que você quer fazer: ")
    print("Soma")
    print("1 - Soma")
    print("2 - Multiplicação escalar")
    print("3 - Multiplicação")
    print("4 - Transporta")
    print("5 - Inversa")

    opcao = int(input("Digite o número da operação: "))

    if opcao == 4 or opcao == 5 and listaLinhaA != listaColunaA or listaLinhaB != listaColunaB:
        print("Para uma matriz ser determinante ou inversa precisa ser uma matriz quadrada")

    if opcao == 4 or opcao == 5 and listaLinhaA != listaLinhaB or listaColunaA != listaColunaB:
        print("Precisa ser uma matriz quadrada")

    match opcao:
        case 1:                
            print( "Vou calcular a soma das matrizes")
            break
        case 2:
            print("Vou calcular a multiplicacão de uma matriz por escalar")
            break
        case 3:
            print("Vou calcular a multiplicação das matrizes")
            break
        case 4:
           print("Vou calcular a transporta da matriz")
           break
        case 5:
            print("Vou calcular a inversa")
            break
        case 0:
            execucao = False
            print("Até mais!")
            break
        case _:
            print("Opção inválida para calcular a matriz")
    
