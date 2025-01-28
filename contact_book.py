# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 18:49:58 2025

@author: jakka
"""

import tkinter as tk
from tkinter import messagebox,ttk
import sqlite3

# Database setup
conn = sqlite3.connect("contacts.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL UNIQUE
                )''')
conn.commit()

# Functions
def add_contact():
    name = name_entry.get()
    phone = phone_entry.get()
    if name and phone:
        try:
            cursor.execute("INSERT INTO contacts (name, phone) VALUES (?, ?)", (name, phone))
            conn.commit()
            update_contacts()
            name_entry.delete(0, tk.END)
            phone_entry.delete(0, tk.END)
            messagebox.showinfo("Success", "Contact added successfully!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Phone number already exists!")
    else:
        messagebox.showwarning("Warning", "Both fields are required!")

def update_contacts():
    contact_list.delete(0, tk.END)
    cursor.execute("SELECT * FROM contacts")
    for row in cursor.fetchall():
        contact_list.insert(tk.END, f"{row[1]} - {row[2]}")

def search_contact():
    search_query = search_entry.get()
    contact_list.delete(0, tk.END)
    cursor.execute("SELECT * FROM contacts WHERE name LIKE ?", ('%' + search_query + '%',))
    for row in cursor.fetchall():
        contact_list.insert(tk.END, f"{row[1]} - {row[2]}")
    if not contact_list.size():
        messagebox.showinfo("Not Found", "No contacts found.")

def delete_contact():
    selected = contact_list.curselection()
    if selected:
        name = contact_list.get(selected).split(" - ")[0]
        cursor.execute("DELETE FROM contacts WHERE name=?", (name,))
        conn.commit()
        update_contacts()
        messagebox.showinfo("Success", "Contact deleted successfully!")
    else:
        messagebox.showwarning("Warning", "Please select a contact to delete.")

# GUI Setup
root = tk.Tk()
root.title("Contact Book")
root.geometry("400x500")

#Styles for GUI
style = ttk.Style()
style.configure("TFrame", background="#87CEEB")
style.configure("TLabel", background="#87CEEB",foreground="green", font=("Arial", 12,"bold"))

frame = ttk.Frame(root, style="TFrame")
frame.pack(pady=20, padx=20, fill="both", expand=True)

ttk.Label(frame, text="Name:",style="TLabel").pack(pady=5)
name_entry = tk.Entry(frame, width=20,bg="white",fg="blue",font=("Arial", 12))
name_entry.pack()

ttk.Label(frame, text="Phone:",style="TLabel").pack(pady=5)
phone_entry = tk.Entry(frame, width=20,bg="white",fg="blue",font=("Arial", 12))
phone_entry.pack()

add_button = tk.Button(frame, text="Add Contact",bg="green",fg="white",font=("Arial", 10), command=add_contact)
add_button.pack(pady=10)

ttk.Label(frame, text="Search Contact:",style="TLabel" ).pack(pady=5)
search_entry = tk.Entry(frame, width=20,bg="white",fg="blue",font=("Arial", 12))
search_entry.pack()
search_button = tk.Button(frame, text="Search",bg="green",fg="white",font=("Arial", 10), command=search_contact)
search_button.pack(pady=5)

contact_list = tk.Listbox(frame, width=50, height=8,font=("Arial", 10))
contact_list.pack(pady=10)

delete_button = tk.Button(frame, text="Delete Contact",bg="green",fg="white",font=("Arial", 10), command=delete_contact)
delete_button.pack(pady=5)

update_contacts()

root.mainloop()

