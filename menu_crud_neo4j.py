from neo4j import GraphDatabase

# Conexão com o banco de dados
uri = "neo4j+s://b48875ec.databases.neo4j.io"
usuario = "neo4j"
senha = "xfAv61-NGfUA3vDPDLszMF6K6GKBJPCEyjSqlttzmso"
driver = GraphDatabase.driver(uri, auth=(usuario, senha))

# Funções de CRUD
def criar_pessoa(tx, nome, idade):
    tx.run("CREATE (p:Pessoa {nome: $nome, idade: $idade})", nome=nome, idade=idade)

def listar_pessoas(tx):
    result = tx.run("MATCH (p:Pessoa) RETURN p.nome AS nome, p.idade AS idade")
    for record in result:
        print(f"{record['nome']} - {record['idade']} anos")

def atualizar_pessoa(tx, nome_antigo, nome_novo, idade_nova):
    tx.run(
        "MATCH (p:Pessoa {nome: $nome_antigo}) "
        "SET p.nome = $nome_novo, p.idade = $idade_nova",
        nome_antigo=nome_antigo, nome_novo=nome_novo, idade_nova=idade_nova
    )

def deletar_pessoa(tx, nome):
    tx.run("MATCH (p:Pessoa {nome: $nome}) DELETE p", nome=nome)

# Menu
def menu():
    while True:
        print("\nMENU CRUD NEO4J")
        print("1 - Criar pessoa")
        print("2 - Listar pessoas")
        print("3 - Atualizar pessoa")
        print("4 - Deletar pessoa")
        print("5 - Sair")

        opcao = input("Escolha uma opção: ")

        with driver.session() as session:
            if opcao == "1":
                nome = input("Nome: ")
                idade = int(input("Idade: "))
                session.write_transaction(criar_pessoa, nome, idade)

            elif opcao == "2":
                session.read_transaction(listar_pessoas)

            elif opcao == "3":
                nome_antigo = input("Nome da pessoa a atualizar: ")
                nome_novo = input("Novo nome: ")
                idade_nova = int(input("Nova idade: "))
                session.write_transaction(atualizar_pessoa, nome_antigo, nome_novo, idade_nova)

            elif opcao == "4":
                nome = input("Nome da pessoa a deletar: ")
                session.write_transaction(deletar_pessoa, nome)

            elif opcao == "5":
                print("Saindo...")
                break

            else:
                print("Opção inválida. Tente novamente.")

# Executar o menu
if __name__ == "__main__":
    menu()