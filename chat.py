import os, urllib3
from datetime import datetime
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders import PyPDFLoader
# from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from rich.console import Console
from rich.markdown import Markdown

urllib3.disable_warnings()

load_dotenv()

chat = ChatGroq(model='llama-3.1-70b-versatile')
#chat = ChatOllama(base_url='http://192.168.1.40:11434',model='gemma2')

def resposta_bot(mensagens, documento):
    system = 'Você é um assistente amigável chamado Rodney Lataria.'
    info_adicional = '' if documento == '' else 'Você utiliza as seguintes informações para formular as suas respostas: {informacoes}'
    system_message = system + info_adicional
    mensagens_modelo = [('system', system_message)]
    mensagens_modelo += mensagens
    template = ChatPromptTemplate.from_messages(mensagens_modelo)
    chain = template | chat
    invoke_dict = {} if documento == '' else {'informacoes': documento}
    retorno = chain.invoke(invoke_dict).content
    return retorno

def carrega_site():
    url_site = input('Digite a url do site: ')
    loader = WebBaseLoader(url_site)
    loader.requests_kwargs = {'verify':False}
    lista_documentos = loader.load()
    documento = ''
    for doc in lista_documentos:
        documento += doc.page_content
    return documento

def carrega_pdf():
    caminho = './arquivos'
    print('Conteúdo do diretório:', caminho)
    for arquivo in os.listdir(caminho):
        caminho_arquivo = os.path.join(caminho, arquivo)
        if os.path.isfile(caminho_arquivo):
            print(f'- {arquivo} (Arquivo)')
        elif os.path.isdir(caminho_arquivo):
            print(f'- {arquivo} (Diretório)')
    
    arquivo = input("Digite o nome do arquivo: ")
    caminho_arquivo = os.path.join(caminho, arquivo)
    if os.path.exists(caminho_arquivo):
        print("Caminho do arquivo:", caminho_arquivo)
    else:
        print("Arquivo não encontrado.")

    # caminho_pdf = '/home/fernando/fernando-ribeiro/Asimov_Academy/introducao_python_para_ia/arquivos/RoteiroViagemEgito.pdf'
    loader = PyPDFLoader(caminho_arquivo)
    lista_documentos = loader.load()
    documento = ''
    for doc in lista_documentos:
        documento += doc.page_content
    return documento

def carrega_video():
    url = input('Digite a url do vídeo: ')
    loader = YoutubeLoader.from_youtube_url(url, language=['pt'])
    lista_documentos = loader.load()
    documento = ''
    for doc in lista_documentos:
        documento += doc.page_content
    return documento

def prompt():
    ''' 
    Função para receber o prompt do usuário e fazer a 
    requisição ao chat com o prompt fornecido
    '''
    try:
        texto_selecao = '''
        ───████████───
        ──▐▀▀▀▀▀▀▀▀▌──
        ─▐▐  ▀  ▀  ▌▌─
        ──▐──▄▄▄▄──▌──
        ──▐  █▄▄█  ▌──
        
        Bem vindo ao ChatBot. 
        
        Digite "0" para não adicionar informação
        Digite "1" para conversar adicionar um site
        Digite "2" para conversar adicionar um pdf
        Digite "3" para conversar adicionar um vídeo do Youtube
        '''
        while True:    
            selecao = input(texto_selecao)
            if selecao == '0':
                documento = ''
                break
            if selecao == '1':
                documento = carrega_site()
                break
            if selecao == '2':
                documento = carrega_pdf()
                break
            if selecao == '3':
                documento = carrega_video()
                break
            print('Digite uma opção válida (1, 2 ou 3) ')
        print('🤖 Como posso te ajudar? \n')

        mensagens = []
        while True:
            pergunta = input(f'[x: sair]\n🙂 >>> ')

            if pergunta.lower() == 'x':
                print('\nSaindo do programa...\n')
                break
            
            if pergunta.lower() == 'r':
                main()
                break

            mensagem = ('user', pergunta)
            mensagens.append(mensagem)
            history(mensagem);
            resposta = resposta_bot(mensagens, documento)
            mensagem = ('assistant', resposta)
            mensagens.append(mensagem)
            history(mensagem);
            print(f'🤖 >>> \n')
            console = Console()
            markdown = Markdown(resposta)
            console.print(markdown)
            print('\n')

        print('Obrigado por me consultar, estarei sempre aqui para te ajudar. 🤖\n')
    except KeyboardInterrupt:
        print("Sinal de interrupção recebido. Encerrando...")

def history(tupla):    
    try:
        now = datetime.now()
        data_hora = now.strftime('%Y-%m-%d %H:%M:%S')
        data = now.strftime('%Y-%m-%d')
        caminho_do_arquivo = f'./history_{data}.txt'
        # Abre o arquivo no modo 'w' (write), que sobrescreve o arquivo se já existir
        with open(caminho_do_arquivo, 'a') as arquivo:
            # Escreve a variável no arquivo
            arquivo.write(data_hora + ' : ' + str(tupla) + '\n')
    except Exception as e:
        print(f"Ocorreu um erro ao escrever o arquivo: {e}")

def main():
    '''
    Função principal que inicia o programa 
    '''
    os.system('clear')    
    prompt()


if __name__ == '__main__':
    main()