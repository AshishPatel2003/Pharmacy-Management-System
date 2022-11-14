from tkinter import *
from tkinter import messagebox
import keyboard
from Dashboard import *

# Function - bg_white
def bg_white():
    login_button['bg'] = '#ffffff'
    
#Key Pressed  
def key_pressed(event):
    if keyboard.is_pressed("enter"):
        login_button['bg'] = '#fcff8c'
        login_button.after(250, bg_white)
        verify()

# Hovering the button
def hover_enter(e): 
    login_button['bg'] = '#fcff8c'         # Skin Color 

def hover_leave(e):
    login_button['bg'] = '#ffffff'          # White color

# Calling Dashboard
def Call_Module_Dashboard():
    dashboard()                # Calling the dashboard() from external module

# User Verification
def verify():
    user_ = username_entry.get()
    pass_ = password_entry.get()
    if  pass_ == '' and user_=='':          # If Entries are Empty
        messagebox.showinfo("Warning"," Please Enter Username and Password")
    elif user_=='admin':
        if pass_ == '12345678':         # If username and password both are correct
            login_root.destroy()
            login_root.after(2000, Call_Module_Dashboard())         # Call Dashboard
        else:
            messagebox.showinfo("Warning","Please Enter Correct Password")
            password_entry.delete(0,END)        # If password is incorrect show warning
    else:
        messagebox.showerror("Warning","Wrong Username and Password")
        username_entry.delete(0,END)            #delete entry
        password_entry.delete(0,END)
        username_entry.focus()                  # Focus on username entry

# Temprory Frame Destroy
def destroy_tempframe():
    tempframe.destroy()
    login_root.configure(bg = '#0f0f0f')
    login_root.overrideredirect(False)

# logo_destroy
def logo_destroy():
    logo_image.destroy()
    tempframe.configure(bg = "black")
    tempframe.after(250,destroy_tempframe)

# =========================== Login Window =====================================
def Login_window():
    global login_root
    login_root = Tk()
    login_root.geometry("595x440+400+175")
    login_root.resizable(False, True)
    login_root.title("Medybest - Pharmacy Management System")
    login_root.configure(bg = "black")
    login_root.overrideredirect(True)          # For removing Title bar 
    medybest_logo = "E:\\Internship_Project\\images\\Logo_image\\MedyBest_Logo.ico"
    login_root.iconbitmap(False, medybest_logo)


    # Global Declaration of tempframe and Mainframe
    global tempframe
    global Mainframe
    global logo_image

    # tempframe for logo design display
    tempframe = Frame(login_root, bd = 0, width = 555, height = 500, bg = "#0f0f0f", relief = SOLID )
    tempframe.pack(anchor="nw", fill = Y)                                   # light dark black color
    tempframe.pack_propagate(0)

    #Displaying the Logo Design 
    logo = PhotoImage(file = "E:\\Internship_Project\\images\\Logo_image\\med-2.png")
    logo_image = Label(tempframe, image = logo)
    logo_image.pack(anchor = "nw")
    tempframe.after(1500,logo_destroy)          # Destroy logo design for entry input

    # Mainframe of Login Page
    Mainframe = Frame(login_root, bd = 0, width = 1000, height = 700, bg = "#0f0f0f", relief = SOLID )
    Mainframe.pack(anchor="nw", fill = Y)
    Mainframe.grid_propagate(0)                 # Fixing the properities of Mainframe

    
    # Heading Frames
    f1 = Frame(Mainframe, bd = 5, width = 100, height = 100, bg = "#0f0f0f")
    f1.grid(row = 0, column = 0, rowspan=3, ipadx = 20, pady =5)
    f2 = Frame(Mainframe, bd = 5, width = 200, height = 50, bg = "#0f0f0f")
    f2.grid(row = 0, column = 1, rowspan = 2)

    f1.grid_propagate(0)
    f2.grid_propagate(0)
    
    #Heading Frame widgets
    plus_image = PhotoImage(file = "E:\\Internship_Project\\images\\plus.png")

    

    heading_pms1 = Label(f1, text = "MedyBest",font =("praetorian 3d", 50), fg = '#ffe608', bg = "#0f0f0f" , justify = 'left')
    heading_pms1.pack()
    heading_image = Label(f2, image = plus_image, width = 90, height = 90, bg = "#0f0f0f")
    heading_image.pack()

    # Login Frame
    Login_frame = Frame(Mainframe, bd = 1, width = 465, height = 250, bg = "#fdffb5", relief = SOLID )
    Login_frame.grid(padx = 20, pady = 20, columnspan = 2)
    Login_frame.grid_propagate(0)

    #Login Subframe
    subframe1 = Frame(Login_frame, bd = 5 ,bg = "#fdffb5")
    subframe1.grid(columnspan = 2, padx = 30,  pady = 20)

    # Globalisation of variables
    global usernamevalue
    global passwordvalue
    global username_entry
    global password_entry

    #Variables
    usernamevalue = StringVar()
    passwordvalue = StringVar()

    
    # Login Widgets
    Login_heading = Label(subframe1, text = "Log In", width = 22,
                          bg = "#0f0f0f", fg = "#fdffb5", font = ("arial", 20, 'bold'))
    Login_heading.grid(row = 0, column = 0, columnspan = 2, ipady = 10)


    # Labels
    username = Label(subframe1, text = "Username : ",font =("bookman old style", 15),bg = "#fdffb5")
    username.grid(row = 1, column = 0, pady = 10)

    password = Label(subframe1, text = "Password : ",font =("bookman old style", 15),bg = "#fdffb5")
    password.grid(row = 2, column = 0, pady = 10)


    # Entires
    username_entry = Entry(subframe1, textvariable = usernamevalue,font =("bookman old style", 15),bg = "#ffffff")
    username_entry.grid(row = 1, column = 1, pady = 10)
    
    password_entry = Entry(subframe1, textvariable = passwordvalue, show = "*", text = "Password : ", font =("bookman old style", 15),bg = "#ffffff")
    password_entry.grid(row = 2, column = 1, pady = 10)

    username_entry.focus()
    
    login_root.bind("<Key>",key_pressed)

    global login_button
    
    # Login_button
    login_button = Button(subframe1,cursor = "hand2", relief = SOLID, width=34, text="Login", bg = '#fdffb5', font =("arial", 15), bd = 1, command = verify)
    login_button.grid(row = 3, column = 0, columnspan = 2)



    login_button.bind('<Enter>', hover_enter)
    login_button.bind('<Leave>', hover_leave)
    login_root.mainloop()
    
# =============================== Login Window closes ===========================

#Login_window()