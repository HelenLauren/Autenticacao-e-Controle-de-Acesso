#Avaliação formativa 01, Segurança da Informação
#Helen Lauren Bonato. BSI 3°período 

import json

#carrega dados de um arquivo JSON
def carregar_dados(nome_arquivo):
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError): #excessao se n achar o arquivo ne
        return {} #retorna erro

#salva os dados no arquivo JSON
def salvar_dados(nome_arquivo, dados):
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, indent=4)

#os arquivos criados e usados 
ARQUIVO_USUARIOS = 'usuarios.json'
ARQUIVO_PERMISSOES = 'permissoes.json'

#carrega os usuarios e as permissoes para os respectivos arquivos
dados_usuarios = carregar_dados(ARQUIVO_USUARIOS)
dados_permissoes = carregar_dados(ARQUIVO_PERMISSOES)

#classe de usuario
class Usuario:
    def __init__(self, nome, senha):
        self.nome = nome
        self.senha = senha  
    
    def autenticar(self):
        return dados_usuarios.get(self.nome) == self.senha #ve se os dados informados sao consistentes

    def cadastrar(self):
        if self.nome in dados_usuarios:
            print("Usuário já existe!")
            return False #retorna falso se ja existir um usuario com mesmo nome
        
         #atribui os valores no arquivo json
        dados_usuarios[self.nome] = self.senha
        dados_permissoes[self.nome] = {"ler": [], "escrever": [], "apagar": []}  #inicia sem permissao obvio

        #salva eles nos arquivos
        salvar_dados(ARQUIVO_USUARIOS, dados_usuarios) 
        salvar_dados(ARQUIVO_PERMISSOES, dados_permissoes)
        return True

#menu de login ou cadastro
usuario_autenticado = None
tentativas = 0  #conta as tentaivas

while tentativas < 5: #enquanto as tentativas forem menor que 5, ele continua o loop (pq comeca com 0).
    opcao = input("MENU:\n1 - Cadastrar\n2 - Entrar\nEscolha: ")
    
    if opcao not in ['1', '2']:
        print("Opção inválida!")
        continue
    
    nome = input("Nome: ")
    senha = input("Senha: ")
    usuario = Usuario(nome, senha) #passa as info para o arquivo
    
    if opcao == '1':
        if usuario.cadastrar(): #cadastro de usuario
            print("Cadastro realizado com sucesso!")
        continue
    
    if usuario.autenticar():
        print(f"Bem-vindo, {nome}.")
        usuario_autenticado = nome  #guarda o nome do usuario auteticado
        break  #sai do loop do menu de login e vai para o menu de permissoes
    else:
        tentativas += 1
        print(f"Usuário ou senha inválidos. Tentativas restantes: {5 - tentativas}")

if tentativas >= 5:
    print("Acesso bloqueado. Muitas tentativas incorretas.")
    exit()  #encerra o programa apos passar as 5 tentativas incorretas

#menu de permissao
while True:
    print("\nOPÇÕES:")
    opcao = input("1 - Ler\n2 - Escrever\n3 - Apagar\n0 - Sair\nEscolha: ")
    
    if opcao == '0': 
        print("Saindo do sistema...")
        break  #encerra pq a pessoa escolheu sair do programa
    
    tipo_acao = {"1": "ler", "2": "escrever", "3": "apagar"}.get(opcao)
    if not tipo_acao:
        print("Opção inválida!")
        continue
    
    arquivo = input("Insira o nome do arquivo que deseja " + tipo_acao + ":")
    
    if arquivo in dados_permissoes[usuario_autenticado][tipo_acao]:
        print("Acesso permitido") #se tiver acesso vai permitir ele
    else:
        print("Acesso negado") #se n tiver ele nega