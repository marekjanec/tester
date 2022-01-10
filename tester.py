import csv
import json
import random
import tkinter as tk
from tkinter import INSERT, END, HORIZONTAL, WORD
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter.messagebox import showinfo
from types import SimpleNamespace

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
file_loaded = False


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
            s.configure("red.Horizontal.TProgressbar",
                        background=progress_bar_color_list[((100 // amount_question) * counter) % 100])

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


def load_questions(file):
    global amount_question
    global pop_list_question
    global otazky
    global filename
    global file_loaded

    otazky.clear()
    pop_list_question.clear()

    filename = file

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

    file_loaded = True


def load_file():
    file = filedialog.askopenfilename()
    file_root = file.split(".")
    if file_root[len(file_root) - 1] == "json":
        load_saved_tester(file)
    elif file_root[len(file_root) - 1] == "csv":
        load_questions(file)
    else:
        messagebox.showinfo('Warning', 'Zlý formát súboru!')


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
    status_label.config(text="Načíta náhodnú otázku bez opakovania.")
    btn_random_question.config(bg=default_grey_highlight)


def btn_random_question_hover_leave(e):
    status_label.config(text="")
    btn_random_question.config(bg=default_grey)


def btn_in_order_question_hover_enter(e):
    status_label.config(text="Načíta následujúcu otázku.")
    btn_in_order_question.config(bg=default_grey_highlight)


def btn_in_order_question_hover_leave(e):
    status_label.config(text="")
    btn_in_order_question.config(bg=default_grey)


def btn_question_answer_hover_enter(e):
    btn_question_answer.config(bg=green_color_highlight)


def btn_question_answer_hover_leave(e):
    btn_question_answer.config(bg=green_color)


def btn_load_hover_enter(e):
    status_label.config(
        text="Vyber uložený tester v .json alebo otázky v .csv súbore s 2 stĺpcami s headrami\n'otazka' a 'odpoved', prvý stĺpec sú otázky a druhý stĺpec sú odpovede.")

    if file_loaded:
        btn_load.config(bg=green_color_highlight)
    else:
        btn_load.config(bg=strong_red_color_highlight)


def btn_load_hover_leave(e):
    status_label.config(text="")

    if file_loaded:
        btn_load.config(bg=green_color)
    else:
        btn_load.config(bg=strong_red_color)


def btn_new_hover_enter(e):
    status_label.config(
        text="Vytvorenie prázdneho súboru pre otázky.\nPre prácu so súborom je potrebné ho načítať cez tlačidlo 'Load'")
    btn_new.config(bg=green_color_highlight)


def btn_new_hover_leave(e):
    status_label.config(text="")
    btn_new.config(bg=green_color)


def btn_question_add_hover_enter(e):
    status_label.config(
        text="Po načítaní setu otázok môže pridať novú otázku, vypísaním poľa 'Question' a 'Answer'.\nPo stlačení tlačidla 'Add' sa otázka pridá do setu.")
    btn_question_add.config(bg=green_color_highlight)


def btn_question_add_hover_leave(e):
    status_label.config(text="")
    btn_question_add.config(bg=green_color)


def btn_question_delete_hover_enter(e):
    status_label.config(
        text="Aktuálne načítaná otázka v poli 'Question' sa natrvalo vymaže zo setu otázok.\n Vymazanie po stlačeni tlačidla 'Delete' je potrebné ešte potvdiť.")
    btn_question_delete.config(bg=red_color_highlight)


def btn_question_delete_hover_leave(e):
    status_label.config(text="")
    btn_question_delete.config(bg=red_color)


def btn_question_update_hover_enter(e):
    status_label.config(
        text="Aktuálne načítanú otázku s odpoveďou vieme upraviť priamo v poli.\nPo stlačení tlačidla 'Update' sa uloží nová verzia otázky do setu")
    btn_question_update.config(bg=yellow_color_highlight)


def btn_question_update_hover_leave(e):
    status_label.config(text="")
    btn_question_update.config(bg=yellow_color)


def btn_clear_hover_enter(e):
    status_label.config(
        text="Tlačidlo vymaže obsah v poliach 'Question' a 'Answer'.\nOtázka zostane v sete otázok nezmenená.")
    btn_clear.config(bg=orange_color_highlight)


def btn_clear_hover_leave(e):
    status_label.config(text="")
    btn_clear.config(bg=orange_color)


def btn_reset_hover_enter(e):
    status_label.config(
        text="Nanovo načíta set otázok a zresetuje postup v otázkach.")
    btn_reset.config(bg=red_color_highlight)


def btn_reset_hover_leave(e):
    status_label.config(text="")
    btn_reset.config(bg=red_color)


##################################SAVE BEFORE EXIT##########################################
def on_closing():
    res = messagebox.askquestion("Warning", "Chceš uložiť aktuálny stav testera?")
    if res == 'no':
        root.destroy()
    elif res == 'yes':
        save_tester()
        messagebox.showinfo('information', 'Tester sa uložil!')
        root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)


def load_saved_tester(file):
    global file_loaded
    global question_index
    global counter
    global otazky
    global amount_question
    global pop_list_question
    global filename
    global question

    with open(file, "r") as f:
        data = json.load(f)
        saved_tester = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))

        question_index = saved_tester.question_index
        counter = saved_tester.counter
        otazky = saved_tester.otazky
        amount_question = saved_tester.amount_question
        pop_list_question = saved_tester.pop_list_question
        filename = saved_tester.filename
        question = saved_tester.question

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

    pb['value'] = (100 / amount_question) * counter
    value_label['text'] = update_progress_label()

    file_loaded = True


class TesterSave():
    question_index = -1
    counter = 0
    otazky = []
    amount_question = 0
    pop_list_question = []
    filename = ""
    question = []
    file_loaded = False

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


save = TesterSave()


def save_tester():
    global save

    save.question_index = question_index
    save.counter = counter
    save.otazky = otazky
    save.amount_question = amount_question
    save.pop_list_question = pop_list_question
    save.filename = filename
    save.question = question
    save.file_loaded = file_loaded

    file = tk.filedialog.asksaveasfilename(parent=root, defaultextension=".json", initialfile="test_save.json",
                                           title="Nove otazky")
    with open(file, "w") as f:
        json.dump(save.toJSON(), f)


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
s = ttk.Style()
s.theme_use('default')

pb = ttk.Progressbar(root, style="red.Horizontal.TProgressbar", orient='vertical', mode='determinate', length=425)
value_label = ttk.Label(root, background="#F0F0EF", text=update_progress_label(), anchor="center")

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

green_color = "#B6D7A8"
red_color = "#EA9999"
strong_red_color = "#F22672"
orange_color = "#F9CB9C"
yellow_color = "#FFE599"
default_grey = "#F0F0EF"

green_color_highlight = "#99C785"
red_color_highlight = "#E58080"
strong_red_color_highlight = "#D90D58"
orange_color_highlight = "#F7B36E"
yellow_color_highlight = "#FFD966"
default_grey_highlight = "#DADAD8"

progress_bar_color_list = ["#ff0000",
                           "#ff1b00",
                           "#ff2a00",
                           "#ff3500",
                           "#ff3e00",
                           "#ff4700",
                           "#ff4f00",
                           "#ff5600",
                           "#ff5d00",
                           "#ff6300",
                           "#ff6a00",
                           "#ff7000",
                           "#ff7600",
                           "#ff7c00",
                           "#ff8200",
                           "#ff8700",
                           "#ff8d00",
                           "#ff9200",
                           "#ff9800",
                           "#ff9d00",
                           "#ffa200",
                           "#ffa800",
                           "#ffad00",
                           "#ffb200",
                           "#ffb700",
                           "#ffbc00",
                           "#ffc100",
                           "#ffc600",
                           "#ffcb00",
                           "#ffd000",
                           "#ffd500",
                           "#fed900",
                           "#fdde00",
                           "#fce300",
                           "#fae800",
                           "#f9ec00",
                           "#f7f100",
                           "#f6f600",
                           "#f4fa00",
                           "#f2ff00",
                           "#f2ff00",
                           "#f2ff00",
                           "#f2ff00",
                           "#f2ff00",
                           "#f2ff00",
                           "#f2ff00",
                           "#f2ff00",
                           "#f2ff00",
                           "#f2ff00",
                           "#f2ff00",
                           "#f2ff00",
                           "#f2ff00",
                           "#f2ff00",
                           "#f2ff00",
                           "#f2ff00",
                           "#f2ff00",
                           "#f2ff00",
                           "#f2ff00",
                           "#f2ff00",
                           "#f2ff00",
                           "#f2ff00",
                           "#f2ff00",
                           "#efff00",
                           "#ebff00",
                           "#e8ff00",
                           "#e5ff00",
                           "#e1ff00",
                           "#deff00",
                           "#daff00",
                           "#d6ff00",
                           "#d3ff00",
                           "#cfff00",
                           "#cbff00",
                           "#c7ff00",
                           "#c4ff00",
                           "#c0ff00",
                           "#bcff00",
                           "#b7ff00",
                           "#b3ff00",
                           "#afff00",
                           "#abff00",
                           "#a6ff00",
                           "#a2ff00",
                           "#9dff00",
                           "#98ff00",
                           "#93ff00",
                           "#8eff00",
                           "#89ff00",
                           "#84ff00",
                           "#7eff00",
                           "#78ff00",
                           "#72ff00",
                           "#6bff00",
                           "#65ff00",
                           "#5dff00",
                           "#55ff02",
                           "#4cff08",
                           "#41ff0e",
                           "#35ff13",
                           "#24ff17",
                           "#00ff1b"
                           ]

btn_clear = tk.Button(root, text="Clear", bg=orange_color, command=clear)
btn_reset = tk.Button(root, text="Reset", bg=red_color, command=reset)

btn_random_question = tk.Button(root, text="Random", command=random_question)
btn_in_order_question = tk.Button(root, text="Next", command=in_order_question)

btn_question_answer = tk.Button(root, text="Answer", bg=green_color, command=question_answer)

btn_question_update = tk.Button(root, text="Update", bg=yellow_color, command=update_question_answer)
btn_question_add = tk.Button(root, text="Add", bg=green_color, command=add_question_answer)
btn_question_delete = tk.Button(root, text="Delete", bg=red_color, command=delete_question_answer)

btn_load = tk.Button(root, text="Load", bg=strong_red_color, command=load_file)
btn_new = tk.Button(root, text="New", bg=green_color, command=new_question_file)

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

btn_question_answer.bind("<Enter>", btn_question_answer_hover_enter)
btn_question_answer.bind("<Leave>", btn_question_answer_hover_leave)

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
filemenu.add_command(label="Load saved tester", command=load_saved_tester)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=on_closing)
menubar.add_cascade(label="Menu", menu=filemenu)

root.config(menu=menubar)

root.mainloop()
