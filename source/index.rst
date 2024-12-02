=========================
Serveur Vocal Interactif
=========================

Ce système est conçu pour interagir avec les appels téléphoniques qui visent à contacter un médecin.

Installation du LLM
===================

Installation des bibliothèques
-------------------------------

Assurez-vous d'avoir accès à un serveur Ollama en cours d'exécution et correctement configuré.

Ensuite, installez `langchain` et `langchain_ollama` pour connecter Ollama comme LLM :

.. code-block:: bash

    pip install langchain langchain-ollama

Configuration du LLM
--------------------

Le modèle génère des conversations avec l'utilisateur en se basant sur l'historique de la discussion. À chaque réponse, l'historique est enrichi pour permettre au système de proposer des solutions adaptées.

Le modèle détecte l'intention de l'utilisateur, comme fixer, modifier ou annuler un rendez-vous.

.. code-block:: python

    from langchain_ollama import OllamaLLM
    from langchain_core.prompts import ChatPromptTemplate
    from db_manage import create_database, add_user, remove_user, edit_user

    template = """
    The chat history is {context}
    User: {question}
    """

    Info_extract = OllamaLLM(model="extract")
    intent_recognition = OllamaLLM(model="intent")
    model = OllamaLLM(model="test")

    lista = ["Full_name", "ID", "phone number", "DATE", "TIME"]
    user = {
        "Full_name": "",
        "ID": "",
        "phone_number": "",
        "DATE": "",
        "TIME": ""
    }

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    History = ""
    context = ""
    print("Hello there, I am your AI assistant for today.")
    while True:
        user_input = input("you: ")
        if user_input.lower() in ["exit", "bye"]:
            break
        History += user_input + "\n"
        result = chain.invoke({"context": context, "question": user_input})
        print("Bot: ", result)
        context += f"\nUser: {user_input}\nAI: {result}"

    Intent = intent_recognition(History)

    for data in lista:
        extracted_data = Info_extract(f"Return the {data} from the following {History}")
        print(data, "  -->  ", extracted_data)
        user[data] = extracted_data

    create_database()
    print(f"User's Info: {user}\nUser's Intent: {Intent}\nUser's Chat History: {History}")

    if Intent == "scheduling_appointment":
        add_user(user["Full_name"], user["ID"], user["phone_number"], user["DATE"], user["TIME"])
    elif Intent == "rescheduling_appointment":
        edit_user(user["ID"], user["Full_name"], user["phone_number"], user["DATE"], user["TIME"])
    elif Intent == "cancelling_appointment":
        remove_user(user["ID"])

Personnalisation du Serveur
---------------------------

Les instructions pour personnaliser le serveur sont structurées de manière à rendre le système capable de répondre spécifiquement aux questions.

.. code-block:: bash

    FROM llama3.1
    PARAMETER temperature 0.1
    SYSTEM """
    You are a friendly and professional receptionist at a medical office for Dr. Simo, a cardiologist. Your task is to assist users by collecting their appointment details.

    1. Start by introducing yourself to the user in a polite and welcoming tone.
    2. Ask the user if they need assistance.
    3. Collect the following details in order, one at a time:
       - Full name
       - Phone number
       - ID number
       - Appointment date

    Confirm details at the end.
    """

Reconnaissance des Intentions
=============================

.. code-block:: bash

    FROM llama3.1
    PARAMETER temperature 0.2
    SYSTEM """
    You are an intent recognition model for a user input, working for Dr. Simo's office.
    - Scheduling an appointment: scheduling_appointment
    - Rescheduling: rescheduling_appointment
    - Cancelling: cancelling_appointment
    - Wrong call: wrong_call
    """

Extraction des Données
======================

Le modèle extrait les données de l'utilisateur pour les insérer dans une base de données.

.. code-block:: bash

    FROM llama3.1
    PARAMETER temperature 0.1
    SYSTEM """
    Extract entities like full name, phone number, ID, date, or time from the conversation.
    """
