#Avaliação formativa 01, Segurança da Informação
#Helen Lauren Bonato. BSI 3°período 

import json
import getpass #sugestao do prof para esconder infos no terminal

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
    print("\n" + "="*40)
    print(" 🔐LOGIN OU CADASTRO".center(40))
    opcao = input("\n1 - Cadastrar\n2 - Entrar\n3- Sair\nEscolha: ")
    print("\n" + "="*40)
    if opcao not in ['1', '2', '3']:
        print("Opção inválida!")
        continue

    if opcao == '3': 
        print("Saindo do sistema...")
        break  #encerra pq a pessoa escolheu sair do programa
    nome = input("\n👤 Nome: ")

    senha = getpass.getpass("\033[1;32m🔑 Senha:\033[m ") 
    print("\n" + "="*40)
    usuario = Usuario(nome, senha) #passa as info para o arquivo
    
    if opcao == '1':
        if usuario.cadastrar(): #cadastro de usuario
            print("✅ Cadastro realizado com sucesso!")
        continue
    
    if usuario.autenticar():
        print(f"Bem-vindo, {nome}. Usuário autenticado!")
        usuario_autenticado = nome  #guarda o nome do usuario auteticado
        break  #sai do loop do menu de login e vai para o menu de permissoes
    else:
        tentativas += 1
        print(f"❌ Usuário ou senha inválidos. Tentativas restantes: {5 - tentativas}")

if tentativas >= 5:
    print("🚫 Acesso bloqueado. Muitas tentativas incorretas 🚫")
    exit()  #encerra o programa apos passar as 5 tentativas incorretas

#menu de permissao
while True:
    print("\n" + "="*40)
    print("📂  MENU DE PERMISSÕES  📂".center(40))
    print("\nOPÇÕES:")
    opcao = input("1 - Ler\n2 - Escrever\n3 - Apagar\n4 - Executar\n5 - Consultar arquivos disponíveis permitidos\n0 - Sair\nEscolha: ")
    print("\n" + "="*40)

    if opcao == '0': 
        print("Saindo do sistema...")
        break  #encerra pq a pessoa escolheu sair do programa

    if opcao == '5': 
        permissoes_usuario = dados_permissoes[usuario_autenticado]
        arquivos_com_permissoes = {} #criado um dicionario para armazenar

        for acao, arquivos in permissoes_usuario.items(): #preenche o dicionario com as infos
            for arquivo in arquivos:
                if arquivo not in arquivos_com_permissoes:
                    arquivos_com_permissoes[arquivo] = []
                    arquivos_com_permissoes[arquivo].append(acao)

        if arquivos_com_permissoes: #exibe os arquivos e tb a acao q a pessoa pode fazer
            print("\nArquivos disponíveis e permissões:")
            for arquivo, acoes in arquivos_com_permissoes.items():
                print(f"  📂 {arquivo}: {', '.join(acoes)}")
        else:
            print("\nNenhum arquivo disponível.")

        continue

    tipo_acao = {"1": "ler", "2": "escrever", "3": "apagar", "4": "executar"}.get(opcao)
    if not tipo_acao:
        print("Opção inválida!")
        continue
    
    arquivo = input("Insira o nome do arquivo que deseja " + tipo_acao + ":")
    
    if arquivo in dados_permissoes[usuario_autenticado][tipo_acao]:
        print("Acesso permitido") #se tiver acesso vai permitir ele
        if opcao == '4': #simulando execucao de arquivo caso a pessoa escolha a opcao 4
            print(f"Executando o arquivo {arquivo}...")
    else:
        print("Acesso negado") #se n tiver ele nega