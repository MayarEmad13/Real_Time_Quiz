import json
import time
from tkinter import *
from socket import *
from threading import *
from tkinter import messagebox
from tkinter.ttk import Combobox


def create_frame(q, question, a, b, c, d, xpos, ypos):
    txt = 'Question'+str(q)+' :'
    answer = StringVar()
    answer.set("")

    frame = Frame(window, width=900, height=80, bg="#F3B5DF")
    frame.place(x=xpos, y=ypos)

    q_label = Label(frame, text=txt, font=("InknutAntiqua Regular", 18 * -1), bg="#F3B5DE")
    q_label.place(x=5.0, y=3.0)

    q_entry = Entry(frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    q_entry.place(x=110, y=3, width=500, height=31.0)
    q_entry.insert(0, question)

    a_label = Label(frame, text="a:", font=("InknutAntiqua Regular", 18 * -1), bg="#F3B5DE")
    a_label.place(x=5.0, y=40)

    a_entry = Entry(frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    a_entry.place(x=25, y=40, width=150, height=31.0)
    a_entry.insert(0, a)

    b_label = Label(frame, text="b:", font=("InknutAntiqua Regular", 18 * -1), bg="#F3B5DE")
    b_label.place(x=180.0, y=40)

    b_entry = Entry(frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    b_entry.place(x=200, y=40, width=150, height=31.0)
    b_entry.insert(0, b)

    c_label = Label(frame, text="c:", font=("InknutAntiqua Regular", 18 * -1), bg="#F3B5DE")
    c_label.place(x=355.0, y=40)

    c_entry = Entry(frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    c_entry.place(x=375, y=40, width=150, height=31.0)
    c_entry.insert(0, c)

    d_label = Label(frame, text="d:", font=("InknutAntiqua Regular", 18 * -1), bg="#F3B5DE")
    d_label.place(x=530.0, y=40)

    d_entry = Entry(frame, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    d_entry.place(x=550, y=40, width=150, height=31.0)
    d_entry.insert(0, d)

    answer_label = Label(frame, text="Answer:", font=("InknutAntiqua Regular", 18 * -1), bg="#F3B5DE")
    answer_label.place(x=710.0, y=40)

    combo = Combobox(frame, textvariable=answer, values=['a', 'b', 'c', 'd'], background='#000000')
    combo.place(x=780.0, y=40.0, width=100.0, height=31.0)
    combo.set("Select")

    answers.append(combo)


def clicked_submit():
    cnt = 0
    score = 0
    for combo in answers:
        var = combo.get()
        if var == correct_answers[cnt]:
            score += 1
        cnt += 1
    name = name_entry.get()
    messagebox.showinfo('Congratulations!', name + ', your Score is ' + str(score))

    window.destroy()


def run_timer(timer_label, time_left):
    while time_left > 0:
        time_left -= 1
        update_timer_label(timer_label, time_left)
        time.sleep(1)  # Sleep for 1 second
    clicked_submit()


def update_timer_label(timer_label, time_left):
    timer_label.config(text="Timer: {}".format(time_left))


def timer(t):
    timer_label = Label(canvas, text="Timer: {}".format(t), font=("Arial", 14, "bold"), bg="#F9E4F2")
    timer_label.place(x=800, y=10)
    run_timer(timer_label, t)


def start():
    button.destroy()
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(('127.0.0.1', 12345))
    t = int(s.recv(1024).decode('utf-8'))
    cnt=1
    x = 10
    y = 120

    # receive questions from server
    received_data = s.recv(2048)  # Receive the data
    json_data = received_data.decode('utf-8')
    data = json.loads(json_data)  # Deserialize the JSON data back into a list
    for question in data:
        l = []
        word =""
        flag = False
        for i in range(len(question)-1):
            if flag:
                flag = False
                continue
            if question[i]=='*' and question[i+1]=='*':
                l.append(word)
                word =""
                flag = True
                continue
            word += question[i]
        create_frame(cnt, l[0], l[1], l[2], l[3], l[4], x, y)
        correct_answers.append(l[5])
        y += 85
        cnt +=1

    button1 = Button(borderwidth=0, highlightthickness=0, text="Submit", fg="#FFFFFF", bg="#000000", command=clicked_submit,
                    relief="flat", font=("InriaSans Regular", 25 * -1, "bold"))
    button1.place(x=350, y=y + 10, width=100.0, height=35.0)

    thread = Thread(target=timer , args=(t,))
    thread.start()


answers = []
correct_answers = []
window = Tk()

window.geometry("930x650")
window.configure(bg="#F5F4FA")
window.title("Real-Time Quiz")


canvas = Canvas(window, bg="#F9E4F2", height=1000, width=900, highlightthickness=0, relief="ridge")
canvas.pack(side=LEFT, fill=BOTH, expand=True)


canvas.create_text(370.0, 5.0, anchor="nw", text="Hello dear!", fill="#000000", font=("InriaSans Regular", 20 * -1))
canvas.create_text(340.0, 30.0, anchor="nw", text="Wish you all the best", fill="#000000", font=("InriaSans Regular", 20 * -1))
canvas.create_text(50.0, 55.0, anchor="nw", text="Lets start the Quiz", fill="#000000", font=("InriaSans Regular", 20 * -1))

button = Button(borderwidth=0, highlightthickness=0, text="Start", fg="#FFFFFF", bg="#000000", command=start,  relief="flat", font=("InriaSans Regular", 25 * -1, "bold"))
button.place(x=80, y=80, width=100.0, height=35.0)

canvas.create_text(635.0, 55.0, anchor="nw", text="Name: ", fill="#000000", font=("InriaSans Regular", 20 * -1))

name_entry = Entry(canvas, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
name_entry.place(x=700, y=55, width=200, height=31.0)

window.resizable(True, True)
window.mainloop()

