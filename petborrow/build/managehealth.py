

from pathlib import Path
import subprocess
from tkinter import Tk, Canvas, Button, PhotoImage, Label, messagebox, Entry
from tkinter import ttk
import mysql.connector

from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\xampp\htdocs\petborrow\build\assets\frame6")

def fetch_pet_data():
    try:
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='breed'
        )
        mycursor = mydb.cursor()
        # Fetch all pet data, regardless of owner
        mycursor.execute("""
            SELECT petname, gender, allergies, vaccine, tvaccine
            FROM pet
        """)
        rows = mycursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        rows = []
    finally:
        if mycursor:
            mycursor.close()
        if mydb:
            mydb.close()
    return rows

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def populate_pet_treeview():
    for row in pet_tree.get_children():
        pet_tree.delete(row)
    data = fetch_pet_data()
    for item in data:
        pet_tree.insert("", "end", values=item)

  
def search_pet_data():
    keyword = entry_3.get().strip()

    if not keyword:
        messagebox.showwarning("Search Error", "Please enter a keyword to search.")
        return

    try:
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='breed'
        )
        mycursor = mydb.cursor()
        query = """
            SELECT petname, gender, age, allergies, vaccine
            FROM pet
            WHERE petname LIKE %s OR gender LIKE %s OR age LIKE %s OR allergies LIKE %s OR vaccine LIKE %s
        """
        like_keyword = f"%{keyword}%"
        mycursor.execute(query, (like_keyword,) * 5)
        rows = mycursor.fetchall()

        # Clear existing data
        for row in pet_tree.get_children():
            pet_tree.delete(row)

        # Insert search results
        for item in rows:
            pet_tree.insert("", "end", values=item)

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

def update_pets_data():
    selected_item = pet_tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a pet to update")
        return

    petname = entry_1.get().strip()
    allergies = entry_2.get().strip()
    vaccine = entry_4.get().strip()
    tvaccine = entry_5.get().strip()

    if not (petname and allergies and vaccine and tvaccine):
        messagebox.showwarning("Input Error", "Please fill all fields")
        return

    try:
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='breed'
        )
        mycursor = mydb.cursor()

        # Get the original petname from selected Treeview item (assuming petname is in first column)
        original_petname = pet_tree.item(selected_item)['values'][0]

        # Update query using original_petname to locate the correct row
        sql = "UPDATE pet SET  allergies=%s, vaccine=%s, tvaccine=%s WHERE petname=%s"
        val = ( allergies, vaccine, tvaccine, original_petname)
        mycursor.execute(sql, val)
        mydb.commit()

        messagebox.showinfo("Success", "Pet data added successfully!")
        populate_pet_treeview()

        # Clear entry fields
        entry_1.delete(0, 'end')
        entry_2.delete(0, 'end')
        entry_4.delete(0, 'end')
        entry_5.delete(0, 'end')

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        if mycursor:
            mycursor.close()
        if mydb:
            mydb.close()


def update_pet_data():
    selected_item = pet_tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a pet to update")
        return

    petname = entry_1.get().strip()
    allergies = entry_2.get().strip()
    vaccine = entry_4.get().strip()
    tvaccine = entry_5.get().strip()

    if not (petname and allergies and vaccine and tvaccine):
        messagebox.showwarning("Input Error", "Please fill all fields")
        return

    try:
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='breed'
        )
        mycursor = mydb.cursor()

        # Get the original petname from selected Treeview item (assuming petname is in first column)
        original_petname = pet_tree.item(selected_item)['values'][0]

        # Update query using original_petname to locate the correct row
        sql = "UPDATE pet SET  allergies=%s, vaccine=%s, tvaccine=%s WHERE petname=%s"
        val = ( allergies, vaccine, tvaccine, original_petname)
        mycursor.execute(sql, val)
        mydb.commit()

        messagebox.showinfo("Success", "Pet data updated successfully!")
        populate_pet_treeview()

        # Clear entry fields
        entry_1.delete(0, 'end')
        entry_2.delete(0, 'end')
        entry_4.delete(0, 'end')
        entry_5.delete(0, 'end')

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        if mycursor:
            mycursor.close()
        if mydb:
            mydb.close()


def delete_vaccine_allergy_data():
    selected_item = pet_tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a pet to clear data.")
        return

    try:
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='breed'
        )
        mycursor = mydb.cursor()

        # Get the original petname from selected Treeview item (assuming petname is in the first column)
        original_petname = pet_tree.item(selected_item)['values'][0]

        # Update query to set allergies and vaccine to empty strings
        sql = "UPDATE pet SET petname='', allergies='', vaccine='', tvaccine='' WHERE petname=%s"
        mycursor.execute(sql, (original_petname,))
        mydb.commit()

        messagebox.showinfo("Success", "data cleared successfully!")
        populate_pet_treeview()

        # Optionally clear input fields
        entry_2.delete(0, 'end')
        entry_4.delete(0, 'end')

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        if mycursor:
            mycursor.close()
        if mydb:
            mydb.close()


def load_selected_pet(event=None):
    selected_item = pet_tree.selection()
    if selected_item:
        values = pet_tree.item(selected_item[0], 'values')
        if len(values) >= 5:  # updated to >= 5 instead of >= 4
            entry_1.delete(0, "end")
            entry_1.insert(0, values[0].strip())

            entry_2.delete(0, "end")
            entry_2.insert(0, values[2].strip())


            entry_4.delete(0, "end")
            entry_4.insert(0, values[3].strip())

            entry_5.delete(0, "end")
            entry_5.insert(0, str(values[4]).strip())  # add this line

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def open_dashboard():
    window.destroy()
    script_dir = Path(__file__).resolve().parent
    addpet_path = script_dir / "dashboard.py"
    subprocess.run(["python", str(addpet_path)])

window = Tk()

window.geometry("1048x525")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 525,
    width = 1048,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    1048.0,
    525.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    294.0,
    112.0,
    1030.0,
    509.0,
    fill="#55714F",
    outline="")

canvas.create_rectangle(
    0.0,
    0.0,
    273.0,
    525.0,
    fill="#55714F",
    outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=open_dashboard,
    relief="flat"
)
button_1.place(
    x=38.0,
    y=13.0,
    width=206.0,
    height=33.312255859375
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=search_pet_data,
    relief="flat"
)
button_2.place(
    x=824.0,
    y=59.0,
    width=206.0,
    height=39.736331939697266
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=update_pet_data,
    relief="flat"
)
button_3.place(
    x=38.0,
    y=405.0,
    width=206.0,
    height=39.736331939697266
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=delete_vaccine_allergy_data,
    relief="flat"
)
button_4.place(
    x=38.0,
    y=461.0,
    width=206.0,
    height=39.736331939697266
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=update_pets_data,
    relief="flat"
)
button_5.place(
    x=38.0,
    y=349.0,
    width=206.0,
    height=39.736331939697266
)

canvas.create_text(
    44.0,
    62.0,
    anchor="nw",
    text="Pet name",
    fill="#FFFFFF",
    font=("Inter ExtraBold", 15 * -1)
)

canvas.create_text(
    47.0,
    131.0,
    anchor="nw",
    text="Allergies",
    fill="#FFFFFF",
    font=("Inter ExtraBold", 15 * -1)
)

canvas.create_text(
    47.0,
    195.0,
    anchor="nw",
    text="No. of Vaccines",
    fill="#FFFFFF",
    font=("Inter ExtraBold", 15 * -1)
)

canvas.create_text(
    44.0,
    272.0,
    anchor="nw",
    text="Type of Vaccine",
    fill="#FFFFFF",
    font=("Inter ExtraBold", 15 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    138.0,
    105.5,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FDF2F2",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=59.0,
    y=88.0,
    width=158.0,
    height=33.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    138.0,
    169.5,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#FDF2F2",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=59.0,
    y=152.0,
    width=158.0,
    height=33.0
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    698.5,
    78.5,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#BEC7BC",
    fg="#000716",
    highlightthickness=0
)
entry_3.place(
    x=615.0,
    y=61.0,
    width=167.0,
    height=33.0
)

entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    138.0,
    238.5,
    image=entry_image_4
)
entry_4 = Entry(
    bd=0,
    bg="#FDF2F2",
    fg="#000716",
    highlightthickness=0
)
entry_4.place(
    x=59.0,
    y=221.0,
    width=158.0,
    height=33.0
)

entry_image_5 = PhotoImage(
    file=relative_to_assets("entry_5.png"))
entry_bg_5 = canvas.create_image(
    138.0,
    315.5,
    image=entry_image_5
)
entry_5 = Entry(
    bd=0,
    bg="#FDF2F2",
    fg="#000716",
    highlightthickness=0
)
entry_5.place(
    x=59.0,
    y=298.0,
    width=158.0,
    height=33.0
)


pet_columns = ('#1', '#2', '#3', '#4', '#5')
pet_tree = ttk.Treeview(window, columns=pet_columns, show='headings')
pet_tree.heading('#1', text='Pet Name')
pet_tree.heading('#2', text='Gender')
pet_tree.heading('#3', text='Allergies')
pet_tree.heading('#4', text='No. of Vaccines')
pet_tree.heading('#5', text='Type of Vaccine')

pet_tree.column('#1', width=100, anchor='center')
pet_tree.column('#2', width=80, anchor='center')
pet_tree.column('#3', width=50, anchor='center')
pet_tree.column('#4', width=100, anchor='center')
pet_tree.column('#5', width=100, anchor='center')

pet_tree.place(x=292.0, y=110.0, width=738.0, height=400.0)
pet_tree.bind('<<TreeviewSelect>>', load_selected_pet)

populate_pet_treeview()

window.resizable(False, False)
window.mainloop()
