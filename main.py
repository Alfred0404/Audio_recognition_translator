# speech recognition script, using google recognization system and deepl api
# UI made with customtkinter

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


# creating the frame
class MyFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # add widgets onto the frame...
        self.label1 = ctk.CTkLabel(self)
        self.label1.grid(row=0, column=0, padx=20)
        self.label2 = ctk.CTkLabel(self)
        self.label2.grid(row=0, column=1, padx=20)
        self.label_text = ctk.CTkLabel(self)
        self.label_text.grid(row=1, column=0, padx=20)
        self.label_translated = ctk.CTkLabel(self)
        self.label_translated.grid(row=1, column=1, padx=20)

        self.label1.configure(text="Text")
        self.label2.configure(text="Translated text")

frame = MyFrame(root)
frame.place(relx=0.5, rely=0.35, anchor="center")


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


def search(input) :
    wb.open_new_tab(f"https://www.google.com/search?q={input}")


# recognize the audio
def recognize() :
    try :
        audio = get_audio()
        texte = r.recognize_google(audio)

        # writing the text in the english file
        if texte :
            write_text(texte, path_en)
            frame.label_text.configure(text=texte)

        # translating the text & showing it
        translated_text = translate_text(texte)

        if translated_text :
            frame.label_translated.configure(text=translated_text)


        # writing the text in the french file
        write_text(translated_text, path_fr)


    except sr.UnknownValueError :
        print("Oups...Can't understand what you said...")

    except sr.RequestError as e :
        print(f"Error : {e}")


search_button = ctk.CTkButton(root, text="SEARCH", command=lambda: search(read_text(path_fr)), width=180)
search_button.place(relx=0.68, rely=0.253, anchor="center")

button_recognize = ctk.CTkButton(root, text="START", command=recognize, width=175)
button_recognize.place(relx=0.315, rely=0.253, anchor="center")

root.mainloop()