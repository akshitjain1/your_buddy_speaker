import pyttsx3
from googletrans import Translator, LANGUAGES
import tkinter as tk
from tkinter import ttk, messagebox

# Supported languages for voice assistants
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'ja': 'Japanese',
    'ko': 'Korean',
    'zh-cn': 'Chinese (Simplified)',
    'ru': 'Russian'
}

def robospeaker():
    def speak_text():
        """
        Function to translate the input text to the selected language and speak it.
        If no language is selected, it auto-detects the language of the input text.
        """
        text = text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Input Error", "Please enter text to speak.")
            return

        target_lang_code = lang_choice.get()
        try:
            # Auto-detect language if no language code is provided
            if not target_lang_code:
                detected_lang = translator.detect(text).lang
                if detected_lang in SUPPORTED_LANGUAGES:
                    target_lang_code = detected_lang
                else:
                    messagebox.showwarning("Language Detection", "Detected language is not supported for speech synthesis.")
                    return

            # Translate the text
            translated = translator.translate(text, dest=target_lang_code)
            translated_text.set(f"Translated Text: {translated.text}")
            engine.say(translated.text)
            engine.runAndWait()
        except Exception as e:
            messagebox.showerror("Translation Error", f"Error: {e}")
            engine.say("Sorry, I couldn't translate that.")
            engine.runAndWait()

    def set_voice():
        """
        Function to set the voice for text-to-speech synthesis based on user selection.
        """
        selected_voice = voice_choice.get()
        if selected_voice.isdigit() and 0 <= int(selected_voice) < len(voices):
            engine.setProperty('voice', voices[int(selected_voice)].id)
            messagebox.showinfo("Voice Selection", "Voice changed successfully!")
        else:
            messagebox.showwarning("Invalid Choice", "Invalid voice selection. Using default voice.")

    # Initialize text-to-speech engine and translator
    engine = pyttsx3.init()
    translator = Translator()

    # Set default properties for the text-to-speech engine
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)

    # Get available voices
    voices = engine.getProperty('voices')

    # Create the main GUI window
    root = tk.Tk()
    root.title("RoboSpeaker")
    root.geometry("500x500")
    root.resizable(False, False)

    # Add a title label
    tk.Label(root, text="RoboSpeaker", font=("Arial", 16, "bold")).pack(pady=10)

    # Add a text input box for the user to enter text
    tk.Label(root, text="Enter text to speak:", font=("Arial", 12)).pack(pady=5)
    text_input = tk.Text(root, height=5, width=50, font=("Arial", 10))
    text_input.pack(pady=5)

    # Add a dropdown to select the target language
    tk.Label(root, text="Select target language (optional):", font=("Arial", 12)).pack(pady=5)
    lang_choice = ttk.Combobox(root, values=[f"{code}: {name}" for code, name in SUPPORTED_LANGUAGES.items()], width=50)
    lang_choice.pack(pady=5)

    def update_lang_code(event):
        """
        Function to update the language code when a language is selected from the dropdown.
        """
        selected = lang_choice.get()
        if ": " in selected:
            lang_code = selected.split(": ")[0]
            lang_choice.set(lang_code)

    lang_choice.bind("<<ComboboxSelected>>", update_lang_code)

    # Add a button to trigger the speak_text function
    tk.Button(root, text="Speak", command=speak_text, font=("Arial", 12), bg="green", fg="white").pack(pady=10)

    # Add a dropdown to select the voice for text-to-speech
    tk.Label(root, text="Available Voices:", font=("Arial", 12)).pack(pady=5)
    voice_choice = ttk.Combobox(root, values=[f"{i}: {voice.name}" for i, voice in enumerate(voices)], width=50)
    voice_choice.pack(pady=5)

    # Add a button to set the selected voice
    tk.Button(root, text="Set Voice", command=set_voice, font=("Arial", 12), bg="blue", fg="white").pack(pady=10)

    # Add a label to display the translated text and make it copyable
    translated_text = tk.StringVar()
    translated_label = tk.Entry(root, textvariable=translated_text, font=("Arial", 12), fg="darkgreen", state="readonly", width=50)
    translated_label.pack(pady=10)

    # Run the main event loop
    root.mainloop()

if __name__ == "__main__":
    robospeaker()


# This code creates a simple GUI application using Tkinter that allows users to input text,
# select a target language for translation, and choose a voice for text-to-speech synthesis.
# It then translates the input text into the selected language and speaks it using the selected voice.
# The application also includes error handling for empty input, unsupported languages, and translation errors.
# The GUI is designed to be user-friendly, with clear labels and buttons for each action.
# The application uses the Google Translate API for translation and pyttsx3 for text-to-speech synthesis.
# The supported languages for translation and speech synthesis are defined in the SUPPORTED_LANGUAGES dictionary.