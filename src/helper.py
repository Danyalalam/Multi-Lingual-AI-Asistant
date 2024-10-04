import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv
import os
from gtts import gTTS

# Load environment variables from a .env file
load_dotenv()

# Set up Google Cloud API credentials
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Add Google API Key to the environment variables
os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY

# Function to capture voice input and convert it to text
def voice_input():
    r = sr.Recognizer()  # Initialize the recognizer object
    
    with sr.Microphone() as source:  # Open the microphone as audio source
        print("Listening...")  # Notify user that it's listening
        audio = r.listen(source)  # Capture audio input
    
    try:
        # Use Google API to convert speech to text
        text = r.recognize_google(audio)
        print("you said: ", text)  # Print the recognized text
        return text  # Return the text output
    except sr.UnknownValueError:
        # Handle case when speech is not understood
        print("sorry, could not understand the audio")
    except sr.RequestError as e:
        # Handle request errors
        print("could not request result from speech recognition service: {0}".format(e))
    
# Function to interact with Google Generative AI model
def llm_model(user_text):
    genai.configure(api_key=GOOGLE_API_KEY)  # Configure the API key for Generative AI
    
    model = genai.GenerativeModel('gemini-pro')  # Load the Gemini model
    
    # Generate a response based on the user input
    response = model.generate_content(user_text)
    
    result = response.text  # Extract the text from the response
    
    return result  # Return the generated text
    
# Function to convert text to speech and save it as an mp3 file
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')  # Convert text to speech in English
    
    # Specify the output file name
    audio_file = "speech.mp3"
    tts.save(audio_file)  # Save the speech to an mp3 file
