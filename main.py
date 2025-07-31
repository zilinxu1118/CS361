# Zilin Xu
# xuzili@oregonstate.edu
# 7/27/2025
# CS 361 Software Engineering 1
# Package Tracking System
# A simple GUI application to track packages using Python's Tkinter library.


import tkinter as tk
from tkinter import messagebox, simpledialog
import os

DATA_FILE = "data.txt"


# ---------------------------
# Helper Functions
# ---------------------------

def load_packages():
    packages = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 4:
                    packages.append({
                        "id": parts[0],
                        "name": parts[1],
                        "address": parts[2],
                        "status": parts[3]
                    })
    return packages


def save_packages(packages):
    with open(DATA_FILE, "w") as f:
        for p in packages:
            f.write(f"{p['id']},{p['name']},{p['address']},{p['status']}\n")


# ---------------------------
# Main Functionalities
# ---------------------------

def add_package():
    def submit():
        pkg_id = entry_id.get().strip()
        name = entry_name.get().strip()
        address = entry_address.get().strip()
        status = status_var.get()

        if not pkg_id or not name or not address or status == "Select":
            messagebox.showwarning("Warning", "All fields are required.")
            return

        packages = load_packages()
        if any(p["id"] == pkg_id for p in packages):
            messagebox.showerror("Error", "Package ID already exists.")
            return

        packages.append({
            "id": pkg_id,
            "name": name,
            "address": address,
            "status": status
        })
        save_packages(packages)
        messagebox.showinfo("Success", "Package added successfully!")
        window.destroy()

    def cancel():
        window.destroy()

    window = tk.Toplevel()
    window.title("Add New Package")

    tk.Label(window, text="Package ID:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_id = tk.Entry(window, width=30)
    entry_id.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(window, text="Recipient Name:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_name = tk.Entry(window, width=30)
    entry_name.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(window, text="Address:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entry_address = tk.Entry(window, width=30)
    entry_address.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(window, text="Status:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    status_var = tk.StringVar(value="Select")
    status_options = ["Preparing", "Shipped", "In Transit", "Delivered"]
    status_menu = tk.OptionMenu(window, status_var, *status_options)
    status_menu.config(width=27)
    status_menu.grid(row=3, column=1, padx=10, pady=5)

    tk.Button(window, text="Submit", command=submit).grid(row=4, column=0, padx=10, pady=15)
    tk.Button(window, text="Cancel", command=cancel).grid(row=4, column=1, padx=10, pady=15)


def view_packages():
    packages = load_packages()
    if not packages:
        messagebox.showinfo("Packages", "No packages found.")
        return

    def filter_packages(status_filter):
        text.config(state=tk.NORMAL)
        text.delete("1.0", tk.END)

        filtered = [p for p in packages if p["status"] == status_filter] if status_filter != "All" else packages

        if not filtered:
            text.insert(tk.END, "No packages with that status.\n")
        else:
            for p in filtered:
                text.insert(tk.END, f"ID: {p['id']}\nName: {p['name']}\nAddress: {p['address']}\nStatus: {p['status']}\n\n")

        text.config(state=tk.DISABLED)

    window = tk.Toplevel()
    window.title("All Packages")

    tk.Label(window, text="Filter by Status:", font=("Arial", 12)).pack(pady=(10, 0))

    filter_var = tk.StringVar(value="All")
    filter_menu = tk.OptionMenu(window, filter_var, "All", "Preparing", "Shipped", "In Transit", "Delivered", command=filter_packages)
    filter_menu.config(width=20)
    filter_menu.pack(pady=5)

    text = tk.Text(window, width=60, height=20, wrap=tk.WORD)
    text.pack(padx=10, pady=10)
    text.config(state=tk.DISABLED)

    filter_packages("All")



def search_package():
    def search():
        pkg_id = entry_id.get().strip()
        if not pkg_id:
            messagebox.showwarning("Warning", "Please enter a Package ID.")
            return

        packages = load_packages()
        for p in packages:
            if p["id"] == pkg_id:
                result_text.set(f"Name: {p['name']}\nAddress: {p['address']}\nStatus: {p['status']}")
                return
        result_text.set("Package not found.")

    window = tk.Toplevel()
    window.title("Search Package by ID")

    tk.Label(window, text="Package ID:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    entry_id = tk.Entry(window, width=30)
    entry_id.grid(row=0, column=1, padx=10, pady=10)

    tk.Button(window, text="Search", command=search).grid(row=1, column=0, columnspan=2, pady=5)

    result_text = tk.StringVar()
    tk.Label(window, textvariable=result_text, fg="blue", justify="left").grid(row=2, column=0, columnspan=2, padx=10, pady=10)


def update_status():
    packages = load_packages()
    if not packages:
        messagebox.showinfo("Info", "No packages available.")
        return

    def on_select(event):
        selected_id = id_var.get()
        for p in packages:
            if p["id"] == selected_id:
                current_status.set(p["status"])
                break

    def update():
        selected_id = id_var.get()
        new_stat = status_var.get()
        if new_stat == "Select":
            messagebox.showwarning("Warning", "Please choose a new status.")
            return

        for p in packages:
            if p["id"] == selected_id:
                p["status"] = new_stat
                break
        save_packages(packages)
        messagebox.showinfo("Success", "Status updated.")
        window.destroy()

    window = tk.Toplevel()
    window.title("Update Package Status")

    tk.Label(window, text="Select Package ID:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    id_var = tk.StringVar()
    id_menu = tk.OptionMenu(window, id_var, *[p["id"] for p in packages], command=on_select)
    id_menu.config(width=25)
    id_menu.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(window, text="Current Status:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    current_status = tk.StringVar()
    tk.Label(window, textvariable=current_status, fg="blue").grid(row=1, column=1, padx=10, pady=5)

    tk.Label(window, text="New Status:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    status_var = tk.StringVar(value="Select")
    status_options = ["Preparing", "Shipped", "In Transit", "Delivered"]
    tk.OptionMenu(window, status_var, *status_options).grid(row=2, column=1, padx=10, pady=5)

    tk.Button(window, text="Update Status", command=update).grid(row=3, column=0, columnspan=2, pady=10)

def delete_package():
    packages = load_packages()
    if not packages:
        messagebox.showinfo("Info", "No packages to delete.")
        return

    def confirm_delete():
        pkg_id = id_var.get()
        if not pkg_id:
            return

        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"⚠️ You are about to permanently delete package '{pkg_id}'.\n\n"
            "This action **cannot be undone**.\n\nDo you want to continue?"
        )
        if confirm:
            new_packages = [p for p in packages if p["id"] != pkg_id]
            save_packages(new_packages)
            messagebox.showinfo("Deleted", f"Package {pkg_id} has been deleted.")
            window.destroy()

    window = tk.Toplevel()
    window.title("Delete Package")

    tk.Label(window, text="Select Package ID to Delete:", font=("Arial", 11)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
    id_var = tk.StringVar()
    tk.OptionMenu(window, id_var, *[p["id"] for p in packages]).grid(row=0, column=1, padx=10, pady=10)

    tk.Button(window, text="Delete Package", command=confirm_delete, fg="white", bg="red").grid(row=1, column=0, columnspan=2, pady=15)


# ---------------------------
# GUI Setup
# ---------------------------

def main():
    root = tk.Tk()
    root.title("📦 Package Tracking System")
    root.geometry("420x450")

    # Title
    tk.Label(root, text="📦 Package Tracker", font=("Helvetica", 18, "bold")).pack(pady=(15, 5))

    # Description
    description = (
        "This desktop application allows users to manage package delivery information locally.\n"
        "You can add, view, update, search, and delete package records using a simple interface."
    )
    tk.Label(root, text=description, font=("Arial", 10), wraplength=380, justify="center", fg="gray").pack(pady=(0, 15))

    # Button Frame
    frame = tk.Frame(root)
    frame.pack(pady=10)

    btn_kwargs = {"width": 25, "height": 2, "font": ("Arial", 10)}

    tk.Button(frame, text="Add Package", command=add_package, **btn_kwargs).pack(pady=5)
    tk.Button(frame, text="View All Packages", command=view_packages, **btn_kwargs).pack(pady=5)
    tk.Button(frame, text="Search Package by ID", command=search_package, **btn_kwargs).pack(pady=5)
    tk.Button(frame, text="Update Package Status", command=update_status, **btn_kwargs).pack(pady=5)
    tk.Button(frame, text="Delete Package", command=delete_package, **btn_kwargs).pack(pady=5)
    tk.Button(root, text="Exit", command=root.quit, **btn_kwargs).pack(pady=10)

    root.mainloop()



if __name__ == "__main__":
    main()
