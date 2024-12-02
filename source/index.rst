=========================
Serveur Vocal Interactif
=========================

Ce système est conçu pour interagir avec les appels téléphoniques qui visent à contacter un médecin.

Installation du LLM
===================

Installation des bibliothèques
-------------------------------

Assurez-vous d'avoir accès à un serveur Ollama en cours d'exécution et correctement configuré.

Ensuite, installez `langchain`  pour connecter Ollama comme LLM :

.. code-block:: bash

    pip install langchain_ollama 

Configuration du LLM
--------------------

Pour ce projet on utilisera llama3.1, pour cela on doit l'importer sur notre machine en utilisant la commande:
.. code-block:: bash

    ollama pull lama3.1


Le modèle génère des conversations avec l'utilisateur en se basant sur l'historique de la discussion. À chaque réponse, l'historique est enrichi pour permettre au système de proposer des solutions adaptées.

Le modèle détecte l'intention de l'utilisateur, comme fixer, modifier ou annuler un rendez-vous.

.. code-block:: python

   from langchain_ollama import OllamaLLM
   from DataBase import *

   Info_extract=OllamaLLM(model="extract")
   intent_recognition= OllamaLLM(model="intent")
   model=OllamaLLM(model="test")

   User_Data=["Full_name","ID","phone number","DATE","TIME"]

   user={"Full_name":"",
       "ID":"",
       "phone_number":"",
       "DATE":"",
       "TIME":""
   }

   History = ""

   while True:
      user_input = input("You: ")
      if user_input.lower() in ["goodbye","exit", "bye"]:
         print("Bot: Goodbye!")
         break
      History += f"User: {user_input}\n"
      result = model.invoke(History)
      print("Bot:", result)
      History += f"AI: {result}\n"
   
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

Cette variation du modele pour savoir coment agir sur la base de données.
On etudie meme le cas d'un appel erroné dédié a un autre docteur ou autre cabine.

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

Le modèle extrait les données d'apres l'historique de la conversation entre l'assissatnt et le client pour les insérer dans une base de données.

.. code-block:: bash

    FROM llama3.1
    PARAMETER temperature 0.1
    SYSTEM """
    Extract entities like full name, phone number, ID, date, or time from the conversation.
    """

Modification de la base de données
==================================
Pour savoir comment doit--t-on agir sur la base de données on doit savoir l'intention de l'utilisateur;s'il veut bien prendre un rendez-vous,modifier la date d'un rendez-vous existant ou bien annuler son rendez-vous.

.. code-block:: python
   Intent=intent_recognition.invoke(History)

Utiliser une variable `user` pour enregistrer les données de l'utilisateur obtenus par extraction a partir de l'historique de la conversation

.. code-block:: python
   for data in User_Data:
      extracted_data=Info_extract.invoke(f"return the {data} from the following {History}")
      user[data]=extracted_data
Finalement les cas pour lesquels on va agir sur la base de données;

.. code-block:: python
   create_db()

   if Intent == "scheduling_appointment":
      add_user(user["Full_name"],
             user["ID"],
             user["phone_number"],
             user["DATE"],
             user["TIME"])
   elif Intent == "rescheduling_appointment":
      update_user(user["Full_name"],
                user["ID"],
                user["phone_number"],
                user["DATE"],
                user["TIME"],)
   elif Intent == "cancelling_appointment":
      delete_user(user["ID"])
