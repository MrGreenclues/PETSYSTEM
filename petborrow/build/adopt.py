from pathlib import Path
import subprocess
from tkinter import Tk, Canvas, Button, PhotoImage, Label, messagebox, Entry
from tkinter import ttk
import mysql.connector

from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\xampp\htdocs\petborrow\build\assets\frame3")

def update_pet_data():
    selected_item = pet_tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a pet to update")
        return

    petname = entry_1.get().strip()
    owner = entry_2.get().strip()
    address = entry_4.get().strip()
    contact = entry_5.get().strip()

    if not (petname and owner and address and contact):
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

        # Get the original petname from selected Treeview item
        original_petname = pet_tree.item(selected_item)['values'][0]

        # Update query now includes setting status = 'Adopted'
        sql = "UPDATE pet SET owner=%s, address=%s, contact=%s, status='Adopted' WHERE petname=%s"
        val = (owner, address, contact, original_petname)
        mycursor.execute(sql, val)
        mydb.commit()

        messagebox.showinfo("Success", "Pet data updated and status set to Adopted!")
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


def add_pet_data():
    selected_item = adopt_tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a pet to update")
        return

    petname = entry_1.get().strip()
    owner = entry_2.get().strip()
    address = entry_4.get().strip()
    contact = entry_5.get().strip()

    if not (petname and owner and address and contact):
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
        original_petname = adopt_tree.item(selected_item)['values'][0]

        # Update query using original_petname to locate the correct row
        sql = "UPDATE pet SET  owner=%s, address=%s, contact=%s WHERE petname=%s"
        val = (  owner, address, contact, original_petname)
        mycursor.execute(sql, val)
        mydb.commit()

        messagebox.showinfo("Success", "Pet data added successfully!")
        populate_adopt_treeview()

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

def fetch_pet_data():
    try:
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='breed'
        )
        mycursor = mydb.cursor()
        # Fetch only pets without an owner
        mycursor.execute("""
            SELECT petname, gender, age,species, owner, address, contact 
            FROM pet 
            WHERE owner IS NULL OR owner = ''
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
            SELECT petname, owner, address, contact
            FROM pet
            WHERE petname LIKE %s OR owner LIKE %s OR address LIKE %s OR contact LIKE %s
        """
        like_keyword = f"%{keyword}%"
        mycursor.execute(query, (like_keyword, like_keyword, like_keyword, like_keyword))
        rows = mycursor.fetchall()

      

        for row in adopt_tree.get_children():
            adopt_tree.delete(row)

        # Insert search results
        for item in rows:
            adopt_tree.insert("", "end", values=item)


    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
    finally:
        if mycursor:
            mycursor.close()
        if mydb:
            mydb.close()


def fetch_adoption_data():
    try:
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='breed'
        )
        mycursor = mydb.cursor()
        # Fetch only rows where the owner is not NULL or empty
        mycursor.execute("""
            SELECT petname, owner, address, contact 
            FROM pet 
            WHERE owner IS NOT NULL AND owner != ''
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



# Placeholder handlers
def load_selected_pet(event=None):
    selected_item = pet_tree.selection()
    if selected_item:
        values = pet_tree.item(selected_item[0], 'values')
        if len(values) > 0:
            entry_1.delete(0, "end")
            entry_1.insert(0, values[0].strip())

def load_selected_adopt(event=None):
    selected_item = adopt_tree.selection()
    if selected_item:
        values = adopt_tree.item(selected_item[0], 'values')
        if len(values) >= 4:
            entry_1.delete(0, "end")
            entry_1.insert(0, values[0].strip())
            entry_2.delete(0, "end")
            entry_2.insert(0, values[1].strip())
            entry_4.delete(0, "end")
            entry_4.insert(0, str(values[2]).strip())
            entry_5.delete(0, "end")
            entry_5.insert(0, values[3].strip())




def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def populate_pet_treeview():
    for row in pet_tree.get_children():
        pet_tree.delete(row)
    data = fetch_pet_data()
    for item in data:
        pet_tree.insert("", "end", values=item)


def populate_adopt_treeview():
    for row in adopt_tree.get_children():
        adopt_tree.delete(row)
    data = fetch_adoption_data()
    for item in data:
        adopt_tree.insert("", "end", values=item)

def open_managepet():
    window.destroy()
    script_dir = Path(__file__).resolve().parent
    addpet_path = script_dir / "managepet.py"
    subprocess.run(["python", str(addpet_path)])

def open_healhtpet():
    window.destroy()
    script_dir = Path(__file__).resolve().parent
    addpet_path = script_dir / "health.py"
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
    command=open_managepet,
    relief="flat"
)
button_1.place(
    x=38.0,
    y=27.687744140625,
    width=206.0,
    height=44.72616195678711
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
    command=open_healhtpet,
    relief="flat"
)
button_3.place(
    x=38.0,
    y=471.061279296875,
    width=206.0,
    height=39.736331939697266
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=add_pet_data,
    relief="flat"
)
button_4.place(
    x=38.0,
    y=422.0,
    width=206.0,
    height=37.8887939453125
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=update_pet_data,
    relief="flat"
)
button_5.place(
    x=38.0,
    y=371.0,
    width=206.0,
    height=39.736331939697266
)

canvas.create_text(
    44.0,
    86.0,
    anchor="nw",
    text="Pet name",
    fill="#FFFFFF",
    font=("Inter ExtraBold", 15 * -1)
)

canvas.create_text(
    44.0,
    161.0,
    anchor="nw",
    text="Owner",
    fill="#FFFFFF",
    font=("Inter ExtraBold", 15 * -1)
)

canvas.create_text(
    44.0,
    227.0,
    anchor="nw",
    text="Shelter Address",
    fill="#FFFFFF",
    font=("Inter ExtraBold", 15 * -1)
)

canvas.create_text(
    44.0,
    295.0,
    anchor="nw",
    text="Contact No.",
    fill="#FFFFFF",
    font=("Inter ExtraBold", 15 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    138.0,
    130.5,
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
    y=113.0,
    width=158.0,
    height=33.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    138.0,
    201.5,
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
    y=184.0,
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
    141.0,
    270.5,
    image=entry_image_4
)
entry_4 = Entry(
    bd=0,
    bg="#FDF2F2",
    fg="#000716",
    highlightthickness=0
)
entry_4.place(
    x=62.0,
    y=253.0,
    width=158.0,
    height=33.0
)

entry_image_5 = PhotoImage(
    file=relative_to_assets("entry_5.png"))
entry_bg_5 = canvas.create_image(
    141.0,
    339.5,
    image=entry_image_5
)
entry_5 = Entry(
    bd=0,
    bg="#FDF2F2",
    fg="#000716",
    highlightthickness=0
)
entry_5.place(
    x=62.0,
    y=322.0,
    width=158.0,
    height=33.0
)


# Pet Treeview
pet_columns = ('#1', '#2', '#3', '#4')
pet_tree = ttk.Treeview(window, columns=pet_columns, show='headings')
pet_tree.heading('#1', text='Pet Name')
pet_tree.heading('#2', text='Gender')
pet_tree.heading('#3', text='Age')
pet_tree.heading('#4', text='Species')

pet_tree.column('#1', width=100, anchor='center')
pet_tree.column('#2', width=80, anchor='center')
pet_tree.column('#3', width=50, anchor='center')
pet_tree.column('#4', width=100, anchor='center')

pet_tree.place(x=292.0, y=110.0, width=738.0, height=190.0)
pet_tree.bind('<<TreeviewSelect>>', load_selected_pet)

# Adoption Treeview
adopt_columns = ('#1', '#2', '#3', '#4')
adopt_tree = ttk.Treeview(window, columns=adopt_columns, show='headings')
adopt_tree.heading('#1', text='Pet Name')
adopt_tree.heading('#2', text='Owner Name')
adopt_tree.heading('#3', text='Address')
adopt_tree.heading('#4', text='Contact')

adopt_tree.column('#1', width=100, anchor='center')
adopt_tree.column('#2', width=100, anchor='center')
adopt_tree.column('#3', width=150, anchor='center')
adopt_tree.column('#4', width=100, anchor='center')

adopt_tree.place(x=292.0, y=320.0, width=738.0, height=190.0)
adopt_tree.bind('<<TreeviewSelect>>', load_selected_adopt)

# Populate data into treeviews
populate_pet_treeview()
populate_adopt_treeview()

window.resizable(False, False)
window.mainloop()
