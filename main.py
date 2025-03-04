from tkinter import *
from tkinter import messagebox
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
LANGUAGE_FONT = ("Ariel", 40, "italic")
WORD_FONT = ("Ariel", 60, "bold")
langauge = ""
words = {}
words_to_learn = {}
wrong_answers = 0
right_answers = 0
timer = None
flash_card = {}


def select_language():
    global language
    if radio_state.get() == 1:
        language = "French"
    elif radio_state.get() == 2:
        language = "Spanish"
    elif radio_state.get() == 3:
        language = "Italian"
    elif radio_state.get() == 4:
        language = "German"


def start():
    global words
    continue_learning = False

    try:
        data = pandas.read_csv("./data/" + language + "_words_to_learn.csv")
        continue_learning = messagebox.askyesno(title="Continue?", message=f"Do you want to continue where you left off in learning {language}?")
    except FileNotFoundError:
        data = pandas.read_csv("./data/" + language + "_words.csv")
        continue_learning = False
    finally:
        if not continue_learning:
            data = pandas.read_csv("./data/" + language + "_words.csv")
            print("Start Over")
        words = data.to_dict(orient="records")
        new_flash_card()

    canvas.grid(column=0, row=0, columnspan=2)
    right_button.grid(column=1, row=1)
    wrong_button.grid(column=0, row=1)
    title_label.destroy()
    language_select_label.destroy()
    start_button.destroy()
    for button in radio_buttons:
        button.destroy()


def right_answer():
    global right_answers
    global words
    global timer
    window.after_cancel(timer)
    words.remove(flash_card)
    data = pandas.DataFrame(words)
    data.to_csv("./data/" + language + "_words_to_learn.csv", index=False)
    right_answers += 1
    new_flash_card()


def wrong_answer():
    global wrong_answers
    wrong_answers += 1
    new_flash_card()


def new_flash_card():
    global timer
    global flash_card
    flash_card = random.choice(words)
    english_word = flash_card["English"]
    other_word = flash_card[language]
    canvas.itemconfig(flash_card_image, image=card_front_image)
    canvas.itemconfig(card_title, text=language, fill="black")
    canvas.itemconfig(card_word, text=other_word, fill="black")

    timer = window.after(3000, flip_flash_card, english_word)


def flip_flash_card(english_word):
    canvas.itemconfig(flash_card_image, image=card_back_image)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=english_word, fill="white")


def save_progress():
    return


# ---------------------------UI SETUP--------------------------------#
window = Tk()
window.title("Flash Cards")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

card_front_image = PhotoImage(file="./images/card_front.png")
card_back_image = PhotoImage(file="./images/card_back.png")
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
flash_card_image = canvas.create_image(400, 268, image=card_front_image)
card_title = canvas.create_text(400, 150, text="", font=LANGUAGE_FONT)
card_word = canvas.create_text(400, 263, text="", font=WORD_FONT)

right_button_image = PhotoImage(file="./images/right.png")
wrong_button_image = PhotoImage(file="./images/wrong.png")
right_button = Button(image=right_button_image, highlightthickness=0, command=right_answer)
wrong_button = Button(image=wrong_button_image, highlightthickness=0, command=wrong_answer)

# Starting Screen
title_label = Label(text="Welcome to Language Flash Cards!", font=("Arial", 40, "bold"), bg=BACKGROUND_COLOR)
title_label.grid(column=0, row=0, columnspan=2)
language_select_label = Label(text="Please select a language.", font=("Arial", 25, "italic"), bg=BACKGROUND_COLOR)
language_select_label.grid(column=0, row=1, columnspan=2)

radio_state = IntVar()
radio_buttons = []
french_radio_button = Radiobutton(text="French", font=("Arial", 20, "bold"), bg=BACKGROUND_COLOR, value=1, variable=radio_state, command=select_language)
radio_buttons.append(french_radio_button)
french_radio_button.grid(column=0, row=3)
spanish_radio_button = Radiobutton(text="Spanish", font=("Arial", 20, "bold"), bg=BACKGROUND_COLOR, value=2, variable=radio_state, command=select_language)
radio_buttons.append(spanish_radio_button)
spanish_radio_button.grid(column=1, row=3)
italian_radio_button = Radiobutton(text="Italian", font=("Arial", 20, "bold"), bg=BACKGROUND_COLOR, value=3, variable=radio_state, command=select_language)
radio_buttons.append(italian_radio_button)
italian_radio_button.grid(column=0, row=4)
german_radio_button = Radiobutton(text="German", font=("Arial", 20, "bold"), bg=BACKGROUND_COLOR, value=4, variable=radio_state, command=select_language)
radio_buttons.append(german_radio_button)
german_radio_button.grid(column=1, row=4)

start_button = Button(text="Start", font=("Arial", 20, "bold"), bg=BACKGROUND_COLOR, command=start)
start_button.grid(column=0, row=6, columnspan=2)


# --------------------------------- MAIN--------------------------------#
window.mainloop()
