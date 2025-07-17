import tkinter as tk
from tkinter import messagebox, simpledialog

# Load questions from string or file
def parse_questions(raw_lines):
    questions = []
    for line in raw_lines:
        parts = line.strip().split("|")
        if len(parts) == 6:
            question, a, b, c, d, correct = parts
            questions.append((question, [a, b, c, d], correct.upper()))
    return questions

def load_questions_from_file(filename):
    try:
        with open(filename, "r") as file:
            return parse_questions(file.readlines())
    except:
        return []

# Main Quiz App
class QuizApp:
    def __init__(self, root, questions, time_per_question, max_wrong):
        self.root = root
        self.root.title("AWS Quiz App")
        self.questions = questions
        self.time_per_question = time_per_question
        self.max_wrong = max_wrong

        self.q_index = 0
        self.score = 0
        self.wrong = 0

        self.timer_label = tk.Label(root, text="", font=("Arial", 12))
        self.timer_label.pack(pady=5)

        self.question_label = tk.Label(root, text="", wraplength=600, font=("Arial", 14))
        self.question_label.pack(pady=20)

        self.buttons = []
        for i in range(4):
            btn = tk.Button(root, text="", font=("Arial", 12), width=40, command=lambda i=i: self.check_answer(i))
            btn.pack(pady=5)
            self.buttons.append(btn)

        # About Button
        about_btn = tk.Button(root, text="ℹ️ About", font=("Arial", 10), command=self.show_about)
        about_btn.pack(pady=10)

        self.load_question()

    def load_question(self):
        if self.q_index >= len(self.questions):
            self.end_game(won=True)
            return

        self.time_left = self.time_per_question
        self.update_timer()

        q, opts, _ = self.questions[self.q_index]
        self.question_label.config(text=f"Q{self.q_index+1}: {q}")
        for i, opt in enumerate(opts):
            self.buttons[i].config(text=f"{chr(65+i)}) {opt}", state="normal")

    def update_timer(self):
        self.timer_label.config(text=f"⏱️ Time left: {self.time_left} seconds")
        if self.time_left > 0:
            self.time_left -= 1
            self.timer = self.root.after(1000, self.update_timer)
        else:
            self.disable_buttons()
            messagebox.showerror("Time's Up", "❌ You ran out of time!")
            self.register_wrong()

    def disable_buttons(self):
        for btn in self.buttons:
            btn.config(state="disabled")

    def check_answer(self, choice):
        self.root.after_cancel(self.timer)
        _, opts, correct = self.questions[self.q_index]
        selected = chr(65 + choice)

        if selected == correct:
            self.score += 1
        else:
            messagebox.showerror("Wrong!", f"❌ Incorrect! Correct answer: {correct}) {opts[ord(correct)-65]}")
            self.register_wrong()
            return

        self.q_index += 1
        self.load_question()

    def register_wrong(self):
        self.wrong += 1
        if self.wrong > self.max_wrong:
            self.end_game(won=False)
        else:
            self.q_index += 1
            self.load_question()

    def end_game(self, won):
        if won:
            messagebox.showinfo("Quiz Completed", f"🎉 You finished the quiz!\nScore: {self.score}/{len(self.questions)}")
        else:
            messagebox.showinfo("Game Over", f"💀 Game Over!\nToo many wrong answers.\nScore: {self.score}/{len(self.questions)}")
        self.root.quit()

    def show_about(self):
        messagebox.showinfo(
            "About This App",
            "📘 AWS Quiz App\n\nDeveloped by Hosam Haroobi 💻\n\nPractice your AWS knowledge with instant feedback.\n\nBuilt with ❤️ using Python + Tkinter on Ubuntu."
        )

# Run App
if __name__ == "__main__":
    try:
        root = tk.Tk()
        root.withdraw()

        source = simpledialog.askstring("Quiz Setup", "Type 'file' to load from questions.txt,\nor 'paste' to enter questions manually:")

        if not source or source.lower() not in ["file", "paste"]:
            raise Exception("Quiz cancelled")

        if source.lower() == "file":
            questions = load_questions_from_file("questions.txt")
        else:
            pasted = simpledialog.askstring("Paste Questions", "Paste questions below:\n(Format: Question|A|B|C|D|CorrectLetter)", initialvalue="")
            if not pasted:
                raise Exception("No questions pasted")
            questions = parse_questions(pasted.strip().splitlines())

        if not questions:
            raise Exception("❌ No valid questions found!")

        time_limit = simpledialog.askinteger("Time per Question", "Enter seconds per question:", minvalue=5, maxvalue=120)
        max_wrong = simpledialog.askinteger("Max Wrong Answers", "Enter allowed wrong answers:", minvalue=0, maxvalue=len(questions))

        if time_limit is None or max_wrong is None:
            raise Exception("Cancelled by user")

        root.deiconify()
        app = QuizApp(root, questions, time_limit, max_wrong)
        root.mainloop()

    except Exception as e:
        print("❌ ERROR:", e)

