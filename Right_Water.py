from tkinter import *
from tkinter import messagebox
from random import randint, choices
from time import time
import sqlite3
import webbrowser
from playsound import playsound # HINT: Install version 1.2.2

# Database codes
def connect_db():
    conn = sqlite3.connect("record.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS best_record (id INTEGER PRIMARY KEY, player_score)")
    conn.commit()
    conn.close()

def insert_db(record_sco):
    conn = sqlite3.connect("record.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO best_record VALUES (NULL,?)", (record_sco,))
    conn.commit()
    conn.close()

def update_db(record_sco):
    conn = sqlite3.connect("record.db")
    cur = conn.cursor()
    cur.execute("UPDATE best_record SET player_score=? WHERE id=?", (record_sco, 1))
    conn.commit()
    conn.close()

def view_db():
    conn = sqlite3.connect("record.db")
    cur = conn.cursor()
    cur.execute("SELECT player_score FROM best_record WHERE id=?", (1,))
    row = cur.fetchone()
    conn.close()
    return row

# Title and geometry of window
software = Tk()
software.title("Right Water")
software.geometry("480x480")
icon = PhotoImage(file="water-32.png")
software.call("wm", "iconphoto", software._w, icon)
software.configure(background="#26a8ff")

# Dictionaries and lists needed to play the game.
water_consumption = ["Drinking water (dw)", "Washing hands (wh)", "Washing dishes (wd)", "Going to the bathroom (gb)", "Watering trees (wt)"]
pass_dict = {"Drinking water (dw)": "dw", "Washing hands (wh)": "wh", "Washing dishes (wd)": "wd", "Going to the bathroom (gb)": "gb", "Watering trees (wt)": "wt"}
range_dict = {"Drinking water (dw)": [5,10], "Washing hands (wh)": [11,20], "Washing dishes (wd)": [21,30], "Going to the bathroom (gb)": [31,50], "Watering trees (wt)": [51,70]}
problem = ""
password = ""
answer = ""
start_time = 0
points = 0

# This function clears the page for other pages.
def clear_page():
    for child in software.winfo_children():
        child.destroy()

def check_score(new_score):
    record_score = view_db()
    if new_score > record_score[0]:
        update_db(new_score)
        messagebox.showinfo("New record", "Congratulations, you got a new record!")

def github_link():
    playsound("btn1.wav", block=False)
    webbrowser.open("https://github.com/PAIREN1383")

# This function generates the problem and the answer of the problem.
def problem_generator():
    global problem, password, start_time
    if start_time == 0:
        start_time = time()
    consumers = choices(water_consumption, k=3)
    number1 = randint(range_dict[consumers[0]][0], range_dict[consumers[0]][1])
    number2 = randint(range_dict[consumers[1]][0], range_dict[consumers[1]][1])
    number3 = randint(range_dict[consumers[2]][0], range_dict[consumers[2]][1])
    numbers = [number1, number2, number3]
    problem = f"{number1} + {number2} + {number3}"
    strpass = f"{pass_dict[consumers[0]]}{pass_dict[consumers[1]]}{pass_dict[consumers[2]]}"
    password = strpass + f"{sum(numbers)}"

# This function checks the player answer.
def check_answer():
    global problem, password, answer, points, start_time
    if password == answer.get():
        start_playing()
        points += 1
    else:
        end_time = time()
        delta_time = round(end_time - start_time)
        if points == 0:
            score_number = 0
        else:
            score_number = round(((100*points) / (delta_time // points)), 2)
        check_score(score_number)
        clear_page()
        explain = Label(software, bg="#d64e47", font="Georgia 18 italic", text="You lost the game.")
        explain.place(x=10, y=10)
        info = Label(software, justify=LEFT, bg="#d3d3d3", font="Tohama 12 bold", text="Drinking water (dw): 5-10 Lit, \nWashing hands (wh): 11-20 Lit, \nWashing dishes (wd): 21-30 Lit, \nGoing to the bathroom (gb): 31-50 Lit, \nWatering trees (wt): 51-70 Lit")
        info.place(x=10, y=55)
        prob_label = Label(software, bg="#c0fabb", font="Tohama 10 bold", text="problem:")
        prob_label.place(x=10, y=200)
        prob = Label(software, bg="#d3d3d3", font="Tohama 10 bold", text=problem)
        prob.place(x=80, y=200)
        passcode_label = Label(software, bg="#c0fabb", font="Tohama 10 bold", text=f"Code: {password}")
        passcode_label.place(x=10, y=250)
        score_label = Label(software, bg="#c0fabb", font="Tohama 10 bold", text=f"Score: {score_number}, Points: {points}, Elapsed time: {delta_time}s")
        score_label.place(x=10, y=290)
        ok_btn = Button(software, width=15, fg="#fff", bg="#131745", font="Georgia 10", text="Ok", command=start_game)
        ok_btn.place(x=10, y=380)

# The game will start with this function.
def start_playing():
    global problem, answer
    clear_page()
    playsound("btn1.wav", block=False)
    problem_generator()
    explain = Label(software, bg="#90ee90", font="Georgia 18 italic", text="Write the code to win.")
    explain.place(x=10, y=10)
    info = Label(software, justify=LEFT, bg="#d3d3d3", font="Tohama 12 bold", text="Drinking water (dw): 5-10 Lit, \nWashing hands (wh): 11-20 Lit, \nWashing dishes (wd): 21-30 Lit, \nGoing to the bathroom (gb): 31-50 Lit, \nWatering trees (wt): 51-70 Lit")
    info.place(x=10, y=55)
    prob_label = Label(software, bg="#c0fabb", font="Tohama 10 bold", text="problem:")
    prob_label.place(x=10, y=200)
    prob = Label(software, bg="#d3d3d3", font="Tohama 10 bold", text=problem)
    prob.place(x=80, y=200)
    passcode_label = Label(software, bg="#c0fabb", font="Tohama 10 bold", text="Code:")
    passcode_label.place(x=10, y=250)
    answer = Entry(software, font="Tohama 10 bold")
    answer.place(x=60, y=251)
    enter_btn = Button(software, width=15, fg="#fff", bg="#131745", font="Georgia 10", text="Enter", command=check_answer)
    enter_btn.place(x=10, y=380)

# Description of how to play the game.
def about_page():
    clear_page()
    playsound("btn2.wav", block=False)
    intro = Label(software, bg="#add8e6", font="Georgia 18 italic", text="Find the code to win.")
    intro.place(x=10, y=10)
    story = Label(software, justify=LEFT, bg="#fc8e4e", font="Tahoma 10 bold", text="Story of the game: One day water shortage started and the\
    \nhead of the country's water and sewage company said\
    \nthat we are researching to find the best way to deal\
    \nwith water shortage. And this is where your work begins\
    \nand you, as an profational employee, must calculate the\
    \namount of water of your customers in order to provide\
    \nuseful information in the form of code to scientists and\
    \npoliticians to decide on this issue and find the best solution.")
    story.place(x=10, y=55)
    about_txt = Label(software, justify=LEFT, bg="#d3d3d3", font="Tahoma 10 bold", text="How to play?\
    \nWrite the first letters of the activities based on the numbers,\
    \nthen solve the problem and write the answer on the same line.\
    \nYou get points for correct answers. Be careful, time is gold.\n\
    \nExample:\
    \nDrinking water (dw) = 5-10 Lit, Washing dishes (wd)= 21-30 Lit\
    \nProblem: 8+10+21\
    \nCode: 'dwdwwd39'")
    about_txt.place(x=10, y=200)
    link_label = Label(software, bg="#90ee90", font="Tahoma 11 bold", text="Check update or star the project in GitHub:")
    link_label.place(x=10, y=370)
    link_btn = Button(software, width=10, fg="#fff", bg="#131745", font="Georgia 9", text="Link", command=github_link)
    link_btn.place(x=340, y=369)
    back_btn = Button(software, width=20, fg="#fff", bg="#131745", font="Georgia 10", text="Back to menu", command=back_btn_fun)
    back_btn.place(x=10, y=430)

# Get ready before the game starts.
def start_game():
    global start_time, points
    clear_page()
    playsound("btn1.wav", block=False)
    start_time = 0
    points = 0
    if view_db() is None:
        insert_db(0)
    explain = Label(software, bg="#90ee90", font="Georgia 18 italic", text="Write the code to win.")
    explain.place(x=10, y=10)
    info = Label(software, bg="#add8e6", font="Georgia 11 italic", text="Read the 'About' page first.")
    info.place(x=10, y=55)
    about = Button(software, width=8, fg="#fff", bg="#131745", font="Georgia 10", text="About", command=about_page)
    about.place(x=10, y=85)
    player_record = Label(software, bg="#ff7575", font="Tahoma 10 italic bold", text=f"Your record: {view_db()[0]} ")
    player_record.place(x=10, y=170)
    start_btn = Button(software, width=10, fg="#fff", bg="#131745", font="Georgia 10", text="Play", command=start_playing)
    start_btn.place(x=10, y=200)
    back_btn = Button(software, width=20, fg="#fff", bg="#131745", font="Georgia 10", text="Back to menu", command=back_btn_fun)
    back_btn.place(x=10, y=430)

# Menu and main page of the game
def game_menu():
    clear_page()
    weltxt = Label(software, fg="#00008b", bg="#add8e6", font="Georgia 19 bold italic", text="Welcome to the Right Water game.")
    weltxt.place(x=10, y=10)
    start = Button(software, width=15, fg="#fff", bg="#131745", font="Georgia 10", text="Start the game", command=start_game)
    start.place(x=10, y=150)
    about = Button(software, width=8, fg="#fff", bg="#131745", font="Georgia 10", text="About", command=about_page)
    about.place(x=10, y=180)
    quit_game = Button(software, width=8, fg="#fff", bg="#131745", font="Georgia 10", text="Quit", command=software.destroy)
    quit_game.place(x=10, y=210)
    factxt = Label(software, fg="#00008b", bg="#90ee90", font="Georgia 15 bold italic", text="Water \nis \nthe \nsource \nof \nlife.")
    factxt.place(x=10, y=270)
    drop_of_water1 = Label(software, bg="#07d1f5", width=12, height=6)
    drop_of_water1.place(x=350, y=100)
    drop_of_water2 = Label(software, bg="#07d1f5", width=15, height=7)
    drop_of_water2.place(x=250, y=200)
    drop_of_water3 = Label(software, bg="#07d1f5", width=18, height=8)
    drop_of_water3.place(x=150, y=320)

def back_btn_fun():
    playsound("btn1.wav", block=False)
    game_menu()

# Start point
connect_db()
game_menu()
playsound("background-sound.wav", block=False)


if __name__ == "__main__":
    software.mainloop()