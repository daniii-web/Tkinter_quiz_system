# quiz.py
# Philippine History Quiz - a Tkinter quiz application
# 10 questions | 15-second timer | answer review | saved high score | restart

import tkinter as tk
from tkinter import messagebox
import random
import os

#LIST OF QUESTIONS
QUESTIONS = [
    {
        "question": "Who led the first circumnavigation expedition that reached the Philippines in 1521?",
        "choices": ["A. Ferdinand Magellan", "B. Christopher Columbus", "C. Vasco da Gama", "D. John Cabot"],
        "answer": "A"
    },
    {
        "question": "What is the capital city of the Philippines?",
        "choices": ["A. Cebu", "B. Davao", "C. Manila", "D. Quezon City"],
        "answer": "C"
    },
    {
        "question": "Which Philippine hero is known as the 'Father of the Philippine Revolution'?",
        "choices": ["A. Andres Bonifacio", "B. Jose Rizal", "C. Emilio Aguinaldo", "D. Apolinario Mabini"],
        "answer": "A"
    },
    {
        "question": "What is the national language of the Philippines?",
        "choices": ["A. English", "B. Filipino", "C. Spanish", "D. Cebuano"],
        "answer": "B"
    },
    {
        "question": "Which Philippine island is known for its Chocolate Hills?",
        "choices": ["A. Palawan", "B. Bohol", "C. Boracay", "D. Mindoro"],
        "answer": "B"
    },
    {
        "question": "Who defeated Ferdinand Magellan at the Battle of Mactan?",
        "choices": ["A. Lapu-Lapu", "B. Juan de Salcedo", "C. Martin de Goiti", "D. Miguel Lopez de Legazpi"],
        "answer": "A"
    },
    {
        "question": "Which three priests were executed in 1872, an event that inspired the Philippine nationalist movement?",
        "choices": ["A. Illustrados", "B. Katipunan", "C. Propagandists", "D. Gomburza"],
        "answer": "D"
    },
    {
        "question": "Which Philippine national hero wrote 'Noli Me Tangere' and 'El Filibusterismo'?",
        "choices": ["A. Andres Bonifacio", "B. Jose Rizal", "C. Emilio Aguinaldo", "D. Apolinario Mabini"],
        "answer": "B"
    },
    {
        "question": "Which Philippine president declared Martial Law in 1972?",
        "choices": ["A. Ferdinand Marcos Sr.", "B. Corazon Aquino", "C. Gloria Macapagal Arroyo", "D. Rodrigo Duterte"],
        "answer": "A"
    },
    {
        "question": "What is the traditional Filipino martial art that focuses on stick fighting?",
        "choices": ["A. Judo", "B. Taekwondo", "C. Arnis", "D. Karate"],
        "answer": "C"
    }
]

TIME_LIMIT = 15  # seconds per question
HIGH_SCORE_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "high_score.txt"
)

# Colors (inspired from the Philippine flag)
BG_COLOR = "#FFF8E7"
BLUE = "#0038A8"
RED = "#CE1126"
YELLOW = "#FCD116"
CORRECT_COLOR = "#2E7D32"
WRONG_COLOR = RED

root = tk.Tk()
root.title("Philippine History Quiz")
root.geometry("750x690")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

#QUIZ STATE VARIABLES
quiz_questions = []      
current_question = 0     
score = 0
time_left = TIME_LIMIT
wrong_answers = []       
timer_job = None         
answered = False         
selected_answer = tk.StringVar()   
name_var = tk.StringVar()          
player_name = ""                   
MAX_NAME_LENGTH = 15

timer_label = None
feedback_label = None
submit_button = None
next_button = None
choice_buttons = []

BG_IMAGE_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "background.png"
)
bg_image = tk.PhotoImage(file=BG_IMAGE_FILE)  
bg_label = tk.Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

main_frame = tk.Frame(root, bg=BG_COLOR, highlightbackground=BLUE,
                      highlightthickness=3)
main_frame.place(relx=0.5, rely=0.5, anchor="center", width=640, height=590)

# HIGH SCORE FUNCTIONS
def get_high_score():
    """Read the saved high score. Return 0 if there is no valid file."""
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, "r") as file:
                return int(file.read().strip())
        except ValueError:
            return 0
    return 0

def save_high_score(new_score):
    """Save the score only if it beats the old high score."""
    if new_score > get_high_score():
        with open(HIGH_SCORE_FILE, "w") as file:
            file.write(str(new_score))
        return True
    return False


# HELPER FUNCTIONS
def clear_screen():
    """Remove every widget from the main frame."""
    for widget in main_frame.winfo_children():
        widget.destroy()

def get_choice_text(question, letter):
    """Return the full choice text (for example 'B. Filipino') from a letter."""
    for choice in question["choices"]:
        if choice.startswith(letter + "."):
            return choice
    return "No answer"


# SCREENS
def show_start_screen():
    clear_screen()
    tk.Label(main_frame, text="Philippines Quiz",
             font=("Georgia", 30, "bold"),
             bg=BG_COLOR, fg=BLUE).pack(pady=(50, 10))
    tk.Label(main_frame,
             text=f"{len(QUESTIONS)} questions  |  {TIME_LIMIT} seconds per question",
             font=("Arial", 13), bg=BG_COLOR).pack(pady=5)
    tk.Label(main_frame,
             text=f"High Score: {get_high_score()} / {len(QUESTIONS)}",
             font=("Arial", 16, "bold"), bg=BG_COLOR, fg=RED).pack(pady=15)

    # Name entry (my added feature)
    tk.Label(main_frame, text="Enter your name:", font=("Arial", 13),
             bg=BG_COLOR).pack(pady=(10, 3))
    name_entry = tk.Entry(main_frame, textvariable=name_var,
                          font=("Arial", 15), width=20, justify="center")
    name_entry.pack(pady=5)
    name_entry.focus_set()
    name_entry.bind("<Return>", lambda event: begin_quiz())

    tk.Button(main_frame, text="Start Quiz", font=("Arial", 16, "bold"),
              bg=BLUE, fg="white", width=15,
              command=begin_quiz).pack(pady=20)

def begin_quiz():
    """Check the typed name, save it, then start the quiz."""
    global player_name
    name = name_var.get().strip()[:MAX_NAME_LENGTH]
    if name == "":
        messagebox.showwarning("Name needed", "Please enter your name first.")
        return
    player_name = name
    start_quiz()

def start_quiz():
    """Reset everything and shuffle the questions."""
    global quiz_questions, current_question, score, wrong_answers
    quiz_questions = random.sample(QUESTIONS, len(QUESTIONS))
    current_question = 0
    score = 0
    wrong_answers = []
    show_question()

def show_question():
    global time_left, answered, timer_label, feedback_label
    global submit_button, next_button, choice_buttons

    clear_screen()
    answered = False
    selected_answer.set("")         
    time_left = TIME_LIMIT
    question = quiz_questions[current_question]

    # Progress and timer
    top_frame = tk.Frame(main_frame, bg=BG_COLOR)
    top_frame.pack(fill="x")
    tk.Label(top_frame,
             text=f"Question {current_question + 1} of {len(quiz_questions)}",
             font=("Arial", 13, "bold"), bg=BG_COLOR, fg=BLUE).pack(side="left")
    timer_label = tk.Label(top_frame, text="", font=("Arial", 13, "bold"),
                           bg=BG_COLOR)
    timer_label.pack(side="right")

    tk.Label(main_frame, text=f"Player: {player_name}   |   Score: {score}",
             font=("Arial", 12), bg=BG_COLOR).pack(anchor="w", pady=(5, 0))

    # Question text
    tk.Label(main_frame, text=question["question"],
             font=("Arial", 18, "bold"), wraplength=620, justify="left",
             bg=BG_COLOR).pack(pady=25, anchor="w")

    # Answer choices
    choice_buttons = []
    for choice in question["choices"]:
        letter = choice[0]        
        button = tk.Radiobutton(main_frame, text=choice,
                                variable=selected_answer, value=letter,
                                font=("Arial", 14), bg=BG_COLOR,
                                activebackground=BG_COLOR, anchor="w")
        button.pack(fill="x", pady=4)
        choice_buttons.append(button)

    feedback_label = tk.Label(main_frame, text="", font=("Arial", 13, "bold"),
                              bg=BG_COLOR, wraplength=620)
    feedback_label.pack(pady=15)

    button_frame = tk.Frame(main_frame, bg=BG_COLOR)
    button_frame.pack()
    submit_button = tk.Button(button_frame, text="Submit Answer",
                              font=("Arial", 13, "bold"), bg=BLUE,
                              fg="white", width=15, command=submit_answer)
    submit_button.pack(side="left", padx=10)

    last_question = current_question == len(quiz_questions) - 1
    next_button = tk.Button(button_frame,
                            text="See Results" if last_question else "Next Question",
                            font=("Arial", 13, "bold"), width=15,
                            state="disabled", command=next_question)
    next_button.pack(side="left", padx=10)

    update_timer()


# TIMER
def update_timer():
    """Runs once per second until the question is answered or time is up."""
    global time_left, timer_job
    if answered:
        return
    timer_label.config(text=f"Time left: {time_left}s",
                       fg=WRONG_COLOR if time_left <= 5 else "black")
    if time_left == 0:
        time_up()
        return
    time_left -= 1
    timer_job = root.after(1000, update_timer)

def stop_timer():
    """Cancel the scheduled timer so it stops counting down."""
    global timer_job
    if timer_job is not None:
        root.after_cancel(timer_job)
        timer_job = None


# ANSWER CHECKING
def lock_choices():
    """Disable all radio buttons after the question is finished."""
    for button in choice_buttons:
        button.config(state="disabled")

def submit_answer():
    global score, answered
    if answered:                      
        return
    choice = selected_answer.get()
    if choice == "":
        messagebox.showwarning("No answer", "Please select an answer first.")
        return

    answered = True
    stop_timer()
    lock_choices()
    submit_button.config(state="disabled")

    question = quiz_questions[current_question]
    if choice == question["answer"]: 
        score += 1
        feedback_label.config(text="Correct!", fg=CORRECT_COLOR)
    else:
        wrong_answers.append({      
            "question": question["question"],
            "your_answer": get_choice_text(question, choice),
            "correct_answer": get_choice_text(question, question["answer"])
        })
        feedback_label.config(
            text="Wrong! Correct answer: "
                 + get_choice_text(question, question["answer"]),
            fg=WRONG_COLOR)
    next_button.config(state="normal")

def time_up():
    """Called when the timer reaches zero. Counts as a wrong answer."""
    global answered
    if answered:
        return
    answered = True
    stop_timer()
    lock_choices()
    submit_button.config(state="disabled")

    question = quiz_questions[current_question]
    wrong_answers.append({
        "question": question["question"],
        "your_answer": "No answer (time is up)",
        "correct_answer": get_choice_text(question, question["answer"])
    })
    feedback_label.config(
        text="Time is up! Correct answer: "
             + get_choice_text(question, question["answer"]),
        fg=WRONG_COLOR)
    next_button.config(state="normal")


def next_question():
    global current_question
    current_question += 1
    if current_question < len(quiz_questions):
        show_question()
    else:
        show_results()


# RESULTS, REVIEW, RESTART
def show_results():
    clear_screen()
    total = len(quiz_questions)
    percentage = (score / total) * 100
    new_record = save_high_score(score)

    if percentage >= 90:
        message = "Excellent work!"
    elif percentage >= 70:
        message = "Good job!"
    elif percentage >= 50:
        message = "Not bad. Keep practicing!"
    else:
        message = "Review the topic and try again."

    tk.Label(main_frame, text=f"Quiz Complete, {player_name}!",
             font=("Georgia", 26, "bold"),
             bg=BG_COLOR, fg=BLUE).pack(pady=(10, 5))
    tk.Label(main_frame, text=f"Score: {score} / {total}  ({percentage:.0f}%)",
             font=("Arial", 18, "bold"), bg=BG_COLOR).pack()
    tk.Label(main_frame, text=message, font=("Arial", 14),
             bg=BG_COLOR).pack(pady=3)

    record_text = ("New high score!" if new_record
                   else f"High Score: {get_high_score()} / {total}")
    tk.Label(main_frame, text=record_text, font=("Arial", 13, "bold"),
             bg=BG_COLOR, fg=CORRECT_COLOR).pack(pady=3)

    tk.Label(main_frame, text="Answer Review (incorrect answers)",
             font=("Arial", 13, "bold"), bg=BG_COLOR).pack(pady=(10, 3), anchor="w")

    review_frame = tk.Frame(main_frame, bg=BG_COLOR)
    review_frame.pack(fill="both", expand=True)
    scrollbar = tk.Scrollbar(review_frame)
    scrollbar.pack(side="right", fill="y")
    review_box = tk.Text(review_frame, height=10, wrap="word",
                         font=("Arial", 11), yscrollcommand=scrollbar.set)
    review_box.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=review_box.yview)

    if not wrong_answers:
        review_box.insert("end", "Perfect! You answered every question correctly.")
    else:
        for number, item in enumerate(wrong_answers, start=1):
            review_box.insert("end", f"{number}. {item['question']}\n")
            review_box.insert("end", f"   Your answer: {item['your_answer']}\n")
            review_box.insert("end", f"   Correct answer: {item['correct_answer']}\n\n")
    review_box.config(state="disabled")   # read-only

    button_frame = tk.Frame(main_frame, bg=BG_COLOR)
    button_frame.pack(pady=15)
    tk.Button(button_frame, text="Restart Quiz", font=("Arial", 13, "bold"),
              bg=BLUE, fg="white", width=15,
              command=restart_quiz).pack(side="left", padx=6)
    tk.Button(button_frame, text="Change Name", font=("Arial", 13, "bold"),
              bg=YELLOW, width=15,
              command=show_start_screen).pack(side="left", padx=6)   # back to the name box
    tk.Button(button_frame, text="Exit", font=("Arial", 13, "bold"),
              bg=RED, fg="white", width=10,
              command=on_close).pack(side="left", padx=6)


def restart_quiz():
    start_quiz()  # reshuffles questions and resets score


def on_close():
    stop_timer()  # cancel the timer before closing the window
    root.destroy()


# START THE PROGRAM
root.protocol("WM_DELETE_WINDOW", on_close)
show_start_screen()
root.mainloop()