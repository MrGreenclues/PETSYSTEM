from pathlib import Path
import subprocess
import mysql.connector
from tkinter import Tk, Canvas, Button, PhotoImage, Label, messagebox

# Path configuration
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\xampp\htdocs\petborrow\build\assets\frame1")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Function to get available pets count
def get_available_pet_count():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="breed"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM pet WHERE TRIM(LOWER(status)) = 'adopted'")
        result = cursor.fetchone()[0]
        conn.close()
        return result
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
        return "Error"

# Function to get adopted pets count
def get_adopted_pet_count():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="breed"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM pet WHERE TRIM(LOWER(status)) = 'available'")
        result = cursor.fetchone()[0]
        conn.close()
        return result
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
        return "Error"

# Function to open login page
def open_login():
    window.destroy()
    script_dir = Path(__file__).resolve().parent
    login_path = script_dir / "login.py"
    subprocess.run(["python", str(login_path)])

def open_managepet():
    window.destroy()
    script_dir = Path(__file__).resolve().parent
    addpet_path = script_dir / "managepet.py"
    subprocess.run(["python", str(addpet_path)])

def open_managehealth():
    window.destroy()
    script_dir = Path(__file__).resolve().parent
    addpet_path = script_dir / "managehealth.py"
    subprocess.run(["python", str(addpet_path)])

# Main window
window = Tk()
window.geometry("1048x493")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=493,
    width=1048,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

# UI rectangles
canvas.create_rectangle(0.0, 0.0, 273.0, 493.0, fill="#55714F", outline="")
canvas.create_rectangle(742.0, 46.0, 991.0, 203.0, fill="#55714F", outline="")
canvas.create_rectangle(367.0, 47.0, 616.0, 204.0, fill="#55714F", outline="")

# Buttons
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
Button(window, image=button_image_1, borderwidth=0, relief="flat").place(x=38.0, y=26.0, width=206.0, height=42.0)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
Button(window, image=button_image_2, borderwidth=0, command=open_managepet, relief="flat").place(x=38.0, y=102.0, width=206.0, height=42.0)

button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
Button(window, image=button_image_3, borderwidth=0, command=open_managehealth, relief="flat").place(x=38.0, y=178.0, width=206.0, height=42.0)

button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
Button(window, image=button_image_4, borderwidth=0, command=open_login, relief="flat").place(x=33.0, y=425.0, width=206.0, height=42.0)

# Display Available Pets Count
available = str(get_available_pet_count())
Label(window, text=available, bg="#55714F", fg="white", font=("Arial", 28, "bold")).place(
    x=867.5 - (len(available) * 8), y=120
)

# Display Adopted Pets Count
adopted = str(get_adopted_pet_count())
Label(window, text=adopted, bg="#55714F", fg="white", font=("Arial", 28, "bold")).place(
    x=493.5 - (len(adopted) * 8), y=130
)

# Images
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
canvas.create_image(498.0, 75.0, image=image_image_1)

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
canvas.create_image(881.0, 75.0, image=image_image_2)

window.resizable(False, False)
window.mainloop()
