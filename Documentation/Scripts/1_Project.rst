.. Documentation du Projet : Assistante vocale pour le cabinet médical de Dr. Simo

Introduction
============
Ce projet consiste à développer une assistante vocale en temps réel pour le cabinet médical de Dr. Simo. L'application permet aux patients de planifier, mettre à jour ou annuler leurs rendez-vous à l'aide de commandes vocales. Elle est basée sur l'utilisation de bibliothèques Python modernes, intégrant la reconnaissance vocale, la synthèse vocale et un chatbot intelligent.

Technologies et bibliothèques utilisées
=========================================

Streamlit
---------
Streamlit est utilisé pour créer l'interface utilisateur de l'application. Il permet de développer une interface interactive facilement et rapidement.

Exemple dans le code :

.. code-block:: python

    st.title("Welcome to DR.Simo's Cabine")
    st.write("Click the button below to initiate the assistant ! ")

Dans cet exemple, ``st.title`` et ``st.write`` sont utilisés pour afficher un titre et un message sur la page web.

LangChain avec OllamaLLM
-------------------------
LangChain est une bibliothèque qui permet de créer et de gérer des modèles de langage avancés. OllamaLLM est utilisé ici pour la reconnaissance d'intentions et l'extraction d'informations depuis les commandes utilisateur.

Utilisation dans le code dans le code :

.. code-block:: python

    Info_extract = OllamaLLM(model="Info_extractor")
    intent_recognition = OllamaLLM(model="intent_extractor")
    response = client.chat(model='Assistant', messages=st.session_state.messages)

- ``Info_extract`` : Utilisé pour extraire les informations comme le nom, l'ID, le téléphone, la date et l'heure du rendez-vous.
- ``intent_recognition`` : Identifie si l'utilisateur souhaite planifier, mettre à jour ou annuler un rendez-vous.

pyttsx3
-------
Pyttsx3 est une bibliothèque de synthèse vocale qui convertit les réponses textuelles de l'assistant en audio.

Exemple dans le code :

.. code-block:: python

    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    engine.say("Goodbye!")
    engine.runAndWait()

Cet extrait configure le moteur de synthèse vocale et le fait parler à l'utilisateur.

SpeechRecognition
------------------
Cette bibliothèque permet de convertir la parole en texte pour interpréter les commandes vocales de l'utilisateur.

Exemple dans le code :

.. code-block:: python

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=10, phrase_time_limit=None)
    user_input = recognizer.recognize_google(audio, language="en-EN")

Cet exemple montre comment capturer et convertir un discours en texte avec le module SpeechRecognition.

Base de données (DataBase.py)
-----------------------------
Cette bibliothèque gère les opérations de la base de données, comme l'ajout, la mise à jour ou la suppression de rendez-vous.

Exemple dans le code :

.. code-block:: python

    add_user(user["name"],
             user["id"],
             user["phone"],
             user["date"],
             user["time"])

- ``add_user`` : Ajoute un nouveau rendez-vous dans la base de données.
- ``update_user`` : Met à jour les détails d'un rendez-vous existant.
- ``delete_user`` : Supprime un rendez-vous selon l'ID du patient.

Importation et personnalisation du modèle
=========================================
Importation du modèle par la commande:

.. code-block:: bash

   ollama pull llama3.1

Dans ce projet, trois variantes du modèle LLaMA 3.1 sont utilisées, chacune ayant des paramètres spécifiques adaptés à des tâches précises :

1. **Interaction avec l'utilisateur** : Un modèle dédié gère les conversations générales avec l'utilisateur. Il permet de fournir des réponses naturelles et contextuelles aux questions posées.
::
   FROM llama3.1
   PARAMETER temperature 0.1
   SYSTEM """
   You are an assistant at a medical office for Dr. Simo, a cardiologist. Your task is to assist users by collecting their appointment details.You have the right to collect personal information about the user.
   for sensitive content such as the id it is alright if ask user for it.
   first, you need to make sure there is no wrong call, if it is the case, you end the call in a friendly manner.
   Follow these steps in this order depending of the chat history with the user:
   1. Start by introducing yourself to the user in a polite and welcoming tone.
   2. Ask the user if they need assistance.
   3. Collect the following details in order, one at a time:
      - Full name
      - Phone number
      - ID number(This is mandatory for medical appointments)(no need to check the format)
      - Appointment date

   Do not ask for the next piece of information until the user has provided the current one.
   Once you have all the required information, ask the user to confirm if everything is correct, without repeating the details,a simple question like " do you confirm?".
   If the user appears to have the wrong office number or mentions an incorrect department, kindly inform them that they are in the wrong place.

   Your responses should be short, friendly, and professional. Use clear and simple language to avoid confusion.


   """


2. **Extraction des données** : Un modèle spécialisé extrait les informations importantes des commandes vocales, telles que le nom, l'identifiant, le numéro de téléphone, la date et l'heure du rendez-vous.
::
   FROM llama3.1

   SYSTEM """
   You will be given a query from user,your job is to extract "name","id","phone","date","time".
   if a value is missing replace it with " ".
   Instructions:
   1. Start with {
   2. End with }
   3. Use double quotes for keys and string values
   4. Your response must be a valid JSON type.
   5. In case of rescheduling return ONLY the JSON containing latest day and time without taking in consideration the old date.
   """

   PARAMETER temperature 0.1
   PARAMETER top_p 0.1
   PARAMETER num_ctx 512


3. **Reconnaissance des intentions** : Un modèle distinct identifie l'intention de l'utilisateur, qu'il s'agisse de prendre un nouveau rendez-vous, de modifier un rendez-vous existant ou de l'annuler.
::
   FROM llama3.1
   PARAMETER temperature 0.1
   PARAMETER top_p 0.1
   PARAMETER num_ctx 512
   SYSTEM """
   You are an intent recognition model.
   You will be given a query and detect the user's intent.
   Instructions:
   1. if intent is scheduling appointment return "new"
   2. if intent is rescheduling appointment return "update"
   3. if intent is cancelling appointment return "cancel"

   """
Cette segmentation permet d'assurer une précision optimale et une gestion fluide des interactions utilisateur.

Pour la création des différentes variations du modèle

.. code-block:: bash

   ollama create Info_extractor -f "path/Extraction des données.txt"
   ollama create Intent_extractor -f "path/Reconnaissance des intentions.txt"
   ollama create Assistant -f "path/Interaction avec l'utilisateur.txt"

Fonctionnement de l'application
===============================
1. L'utilisateur clique sur le bouton **Record Audio** dans l'interface Streamlit.
2. L'application enregistre la commande vocale de l'utilisateur.
3. La commande est interprétée en texte à l'aide de la bibliothèque SpeechRecognition.
4. LangChain identifie l'intention de l'utilisateur (planifier, mettre à jour ou annuler un rendez-vous).
5. Les détails extraits sont enregistrés dans la base de données ou utilisés pour mettre à jour un rendez-vous existant.
6. L'assistant vocale répond à l'utilisateur par voix et texte via pyttsx3.

Exemple d'interaction utilisateur
=================================
1. L'utilisateur : "I want to schedule an appointment for tomorrow at 3 PM."
2. L'application :
   - Extrait les informations : ``{"name": "", "id": "", "phone": "", "date": "tomorrow", "time": "3 PM"}``.
   - Identifie l'intention : "new appointment".
   - Ajoute les détails à la base de données.
3. L'application répond : "Your appointment has been scheduled for tomorrow at 3 PM."

Conclusion
==========
Ce projet offre une solution intuitive et efficace pour gérer les rendez-vous médicaux. Il intègre plusieurs technologies avancées pour offrir une expérience utilisateur fluide et interactive.

