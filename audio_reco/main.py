# speech recognition script, using google recognization system

# importing the libraries
import speech_recognition as sr
import webbrowser as wb
import deepl as dl
import customtkinter as ctk

# creating the main window
root = ctk.CTk()
ctk.set_appearance_mode("dark")
root.geometry("500x500")
root.title("Speech Recognition Translator")


# path to the text file
path_en = "./text/eng.txt"
path_fr = "./text/fr.txt"
auth_key = "d7f5b7bc-b5b0-b348-4e8f-1958c8223844:fx"
translator = dl.Translator(auth_key)

# getting the audio
def get_audio() :
    global r
    r = sr.Recognizer()
    with sr.Microphone() as source :
        print("say something")
        audio = r.listen(source)
    return audio


# writing the text in the file
def write_text(text, path) :
    with open(path, "w") as f :
        f.write(str(text))


# reading the text from the file
def read_text(path) :
    with open(path, "r") as f :
        return f.read()


# translating the text
def translate_text(text, language="FR") :
    result = translator.translate_text(text, target_lang=language)
    return result


# recognize the audio
def recognize() :
    try :
        audio = get_audio()
        texte = r.recognize_google(audio)
        print(f"I think you said : \n{texte}")
        label = ctk.CTkLabel(root, text=f"I think you said : \n{texte}")
        label.pack()

        # writing the text in the english file
        write_text(texte, path_en)

        # translating the text & showing it
        translated_text = translate_text(texte)
        print(f"Translated text : \n{translated_text}")
        label_translated = ctk.CTkLabel(root, text=f"Translated text : \n{translated_text}")
        label_translated.pack()

        # writing the text in the french file
        write_text(translated_text, path_fr)


    except sr.UnknownValueError :
        print("Oups...Can't understand what you said...")

    except sr.RequestError as e :
        print(f"Error : {e}")


button_recognize = ctk.CTkButton(root, text="START", command=recognize)
button_recognize.pack()

root.mainloop()