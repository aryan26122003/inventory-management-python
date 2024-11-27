from tkinter import*
from tkinter import ttk,messagebox
from tkcalendar import DateEntry
import pymysql 



import pymysql
from tkinter import messagebox

def connect_database():
    try:
        connection = pymysql.connect(host='localhost', user='root', password='123456')
        cursor = connection.cursor()
    except:
        messagebox.showerror("Error", "Connection failed")
        return None, None
    
    return cursor, connection

def create_database_table():
        cursor, connection = connect_database()
        cursor.execute('CREATE DATABASE IF NOT EXISTS prabhat_automobiles')
        cursor.execute('USE prabhat_automobiles')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees_data (
            empid INT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(50),
            gender VARCHAR(50),
            dob VARCHAR(30),
            contact VARCHAR(30),
            employment_type VARCHAR(50),
            work_shift VARCHAR(50),
            address VARCHAR(100),
            doj VARCHAR(30),
            salary VARCHAR(50),
            user_type VARCHAR(50),
            password VARCHAR(50),
            education VARCHAR(30)
        )
        ''')
   

def treeview_data():
    cursor,connection=connect_database()

    if not cursor or not connection:
        return
    cursor.execute('use prabhat_automobiles')
    try:    
        cursor.execute('SELECT * FROM employees_data')
        employee_records=cursor.fetchall()
        employee_treeview.delete(*employee_treeview.get_children())
        for record in employee_records:
            employee_treeview.insert('',END,values=record)
    except Exception as e:
        messagebox.showerror('Error',f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()   



def select_data(event,empid_entry, name_entry, email_entry, contact_entry, 
                gender_combobox, dob_date_entry, employment_type_combobox, 
                work_shift_combobox, address_text, doj_date_entry, 
                salary_entry, user_type_combobox, password_entry, 
                eductaion_combobox):
    index=employee_treeview.selection()
    content=employee_treeview.item(index)
    row=content['values']
    clear_fields(empid_entry, name_entry, email_entry, contact_entry, 
                gender_combobox, dob_date_entry, employment_type_combobox, 
                work_shift_combobox, address_text, doj_date_entry, 
                salary_entry, user_type_combobox, password_entry, 
                eductaion_combobox,FALSE)


          #data placing 
    empid_entry.insert(0,row[0])
    name_entry.insert(0,row[1])
    email_entry.insert(0,row[2])
    contact_entry.insert(0,row[3])
    gender_combobox.set(row[4])
    dob_date_entry.set_date(row[5])
    employment_type_combobox.set(row[6])
    work_shift_combobox.set(row[7])
    address_text.insert(1.0,row[8])
    doj_date_entry.set_date(row[9])
    salary_entry.insert(0,row[10])
    user_type_combobox.set(row[11])
    password_entry.insert(0,row[12])
    eductaion_combobox.set(row[13])



   




def add_employee(empid, name, email, contact, gender, dob, employment_type, education, work_shift, address, doj, salary, user_type, password):
    if (empid == '' or name == '' or email == '' or gender == 'Select Gender' or contact == '' or employment_type == 'Select Type' or education == 'Select Education' or work_shift == 'Select Shift' or address == '\n' or salary == '' or user_type == '' or password == ''):
        messagebox.showerror("Error", "Please fill all the fields")
    else:
        cursor, connection = connect_database()
        
        # Check if the connection was successful
        if not cursor or not connection:
            return  # Exit the function if the connection failed
        cursor.execute('USE prabhat_automobiles')
        try:
              # Set the database to use
            cursor.execute('SELECT empid from employees_data WHERE empid=%s', (empid,))
            if cursor.fetchone():
                messagebox.showerror('Error', 'Employee ID already exists')
                return
            
            address=address.strip()
            cursor.execute('INSERT INTO employees_data VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                               (empid, name, email, contact, gender, dob, employment_type, education, work_shift, address, doj, salary, user_type, password))
            connection.commit()
            treeview_data()  # Refresh the treeview
            messagebox.showinfo("Success", "Employee added successfully")
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            cursor.close()  # Close the cursor
            connection.close()  # Close the connection

def update_employee(empid, name, email, contact, gender, dob, employment_type, education, work_shift, address, doj, salary, user_type, password):
    selected = employee_treeview.selection()
    if not selected:
        messagebox.showerror('Error', 'Select an employee to update')
        return
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
    try:    
            cursor.execute('USE prabhat_automobiles')
            cursor.execute('SELECT *from employees_data WHERE empid=%s',(empid,))
            current_data=cursor.fetchone()
            current_data=current_data[1:]
            address=address.strip()
            new_data=(empid, name, email, contact, gender, dob, employment_type, education, work_shift, address, doj, salary, user_type, password,)
            

            if current_data==new_data:
                messagebox.showinfo('Information', 'No changes made')
                return
    
            cursor.execute('''UPDATE employees_data SET name=%s, email=%s, gender=%s, dob=%s, contact=%s, employment_type=%s, education=%s, work_shift=%s, address=%s, doj=%s, salary=%s, user_type=%s, password=%s WHERE empid=%s''',
                       (name, email, gender, dob, contact, employment_type, education, work_shift, address, doj, salary, user_type, password, empid))
        
            connection.commit()
            treeview_data()  # Refresh the treeview
            messagebox.showinfo('Success', 'Employee data updated successfully')
    except Exception as e:
                messagebox.showerror('Error', f'Error due to {e}')
    finally:
            cursor.close()  # Close the cursor
            connection.close()  # Close the connection

def delete_employee(empid,):

    selected = employee_treeview.selection()
    if not selected:
        messagebox.showerror('Error', 'no row is selected')
    else: 
        result=messagebox.askyesno('Confirm','Do you really want to delete the record')
        if result:
            cursor, connection = connect_database()
            if not cursor or not connection:
                return
        try:    
            cursor.execute('USE prabhat_automobiles')
            cursor.execute('DELETE FROM employees_data where empid=%s',(empid,))
            connection.commit()
            treeview_data()
            messagebox.showinfo('Success', 'Employee data deleted successfully')
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            cursor.close()  # Close the cursor
            connection.close()  # Close the connection


def search_employee(search_option, value):
    if search_option == 'Search By':
        messagebox.showerror('Error', 'No option is selected')
        return
    elif value == '':
        search_option=search_option.replace(' ','_')
        messagebox.showerror('Error', 'No value is entered')
        return

    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    try:
        cursor.execute('USE prabhat_automobiles')
        
        # Formulate the query string with the column name
        query = f"SELECT * FROM employees_data WHERE {search_option} LIKE %s"
        
        # Execute the query with a parameter for the value
        cursor.execute(query, (f'%{value}%',))
        
        records = cursor.fetchall()
        
        # Clear the TreeView and insert fetched records
        employee_treeview.delete(*employee_treeview.get_children())
        for record in records:
            employee_treeview.insert('', END, values=record)

    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')

    finally:
        cursor.close()  # Close the cursor
        connection.close()  # Close the connection

def show_all(search_entry,search_combobox):
    treeview_data()
    search_entry.delete(0,END)
    search_combobox.set('Search By')
    
    
              

def clear_fields(empid_entry, name_entry, email_entry, contact_entry, 
    gender_combobox, dob_date_entry, employment_type_combobox, 
    work_shift_combobox, address_text, doj_date_entry, 
    salary_entry, user_type_combobox, password_entry, 
    eductaion_combobox,check):


    empid_entry.delete(0,END)
    name_entry.delete(0,END)
    email_entry.delete(0,END)
    contact_entry.delete(0,END)
    gender_combobox.set("Select Gender")
    from datetime import date
    dob_date_entry.set_date(date.today())
    employment_type_combobox.set('Select Type')
    salary_entry.delete(0,END)
    user_type_combobox.set('Select User type')
    password_entry.delete(0,END)
    eductaion_combobox.set('Select Education')
    address_text.delete(1.0,END)
    doj_date_entry.set_date(date.today())
    work_shift_combobox.set('Select Shift')

    if check:
        employee_treeview.selection_remove(employee_treeview.selection())


def employee_form(window):
    global back_button_icon,employee_treeview
    employee_frame=Frame(window,height=700,width=1320,bg='white')
    employee_frame.place(x=200, y=130)
    heading_label=Label(employee_frame,text='MANAGE EMPLOYEE DETAILS',font=('times new roman',16,'bold'),bg='#0f4d7d',fg='white')
    heading_label.place(x=0,y=0,relwidth=1)

    back_button_icon=PhotoImage(file='arrow.png')
    back_button=Button(employee_frame,image=back_button_icon,bd=0,cursor='hand2',bg='white',command=lambda:employee_frame.place_forget())
    back_button.place(x=10,y=35)
#top frame
    topFrame=Frame(employee_frame,bg='white')
    topFrame.place(x=0,y=70,relwidth=1,height=235)
#search frame inside of the top frame
    search_frame=Frame(topFrame,bg='white')
    search_frame.pack()
    search_combobox=ttk.Combobox(search_frame,values=('EmpId','Name','Email','Employment Type','Education','Work Shift'),font=('times new roman',12),state='readonly')
    search_combobox.set('Search By')
    search_combobox.grid(row=0,column=0,padx=20)

    search_entry=Entry(search_frame,font=('times new roman',12),bg='lightyellow')
    search_entry.grid(row=0,column=1)

    search_button=Button(search_frame,text='Search',font=('times new roman',12,'bold'),bg='#010c48',width=10,cursor='hand2',fg='white',bd=0,command=lambda: search_employee(search_combobox.get(),search_entry.get()))
    search_button.grid(row=0,column=2,padx=20)

    showall_button=Button(search_frame,text='Show all',font=('times new roman',12,'bold'),bg='#010c48',width=10,cursor='hand2',fg='white',bd=0,command=lambda: show_all(search_entry,search_combobox))
    showall_button.grid(row=0,column=3)


    horizontal_scrollbar=Scrollbar(topFrame,orient=HORIZONTAL)
    vertital_scrollbar=Scrollbar(topFrame,orient=VERTICAL)
    employee_treeview=ttk.Treeview(topFrame,columns=('empid','name','email','contact','gender','dob','employement_type','education','work_shift','address','doj','salary','user_type'),show='headings',yscrollcommand=horizontal_scrollbar.set,xscrollcommand=vertital_scrollbar.set)
   
    horizontal_scrollbar.pack(side=BOTTOM,fill=X)
    vertital_scrollbar.pack(side=RIGHT,fill=Y,pady=(10,0))
    horizontal_scrollbar.config(command=employee_treeview.xview)
    vertital_scrollbar.config(command=employee_treeview.yview)

    employee_treeview.pack(pady=(10,0))

# to work on it
    employee_treeview.heading('empid',text='EmpId')
    employee_treeview.heading('name',text='Name')
    employee_treeview.heading('email',text='Email')
    employee_treeview.heading('contact',text='Contact')
    employee_treeview.heading('gender',text='Gender')
    employee_treeview.heading('dob',text='DOB')
    employee_treeview.heading('employement_type',text='Position')
    employee_treeview.heading('salary',text='Salary')
    employee_treeview.heading('address',text='Address')
    employee_treeview.heading('work_shift',text='Shift')
    employee_treeview.heading('doj',text='DOJ')
    employee_treeview.heading('user_type',text='User type')
    employee_treeview.heading('education',text='Highest_Eductaion')


    employee_treeview.column('empid',width=60)
    employee_treeview.column('name',width=140)
    employee_treeview.column('email',width=180)
    employee_treeview.column('contact',width=100)
    employee_treeview.column('gender',width=80)
    employee_treeview.column('dob',width=100)
    employee_treeview.column('employement_type',width=120)
    employee_treeview.column('salary',width=120)
    employee_treeview.column('address',width=200)
    employee_treeview.column('work_shift',width=120)
    employee_treeview.column('doj',width=100)
    employee_treeview.column('user_type',width=120)
    employee_treeview.column('education',width=120)


# caaling the display detail of emp
    treeview_data()
   


    detail_frame=Frame(employee_frame,bg='white')
    detail_frame.place(x=180,y=350)

    empid_label=Label(detail_frame,text='EmpId',font=('times new roman',12),bg='white')
    empid_label.grid(row=0,column=0,sticky='w')
    empid_entry=Entry(detail_frame,font=('times new roman',12),bg='lightyellow')
    empid_entry.grid(row=0,column=1,padx=20,pady=10,sticky='w')

    name_label=Label(detail_frame,text='Name',font=('times new roman',12),bg='white')
    name_label.grid(row=0,column=2,sticky='w')
    name_entry=Entry(detail_frame,font=('times new roman',12),bg='lightyellow')
    name_entry.grid(row=0,column=3,padx=20,pady=10,sticky='w')
   
    email_label=Label(detail_frame,text='Email',font=('times new roman',12),bg='white')
    email_label.grid(row=0,column=4,sticky='w')
    email_entry=Entry(detail_frame,font=('times new roman',12),bg='lightyellow')
    email_entry.grid(row=0,column=5,padx=20,pady=10,sticky='w')
    
    gender_label=Label(detail_frame,text='Gender',font=('times new roman',12),bg='white')
    gender_label.grid(row=1,column=0,sticky='w')
    gender_combobox=ttk.Combobox(detail_frame,font=('times new roman',12),values=('Male','Female'),width=18,state='readonly')
    gender_combobox.set('Select Gender')
    gender_combobox.grid(row=1,column=1,padx=20,pady=10,sticky='w')
    
    dob_label=Label(detail_frame,text='Date of Birth',font=('times new roman',12),bg='white')
    dob_label.grid(row=1,column=2,padx=9,pady=10,sticky='w')
    
    dob_date_entry=DateEntry(detail_frame,width=18,font=('times new roman',12),state='readonly',date_pattern='dd/mm/yyyy')
    dob_date_entry.grid(row=1,column=3,sticky='w')

    contact_label=Label(detail_frame,text='Contact',font=('times new roman',12),bg='white')
    contact_label.grid(row=1,column=4,padx=20,pady=10,sticky='w')

    contact_entry=Entry(detail_frame,font=('times new roman',12),bg='lightyellow')
    contact_entry.grid(row=1,column=5,padx=20,pady=10,sticky='w')

    employment_type_label=Label(detail_frame,text='Employment type',font=('times new roman',12),bg='white')
    employment_type_label.grid(row=2,column=0,sticky='w')
    employment_type_combobox=ttk.Combobox(detail_frame,font=('times new roman',12),values=('Full time','Part time','casual','intern'),width=18,state='readonly')
    employment_type_combobox.set('Select Employment type')
    employment_type_combobox.grid(row=2,column=1,padx=20,pady=10,sticky='w')

    eductaion_label=Label(detail_frame,text='Education',font=('times new roman',12),bg='white')
    eductaion_label.grid(row=2,column=2,sticky='w')
    eductaion_combobox=ttk.Combobox(detail_frame,font=('times new roman',12),values=('12th','10th','B.sc','M.sc','B.tech','M.tech','BBA','MBA','B.Arch','M.Arch','B.Com','M.Com'),width=18,state='readonly')
    eductaion_combobox.set('Select Eductaion')
    eductaion_combobox.grid(row=2,column=3,padx=20,pady=10,sticky='w')

    work_shift_label=Label(detail_frame,text='Work Shift',font=('times new roman',12),bg='white')
    work_shift_label.grid(row=2,column=4,sticky='w')
    work_shift_combobox=ttk.Combobox(detail_frame,font=('times new roman',12),values=('Day Shift','Night'),width=18,state='readonly')
    work_shift_combobox.set('Select Work Shift')
    work_shift_combobox.grid(row=2,column=5,padx=20,pady=10,sticky='w')

    address_shift_label=Label(detail_frame,text='Address',font=('times new roman',12),bg='white')
    address_shift_label.grid(row=3,column=0,padx=20,pady=10,sticky='w')
    address_text=Text(detail_frame,width=20,height=3,bg='lightyellow',font=('times new roman',12))
    address_text.grid(row=3,column=1,rowspan=2)


    doj_label=Label(detail_frame,text='Date of joining',font=('times new roman',12),bg='white')
    doj_label.grid(row=3,column=2,padx=20,pady=10,sticky='w')
    
    doj_date_entry=DateEntry(detail_frame,width=18,font=('times new roman',12),state='readonly',date_pattern='dd/mm/yyyy')
    doj_date_entry.grid(row=3,column=3,sticky='w')

    user_type_label=Label(detail_frame,text='User type',font=('times new roman',12),bg='white')
    user_type_label.grid(row=4,column=2,sticky='w')
    user_type_combobox=ttk.Combobox(detail_frame,font=('times new roman',12),values=('Admin','employee'),width=18,state='readonly')
    user_type_combobox.set('Select User Type')
    user_type_combobox.grid(row=4,column=3,padx=20,pady=10,sticky='w')

    salary_label=Label(detail_frame,text='Salary',font=('times new roman',12),bg='white')
    salary_label.grid(row=3,column=4,padx=20,pady=10,sticky='w')

    salary_entry=Entry(detail_frame,font=('times new roman',12),bg='lightyellow')
    salary_entry.grid(row=3,column=5,padx=20,pady=10,sticky='w')
   
    password_label=Label(detail_frame,text='Password',font=('times new roman',12),bg='white')
    password_label.grid(row=4,column=4,padx=20,pady=10,sticky='w')

    password_entry=Entry(detail_frame,font=('times new roman',12),bg='lightyellow')
    password_entry.grid(row=4,column=5,padx=20,pady=10,sticky='w')

    button_frame=Frame(employee_frame,bg='white')
    button_frame.place(x=400,y=620)


    add_button=Button(button_frame,text='Add',font=('times new roman',12,'bold'),bg='#010c48',width=10,cursor='hand2',fg='white',bd=0,command=lambda: add_employee(
    empid_entry.get(), name_entry.get(), email_entry.get(), contact_entry.get(), 
    gender_combobox.get(), dob_date_entry.get(), employment_type_combobox.get(), 
    work_shift_combobox.get(), address_text.get(1.0,END), doj_date_entry.get(), 
    salary_entry.get(), user_type_combobox.get(), password_entry.get(), 
    eductaion_combobox.get()))

    add_button.grid(row=0,column=0,padx=20)

    update_button=Button(button_frame,text='Update',font=('times new roman',12,'bold'),bg='#010c48',width=10,cursor='hand2',fg='white',bd=0,command=lambda: update_employee(empid_entry.get(), name_entry.get(), email_entry.get(), contact_entry.get(), 
    gender_combobox.get(), dob_date_entry.get(), employment_type_combobox.get(), 
    work_shift_combobox.get(), address_text.get(1.0,END), doj_date_entry.get(), 
    salary_entry.get(), user_type_combobox.get(), password_entry.get(), 
    eductaion_combobox.get()))
    update_button.grid(row=0,column=1,padx=20)

    delete_button=Button(button_frame,text='Delete',font=('times new roman',12,'bold'),bg='#010c48',width=10,cursor='hand2',fg='white',bd=0,command=lambda:delete_employee(empid_entry.get(),))
    delete_button.grid(row=0,column=2,padx=20)

    clear_button=Button(button_frame,text='Clear',font=('times new roman',12,'bold'),bg='#010c48',width=10,cursor='hand2',fg='white',bd=0,command= lambda : clear_fields(empid_entry, name_entry, email_entry, contact_entry, 
                                                                                                                                                                        gender_combobox, dob_date_entry, employment_type_combobox, 
                                                                                                                                                                        work_shift_combobox, address_text, doj_date_entry, 
                                                                                                                                                                        salary_entry, user_type_combobox, password_entry, 
                                                                                                                                                                        eductaion_combobox,TRUE))
    clear_button.grid(row=0,column=3,padx=20)

    employee_treeview.bind('<ButtonRelease-1>',lambda event :select_data(event,empid_entry, name_entry, email_entry, contact_entry, 
                                                            gender_combobox, dob_date_entry, employment_type_combobox, 
                                                            work_shift_combobox, address_text, doj_date_entry, 
                                                            salary_entry, user_type_combobox, password_entry, 
                                                            eductaion_combobox))


create_database_table()