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
::

    st.title("Welcome to DR.Simo's Cabine")
    st.write("Click the button below to initiate the assistant ! ")

Dans cet exemple, ``st.title`` et ``st.write`` sont utilisés pour afficher un titre et un message sur la page web.

LangChain avec OllamaLLM
-------------------------
LangChain est une bibliothèque qui permet de créer et de gérer des modèles de langage avancés. OllamaLLM est utilisé ici pour la reconnaissance d'intentions et l'extraction d'informations depuis les commandes utilisateur.

Exemple dans le code :
::

    Info_extract = OllamaLLM(model="testox")
    intent_recognition = OllamaLLM(model="intent1")

- ``Info_extract`` : Utilisé pour extraire les informations comme le nom, l'ID, le téléphone, la date et l'heure du rendez-vous.
- ``intent_recognition`` : Identifie si l'utilisateur souhaite planifier, mettre à jour ou annuler un rendez-vous.

pyttsx3
-------
Pyttsx3 est une bibliothèque de synthèse vocale qui convertit les réponses textuelles de l'assistant en audio.

Exemple dans le code :
::

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
::

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=10, phrase_time_limit=None)
    user_input = recognizer.recognize_google(audio, language="en-EN")

Cet exemple montre comment capturer et convertir un discours en texte avec le module SpeechRecognition.

Base de données (DataBase.py)
-----------------------------
Cette bibliothèque gère les opérations de la base de données, comme l'ajout, la mise à jour ou la suppression de rendez-vous.

Exemple dans le code :
::

    add_user(user["name"],
             user["id"],
             user["phone"],
             user["date"],
             user["time"])

- ``add_user`` : Ajoute un nouveau rendez-vous dans la base de données.
- ``update_user`` : Met à jour les détails d'un rendez-vous existant.
- ``delete_user`` : Supprime un rendez-vous selon l'ID du patient.

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

