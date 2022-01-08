import csv
import random
import tkinter as tk
from tkinter import INSERT, END, HORIZONTAL, WORD
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter.messagebox import showinfo

root = tk.Tk()
root.title('Testovac')

w = 460
h = 585

# get screen width and height
ws = root.winfo_screenwidth()  # width of the screen
hs = root.winfo_screenheight()  # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2) - 50

# set the dimensions of the screen
# and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

question_index = -1
counter = 0
delete_index = 0
otazky = []
amount_question = 0
pop_list_question = []
filename = ""
exam_question_list = []
exam_question_amount = 0
exam_score = 0
exam = False
question = []
question_btn_clicked = False


def clear():
    txt_field_question.delete("1.0", "end")
    txt_field_answer.delete("1.0", "end")


def reset():
    clear()
    global counter
    global in_order_index
    global pop_list_question
    global amount_question

    amount_question = len(otazky)

    counter = 0
    in_order_index = -1

    pb['value'] = 0
    value_label['text'] = update_progress_label()

    pop_list_question = otazky.copy()


def random_question():
    global question_index
    global counter
    global question
    global question_btn_clicked

    txt_field_question.delete("1.0", "end")
    txt_field_answer.delete("1.0", "end")

    if len(pop_list_question) == 0:
        return
    else:
        question = random.choice(pop_list_question)
        question_index = pop_list_question.index(question)
        question = pop_list_question[question_index].copy()

        txt_field_question.insert(INSERT, (question[0] + "\n"))

    counter += 1

    question_btn_clicked = True


def in_order_question():
    global question_index
    global counter
    global question
    global question_btn_clicked

    txt_field_question.delete("1.0", "end")
    txt_field_answer.delete("1.0", "end")

    if len(pop_list_question) == 0:
        return
    else:
        question_index = 0

    question = pop_list_question[question_index].copy()
    txt_field_question.insert(INSERT, (pop_list_question[question_index][0] + "\n"))

    counter += 1

    question_btn_clicked = True


def question_answer():
    global question_index
    global question_btn_clicked

    if question_btn_clicked:
        txt_field_answer.insert(INSERT, pop_list_question[question_index][1])
        pop_list_question.pop(pop_list_question.index(pop_list_question[question_index]))

        if pb['value'] < 100:
            pb['value'] = (100 / amount_question) * counter
            value_label['text'] = update_progress_label()

        if counter == amount_question and not exam:
            showinfo(message='Chill time!')

        question_btn_clicked = False


def update_progress_label():
    global counter
    return f"{counter}/{amount_question}"


def update_question_answer():
    global question_index
    global filename

    question = txt_field_question.get(1.0, END)
    answer = txt_field_answer.get(1.0, END)

    otazky[question_index] = [question, answer]

    with open(filename, 'w', newline='', encoding="utf-8") as csvfile:
        fieldnames = ['otazka', 'odpoved']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for element in otazky:
            writer.writerow({'otazka': element[0], 'odpoved': element[1]})

    showinfo(message='Otazka aktualizovana!')


def load_questions():
    global amount_question
    global pop_list_question
    global otazky
    global filename

    otazky.clear()
    pop_list_question.clear()

    filename = filedialog.askopenfilename()

    file = open(filename, encoding="utf-8")
    csvreader = csv.reader(file)
    header = []
    header = next(csvreader)
    otazky = []
    for row in csvreader:
        otazky.append(row)

    file.close()

    amount_question = len(otazky)
    pop_list_question = otazky.copy()

    global btn_load
    btn_load.config(bg="#B6D7A8")
    btn_load.config(text="Loaded")

    global root
    title_text = filename.split("/")
    root.title('Testovac - ' + title_text[len(title_text) - 1])

    btn_clear["state"] = "normal"
    btn_reset["state"] = "normal"
    btn_random_question["state"] = "normal"
    btn_in_order_question["state"] = "normal"
    btn_question_answer["state"] = "normal"
    btn_question_update["state"] = "normal"
    btn_question_add["state"] = "normal"
    btn_question_delete["state"] = "normal"

    amount_question = len(otazky)

    pb['value'] = 0
    value_label['text'] = update_progress_label()


def load_exam():
    global otazky
    filename = filedialog.askopenfilename()

    file = open(filename, encoding="utf-8")
    csvreader = csv.reader(file)
    header = []
    header = next(csvreader)

    for row in csvreader:
        otazky.append(row)

    file.close()

    global es_label_file
    global es_label_questions
    global scala
    label = filename.split("/")
    es_label_file.config(text=label[len(label) - 1])
    es_label_questions.config(text="Number of questions in exam: " + str(len(otazky)))
    scala.config(to=len(otazky))


def add_question_answer():
    global filename

    question = txt_field_question.get(1.0, END)
    answer = txt_field_answer.get(1.0, END)

    otazky.append([question, answer])

    with open(filename, 'w', newline='', encoding="utf-8") as csvfile:
        fieldnames = ['otazka', 'odpoved']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for element in otazky:
            writer.writerow({'otazka': element[0], 'odpoved': element[1]})

    txt_field_question.delete("1.0", "end")
    txt_field_answer.delete("1.0", "end")

    showinfo(message='Otazka pridana!')


def delete_question_answer():
    global filename
    global question

    res = messagebox.askquestion("Warning", "Are you sure?")
    if res == 'no':
        messagebox.showinfo('information', 'Otazka sa nevymazala!')
        return

    otazky.pop(otazky.index(question))

    with open(filename, 'w', newline='', encoding="utf-8") as csvfile:
        fieldnames = ['otazka', 'odpoved']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for element in otazky:
            writer.writerow({'otazka': element[0], 'odpoved': element[1]})

    txt_field_question.delete("1.0", "end")
    txt_field_answer.delete("1.0", "end")

    showinfo(message='Otazka vymazana!')


def new_question_file():
    global filename

    filename = tk.filedialog.asksaveasfilename(parent=root, defaultextension=".csv", initialfile="nove_otazky.csv",
                                               title="Nove otazky")

    with open(filename, 'w', newline='', encoding="utf-8") as csvfile:
        fieldnames = ['otazka', 'odpoved']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()


###########################################HOVER TEXT ON BUTTONS################################################

def btn_random_question_hover_enter(e):
    status_label.config(
        text="Nacita nahodnu otazku bez opakovania.")


def btn_random_question_hover_leave(e):
    status_label.config(text="")


def btn_in_order_question_hover_enter(e):
    status_label.config(
        text="Nacita nasleduju otazku.")


def btn_in_order_question_hover_leave(e):
    status_label.config(text="")


def btn_load_hover_enter(e):
    status_label.config(
        text="Pre nacitanie otazok je potrebne vlozit .csv subor s 2 stlpcami s headrami\n'otazka' a 'odpoved', prvy stlpec su otazky a druhy stlpce su odpovede.")


def btn_load_hover_leave(e):
    status_label.config(text="")


def btn_new_hover_enter(e):
    status_label.config(
        text="Vytvorenie prazdneho suboru pre otazky.\nPre pracu so suborom je potrebneho ho nacitat cez tlacidlo 'Load'")


def btn_new_hover_leave(e):
    status_label.config(text="")


def btn_question_add_hover_enter(e):
    status_label.config(
        text="Po nacitani setu otazok moze pridat novu otazku, vypisanim pola 'Question' a 'Answer'.\nPo stlaceni tlacidla 'Add' sa otazka prida do setu.")


def btn_question_add_hover_leave(e):
    status_label.config(text="")


def btn_question_delete_hover_enter(e):
    status_label.config(
        text="Aktualne nacitana otazka v poli 'Question' sa natrvalo vymaze zo setu otazok.\n Vymazanie po stlaceni tlacidla 'Delete' je potrebne este potvdit.")


def btn_question_delete_hover_leave(e):
    status_label.config(text="")


def btn_question_update_hover_enter(e):
    status_label.config(
        text="Aktualne nacitanu otazku s odpovedou vieme upravit priamo v poli.\nPo stlaceni tlacidla 'Update' sa ulozi nova verzia otazky do setu")


def btn_question_update_hover_leave(e):
    status_label.config(text="")


def btn_clear_hover_enter(e):
    status_label.config(
        text="Tlacidlo vymaze obsah v poliach 'Question' a 'Answer'.\nOtazka zostane v sete otazok nezmenena.")


def btn_clear_hover_leave(e):
    status_label.config(text="")


def btn_reset_hover_enter(e):
    status_label.config(
        text="Nanovo nacita set otazok a zresetuje postup v otazkach.")


def btn_reset_hover_leave(e):
    status_label.config(text="")


###################################EXAM SETTING###########################################
def set_question_amount(val):
    global exam_question_amount
    exam_question_amount = val


def correct_answer():
    global exam_score
    exam_score += 1

    if counter == amount_question:
        showinfo(message='Score: ' + str(exam_score) + "/" + str(amount_question))


def wrong_answer():
    global exam_score
    exam_score += 0

    if counter == amount_question:
        showinfo(message='Score: ' + str(exam_score) + "/" + str(amount_question))


def start_exam():
    global counter
    global in_order_index
    global pop_list_question
    global amount_question
    global exam_question_amount
    global exam_question_list
    global pop_list_question
    global newWindow
    global exam

    exam = True

    if int(exam_question_amount) > 0:
        exam_question_list = random.sample(otazky, int(exam_question_amount))
        amount_question = len(exam_question_list)

        counter = 0
        in_order_index = -1

        pb['value'] = 0
        value_label['text'] = update_progress_label()

        pop_list_question = exam_question_list.copy()
        newWindow.destroy()

        btn_correct = tk.Button(root, text="Correct", bg="#F9CB9C", command=correct_answer)
        btn_wrong = tk.Button(root, text="Wrong", bg="#EA9999", command=wrong_answer)

        btn_correct.place(height=70, width=90, x=290, y=470)
        btn_wrong.place(height=70, width=90, x=195, y=470)

        btn_next_question = tk.Button(root, text="Next", command=in_order_question)

        btn_answer = tk.Button(root, text="Answer", bg="#B6D7A8", command=question_answer)

        btn_next_question.place(height=70, width=90, x=5, y=470)
        btn_answer.place(height=70, width=90, x=100, y=470)

        btn_load.destroy()
        btn_clear.destroy()
        btn_reset.destroy()
        btn_random_question.destroy()
        btn_in_order_question.destroy()

        btn_question_update.destroy()
        btn_question_delete.destroy()
        btn_question_add.destroy()
        btn_new.destroy()

    else:
        messagebox.showinfo('warning', 'Nastav pocet otazok!')


def open_exam_settings():
    global newWindow
    # Toplevel object which will
    # be treated as a new window
    newWindow = tk.Toplevel(root)
    # sets the title of the
    # Toplevel widget
    newWindow.title("Exam setting")

    # sets the geometry of toplevel
    newWindow.geometry("300x200")

    es_btn_load = tk.Button(newWindow, text="Load questions", command=load_exam)
    es_btn_start = tk.Button(newWindow, text="Start", command=start_exam)

    global es_label_file
    global es_label_questions
    es_label_file = tk.Label(newWindow, text="nothing loaded")
    es_label_questions = tk.Label(newWindow, text="Number of questions in exam: 0", anchor="center")

    global scala
    scala = tk.Scale(newWindow, from_=0, to=0, orient=HORIZONTAL, command=set_question_amount)

    es_btn_load.place(height=20, width=100, x=5, y=100)
    es_btn_start.place(height=20, width=200, x=50, y=150)

    es_label_file.place(height=20, width=100, x=105, y=100)
    es_label_questions.place(height=20, width=300, x=0, y=0)

    scala.place(height=40, width=290, x=5, y=40)


########################################PROGRESS BAR###################################################


pb = ttk.Progressbar(root, orient='vertical', mode='determinate', length=425)
value_label = ttk.Label(root, text=update_progress_label(), anchor="center")

pb.place(x=418, y=30)
value_label.place(height=20, width=60, x=400, y=5)

###########################################TEXTFIELDS LABELS################################################


label_question = tk.Label(root, text="Question")
label_answer = tk.Label(root, text="Answer")

label_question.place(height=20, width=200, x=100, y=5)
label_answer.place(height=20, width=200, x=100, y=235)

txt_field_question = tk.Text(root, wrap=WORD)
txt_field_answer = tk.Text(root, wrap=WORD)

txt_field_question.place(height=200, width=390, x=5, y=30)
txt_field_answer.place(height=200, width=390, x=5, y=260)

#########################################BUTTONS#################################################

btn_clear = tk.Button(root, text="Clear", bg="#F9CB9C", command=clear)
btn_reset = tk.Button(root, text="Reset", bg="#EA9999", command=reset)

btn_random_question = tk.Button(root, text="Random", command=random_question)
btn_in_order_question = tk.Button(root, text="Next", command=in_order_question)

btn_question_answer = tk.Button(root, text="Answer", bg="#B6D7A8", command=question_answer)

btn_question_update = tk.Button(root, text="Update", bg="#FFE599", command=update_question_answer)
btn_question_add = tk.Button(root, text="Add", bg="#FFE599", command=add_question_answer)
btn_question_delete = tk.Button(root, text="Delete", bg="#EA9999", command=delete_question_answer)

btn_load = tk.Button(root, text="Load", bg="#F22672", command=load_questions)
btn_new = tk.Button(root, text="New", bg="#B6D7A8", command=new_question_file)

status_label = tk.Label(root, text="", anchor="center")

##########################################BUTTONS DISABLED#################################################
btn_clear["state"] = "disabled"
btn_reset["state"] = "disabled"
btn_random_question["state"] = "disabled"
btn_in_order_question["state"] = "disabled"
btn_question_answer["state"] = "disabled"
btn_question_update["state"] = "disabled"
btn_question_add["state"] = "disabled"
btn_question_delete["state"] = "disabled"
###############################################BUTTONS POSITIONS############################################

btn_clear.place(height=30, width=90, x=290, y=470)
btn_reset.place(height=30, width=90, x=290, y=510)

btn_random_question.place(height=30, width=90, x=5, y=470)
btn_in_order_question.place(height=30, width=90, x=5, y=510)
btn_question_answer.place(height=70, width=90, x=100, y=470)

btn_question_update.place(height=30, width=90, x=195, y=470)
btn_question_delete.place(height=30, width=40, x=245, y=510)
btn_question_add.place(height=30, width=40, x=195, y=510)
btn_load.place(height=30, width=70, x=385, y=470)
btn_new.place(height=30, width=70, x=385, y=510)

status_label.place(height=35, width=450, x=5, y=545)

#########################################BUTTONS BINDING##################################################

btn_random_question.bind("<Enter>", btn_random_question_hover_enter)
btn_random_question.bind("<Leave>", btn_random_question_hover_leave)

btn_in_order_question.bind("<Enter>", btn_in_order_question_hover_enter)
btn_in_order_question.bind("<Leave>", btn_in_order_question_hover_leave)

btn_load.bind("<Enter>", btn_load_hover_enter)
btn_load.bind("<Leave>", btn_load_hover_leave)

btn_new.bind("<Enter>", btn_new_hover_enter)
btn_new.bind("<Leave>", btn_new_hover_leave)

btn_question_update.bind("<Enter>", btn_question_update_hover_enter)
btn_question_update.bind("<Leave>", btn_question_update_hover_leave)

btn_question_add.bind("<Enter>", btn_question_add_hover_enter)
btn_question_add.bind("<Leave>", btn_question_add_hover_leave)

btn_question_delete.bind("<Enter>", btn_question_delete_hover_enter)
btn_question_delete.bind("<Leave>", btn_question_delete_hover_leave)

btn_clear.bind("<Enter>", btn_clear_hover_enter)
btn_clear.bind("<Leave>", btn_clear_hover_leave)

btn_reset.bind("<Enter>", btn_reset_hover_enter)
btn_reset.bind("<Leave>", btn_reset_hover_leave)

###########################################MENU################################################


menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="New exam simulation", command=open_exam_settings)
filemenu.add_command(label="Load .csv", command=load_questions)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Menu", menu=filemenu)

root.config(menu=menubar)

root.mainloop()
