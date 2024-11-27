from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymysql
from employees import connect_database




def category_form(window):

    global back_button_icon,bg_image

    category_frame=Frame(window,height=700,width=1320,bg='white')
    category_frame.place(x=200, y=130)

    heading_label= Label(category_frame,text='MANAGE CATEGORY DETAILS',font=('times new roman',16,'bold'),bg='#0f4d7d',fg='white')
    heading_label.place(x=0,y=0,relwidth=1)

    back_button_icon=PhotoImage(file='arrow.png')
    back_button=Button(category_frame,image=back_button_icon,bd=0,cursor='hand2',bg='white',command=lambda:category_frame.place_forget())
    back_button.place(x=10,y=35)

    bg_image=PhotoImage(file='logo.png')
    label=Label(category_frame,image=bg_image)
    label.place(x=30,y=100)

    details_frame=Frame(category_frame)
    details_frame.place(x=640,y=90)


    id_label=Label(details_frame,text='Id',font=('times new roman',14,'bold'),bg='white')
    id_label.grid(row=0,column=0,padx=(30,30),pady=60,sticky='w')
    id_entry=Entry(details_frame,font=('times new roman',14,'bold'),bg='lightyellow')
    id_entry.grid(row=0,column=1)

    
