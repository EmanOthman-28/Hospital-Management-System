# الكلاس الأساسي 
class Person:
    def __init__(self, name, id_number):
        self.name = name
        self.id_number = id_number

# السجل الطبي
class MedicalRecord:
    def __init__(self):
        self.__data = [] 
    
    def add(self, note):
        self.__data.append(note)

# الدكتور يورث من الشخص
class Doctor(Person):
    def __init__(self, name, id_number, spec):
        super().__init__(name, id_number)
        self.spec = spec

# المريض يورث من الشخص
class Patient(Person):
    def __init__(self, name, id_number):
        super().__init__(name, id_number)
        self.record = MedicalRecord()

# بيانات الدكاترة والمرضى
doctors = {
    "Dr. Eman": Doctor("Dr. Eman", "123", "Heart"),
    "Dr. Alia": Doctor("Dr. Alia", "456", "Kids")
}

patients = {
    "Mohamed": Patient("Mohamed", "789"),
    "Ahmed": Patient("Ahmed", "101"),
    "Sara": Patient("Sara", "202")
}

import tkinter as tk
from tkinter import ttk, messagebox

app = tk.Tk()
app.title("Hospital System")
app.geometry("450x650")

# متغير لحفظ المريض المختار
active_patient = None 

#  تبديل الصفحات
def show_page(frame):
    frame.tkraise()


home_page = tk.Frame(app)
doctor_page = tk.Frame(app)
patient_page = tk.Frame(app)

#  الصفحات فوق بعضها
home_page.grid(row=0, column=0, sticky='nsew')
doctor_page.grid(row=0, column=0, sticky='nsew')
patient_page.grid(row=0, column=0, sticky='nsew')

app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

# صفحة الدخول الرئيسية
tk.Label(home_page, text="Clinic System", font=("Arial", 22, "bold"), fg="darkblue").pack(pady=50)
tk.Label(home_page, text="Enter Name:").pack(pady=5)
name_entry = tk.Entry(home_page, width=25)
name_entry.pack(pady=10)

def login(user_type):
    global active_patient
    user_name = name_entry.get().strip()
    
    if user_name == "":
        messagebox.showwarning("Warning", "Please enter your name")
        return

    if user_type == "doctor":
        if user_name in doctors:
            doc_msg.config(text="Welcome " + user_name)
            show_page(doctor_page)
        else:
            messagebox.showerror("Error", "Doctor not found")
    else:
        if user_name in patients:
            active_patient = patients[user_name]
            pat_msg.config(text="Hello " + user_name)
            show_page(patient_page)
        else:
            messagebox.showerror("Error", "Patient not found")

tk.Button(home_page, text="Login as Doctor", width=20, command=lambda: login("doctor")).pack(pady=10)
tk.Button(home_page, text="Login as Patient", width=20, command=lambda: login("patient")).pack(pady=10)

# صفحة الدكتور
doc_msg = tk.Label(doctor_page, text="", font=("Arial", 16, "bold"), fg="blue")
doc_msg.pack(pady=20)

tk.Label(doctor_page, text="Select Patient:").pack()
patient_list = ttk.Combobox(doctor_page, values=list(patients.keys()), state="readonly")
patient_list.pack(pady=5)

tk.Label(doctor_page, text="Prescription:").pack(pady=5)
note_area = tk.Text(doctor_page, height=10, width=50)
note_area.pack(pady=10)

def save_note():
    selected_name = patient_list.get()
    if selected_name == "":
        messagebox.showwarning("!", "Select a patient")
        return

    text = note_area.get("1.0", tk.END).strip()
    if text != "":
        patients[selected_name].record.add(text)
        messagebox.showinfo("Done", "Note saved for " + selected_name)
    else:
        messagebox.showwarning("!", "Note is empty")

tk.Button(doctor_page, text="Save", width=15, bg="green", fg="white", command=save_note).pack(pady=10)
tk.Button(doctor_page, text="Logout", width=15, bg="red", fg="white", command=lambda: show_page(home_page)).pack()

# صفحة المريض
pat_msg = tk.Label(patient_page, text="", font=("Arial", 16, "bold"), fg="green")
pat_msg.pack(pady=20)

tk.Label(patient_page, text="Choose Doctor:").pack()
doctor_drop = ttk.Combobox(patient_page, values=list(doctors.keys()), state="readonly")
doctor_drop.pack(pady=10)

tk.Label(patient_page, text="Date:").pack()
date_entry = tk.Entry(patient_page)
date_entry.pack(pady=5)

table = ttk.Treeview(patient_page, columns=("Doc", "Date", "Stat"), show="headings", height=6)
table.heading("Doc", text="Doctor")
table.heading("Date", text="Date")
table.heading("Stat", text="Status")
table.pack(pady=20)

def booking():
    d = doctor_drop.get()
    t = date_entry.get()
    if d != "" and t != "":
        table.insert("", tk.END, values=(d, t, "Confirmed"))
        messagebox.showinfo("Success", "Booked!")
    else:
        messagebox.showerror("!", "Missing info")

tk.Button(patient_page, text="Book Now", width=20, bg="darkgreen", fg="white", command= booking).pack(pady=10)
tk.Button(patient_page, text="Logout", width=20, bg="red", fg="white", command=lambda: show_page(home_page)).pack()

show_page(home_page)
app.mainloop()