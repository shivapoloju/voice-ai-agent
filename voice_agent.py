import asyncio
import tempfile
import os
from gtts import gTTS
from logger import setup_logger
import time
import speech_recognition as sr
import queue
import base64

logger = setup_logger(__name__)


class VoiceAgent:
    def __init__(self, default_voice_language="en-US"):
        try:
            os.environ['SDL_AUDIODRIVER'] = 'dummy'

            self._loop = None
            self.temp_dir = tempfile.gettempdir()
            self.recognizer = sr.Recognizer()
            self.current_audio_file = None

            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.energy_threshold = 500
            self.recognizer.pause_threshold = 0.2
            self.recognizer.phrase_threshold = 0.1
            self.recognizer.non_speaking_duration = 0.1

            self.audio_queue = queue.Queue()
            self.is_recording = False
            self.voice_language = default_voice_language

            logger.info("VoiceAgent initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize VoiceAgent: {e}")
            raise RuntimeError(f"VoiceAgent initialization failed: {e}")

    def _get_event_loop(self):
        try:
            return asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop

    def process_voice_command(self, audio_data=None):
        logger.info(
            f"Received audio_data: {audio_data is not None}, "
            f"length: {len(audio_data) if audio_data else 0}"
        )

        if not audio_data:
            logger.error("No audio data received in process_voice_command.")
            return "No audio data received. Please try again."

        try:
            audio_bytes = base64.b64decode(audio_data)

            temp_file = os.path.join(
                self.temp_dir,
                f"voice_input_{int(time.time())}.wav"
            )

            with open(temp_file, 'wb') as f:
                f.write(audio_bytes)

            logger.info(
                f"Saved audio file: {temp_file}, "
                f"size: {os.path.getsize(temp_file)} bytes"
            )

            with sr.AudioFile(temp_file) as source:
                audio = self.recognizer.record(source)

                text = self.recognizer.recognize_google(
                    audio,
                    language=self.voice_language
                )

            try:
                os.unlink(temp_file)
            except Exception as e:
                logger.error(f"Error cleaning up audio file: {str(e)}")

            return text

        except Exception as e:
            logger.error(
                f"Error processing voice command: {str(e)}",
                exc_info=True
            )

            return (
                "Sorry, there was an error processing your "
                "voice input. Please try again."
            )

    def text_to_speech(self, text):
        try:
            if not text:
                logger.warning("Empty text provided for text-to-speech")
                return None

            logger.info(f"Converting text to speech: {text}")

            temp_file = os.path.join(
                self.temp_dir,
                f"tts_{int(time.time())}.mp3"
            )

            tts_lang = self._tts_language()

            tts = gTTS(
                text=text,
                lang=tts_lang,
                slow=False
            )

            tts.save(temp_file)

            with open(temp_file, 'rb') as audio_file:
                audio_data = audio_file.read()

                base64_audio = base64.b64encode(
                    audio_data
                ).decode('utf-8')

            try:
                os.unlink(temp_file)
            except Exception as e:
                logger.error(f"Error cleaning up audio file: {str(e)}")

            return base64_audio

        except Exception as e:
            logger.error(f"Error in text to speech: {str(e)}")
            return None

    def set_language(self, language_code: str):
        self.voice_language = language_code
        logger.info(f"VoiceAgent language set to: {language_code}")

    def _tts_language(self):
        if not self.voice_language:
            return "en"

        language_code = self.voice_language.split('-')[0].lower()

        if language_code in {"en", "hi", "ta"}:
            return language_code

        return "en"

    def get_audio_html(self, text):
        audio_data = self.text_to_speech(text)

        if audio_data:
            return f"""
            <audio controls autoplay>
                <source src="data:audio/mp3;base64,{audio_data}" type="audio/mp3">
                Your browser does not support the audio element.
            </audio>
            """

        return ""
