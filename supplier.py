from tkinter import *
from tkinter import ttk
from tkinter import messagebox 
from employees import connect_database
import pymysql


def select_data(event,invoice_entry,name_entry,contact_entry,description_entry,tree_view):
    index=tree_view.selection()
    content=tree_view.item(index)
    actual_content=content['values']
    invoice_entry.delete(0,END)
    name_entry.delete(0,END)
    contact_entry.delete(0,END)
    description_entry.delete(1.0,END)
    invoice_entry.insert(0,actual_content[0])
    name_entry.insert(0,actual_content[1])
    contact_entry.insert(0,actual_content[2])
    description_entry.insert(1.0,actual_content[3])


def treeview_data(tree_view):
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use prabhat_automobiles')
        cursor.execute('SELECT * from supplier')
        records=cursor.fetchall()
        tree_view.delete(* tree_view.get_children())
        for record in records:
            tree_view.insert('', END, values=record)
    except Exception as e:
         messagebox.showerror('Error',f'Error due to {e}') 
    finally:
        cursor.close()
        connection.close()

        


def add_supplier(invoice,name,contact,description,tree_view):
    if invoice==''or name==''or contact==''or description.strip()=='':
        messagebox.showerror('Error','All fields are required')
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
    try:

        cursor.execute('use prabhat_automobiles')
        cursor.execute('CREATE TABLE IF NOT EXISTS supplier (invoice INT(20) PRIMARY KEY,name VARCHAR(100),contact VARCHAR(15),description VARCHAR(500))')
        cursor.execute('SELECT * FROM supplier WHERE invoice=%s',invoice)
        if cursor.fetchone():
            messagebox.showerror("Error",'Invoice no. already exists')
            return
        cursor.execute('INSERT INTO supplier VALUES (%s,%s,%s,%s)',(invoice,name,contact,description.strip()))
        connection.commit()
        messagebox.showinfo('Info',' Supplier Data is instered')
        treeview_data(tree_view)
    except Exception as e:
        messagebox.showerror('Error',f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()    


def update(invoice,name,contact,description,tree_view):
    index=tree_view.selection()
    
    if not index:
         messagebox.showerror('Error','Please select the supplier data you want to update')
         return
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    cursor.execute('use prabhat_automobiles')
    cursor.execute('SELECT * FROM supplier WHERE invoice=%s',invoice)
    current_data=cursor.fetchone()
    current_data=current_data[1:]

    new_data=(name,contact,description)
    if current_data==new_data:
        messagebox.showinfo('Info','No changes detected')
        return
    
    cursor.execute('UPDATE supplier SET name=%s,contact=%s,description=%s WHERE invoice=%s',(name,contact,description,invoice))
    connection.commit()
    messagebox.showinfo('Info','Data is updated')
    treeview_data(tree_view)

def clear_fields(invoice_entry, name_entry, contact_entry, description_entry, tree_view, check=False):
    # Clear input fields
    invoice_entry.delete(0, END)
    name_entry.delete(0, END)
    contact_entry.delete(0, END)
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
                # Fetch the 'invoice' value from the selected row
                item = tree_view.item(selected[0])
                invoice = item['values'][0]  # Assuming 'invoice' is the first column
                cursor.execute('DELETE FROM supplier WHERE invoice=%s', (invoice,))
                connection.commit()
                treeview_data(tree_view)  # Refresh the Treeview after deletion
                messagebox.showinfo('Success', 'Supplier record deleted successfully')
            except Exception as e:
                messagebox.showerror('Error', f'Error due to {e}')
            finally:
                cursor.close()  # Close the cursor
                connection.close()  # Close the connection


def supplier_form(window):
    global back_button_icon
    supplier_frame=Frame(window,height=700,width=1320,bg='white')
    supplier_frame.place(x=200, y=130)

    heading_label=Label(supplier_frame,text='MANAGE SUPPLIER DETAILS',font=('times new roman',16,'bold'),bg='#0f4d7d',fg='white')
    heading_label.place(x=0,y=0,relwidth=1)

    back_button_icon=PhotoImage(file='arrow.png')
    back_button=Button(supplier_frame,image=back_button_icon,bd=0,cursor='hand2',bg='white',command=lambda:supplier_frame.place_forget())
    back_button.place(x=10,y=35)

    left_frame=Frame(supplier_frame,bg='white')
    left_frame.place(x=0,y=70,)

    invoice_label=Label(left_frame,text='Invoice No.',font=('times new roman',14,'bold'),bg='white')
    invoice_label.grid(row=0,column=0,padx=(30,80),pady=60,sticky='w')
    invoice_entry=Entry(left_frame,font=('times new roman',14,'bold'),bg='lightyellow')
    invoice_entry.grid(row=0,column=1)

    name_label=Label(left_frame,text='Name',font=('times new roman',14,'bold'),bg='white')
    name_label.grid(row=1,column=0,padx=(30,60),sticky='w')
    name_entry=Entry(left_frame,font=('times new roman',14,'bold'),bg='lightyellow')
    name_entry.grid(row=1,column=1)

    contact_label=Label(left_frame,text='Contact',font=('times new roman',14,'bold'),bg='white')
    contact_label.grid(row=2,column=0,padx=(30,60),pady=15,sticky='w')
    contact_entry=Entry(left_frame,font=('times new roman',14,'bold'),bg='lightyellow')
    contact_entry.grid(row=2,column=1)


    description_label=Label(left_frame,text='Description',font=('times new roman',14,'bold'),bg='white')
    description_label.grid(row=3,column=0,padx=(30,60),pady=25,sticky='nw')
    description_entry=Text(left_frame,font=('times new roman',14,'bold'),width=20,height=4,bd=2,bg='lightyellow')
    description_entry.grid(row=3,column=1,pady=15)

    button_frame=Frame(left_frame,bg="white")
    button_frame.grid(row=4,columnspan=2,padx=(30,60),pady=25)

    add_button=Button(button_frame,text='ADD',font=('times new roman',14,'bold'),bg='#010c48',width=8,cursor='hand2',fg='white',bd=0,command=lambda:add_supplier(invoice_entry.get(),contact_entry.get(),name_entry.get(),description_entry.get(1.0,END).strip(),tree_view))
    add_button.grid(row=0,column=1,padx=20)

    update_button=Button(button_frame,text='UPDATE',font=('times new roman',14,'bold'),bg='#010c48',width=8,cursor='hand2',fg='white',bd=0 ,command=lambda:update(invoice_entry.get(),contact_entry.get(),name_entry.get(),description_entry.get(1.0,END).strip(),tree_view))
    update_button.grid(row=0,column=2,padx=20)

    delete_button=Button(button_frame,text='DELETE',font=('times new roman',14,'bold'),bg='#010c48',width=8,cursor='hand2',fg='white',bd=0,command=lambda:delete(tree_view))
    delete_button.grid(row=0,column=3,padx=20)

    clear_button = Button(button_frame,text='CLEAR',font=('times new roman', 14, 'bold'),bg='#010c48',width=8,cursor='hand2',fg='white',bd=0,command=lambda: clear_fields(invoice_entry, name_entry, contact_entry, description_entry, tree_view, check=True))
    clear_button.grid(row=0,column=4,padx=20)

########
    right_frame=Frame(supplier_frame,bg='white')
    right_frame.place(x=640,y=90,width=650,height=500)



    search_frame=Frame(right_frame,bg='white')
    search_frame.pack(pady=(0,20))

    num_label=Label(search_frame,text='Invoice No.',font=('times new roman',14),bg='white')
    num_label.grid(row=0,column=0,padx=(0,20),sticky='w',pady=0)
    search_entry=Entry(search_frame,font=('times new roman',14),bg='lightyellow')
    search_entry.grid(row=0,column=1)

    search_button=Button(search_frame,text='Search',font=('times new roman',14),bg='#010c48',width=8,cursor='hand2',fg='white',bd=0)
    search_button.grid(row=0,column=2,padx=20)

    show_button=Button(search_frame,text='Show All',font=('times new roman',14),bg='#010c48',width=8,cursor='hand2',fg='white',bd=0)
    show_button.grid(row=0,column=3,padx=20)

    scrolly=Scrollbar(right_frame,orient=VERTICAL)
    scrollx=Scrollbar(right_frame,orient=HORIZONTAL)

    tree_view=ttk.Treeview(right_frame,columns=('invoice','name','contact','description'),show='headings'
                           ,yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
    scrolly.pack(side=RIGHT,fill=Y)
    scrollx.pack(side=BOTTOM,fill=X)
    scrollx.config(command=tree_view.xview)
    scrolly.config(command=tree_view.yview)
    tree_view.pack(padx=20,fill=BOTH,expand=1)

    tree_view.heading('invoice',text='Invoice Id')
    tree_view.heading('name',text='Supplier Name')
    tree_view.heading('contact',text='Supplier contact')
    tree_view.heading('description',text='Description')

    tree_view.column('invoice',width=60)
    tree_view.column('name',width=140)
    tree_view.column('contact',width=180)
    tree_view.column('description',width=300)


    treeview_data(tree_view)
    tree_view.bind('<ButtonRelease-1>',lambda event :select_data(event,invoice_entry,name_entry,contact_entry,description_entry,tree_view))