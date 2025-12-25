import speech_recognition as sr
from loggin.logger import setup_logger

logging = setup_logger(__name__)


def listen() -> str | None:
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        logging.info("Listening...")

        recognizer.pause_threshold = 1
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language="en-IN")

        print(f"User said: {query}")
        logging.info(f"User said: {query}")

        return query

    except sr.UnknownValueError:
        print("Could not understand audio")
        logging.warning("Speech not understood")
        return None

    except sr.RequestError as e:
        print("Speech service error")
        logging.error(f"Speech Recognition request failed: {e}")
        return None
