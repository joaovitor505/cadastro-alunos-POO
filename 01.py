import sqlite3

conexao = sqlite3.connect("alunos.db")
cursor = conexao.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        nota REAL
    )
""")
conexao.commit()

class Aluno:
    def __init__(self, nome, nota):
        self.nome = nome
        self.nota = nota

    def salvar(self):
        cursor.execute(
            "INSERT INTO alunos (nome, nota) VALUES (?, ?)",
            (self.nome, self.nota)
        )
        conexao.commit()

    def situacao(self):
        return "aprovado" if self.nota >= 6 else "reprovado"

while True:

    cont = input(str('voce deseja continuar com o programa? [s/n]')).upper()
    if cont == 'S':
        opcao = input("Você deseja adicionar um nome [1], você deseja ver a nota de um nome já mencionado [2], você deseja alterar a nota [3], ou você deseja excluir algum aluno do banco [4]? ")

        if opcao == '1':
            nome = input("Digite o nome do aluno: ")
            nota = float(input("Digite a nota do aluno: "))
            aluno = Aluno(nome, nota)
            aluno.salvar()
            print("Aluno salvo!")
            print(f'aluno {aluno.situacao()}')

        elif opcao == '2':
            nome_busca = input("Qual aluno você deseja saber a nota? ")

            cursor.execute("SELECT nome, nota FROM alunos WHERE nome = ?", (nome_busca,))
            resultado = cursor.fetchone()

            if resultado:
                print(f"{resultado[0]} tem nota {resultado[1]}")
                aluno = Aluno(resultado[0], resultado[1])
                print(f'{aluno.nome} situação: {aluno.situacao()}')
            else:
                print("Aluno não encontrado.")

        elif opcao == '3':
            nome_alterar = input("Qual aluno você quer alterar a nota? ")
            nova_nota = float(input("Digite a nova nota: "))

            cursor.execute(
                "UPDATE alunos SET nota = ? WHERE nome = ?",
                (nova_nota, nome_alterar)
            )
            conexao.commit()
            print("Nota atualizada!")

        elif opcao == '4':
            nome_apagar = input("Qual aluno você quer apagar? ")

            cursor.execute(
                "DELETE FROM alunos WHERE nome = ?",
                (nome_apagar,)
            )
            conexao.commit()
            print("Aluno apagado!")

        elif opcao == 'delete':
            cursor.execute("DELETE FROM alunos")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='alunos'")
            conexao.commit()
            print("Banco resetado!")

        else:
            print("Opção inválida.")

    elif cont == 'N':
        print('obrigado por ter utilizado o programa')
        break

    else:
        print('Opção invalida.')

conexao.close()