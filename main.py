import questao_1
import questao_2
import questao_3

def main():
    print("=== Menu ===")
    print("1 - Questão 1")
    print("2 - Questão 2")
    print("3 - Questão 3")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        questao_1.run()
    elif opcao == "2":
        questao_2.run()
    elif opcao == "3":
        questao_3.run()
    else:
        print("Opção inválida!")

if __name__ == "__main__":
    main()