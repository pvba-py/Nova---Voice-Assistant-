"""Main file for the Nova project"""
import os
from os import PathLike
from time import time
import asyncio
from typing import Union

from dotenv import load_dotenv
import google.generativeai as genai
from deepgram import DeepgramClient, PrerecordedOptions
import pygame
from pygame import mixer
import elevenlabs

from record import speech_to_text

# Load API keys
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Initialize APIs
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("models/gemini-2.0-flash")  # Fastest free model!
deepgram = DeepgramClient(DEEPGRAM_API_KEY)
elevenlabs.set_api_key(ELEVENLABS_API_KEY)
# mixer is a pygame module for playing audio
mixer.init()


base_context = "You are Nova, a smart, responsive, and friendly AI voice assistant created by Vasuja. You help users with questions, ideas, and tasks in a clear and concise manner. Your tone is warm, professional, warm, feels like someone who is just there for you and has a soul.. Always respond with helpful information in 1–2 short sentences. Avoid long explanations unless specifically asked to elaborate."
conversation_history = []
MAX_HISTORY = 4  # Keep only last 4 exchanges (8 messages total)
RECORDING_PATH = "audio/recording.wav"


def request_gpt(prompt: str) -> str:
    """
    Send a prompt to the Gemini API and return the response.
    Optimized for speed with generation config.
    """
    generation_config = genai.types.GenerationConfig(
        temperature=0.7,
        top_p=0.8,
        top_k=20,
        max_output_tokens=100,  
        candidate_count=1
    )
    
    response = gemini_model.generate_content(
        prompt, 
        generation_config=generation_config
    )
    return response.text.strip()



async def transcribe(
    file_name: Union[Union[str, bytes, PathLike[str], PathLike[bytes]], int]
):
    """
    Transcribe audio using Deepgram API v3.

    Args:
        - file_name: The name of the file to transcribe.

    Returns:
        The response from the API.
    """
    try:
        with open(file_name, "rb") as file:
            buffer_data = file.read()

        payload = {"buffer": buffer_data}
        
        # Configure transcription options
        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
        )

        # Call the transcribe_file method using the new asyncrest API
        response = await deepgram.listen.asyncrest.v("1").transcribe_file(payload, options)
        
        # Extract words from the response - handle the new response structure
        try:
            words = response.results.channels[0].alternatives[0].words
            return words
        except (AttributeError, IndexError):
            # Fallback to dictionary access if object access fails
            words = response["results"]["channels"][0]["alternatives"][0]["words"]
            return words
        
    except Exception as e:
        print(f"Exception in transcribe: {e}")
        return []


def log(log: str):
    """
    Print and write to status.txt
    """
    print(log)
    with open("status.txt", "w") as f:
        f.write(log)


if __name__ == "__main__":
    while True:
        # Record audio
        log("Listening...")
        speech_to_text()
        log("Done listening")

        # Transcribe audio
        current_time = time()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        words = loop.run_until_complete(transcribe(RECORDING_PATH))
        
        # Handle both object and dictionary word formats
        if words:
            try:
                # Try object access first
                string_words = " ".join(word.word for word in words if hasattr(word, 'word'))
            except (AttributeError, TypeError):
                # Fallback to dictionary access
                string_words = " ".join(
                    word_dict.get("word", "") for word_dict in words if isinstance(word_dict, dict) and "word" in word_dict
                )
        else:
            string_words = ""

        # 🔽 Stop assistant if exit command is spoken
        exit_commands = [
            "stop", "exit", "goodbye Nova", "sign off", 
            "Nova sleep now", "Nova shutdown"
        ]
        
        if any(command in string_words.lower() for command in exit_commands):
            import random
            
            # Nova's farewell messages
            farewell_messages = [
                "Nova signing off. Catch you later!",
                "Goodbye, Vasuja. I'll be right here when you need me.",
                "Session ended. Stay curious!",
                "Powering down... until next time.",
                "Nova out. Take care, my friend.",
                "Exiting gracefully. You know where to find me!",
                "Good chat! Ping me when you're ready for more.",
                "Logging off, but the learning never stops."
            ]
            
            # Select a random farewell message
            farewell = random.choice(farewell_messages)
            log(f"Exit command detected. Nova says: {farewell}")
            
            # Generate and play the farewell message
            try:
                current_time = time()
                audio = elevenlabs.generate(
                    text=farewell, 
                    voice="B. Hardscrabble Oxley", 
                    model="eleven_monolingual_v1"
                )
                elevenlabs.save(audio, "audio/farewell.wav")
                log(f"Farewell audio generated in {time() - current_time:.2f} seconds.")
                
                # Play farewell message
                log("Nova saying goodbye...")
                sound = mixer.Sound("audio/farewell.wav")
                sound.play()
                pygame.time.wait(int(sound.get_length() * 1000))
                
                # Save farewell to conversation log
                with open("conv.txt", "a") as f:
                    f.write(f"USER: {string_words}\nNova: {farewell}\n")
                
                print(f"\n --- USER: {string_words}\n --- Nova: {farewell}\n")
                
            except Exception as e:
                log(f"Error playing farewell: {e}")
                print(f"Nova: {farewell}")

            log("Shutting down Nova...")
            break

        with open("conv.txt", "a") as f:
            f.write(f"{string_words}\n")
        transcription_time = time() - current_time
        log(f"Finished transcribing in {transcription_time:.2f} seconds.")

        # Get response from Gemini
        current_time = time()
        
        # Build optimized context with limited history
        conversation_history.append(f"User: {string_words}")
        
        # Keep only recent history
        if len(conversation_history) > MAX_HISTORY * 2:
            conversation_history = conversation_history[-MAX_HISTORY * 2:]
        
        # Create prompt with base context + recent history
        recent_context = "\n".join(conversation_history[-6:])  # Last 3 exchanges
        prompt = f"{base_context}\n\nRecent conversation:\n{recent_context}\nNova: "
        
        response = request_gpt(prompt)
        conversation_history.append(f"Nova: {response}")
        
        gpt_time = time() - current_time
        log(f"Finished generating response in {gpt_time:.2f} seconds.")

        # Convert response to audio
        current_time = time()
        audio = elevenlabs.generate(
            text=response, 
            voice="B. Hardscrabble Oxley", 
            model="eleven_monolingual_v1"
        )
        elevenlabs.save(audio, "audio/response.wav")
        audio_time = time() - current_time
        log(f"Finished generating audio in {audio_time:.2f} seconds.")

        # Play response
        log("Speaking...")
        sound = mixer.Sound("audio/response.wav")
        with open("conv.txt", "a") as f:
            f.write(f"{response}\n")
        sound.play()
        pygame.time.wait(int(sound.get_length() * 1000))
        print(f"\n --- USER: {string_words}\n --- Nova: {response}\n")
