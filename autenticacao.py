# Avaliação formativa 01, Segurança da Informação
# Helen Lauren Bonato. BSI 3°período 

import json
import getpass

# carrega dados de um arquivo JSON
def carregar_dados(nome_arquivo):
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# salva os dados no arquivo JSON
def salvar_dados(nome_arquivo, dados):
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, indent=4)

# arquivos usados
ARQUIVO_USUARIOS = 'usuarios.json'
ARQUIVO_PERMISSOES = 'permissoes.json'

# carrega os dados
dados_usuarios = carregar_dados(ARQUIVO_USUARIOS)
dados_permissoes = carregar_dados(ARQUIVO_PERMISSOES)

# classe de usuário
class Usuario:
    def __init__(self, nome, senha):
        self.nome = nome
        self.senha = senha

    def autenticar(self):
        usuario = dados_usuarios.get(self.nome)

        if not usuario:
            return False, "Usuário não encontrado."

        if usuario.get('bloqueado', False):
            return False, "🚫 Conta bloqueada permanentemente por excesso de tentativas."

        if usuario['senha'] == self.senha:
            usuario['tentativas'] = 0  # zera as tentativas no login bem-sucedido
            salvar_dados(ARQUIVO_USUARIOS, dados_usuarios)
            return True, "✅ Autenticado com sucesso!"
        else:
            usuario['tentativas'] = usuario.get('tentativas', 0) + 1

            if usuario['tentativas'] >= 3:
                usuario['bloqueado'] = True
                salvar_dados(ARQUIVO_USUARIOS, dados_usuarios)
                return False, "🚫 Conta bloqueada após 3 tentativas inválidas."

            salvar_dados(ARQUIVO_USUARIOS, dados_usuarios)
            tentativas_restantes = 3 - usuario['tentativas']
            return False, f"❌ Senha incorreta. Tentativas restantes: {tentativas_restantes}"

    def cadastrar(self):
        if self.nome in dados_usuarios:
            print("Usuário já existe!")
            return False

        # novo formato com tentativas e bloqueio
        dados_usuarios[self.nome] = {
            'senha': self.senha,
            'tentativas': 0,
            'bloqueado': False
        }

        dados_permissoes[self.nome] = {"ler": [], "escrever": [], "apagar": []}

        salvar_dados(ARQUIVO_USUARIOS, dados_usuarios)
        salvar_dados(ARQUIVO_PERMISSOES, dados_permissoes)
        return True

# menu de login ou cadastro
usuario_autenticado = None

while True:
    print("\n" + "="*40)
    print(" 🔐LOGIN OU CADASTRO".center(40))
    opcao = input("\n1 - Cadastrar\n2 - Entrar\n3 - Sair\nEscolha: ")
    print("\n" + "="*40)
    if opcao not in ['1', '2', '3']:
        print("Opção inválida!")
        continue

    if opcao == '3':
        print("Saindo do sistema...")
        break

    nome = input("\n👤 Nome: ")
    senha = getpass.getpass("\033[1;32m🔑 Senha:\033[m ")
    print("\n" + "="*40)
    usuario = Usuario(nome, senha)

    if opcao == '1':
        if usuario.cadastrar():
            print("✅ Cadastro realizado com sucesso!")
        continue

    autenticado, mensagem = usuario.autenticar()
    print(mensagem)
    if autenticado:
        usuario_autenticado = nome
        break

# menu de permissões
if usuario_autenticado:
    while True:
        print("\n" + "="*40)
        print("📂  MENU DE PERMISSÕES  📂".center(40))
        print("\nOPÇÕES:")
        opcao = input("1 - Ler\n2 - Escrever\n3 - Apagar\n4 - Executar\n5 - Consultar arquivos disponíveis permitidos\n0 - Sair\nEscolha: ")
        print("\n" + "="*40)

        if opcao == '0':
            print("Saindo do sistema...")
            break

        if opcao == '5':
            permissoes_usuario = dados_permissoes.get(usuario_autenticado, {})
            arquivos_com_permissoes = {}

            for acao, arquivos in permissoes_usuario.items():
                for arquivo in arquivos:
                    if arquivo not in arquivos_com_permissoes:
                        arquivos_com_permissoes[arquivo] = []
                    arquivos_com_permissoes[arquivo].append(acao)

            if arquivos_com_permissoes:
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

        arquivo = input("Insira o nome do arquivo que deseja " + tipo_acao + ": ")

        if arquivo in dados_permissoes.get(usuario_autenticado, {}).get(tipo_acao, []):
            print("Acesso permitido")
            if opcao == '4':
                print(f"Executando o arquivo {arquivo}...")
        else:
            print("Acesso negado")
