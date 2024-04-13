import tkinter as tk
from tkinter import messagebox
import pickle
import os

class WorkoutApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TSPA")
        self.geometry("400x500")

        self.workout_plan_file = "workout_plan.pkl"
        self.completed_exercises_file = "completed_exercises.pkl"

        # Remove the completed exercises file if it exists
        if os.path.exists(self.completed_exercises_file):
            os.remove(self.completed_exercises_file)

        self.load_workout_plan()
        self.completed_exercises = {}
        self.create_widgets()

    def load_workout_plan(self):
        try:
            with open(self.workout_plan_file, "rb") as file:
                self.workout_plan = pickle.load(file)
        except FileNotFoundError:
            self.workout_plan = {
                "Push-ups": {"sets": 3, "reps": 10},
                "Squats": {"sets": 3, "reps": 12},
                "Plank": {"sets": 3, "reps": 30}
            }

    def load_completed_exercises(self):
        try:
            with open(self.completed_exercises_file, "rb") as file:
                self.completed_exercises = pickle.load(file)
        except FileNotFoundError:
            self.completed_exercises = {}

    def save_workout_plan(self):
        with open(self.workout_plan_file, "wb") as file:
            pickle.dump(self.workout_plan, file)

    def save_completed_exercises(self):
        with open(self.completed_exercises_file, "wb") as file:
            pickle.dump(self.completed_exercises, file)

    def create_widgets(self):
        self.label = tk.Label(self, text="Šodienas treniņš:")
        self.label.pack()

        self.checkbuttons = {}
        self.remove_buttons = {}
        for exercise, details in self.workout_plan.items():
            check_var = tk.BooleanVar(value=exercise in self.completed_exercises)
            check_button = tk.Checkbutton(self, text=exercise, variable=check_var)
            check_button.pack(anchor='w')
            self.checkbuttons[exercise] = {"var": check_var, "details": details}

            remove_button = tk.Button(self, text="Izdzēst", command=lambda ex=exercise: self.remove_exercise(ex))
            remove_button.pack(anchor='w')
            self.remove_buttons[exercise] = remove_button

        self.new_exercise_label = tk.Label(self, text="Pievienot jaunu vingrinājumu:")
        self.new_exercise_label.pack()

        self.new_exercise_name = tk.Entry(self)
        self.new_exercise_name.pack()

        self.new_sets_label = tk.Label(self, text="Reizes:")
        self.new_sets_label.pack()
        self.new_sets = tk.Entry(self)
        self.new_sets.pack()

        self.new_reps_label = tk.Label(self, text="Atkārtojumi:")
        self.new_reps_label.pack()
        self.new_reps = tk.Entry(self)
        self.new_reps.pack()

        self.add_button = tk.Button(self, text="Pievienot jaunu vingrinājumu", command=self.add_exercise)
        self.add_button.pack()

        self.check_button = tk.Button(self, text="Pārbaudīt vingrinājumu", command=self.check_exercise)
        self.check_button.pack()

        self.progress_button = tk.Button(self, text="Parādīt progresu", command=self.show_progress)
        self.progress_button.pack()

    def add_exercise(self):
        new_exercise = self.new_exercise_name.get()
        sets = self.new_sets.get()
        reps = self.new_reps.get()

        if new_exercise.strip() == "":
            messagebox.showerror("Kļūda", "Lūdzu ierakstiet vingrinājuma nosaukumu.")
            return

        try:
            sets = int(sets)
            reps = int(reps)
        except ValueError:
            messagebox.showerror("Kļūda", "Reizes un atkārtojumi jābūt kā veseli skaitļi.")
            return

        self.workout_plan[new_exercise] = {"sets": sets, "reps": reps}
        self.checkbuttons[new_exercise] = {"var": tk.BooleanVar(), "details": {"sets": sets, "reps": reps}}

        remove_button = tk.Button(self, text="Remove", command=lambda ex=new_exercise: self.remove_exercise(ex))
        remove_button.pack(anchor='w')
        self.remove_buttons[new_exercise] = remove_button

        messagebox.showinfo("Success", f"New exercise '{new_exercise}' added to the workout plan.")
        self.save_workout_plan()

    def remove_exercise(self, exercise):
        if messagebox.askyesno("Confirm", f"Are you sure you want to remove '{exercise}'?"):
            del self.workout_plan[exercise]
            del self.checkbuttons[exercise]
            self.remove_buttons[exercise].pack_forget()
            del self.remove_buttons[exercise]
            messagebox.showinfo("Success", f"Exercise '{exercise}' removed from the workout plan.")
            self.save_workout_plan()

    def check_exercise(self):
        for exercise, data in self.checkbuttons.items():
            var = data["var"]
            if var.get():
                if exercise in self.completed_exercises:
                    self.completed_exercises[exercise] += 1
                else:
                    self.completed_exercises[exercise] = 1
                messagebox.showinfo("Success", f"{exercise} completed!")
        self.save_completed_exercises()

    def show_progress(self):
        if not self.completed_exercises:
            messagebox.showinfo("Progress", "Neviens vingrinājums nav izdarīts.")
        else:
            progress_message = "Tavs treniņa progress:\n"
            for exercise, count in self.completed_exercises.items():
                progress_message += f"{exercise}: {count} times\n"
            messagebox.showinfo("Progress", progress_message)

if __name__ == "__main__":
    app = WorkoutApp()
    app.mainloop()