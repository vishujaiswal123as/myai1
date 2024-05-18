import streamlit as st
from groq import Groq

from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
from rembg import remove
from PIL import Image

# # from pywikihow import search_wikihow
import pyttsx3
import time
import webbrowser
import wikipedia
import os
import speech_recognition as sr

import datetime
import random
import psutil  # for battery
            
# req
# # streamlit
# # langchain
# # langchain-groq
# # python-dotenv

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

# for i in range(len(voices)):
#  print(voices[i].id)
# #  o and 1 is same voices 4 is female zira
# print(voices[1].id)
# print(voices[2].id)

engine.setProperty('voice', voices[4].id)
# engine.setProperty('rate',200)

# def speak(audio):
#    engine.say(audio)
#    engine.runAndWait()

# engine = pyttsx3.init()

def speak(text):
  try:
    global engine

    # Stop the engine if it's still running
    engine.stop()

    # Clear the previous speech buffer
    engine.say("")

    # Convert the text to speech
    engine.say(text)

    # Start the engine's run loop and wait for it to finish
    engine.runAndWait()

    # Wait for any currently running tasks to complete
    engine.idle()
  except:
      pass
    
def takecommand():
    #  It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        st.write("Recognizing...")
        query = r.recognize_google(audio, language='en-in')  # .lower()
        st.write(f"User said: {query}\n")

    except Exception as e:
      #   st.write(e)
        st.write("Say that again please...")

    return query


def wish_me():
    timee = int(time.strftime('%H'))
    # st.write(timee)
    if (5 <= timee and timee < 12):
        speak('Good morning sir')
    elif (12 <= timee and timee < 17):
        speak('Good afternoon sir')
    elif (17 <= timee and timee <= 20):
        speak('Good evening sir')
    else:
        speak('Night time')
    speak('I am a jarvish. please tell me how may i help you')


load_dotenv()

groq_api_key = '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'


def remove_background():
    st.header('Upload Your image for removing background')

    def remove_background_with_rembg(image_path, output_path):
        # Load the image
        input_image = Image.open(image_path)

        # Remove the background
        output_image = remove(input_image)

        # Save the output image
        output_image.save(output_path)
        st.write('Feel free to ask me anything...')
        return output_path

    # Usage
    user_image = st.file_uploader(
        'Upload Image here', type=['png', 'jpg', 'jpeg'])
    if user_image:
        output_path = remove_background_with_rembg(user_image, "output.png")

        if os.path.exists(output_path):
            st.write("Background removed successfully!")
            with open(output_path, "rb") as file:
                st.download_button(label="Download image", data=file,
                                   file_name="my.png", mime="image/png")
        else:
            st.write("Error: The output image does not exist.")


def main():

    st.title("Rock Chat App")

    # Add customization options to the sidebar

    conversational_memory_length = st.sidebar.slider(
        'Conversational memory length:', 1, 10, value=5)

    memory = ConversationBufferWindowMemory(k=conversational_memory_length)

    user_question = st.text_area("Ask a question:")

    if user_question == 'what is my name' or user_question == "what's my name":
        st.write('Your name is vishal')
    elif user_question == 'who made you' or user_question == 'who makes you' or user_question == "who make's you":
        st.write('i made by vishal')
    elif 'remove background' in user_question or 'background remove' in user_question:
        remove_background()
    # session state variable
    else:
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        else:
            for message in st.session_state.chat_history:
                memory.save_context({'input': message['human']}, {
                                    'output': message['AI']})

        # Initialize Groq Langchain chat object and conversation
        groq_chat = ChatGroq(
            groq_api_key=groq_api_key,
            model_name=model
        )

        conversation = ConversationChain(
            llm=groq_chat,
            memory=memory
        )

        if user_question:
            response = conversation(user_question)
            message = {'human': user_question, 'AI': response['response']}
            st.session_state.chat_history.append(message)
            st.write("Chatbot:", response['response'])


def main1(user_question):

    st.title("Rock Chat App")

    # Add customization options to the sidebar

    conversational_memory_length = st.sidebar.slider(
        'Conversational memory length:', 1, 10, value=5)

    memory = ConversationBufferWindowMemory(k=conversational_memory_length)

    # user_question = st.text_area("Ask a question:")

    if user_question == 'what is my name' or user_question == "what's my name":
        st.write('Your name is vishal')
    elif user_question == 'who made you' or user_question == 'who makes you' or user_question == "who make's you":
        st.write('i made by vishal')
    elif 'remove background' in user_question or 'background remove' in user_question:
        remove_background()
    # session state variable
    else:
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        else:
            for message in st.session_state.chat_history:
                memory.save_context({'input': message['human']}, {
                                    'output': message['AI']})

        # Initialize Groq Langchain chat object and conversation
        groq_chat = ChatGroq(
            groq_api_key=groq_api_key,
            model_name=model
        )

        conversation = ConversationChain(
            llm=groq_chat,
            memory=memory
        )

        if user_question:
            response = conversation(user_question)
            message = {'human': user_question, 'AI': response['response']}
            st.session_state.chat_history.append(message)
            st.write("Chatbot:", response['response'])
            
def main2():
    st.title("Rock Chat App")
    if st.button('Run'):
        user_question = takecommand().lower()
        st.write(user_question)
        speak(user_question)
        if user_question == 'what is my name' or user_question == "what's my name" or user_question=='who developed you':
            st.write('Your name is vishal')
        elif "what's the time" ==user_question or "what is the time" ==user_question or "what's the current time" ==user_question:
            wish_me()
        elif user_question == 'who made you' or user_question == 'who makes you' or user_question == "who make's you":
            st.write('i made by vishal')
        elif 'remove background' in user_question and len(user_question)<30 or 'background remove' in user_question and len(user_question)<30:
            remove_background()
        elif ('wikipedia' in user_question):
            speak('Searching Wikipedia.. \njust a moment')
            user_question = user_question.replace('wikipedia', '')
            results = wikipedia.summary(user_question, sentences=2)
            speak(f'According to wikipedia')
            st.write(results)
            speak(results)
        elif ('am i audiable' in user_question or 'can you listen me' in user_question or 'am I audible' in user_question):
            st.write(f'yes')
            speak(f'yes ')
        elif ('where i am currently' in user_question or 'my current location' in user_question):
            st.write(f'you are in your room at present, i think')
            speak(f'you are in your room at present, i think')
        elif ('open youtube' in user_question):
            webbrowser.open('youtube.com')
        elif ('open google' in user_question):
            webbrowser.open('google.com')
        elif ('open whatsappweb' in user_question):
            webbrowser.open('whatsappweb.com')
        elif ('the time' in user_question or 'what\'s the time' in user_question):
            strTime = datetime.datetime.now().strftime("%H:%M")
            speak(f" the time is {strTime}")
        # elif ('activate how to do mode' in user_question or 'activate mode' in user_question):
        #     speak(f'how to do mode is Activated. now what i do')
        #     how = takecommand().lower()
        #     max_result = 1
        #     how_to = search_wikihow(how, max_result)
        #     assert len(how_to) == 1
        #     how_to[0].st.write()
        #     speak(how_to[0].summary)
        elif ('how much bettery' in user_question or 'how much power' in user_question or 'how much power left' in user_question):
            battry = psutil.sensors_battery()
            percentage = battry.percent
            st.write(f'our system has {percentage} percent battery power')
            speak(f'our system has {percentage} percent battery power')
        elif ('play the music' in user_question or 'play music' in user_question or 'open music' in user_question or 'sing a song' in user_question):
            st.write(f'sure ')
            speak(f'sure ')
            music_dir = 'e:\\songs1'
            songs = os.listdir(music_dir)
            rand = random.randint(0, len(songs))
            # st.write(rand)
            os.startfile(os.path.join(music_dir, songs[rand]))
        elif ('next' in user_question or 'song' in user_question):
            count += 1
            music_dir = 'e:\\songs1'
            songs = os.listdir(music_dir)
            # st.write(count+rand)
            if ((rand+count) < len(songs)):
                os.startfile(os.path.join(music_dir, songs[rand+count]))
            else:
                st.write(f'song list is ended')
                speak(f'song list is ended')
        elif ('open browser' in user_question):
            codepath = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
            os.startfile(codepath)
        elif ('open file' in user_question or 'this pc' in user_question):
            codepath = 'C:\\'
            os.startfile(codepath)

        else:
            main1(user_question)


# st.sidebar.title('Select an LLM')
model = st.sidebar.selectbox(
    'Choose a model',
    ['mixtral-8x7b-32768', 'Advance AI', 'Remove Background']
)

if model == 'mixtral-8x7b-32768':
    main()
elif model == 'Remove Background':
    remove_background()
elif model == 'Advance AI':
    model = 'mixtral-8x7b-32768'
    main2()
