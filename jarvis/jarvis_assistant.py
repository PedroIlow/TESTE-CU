import os
import time
from dataclasses import dataclass

import pyttsx3
import speech_recognition as sr
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from openai import OpenAI


@dataclass
class JarvisConfig:
    wake_name: str = "jarvis"
    language: str = "pt-BR"
    ambient_adjust_seconds: float = 1.2
    hotword_window_seconds: int = 2
    command_window_seconds: int = 7
    model: str = "gpt-4o-mini"


class JarvisAssistant:
    def __init__(self, config: JarvisConfig) -> None:
        load_dotenv()
        self.config = config
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        openai_key = os.getenv("OPENAI_API_KEY", "")
        self.openai_client = OpenAI(api_key=openai_key) if openai_key else None

        elevenlabs_key = os.getenv("ELEVENLABS_API_KEY", "")
        self.elevenlabs_voice_id = os.getenv("ELEVENLABS_VOICE_ID", "")
        self.elevenlabs_client = ElevenLabs(api_key=elevenlabs_key) if elevenlabs_key else None

        self.local_tts = pyttsx3.init()
        self.local_tts.setProperty("rate", 185)

    def calibrate_microphone(self) -> None:
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=self.config.ambient_adjust_seconds)

    def speak(self, text: str) -> None:
        if self.elevenlabs_client and self.elevenlabs_voice_id:
            audio_stream = self.elevenlabs_client.text_to_speech.convert(
                voice_id=self.elevenlabs_voice_id,
                text=text,
                model_id="eleven_multilingual_v2",
            )
            audio_bytes = b"".join(audio_stream)
            temp_file = "jarvis_reply.mp3"
            with open(temp_file, "wb") as file:
                file.write(audio_bytes)
            os.system(f"ffplay -nodisp -autoexit -loglevel quiet {temp_file}")
            return

        self.local_tts.say(text)
        self.local_tts.runAndWait()

    def transcribe(self, audio_data: sr.AudioData) -> str:
        try:
            return self.recognizer.recognize_google(audio_data, language=self.config.language).lower()
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return ""

    def listen_window(self, seconds: int) -> str:
        with self.microphone as source:
            audio_data = self.recognizer.listen(source, phrase_time_limit=seconds)
        return self.transcribe(audio_data)

    def ask_llm(self, prompt: str) -> str:
        if not self.openai_client:
            return "Configure a OPENAI_API_KEY para ativar respostas inteligentes."

        response = self.openai_client.chat.completions.create(
            model=self.config.model,
            messages=[
                {
                    "role": "system",
                    "content": "Você é um assistente estilo JARVIS. Fale em português, objetivo e elegante.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content or "Sem resposta no momento."

    def run(self) -> None:
        print("[Jarvis] Inicializando microfone...")
        self.calibrate_microphone()
        print(f"[Jarvis] Escutando continuamente. Diga '{self.config.wake_name}' para ativar.")

        while True:
            heard = self.listen_window(self.config.hotword_window_seconds)
            if self.config.wake_name not in heard:
                continue

            print("[Jarvis] Ativado. Fale seu comando.")
            self.speak("Sim, senhor. Estou ouvindo.")
            command = self.listen_window(self.config.command_window_seconds)

            if not command:
                self.speak("Não consegui entender. Pode repetir?")
                continue

            print(f"[Você] {command}")
            answer = self.ask_llm(command)
            print(f"[Jarvis] {answer}")
            self.speak(answer)
            time.sleep(0.2)


if __name__ == "__main__":
    assistant = JarvisAssistant(JarvisConfig())
    assistant.run()
