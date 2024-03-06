import tkinter as tk
from tkinter import messagebox
import threading
import time
import csv

class Lab:
    def __init__(self, lab_id, num_computers):
        self.lab_id = lab_id
        self.num_computers = num_computers
        self.available_computers = num_computers
        self.current_class = None
        self.assignment_thread = None
        self.class_name = None
        self.assigned_time = None
        self.time_duration = None
        self.total_students = None

    def assign_class(self, class_name, num_students, class_duration_hours):
        class_duration_seconds = class_duration_hours * 3600  # Convert hours to seconds
        if self.current_class is None and num_students <= self.available_computers:
            self.current_class = class_name
            self.available_computers -= num_students
            self.class_name = class_name
            self.assigned_time = time.strftime("%H:%M:%S")
            self.time_duration = class_duration_hours
            self.total_students = num_students
            message = f"Class '{class_name}' assigned to Lab {self.lab_id} for {class_duration_hours} hours."
            output_text.insert(tk.END, message + "\n")
            self.assignment_thread = threading.Thread(target=self.run_class, args=(class_name, class_duration_seconds))
            self.assignment_thread.start()
            self.save_to_csv()
        elif self.current_class is not None:
            message = f"Lab {self.lab_id} is occupied by '{self.current_class}' class."
            output_text.insert(tk.END, message + "\n")
        else:
            message = f"Not enough computers in Lab {self.lab_id} for the class."
            output_text.insert(tk.END, message + "\n")

    def run_class(self, class_name, class_duration):
        time.sleep(class_duration)  # Simulate class duration
        self.current_class = None
        self.available_computers = self.num_computers
        message = f"Class '{class_name}' completed in Lab {self.lab_id}."
        output_text.insert(tk.END, message + "\n")

    def save_to_csv(self):
        with open("Lab_data.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([self.lab_id, self.class_name, self.assigned_time, self.time_duration, self.total_students])


class LabManagementSystem:
    def __init__(self, lab_capacity_list):
        self.labs = [Lab(i + 1, num_computers) for i, num_computers in enumerate(lab_capacity_list)]

    def assign_class_to_lab(self, class_name, num_students, class_duration_hours):
        for lab in self.labs:
            if lab.current_class is None:
                lab.assign_class(class_name, num_students, class_duration_hours)
                return
        message = "No available labs for the class at the moment."
        output_text.insert(tk.END, message + "\n")

    def display_lab_status(self):
        for lab in self.labs:
            lab.display_status()


def assign_class():
    class_name = class_name_entry.get()
    num_students = int(num_students_entry.get())
    class_duration_hours = int(class_duration_entry.get())
    lab_system.assign_class_to_lab(class_name, num_students, class_duration_hours)
    lab_system.display_lab_status()


root = tk.Tk()
root.title("Lab Management System")

lab_system = None
num_labs = 0

def create_lab_system():
    global lab_system, num_labs
    lab_capacity_list = [int(entry.get()) for entry in lab_capacity_entries]
    lab_system = LabManagementSystem(lab_capacity_list)
    num_labs = len(lab_capacity_list)

num_labs_label = tk.Label(root, text="Enter the number of labs:")
num_labs_label.grid(row=0, column=0, sticky=tk.W)

num_labs_entry = tk.Entry(root)
num_labs_entry.grid(row=0, column=1, sticky=tk.W)

create_labs_button = tk.Button(root, text="Create Labs", command=create_lab_system)
create_labs_button.grid(row=0, column=2, sticky=tk.W)

lab_capacity_entries = []

def create_lab_capacity_entries():
    global num_labs
    num_labs = int(num_labs_entry.get())
    for i in range(num_labs):
        lab_capacity_label = tk.Label(root, text=f"Enter the number of computers in Lab {i + 1}:")
        lab_capacity_label.grid(row=i + 1, column=1, sticky=tk.W)
        lab_capacity_entry = tk.Entry(root)
        lab_capacity_entry.grid(row=i + 1, column=2, sticky=tk.W)
        lab_capacity_entries.append(lab_capacity_entry)

    class_name_label.grid(row=num_labs + 1, column=0, sticky=tk.W)
    class_name_entry.grid(row=num_labs + 1, column=1, sticky=tk.W)

    num_students_label.grid(row=num_labs + 2, column=0, sticky=tk.W)
    num_students_entry.grid(row=num_labs + 2, column=1, sticky=tk.W)

    class_duration_label.grid(row=num_labs + 3, column=0, sticky=tk.W)
    class_duration_entry.grid(row=num_labs + 3, column=1, sticky=tk.W)

    assign_class_button.grid(row=num_labs + 4, column=0, columnspan=2, sticky=tk.W)


create_lab_capacity_entries_button = tk.Button(root, text="Create Lab Capacity Entries", command=create_lab_capacity_entries)
create_lab_capacity_entries_button.grid(row=num_labs + 1, column=0, columnspan=2, sticky=tk.W)

class_name_label = tk.Label(root, text="Enter the class name:")
class_name_label.grid(row=num_labs + 2, column=0, sticky=tk.W)

class_name_entry = tk.Entry(root)
class_name_entry.grid(row=num_labs + 2, column=1, sticky=tk.W)

num_students_label = tk.Label(root, text="Enter the number of students:")
num_students_label.grid(row=num_labs + 3, column=0, sticky=tk.W)

num_students_entry = tk.Entry(root)
num_students_entry.grid(row=num_labs + 3, column=1, sticky=tk.W)

class_duration_label = tk.Label(root, text="Enter the duration of the class (in hours):")
class_duration_label.grid(row=num_labs + 4, column=0, sticky=tk.W)

class_duration_entry = tk.Entry(root)
class_duration_entry.grid(row=num_labs + 4, column=1, sticky=tk.W)

assign_class_button = tk.Button(root, text="Assign Class", command=assign_class)
assign_class_button.grid(row=num_labs + 5, column=0, columnspan=2, sticky=tk.W)

output_text = tk.Text(root, height=30, width=50)
output_text.grid(row=0, column=3, rowspan=num_labs + 6, padx=10, pady=10)

root.mainloop()
