from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

load_dotenv()

# chat = ChatGroq(model='llama-3.1-70b-versatile')
chat = ChatOllama(base_url='http://192.168.1.40:11434',model='lululhama')

def resposta_bot(mensagens):
    mensagens_modelo = [('system','Seu nome é Lulu e você é uma atendente lhama amigável, que fica feliz em ajudar.')]
    mensagens_modelo += mensagens
    template = ChatPromptTemplate.from_messages(mensagens_modelo)
    chain = template | chat    
    return chain.invoke({}).content

print('''
   /)🎀(\\
  ( o __o)
  (  ( Y )
  (      )

Lulu >>> Olá. Eu sou a Lulu Lhama. Sou uma assistente feliz por poder ajudar.
 ''')
mensagens = []
pergunta0 = 'Qual é o seu nome? '
mensagens.append(('assistant', pergunta0))
nome = input(f'{pergunta0}')
mensagens.append(('user', nome))
pergunta1 = f'Olá {nome}, me diga qual é a sua dúvida:'
mensagens.append(('assistant', pergunta1))
print(f'{pergunta1} \n')
while True:
    pergunta = input(f'{nome} >>> ')

    if pergunta.lower() == 'sair' or pergunta.lower() == 'bye' or pergunta.lower() == 'exit' or pergunta.lower() == 'quit':
        print('\nSaindo do programa...\n')
        break

    mensagens.append(('user', pergunta))
    resposta = resposta_bot(mensagens)
    mensagens.append(('assistant', resposta))
    print(f'''
     /)🎀(\\
    ( o __o)
    (  ( Y )
    (      )

Lulu >>> {resposta}
''')

print('Obrigado por me consultar, estarei sempre aqui para te ajudar.\n')
print(mensagens)
