from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
import pymysql 
from employees import employee_form
from supplier import supplier_form
from category import category_form
#functions

#employee section gui and function

    
#gui

window= Tk()
window.title('Dashboard')
window.geometry('1540x840+0+0')
window.resizable(0,0)
window.config(bg='white')

bg_image=PhotoImage(file='engine.png')
titleLabel=Label(window,image=bg_image,compound=RIGHT,text='CRM DASHBOARD',font=('times new roman',40,'bold'),bg='white',fg='#010c48',anchor='w',padx=20,pady=20)
titleLabel.place(x=0,y=0,relwidth=1)

logoutButton= Button(window,text='Logout',font=('times new roman',20,'bold'),bg='white',fg='#010c48')
logoutButton.place(x=1400,y=20)

subtitleLabel=Label(window,text='Welcome ADMIN \t\t Date: 08-07-2024\t\t TIME:20:35:55 pm',font=('times new roman',15),bg='#010c48',fg='white')
subtitleLabel.place(x=0,y=100,relwidth=1)


leftFrame = Frame(window)
leftFrame.place(x=0,y=128,width=200,height=955)


logoImage= PhotoImage(file='logo.png')
imageLabel=Label(leftFrame,image=logoImage)
imageLabel.pack()

menuLabel=Label(leftFrame,text='Menu',font=('times new roman',20),bg='#0ca3c4',fg='black')
menuLabel.pack(fill=X)

employeeImage= PhotoImage(file='meeting.png')
employeeButton= Button(leftFrame,image=employeeImage,compound=LEFT,text='  Employee',font=('times new roman',20,'bold'),anchor='w',padx=10,command=lambda:employee_form(window))
employeeButton.pack(fill=X)

supplierImage= PhotoImage(file='logistics.png')
supplierButton= Button(leftFrame,image=supplierImage,compound=LEFT,text='  Supplier',font=('times new roman',20,'bold'),anchor='w',padx=10,command=lambda:supplier_form(window))
supplierButton.pack(fill=X)

categoryImage= PhotoImage(file='computer.png')
categoryButton= Button(leftFrame,image=categoryImage,compound=LEFT,text='  Category',font=('times new roman',20,'bold'),anchor='w',padx=10,command= lambda:category_form(window))
categoryButton.pack(fill=X)

productImage= PhotoImage(file='trolley.png')
productButton= Button(leftFrame,image=productImage,compound=LEFT,text='  Product',font=('times new roman',20,'bold'),anchor='w',padx=10)
productButton.pack(fill=X)


salesImage= PhotoImage(file='sales.png')
salesButton= Button(leftFrame,image=salesImage,compound=LEFT,text='  Sales',font=('times new roman',20,'bold'),anchor='w',padx=10)
salesButton.pack(fill=X)


exitImage= PhotoImage(file='log-out.png')
exitButton= Button(leftFrame,image=exitImage,compound=LEFT,text='  Exit',font=('times new roman',20,'bold'),anchor='w',padx=10)
exitButton.pack(fill=X)

logoutImage= PhotoImage(file='switch.png')
logoutButton= Button(leftFrame,compound=LEFT,image=logoutImage,text='  Logout',font=('times new roman',20,'bold'),anchor='w',padx=10)
logoutButton.pack(fill=X)




emp_frame =Frame(window,bg='#2c3e50',bd=3,relief=RIDGE)
emp_frame.place(x=400,y=200,height=170,width=280)

total_emp=PhotoImage(file='meeting-64.png')
total_emp_label=Label(emp_frame,image=total_emp,bg='#2c3e50')
total_emp_label.pack(pady=10)

total_emp_text_label=Label(emp_frame,text='Total Employees',font=('times new roman',20,'bold'),bg='#2c3e50',fg='white')
total_emp_text_label.pack()

total_emp_text_count=Label(emp_frame,text='0',font=('times new roman',30,'bold'),bg='#2c3e50',fg='white')
total_emp_text_count.pack()



sup_frame =Frame(window,bg='#8e44ad',bd=3,relief=RIDGE)
sup_frame.place(x=800,y=200,height=170,width=280)
total_sup=PhotoImage(file='meeting-64.png')
total_sup_label=Label(sup_frame,image=total_sup,bg='#8e44ad')
total_sup_label.pack(pady=10)

total_sup_text_label=Label(sup_frame,text='Total Supplier',font=('times new roman',20,'bold'),bg='#8e44ad',fg='white')
total_sup_text_label.pack()

total_sup_text_count=Label(sup_frame,text='0',font=('times new roman',30,'bold'),bg='#8e44ad',fg='white')
total_sup_text_count.pack()







cat_frame =Frame(window,bg='#27ae60',bd=3,relief=RIDGE)
cat_frame.place(x=400,y=450,height=170,width=280)
total_cat=PhotoImage(file='meeting-64.png')
total_cat_label=Label(cat_frame,image=total_cat,bg='#27ae60')
total_cat_label.pack(pady=10)

total_cat_text_label=Label(cat_frame,text='Total Categories',font=('times new roman',20,'bold'),bg='#27ae60',fg='white')
total_cat_text_label.pack()

total_cat_text_count=Label(cat_frame,text='0',font=('times new roman',30,'bold'),bg='#27ae60',fg='white')
total_cat_text_count.pack()



prod_frame =Frame(window,bg='#2c3e50',bd=3,relief=RIDGE)
prod_frame.place(x=800,y=450,height=170,width=280)
total_prod=PhotoImage(file='meeting-64.png')
total_prod_label=Label(prod_frame,image=total_prod,bg='#2c3e50')
total_prod_label.pack(pady=10)

total_prod_text_label=Label(prod_frame,text='Total products',font=('times new roman',20,'bold'),bg='#2c3e50',fg='white')
total_prod_text_label.pack()

total_prod_text_count=Label(prod_frame,text='0',font=('times new roman',30,'bold'),bg='#2c3e50',fg='white')
total_prod_text_count.pack()


sales_frame =Frame(window,bg='#e74c3c',bd=3,relief=RIDGE)
sales_frame.place(x=600,y=660,height=170,width=280)
total_sales=PhotoImage(file='meeting-64.png')
total_sales_label=Label(sales_frame,image=total_sales,bg='#e74c3c')
total_sales_label.pack(pady=10)

total_sales_text_label=Label(sales_frame,text='Total products',font=('times new roman',20,'bold'),bg='#e74c3c',fg='white')
total_sales_text_label.pack()

total_sales_text_count=Label(sales_frame,text='0',font=('times new roman',30,'bold'),bg='#e74c3c',fg='white')
total_sales_text_count.pack()

window.mainloop()