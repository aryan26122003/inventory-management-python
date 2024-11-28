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
    button_frame.place(x=800, y=400)

    add_button = Button(button_frame, text='ADD', font=('times new roman', 14, 'bold'), bg='#010c48', width=8, cursor='hand2', fg='white', bd=0)
    add_button.grid(row=0, column=0, padx=(32, 0))

    delete_button = Button(button_frame, text='CLEAR', font=('times new roman', 14, 'bold'), bg='#010c48', width=8, cursor='hand2', fg='white', bd=0)
    delete_button.grid(row=0, column=1, padx=20)

    treeview_frame = Frame(category_frame, bg='yellow')
    treeview_frame.place(x=820, y=500, height=200, width=500)

    tree_view = ttk.Treeview(treeview_frame, columns=("ID", "Name", "Description"), show="headings")
    tree_view.heading("ID", text="Category ID")
    tree_view.heading("Name", text="Category Name")
    tree_view.heading("Description", text="Description")
    tree_view.pack(fill=BOTH, expand=True)