from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
import keyboard
from datetime import date
import time
import mysql.connector
import os

# Inputing the MySql Password
# mysqlpassword = str(input("Enter your MySQL Password: "))
os.chdir('E:\\Internship_Project\\Bills')


mydb = mysql.connector.connect(host = 'localhost', user = 'root', passwd  = "")
my_cursor = mydb.cursor()
# Databse Creation - medybest
my_cursor.execute("create database if not exists medybest")
my_cursor.execute("use medybest")
mydb.commit()


mydb1 = mysql.connector.connect(host= 'localhost', user = 'root', passwd = "")
my_cursor1 = mydb1.cursor()
# Database Creation - customer_orders_list
my_cursor1.execute("create database if not exists customer_orders_list")
my_cursor1.execute("use customer_orders_list")
mydb1.commit()


# <<<<<<<<<<<<<<<<<<<<<<  Tables Creation  >>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Table - medicine_table
my_cursor.execute('CREATE TABLE IF NOT EXISTS medicine_table (Sr_no INT AUTO_INCREMENT PRIMARY KEY, Medicine_Name VARCHAR(100), Quantity INT(6), Batch_no INT(10), Category VARCHAR(50), Manufacturer VARCHAR(100), Production_Date varchar(10), Expiry_Date varchar(10), Entry_Date varchar(10), Buying_price DECIMAL(10, 2), Selling_price DECIMAL(10, 2))')

# Table - company_table
my_cursor.execute('create table if not exists company_table(Sr_no int(255) auto_increment primary key, Company_name varchar(200), Contact_person varchar(50), Address varchar(200), Email varchar(100), Contact_no bigint(12), Entry_date VARCHAR(10))')

# Table - staff_table
my_cursor.execute('create table if not exists staff_table(Sr_no int(255) auto_increment primary key,Name varchar(50), Age int(3), Gender varchar(25), Marital_status varchar(50), Blood_group varchar(3),Address varchar(250), Date_of_birth varchar(10), Joining_date varchar(10), Contact_no bigint(20),Email varchar(100), Aadhar_no bigint(25), Salary decimal(10, 2))')

# Table - sales_info
my_cursor.execute('create table if not exists sales_info(Sr_no int(255) auto_increment primary key,Customer_Name varchar(50), Phone_Number bigint(10), Time varchar(50),Date varchar(50), Net_Total Decimal(50,2),Gross_total Decimal(50,2), Discount Decimal(50,2), Payment_mode varchar(50),Paid_amount Decimal(50,2),Return_amount Decimal(50,2))')

# Assignment of 'date.today()' to a variable "today"
today = date.today()


global gross, discount
gross = 0
discount = 0
net_total = 0

global count_order
count_order = 0

# Clear Sales Treeview
def clear_sales_list_treeview():
    for x in sales_list_treeview.get_children():
        sales_list_treeview.delete(x)

# Reset Sales Treeview
def reset_view_sales():
    clear_sales_list_treeview()
    sql_command = "select * from sales_info"
    my_cursor.execute(sql_command)
    sales_list = my_cursor.fetchall()
    count_sales = 0
    for list in sales_list:
        if count_sales%2==0:
            sales_list_treeview.insert(parent='', index='end', iid=count_sales, text= '', values=(list[0], list[1], list[2], list[3], list[4], list[5], list[6], list[7], list[8], list[9], list[10]), tags=('evenrow',))
        else:
            sales_list_treeview.insert(parent='', index='end', iid=count_sales, text= '', values=(list[0], list[1], list[2], list[3], list[4], list[5], list[6], list[7], list[8], list[9], list[10]), tags=('oddrow',))
        count_sales+=1

# Search Function
def search_sales():

    if search_sales_by_entry.get()=="Customer Name":
        search_by = "Customer_Name"
    else:
        search_by = "Sr_no"
    search_name = search_sales_name_entry.get()

    clear_sales_list_treeview()

    sql_command_search = "Select * from sales_info where "+search_by+"=%s"
    search_values = [search_name]
    my_cursor.execute(sql_command_search, search_values)
    sales_list = my_cursor.fetchall()
    count_sales = 0
    for list in sales_list:
        if count_sales%2==0:
            sales_list_treeview.insert(parent='', index='end', iid=count_sales, text= '', values=(list[0], list[1], list[2], list[3], list[4], list[5], list[6], list[7], list[8], list[9], list[10]), tags=('evenrow',))
        else:
            sales_list_treeview.insert(parent='', index='end', iid=count_sales, text= '', values=(list[0], list[1], list[2], list[3], list[4], list[5], list[6], list[7], list[8], list[9], list[10]), tags=('oddrow',))
        count_sales+=1


# Function to clear f4 frame "Widgets"
def clear_f4():
    for widgets in f4.winfo_children():
        widgets.destroy()

#General or Common Notebook Frame for Sales, Medicine, Staff and Company
def Notebook_frames():
    global frame_option, frame_1, frame_2
    frame_option = ttk.Notebook(f4)
    frame_option.pack(pady = 5)
    frame_1 = Frame(frame_option, bg = "#ffffff", width = 1150, height = 480)
    frame_2 = Frame(frame_option, bg = "#ffffff", width = 1150, height = 575)
    frame_1.pack(fill = "both", expand = 1)
    frame_2.pack(fill = "both", expand = 1)

# Discount Lock - Unlock
def lock_discount():
    if discount_entry['state'] == NORMAL:
        discount_entry['state'] = DISABLED
        lock_button['text'] = 'Unlock'
    elif discount_entry['state'] == DISABLED:
        discount_entry['state'] = NORMAL
        lock_button['text'] = 'Lock'

# Calculate Order
def calculate_order():
    # messagebox.showinfo('Submited Order', 'Order Submited. \n\n \tPrint Recipt')
    
    global gross, discount, net_total
    gross = 0
    net_total = 0
    customer_name = customer_name_entry.get().replace(" ","_")
    my_cursor1.execute("select * from "+customer_name+" where Date=%s", [today.strftime("%d-%m")])
    order_list = my_cursor1.fetchall()
    for list in order_list:
        gross = gross + float(list[3])
    discount = float(discount_entry.get())
    net_total = gross-discount
    gross_total_entry['state'] = NORMAL
    gross_total_entry.delete(0,END)
    gross_total_entry.insert(0,round(gross,2))
    gross_total_entry['state'] = DISABLED

    # discount_entry
    net_entry.config(text=net_total)

# Save to sales_info
def save_to_sales_info():

    sql_command = '''insert into sales_info(Customer_Name, Phone_Number, Time, Date, Net_Total, Gross_total, Discount, Payment_mode, Paid_amount, Return_amount) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    sales_values = [customer_name_entry.get(), phone_no_entry.get(), time.strftime('%I:%M:%S %p'), today.strftime("%d, %m %Y"), float(net_entry.cget('text')), round(float(gross_total_entry.get()),2), discount_entry.get(), payment_mode_entry.get(), paid_amt_entry.get(),return_amt_entry.get()]
    my_cursor.execute(sql_command, sales_values)
    mydb.commit()
    #print

# Sales Button Subbmition
def sales_submit_button_command():
    valid_submit_button = 0
    if customer_name_entry.get().isalpha() != True:
        messagebox.showerror('Error', 'Customer Name must carry Alphabets')
    
    elif phone_no_entry.get().isdigit() != True or len(phone_no_entry.get()) < 10 or len(phone_no_entry.get()) > 10:
        messagebox.showerror('Error', 'Phono Number : \n\tMust contain Numbers.\n\tMust contain 10 Numbers')
    
    else:
        valid_submit_button = 1

    if valid_submit_button == 1:
        calculate_order()
        
        payment_mode_entry['state'] = NORMAL
        paid_amt_entry['state'] = NORMAL
        return_amt_entry['state'] = NORMAL
        generate_receipt_button['state'] = NORMAL
        cancel_order_button['state'] = NORMAL

        customer_name_entry.config(state = DISABLED)
        phone_no_entry.config(state=DISABLED)
        quantity_dropdown.config(state = DISABLED)
        product_dropdown.config(state = DISABLED)
        submit_order_button['state'] = DISABLED
        add_button.config(state = DISABLED)
        delete_button.config(state = DISABLED)

# Fill order Entry
def fill_order_entry(e):
    product_dropdown.delete(0, END)
    quantity_dropdown.delete(0, END)

    selected = order_list_treeview.focus()
    value=order_list_treeview.item(selected, 'values')

    product_dropdown.insert(0, value[0])
    quantity_dropdown.insert(0, 1)

# Fill Product Entry
def fill_product_entry(e):
    product_dropdown.delete(0, END)
    quantity_dropdown.delete(0, END)

    selected = product_list_treeview.focus()
    value=product_list_treeview.item(selected, 'values')

    product_dropdown.insert(0, value[0])
    quantity_dropdown.insert(0, 1)

# Clear order List
def clear_order_list():
    for item in order_list_treeview.get_children():
        order_list_treeview.delete(item)

# Delete Order function
def delete_order():
    selected = order_list_treeview.selection()[0]
    value_2 = order_list_treeview.item(order_list_treeview.focus(), "values")
    
    # print(value_2[1])
    product_dropdown.delete(0, END)
    product_dropdown.insert(0,value_2[0])
    sql_command = '''DELETE FROM '''+customer_name+''' WHERE Product_name="'''+product_dropdown.get()+'''"'''
    my_cursor1.execute(sql_command)
    mydb1.commit()#print    
    order_list_treeview.delete(selected)

# Add button function
def add_to_order():
    if len(customer_name_entry.get())==0:
        messagebox.showinfo("Warning", "Please Enter Customer Name.")
    else:
        selected = product_list_treeview.focus()
        value = product_list_treeview.item(selected, 'values')
        price_of_item = float(value[1])*float(quantity_dropdown.get())
        
        global customer_name
        customer_name = customer_name_entry.get().replace(" ","_")
        
        sql_command = "create table if not exists %s (Sr_no int(20) auto_increment primary key,Product_name varchar(100), Quantity int(30), Cost decimal(20, 2), Date varchar(20))"%customer_name
        
        my_cursor1.execute(sql_command)
        mydb1.commit()

        record_query = "insert into "+ customer_name+"(Product_name , Quantity, Cost, Date) values(%s, %s, %s, %s)"
        query_values = [product_dropdown.get(),quantity_dropdown.get(),price_of_item, today.strftime("%d-%m")]
        my_cursor1.execute(record_query, query_values)
        mydb1.commit()

        my_cursor1.execute("select * from "+customer_name+" where Date=%s", [today.strftime("%d-%m")])
        order_list = my_cursor1.fetchall()
        
        clear_order_list()
        
        for list in order_list:
            global count_order
            if count_order%2==0:
                order_list_treeview.insert(parent='', index='end', iid=count_order, values=(list[1], list[2], list[3]), tags=('evenrow',))
            else:
                order_list_treeview.insert(parent='', index='end', iid=count_order, values=(list[1], list[2], list[3]), tags=('oddrow',))
            count_order+=1

        product_dropdown.delete(0, END)
        quantity_dropdown.delete(0, END)

# Reset Point of Sales Entries
def reset_point_of_sales():
    customer_name_entry.config(state = NORMAL)
    phone_no_entry.config(state = NORMAL)
    product_dropdown.config(state = NORMAL)
    quantity_dropdown.config(state = NORMAL)
    add_button.config(state = NORMAL)
    delete_button.config(state = NORMAL)
    submit_order_button.config(state = NORMAL)

    customer_name_entry.delete(0, END)
    phone_no_entry.delete(0, END)
    product_dropdown.delete(0, END)
    quantity_dropdown.delete(0, END)

    gross_total_entry.config(state = NORMAL)
    gross_total_entry.delete(0, END)
    gross_total_entry.config(state = DISABLED)

    net_entry.config(state = NORMAL)
    net_entry.config(text = ' ')
    net_entry.config(state = DISABLED)

    payment_mode_entry.config(state = NORMAL)
    paid_amt_entry.config(state = NORMAL)
    return_amt_entry.config(state = NORMAL)

    payment_mode_entry.delete(0, END)
    paid_amt_entry.delete(0, END)
    return_amt_entry.delete(0, END)

    payment_mode_entry.config(state = DISABLED)
    paid_amt_entry.config(state = DISABLED)
    return_amt_entry.config(state = DISABLED)

    discount_entry.config(state = NORMAL)
    discount_entry.delete(0, END)
    discount_entry.insert(0,0)
    discount_entry.config(state = DISABLED)
    lock_button.config(text = 'Lock')

    cancel_order_button.config(state = DISABLED)
    payment_mode_entry.config(state = DISABLED)
    paid_amt_entry.config(state = DISABLED)
    return_amt_entry.config(state = DISABLED)
    generate_receipt_button.config(state = DISABLED)

    clear_order_list()

# Destroy Geerate Bill
def destroy_bill():
    reciept_root.destroy()
    reset_point_of_sales()

# Read general file for bill
def read_bill_header_file():
    os.chdir("E:\\Internship_Project")
    bill_header = open('Bills\\General\\bill.txt','r')
    bill_table_header = open('Bills\\General\\bill_table_header.txt','r')
    bill_end = open('Bills\\General\\bill_ending.txt','r')
    try:
        os.chdir("E:\\Internship_Project\\Bills\\"+str(today.strftime('%d-%m-%Y')))
    except:
        os.chdir("E:\\Internship_Project\\Bills")
        os.mkdir(str(today.strftime("%d-%m-%Y")))
        os.chdir("E:\\Internship_Project\\Bills\\"+str(today.strftime("%d-%m-%Y")))

    file_name_path = str(customer_name_entry.get())+".txt"
    write_file = open(file_name_path,'w')
    bill_box.insert(END,bill_header.read()+"\n")
    
    customer_name_bill = "Name: "+str(customer_name_entry.get())+"\t\t\t\t\t        "+str(today.strftime("%d, %B %Y")+'\n')

    bill_box.insert(END,customer_name_bill)
    bill_box.insert(END,bill_table_header.read()+'\n')

    my_cursor1.execute("select * from "+customer_name+" where Date=%s", [today.strftime("%d-%m")])
    order_list = my_cursor1.fetchall()
    for value in order_list:
        bill_record = [value[1], value[2],value[2]]
        string = str(value[1])+'\t\t\t\t\t    '+str(value[2])+'\t     '+str(value[3])+'\n'
        bill_box.insert(END,string)

    bill_box.insert(END, bill_end.read())
    write_file.write(bill_box.get(1.0,END))

    os.chdir('E:\\Internship_Project')  #print

# generate_receipt()
def generate_receipt():
    save_to_sales_info()
    global reciept_root
    reciept_root = Toplevel(dashboard_root)
    reciept_root.geometry('566x550+100+10')
    reciept_root.resizable(False,False)
    
    bill_label = Label(reciept_root, text = 'Bill', font = ('consolas',15,'bold'))
    bill_label.pack()
    global bill_box
    bill_box = Text(reciept_root, height=25, font = ('bookman old style',12))
    bill_box.pack(fill = X)

    read_bill_header_file()

    exit_button = Button(reciept_root, text = 'Close', command = destroy_bill)
    exit_button.pack()
    reciept_root.mainloop()

# Cancel Order
def cancel_order():
    payment_mode_entry.config(state = DISABLED)
    paid_amt_entry.config(state = DISABLED)
    return_amt_entry.config(state = DISABLED)
    generate_receipt_button.config(state = DISABLED)
    cancel_order_button.config(state = DISABLED)

    customer_name_entry.config(state = NORMAL)
    phone_no_entry.config(state = NORMAL)
    product_dropdown.config(state = NORMAL)
    quantity_dropdown.config(state = NORMAL)
    submit_order_button.config(state = NORMAL)
    add_button.config(state = NORMAL)
    delete_button.config(state = NORMAL)

# ///////////////////////  Calling Sales frame  \\\\\\\\\\\\\\\\\\\\\\\\\\\\
def sales():
    clear_f4()
    f4.config(bg = "#fccb83")       # Light Orangish color for Sales

    style = ttk.Style()                 
    style.configure("TNotebook", bd =0, background="#fccb83", foreground='black')
    Notebook_frames()    
    frame_option.add(frame_1, text = "Point of Sale")
    frame_option.add(frame_2, text = "View Sales")
    style.configure("TNotebook.Tab", bd = 0, width = 15, font = ('bookman old style', 10), foreground='black')

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Point of Sales >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    # Globalisation of variable used in frames

    global sale_no_entry, customer_name_entry, phone_no_entry
    global product_dropdown, quantity_dropdown
    global gross_total_entry, discount_entry, net_entry, payment_mode_entry, paid_amt_entry, return_amt_entry, add_button, delete_button
    global lock_button, submit_order_button, cancel_order_button, generate_receipt_button
    
    global search_sales_by_entry,search_sales_name_entry
    # ******************* Frame Header - Point of Sales ********************
    frame_header_sales = Frame(frame_1 , bg = '#ffffff', width = 1150, height = 60)
    frame_header_sales.pack(side = TOP)
                                # Label - Point of Sales
    point_of_sales_text = Label(frame_header_sales, bg = '#ffffff', text = "Point of ", font = ('arial', 20, 'bold'))
    point_of_sales_text.pack(side = "left", padx = 0, pady = 10)
    point_of_sales_text = Label(frame_header_sales, bg = '#9c5600', text = "Sales", font = ('arial', 25, 'bold'), fg = '#ffffff')
    point_of_sales_text.pack(ipadx = 10, pady = 10)
    

    # ******************* Frame Add and View Item list *********************
    frame_add_item_and_list = Frame(frame_1, bd = 0, relief = RAISED, width = 850, height = 490, bg = '#fccb83')
    frame_add_item_and_list.pack(side = LEFT, expand = 1)
    frame_add_item_and_list.pack_propagate(0)

    

    # Frame - Reference No., Customer Details and Phono No. 
    frame_customer = Frame(frame_add_item_and_list, bd = 0, relief = SOLID, width = 360, height = 120, bg = '#fccb83')
    frame_customer.grid(row = 0, column =0)
    frame_customer.grid_propagate(0)
    
    sale_no = Label(frame_customer, text = 'Reference No. \t:', font = ('arial', 11), bg = '#fccb83', justify = 'left')
    sale_no.grid(row = 0, column = 0, padx = 5, pady = 5)
    sale_no_entry = Entry(frame_customer, font = ('arial', 14), width = 8, state = 'disabled')
    sale_no_entry.grid(row = 0, column = 1, padx = 5, pady = 10,columnspan=2)
    
    customer_name = Label(frame_customer, text = 'Customer Name \t:', font = ('arial', 11), bg = '#fccb83', justify = 'left')
    customer_name.grid(row = 1, column = 0, padx = 5, pady = 5)
    customer_name_entry = Entry(frame_customer, font = ('arial', 12), width = 21)
    customer_name_entry.grid(row = 1, column = 1, columnspan = 4)

    phone_no = Label(frame_customer, text = 'Phone No.\t:', font = ('arial', 11), bg = '#fccb83', justify = 'left')
    phone_no.grid(row = 2, column = 0, padx = 5, pady = 5)
    country_national_no_entry = Entry(frame_customer,textvariable=StringVar(), font = ('arial', 12), width = 3)
    country_national_no_entry.grid(row = 2, column = 1)
    phone_no_entry = Entry(frame_customer,textvariable=StringVar(), font = ('arial', 12), width = 17,justify=RIGHT)
    phone_no_entry.grid(row = 2, column = 2,padx = 4, columnspan=2)
    country_national_no_entry.insert(0,91)

    # Frame - Product Dropdown list, Item Add button and Submit order button
    frame_add_item = Frame(frame_add_item_and_list, bd = 0, relief = SOLID, width = 368, height = 120, bg = '#fccb83')
    frame_add_item.grid(row = 0, column = 1)
    frame_add_item.grid_propagate(0)

    product = Label(frame_add_item, text = 'Product:', font = ('arial', 12), bg = '#fccb83', justify = 'left')
    product.grid(row = 0, column = 0, pady = 5)

    product_dropdown = ttk.Combobox(frame_add_item, width = 34, font = ('arial', 13))
    product_dropdown.grid(row = 1, column = 0, columnspan = 30, padx = 15)
    

    Label(frame_add_item, text = '', font = ('arial', 5), bg = '#fccb83', justify = 'left').grid(row = 2, column = 0)
    quantity = Label(frame_add_item, text = 'Quantity:', font = ('arial', 12), bg = '#fccb83', justify = 'left')
    quantity.grid(row = 3, column = 0, pady = 5)

    quantity_dropdown = ttk.Combobox(frame_add_item, width = 3, font = ('arial', 13))
    quantity_dropdown.grid(row = 3, column = 1)
    quantity_dropdown['values'] = (1,2,3,4,5,6,7,8,9,10)

    add_button = Button(frame_add_item, text = 'Add', width = 6, bd = 1, bg = '#179101', fg = '#ffffff', font = ('bookman old style', 12), command = add_to_order)
    add_button.grid(row = 3, column = 22)

    delete_button = Button(frame_add_item, text = 'Delete', width = 6, bd = 1, bg = '#c20000', fg = '#ffffff', font = ('bookman old style', 12),command=delete_order)
    delete_button.grid(row = 3, column = 25)
    

    # Frame - Submit and Unsubmit order
    frame_submit = Frame(frame_add_item_and_list, bd = 0, relief = SOLID, width = 122, height = 120, bg = '#fccb83')
    frame_submit.grid(row = 0, column = 2)
    frame_submit.grid_propagate(0)

    submit_order_button = Button(frame_submit, text = 'Submit \nOrder ', width = 11, bd = 1, height = 2, bg = '#0097c9', fg = '#ffffff', font = ('bookman old style', 11))
    submit_order_button.grid(row = 0, column = 0, padx = 5, pady = 6)

    cancel_order_button = Button(frame_submit, text = 'Cancel \nOrder ', width = 11, bd = 1, height = 2, bg = '#c20000', fg = '#ffffff', font = ('bookman old style', 11), command=cancel_order, state=DISABLED)
    cancel_order_button.grid(row = 1, column = 0, padx = 5)             
    
    # Item list View
    frame_item_list = Frame(frame_add_item_and_list, bd = 7, relief = SUNKEN, width = 344, height = 346, bg = '#ffffff')
    frame_item_list.grid(row = 1, column =0)
    frame_item_list.pack_propagate(0)


    #<<<<<<<<<<<<<<<<<<<<<<< TreeView >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


    global product_list_treeview

    style = ttk.Style()
    style.configure("Treeview", background = '#9c5600', rowheight = 21, font = ('arial', 10),  foreground = "#ffffff")
    style.map('Treeview', background = [('selected','#bf4d00')])

    product_list_scroll = Scrollbar(frame_item_list)
    product_list_scroll.pack(side = RIGHT, fill = Y)

    product_list_treeview = ttk.Treeview(frame_item_list, yscrollcommand=product_list_scroll.set, selectmode='extended', height = 15)
    product_list_treeview.pack()

    product_list_scroll.config(command=product_list_treeview.yview)

    product_list_treeview['columns'] = ('Product Name', "Cost")

    product_list_treeview.column("#0", width=0, stretch=NO)
    product_list_treeview.column("Product Name", anchor=W,width=240)
    product_list_treeview.column("Cost", anchor=E,width=70)

    product_list_treeview.heading("#0", text = "", anchor = W)
    product_list_treeview.heading("Product Name", text = "Product Name", anchor = W)
    product_list_treeview.heading("Cost", text = "Cost", anchor = CENTER)


    my_cursor.execute('select Distinct Medicine_Name, Selling_price from medicine_table ORDER BY Medicine_Name')
    medicine_list = my_cursor.fetchall()

    
    product_list_treeview.tag_configure('oddrow', background = "#f0d6af")
    product_list_treeview.tag_configure('evenrow', background='#f7be6a')

    count = 0
    products = []
    for list in medicine_list:
        products.append(str(list[0]))
        if count%2==0:
            product_list_treeview.insert(parent='', index='end', iid=count, text= '', values=(list[0],list[1]), tags=('evenrow',))
        else:
            product_list_treeview.insert(parent='', index='end', iid=count, text= '', values=(list[0],list[1]), tags=('oddrow',))
        count+=1

    product_list_treeview.bind('<ButtonRelease-1>', fill_product_entry)
    product_dropdown['values'] = products
        


    #Frame - Order list
    frame_order_list = Frame(frame_add_item_and_list, bd = 7, relief = SUNKEN, width = 490, height = 346, bg = '#ffffff')
    frame_order_list.grid(row = 1, column =1, columnspan = 2,pady=10)
    frame_order_list.pack_propagate(0)

    your_order = Label(frame_order_list, text = "Your Order", bd = 0, relief = SOLID, width = 490, height=2, font = ("arial",12, 'bold'), bg = "#9c5600", fg = "#ffffff")
    your_order.pack()


    #<<<<<<<<<<<<<<<<<<<<<<< TreeView >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    global order_list_treeview

    style = ttk.Style()
    style.configure("Treeview", background = '#9c5600', rowheight = 21, font = ('arial', 10),  foreground = "#ffffff")
    style.map('Treeview', background = [('selected','#bf4d00')])

    frame_calculate_order = Frame(frame_order_list, bd = 1, relief = SOLID, width = 344, height = 46, bg = '#ffffff')
    frame_calculate_order.pack(side=BOTTOM)
    
    calculate_button = Button(frame_calculate_order,width=25, text = "Calculate Order", bg = "#faaf41",height=1,font = ("arial",16, "bold"), command = calculate_order)
    calculate_button.pack(side = RIGHT)
    reset_point_of_sales_button = Button(frame_calculate_order,width=20, text = "Reset", bg = "#faaf41",height=1,font = ("arial",16, "bold"), command = reset_point_of_sales)
    reset_point_of_sales_button.pack(side = RIGHT)

    order_list_scroll = Scrollbar(frame_order_list, width = 10)
    order_list_scroll.pack(side = RIGHT, fill = Y)

    order_list_treeview = ttk.Treeview(frame_order_list, yscrollcommand=order_list_scroll.set, selectmode='extended', height = 11)
    order_list_treeview.pack(fill = 'both')


    order_list_scroll.config(command=product_list_treeview.yview)


    order_list_treeview['columns'] = ('Product Name', 'Quantity', "Cost")

    order_list_treeview.column("#0", width=0, stretch=NO)
    order_list_treeview.column("Product Name", anchor=W,width=250)
    order_list_treeview.column("Quantity", anchor=E,width=80)
    order_list_treeview.column("Cost", anchor=E,width=100)


    order_list_treeview.heading("#0", text = "", anchor = W)
    order_list_treeview.heading("Product Name", text = "Product Name", anchor = W)
    order_list_treeview.heading("Quantity", text = "Quantity", anchor = CENTER)
    order_list_treeview.heading("Cost", text = "Cost", anchor = CENTER)
    

    order_list_treeview.tag_configure('oddrow', background = "#f0d6af")
    order_list_treeview.tag_configure('evenrow', background='#f7be6a')
    order_list_treeview.bind('<ButtonRelease-1>',fill_order_entry)
    

    
    # *********************** Frame Billing System ***************************
    frame_bill_system = Frame(frame_1, bd = 0, relief = SOLID, width = 300, height = 490, bg = '#fccb83')
    frame_bill_system.pack(side = LEFT)
    frame_bill_system.grid_propagate(0)

    #{{{{{{{{{{{{{{{{{ Frame - BILL SYSTEM Heading }}}}}}}}}}}}}}}}}}}
    billing_system_text_frame = Frame(frame_bill_system, bd = 5, relief = SUNKEN, width = 285, height = 480, bg = '#9c5600')
    billing_system_text_frame.grid(row = 0, column = 0, padx = 5, pady = 5)
    billing_system_text = Label(billing_system_text_frame, bg = '#ffffff', text = "Billing System", font = ('georgia', 30))
    billing_system_text.pack(ipadx = 8)

    # {{{{{{{{{{{{{{{{ Frame BILL SYSTEM Widgets }}}}}}}}}}}}}}}}}}}}
    billing_system_widgets_frame = Frame(frame_bill_system, bd = 5, relief = SUNKEN, width = 285, height = 405, bg = '#fccb83')
    billing_system_widgets_frame.grid(row = 1, column = 0, padx = 5)
    billing_system_widgets_frame.grid_propagate(0)

    gross_total_label = Label(billing_system_widgets_frame, text = 'Gross Total         :', bg = '#fccb83', font = ('bookmam old style', 12, 'bold'), bd = 0, relief = SOLID)
    gross_total_label.grid(row = 0, column = 0, padx = 5, pady = 10)

    gross_total_entry = Entry(billing_system_widgets_frame, font = ('bookmam old style', 14), width = 10, bd = 1, relief = SOLID, state = DISABLED)
    gross_total_entry.grid(row = 0, column = 1, columnspan=2)

    discount_label = Label(billing_system_widgets_frame, text = 'Discount (If any) :', bg = '#fccb83', font = ('bookmam old style', 12, 'bold'), bd = 0, relief = SOLID)
    discount_label.grid(row = 1, column = 0, padx = 5, pady = 10)

    discount_entry = Entry(billing_system_widgets_frame, font = ('bookmam old style', 14), width = 5, bd = 1, relief = SOLID)
    discount_entry.grid(row = 1, column = 1)
    discount_entry.insert(0,0)
    discount_entry['state'] = DISABLED
    lock_button = Button(billing_system_widgets_frame, width = 7, text = 'Lock', font = ('arial', 8), command=lock_discount)
    lock_button.grid(row = 1, column=2)

    Label(billing_system_widgets_frame, bg = '#fccb83').grid(row = 2, column = 0)
    net_label = Label(billing_system_widgets_frame, text = 'Net Total\t ', bg = '#fccb83', font = ('georgia', 14, 'bold'), bd = 0, relief = SOLID)
    net_label.grid(row = 3, column = 0, padx = 10)

    # Frame - Net Total
    frame_net_total = Frame(billing_system_widgets_frame, bd = 2, width = 250, height = 70, relief = SOLID, bg = '#ffffff')
    frame_net_total.grid(row = 4, column = 0, padx = 10, columnspan = 3)
    frame_net_total.pack_propagate(0)
    Label(frame_net_total, text = 'Rs.', font = ('bookman old style', 25), bg = '#ffffff').pack(side = LEFT, ipady = 6)
    net_entry = Label(frame_net_total, font = ('bookmam old style', 24), bg = '#ffffff', justify = 'right', width = 8, bd = 0, relief = SOLID, state = NORMAL)
    net_entry.pack(side = LEFT, ipady = 10, ipadx = 10)

    Label(billing_system_widgets_frame, bg = '#fccb83').grid(row = 5, column = 0)

    # Frame - Payment
    payment_frame = Frame(billing_system_widgets_frame, bd = 1, width = 260, height = 100, bg = '#fccb83')
    payment_frame.grid(row = 6, column = 0, columnspan = 3)
    payment_frame.grid_propagate(0)
    payment_mode_label = Label(payment_frame, text = 'Payment Mode:', bg = '#fccb83', font = ('arial', 12), bd = 0, relief = SOLID)
    payment_mode_label.grid(row = 0, column = 0)
    payment_mode_entry = ttk.Combobox(payment_frame, font = ('bookmam old style', 12), width = 12, state = DISABLED)
    payment_mode_entry.grid(row = 0, column = 1)
    payment_mode_entry['values'] = ('Cash','Google Pay','Paytm','Credit Card','Debit Card')
    
    paid_amt_label = Label(payment_frame, text = 'Paid Amt     :', bg = '#fccb83', font = ('arial', 12), bd = 0, relief = SOLID)
    paid_amt_label.grid(row = 1, column = 0)
    paid_amt_entry = Entry(payment_frame, font = ('bookmam old style', 14), width = 11, state = DISABLED)
    paid_amt_entry.grid(row = 1, column = 1, pady = 10, columnspan=2)

    return_amt_label = Label(payment_frame, text = 'Return Amt  :', bg = '#fccb83', font = ('arial', 12), bd = 0, relief = SOLID)
    return_amt_label.grid(row = 2, column = 0)
    return_amt_entry = Entry(payment_frame, font = ('bookmam old style', 14), width = 11, state = DISABLED)
    return_amt_entry.grid(row = 2, column = 1, columnspan=2)


    Label(billing_system_widgets_frame, font = ('arial', 1), bg = '#fccb83').grid(row = 7, column = 0)
    generate_receipt_button = Button(billing_system_widgets_frame, bg = 'lightskyblue', text = 'Generate\nReceipt', bd = 5, relief = RAISED, width = 19, height = 2, font = ('bookman old style', 14, 'bold'), command=generate_receipt, state = DISABLED)
    generate_receipt_button.grid(row = 9, column = 0, columnspan = 3, padx = 7,)

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<< Point of Sales End >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
    submit_order_button['command'] = sales_submit_button_command


    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< View Sales >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    # **************** Header Frame *****************
    frame_header_view_sales = Frame(frame_2 , bg = '#ffffff', width = 1150, height = 60)
    frame_header_view_sales.pack(side = TOP)
    
    # Label - View Sales
    point_of_sales_text = Label(frame_header_view_sales, bg = '#ffffff', text = "View ", font = ('arial', 20, 'bold'))
    point_of_sales_text.pack(side = "left", padx = 0, pady = 10)
    point_of_sales_text = Label(frame_header_view_sales, bg = '#9c5600', text = "Sales", font = ('arial', 25, 'bold'), fg = '#ffffff')
    point_of_sales_text.pack(ipadx = 10, pady = 10)

    # **************** Search Frame *****************
    frame_search_sales = Frame(frame_2, width=1130, height=80, bg='#fccb83', bd=1, relief=SOLID)
    frame_search_sales.pack(side = TOP)
    frame_search_sales.pack_propagate(0)

    search_label = Label(frame_search_sales, width=113,text = 'Search Sales', bg = '#9c5600', fg = '#ffffff', font=("arial",13, "bold"))
    search_label.pack(anchor='n')

    search_sales_by =Label(frame_search_sales,text='Search By\t:', width=15, bg = '#fccb83', font=("arial",12, "bold"))
    search_sales_by.pack(side=LEFT, padx = 10)
    search_sales_by_entry = ttk.Combobox(frame_search_sales, width=20, font=("arial",12, "bold"), values=['Customer Name', 'Sales Id'])
    search_sales_by_entry.pack(side=LEFT)

    search_sales_name =Label(frame_search_sales,text='Search\t:', width=15,bg = '#fccb83', font=("arial",12, "bold"))
    search_sales_name.pack(side=LEFT, padx = 10)
    search_sales_name_entry =Entry(frame_search_sales, width=20, font=("arial",12, "bold"))
    search_sales_name_entry.pack(side=LEFT)

    search_sales_button =Button(frame_search_sales, text = 'Search', fg = '#ffffff', bg = '#9c5600', width=10, font=("arial",12, "bold"), command = search_sales)
    search_sales_button.pack(side=LEFT, padx = 20)

    reset_sales_button = Button(frame_search_sales, text = 'Reset', fg = '#ffffff', bg = '#9c5600', width=10, font=("arial",12, "bold"), command = reset_view_sales)
    reset_sales_button.pack(side=LEFT, padx = 20)




    # *********************** View Medicine List Frame *******************
    frame_view_medicine = Frame(frame_2, width=1130, height=390, bg='#fccb83', bd=1, relief=SOLID)
    frame_view_medicine.pack(side = TOP,pady = 10)
    frame_view_medicine.pack_propagate(0)


    # <<<<<<<<<<<<<<<<<<<<<<<<<<< TreeView >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    global sales_list_treeview

    style = ttk.Style()
    style.configure("Treeview", background = '#9c5600', rowheight = 21, font = ('arial', 11),  foreground = "#ffffff")
    style.map('Treeview', background = [('selected','#bf4d00')])

    sales_list_side_scroll = Scrollbar(frame_view_medicine, width = 10, orient='vertical')
    sales_list_side_scroll.pack(side = RIGHT, fill = Y)
    sales_list_bottom_scroll = Scrollbar(frame_view_medicine, width = 10, orient='horizontal')
    sales_list_bottom_scroll.pack(side = BOTTOM, fill = X)

    sales_list_treeview = ttk.Treeview(frame_view_medicine, xscrollcommand=sales_list_bottom_scroll.set, yscrollcommand=sales_list_side_scroll.set, selectmode='extended', height = 17)
    sales_list_treeview.pack(fill = 'both')


    sales_list_side_scroll.config(command=sales_list_treeview.yview)
    sales_list_bottom_scroll.config(command=sales_list_treeview.xview)

    sales_list_treeview['columns'] = ("Sales No.", "Customer Name", "Phone No.", "Time", "Date", "Net Total", "Gross Total", "Discount", "Payment Mode", "Paid Amount", "Return Amount")

    sales_list_treeview.column("#0", width=0, stretch=NO)
    sales_list_treeview.column("Sales No.", anchor=W,width=50)
    sales_list_treeview.column("Customer Name", anchor=W,width=200)
    sales_list_treeview.column("Phone No.", anchor=W,width=100)
    sales_list_treeview.column("Time", anchor=W,width=100)
    sales_list_treeview.column("Date", anchor=W,width=100)
    sales_list_treeview.column("Net Total", anchor=W,width=100)
    sales_list_treeview.column("Gross Total", anchor=W,width=100)
    sales_list_treeview.column("Discount", anchor=W,width=100)
    sales_list_treeview.column("Payment Mode", anchor=W,width=120)
    sales_list_treeview.column("Paid Amount", anchor=W,width=100)
    sales_list_treeview.column("Return Amount", anchor=W,width=100)


    sales_list_treeview.heading("#0", text = "", anchor = W)
    sales_list_treeview.heading("Sales No.", text = "Sales No.", anchor = W)
    sales_list_treeview.heading("Customer Name", text = "Customer Name", anchor = W)
    sales_list_treeview.heading("Phone No.", text = "Phone No.", anchor = W)
    sales_list_treeview.heading("Time", text = "Time", anchor = W)
    sales_list_treeview.heading("Date", text = "Date", anchor = W)
    sales_list_treeview.heading("Net Total", text = "Net Total", anchor = W)
    sales_list_treeview.heading("Gross Total", text = "Gross Total", anchor = W)
    sales_list_treeview.heading("Discount", text = "Discount", anchor = W)
    sales_list_treeview.heading("Payment Mode", text = "Payment Mode", anchor = W)
    sales_list_treeview.heading("Paid Amount", text = "Paid Amount", anchor = W)
    sales_list_treeview.heading("Return Amount", text = "Return Amount", anchor = W)



    sales_list_treeview.tag_configure('oddrow', background = "#f5c1b0")
    sales_list_treeview.tag_configure('evenrow', background='#f7be6a')
    sales_list_treeview.bind('<ButtonRelease-1>',fill_order_entry)


    my_cursor.execute('select * from sales_info ORDER BY Sr_no')
    medicine_list = my_cursor.fetchall()
    for list in medicine_list:
            if count%2==0:
                sales_list_treeview.insert(parent='', index='end', iid=count, text= '', values=(list[0], list[1], list[2], list[3], list[4], list[5], list[6], list[7], list[8], list[9], list[10]), tags=('evenrow',))
            else:
                sales_list_treeview.insert(parent='', index='end', iid=count, text= '', values=(list[0], list[1], list[2], list[3], list[4], list[5], list[6], list[7], list[8], list[9], list[10]), tags=('oddrow',))
            count+=1
# \\\\\\\\\\\\\\\\\\\\\\\  Sales Frame Ending   ////////////////////////////


# Clear Medicine Treeview
def clear_medicine_list_treeview():
    for x in my_tree_medicine.get_children():
        my_tree_medicine.delete(x)

# Reset View Medicine Treeview
def reset_view_medicine():
    clear_medicine_list_treeview()
    sql_command = "select * from medicine_table"
    my_cursor.execute(sql_command)
    medicine_list = my_cursor.fetchall()
    count_medicine = 0
    for list in medicine_list:
        if count_medicine%2==0:
            my_tree_medicine.insert(parent='', index='end', iid=count_medicine, text= '', values=(list[0], list[1], list[2], list[3], list[4], list[5], list[6], list[7], list[8], list[9], list[10]), tags=('evenrow',))
        else:
            my_tree_medicine.insert(parent='', index='end', iid=count_medicine, text= '', values=(list[0], list[1], list[2], list[3], list[4], list[5], list[6], list[7], list[8], list[9], list[10]), tags=('oddrow',))
        count_medicine+=1

# Search Function
def search_medicine():

    if search_medicine_by_entry.get()=="Medicine Name":
        search_by = "Medicine_Name"
    else:
        search_by = "Sr_no"
    search_name = search_medicine_name_entry.get()

    clear_medicine_list_treeview()

    sql_command_search = "Select * from medicine_table where "+search_by+"=%s"
    search_values = [search_name]
    my_cursor.execute(sql_command_search, search_values)
    medicine_list = my_cursor.fetchall()
    count_medicine = 0
    for list in medicine_list:
        if count_medicine%2==0:
            my_tree_medicine.insert(parent='', index='end', iid=count_medicine, text= '', values=(list[0], list[1], list[2], list[3], list[4], list[5], list[6], list[7], list[8], list[9], list[10]), tags=('evenrow',))
        else:
            my_tree_medicine.insert(parent='', index='end', iid=count_medicine, text= '', values=(list[0], list[1], list[2], list[3], list[4], list[5], list[6], list[7], list[8], list[9], list[10]), tags=('oddrow',))
        count_medicine+=1

# Reset Add Medicine Entries
def reset_add_medicine():
    quantity_entry.delete(0, END)
    medicine_name_entry.delete(0, END)
    batchno_entry.delete(0, END)
    category_entry.delete(0, END)
    manufacture_entry.delete(0, END)
    productiondate_entry.delete(0, END)
    expirydate_entry.delete(0, END)
    entrydate_entry.delete(0, END)
    buyingprice_entry.delete(0, END)
    selling_price_entry.delete(0, END)

# Save Data to Medicine Table
def save_to_medicine_table():
    sql_command = "INSERT INTO medicine_table(Medicine_Name, Quantity, Batch_no, Category, Manufacturer, Production_Date, Expiry_Date, Entry_Date, Buying_price, Selling_price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (medicine_name_entry.get(), quantity_entry.get(), batchno_entry.get(),category_entry.get(), manufacture_entry.get(), productiondate_entry.get_date(), expirydate_entry.get_date(), entrydate_entry.get_date(), buyingprice_entry.get(), selling_price_entry.get())
    my_cursor.execute(sql_command, values)

    mydb.commit()
    messagebox.showinfo("Save", "Medicine record saved successfully.")
    reset_add_medicine()
    medicine_name_entry.focus_set()
    # print("Medicine Record save to MySQL Database.")

# Validate Add Medicine Entries
def validate_add_medicine():
    valid = 1
    if quantity_entry.get().isdigit()==False:
        messagebox.showinfo("Warning", "Quantity must be Number.")
        quantity_entry.focus_set()
        valid = 0
    elif batchno_entry.get().isdigit()==False:
        messagebox.showinfo("Warning", "Batch no. must be Number.")
        batchno_entry.focus_set()
        valid = 0
    elif buyingprice_entry.get().isalpha()==True or len(buyingprice_entry.get())==0:
        messagebox.showinfo("Warning", "Buying Price must be Decimal or Number.")
        buyingprice_entry.focus_set()
        valid = 0
    elif selling_price_entry.get().isalpha()==True or len(selling_price_entry.get())==0:
        messagebox.showinfo("Warning", "Selling Price must be Decimal or Number.")
        selling_price_entry.focus_set()
        valid = 0
    
    if valid==1:
        
        confirm = messagebox.askyesno("Comfirm","Do you want Save the Record")
        if confirm==1:
            if frame_option.index('current') == 0:  
                save_to_medicine_table()
                # print("Add Medicine Tab")
            else:
                pass
                # print("Edit Medicne Tab...")

# Fill Medicine Edit Entries
def  fill_enteries_medicine(e):
    medicine_id_entry.delete(0,END)
    medicine_name_entry_edit.delete(0,END)
    medicine_quantity_entry.delete(0,END)
    medicine_batch_entry.delete(0,END)
    medicine_category_entry.delete(0,END)
    medicine_manufacturer_entry.delete(0,END)
    medicine_prod_date_entry.delete(0,END)
    medicine_expiry_date_entry.delete(0,END)
    medicine_entry_date_entry.delete(0,END)
    medicine_buying_entry.delete(0,END)
    medicine_salary_entry.delete(0,END)

    selected = my_tree_medicine.focus()
    value = my_tree_medicine.item(selected , "values")

    medicine_id_entry.insert(0,value[0])
    medicine_name_entry_edit.insert(0,value[1])
    medicine_quantity_entry.insert(0,value[2])
    medicine_batch_entry.insert(0,value[3])
    medicine_category_entry.insert(0,value[4])
    medicine_manufacturer_entry.insert(0,value[5])
    medicine_prod_date_entry.insert(0,value[6])
    medicine_expiry_date_entry.insert(0,value[7])
    medicine_entry_date_entry.insert(0,value[8])
    medicine_buying_entry.insert(0,value[9])
    medicine_salary_entry.insert(0,value[10])

# Clear Medicine Entries
def clear_enteries_medicine():
    medicine_id_entry.delete(0,END)
    medicine_name_entry_edit.delete(0,END)
    medicine_quantity_entry.delete(0,END)
    medicine_batch_entry.delete(0,END)
    medicine_category_entry.delete(0,END)
    medicine_manufacturer_entry.delete(0,END)
    medicine_prod_date_entry.delete(0,END)
    medicine_expiry_date_entry.delete(0,END)
    medicine_entry_date_entry.delete(0,END)
    medicine_buying_entry.delete(0,END)
    medicine_salary_entry.delete(0,END)
    reset_view_medicine()

# Fill All Entries of Edit Medicine by Mouse left click release
def  fill_enteries_medicine(e):
    medicine_id_entry.delete(0,END)
    medicine_name_entry_edit.delete(0,END)
    medicine_quantity_entry.delete(0,END)
    medicine_batch_entry.delete(0,END)
    medicine_category_entry.delete(0,END)
    medicine_manufacturer_entry.delete(0,END)
    medicine_prod_date_entry.delete(0,END)
    medicine_expiry_date_entry.delete(0,END)
    medicine_entry_date_entry.delete(0,END)
    medicine_buying_entry.delete(0,END)
    medicine_salary_entry.delete(0,END)

    selected = my_tree_medicine.focus()
    value = my_tree_medicine.item(selected , "values")

    medicine_id_entry.insert(0,value[0])
    medicine_name_entry_edit.insert(0,value[1])
    medicine_quantity_entry.insert(0,value[2])
    medicine_batch_entry.insert(0,value[3])
    medicine_category_entry.insert(0,value[4])
    medicine_manufacturer_entry.insert(0,value[5])
    medicine_prod_date_entry.insert(0,value[6])
    medicine_expiry_date_entry.insert(0,value[7])
    medicine_entry_date_entry.insert(0,value[8])
    medicine_buying_entry.insert(0,value[9])
    medicine_salary_entry.insert(0,value[10])

# Delete Record from Medicine Table
def delete_record_medicine():
    x = my_tree_medicine.selection()[0]
    my_tree_medicine.delete(x)

    string = "DELETE FROM medicine_table WHERE Sr_no="+str(medicine_id_entry.get())
    # print(string)
    my_cursor.execute(string)
    messagebox.showinfo("Deleted", "Desired Record has been deleted")

# Update Record from Medicine Table
def update_record_medicine():
    #grab the record 
    selected = my_tree_medicine.focus()

    #Update the record 
    my_tree_medicine.item(selected , text="" ,values=(medicine_id_entry.get(),medicine_name_entry_edit.get(),medicine_quantity_entry.get(),medicine_batch_entry.get()
    ,medicine_category_entry.get(),medicine_manufacturer_entry.get(),medicine_prod_date_entry.get_date(),medicine_expiry_date_entry.get_date(),
    medicine_entry_date_entry.get_date(),medicine_buying_entry.get(),medicine_salary_entry.get()))


    sql_command = '''UPDATE medicine_table SET Medicine_Name=%s, Quantity=%s,Batch_no=%s,Category=%s,Manufacturer=%s,Production_Date=%s,Expiry_Date=%s,Entry_Date=%s,Buying_price=%s,Selling_price=%s where Sr_no=%s'''
    values = (medicine_name_entry_edit.get(),medicine_quantity_entry.get(), medicine_batch_entry.get(), medicine_category_entry.get(), medicine_manufacturer_entry.get(), medicine_prod_date_entry.get_date(), medicine_expiry_date_entry.get_date(), medicine_entry_date_entry.get_date(), medicine_buying_entry.get(), medicine_salary_entry.get(), medicine_id_entry.get())

    my_cursor.execute(sql_command, values)
    mydb.commit()
    clear_enteries_medicine()
    messagebox.showinfo("Updated", "Desired Record has been Updated")

# ///////////////////////  Call Medicine Frame  \\\\\\\\\\\\\\\\\\\\\\\\\\\
def medicine():
    clear_f4()
    f4.config(bg="#ffb8b8")         # Light redish color for Medicine Frame

    style = ttk.Style()
    style.configure("TNotebook", bd =0, background="#ffb8b8", foreground='green')
    Notebook_frames()
    frame_option.add(frame_1, text = "Add Medicine  ")
    frame_option.add(frame_2, text = "  Edit Medicine  ")

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Add Medicine >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    # Globalisation of variables
    global medicine_name_entry
    global quantity_entry
    global batchno_entry
    global category_entry
    global manufacture_entry
    global productiondate_entry
    global expirydate_entry
    global entrydate_entry
    global buyingprice_entry
    global selling_price_entry
    
    global medicine_id_entry,medicine_name_entry_edit,medicine_quantity_entry,medicine_batch_entry,medicine_category_entry,medicine_manufacturer_entry,medicine_prod_date_entry,medicine_expiry_date_entry,medicine_entry_date_entry,medicine_buying_entry,medicine_salary_entry

    global edit_count_medicine
    global search_medicine_name_entry, search_medicine_by_entry

    frame_header_medicine = Frame(frame_1, width = 1150, height= 60, bg = '#ffffff', bd= 0, relief= SOLID)
    frame_header_medicine.grid(row = 0, column = 0)
    frame_header_medicine.pack_propagate(0)
    
    add_medicine_text = Label(frame_header_medicine, text= 'Add Medicine',font = ('arial', 25, 'bold'), fg= '#730a17',bd= 0,  width = 100 ,bg = '#ffffff', relief= SOLID)
    add_medicine_text.pack(padx = 5, pady= 10)



    # ************** Frame for medicine info ******************
    frame_medicineinfo = Frame(frame_1, width = 1140, height= 30, bg = '#b00b1e',  bd= 1, relief= SOLID)
    frame_medicineinfo.grid(row = 1, column = 0, padx= 5)
    frame_medicineinfo.pack_propagate(0)

    add_medicine_info_text = Label(frame_medicineinfo, text= 'Medicine Information', font= ('arial', 12, 'bold'), fg = '#ffffff', width = 17, bg= '#b00b1e')
    add_medicine_info_text.pack(side= LEFT, padx=0)

    

    # ************** Frame for medicine details **************
    frame_medicine_detail = Frame(frame_1, width = 1140, height=405, bg = '#ffb8b8',  bd= 1, relief= SOLID)
    frame_medicine_detail.grid(row = 2, column = 0, padx= 5)
    frame_medicine_detail.grid_propagate(0)

    medicine_name_text= Label( frame_medicine_detail, text= 'Medicine Name\t:', font= ('arial', 15), bg= '#ffb8b8', bd= 0, relief= SOLID)
    medicine_name_text.grid(row= 0, column= 0, padx= 10, pady=25)

    medicine_name_entry= Entry( frame_medicine_detail, bd=1 , relief= SOLID, font= ('arial', 15), width = 30)
    medicine_name_entry.grid(row= 0, column= 1,  pady= 25)

    quantity_text= Label( frame_medicine_detail, text= 'Quantity\t\t:',  font= ('arial', 15), bg= '#ffb8b8', bd= 0, relief= SOLID)
    quantity_text.grid(row= 1, column= 0, padx= 10, pady=25)

    quantity_entry= Entry( frame_medicine_detail, bd=1 , relief= SOLID, font= ('arial', 15), width = 30)
    quantity_entry.grid(row= 1, column= 1,  pady= 25)

    batchno_text= Label( frame_medicine_detail, text= 'Batch no.\t\t:', font= ('arial', 15), bg= '#ffb8b8', bd= 0, relief= SOLID)
    batchno_text.grid(row= 2, column= 0, padx= 10, pady=25)

    batchno_entry= Entry( frame_medicine_detail, bd=1 , relief= SOLID, font= ('arial', 15), width = 30)
    batchno_entry.grid(row= 2, column=1,  pady= 25)

    category_text= Label( frame_medicine_detail, text= 'Category\t\t:', font= ('arial', 15), bg= '#ffb8b8', bd= 0, relief= SOLID)
    category_text.grid(row= 3, column= 0, padx= 10, pady=25)
    

    category_entry= ttk.Combobox( frame_medicine_detail, font= ('arial', 15), width = 29)
    category_entry.grid(row= 3, column=1,  pady= 25)
    category_entry['values']= ('Tablet' , 'Capsule', 'Syrub' , 'Injection', 'Medical Equipment', 'Madical Material') 

    manufacture_text= Label( frame_medicine_detail, text= 'Manufacturer\t:', font= ('arial', 15), bg= '#ffb8b8', bd= 0, relief= SOLID)
    manufacture_text.grid(row= 4, column= 0, padx= 10, pady=25)

    manufacture_entry= Entry( frame_medicine_detail, bd=1 , relief= SOLID, font= ('arial', 15), width = 30)
    manufacture_entry.grid(row= 4, column=1,  pady= 25)

    productiondate_text= Label( frame_medicine_detail, text= 'Producation date\t:', font= ('arial', 15), bg= '#ffb8b8', bd= 0, relief= SOLID)
    productiondate_text.grid(row= 0, column= 2, padx= 10, pady=25)

    productiondate_entry= DateEntry(frame_medicine_detail ,font= ('arial', 15), date_pattern = 'YYYY/mm/dd', width=30, background='#b00b1e', foreground='white', borderwidth=2)
    productiondate_entry.grid(row = 0, column= 3, pady=25)

    expirydate_text= Label( frame_medicine_detail, text= 'Expiry date\t:', font= ('arial', 15), bg= '#ffb8b8', bd= 0, relief= SOLID)
    expirydate_text.grid(row= 1, column= 2, padx= 10, pady=25)

    expirydate_entry= DateEntry(frame_medicine_detail ,font= ('arial', 15), date_pattern = 'YYYY/mm/dd', width=30, background='#b00b1e', foreground='white', borderwidth=2)
    expirydate_entry.grid(row = 1, column= 3, pady=25)

    entrydate_text= Label( frame_medicine_detail, text= 'Entry date\t:', font= ('arial', 15), bg= '#ffb8b8', bd= 0, relief= SOLID)
    entrydate_text.grid(row= 2, column= 2, padx= 10, pady=25)

    entrydate_entry= DateEntry(frame_medicine_detail ,font= ('arial', 15), date_pattern = 'YYYY/mm/dd', width=30, background='#b00b1e', foreground='white', borderwidth=2)
    entrydate_entry.grid(row = 2, column= 3, pady=25)
    
    buyingprice_text= Label( frame_medicine_detail, text= 'Buying price\tRs.', font= ('arial', 15), bg= '#ffb8b8', bd= 0, relief= SOLID)
    buyingprice_text.grid(row= 3, column= 2, padx= 10, pady=25)

    buyingprice_entry= Entry( frame_medicine_detail, bd=1 , relief= SOLID, font= ('arial', 15), width = 31)
    buyingprice_entry.grid(row= 3, column=3,  pady= 25)
        
    selling_price_text= Label( frame_medicine_detail, text= 'Selling price\tRs.', font= ('arial', 15), bg= '#ffb8b8', bd= 0, relief= SOLID)
    selling_price_text.grid(row= 4, column= 2, padx= 10, pady=25)

    selling_price_entry= Entry( frame_medicine_detail, bd=1 , relief= SOLID, font= ('arial', 15), width = 31)
    selling_price_entry.grid(row= 4, column=3,  pady= 25)
        

    # ************** Frame for medicine Buttons **************

    frame_medicine_button = Frame(frame_1, width = 1150, height=50, bg = '#ffffff',  bd= 0, relief= SOLID)
    frame_medicine_button.grid(row = 3, column = 0)

    reset_button= Button( frame_medicine_button,text='RESET',  bd=1 , relief= SOLID,bg='#b00b1e', font= ('arial', 12, 'bold'),fg='#ffffff', width = 31, command = reset_add_medicine)
    reset_button.grid(row= 0, column=0,padx= 10,  pady= 10)
    
    medicine_save_button= Button( frame_medicine_button,text='SAVE',  bd=1 , relief= SOLID, bg='#b00b1e', font= ('arial', 12, 'bold'), fg='#ffffff', width = 31, command = validate_add_medicine)
    medicine_save_button.grid(row= 0, column=1,  pady= 10)


    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Add medicine closes >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Edit medicine >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    

    frame_header_medicine = Frame(frame_2, width=1150, height=60, bg='#ffffff', bd=0, relief=SOLID)
    frame_header_medicine.grid(row=0, column=0,columnspan=2,pady=5)
    frame_header_medicine.pack_propagate(0)

    edit_medicine_header = Label(frame_header_medicine, text='Edit Medicine', font=('arial', 25, 'bold'), fg='#730a17',bd=0, bg='#ffffff', relief=SOLID)
    edit_medicine_header.pack(pady=5)


    # **************** Edit Medicine frame **********************
    frame_edit_medicine = Frame(frame_2, width=372, height=460, bg='#ffffff', bd=1, relief=SOLID)
    frame_edit_medicine.grid(row=1, column=0,rowspan=2,padx=5,pady=5)
    frame_edit_medicine.grid_propagate(0)

    # Frame - Medicine Input boxes
    edit_medicine_subframe_1 = Frame(frame_edit_medicine,width=370,height=40, bg = '#b00b1e')
    edit_medicine_subframe_1.grid()
    edit_medicine_subframe_1.grid_propagate(0)

    medicine_id_label = Label(edit_medicine_subframe_1, text='Medicine Id\t:', bg = '#b00b1e', fg = '#ffffff', font=('arial',13))
    medicine_id_label.grid(padx=5,pady=5)
    medicine_id_entry = Entry(edit_medicine_subframe_1,  font=('arial', 13))
    medicine_id_entry.grid(padx=5, pady=5,row=0,column=1)

    # Frame - Inputs and Labels of Medicine
    edit_medicine_subframe_2 = Frame(frame_edit_medicine,width=370,height=350,bg='#ffb8b8')
    edit_medicine_subframe_2.grid(row=1, column=0)
    edit_medicine_subframe_2.grid_propagate(0)

    medicine_name_label = Label(edit_medicine_subframe_2, text='Medicine Name\t:', font=('arial', 12), bg = '#ffb8b8')
    medicine_name_label.grid(padx=5, pady=5)
    medicine_name_entry_edit = Entry(edit_medicine_subframe_2, font=('arial', 12))
    medicine_name_entry_edit.grid(padx=5, pady=5, row=0, column=1)

    medicine_quantity_label = Label(edit_medicine_subframe_2, text='Quantity\t\t:', font=('arial', 12), bg = '#ffb8b8')
    medicine_quantity_label.grid(padx=5, pady=5,row=1,column=0)
    medicine_quantity_entry = Entry(edit_medicine_subframe_2, font=('arial', 12))
    medicine_quantity_entry.grid(padx=5, pady=5, row=1, column=1)

    medicine_batch_label = Label(edit_medicine_subframe_2, text='Batch no\t\t:', font=('arial', 12), bg = '#ffb8b8')
    medicine_batch_label.grid(padx=5, pady=5, row=2, column=0)
    medicine_batch_entry = Entry(edit_medicine_subframe_2, font=('arial', 12))
    medicine_batch_entry.grid(padx=5, pady=5, row=2, column=1)

    medicine_category_label = Label(edit_medicine_subframe_2, text='Category\t\t:', font=('arial', 12), bg = '#ffb8b8')
    medicine_category_label.grid(padx=5, pady=5, row=3, column=0)
    medicine_category_entry = ttk.Combobox(edit_medicine_subframe_2, font=('arial', 12),width=18)
    medicine_category_entry.grid(padx=5, pady=5, row=3, column=1)
    medicine_category_entry['values'] = ('Tablet', 'Capsule', 'Syrub', 'Injection', 'Medical Equipment', 'Madical Material')

    medicine_manufacturer_label = Label(edit_medicine_subframe_2, text='Manufacturer\t:', font=('arial', 12), bg = '#ffb8b8')
    medicine_manufacturer_label.grid(padx=5, pady=5, row=4, column=0)
    medicine_manufacturer_entry = Entry(edit_medicine_subframe_2, font=('arial', 12))
    medicine_manufacturer_entry.grid(padx=5, pady=5, row=4, column=1)

    medicine_prod_date_label = Label(edit_medicine_subframe_2, text='Production Date\t:', font=('arial', 12), bg = '#ffb8b8')
    medicine_prod_date_label.grid(padx=5, pady=5, row=5, column=0)
    medicine_prod_date_entry = DateEntry(edit_medicine_subframe_2, font=('arial', 12), background = '#b00b1e', width=18, date_pattern = 'dd/mm/y')
    medicine_prod_date_entry.grid(padx=5, pady=5, row=5, column=1)

    medicine_expiry_date_label = Label(edit_medicine_subframe_2, text='Expiry Date\t:', font=('arial', 12), bg = '#ffb8b8')
    medicine_expiry_date_label.grid(padx=5, pady=5, row=6, column=0)
    medicine_expiry_date_entry = DateEntry(edit_medicine_subframe_2, font=('arial', 12), background = '#b00b1e', width=18, date_pattern='dd/mm/y')
    medicine_expiry_date_entry.grid(padx=5, pady=5, row=6, column=1)

    medicine_entry_date_label = Label(edit_medicine_subframe_2, text='Entry Date\t:', font=('arial', 12), bg = '#ffb8b8')
    medicine_entry_date_label.grid(padx=5, pady=5, row=7, column=0)
    medicine_entry_date_entry = DateEntry(edit_medicine_subframe_2, font=('arial', 12), background = '#b00b1e', width=18, date_pattern='dd/mm/y')
    medicine_entry_date_entry.grid(padx=5, pady=5, row=7, column=1)

    medicine_buying_label = Label(edit_medicine_subframe_2, text='Buying Price Rs.\t:', font=('arial', 12), bg = '#ffb8b8')
    medicine_buying_label.grid(padx=5, pady=5, row=8, column=0)
    medicine_buying_entry = Entry(edit_medicine_subframe_2, font=('arial', 12))
    medicine_buying_entry.grid(padx=5, pady=5, row=8, column=1)

    medicine_salary_label = Label(edit_medicine_subframe_2, text='salary Price Rs.\t:', font=('arial', 12), bg = '#ffb8b8')
    medicine_salary_label.grid(padx=5, pady=5, row=9, column=0)
    medicine_salary_entry = Entry(edit_medicine_subframe_2, font=('arial', 12))
    medicine_salary_entry.grid(padx=5, pady=5, row=9, column=1)

    # Frames - Operational Buttons - Update, Delete, Reset and Print
    edit_medicine_subframe_3 = Frame(frame_edit_medicine, width=370, height=68, bg='#ffb8b8')
    edit_medicine_subframe_3.grid(row=3, column=0)
    edit_medicine_subframe_3.grid_propagate(0)

    edit_update_button = Button(edit_medicine_subframe_3, text='Update', bd=1, relief=SOLID, bg='#b00b1e', font=('arial', 11, 'bold'), fg='#ffffff', width=10,height=2 ,command=update_record_medicine)
    edit_update_button.grid(row=0, column=0, padx=20, pady=10)

    edit_delete_button = Button(edit_medicine_subframe_3, text='Delete', bd=1, relief=SOLID, bg='#b00b1e',font=('arial', 11, 'bold'), fg='#ffffff', width=10,height=2 , command=delete_record_medicine)
    edit_delete_button.grid(row=0, column=1, pady=10)

    edit_reset_button = Button(edit_medicine_subframe_3, text='Reset', bd=1, relief=SOLID, bg='#b00b1e', font=('arial', 11, 'bold'), fg='#ffffff', width=10,height=2,command=clear_enteries_medicine)
    edit_reset_button.grid(row=0, column=2, pady=10,padx=20)


    # ************************ Search Medicine Frame *********************

    frame_search_medicine = Frame(frame_2, width=750, height=60, bg='#ffb8b8', bd=1, relief=SOLID)
    frame_search_medicine.grid(row = 1, column=1, padx = 5,pady = 5)
    frame_search_medicine.pack_propagate(0)

    search_label = Label(frame_search_medicine, width=74,text = 'Search Medicine', bg = '#b00b1e', fg = '#ffffff', font=("arial",13, "bold"))
    search_label.pack(anchor='n', ipadx = 4)

    search_medicine_by =Label(frame_search_medicine,text='Search By :', width=15, bg = '#ffb8b8', font=("arial",12, "bold"))
    search_medicine_by.pack(side=LEFT)
    search_medicine_by_entry =ttk.Combobox(frame_search_medicine, width=18, font=("arial",12, "bold"))
    search_medicine_by_entry.pack(side=LEFT)
    search_medicine_by_entry['values'] = ['Medicine Name', 'Medicine Id']
    search_medicine_by_entry.set("Medicine Name")
    search_medicine_name =Label(frame_search_medicine,text='Search :', width=15,bg = '#ffb8b8', font=("arial",12, "bold"))
    search_medicine_name.pack(side=LEFT, padx = 10)
    search_medicine_name_entry =Entry(frame_search_medicine, width=18, font=("arial",12, "bold"))

    # Search Medicine Button
    search_medicine_name_entry.pack(side=LEFT)
    medicine_search_button = Button(frame_search_medicine, text = "Search", bg = '#b00b1e', fg = '#ffffff', width = 10 , command= search_medicine)
    medicine_search_button.pack(side = LEFT, padx = 10)



    # *********************** View Medicine List Frame *******************
    frame_view_medicine = Frame(frame_2, width=750, height=390, bg='#ffffff', bd=1, relief=SOLID)
    frame_view_medicine.grid(row=2, column=1,pady=5, )
    frame_view_medicine.pack_propagate(0)

    # <<<<<<<<<<<<<<<<<<<<<    TREE VIEW >>>>>>>>>>>>>>>>>>>>>

    global my_tree_medicine

    # Add Some Style
    style = ttk.Style()

 

    # Configure the Treeview Colors
    style.configure("Treeview",
        background="#b00b1e",
        foreground="black",
        rowheight=25,
        fieldbackground="#b00b1e", font = ("arial", 10))

    # Change Selected Color #347083
    style.map('Treeview',
        background=[('selected', '#eb1717')])

    # Create a Treeview Frame
    tree_frame = Frame(frame_view_medicine)
    tree_frame.pack()

    # Create a Treeview Scrollbar
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    # Create The Treeview
    my_tree_medicine = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended", height=390)
    my_tree_medicine.pack(fill="both")

    # Configure the Scrollbar
    tree_scroll.config(command=my_tree_medicine.yview)

    
    # Define Our Columns
    my_tree_medicine['columns'] = ("Sr.No", "Medicine Name", "Quantity", "Batch.No", "Category", "Manufacturer", "Production date" ,"Expiriy Date" , "Entry Date" ,"Buying Price" , "Selling Price")


    # Format Our Columns
    my_tree_medicine.column("#0", width=0, stretch=NO)
    my_tree_medicine.column("Sr.No", anchor=W, width=30)
    my_tree_medicine.column("Medicine Name", anchor=W, width=150)
    my_tree_medicine.column("Quantity", anchor=W, width=60)
    my_tree_medicine.column("Batch.No", anchor=CENTER, width=60)
    my_tree_medicine.column("Category", anchor=CENTER, width=100)
    my_tree_medicine.column("Manufacturer", anchor=CENTER, width=120)
    my_tree_medicine.column("Production date", anchor=CENTER, width=60)
    my_tree_medicine.column("Expiriy Date", anchor=CENTER, width=60)
    my_tree_medicine.column("Entry Date", anchor=CENTER, width=65)
    my_tree_medicine.column("Buying Price", anchor=CENTER, width=70)
    my_tree_medicine.column("Selling Price", anchor=CENTER, width=70)
   


    # Create Headings
    my_tree_medicine.heading("#0", text="", anchor=W ) 
    my_tree_medicine.heading("Sr.No", anchor=W, text="Sr.No" )
    my_tree_medicine.heading("Medicine Name", anchor=W, text="Medicine Name")
    my_tree_medicine.heading("Quantity", anchor=W, text="Quantity")
    my_tree_medicine.heading("Batch.No", anchor=CENTER, text="Batch.No")
    my_tree_medicine.heading("Category", anchor=CENTER, text="Category")
    my_tree_medicine.heading("Manufacturer", anchor=CENTER, text="Manufacturer")
    my_tree_medicine.heading("Production date", anchor=CENTER, text="Production Date")
    my_tree_medicine.heading("Expiriy Date", anchor=CENTER, text="Expiry Date")
    my_tree_medicine.heading("Entry Date", anchor=CENTER, text="Entry Date")
    my_tree_medicine.heading("Buying Price", anchor=CENTER, text="Buying Price")
    my_tree_medicine.heading("Selling Price", anchor=CENTER, text="Selling Price")

    

    # Create Striped Row Tags
    my_tree_medicine.tag_configure('oddrow', background="white")
    my_tree_medicine.tag_configure('evenrow', background='#ffb8b8')

    #Adding data to the tree

    my_cursor.execute("SELECT * FROM medicine_table")
    records=my_cursor.fetchall()

    edit_count_medicine =0

    for record in records :
        if edit_count_medicine % 2 == 0:
            my_tree_medicine.insert(parent='' , index='end' ,iid = edit_count_medicine, text='', values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7] ,record[8],record[9] ,record[10]),  tags=('evenrow', ))
 
        else :
            my_tree_medicine.insert(parent='' , index='end' ,iid = edit_count_medicine, text='', values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7] ,record[8],record[9] ,record[10]), tags=('oddrow', ))
        edit_count_medicine +=1
    my_tree_medicine.bind("<ButtonRelease-1>" , fill_enteries_medicine)

 # Call Staff Frame
# \\\\\\\\\\\\\\\\\\\\\\\  Medicine Frame Ends  ///////////////////////



# Clear Medicine Treeview
def clear_staff_list_treeview():
    for x in my_tree_staff.get_children():
        my_tree_staff.delete(x)

# Reset View Medicine Treeview
def reset_view_staff():
    clear_staff_list_treeview()
    sql_command = "select * from staff_table"
    my_cursor.execute(sql_command)
    staff_list = my_cursor.fetchall()
    count_staff = 0
    for list in staff_list:
        if count_staff%2==0:
            my_tree_staff.insert(parent='', index='end', iid=count_staff, text= '', values=(list[0], list[1], list[2], list[3], list[4], list[5], list[6], list[7], list[8], list[9], list[10], list[11], list[12]), tags=('evenrow',))
        else:
            my_tree_staff.insert(parent='', index='end', iid=count_staff, text= '', values=(list[0], list[1], list[2], list[3], list[4], list[5], list[6], list[7], list[8], list[9], list[10], list[11], list[12]), tags=('oddrow',))
        count_staff+=1

# Search Function
def search_staff():

    if search_staff_by_entry.get()=="Staff Name":
        search_by = "Name"
    else:
        search_by = "Sr_no"
    search_name = search_staff_name_entry.get()

    clear_staff_list_treeview()

    sql_command_search = "Select * from staff_table where "+search_by+"=%s"
    search_values = [search_name]
    my_cursor.execute(sql_command_search, search_values)
    staff_list = my_cursor.fetchall()
    count_staff = 0
    for list in staff_list:
        if count_staff%2==0:
            my_tree_staff.insert(parent='', index='end', iid=count_staff, text= '', values=(list[0], list[1], list[2], list[3], list[4], list[5], list[6], list[7], list[8], list[9], list[10]), tags=('evenrow',))
        else:
            my_tree_staff.insert(parent='', index='end', iid=count_staff, text= '', values=(list[0], list[1], list[2], list[3], list[4], list[5], list[6], list[7], list[8], list[9], list[10]), tags=('oddrow',))
        count_staff+=1

# Reset Add Staff Entries
def reset_add_staff():
    staff_name_entry.delete(0, END)
    age_entry.delete(0, END)
    gender_entry.delete(0, END)
    marital_status_entry.delete(0, END)
    blood_group_entry.delete(0, END)
    address_entry.delete('1.0',"end")
    dateofbirth_entry.delete(0, END)
    joiningdate_entry.delete(0, END)
    contactno_entry.delete(0, END)
    Email_entry.delete(0, END)
    aadhar_entry.delete(0, END)
    salary_entry.delete(0, END)
    staff_name_entry.focus()

# Save to Staff Table
def save_to_staff_table():
    sql_command = "INSERT INTO staff_table(Name, Age, Gender, Marital_status, Blood_group, Address, Date_of_birth, Joining_date, Contact_no, Email, Aadhar_no, Salary) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (staff_name_entry.get(),age_entry.get(),gender_entry.get(),marital_status_entry.get(),blood_group_entry.get(),address_entry.get("1.0", "end-1c"),dateofbirth_entry.get_date(),joiningdate_entry.get_date(),contactno_entry.get(),Email_entry.get(),aadhar_entry.get(),salary_entry.get())
    my_cursor.execute(sql_command, values)
    mydb.commit()
    messagebox.showinfo("Save", "Staff record saved successfully.")
    reset_add_staff()
    staff_name_entry.focus()

# Validate Add Staff Entries
def validate_add_staff():
    valid = 1
    if staff_name_entry.get().isalpha()==False:
        messagebox.showinfo("Warning", "Staff Name must contains Alphabets.")
        staff_name_entry.focus_set()
        valid = 0
    elif len(age_entry.get())!=2 or int(age_entry.get())==0 or int(age_entry.get())<18 or int(age_entry.get())>60:
        messagebox.showinfo("Warning", "Staff Age Must be greater than 18 years and less than 60 years.")
        age_entry.focus_set()
        valid = 0
    elif gender_entry.get()!="Male":
        if gender_entry.get()!="Female":
            if gender_entry.get()!="Transgender":
                messagebox.showinfo("Warning", "Please, Select gender...")
                gender_entry.focus_set()
                valid = 0
    if valid == 1:
        if marital_status_entry.get()!="Single":
            if marital_status_entry.get()!="Married":
                if marital_status_entry.get()!="Widowed":
                    if marital_status_entry.get()!="Seperated":
                        if marital_status_entry.get()!="Divorced":
                            messagebox.showinfo("Warning", "Please, Select Marital status...")
                            marital_status_entry.focus_set()
                            valid = 0
    if valid==1:
        if len(blood_group_entry.get())<=3:
            if blood_group_entry.get()=="A+" or blood_group_entry.get()=="A-" or blood_group_entry.get()=="B+" or blood_group_entry.get()=="B-" or blood_group_entry.get()=="O+" or blood_group_entry.get()=="O-" or blood_group_entry.get()=="AB+" or blood_group_entry.get()=="AB-":
                pass
            else:
                messagebox.showinfo("Warning", "Please select valid option.")
                blood_group_entry.focus_set()
                valid = 0
    if valid==1:
        if contactno_entry.get().isdigit() != True or len(contactno_entry.get()) < 10 or len(contactno_entry.get()) == 11 or len(contactno_entry.get()) > 12:
            messagebox.showerror('Error', 'Contact Number : \n\tMust contain Numbers.\n\tMust contain 10 Numbers')
            contactno_entry.focus_set()
            valid = 0
        elif "@" not in Email_entry.get():
            messagebox.showerror("Warning", "Please enter Valid Email Id.")
            Email_entry.focus_set()
            valid = 0
        elif aadhar_entry.get().isdigit()!=True or len(aadhar_entry.get())!=12:
            messagebox.showinfo("Warning", "Please enter valid Addhar Number.")
            aadhar_entry.focus_set()
            valid = 0
        elif salary_entry.get().isalpha() == True:
            messagebox.showinfo("Warning", "Please enter valid salary.")
            salary_entry.focus_set()
            valid = 0
        else:
            valid = 1
        
    if valid == 1:
        confirm = messagebox.askyesno("Comfirm","Do you want Save the Record")
        if confirm==1:
            save_to_staff_table()

# Fill Entries of Edit Staff by Mouse left click release
def  fill_enteries_staff(e):

    staff_id_entry.delete(0,END)
    staff_name_edit_entry.delete(0,END)
    staff_age_edit_entry.delete(0,END)
    staff_gender_edit_entry.delete(0,END)
    staff_marital_edit_entry.delete(0,END)
    dateofbirth_edit_entry.delete(0,END)
    joiningdate_edit_entry.delete(0,END)
    staff_blood_grp_edit_entry.delete(0,END)
    staff_address_edit_entry.delete(0,END)
    staff_contact_edit_entry.delete(0,END)
    staff_email_edit_entry.delete(0,END)
    staff_addharr_edit_entry.delete(0,END)
    staff_salary_edit_entry.delete(0,END)

    
    selected = my_tree_staff.focus()
    value = my_tree_staff.item(selected , "values")

    staff_id_entry.insert(0,value[0])
    staff_name_edit_entry.insert(0,value[1])
    staff_age_edit_entry.insert(0,value[2])
    staff_gender_edit_entry.insert(0,value[3])
    staff_marital_edit_entry.insert(0,value[4])
    staff_blood_grp_edit_entry.insert(0,value[5])
    staff_address_edit_entry.insert(0,value[6])
    dateofbirth_edit_entry.insert(0,value[7])
    joiningdate_edit_entry.insert(0,value[8])
    staff_contact_edit_entry.insert(0,value[9])
    staff_email_edit_entry.insert(0,value[10])
    staff_addharr_edit_entry.insert(0,value[11])
    staff_salary_edit_entry.insert(0,value[12])

# Clear Entries of Staff Edit
def clear_enteries_staff():
    staff_id_entry.delete(0,END)
    staff_name_edit_entry.delete(0,END)
    staff_age_edit_entry.delete(0,END)
    staff_gender_edit_entry.delete(0,END)
    staff_marital_edit_entry.delete(0,END)
    dateofbirth_edit_entry.delete(0,END)
    joiningdate_edit_entry.delete(0,END)
    staff_blood_grp_edit_entry.delete(0,END)
    staff_address_edit_entry.delete(0,END)
    staff_contact_edit_entry.delete(0,END)
    staff_email_edit_entry.delete(0,END)
    staff_addharr_edit_entry.delete(0,END)
    staff_salary_edit_entry.delete(0,END)
    reset_view_staff()

# Delete Record from Staff Table
def delete_record_staff():
    x = my_tree_staff.selection()[0]
    my_tree_staff.delete(x)

    string = "DELETE FROM staff_table WHERE Sr_no="+str(staff_id_entry.get())
    # print(string)
    my_cursor.execute(string)
    messagebox.showinfo("Deleted", "Desired Record has been deleted")

# Update Record in Staff Table
def update_record_staff():
    #grab the record 
    selected = my_tree_staff.focus()

    #Update the record 
    my_tree_staff.item(selected , text="" ,values=( 
        staff_id_entry.get(),
        staff_name_edit_entry.get(),
        staff_age_edit_entry.get(),
        staff_gender_edit_entry.get(),
        staff_marital_edit_entry.get(),
        dateofbirth_edit_entry.get_date(),
        joiningdate_edit_entry.get_date(),
        staff_blood_grp_edit_entry.get(),
        staff_address_edit_entry.get(),
        staff_contact_edit_entry.get(),
        staff_email_edit_entry.get(),
        staff_addharr_edit_entry.get(),
        staff_salary_edit_entry.get()))


    sql_command = '''UPDATE staff_table SET Name=%s, Age=%s,Gender=%s, Marital_status=%s,Blood_group=%s,Address=%s,Date_of_birth=%s,Joining_date=%s,Contact_no=%s,Email=%s , Aadhar_no=%s , Salary=%s where Sr_no=%s'''
    values = (staff_name_edit_entry.get(),
        staff_age_edit_entry.get(),
        staff_gender_edit_entry.get(),
        staff_marital_edit_entry.get(),
        staff_blood_grp_edit_entry.get(),
        staff_address_edit_entry.get(),
        dateofbirth_edit_entry.get_date(),
        joiningdate_edit_entry.get_date(),
    
        staff_contact_edit_entry.get(),
        staff_email_edit_entry.get(),
        staff_addharr_edit_entry.get(),
        staff_salary_edit_entry.get(),
        staff_id_entry.get(),
        )

    my_cursor.execute(sql_command, values)
    mydb.commit()
    clear_enteries_staff()
    messagebox.showinfo("Updated", "Desired Record has been Updated")

# /////////////////////////////  Call Staff Frame  \\\\\\\\\\\\\\\\\\\\\\\\\\\\\
def staff():
    clear_f4()
    f4.config(bg = "#a8e3ff")       # Light Sky Blue color for Staff Frame

    style = ttk.Style()
    style.configure("TNotebook", bd =0, background="#a8e3ff", foreground='green')
    Notebook_frames()
    frame_option.add(frame_1, text = "Add staff  ")
    frame_option.add(frame_2, text = "  Edit staff  ")

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Add Staff >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    # Globalisation of Variables of Staff
    global staff_name_entry,age_entry,gender_entry,marital_status_entry,blood_group_entry,address_entry,dateofbirth_entry,joiningdate_entry,contactno_entry,Email_entry,aadhar_entry,salary_entry

    global staff_id_entry,staff_name_edit_entry,staff_age_edit_entry,staff_gender_edit_entry,staff_marital_edit_entry,dateofbirth_edit_entry,joiningdate_edit_entry,staff_blood_grp_edit_entry,staff_address_edit_entry,staff_contact_edit_entry,staff_email_edit_entry,staff_addharr_edit_entry,staff_salary_edit_entry

    global edit_count_staff, search_staff_by_entry, search_staff_name_entry
    # *********************** Frame for Add Staff ************************

    frame_header_staff = Frame(frame_1, width = 1150, height= 60, bg = '#ffffff', bd= 0, relief= SOLID)
    frame_header_staff.grid(row = 0, column = 0)
    frame_header_staff.pack_propagate(0)
    
    add_staff_text = Label(frame_header_staff, text= 'Add Staff',font = ('arial', 25, 'bold'), fg= '#012552',bd= 0,  width = 100 ,bg = '#ffffff', relief= SOLID)
    add_staff_text.pack(padx = 5, pady= 10)

    # *********************** Frame for Staff Info Label *******************

    frame_staffinfo = Frame(frame_1, width = 1140, height= 30, bg = '#0f0b7d',  bd= 1, relief= SOLID)
    frame_staffinfo.grid(row = 1, column = 0, padx= 5)
    frame_staffinfo.pack_propagate(0)

    add_staff_info_text = Label(frame_staffinfo, text= 'Staff Information', font= ('arial', 12, 'bold'), fg = '#ffffff', width = 17, bg= '#0f0b7d')
    add_staff_info_text.pack(side= LEFT, padx=0)

    # *********************** Frame for Staff Details **********************


    frame_staff_detail = Frame(frame_1, width = 1140, height=405, bg = '#a8e3ff',  bd= 1, relief= SOLID)
    frame_staff_detail.grid(row = 2, column = 0, padx= 5)
    frame_staff_detail.grid_propagate(0)

    staff_name_text= Label( frame_staff_detail, text= 'Name\t\t:', font= ('arial', 15), bg= '#a8e3ff', bd= 0, relief= SOLID)
    staff_name_text.grid(row= 0, column= 0, padx= 10, pady=20)

    staff_name_entry= Entry( frame_staff_detail, bd=1 , relief= SOLID, font= ('arial', 15), width = 30)
    staff_name_entry.grid(row= 0, column= 1,  pady= 15)

    age_text= Label( frame_staff_detail, text= 'Age\t\t:', font= ('arial', 15), bg= '#a8e3ff', bd= 0, relief= SOLID)
    age_text.grid(row= 1, column= 0, padx= 10, pady=15)

    age_entry= Entry( frame_staff_detail, bd=1 , relief= SOLID, font= ('arial', 15), width = 30)
    age_entry.grid(row= 1, column= 1,  pady= 15)    
    

    gender_text= Label( frame_staff_detail, text= 'Gender\t\t:', font= ('arial', 15), bg= '#a8e3ff', bd= 0, relief= SOLID)
    gender_text.grid(row= 2, column= 0, padx= 10, pady=15)

    gender_entry= ttk.Combobox( frame_staff_detail, font= ('arial', 15), width = 29)
    gender_entry.grid(row= 2, column= 1,  pady= 15)
    gender_entry['values'] = ('Male','Female','Transgender')

    marital_status_text= Label( frame_staff_detail, text= 'Marital Status\t:', font= ('arial', 15), bg= '#a8e3ff', bd= 0, relief= SOLID)
    marital_status_text.grid(row= 3, column= 0, padx= 10, pady=15)

    marital_status_entry= ttk.Combobox( frame_staff_detail, font= ('arial', 15), width = 29)
    marital_status_entry.grid(row= 3, column= 1,  pady= 15)
    marital_status_entry['values'] = ('Single', 'Married', 'Widowed', 'Seperated', 'Divorced')
   
    blood_group_text= Label( frame_staff_detail, text= 'Blood Group\t:', font= ('arial', 15), bg= '#a8e3ff', bd= 0, relief= SOLID)
    blood_group_text.grid(row= 4, column= 0, padx= 10, pady=15)

    blood_group_entry= ttk.Combobox( frame_staff_detail, font= ('arial', 15), width = 29)
    blood_group_entry.grid(row= 4, column= 1,  pady= 15)
    blood_group_entry["values"] = ('A+','A-','B+','B-','O+','O-','AB+','AB-')
       
    address_text= Label( frame_staff_detail, text= 'Address\t\t :', font= ('arial', 15), bg= '#a8e3ff', bd= 0, relief= SOLID)
    address_text.grid(row= 5, column= 0, padx= 10, pady=15)

    address_entry= Text( frame_staff_detail, bd=1 , relief= SOLID, height = 4, font= ('arial', 12), width = 37)
    address_entry.grid(row= 5, column= 1,  pady= 15, rowspan = 5)

    blank_text= Label( frame_staff_detail, bg= '#a8e3ff', font= ('arial', 5))
    blank_text.grid(row= 6, column= 0)
    blank_text= Label( frame_staff_detail, bg= '#a8e3ff', font= ('arial', 5))
    blank_text.grid(row= 7, column= 0)

    dateofbirth_text= Label( frame_staff_detail, text= 'Date of Birth(DOB)  :', font= ('arial', 15), bg= '#a8e3ff', bd= 0, relief= SOLID)
    dateofbirth_text.grid(row= 0, column= 2, padx= 10, pady=15)

    dateofbirth_entry= DateEntry( frame_staff_detail, background = '#0f0b7d', date_pattern = 'dd/mm/y', bd=1 , relief= SOLID, font= ('arial', 15), width = 30)
    dateofbirth_entry.grid(row= 0, column= 3,  pady= 15)

    joiningdate_text= Label( frame_staff_detail, text= 'Joining Date\t :', font= ('arial', 15), bg= '#a8e3ff', bd= 0, relief= SOLID)
    joiningdate_text.grid(row= 1, column= 2, padx= 10, pady=15)

    joiningdate_entry= DateEntry( frame_staff_detail, background = '#0f0b7d', date_pattern = 'dd/mm/y', bd=1 , relief= SOLID, font= ('arial', 15), width = 30)
    joiningdate_entry.grid(row= 1, column= 3,  pady= 15)
   
    contactno_text= Label( frame_staff_detail, text= 'Contact no.\t :', font= ('arial', 15), bg= '#a8e3ff', bd= 0, relief= SOLID)
    contactno_text.grid(row= 2, column= 2, padx= 10, pady=15)

    contactno_entry= Entry( frame_staff_detail, bd=1 , relief= SOLID, font= ('arial', 15), width = 30)
    contactno_entry.grid(row= 2, column= 3,  pady= 15)

    Email_text= Label( frame_staff_detail, text= 'Email\t\t :', font= ('arial', 15), bg= '#a8e3ff', bd= 0, relief= SOLID)
    Email_text.grid(row= 3, column= 2, padx= 10, pady=15)

    Email_entry= Entry( frame_staff_detail, bd=1 , relief= SOLID, font= ('arial', 15), width = 30)
    Email_entry.grid(row= 3, column= 3,  pady= 15)

    aadhar_text= Label( frame_staff_detail, text= 'Aadhar\t\t :', font= ('arial', 15), bg= '#a8e3ff', bd= 0, relief= SOLID)
    aadhar_text.grid(row= 4, column= 2, padx= 10, pady=15)

    aadhar_entry= Entry( frame_staff_detail, bd=1 , relief= SOLID, font= ('arial', 15), width = 30)
    aadhar_entry.grid(row= 4, column= 3,  pady= 15)

    salary_text= Label( frame_staff_detail, text= 'Salary\t\tRs.', font= ('arial', 15), bg= '#a8e3ff', bd= 0, relief= SOLID)
    salary_text.grid(row= 5, column= 2, padx= 10, pady=15)

    salary_entry= Entry( frame_staff_detail, bd=1 , relief= SOLID, font= ('arial', 15), width = 30)
    salary_entry.grid(row= 5, column= 3,  pady= 1)
    
    
    # *********************** Frame for Staff Buttons ***********************

    frame_staff_button = Frame(frame_1, width = 1150, height=50, bg = '#ffffff',  bd= 0, relief= SOLID)
    frame_staff_button.grid(row = 3, column = 0)

    reset_button= Button( frame_staff_button,text='RESET',  bd=1 , relief= SOLID,bg='#0f0b7d', font= ('arial', 12, 'bold'),fg='#ffffff', width = 31, command = reset_add_staff)
    reset_button.grid(row= 0, column=0,padx= 10,  pady= 10)
    
    save_staff_button= Button( frame_staff_button,text='SAVE',  bd=1 , relief= SOLID, bg='#0f0b7d', font= ('arial', 12, 'bold'), fg='#ffffff', width = 31, command = validate_add_staff)
    save_staff_button.grid(row= 0, column=1,  pady= 10)

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Edit Staff >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    frame_header_staff = Frame(frame_2, width=1150, height=60, bg='#ffffff', bd=0, relief=SOLID)
    frame_header_staff.grid(row=0, column=0, columnspan=2, pady=5)
    frame_header_staff.pack_propagate(0)

    edit_staff_header = Label(frame_header_staff, text='Edit Staff', font=('arial', 25, 'bold'), fg='#012552', bd=0, bg='#ffffff', relief=SOLID)
    edit_staff_header.pack(pady=5)

    # **************** Edit Staff frame **********************
    frame_edit_staff = Frame(frame_2, width=372, height=460, bg='#ffffff', bd=1, relief=SOLID)
    frame_edit_staff.grid(row=1, column=0, rowspan=2, padx=5, pady=5)
    frame_edit_staff.grid_propagate(0)

    # Frame - Staff Input boxes
    edit_staff_subframe_1 = Frame(frame_edit_staff, width=370, height=35, bg='#0f0b7d')
    edit_staff_subframe_1.grid()
    edit_staff_subframe_1.grid_propagate(0)

    staff_id_label = Label(edit_staff_subframe_1, text='Staff Id\t\t:', bg='#0f0b7d', fg='#ffffff',font=('arial', 13))
    staff_id_label.grid(padx=5, pady=5)
    staff_id_entry = Entry(edit_staff_subframe_1, font=('arial', 13))
    staff_id_entry.grid(padx=5, pady=5, row=0, column=1)

    # Frame - Inputs and Labels of Staff Details
    edit_staff_subframe_2 = Frame(frame_edit_staff, width=370, height=360, bg='#a8e3ff')
    edit_staff_subframe_2.grid(row=1, column=0)
    edit_staff_subframe_2.grid_propagate(0)

    staff_name_edit_label = Label(edit_staff_subframe_2, text='Name\t\t:', font=('arial', 12), bg='#a8e3ff')
    staff_name_edit_label.grid(padx=5, pady=3)
    staff_name_edit_entry = Entry(edit_staff_subframe_2, font=('arial', 12))
    staff_name_edit_entry.grid(padx=5, pady=3, row=0, column=1)

    staff_age_edit_label = Label(edit_staff_subframe_2, text='Age\t\t:', font=('arial', 12), bg='#a8e3ff')
    staff_age_edit_label.grid(padx=5, pady=3, row=1, column=0)
    staff_age_edit_entry = Entry(edit_staff_subframe_2, font=('arial', 12))
    staff_age_edit_entry.grid(padx=5, pady=3, row=1, column=1)

    staff_gender_edit_label = Label(edit_staff_subframe_2, text='Gender\t\t:', font=('arial', 12), bg='#a8e3ff')
    staff_gender_edit_label.grid(padx=5, pady=3, row=2, column=0)
    staff_gender_edit_entry = ttk.Combobox(edit_staff_subframe_2, font=('arial', 12), width=18)
    staff_gender_edit_entry.grid(padx=5, pady=3, row=2, column=1)
    staff_gender_edit_entry['values'] = ('Male', 'Female', 'Transgender')

    staff_marital_edit_label = Label(edit_staff_subframe_2, text='Marital Status\t:', font=('arial', 12), bg='#a8e3ff')
    staff_marital_edit_label.grid(padx=5, pady=3, row=4, column=0)
    staff_marital_edit_entry = ttk.Combobox(edit_staff_subframe_2, font=('arial', 12), width=18)
    staff_marital_edit_entry.grid(padx=5, pady=3, row=4, column=1)
    staff_marital_edit_entry['values'] = ('Single', 'engaged', 'Married')

    dateofbirth_edit_text= Label(edit_staff_subframe_2, text= 'Date of Birth(DOB)   :', font= ('arial', 12), bg= '#a8e3ff')
    dateofbirth_edit_text.grid(padx=5, pady=3, row=5, column=0)
    dateofbirth_edit_entry= DateEntry(edit_staff_subframe_2, background = '#0f0b7d', date_pattern = 'dd/mm/y', font= ('arial', 12), width = 18)
    dateofbirth_edit_entry.grid(padx=5, pady=3, row=5, column=1)

    joiningdate_edit_text= Label(edit_staff_subframe_2, text= 'Joining Date\t:', font= ('arial', 12), bg= '#a8e3ff')
    joiningdate_edit_text.grid(padx=5, pady=3, row=6, column=0)
    joiningdate_edit_entry= DateEntry(edit_staff_subframe_2, background = '#0f0b7d', date_pattern = 'dd/mm/y', font= ('arial', 12), width = 18)
    joiningdate_edit_entry.grid(padx=5, pady=3, row=6, column=1)

    staff_blood_grp_edit_label = Label(edit_staff_subframe_2, text='Blood Group\t:', font=('arial', 12), bg='#a8e3ff')
    staff_blood_grp_edit_label.grid(padx=5, pady=3, row=7, column=0)
    staff_blood_grp_edit_entry = Entry(edit_staff_subframe_2, font=('arial', 12))
    staff_blood_grp_edit_entry.grid(padx=5, pady=3, row=7, column=1)

    staff_address_edit_label = Label(edit_staff_subframe_2, text='Address\t\t:', font=('arial', 12), bg='#a8e3ff')
    staff_address_edit_label.grid(padx=5, pady=3, row=8, column=0)
    staff_address_edit_entry = Entry(edit_staff_subframe_2, font=('arial', 12))
    staff_address_edit_entry.grid(padx=5, pady=3, row=8, column=1)

    staff_contact_edit_label = Label(edit_staff_subframe_2, text='Contact no.\t:', font=('arial', 12), bg='#a8e3ff')
    staff_contact_edit_label.grid(padx=5, pady=3, row=9, column=0)
    staff_contact_edit_entry = Entry(edit_staff_subframe_2, font=('arial', 12))
    staff_contact_edit_entry.grid(padx=5, pady=3, row=9, column=1)

    staff_email_edit_label = Label(edit_staff_subframe_2, text='Email Address\t:', font=('arial', 12),bg='#a8e3ff')
    staff_email_edit_label.grid(padx=5, pady=3, row=10, column=0)
    staff_email_edit_entry = Entry(edit_staff_subframe_2, font=('arial', 12))
    staff_email_edit_entry.grid(padx=5, pady=3, row=10, column=1)

    staff_addharr_edit_label = Label(edit_staff_subframe_2, text='Addharr no.\t:', font=('arial', 12),bg='#a8e3ff')
    staff_addharr_edit_label.grid(padx=5, pady=3, row=11, column=0)
    staff_addharr_edit_entry = Entry(edit_staff_subframe_2, font=('arial', 12))
    staff_addharr_edit_entry.grid(padx=5, pady=3, row=11, column=1)

    staff_salary_edit_label = Label(edit_staff_subframe_2, text='Salary\t\t:', font=('arial', 12), bg='#a8e3ff')
    staff_salary_edit_label.grid(padx=5, pady=3, row=12, column=0)
    staff_salary_edit_entry = Entry(edit_staff_subframe_2, font=('arial', 12))
    staff_salary_edit_entry.grid(padx=5, pady=3, row=12, column=1)

    
    # Frames - Operational Buttons - Update, Delete, Reset and Print
    edit_staff_subframe_3 = Frame(frame_edit_staff, width=370, height=63, bg='#a8e3ff')
    edit_staff_subframe_3.grid(row=3, column=0)
    edit_staff_subframe_3.grid_propagate(0)

    edit_update_button = Button(edit_staff_subframe_3, text='Update', bd=1, relief=SOLID, bg='#0f0b7d',font=('arial', 11, 'bold'), fg='#ffffff', width=10, height=2 , command=update_record_staff)
    edit_update_button.grid(row=0, column=0, padx=20, pady=10)

    edit_delete_button = Button(edit_staff_subframe_3, text='Delete', bd=1, relief=SOLID, bg='#0f0b7d',font=('arial', 11, 'bold'), fg='#ffffff', width=10, height=2 , command=delete_record_staff)
    edit_delete_button.grid(row=0, column=1, pady=10)

    edit_reset_button = Button(edit_staff_subframe_3, text='Reset', bd=1, relief=SOLID, bg='#0f0b7d',font=('arial', 11, 'bold'), fg='#ffffff', width=10, height=2 , command=clear_enteries_staff)
    edit_reset_button.grid(row=0, column=2, pady=10, padx=20)



    # ************************ Search Staff Frame *********************

    frame_search_staff = Frame(frame_2, width=750, height=60, bg='#a8e3ff', bd=1, relief=SOLID)
    frame_search_staff.grid(row=1, column=1, padx=5, pady=5)
    frame_search_staff.pack_propagate(0)

    search_label = Label(frame_search_staff, width=74, text='Search Staff', bg='#0f0b7d', fg='#ffffff',font=("arial", 13, "bold"))
    search_label.pack(anchor='n', ipadx=4)

    search_staff_by = Label(frame_search_staff, text='Search By :', width=15, bg='#a8e3ff',font=("arial", 12, "bold"))
    search_staff_by.pack(side=LEFT)
    search_staff_by_entry = ttk.Combobox(frame_search_staff, width=16, font=("arial", 12, "bold"))
    search_staff_by_entry.pack(side=LEFT)
    search_staff_by_entry['values'] = ['Staff Name', 'Staff Id']
    search_staff_by_entry.set("Staff Name")
    search_staff_name = Label(frame_search_staff, text='Search :', width=15, bg='#a8e3ff',font=("arial", 12, "bold"))
    search_staff_name.pack(side=LEFT, padx=10)
    search_staff_name_entry = Entry(frame_search_staff, width=18, font=("arial", 12, "bold"))
    search_staff_name_entry.pack(side=LEFT)

    # Search Staff Button
    staff_search_button = Button(frame_search_staff, text = "Search", bg = '#0f0b7d', fg = '#ffffff', width = 10, command=search_staff)
    staff_search_button.pack(side = LEFT, padx = 10)

    # *********************** View Staff List Frame *******************
    frame_view_staff = Frame(frame_2, width=750, height=390, bg='#ffffff', bd=1, relief=SOLID)
    frame_view_staff.grid(row=2, column=1, pady=5, padx=5)
    frame_view_staff.pack_propagate(0)


    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  TREE VIEW >>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    
    global my_tree_staff

    # Add Some Style
    style_tree_staff = ttk.Style()

    # Pick A Theme
    # style.theme_use('default')

    # Configure the Treeview Colors
    style_tree_staff.configure("Treeview",
        background="#a8e3ff",
        foreground="black",
        rowheight=25,
        fieldbackground="#a8e3ff",
        font = ("arial", 10))

    # Change Selected Color #347083
    style_tree_staff.map('Treeview',
        background=[('selected', '#006aff')])

    # Create a Treeview Frame
    tree_frame_staff = Frame(frame_view_staff)
    tree_frame_staff.pack()

    # Create a Treeview Scrollbar
    tree_scroll = Scrollbar(tree_frame_staff , orient="vertical")
    tree_scroll_bottom = Scrollbar(tree_frame_staff, orient="horizontal")
    tree_scroll_bottom.pack(side=BOTTOM , fill=X)
    tree_scroll.pack(side=RIGHT, fill=Y)

    # Create The Treeview
    my_tree_staff = ttk.Treeview(tree_frame_staff, yscrollcommand=tree_scroll.set, xscrollcommand=tree_scroll_bottom, selectmode="extended", height=390)
    
    my_tree_staff.pack(fill="both")

    # Configure the Scrollbar
    tree_scroll.config(command=my_tree_staff.yview)
    tree_scroll_bottom.config(command = my_tree_staff.xview)

    
    # Define Our Columns
    my_tree_staff['columns'] = ("Sr.No", "Name","Age","Gender","Marital Status","BG","Address","DOB","Joining date","Contact","Email","Aadhar","Salary")


    # Format Our Columns
    my_tree_staff.column("#0", width=0, stretch=NO)
    my_tree_staff.column("Sr.No", anchor=W, width=20)
    my_tree_staff.column("Name", anchor=W, width=150)
    my_tree_staff.column("Age", anchor=W, width=40)
    my_tree_staff.column("Gender", anchor=W, width=50)
    my_tree_staff.column("Marital Status", anchor=CENTER, width=80)
    my_tree_staff.column("BG", anchor=CENTER, width=40)
    my_tree_staff.column("Address", anchor=CENTER, width=120)
    my_tree_staff.column("DOB", anchor=CENTER, width=70)
    my_tree_staff.column("Joining date", anchor=CENTER, width=70)
    my_tree_staff.column("Contact", anchor=CENTER, width=80)
    my_tree_staff.column("Email", anchor=CENTER, width=150)
    my_tree_staff.column("Aadhar", anchor=CENTER, width=80)
    my_tree_staff.column("Salary", anchor=CENTER, width=80)
   


    # Create Headings
    my_tree_staff.heading("#0", text="", anchor=W ) 
    my_tree_staff.heading("Sr.No", anchor=W, text="Sr.No" )
    my_tree_staff.heading("Name", anchor=W, text="Name")
    my_tree_staff.heading("Age", anchor=W, text="Age")
    my_tree_staff.heading("Gender", anchor=W, text="Gender")
    my_tree_staff.heading("Marital Status", anchor=CENTER, text="Marital Status")
    my_tree_staff.heading("BG", anchor=CENTER, text="BG")
    my_tree_staff.heading("Address", anchor=CENTER, text="Address")
    my_tree_staff.heading("DOB", anchor=CENTER, text="DOB Date")
    my_tree_staff.heading("Joining date", anchor=CENTER, text="Joining date")
    my_tree_staff.heading("Contact", anchor=CENTER, text="Contact")
    my_tree_staff.heading("Email", anchor=CENTER, text="Email")
    my_tree_staff.heading("Aadhar", anchor=CENTER, text="Aadhar")
    my_tree_staff.heading("Salary", anchor=CENTER, text="Salary")

    

    # Create Striped Row Tags
    my_tree_staff.tag_configure('oddrow', background="white")
    my_tree_staff.tag_configure('evenrow', background='#a8e3ff')

    #Adding data to the tree

    my_cursor.execute("SELECT * FROM staff_table")
    records=my_cursor.fetchall()

    edit_count_staff =0

    for record in records :
        if edit_count_staff % 2 == 0:
            my_tree_staff.insert(parent='' , index='end' ,iid = edit_count_staff, text='', values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7] ,record[8],record[9] ,record[10],record[11],record[12]),  tags=('evenrow', ))
 
        else :
            my_tree_staff.insert(parent='' , index='end' ,iid = edit_count_staff, text='', values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7] ,record[8],record[9] ,record[10],record[11],record[12]), tags=('oddrow', ))
        edit_count_staff +=1
    my_tree_staff.bind("<ButtonRelease-1>" , fill_enteries_staff)
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\  Staff Closes ////////////////////////////////


# Clear Medicine Treeview
def clear_company_list_treeview():
    for x in my_tree_company.get_children():
        my_tree_company.delete(x)

# Reset View Medicine Treeview
def reset_view_company():
    clear_company_list_treeview()
    sql_command = "select * from company_table"
    my_cursor.execute(sql_command)
    company_list = my_cursor.fetchall()
    count_company = 0
    for list in company_list:
        if count_company%2==0:
            my_tree_company.insert(parent='', index='end', iid=count_company, text= '', values=[list[0], list[1], list[2], list[3], list[4], list[5], list[6]], tags=('evenrow',))
        else:
            my_tree_company.insert(parent='', index='end', iid=count_company, text= '', values=[list[0], list[1], list[2], list[3], list[4], list[5], list[6]], tags=('oddrow',))
        count_company+=1

# Search Function
def search_company():

    if search_company_by_entry.get()=="Company Name":
        search_by = "Company_name"
    else:
        search_by = "Sr_no"
    search_name = search_company_name_entry.get()

    clear_company_list_treeview()

    sql_command_search = "Select * from company_table where "+search_by+"=%s"
    search_values = [search_name]
    my_cursor.execute(sql_command_search, search_values)
    company_list = my_cursor.fetchall()
    count_company = 0
    for list in company_list:
        if count_company%2==0:
            my_tree_company.insert(parent='', index='end', iid=count_company, text= '', values=(list[0], list[1], list[2], list[3], list[4], list[5], list[6]), tags=('evenrow',))
        else:
            my_tree_company.insert(parent='', index='end', iid=count_company, text= '', values=(list[0], list[1], list[2], list[3], list[4], list[5], list[6]), tags=('oddrow',))
        count_company+=1

# Reset Add Company
def reset_add_company():
    company_name_entry.delete(0, END)
    contact_person_entry.delete(0, END)
    address_entry.delete('1.0', 'end')
    email_entry.delete(0, END)
    contactno_entry.delete(0, END)
    entrydate_entry.delete(0, END)

# Save record to Company Table
def save_to_company_table():
    sql_command = "INSERT INTO company_table(Company_name, Contact_person, Address, Email, Contact_no, Entry_date) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (company_name_entry.get(), contact_person_entry.get(), address_entry.get("1.0", "end-1c"), email_entry.get(), contactno_entry.get(), entrydate_entry.get_date())
    my_cursor.execute(sql_command, values)
    mydb.commit()
    messagebox.showinfo("Save", "Company record saved successfully.")
    reset_add_company()
    company_name_entry.focus()

# Validate Add Company Entries
def validate_add_company():
    valid = 1
    if valid == 1:
        if contact_person_entry.get().isdigit()==True:
            messagebox.showinfo("Warning", "Numbers are not allowed in Contact Person Name.")
            valid = 0
            contact_person_entry.focus_set()
    if valid ==1:
        if '@' not in email_entry.get():
            messagebox.showinfo("Warning", "Please enter valid Email Id.")
            valid = 0
            email_entry.focus_set()
    if contactno_entry.get().isdigit()==False:
        messagebox.showinfo("Warning", "Alphbets are not allowed in Contact No.")
        valid = 0
        contactno_entry.focus_set()
    if valid==1:
        if len(contactno_entry.get())!=10:
            if len(contactno_entry.get())!=12:
                messagebox.showinfo("Warning", "Conatct No. must contain:\n2. Length of 10 or 12 Numbers.")
                valid = 0
                contactno_entry.focus_set()
    
    if valid == 1:
        confirm = messagebox.askyesno("Comfirm","Do you want Save the Record")
        if confirm==1:
            save_to_company_table()

# Fill Entries Edit Company by Mouse left click release
def  fill_enteries_company(e):
    company_id_entry.delete(0,END)
    company_name_edit_entry.delete(0,END)
    company_contact_person_edit_entry.delete(0,END)
    company_address_edit_entry.delete(0,END)
    company_email_edit_entry.delete(0,END)
    
    company_contact_edit_entry.delete(0,END)
    company_entry_edit_date_entry.delete(0,END)
    
    selected = my_tree_company.focus()
    value = my_tree_company.item(selected , "values")

    company_id_entry.insert(0,value[0])
    company_name_edit_entry.insert(0,value[1])
    company_contact_person_edit_entry.insert(0,value[2])
    company_address_edit_entry.insert(0,value[3])
    company_email_edit_entry.insert(0,value[4])
    company_contact_edit_entry.insert(0,value[5])
    company_entry_edit_date_entry.insert(0,value[6])

# Clear Entries Edit Company
def clear_enteries_company():
    company_id_entry.delete(0,END)
    company_name_edit_entry.delete(0,END)
    company_contact_person_edit_entry.delete(0,END)
    company_email_edit_entry.delete(0,END)
    company_address_edit_entry.delete(0,END)
    company_contact_edit_entry.delete(0,END)
    company_entry_edit_date_entry.delete(0,END)
    reset_view_company()

# Delete Record from Company Table
def delete_record_company():
    x = my_tree_company.selection()[0]
    my_tree_company.delete(x)

    string = "DELETE FROM company_table WHERE Sr_no="+str(company_id_entry.get())
    # print(string)
    my_cursor.execute(string)
    messagebox.showinfo("Deleted", "Desired Record has been deleted")
    clear_enteries_company()

# Update Record to Company Table
def update_record_company():
    #grab the record 
    selected = my_tree_company.focus()

    #Update the record 
    my_tree_company.item(selected , text="" ,values=( 
        company_id_entry.get(),
        company_name_edit_entry.get(),
        company_contact_person_edit_entry.get(),
        company_address_edit_entry.get(),
        company_email_edit_entry.get(),
       
        company_contact_edit_entry.get(),
        company_entry_edit_date_entry.get_date()
        ))


    sql_command = '''UPDATE company_table SET Company_name=%s ,Contact_person=%s , Address=%s , Email=%s , Contact_no=%s, Entry_date=%s where Sr_no=%s'''
    values = (
        company_name_edit_entry.get(),
        company_contact_person_edit_entry.get(),
        company_address_edit_entry.get(),
        company_email_edit_entry.get(),
        
        company_contact_edit_entry.get(),
        company_entry_edit_date_entry.get_date(),
        company_id_entry.get()
        )

    my_cursor.execute(sql_command, values)
    mydb.commit()
    clear_enteries_company()
    messagebox.showinfo("Updated", "Desired Record has been Updated")

# Call Company Frame
def company():
    clear_f4()
    f4.config(bg = "#9cffbb")       # Light Green color for Company Frame
    
    style = ttk.Style()
    style.configure("TNotebook", bd =0, background="#9cffbb", foreground='green')
    Notebook_frames()
    frame_option.add(frame_1, text = "Add company  ")
    frame_option.add(frame_2, text = "  Edit company  ")

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Add Company >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    global company_name_entry, contact_person_entry, address_entry, email_entry, contactno_entry, entrydate_entry

    global  company_id_entry,company_name_edit_entry,company_contact_person_edit_entry,company_email_edit_entry,company_address_edit_entry,company_contact_edit_entry,company_entry_edit_date_entry
    
    global edit_count_company, search_company_by_entry, search_company_name_entry

    # ******************** Frame for Heading - Add Company ********************

    frame_header_company = Frame(frame_1, width = 1150, height= 60, bg = '#ffffff', bd= 0, relief= SOLID)
    frame_header_company.grid(row = 0, column = 0)
    frame_header_company.pack_propagate(0)

    add_company_text = Label(frame_header_company, text= 'Add Company',font = ('arial', 25, 'bold'), fg= '#014710',bd= 0,  width = 100 ,bg = '#ffffff', relief= SOLID)
    add_company_text.pack(padx = 5, pady= 10)

    # ******************** Frame for Company Info Label ***********************

    frame_companyinfo = Frame(frame_1, width = 1140, height= 30, bg = '#098021',  bd= 1, relief= SOLID)
    frame_companyinfo.grid(row = 1, column = 0, padx= 5)
    frame_companyinfo.pack_propagate(0)

    add_company_info_text = Label(frame_companyinfo, text= 'Company Information', font= ('arial', 12, 'bold'), fg = '#ffffff', width = 17, bg= '#098021')
    add_company_info_text.pack(side= LEFT, padx=0)

    # ******************** Frame for Company Details **************************

    frame_company_detail = Frame(frame_1, width = 1140, height=405, bg = '#9cffbb',  bd= 1, relief= SOLID)
    frame_company_detail.grid(row = 2, column = 0, padx= 5)
    frame_company_detail.grid_propagate(0)

    company_name_text= Label( frame_company_detail, text= 'Company Name\t:', font= ('arial', 15), bg= '#9cffbb', bd= 0, relief= SOLID)
    company_name_text.grid(row= 0, column= 0, padx= 10, pady=40)

    company_name_entry= Entry( frame_company_detail, bd=1 , relief= SOLID, font= ('arial', 15), width = 30)
    company_name_entry.grid(row= 0, column= 1,  pady= 40)
    
    contact_person_text= Label( frame_company_detail, text= 'Contact Person\t:', font= ('arial', 15), bg= '#9cffbb', bd= 0, relief= SOLID)
    contact_person_text.grid(row= 1, column= 0, padx= 10, pady=40)

    contact_person_entry= Entry( frame_company_detail, bd=1 , relief= SOLID, font= ('arial', 15), width = 30)
    contact_person_entry.grid(row= 1, column= 1,  pady= 40)
    
    address_text= Label( frame_company_detail, text= 'Address\t\t:', font= ('arial', 15), bg= '#9cffbb', bd= 0, relief= SOLID)
    address_text.grid(row= 2, column= 0, padx= 10, pady=40 )

    address_entry= Text( frame_company_detail, bd=1, height = 4, relief= SOLID, font= ('arial', 15), width = 31)
    address_entry.grid(row= 2, column= 1,  pady= 40, rowspan = 4)

    blank_text= Label( frame_company_detail, bg= '#a8e3ff', font= ('arial', 5))
    blank_text.grid(row= 3, column= 0)
    blank_text= Label( frame_company_detail, bg= '#a8e3ff', font= ('arial', 5))
    blank_text.grid(row= 4, column= 0)
    

    email_text= Label( frame_company_detail, text= 'Email\t\t:', font= ('arial', 15), bg= '#9cffbb', bd= 0, relief= SOLID)
    email_text.grid(row= 0, column= 2, padx= 10, pady=40)

    email_entry= Entry( frame_company_detail, bd=1 , relief= SOLID, font= ('arial', 15), width = 30)
    email_entry.grid(row= 0, column= 3,  pady= 40)

    contactno_text= Label( frame_company_detail, text= 'Contact no.\t:', font= ('arial', 15), bg= '#9cffbb', bd= 0, relief= SOLID)
    contactno_text.grid(row= 1, column= 2, padx= 10, pady=40)

    contactno_entry= Entry( frame_company_detail, bd=1 , relief= SOLID, font= ('arial', 15), width = 31)
    contactno_entry.grid(row= 1, column= 3,  pady= 40)

    entrydate_text= Label( frame_company_detail, text= 'Entry date\t:', font= ('arial', 15), bg= '#9cffbb', bd= 0, relief= SOLID)
    entrydate_text.grid(row= 2, column= 2, padx= 10, pady=40)

    entrydate_entry= DateEntry(frame_company_detail ,font= ('arial', 15), width=30, background='#098021', date_pattern = "dd/mm/yyyy", foreground='white', borderwidth=2)
    entrydate_entry.grid(row = 2, column= 3, pady=40)

    # ******************** Frame for Heading - Add Company ********************

    frame_company_button = Frame(frame_1, width = 1150, height=50, bg = '#ffffff',  bd= 0, relief= SOLID)
    frame_company_button.grid(row = 3, column = 0)

    reset_button= Button( frame_company_button,text='RESET',  bd=1 , relief= SOLID,bg='#098021', font= ('arial', 12, 'bold'),fg='#ffffff', width = 31, command = reset_add_company)
    reset_button.grid(row= 0, column=0,padx= 10,  pady= 10)
    
    reset_button= Button( frame_company_button,text='SAVE',  bd=1 , relief= SOLID, bg='#098021', font= ('arial', 12, 'bold'), fg='#ffffff', width = 31, command = validate_add_company)
    reset_button.grid(row= 0, column=1,  pady= 10)

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Edit Company >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


    frame_header_company= Frame(frame_2, width=1150, height=60, bg='#ffffff', bd=0, relief=SOLID)
    frame_header_company.grid(row=0, column=0, columnspan=2, pady=5)
    frame_header_company.pack_propagate(0)

    edit_company_header = Label(frame_header_company, text='Edit Company', font=('arial', 25, 'bold'), fg='#014710', bd=0, bg='#ffffff', relief=SOLID) 
    edit_company_header.pack(pady=5)

    # **************** Edit Company frame **********************
    frame_edit_company = Frame(frame_2, width=372, height=460, bg='#ffffff', bd=1, relief=SOLID)
    frame_edit_company.grid(row=1, column=0, rowspan=2, padx=5, pady=5)
    frame_edit_company.grid_propagate(0)

    # Frame - Company Input boxes
    edit_company_subframe_1 = Frame(frame_edit_company, width=370, height=40, bg='#098021')
    edit_company_subframe_1 .grid()
    edit_company_subframe_1 .grid_propagate(0)

    company_id_label = Label(edit_company_subframe_1 , text='Company Id\t:', bg='#098021', fg='#ffffff', font=('arial', 13))
    company_id_label.grid(padx=5, pady=5)
    company_id_entry = Entry(edit_company_subframe_1 , font=('arial', 13))
    company_id_entry.grid(padx=5, pady=5, row=0, column=1)

    # Frame - Inputs and Labels of Company Details
    edit_company_subframe_2 = Frame(frame_edit_company, width=370, height=350, bg='#9cffbb')
    edit_company_subframe_2.grid(row=1, column=0)
    edit_company_subframe_2.grid_propagate(0)

    company_name_edit_label = Label(edit_company_subframe_2, text='Company Name\t:', font=('arial', 12), bg='#9cffbb')
    company_name_edit_label.grid(padx=5, pady=15)
    company_name_edit_entry = Entry(edit_company_subframe_2, font=('arial', 12))
    company_name_edit_entry.grid(padx=5, pady=15, row=0, column=1)

    company_contact_person_edit_label = Label(edit_company_subframe_2, text='Contact Person\t:', font=('arial', 12), bg='#9cffbb')
    company_contact_person_edit_label.grid(padx=5, pady=15, row=1, column=0)
    company_contact_person_edit_entry = Entry(edit_company_subframe_2, font=('arial', 12))
    company_contact_person_edit_entry.grid(padx=5, pady=15, row=1, column=1)

    company_email_edit_label = Label(edit_company_subframe_2, text='Email\t\t:', font=('arial', 12), bg='#9cffbb')
    company_email_edit_label.grid(padx=5, pady=15, row=2, column=0)
    company_email_edit_entry = Entry(edit_company_subframe_2, font=('arial', 12))
    company_email_edit_entry.grid(padx=5, pady=15, row=2, column=1)

    company_address_edit_label = Label(edit_company_subframe_2, text='Address\t\t:', font=('arial', 12), bg='#9cffbb')
    company_address_edit_label.grid(padx=5, pady=15, row=4, column=0)
    company_address_edit_entry = Entry(edit_company_subframe_2, font=('arial', 12))
    company_address_edit_entry.grid(padx=5, pady=15, row=4, column=1)

    company_contact_edit_label = Label(edit_company_subframe_2, text='Contact no.\t:', font=('arial', 12), bg='#9cffbb')
    company_contact_edit_label.grid(padx=5, pady=15, row=5, column=0)
    company_contact_edit_entry = Entry(edit_company_subframe_2, font=('arial', 12))
    company_contact_edit_entry.grid(padx=5, pady=15, row=5, column=1)

    company_entry_edit_date_label = Label(edit_company_subframe_2, text='Entry Date\t:', font=('arial', 12), bg='#9cffbb')
    company_entry_edit_date_label.grid(padx=5, pady=15, row=6, column=0)
    company_entry_edit_date_entry = DateEntry(edit_company_subframe_2, font=('arial', 12), background='#098021', width=18, date_pattern='dd/mm/y')
    company_entry_edit_date_entry.grid(padx=5, pady=15, row=6, column=1)

    # Frames - Operational Buttons - Update, Delete, Reset and Print
    edit_company_subframe_3 = Frame(frame_edit_company, width=370, height=68, bg='#9cffbb')
    edit_company_subframe_3.grid(row=3, column=0)
    edit_company_subframe_3.grid_propagate(0)

    edit_update_button = Button(edit_company_subframe_3, text='Update', bd=1, relief=SOLID, bg='#098021', font=('arial', 11, 'bold'), fg='#ffffff', width=10, height=2 , command=update_record_company)
    edit_update_button.grid(row=0, column=0, padx=20, pady=10)

    edit_delete_button = Button(edit_company_subframe_3, text='Delete', bd=1, relief=SOLID, bg='#098021', font=('arial', 11, 'bold'), fg='#ffffff', width=10, height=2 , command=delete_record_company)
    edit_delete_button.grid(row=0, column=1, pady=10)

    edit_reset_button = Button(edit_company_subframe_3, text='Reset', bd=1, relief=SOLID, bg='#098021', font=('arial', 11, 'bold'), fg='#ffffff', width=10, height=2 , command=clear_enteries_company)
    edit_reset_button.grid(row=0, column=2, pady=10, padx=20)


    # ************************ Search company Frame *********************

    frame_search_company = Frame(frame_2, width=750, height=60, bg='#9cffbb', bd=1, relief=SOLID)
    frame_search_company.grid(row=1, column=1, padx=5, pady=5)
    frame_search_company.pack_propagate(0)

    search_label = Label(frame_search_company, width=74, text='Search Company', bg='#098021', fg='#ffffff', font=("arial", 13, "bold"))
    search_label.pack(anchor='n', ipadx=4)

    search_company_by = Label(frame_search_company, text='Search By :', width=15, bg='#9cffbb', font=("arial", 12, "bold"))
    search_company_by.pack(side=LEFT)
    search_company_by_entry = ttk.Combobox(frame_search_company, width=16, font=("arial", 12, "bold"))
    search_company_by_entry.pack(side=LEFT)
    search_company_by_entry['values'] = ['Company Name', 'Company Id']
    search_company_by_entry.set("Company Name")

    search_company_name = Label(frame_search_company, text='Search :', width=15, bg='#9cffbb', font=("arial", 12, "bold"))
    search_company_name.pack(side=LEFT, padx=10)
    search_company_name_entry = Entry(frame_search_company, width=18, font=("arial", 12, "bold"))
    search_company_name_entry.pack(side=LEFT)

    # Search Company Button
    company_search_button = Button(frame_search_company, text = "Search", bg = '#098021', fg = '#ffffff', width = 10, command = search_company)
    company_search_button.pack(side = LEFT, padx = 10)

    # *********************** View Company List Frame *******************
    frame_view_company = Frame(frame_2, width=750, height=390, bg='#ffffff', bd=1, relief=SOLID)
    frame_view_company.grid(row=2, column=1, pady=5, padx=5)
    frame_view_company.pack_propagate(0)


    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  TREE VIEW >>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    
    global my_tree_company

    # Add Some Style
    style_tree_company = ttk.Style()

    # Pick A Theme
    # style.theme_use('default')

    # Configure the Treeview Colors
    style_tree_company.configure("Treeview",
        background="#a8e3ff",
        foreground="black",
        rowheight=25,
        fieldbackground="#a8e3ff",
        font = ("arial", 10))

    # Change Selected Color #347083
    style_tree_company.map('Treeview',
        background=[('selected', '#04b32c')])

    # Create a Treeview Frame
    tree_frame_company = Frame(frame_view_company)
    tree_frame_company.pack()

    # Create a Treeview Scrollbar
    tree_scroll = Scrollbar(tree_frame_company , orient="vertical")
    tree_scroll_bottom = Scrollbar(tree_frame_company, orient="horizontal")
    tree_scroll_bottom.pack(side=BOTTOM , fill=X)
    tree_scroll.pack(side=RIGHT, fill=Y)

    # Create The Treeview
    my_tree_company = ttk.Treeview(tree_frame_company, yscrollcommand=tree_scroll.set, xscrollcommand=tree_scroll_bottom, selectmode="extended", height=390)
    
    my_tree_company.pack(fill="both")

    # Configure the Scrollbar
    tree_scroll.config(command=my_tree_company.yview)
    tree_scroll_bottom.config(command = my_tree_company.xview)

    
    # Define Our Columns
    my_tree_company['columns'] = ("Sr.No", "Company Name","Contact Person","Address","Email","Contact No","Entry date")


    # Format Our Columns
    my_tree_company.column("#0", width=0, stretch=NO)
    my_tree_company.column("Sr.No", anchor=W, width=40)
    my_tree_company.column("Company Name", anchor=W, width=128)
    my_tree_company.column("Contact Person", anchor=W, width=100)
    my_tree_company.column("Address", anchor=CENTER, width=180)
    my_tree_company.column("Email", anchor=CENTER, width=150)
    my_tree_company.column("Contact No", anchor=CENTER, width=70)
    my_tree_company.column("Entry date", anchor=CENTER, width=60)
    
 
   

    # Create Headings
    my_tree_company.heading("#0", text="", anchor=W ) 
    my_tree_company.heading("Sr.No", anchor=W, text="Sr.No" )
    my_tree_company.heading("Company Name", anchor=W, text="Company Name")
    my_tree_company.heading("Contact Person", anchor=W, text="Contact Person")
   
    my_tree_company.heading("Address", anchor=CENTER, text="Address")
    my_tree_company.heading("Email", anchor=CENTER, text="Email")

    my_tree_company.heading("Contact No", anchor=CENTER, text="Contact No")
    my_tree_company.heading("Entry date", anchor=CENTER, text="Entry date")
    
   
  

    # Create Striped Row Tags
    my_tree_company.tag_configure('oddrow', background="white")
    my_tree_company.tag_configure('evenrow', background='#9cffbb')

    #Adding data to the tree

    my_cursor.execute("SELECT * FROM company_table")
    records=my_cursor.fetchall()

    edit_count_company =0

    for record in records :
        if edit_count_company % 2 == 0:
            my_tree_company.insert(parent='' , index='end' ,iid = edit_count_company, text='', values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6]),  tags=('evenrow', ))
 
        else :
            my_tree_company.insert(parent='' , index='end' ,iid = edit_count_company, text='', values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6]), tags=('oddrow', ))
        edit_count_company +=1
    my_tree_company.bind("<ButtonRelease-1>" , fill_enteries_company)



# Command of Bottons
def command_button(button_press):
    if button_press == 'sales':
        active_button = 'sales'
        f_sales.config(bg="#fccb83")
        f_medic.config(bg="#ffffff")
        f_staff.config(bg="#ffffff")
        f_compa.config(bg="#ffffff")
        sales_button['bg'] = "#fccb83"
        medicine_button['bg'] = "#ffffff"
        staff_button['bg'] = "#ffffff"
        company_button['bg'] = "#ffffff"
        sales()
        
    elif button_press == 'medicine':
        active_button = 'medicine'
        f_sales.config(bg="#ffffff")
        f_medic.config(bg="#ffb8b8")
        f_staff.config(bg="#ffffff")
        f_compa.config(bg="#ffffff")
        sales_button['bg'] = "#ffffff"
        medicine_button['bg'] = "#ffb8b8"
        staff_button['bg'] = "#ffffff"
        company_button['bg'] = "#ffffff"
        medicine()
        
    elif button_press == 'staff':
        active_button = 'staff'
        f_sales.config(bg="#ffffff")
        f_medic.config(bg="#ffffff")
        f_staff.config(bg="#a8e3ff")
        f_compa.config(bg="#ffffff")
        sales_button['bg'] = "#ffffff"
        medicine_button['bg'] = "#ffffff"
        staff_button['bg'] = "#a8e3ff"
        company_button['bg'] = "#ffffff"
        staff()
        
    elif button_press == 'company':
        active_button = 'company'
        f_sales.config(bg="#ffffff")
        f_medic.config(bg="#ffffff")
        f_staff.config(bg="#ffffff")
        f_compa.config(bg="#9cffbb")
        sales_button['bg'] = "#ffffff"
        medicine_button['bg'] = "#ffffff"
        staff_button['bg'] = "#ffffff"
        company_button['bg'] = "#9cffbb"
        company()

# Shortcuts - Key Recognision
def key_pressed(event):
    
    if keyboard.is_pressed("ctrl+shift+f"):
        dashboard_root.state('zoomed')

    elif keyboard.is_pressed("Esc"):
        dashboard_root.state('normal')

    # Navigation - Sales Tabs
    elif keyboard.is_pressed("e+1"):
        active_button = 'sales'
        command_button(active_button)
        frame_option.select(0)
    elif keyboard.is_pressed("e+2"):
        active_button = 'sales'
        command_button(active_button)
        frame_option.select(1)

    #Navigation - Medicine Tabs
    elif keyboard.is_pressed("t+1"):
        active_button = 'medicine'
        command_button(active_button)
        frame_option.select(0)
    elif keyboard.is_pressed("t+2"):
        active_button = 'medicine'
        command_button(active_button)
        frame_option.select(1)

    #Navigation - Staff Tabs
    elif keyboard.is_pressed("z+1"):
        active_button = 'staff'
        command_button(active_button)
        frame_option.select(0)
    elif keyboard.is_pressed("z+2"):
        active_button = 'staff'
        command_button(active_button)
        frame_option.select(1)

    #Navigation - Company Tabs
    elif keyboard.is_pressed("c+1"):
        active_button = 'company'
        command_button(active_button)
        frame_option.select(0)
    elif keyboard.is_pressed("c+2"):
        active_button = 'company'
        command_button(active_button)
        frame_option.select(1)

# Date Function 
def date():
    today_date = today.strftime("%d, %B %Y")
    return str(today_date)

#Day Function 
def day():
    today_day = today.strftime("%A")
    return str(today_day)

# Digital clock time
def clock():
    digital_clock = time.strftime('%I:%M:%S %p')
    current_time.config(text=digital_clock)
    current_time.after(1000, clock)

# Close Shorcuts
def close_shortcut():
    shortcut_window.destroy()

# ShortCuts
def shortcut():
    global shortcut_window
    shortcut_window = Toplevel(dashboard_root)
    shortcut_window.config(bg = "#ffffff")

    shortcut_label = Label(shortcut_window, text="Shortcuts", bg = "#ffffff", font=("arial", 25,'bold'))
    shortcut_label.pack()

    Mainframe = Frame(shortcut_window, bd = 1, relief=SOLID, bg = "#ffffff")
    Mainframe.pack()

    shortcuts_list_box = Text(Mainframe, width=60, height=10, bg = "#ffffff", bd=0, relief = SOLID)
    shortcuts_list_box.pack()

    full_screen = Label(shortcuts_list_box, text = "General", bg = "#ffffff", font = ('Consolas',15, 'bold'), width=60)
    full_screen.pack()

    shortcuts_list_box = Text(Mainframe, width=100, height=10, bg = "#ffffff", bd=0, relief = SOLID)
    shortcuts_list_box.pack()

    full_screen = Label(shortcuts_list_box, text = "Full Screen on\t\t\t\t", bg = "#ffffff", width=40, font = ('Consolas',12), justify=LEFT)
    full_screen.pack(side = LEFT)
    full_screen = Label(shortcuts_list_box, text = "ctrl+shift+f", bg = "#ffffff", width=20, font = ('Consolas',12), justify=RIGHT)

    shortcuts_list_box = Text(Mainframe, width=100, height=10, bg = "#ffffff", bd=0, relief = SOLID)
    shortcuts_list_box.pack()
    
    full_screen.pack(side = LEFT)
    full_screen = Label(shortcuts_list_box, text = "Full Screen off\t\t\t\t", bg = "#ffffff", width=40, font = ('Consolas',12), justify=LEFT)
    full_screen.pack(side = LEFT)
    full_screen = Label(shortcuts_list_box, text = "esc", width=20, bg = "#ffffff", font = ('Consolas',12), justify=RIGHT)
    full_screen.pack(side = LEFT)



    Mainframe = Frame(shortcut_window, bd = 1, relief=SOLID, bg = "#ffffff")
    Mainframe.pack()

    shortcuts_list_box = Text(Mainframe, width=60, height=10, bg = "#ffffff", bd=0, relief = SOLID)
    shortcuts_list_box.pack()

    full_screen = Label(shortcuts_list_box, text = "Sales", bg = "#ffffff", font = ('Consolas',15, 'bold'), width=60)
    full_screen.pack()

    shortcuts_list_box = Text(Mainframe, width=100, height=10, bg = "#ffffff", bd=0, relief = SOLID)
    shortcuts_list_box.pack()

    full_screen = Label(shortcuts_list_box, text = "Point of Sales\t\t\t\t", bg = "#ffffff", width=40, font = ('Consolas',12), justify=LEFT)
    full_screen.pack(side = LEFT)
    full_screen = Label(shortcuts_list_box, text = "e+1", bg = "#ffffff", width=20, font = ('Consolas',12), justify=RIGHT)

    shortcuts_list_box = Text(Mainframe, width=100, height=10, bg = "#ffffff", bd=0, relief = SOLID)
    shortcuts_list_box.pack()
    
    full_screen.pack(side = LEFT)
    full_screen = Label(shortcuts_list_box, text = "View Sales\t\t\t\t", bg = "#ffffff", width=40, font = ('Consolas',12), justify=LEFT)
    full_screen.pack(side = LEFT)
    full_screen = Label(shortcuts_list_box, text = "e+2", width=20, bg = "#ffffff", font = ('Consolas',12), justify=RIGHT)
    full_screen.pack(side = LEFT)



    Mainframe = Frame(shortcut_window, bd = 1, relief=SOLID, bg = "#ffffff")
    Mainframe.pack()
    
    shortcuts_list_box = Text(Mainframe, width=60, height=10, bg = "#ffffff", bd=0, relief = SOLID)
    shortcuts_list_box.pack()

    full_screen = Label(shortcuts_list_box, text = "Medicine", bg = "#ffffff", font = ('Consolas',15, 'bold'), width=60)
    full_screen.pack()

    shortcuts_list_box = Text(Mainframe, width=100, height=10, bg = "#ffffff", bd=0, relief = SOLID)
    shortcuts_list_box.pack()

    full_screen = Label(shortcuts_list_box, text = "Add Medicine\t\t\t\t", bg = "#ffffff", width=40, font = ('Consolas',12), justify=LEFT)
    full_screen.pack(side = LEFT)
    full_screen = Label(shortcuts_list_box, text = "t+1", bg = "#ffffff", width=20, font = ('Consolas',12), justify=RIGHT)

    shortcuts_list_box = Text(Mainframe, width=100, height=10, bg = "#ffffff", bd=0, relief = SOLID)
    shortcuts_list_box.pack()
    
    full_screen.pack(side = LEFT)
    full_screen = Label(shortcuts_list_box, text = "Edit Medicine\t\t\t\t", bg = "#ffffff", width=40, font = ('Consolas',12), justify=LEFT)
    full_screen.pack(side = LEFT)
    full_screen = Label(shortcuts_list_box, text = "t+2", width=20, bg = "#ffffff", font = ('Consolas',12), justify=RIGHT)
    full_screen.pack(side = LEFT)


    Mainframe = Frame(shortcut_window, bd = 1, relief=SOLID, bg = "#ffffff")
    Mainframe.pack()

    shortcuts_list_box = Text(Mainframe, width=60, height=10, bg = "#ffffff", bd=0, relief = SOLID)
    shortcuts_list_box.pack()

    full_screen = Label(shortcuts_list_box, text = "Staff", bg = "#ffffff", font = ('Consolas',15, 'bold'), width=60)
    full_screen.pack()

    shortcuts_list_box = Text(Mainframe, width=100, height=10, bg = "#ffffff", bd=0, relief = SOLID)
    shortcuts_list_box.pack()

    full_screen = Label(shortcuts_list_box, text = "Add Staff\t\t\t\t", bg = "#ffffff", width=40, font = ('Consolas',12), justify=LEFT)
    full_screen.pack(side = LEFT)
    full_screen = Label(shortcuts_list_box, text = "z+1", bg = "#ffffff", width=20, font = ('Consolas',12), justify=RIGHT)

    shortcuts_list_box = Text(Mainframe, width=100, height=10, bg = "#ffffff", bd=0, relief = SOLID)
    shortcuts_list_box.pack()
    
    full_screen.pack(side = LEFT)
    full_screen = Label(shortcuts_list_box, text = "Edit Staff\t\t\t\t", bg = "#ffffff", width=40, font = ('Consolas',12), justify=LEFT)
    full_screen.pack(side = LEFT)
    full_screen = Label(shortcuts_list_box, text = "z+2", width=20, bg = "#ffffff", font = ('Consolas',12), justify=RIGHT)
    full_screen.pack(side = LEFT)



    Mainframe = Frame(shortcut_window, bd = 1, relief=SOLID, bg = "#ffffff")
    Mainframe.pack()

    shortcuts_list_box = Text(Mainframe, width=60, height=10, bg = "#ffffff", bd=0, relief = SOLID)
    shortcuts_list_box.pack()

    full_screen = Label(shortcuts_list_box, text = "Company", bg = "#ffffff", font = ('Consolas',15, 'bold'), width=60)
    full_screen.pack()

    shortcuts_list_box = Text(Mainframe, width=100, height=10, bg = "#ffffff", bd=0, relief = SOLID)
    shortcuts_list_box.pack()

    full_screen = Label(shortcuts_list_box, text = "Add Company\t\t\t\t", bg = "#ffffff", width=40, font = ('Consolas',12), justify=LEFT)
    full_screen.pack(side = LEFT)
    full_screen = Label(shortcuts_list_box, text = "c+1", bg = "#ffffff", width=20, font = ('Consolas',12), justify=RIGHT)

    shortcuts_list_box = Text(Mainframe, width=100, height=10, bg = "#ffffff", bd=0, relief = SOLID)
    shortcuts_list_box.pack()
    
    full_screen.pack(side = LEFT)
    full_screen = Label(shortcuts_list_box, text = "Edit Company\t\t\t\t", bg = "#ffffff", width=40, font = ('Consolas',12), justify=LEFT)
    full_screen.pack(side = LEFT)
    full_screen = Label(shortcuts_list_box, text = "c+2", width=20, bg = "#ffffff", font = ('Consolas',12), justify=RIGHT)
    full_screen.pack(side = LEFT)

    close_button = Button(shortcut_window, text = "Close", font=("arial", 15), width = 20, height=2, command = close_shortcut)
    close_button.pack()
    


    shortcut_window.mainloop()

# Menus function
def menus():
    Menus = Menu(dashboard_root)
    Menus.add_command(label='Shortcut', command = shortcut)
    dashboard_root.config(menu=Menus)

# /////////////////////////////////// Dashboard Starts \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
def dashboard():

    # Globalisation of Dashboard Window
    global dashboard_root
    dashboard_root = Tk()
    dashboard_root.geometry("1366x675+0+0")
    dashboard_root.resizable(True, True)
    dashboard_root.title("MedyBest+")
    dashboard_root.configure(bg="#0f0f0f")
    dashboard_root.state("zoomed")
    medybest_logo = 'E:\\Internship_Project\\images\\Logo_image\\MedyBest_Logo.ico'
    dashboard_root.iconbitmap(False, medybest_logo)

    dashboard_root.bind("<Key>", key_pressed)

    menus()

    # Globalisation of variable used in this
    global active_button
    global f1, f2, f3, f4
    global current_time
    global f_sales
    global f_medic
    global f_staff
    global f_compa
    global sales_button
    global medicine_button
    global staff_button
    global company_button
    global current_bg_sales
    global current_bg_medicine
    global current_bg_staff
    global current_bg_company


    plus_image = PhotoImage(file="E:\\Internship_Project\\images\\plus.png")
    
    # Declaration of Frames
    f1 = Frame(dashboard_root, bd=0, relief = SOLID, bg="#0f0f0f", width=1100, height=100)
    f2 = Frame(dashboard_root, bd=0, relief=SOLID, bg="#ffffff", width=200, height=585)
    f3 = Frame(dashboard_root, bd = 0, relief = SOLID, bg = "#e6ffff", width = 1176, height = 585)
    f4 = Frame(f3, bd = 0, relief = SOLID, bg = "#e6ff3e", width = 1174, height = 587)
    f5 = Frame(dashboard_root, bd=0, relief=GROOVE, bg="#0f0f0f", width=224, height=106)

    # Grid of Frames
    f1.grid(row=0, column=0, columnspan=2)
    f2.grid(row=1, column=0)
    f3.grid(row = 1, column = 1, columnspan = 2)
    f4.pack()
    f5.grid(row=0, column=2, ipadx=25, ipady=6)

    # Fixing the properites of frames like width and height
    f1.grid_propagate(0)
    f2.grid_propagate(0)
    f3.grid_propagate(0)
    f4.pack_propagate(0)
    f5.grid_propagate(0)

    # Delcaration Title Label of Frame1
    welcome = Label(f1, text="Welcome to ", font=("bookman old style", 15), bg='#0f0f0f', fg='#ffb108')
    medybest = Label(f1, text=" MedyBest", font=("praetorian 3d", 50), bg='#0f0f0f', fg='#ffe608')
    plus = Label(f1, image=plus_image, width=130, font=("Bookman Old Style", 57), bg='#0f0f0f', fg='#ffffff')

    # Grid of Tity_texttle Label of Frame1
    welcome.grid(row=0, column=0, padx=10)
    medybest.grid(row=0, column=1, pady=5, rowspan=3)
    plus.grid(row=0, column=2, padx=7, rowspan=3)

    # Declaration of Date and Time in Frame5
    current_date = Label(f5, text=date(), width=0, height=0, font=("eras medium itc", 12), bg='#0f0f0f', fg='#deff08')
    current_day = Label(f5, text=day(), width=0, height=0, font=("eras medium itc", 12), bg='#0f0f0f', fg='#deff08')
    current_time = Label(f5, text='TIME', width=0, height=1, font=("eras medium itc", 22, 'bold'), bg='#0f0f0f', fg='#deff08')

    # Grid of Date and Time in Frames5
    current_date.pack(anchor='ne',padx = 23, pady = 7)
    current_day.pack(anchor='e',padx = 23)
    current_time.pack(anchor='se',padx = 23)

    # Logo for Menus buttons
    logo_sales = PhotoImage(file="E:\\Internship_Project\\images\\main_buttons\\sales.png")
    logo_medicine = PhotoImage(file="E:\\Internship_Project\\images\\main_buttons\\medicine.png")
    logo_staff = PhotoImage(file="E:\\Internship_Project\\images\\main_buttons\\staff.png")
    logo_company = PhotoImage(file="E:\\Internship_Project\\images\\main_buttons\\company.png")

    # subframes of Frame2
    f_sales = Frame(f2, bd=0, bg='#ffffff', relief=SOLID)
    f_medic = Frame(f2, bd=0, bg='#ffffff', relief=SOLID)
    f_staff = Frame(f2, bd=0, bg='#ffffff', relief=SOLID)
    f_compa = Frame(f2, bd=0, bg='#ffffff', relief=SOLID)

    f_sales.pack()
    f_medic.pack()
    f_staff.pack()
    f_compa.pack()

    # Buttons of dashboard in Frame2
    sales_button = Button(f_sales, image=logo_sales, cursor="hand2", width=114, bg='#ffffff', bd=0,text="Sales", font=("arial", 12), relief=SOLID, command=lambda b='sales': command_button(b))
    medicine_button = Button(f_medic, image=logo_medicine, cursor="hand2", width=114, bg='#ffffff', bd=0,text="Medicine", font=("arial", 12), relief=SOLID, command=lambda b='medicine': command_button(b))
    staff_button = Button(f_staff, image=logo_staff, cursor="hand2", width=114, bg='#ffffff', bd=0,text="Staff", font=("arial", 12), relief=SOLID, command=lambda b='staff': command_button(b))
    company_button = Button(f_compa, image=logo_company, cursor="hand2", width=114, bg='#ffffff', bd=0,text="Company", font=("arial", 12), relief=SOLID, command=lambda b='company': command_button(b))

    # Grid of Buttons
    sales_button.grid(row=0, column=0, padx=40, ipady=14)
    medicine_button.grid(row=1, column=0, padx=40, ipady=14)
    staff_button.grid(row=2, column=0, padx=40, ipady=14)
    company_button.grid(row=3, column=0, padx=40, ipady=14)

    # Calling the clock function 
    clock()

    # Default active button from 4 of them - Sales
    active_button = 'sales'
    command_button(active_button)

    dashboard_root.mainloop()
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ Dashboard Closes ////////////////////////////////////
#dashboard()
