from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymysql
from employees import connect_database

def select_data(event,category_combobox,supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox,tree_view):
    index=tree_view.selection()
    content=tree_view.item(index)
    actual_content=content['values']
    name_entry.delete(0,END)
    price_entry.delete(0,END)
    quantity_entry.delete(0,END)
    category_combobox.set(actual_content[1])
    supplier_combobox.set(actual_content[2])
    name_entry.insert(0,actual_content[3])
    price_entry.insert(0,actual_content[4])
    quantity_entry.insert(0,actual_content[5])
    status_combobox.set(actual_content[6])

def treeview_data(tree_view):
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use prabhat_automobiles')
        cursor.execute('SELECT * from product')
        records=cursor.fetchall()
        tree_view.delete(* tree_view.get_children())
        for record in records:
            tree_view.insert('', END, values=record)
    except Exception as e:
         messagebox.showerror('Error',f'Error due to {e}') 
    finally:
        cursor.close()
        connection.close()

def fetch_supplier_category(category_combobox,supplier_combobox):
     category_option=[]
     supplier_option=[]
     cursor,connection = connect_database()
     if not cursor or not connection:
          return
     cursor.execute('use prabhat_automobiles')
     cursor.execute('SELECT name from category')
     names=cursor.fetchall()
     if len(names)>0:
          category_combobox.set('Select')
     for name in names:
        category_option.append(name[0])
     category_combobox.config(values=category_option)
     
     cursor.execute('SELECT name from supplier')
     supplier_name=cursor.fetchall()
     if len(supplier_name)>0:
          supplier_combobox.set('Select')
     for supp in supplier_name:
        supplier_option.append(supplier_name[0])
     supplier_combobox.config(values=supplier_option)



def add(category, supplier, name, price, quantity, status, tree_view):
    if category == "Empty":
        messagebox.showerror('Error', 'Please add category')
    elif supplier == "Empty":
        messagebox.showerror('Error', 'Please add supplier')
    elif category == "Select" or supplier =="Select" or name =="" or price =="" or quantity =="" or status == "Selct Status":
        messagebox.showerror('Error', 'Please fill all fields')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('USE prabhat_automobiles')
            cursor.execute('CREATE TABLE IF NOT EXISTS product (id INT AUTO_INCREMENT PRIMARY KEY, category VARCHAR(100),supplier VARCHAR(100), name VARCHAR(100), price DECIMAL(10,2), quantity INT(20), status VARCHAR(20))')
            cursor.execute('SELECT * from product WHERE category=%s AND supplier=%s AND name=%s',(category,supplier,name))
            existing_product=cursor.fetchone()
            if existing_product:
                messagebox.showerror('Error', 'Product already exists')
                return
            cursor.execute('INSERT INTO product (category, supplier, name, price, quantity, status) VALUES (%s, %s, %s, %s, %s, %s)',(category, supplier, name, price, quantity, status))
            connection.commit()
            messagebox.showinfo('Info', 'New product is added')
            treeview_data(tree_view)
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()

def update(category, supplier, name, price, quantity, status, tree_view):
    # Get the selected item
    index = tree_view.selection()
    if not index:
        messagebox.showerror('Error', 'Please select a product to update')
        return
    
    dict = tree_view.item(index)
    content = dict['values']
    id = content[0]

    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    try:
        cursor.execute('USE prabhat_automobiles')

        # Fetch current product data
        cursor.execute('SELECT * FROM product WHERE id=%s', (id,))
        current_data = cursor.fetchone()

        if current_data is None:
            messagebox.showerror('Error', 'No matching product found for the given ID')
            return

        # Compare current and new data
        current_data = list(current_data[1:])  # Exclude ID
        current_data[3] = str(current_data[3])  # Convert price to string for comparison
        new_data = [category, supplier, name, price, int(quantity), status]

        if current_data == new_data:
            messagebox.showinfo('Info', 'No changes detected')
            return

        # Update the product in the database
        cursor.execute(
            'UPDATE product SET category=%s, supplier=%s, name=%s, price=%s, quantity=%s, status=%s WHERE id=%s',
            (category, supplier, name, price, quantity, status, id)
        )
        connection.commit()
        messagebox.showinfo('Info', 'Product updated successfully')

        # Refresh the tree view
        treeview_data(tree_view)

    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()


def clear_fields(category_combobox,supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox, tree_view, check=False):
    # Clear input fields
    category_combobox.set('Select')
    supplier_combobox.set('Select')
    name_entry.delete(0, END)
    price_entry.delete(0, END)
    quantity_entry.delete(0, END)
    status_combobox.set('Select Status')
    

    # Deselect items in TreeView if 'check' is True
    if check:
        selected_items = tree_view.selection()
        for item in selected_items:
            tree_view.selection_remove(item)



def delete(tree_view, category_combobox, supplier_combobox, name_entry, price_entry, quantity_entry, status_combobox):
    # Ensure at least one item is selected
    selected = tree_view.selection()
    if not selected:
        messagebox.showerror('Error', 'No row is selected')
        return

    # Confirm deletion
    result = messagebox.askyesno('Confirm', 'Do you really want to delete the selected record?')
    if not result:
        return

    # Get the selected item's ID
    item = tree_view.item(selected[0])
    values = item.get('values')
    if not values or len(values) == 0:
        messagebox.showerror('Error', 'No valid data selected for deletion')
        return

    # Assuming the first column (values[0]) contains the ID
    product_id = values[0]

    # Delete the record from the database
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('USE prabhat_automobiles')
        cursor.execute('DELETE FROM product WHERE id=%s', (product_id,))
        connection.commit()

        # Refresh UI
        clear_fields(category_combobox, supplier_combobox, name_entry, price_entry, quantity_entry, status_combobox)
        treeview_data(tree_view)  # Refresh the tree view
        messagebox.showinfo('Success', 'Product record deleted successfully')
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()


    


def product_form(window):
    global back_button_icon

    product_frame = Frame(window, height=700, width=1320, bg='white')
    product_frame.place(x=200, y=130)

    back_button_icon = PhotoImage(file='arrow.png')
    back_button = Button(product_frame, image=back_button_icon, bd=0, cursor='hand2', bg='white', command=lambda: product_frame.place_forget())
    back_button.place(x=10, y=35)



    left_frame=Frame(product_frame,bg='white',relief=RIDGE)
    left_frame.place(x=90,y=70)

    heading_label = Label(left_frame, text='MANAGE PRODUCT DETAILS', font=('times new roman', 16, 'bold'), bg='#0f4d7d', fg='white')
    heading_label.grid(row=0,columnspan=2,sticky='we')


    
    category_label = Label(left_frame, text='Category', font=('times new roman', 16, 'bold'), bg='white')
    category_label.grid(row=1, column=0, padx=30, pady=20, sticky='w')

    category_combobox=ttk.Combobox(left_frame,font=('times new roman',14),state='readonly')
    category_combobox.set('Empty')
    category_combobox.grid(row=1,column=1)


    supplier_label = Label(left_frame, text='Supplier', font=('times new roman', 16, 'bold'), bg='white')
    supplier_label.grid(row=2, column=0, padx=30, pady=20, sticky='w')

    supplier_combobox=ttk.Combobox(left_frame,font=('times new roman',14),state='readonly')
    supplier_combobox.set('Empty')
    supplier_combobox.grid(row=2,column=1)


    name_label=Label(left_frame,text='Name',font=('times new roman',14,'bold'),bg='white')
    name_label.grid(row=3,column=0,padx=30,pady=15,sticky='w')
    name_entry=Entry(left_frame,font=('times new roman',14,'bold'))
    name_entry.grid(row=3,column=1)

    price_label=Label(left_frame,text='Price',font=('times new roman',14,'bold'),bg='white')
    price_label.grid(row=4,column=0,padx=30,pady=15,sticky='w')
    price_entry=Entry(left_frame,font=('times new roman',14,'bold'))
    price_entry.grid(row=4,column=1)

    
    quantity_label=Label(left_frame,text='Quantity',font=('times new roman',14,'bold'),bg='white')
    quantity_label.grid(row=5,column=0,padx=30,pady=15,sticky='w')
    quantity_entry=Entry(left_frame,font=('times new roman',14,'bold'))
    quantity_entry.grid(row=5,column=1)

    
    status_label = Label(left_frame, text='Status', font=('times new roman', 16, 'bold'), bg='white')
    status_label.grid(row=7, column=0, padx=30, pady=20, sticky='w')

    status_combobox=ttk.Combobox(left_frame,values=('Active','Inactive'),font=('times new roman',14),state='readonly')
    status_combobox.set('Select Status')
    status_combobox.grid(row=7,column=1)


    button_frame=Frame(left_frame,bg='white')
    button_frame.grid(row=10,column=0,columnspan=2,pady=30)

    add_button = Button(button_frame,text='Add',font=('times new roman',14),width=8, fg='white',bg='#0f4d7d',command=lambda:add(category_combobox.get(),supplier_combobox.get(),name_entry.get(),price_entry.get() ,quantity_entry.get(),status_combobox.get(),tree_view))
    add_button.grid(row=0,column=0,padx=10)
    

    update_button = Button(button_frame,text='Update',font=('times new roman',14),width=8, fg='white',bg='#0f4d7d',command=lambda:update(category_combobox.get(),supplier_combobox.get(),name_entry.get(),price_entry.get(),quantity_entry.get(),status_combobox.get(),tree_view))
    update_button.grid(row=0,column=1,padx=10)

    delete_button = Button(button_frame,text='Delete',font=('times new roman',14),width=8, fg='white',bg='#0f4d7d',command=lambda:delete(category_combobox,supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox,tree_view))
    delete_button.grid(row=0,column=2,padx=10)

    clear_button = Button(button_frame,text='Clear',font=('times new roman',14),width=8, fg='white',bg='#0f4d7d',command=lambda:clear_fields(category_combobox,supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox,tree_view,TRUE))
    clear_button.grid(row=0,column=3,padx=10)


    search_frame=LabelFrame(product_frame,text='Search Product',font=('times new roman',14))
    search_frame.place(x=640,y=70)

    search_combobox=ttk.Combobox(search_frame,values=('Category','Supplier','Name','Status'),state='readonly', width=16,font=('times new roman',14,'bold'))
    search_combobox.set('Search By')
    search_combobox.grid(row=0,column=0,padx=10,pady=10)

    search_entry= Entry(search_frame,font=('times new roman',14),bg='light yellow')
    search_entry.grid(row=0,column=1,padx=10,pady=10)

    search_button = Button(search_frame,text='Search',font=('times new roman',14),width=8, fg='white',bg='#0f4d7d')
    search_button.grid(row=0,column=2,padx=10)

    Showall_button = Button(search_frame,text='Show all',font=('times new roman',14),width=8, fg='white',bg='#0f4d7d')
    Showall_button.grid(row=0,column=3,padx=10)

    treeview_frame=Frame(product_frame,)
    treeview_frame.place(x=630,y=200 ,width=640,height=470)



     # Scrollbars for the Treeview
    treeview_scroll_y = Scrollbar(treeview_frame, orient=VERTICAL)
    treeview_scroll_y.pack(side=RIGHT, fill=Y)

    treeview_scroll_x = Scrollbar(treeview_frame, orient=HORIZONTAL)
    treeview_scroll_x.pack(side=BOTTOM, fill=X)

    # Treeview with Scrollbars
    tree_view = ttk.Treeview(treeview_frame, columns=("id","category","supplier", "name", "price","quantity",'status'), show="headings",
                             yscrollcommand=treeview_scroll_y.set, xscrollcommand=treeview_scroll_x.set)
    tree_view.heading('id',text='Id')
    tree_view.heading("category", text="Category")
    tree_view.heading("supplier", text="Supplier")
    tree_view.heading("name", text="Name")
    tree_view.heading("price", text="Price")
    tree_view.heading("quantity", text="Quantity")
    tree_view.heading("status", text="Status")

    # Configure Scrollbars
    treeview_scroll_y.config(command=tree_view.yview)
    treeview_scroll_x.config(command=tree_view.xview)

    tree_view.pack(fill=BOTH, expand=True)

    fetch_supplier_category(category_combobox,supplier_combobox)
    treeview_data(tree_view)
    tree_view.bind('<ButtonRelease-1>',lambda event :select_data(event,category_combobox,supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox,tree_view))



