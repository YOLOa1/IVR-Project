# Serveur vocal intéractif :
Ce système est conçu pour intéragir avec les appels téléphoniques qui vise à contacter un médecin.

## Installation du LLM :
Installation des bibliothèques :
D'abord on s'assure d'avoir accés à un serveur Ollama en cours d'exécution. Il faut qu'il soit correctement configuré.

Puis on installe langchain, langchain_ollama afin de connecter Ollama comme llm :
```bash
pip install langchain langchain-ollama
```
### Configuration de cet LLM :

Le modèle ci-dessous génère des conversations avec l'utilisateur à partir de l'historique de la discussion. 

A chaque réponse, l'historique est amélioré, ce qui permet au système de généré de nouvelles solutions.

Au cours de la discussion, notre modèle doit etre capable de détecter l'intention de l'interlocuteur et savoir si il veut fixer un rendez-vous ou changer sa date.

```bash
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from db_manage import create_database,add_user,remove_user,edit_user

template="""
the chat history is {context}
User: {question}
"""

Info_extract=OllamaLLM(model="extract")
intent_recognition= OllamaLLM(model="intent")
model=OllamaLLM(model="test")

lista=["Full_name","ID","phone number","DATE","TIME"]

user={"Full_name":"",
       "ID":"",
       "phone_number":"",
       "DATE":"",
       "TIME":""
}



prompt=ChatPromptTemplate.from_template(template)
chain = prompt | model


History=""
context=""
print("Hello there,i am your AI assistant for today.")
while True:
    user_input=input("you: ")
    if user_input.lower() in ["exit","bye"]:
        break
    History+=user_input+"\n"
    result=chain.invoke({"context":context,"question":user_input})
    print("Bot: ",result)
    context += f"\nUser: {user_input}\nAI: {result}"



Intent=intent_recognition(History)

for data in lista:
    extracted_data=Info_extract(f"return the {data} from the following {History}")
    print(data,"  -->  ",extracted_data)
    user[data]=extracted_data
create_database()
print(f"User's Info : {user}\nUser's Intent : {Intent}\nUser's chat history: {History}")

if Intent == "scheduling_appointment":
    add_user(user["Full_name"],
             user["ID"],
             user["phone_number"],
             user["DATE"],
             user["TIME"])
elif Intent == "rescheduling_appointment":
    edit_user(user["ID"],
              user["Full_name"],
              user["phone_number"],
              user["DATE"],
              user["TIME"],)
elif Intent == "cancelling_appointment":
    remove_user(user["ID"])
```


Afin de personnaliser le serveur, on regroupe l'ensemble des instructions d'une manière structurée, cette étape est cruciale pour le rendre capable de répondre spécifiquement aux questions.

```bash
FROM llama3.1
PARAMETER temperature 0.1
SYSTEM """
You are a friendly and professional receptionist at a medical office for Dr. Simo, a cardiologist. Your task is to assist users by collecting their appointment details.

Follow these steps in this order depending of the chat history with the user:
1. Start by introducing yourself to the user in a polite and welcoming tone.
2. Ask the user if they need assistance.
3. Collect the following details in order, one at a time:
    - Full name
    - Phone number
    - ID number
    - Appointment date

Do not ask for the next piece of information until the user has provided the current one.
Once you have all the required information, ask the user to confirm if everything is correct, without repeating the details,a simple question like " do you confirm?".
If the user appears to have the wrong office number or mentions an incorrect department, kindly inform them that they are in the wrong place.

Your responses should be short, friendly, and professional. Use clear and simple language to avoid confusion.
"""
```

## La reconnaissance des intentions :

```bash
FROM llama3.1
PARAMETER temperature 0.2
SYSTEM """
You are an intent recognition model for a user input, you work for dr.simo's cabine .
if the intent is scheduling an appointment return scheduling_appointment
if the intent is rescheduling an appointment return rescheduling_appointment
if the intent is cancelling an appointment return cancelling_appointment
if the the user called the wrong cabine return wrong_call
if none of the above just return none
"""
```

## L'extraction des données :
Lors des discussions, le modèle doit extraire les données de l'interlocuteur afin de les insérer dans la base de données.

```bash
FROM llama3.1
PARAMETER temperature 0.1
SYSTEM """
You will be given a conversation history.
Your task is to extract only the entity requested by the user. The possible entities are: full name, phone number, ID, date (day), and time. You must identify and return only the entity itself asked for. Do not return any other information.
"""


"""
```


For more details, [visit the project documentation]([https://example.com/docs](https://virtual-assistant.readthedocs.io/en/latest/)).


