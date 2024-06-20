import json
from tkinter import *
from socket import *
from threading import *
from tkinter import messagebox
from tkinter.ttk import Combobox

class QFrame:
    def __init__(self, frame, question , a, b, c, d, answer):
        self.frame = frame
        self.question = question
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.answer = answer


frames = []
button = None

def create_frame(q, xpos, ypos):
    txt = 'Question'+str(q)+' :'
    answer = StringVar()
    answer.set("")

    frame = Frame(window, width=900, height=80, bg="#F3B5DF")
    frame.place(x=xpos, y=ypos)

    q_label = Label(frame, text=txt, font=("InknutAntiqua Regular", 18 * -1), bg="#F3B5DE")
    q_label.place(x=5.0, y=3.0)

    q_entry = Entry(frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    q_entry.place(x=110, y=3, width=500, height=31.0)

    a_label = Label(frame, text="a:", font=("InknutAntiqua Regular", 18 * -1), bg="#F3B5DE")
    a_label.place(x=5.0, y=40)

    a_entry = Entry(frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    a_entry.place(x=25, y=40, width=150, height=31.0)

    b_label = Label(frame, text="b:", font=("InknutAntiqua Regular", 18 * -1), bg="#F3B5DE")
    b_label.place(x=180.0, y=40)

    b_entry = Entry(frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    b_entry.place(x=200, y=40, width=150, height=31.0)

    c_label = Label(frame, text="c:", font=("InknutAntiqua Regular", 18 * -1), bg="#F3B5DE")
    c_label.place(x=355.0, y=40)

    c_entry = Entry(frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    c_entry.place(x=375, y=40, width=150, height=31.0)

    d_label = Label(frame, text="d:", font=("InknutAntiqua Regular", 18 * -1), bg="#F3B5DE")
    d_label.place(x=530.0, y=40)

    d_entry = Entry(frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    d_entry.place(x=550, y=40, width=150, height=31.0)

    answer_label = Label(frame, text="Answer:", font=("InknutAntiqua Regular", 18 * -1), bg="#F3B5DE")
    answer_label.place(x=710.0, y=40)

    combo = Combobox(frame, textvariable=answer, values=['a', 'b', 'c', 'd'], background='#000000')
    combo.place(x=780.0, y=40.0, width=100.0, height=31.0)
    combo.set("Select")

    frames.append(QFrame(frame, q_entry, a_entry, b_entry, c_entry, d_entry, combo))


def make_frames(number_chosen):
    x = 10
    y = 140
    cnt = 1
    chosen_number = int(number_chosen.get())
    if chosen_number:
        for num in range(0, chosen_number):
            create_frame(cnt, x, y)
            cnt += 1
            y += 85
    button = Button(borderwidth=0, highlightthickness=0, text="Set", fg="#FFFFFF", bg="#000000",command= clicked_set, relief="flat", font=("InriaSans Regular", 25 * -1, "bold"))
    button.place(x=350, y=y+10, width=100.0, height=35.0)
    return button


def refresh(frame_numbers):
    global button
    while frames:
        frame = frames.pop()
        frame.frame.destroy()
    if button:
        button.destroy()
    button = make_frames(frame_numbers)


def handle(client, chosen_number,data):
    client.send(chosen_number.encode('utf-8'))

    json_data = json.dumps(data)  # Serialize the list to JSON format
    # send the JSON-encoded data
    client.send(json_data.encode('utf-8'))



def handle_clients(time, data, students):
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('127.0.0.1', 12345))
    s.listen(5)

    # handle number of students
    for i in range(0, students):
        client, addr = s.accept()
        thread=Thread(target=handle, args=(client, time ,data))
        thread.start()


def clicked_set():
    try:
        questions = []
        data = []
        for frame in frames:
            try:
                q = frame.question.get()
                a = frame.a.get()
                b = frame.b.get()
                c = frame.c.get()
                d = frame.d.get()
                answer1 = frame.answer.get()
                questions.append([q, a, b, c, d, answer1])
            except ValueError:
                messagebox.showerror('Error', 'Please Enter Missed input fields..')

        time = time_entry.get()
        students = int(students_entry.get())
        for question in questions:
            que = ""
            for txt in question:
                que += (txt + '**')
            data.append(que)

        handle_clients(time, data, students)

    except ValueError:
        messagebox.showerror('Error', 'Please Enter Missed input fields..')



window = Tk()

window.geometry("930x650")
window.configure(bg="#F5F4FA")
window.title("Real-Time Quiz")


canvas = Canvas(window, bg="#F9E4F2", height=1000, width=900, highlightthickness=0, relief="ridge")
canvas.pack(side=LEFT, fill=BOTH, expand=True)
""""
yscrollbar = Scrollbar(window, orient="vertical", command=canvas.yview)
yscrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
canvas.configure(yscrollcommand=yscrollbar.set)
canvas.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
"""


canvas.create_text(360.0, 5.0, anchor="nw", text="Hello Professor!", fill="#000000", font=("InriaSans Regular", 20 * -1))
canvas.create_text(350.0, 30.0, anchor="nw", text="Hope you are well", fill="#000000", font=("InriaSans Regular", 20 * -1))

number = ['1', '2','3', '4', '5', '6', '7', '8', '9', '10']
number_chosen = StringVar()
number_chosen.set("0")

canvas.create_text(10.0, 70.0, anchor="nw", text="Lets go to set Quiz", fill="#000000", font=("InriaSans Regular", 20 * -1))
canvas.create_text(10.0, 100.0, anchor="nw", text="Number of Questions: ", fill="#000000", font=("InknutAntiqua Regular", 20 * -1))

canvas.create_text(365.0, 100.0, anchor="nw", text="Time: ", fill="#000000", font=("InknutAntiqua Regular", 20 * -1))
time_entry = Entry(canvas, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
time_entry.place(x=420, y=100, width=150, height=31.0)

canvas.create_text(585.0, 100.0, anchor="nw", text="Number of Students: ", fill="#000000", font=("InknutAntiqua Regular", 20 * -1))
students_entry = Entry(canvas, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
students_entry.place(x=770, y=100, width=150, height=31.0)

combo1 = Combobox(canvas, textvariable= number_chosen, values=number, background='#000000')
combo1.place(x=205.0, y=100.0, width=150.0, height=31.0)
combo1.set("Select")


number_chosen.trace("w", lambda *args: refresh(number_chosen))


window.resizable(True, True)
window.mainloop()
