import pathlib
import random
from string import ascii_lowercase
import tkinter as tk
from tkinter import messagebox
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

NUM_QUESTIONS_PER_QUIZ = 5
QUESTIONS_PATH = pathlib.Path(__file__).parent / "questions.toml"

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz App")
        
        self.current_question = 0
        self.questions = []
        self.num_correct = 0
        
        self.setup_start_screen()

    def setup_start_screen(self):
        """Setup the start screen with the topic selection."""
        self.clear_screen()
        
        try:
            self.topics = self.load_topics()
        except Exception as e:
            print(f"Error loading topics: {e}")
            messagebox.showerror("Error", f"An error occurred while loading topics: {e}")
            self.root.quit()
            return
        
        if not self.topics:
            messagebox.showerror("Error", "No topics found. Make sure 'questions.toml' is present and correctly formatted.")
            self.root.quit()
            return

        self.topic_label = tk.Label(self.root, text="Select a topic:")
        self.topic_label.pack(pady=10)
        
        self.topic_var = tk.StringVar(value=self.topics[0])
        self.topic_menu = tk.OptionMenu(self.root, self.topic_var, *self.topics)
        self.topic_menu.pack(pady=10)
        
        self.start_button = tk.Button(self.root, text="Start Quiz", command=self.start_quiz)
        self.start_button.pack(pady=20)

    def load_topics(self):
        """Load topics from the TOML file."""
        if not QUESTIONS_PATH.exists():
            raise FileNotFoundError(f"File not found: {QUESTIONS_PATH}")
        
        topic_info = tomllib.loads(QUESTIONS_PATH.read_text())
        print("Loaded topics:", topic_info)  # Debugging line
        
        topics = [topic["label"] for topic in topic_info.values()]
        return sorted(topics)

    def start_quiz(self):
        """Start the quiz by loading questions from the selected topic."""
        topic_label = self.topic_var.get()
        try:
            self.questions = self.prepare_questions(topic_label)
        except Exception as e:
            print(f"Error preparing questions: {e}")
            messagebox.showerror("Error", f"An error occurred while preparing the questions: {e}")
            self.root.quit()
            return
        
        self.current_question = 0
        self.num_correct = 0
        self.ask_question(self.questions[self.current_question])

    def prepare_questions(self, topic_label):
        """Prepare questions based on the selected topic."""
        topic_info = tomllib.loads(QUESTIONS_PATH.read_text())
        questions = [
            topic for topic in topic_info.values() if topic["label"] == topic_label
        ][0]["questions"]
        return random.sample(questions, k=NUM_QUESTIONS_PER_QUIZ)

    def ask_question(self, question):
        """Display the current question and choices."""
        self.clear_screen()
        
        self.question_label = tk.Label(self.root, text=question["question"])
        self.question_label.pack(pady=10)
        
        self.alternatives = question["answers"] + question["alternatives"]
        random.shuffle(self.alternatives)

        self.buttons = []
        for idx, alternative in enumerate(self.alternatives):
            button = tk.Button(self.root, text=alternative, 
                               command=lambda alt=alternative: self.check_answer(alt, question))
            button.pack(pady=5)
            self.buttons.append(button)

        self.hint_button = None
        if "hint" in question:
            self.hint_button = tk.Button(self.root, text="Hint", command=lambda: self.show_hint(question))
            self.hint_button.pack(pady=10)

    def check_answer(self, answer, question):
        """Check if the selected answer is correct."""
        correct_answers = question["answers"]
        if set([answer]) == set(correct_answers):
            self.num_correct += 1
            messagebox.showinfo("Correct!", "⭐ Correct! ⭐")
        else:
            messagebox.showinfo("Incorrect", f"No, the correct answer(s) is/are: {', '.join(correct_answers)}")
        
        if "explanation" in question:
            messagebox.showinfo("Explanation", question["explanation"])
        
        self.current_question += 1
        if self.current_question < len(self.questions):
            self.ask_question(self.questions[self.current_question])
        else:
            self.show_result()

    def show_hint(self, question):
        """Display the hint for the current question."""
        messagebox.showinfo("Hint", question["hint"])

    def show_result(self):
        """Show the final score after all questions."""
        self.clear_screen()
        result_text = f"You got {self.num_correct} correct out of {len(self.questions)} questions!"
        result_label = tk.Label(self.root, text=result_text, font=("Helvetica", 16))
        result_label.pack(pady=20)
        
        restart_button = tk.Button(self.root, text="Restart Quiz", command=self.setup_start_screen)
        restart_button.pack(pady=20)

    def clear_screen(self):
        """Clear the current screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = QuizApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Error starting the quiz: {e}")
        messagebox.showerror("Error", f"An error occurred while starting the quiz: {e}")
