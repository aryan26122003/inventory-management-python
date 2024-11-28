from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymysql
from employees import connect_database

def treeview_data(tree_view):
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use prabhat_automobiles')
        cursor.execute('SELECT * from category')
        records=cursor.fetchall()
        tree_view.delete(* tree_view.get_children())
        for record in records:
            tree_view.insert('', END, values=record)
    except Exception as e:
         messagebox.showerror('Error',f'Error due to {e}') 
    finally:
        cursor.close()
        connection.close()

def select_data(event,id_entry,name_entry,description_entry,tree_view):
    index=tree_view.selection()
    content=tree_view.item(index)
    actual_content=content['values']
    id_entry.delete(0,END)
    name_entry.delete(0,END)
    description_entry.delete(1.0,END)
    id_entry.insert(0,actual_content[0])
    name_entry.insert(0,actual_content[1])
    description_entry.insert(1.0,actual_content[2])

def clear_fields(id_entry, name_entry, description_entry, tree_view, check=False):
    # Clear input fields
    id_entry.delete(0, END)
    name_entry.delete(0, END)
    description_entry.delete(1.0, END)

    # Deselect items in TreeView if 'check' is True
    if check:
        selected_items = tree_view.selection()
        for item in selected_items:
            tree_view.selection_remove(item)

def delete(tree_view):
    selected = tree_view.selection()
    if not selected:
        messagebox.showerror('Error', 'No row is selected')
    else:
        result = messagebox.askyesno('Confirm', 'Do you really want to delete the record?')
        if result:
            cursor, connection = connect_database()
            if not cursor or not connection:
                return
            try:
                cursor.execute('USE prabhat_automobiles')
                # Fetch the 'id' value from the selected row
                item = tree_view.item(selected[0])
                id = item['values'][0]  # Assuming 'id' is the first column
                cursor.execute('DELETE FROM category WHERE id=%s', (id,))
                connection.commit()
                treeview_data(tree_view)  # Refresh the Treeview after deletion
                messagebox.showinfo('Success', 'category record deleted successfully')
            except Exception as e:
                messagebox.showerror('Error', f'Error due to {e}')
            finally:
                cursor.close()  # Close the cursor
                connection.close()  # Close the connection


def add_category(id,name,description,tree_view):
    if id==''or name==''or description=='':
        messagebox.showerror('Error','all feilds are manadatory to be filled')
    else:
         cursor,connection=connect_database()
         if not cursor or not connection:
            return
    try:

            cursor.execute('use prabhat_automobiles')
            cursor.execute('CREATE TABLE IF NOT EXISTS category (id INT(20) PRIMARY KEY,name VARCHAR(100),description VARCHAR(500))')
            cursor.execute('SELECT * FROM category WHERE id=%s',id)
            if cursor.fetchone():
                messagebox.showerror("Error",'Id already exists')
                return
            cursor.execute('INSERT INTO category VALUES (%s,%s,%s)',(id,name,description.strip()))
            connection.commit()
            messagebox.showinfo('Info','New category id is added')
            treeview_data(tree_view)
    except Exception as e:
            messagebox.showerror('Error',f'Error due to {e}')
    finally:
            cursor.close()
            connection.close()       

def category_form(window):
    global back_button_icon, bg_image

    category_frame = Frame(window, height=700, width=1320, bg='white')
    category_frame.place(x=200, y=130)

    heading_label = Label(category_frame, text='MANAGE CATEGORY DETAILS', font=('times new roman', 16, 'bold'), bg='#0f4d7d', fg='white')
    heading_label.place(x=0, y=0, relwidth=1)

    back_button_icon = PhotoImage(file='arrow.png')
    back_button = Button(category_frame, image=back_button_icon, bd=0, cursor='hand2', bg='white', command=lambda: category_frame.place_forget())
    back_button.place(x=10, y=35)

    bg_image = PhotoImage(file='logo.png')
    label = Label(category_frame, image=bg_image)
    label.place(x=30, y=100)

    details_frame = Frame(category_frame, bg="white")
    details_frame.place(x=640, y=70)

    id_label = Label(details_frame, text='Category ID', font=('times new roman', 14, 'bold'), bg='white')
    id_label.grid(row=0, column=0, padx=30, pady=60, sticky='w')
    id_entry = Entry(details_frame, font=('times new roman', 14, 'bold'), bg='lightyellow')
    id_entry.grid(row=0, column=1)

    name_label = Label(details_frame, text='Category Name', font=('times new roman', 14, 'bold'), bg='white')
    name_label.grid(row=1, column=0, padx=30, sticky='w')
    name_entry = Entry(details_frame, font=('times new roman', 14, 'bold'), bg='lightyellow')
    name_entry.grid(row=1, column=1)

    description_label = Label(details_frame, text='Description', font=('times new roman', 14, 'bold'), bg='white')
    description_label.grid(row=3, column=0, padx=(30, 60), pady=25, sticky='nw')
    description_entry = Text(details_frame, font=('times new roman', 14, 'bold'), width=20, height=4, bd=2, bg='lightyellow')
    description_entry.grid(row=3, column=1, pady=15)

    button_frame = Frame(category_frame, bg="white")
    button_frame.place(x=800, y=380)

    add_button = Button(button_frame, text='ADD', font=('times new roman', 14, 'bold'), bg='#010c48', width=8, cursor='hand2', fg='white', bd=0,command=lambda:add_category(id_entry.get(),name_entry.get(),description_entry.get(1.0,END).strip(),tree_view))
    add_button.grid(row=0, column=0, padx=(32, 0))

    clear_button = Button(button_frame, text='CLEAR', font=('times new roman', 14, 'bold'), bg='#010c48', width=8, cursor='hand2', fg='white', bd=0,command=lambda:clear_fields(id_entry, name_entry, description_entry, tree_view,TRUE))
    clear_button.grid(row=0, column=1, padx=20)
    
    delete_button = Button(button_frame, text='DELETE', font=('times new roman', 14, 'bold'), bg='#010c48', width=8, cursor='hand2', fg='white', bd=0,command=lambda:delete(tree_view))
    delete_button.grid(row=0, column=2, padx=20)

    treeview_frame = Frame(category_frame, bg='yellow')
    treeview_frame.place(x=650, y=450, height=200, width=600)

    # Scrollbars for the Treeview
    treeview_scroll_y = Scrollbar(treeview_frame, orient=VERTICAL)
    treeview_scroll_y.pack(side=RIGHT, fill=Y)

    treeview_scroll_x = Scrollbar(treeview_frame, orient=HORIZONTAL)
    treeview_scroll_x.pack(side=BOTTOM, fill=X)

    # Treeview with Scrollbars
    tree_view = ttk.Treeview(treeview_frame, columns=("ID", "Name", "Description"), show="headings",
                             yscrollcommand=treeview_scroll_y.set, xscrollcommand=treeview_scroll_x.set)
    tree_view.heading("ID", text="Category ID")
    tree_view.heading("Name", text="Category Name")
    tree_view.heading("Description", text="Description")

    # Configure Scrollbars
    treeview_scroll_y.config(command=tree_view.yview)
    treeview_scroll_x.config(command=tree_view.xview)

    tree_view.pack(fill=BOTH, expand=True)

    treeview_data(tree_view)
    tree_view.bind('<ButtonRelease-1>',lambda event :select_data(event,id_entry,name_entry,description_entry,tree_view))