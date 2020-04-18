from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import re,pymysql

def adjustWindow(window):
    w=600
    h=600
    ws=screen.winfo_screenwidth()
    hs=screen.winfo_screenheight()
    x=(ws/2)-(w/2)
    y=(hs/2)-(h/2)
    window.geometry('%dx%d+%d+%d'%(w,h,x,y))
    window.resizable(False,False)
    window.configure(background='white')
    
def login_verify():
    global studentID
    connection = pymysql.connect(host="localhost", user="root", passwd="",database="edumate")
    cursor = connection.cursor()
    select_query = "SELECT * FROM student_details where email = '" + username_verify.get() + "' AND password = '" + password_verify.get() + "';"
    cursor.execute(select_query)
    student_info = cursor.fetchall()
    connection.commit()
    connection.close()
    if student_info:
        messagebox.showinfo("Congratulation", "Login Succesfull")
        studentID = student_info[0][0]
        welcome_page(student_info)
    else:
        messagebox.showerror("Error", "Invalid Username or Password") 

def welcome_page(student_info):
    global screen2
    screen2 = Toplevel(screen)
    screen2.title("Welcome")
    adjustWindow(screen2)
    Label(screen2, text="Welcome " + student_info[0][1], width='40', height="2", font=("Calibri", 22, 'bold'), fg='white', bg='#d9660a').place(x=0, y=0)
    Label(screen2, text="", bg='#174873', width='30', height='32').place(x=0, y=96)
    Message(screen2, text='" Some people dream of accomplishing great things. Others stay awake and make it happen. "\n\n - By Some Night Owl', width='180', font=("Helvetica",10, 'bold', 'italic'), fg='white', bg='#174873', anchor = CENTER).place(x=10, y=110)
    photo = ImageTk.PhotoImage(file="welcome_page.png")
    label = Label(screen2, image=photo, text="")
    label.place(x=10, y=270)
    label.image = photo
    photo1 = ImageTk.PhotoImage(file="background.png")
    label1 = Label(screen2, image=photo1, text="")
    label1.place(x=200, y=96)
    label1.image = photo1
    Button(screen2, text='Enter your grades', width=20, font=("Open Sans", 13, 'bold'),bg='brown', fg='white',command=student_new_record).place(x=270, y=250)
    Button(screen2, text='Check your result', width=20, font=("Open Sans", 13, 'bold'),bg='brown', fg='white',command=student_records).place(x=270, y=350)
    
def student_new_record():
    global screen4
    semester = StringVar()
    entryField = list()
    screen4 = Toplevel(screen)
    screen4.title("New Record")
    adjustWindow(screen4)
    Label(screen4, text="Enter New Record", width='40', height="2", font=("Calibri", 22,'bold'), fg='white', bg='#d9660a').grid(row=0, sticky=W, columnspan=4)
    Label(screen4, text="", bg='#174873', width='90', height='25').place(x=0, y=96)
    Label(screen4, text="", bg='white').grid(row=1,column=0)
    Label(screen4, text="Subject Name", font=("Open Sans", 12, 'bold'), fg='white',bg='#174873').grid(row=2,column=0, pady=(5,10))
    Label(screen4, text="Your Marks", font=("Open Sans", 12, 'bold'), fg='white',bg='#174873').grid(row=2,column=1, pady=(5,10))
    Label(screen4, text="Out of", font=("Open Sans", 12, 'bold'), fg='white',bg='#174873').grid(row=2,column=2, pady=(5,10))
    Label(screen4, text="Credits Points", font=("Open Sans", 12, 'bold'), fg='white',bg='#174873').grid(row=2,column=3, pady=(5,10))
    rowNo = 3
    for i in range(6):
        temp = list()
        for j in range(4):
            e = Entry(screen4, width=14)
            e.grid(row=rowNo,column=j, padx=(3,0), pady=(0,25))
            temp.append(e)
        entryField.append(temp)
        rowNo += 2
    Label(screen4, text="Select Sem:", font=("Open Sans", 12, 'bold'), fg='white',bg='#174873').grid(row=rowNo,column=0, pady=(15,0))
    list1 = ['1','2','3','4','5','6','7','8']
    droplist = OptionMenu(screen4, semester, *list1)
    semester.set('--0--')
    droplist.config(width=5)
    droplist.grid(row=rowNo, column=1, pady=(15,0))
    Button(screen4, text='Submit', width=20, font=("Open Sans", 13, 'bold'), bg='brown',fg='white', command=lambda: enter_new_record(entryField,semester)).grid(row=rowNo,columnspan=2,column=2, pady=(15,0))
    
def enter_new_record(entryField, semester):
    found = 0
    for student in entryField:
        for field in student:
            if(field.get() == ""):
                found = 1
                break
    if found == 0:
        if semester.get() == '--0--':
            messagebox.showerror("Error", "Please select your current semester",parent=screen4)
        else:
            connection = pymysql.connect(host="localhost", user="root",passwd="", database="edumate")
            cursor = connection.cursor()
            for fields in entryField:
                insert_query = "INSERT INTO student_records (subject_name, marks_scored, out_off, credit_point, semester, student_id) VALUES('"+ fields[0].get() + "', "+ str(fields[1].get()) + ", "+ str(fields[2].get()) + ", "+ str(fields[3].get()) + ", "+ str(semester.get()) + ", "+ str(studentID) + ");" 
                cursor.execute(insert_query) 
            connection.commit()
            connection.close()
            messagebox.showinfo("Congratulation", "Entry Succesfull",parent=screen2)
            screen4.destroy()
    else:
        messagebox.showerror("Error", "Please fill all the details", parent=screen4)
            
def student_records():
    global screen3
    semester = StringVar()
    screen3 = Toplevel(screen)
    screen3.title("Student Records")
    adjustWindow(screen3)
    Label(screen3, text="Your Record", width='40', height="2", font=("Calibri", 22, 'bold'),fg='white', bg='#d9660a').grid(row=0, sticky=W, columnspan=4)
    Label(screen3, text="", bg='#174873', width='81', height='27').place(x=15, y=92)
    Label(screen3, text="", bg='white').grid(row=1,column=0)
    Label(screen3, text="Select Sem:", font=("Open Sans", 12, 'bold'), fg='white',bg='#174873').grid(row=2,column=0, pady=(5,0))
    list1 = ['1','2','3','4','5','6','7','8']
    droplist = OptionMenu(screen3, semester, *list1, command=lambda x: fetch_record(semester))
    semester.set('--0--')
    droplist.config(width=5)
    droplist.grid(row=2, column=1, pady=(5,0))
    Label(screen3, text="Subject Name", font=("Open Sans", 12, 'bold'), fg='white',bg='#174873').grid(row=3,column=0, pady=(15,10))
    Label(screen3, text="Your Marks", font=("Open Sans", 12, 'bold'), fg='white',bg='#174873').grid(row=3,column=1, pady=(15,10))
    Label(screen3, text="Out of", font=("Open Sans", 12, 'bold'), fg='white',bg='#174873').grid(row=3,column=2, pady=(15,10))
    Label(screen3, text="Credits Points", font=("Open Sans", 12, 'bold'), fg='white',bg='#174873').grid(row=3,column=3, pady=(15,10))

def fetch_record(semester):
    if semester == '--0--':
        messagebox.showerror("Error", "Please select proper semester", parent=screen4)
    else:
        connection = pymysql.connect(host="localhost", user="root", passwd="", database="edumate")
        cursor = connection.cursor()
        select_query = "SELECT subject_name, marks_scored, out_off, credit_point FROM student_records where semester = " + str(semester.get()) + " AND student_id = " + str(studentID) + ";"    
        cursor.execute(select_query)
        student_record = cursor.fetchall()
        connection.commit()
        connection.close()
        if len(student_record) > 0:
            for i in range(len(student_record)):
                for j in range(4):
                    Label(screen3, text=student_record[i][j], font=("Open Sans", 11, 'bold'), fg='white', bg='#174873').grid(row=i+4,column=j, pady=(5,10))
            output = list()
            for record in student_record:
                temp = list()
                per = (record[1]/record[2]) * 100
                if per >= 80:
                    temp.append(10)
                    temp.append(record[3])
                    output.append(temp)
                elif per >= 75 and per < 80:
                    temp.append(9)
                    temp.append(record[3])
                    output.append(temp)
                elif per >= 70 and per < 75:
                    temp.append(8)
                    temp.append(record[3])
                    output.append(temp)
                elif per >= 60 and per < 70:
                    temp.append(7)
                    temp.append(record[3])
                    output.append(temp)
                elif per >= 50 and per < 60:
                    temp.append(6)
                    temp.append(record[3])
                    output.append(temp)
                elif per >= 45 and per < 50:
                    temp.append(5)
                    temp.append(record[3])
                    output.append(temp)
                elif per >= 40 and per < 45:
                    temp.append(4)
                    temp.append(record[3])
                    output.append(temp)
                else:
                    temp.append(0)
                    temp.append(record[3])
                    output.append(temp)
            credits_earned = total_credit_points = 0
            for result in output:
                credits_earned += result[0] * result[1]
                total_credit_points += result[1]
            cgpa = credits_earned/total_credit_points
            percentage = 7.1 * cgpa + 11
            Label(screen3, text="Your CGPI", font=("Open Sans", 12, 'bold'), fg='white', bg='#174873').grid(row=10,column=0, pady=(15,10))
            Label(screen3, text=cgpa, font=("Open Sans", 12, 'bold'), fg='white', bg='#174873').grid(row=10,column=1, pady=(15,10))
            Label(screen3, text="Percentage", font=("Open Sans", 12, 'bold'), fg='white', bg='#174873').grid(row=10,column=2, pady=(15,10))
            Label(screen3, text=percentage, font=("Open Sans", 12, 'bold'), fg='white', bg='#174873').grid(row=10,column=3, pady=(15,10))
        else:
            messagebox.showerror("Error", "Entry not found", parent=screen3)      
                    
def register():
    global screen1, fullname, email, password, repassword, university, gender, tnc
    fullname = StringVar()
    email = StringVar()
    password = StringVar()
    repassword = StringVar()
    university = StringVar()
    gender = IntVar()
    tnc = IntVar()
    screen1 = Toplevel(screen)
    screen1.title("Registeration")
    adjustWindow(screen1)
    Label(screen1, text="Registration Form", width='40', height="2", font=("Calibri", 22,'bold'), fg='white', bg='#d9660a').place(x=0, y=0)
    Label(screen1, text="", bg='#174873', width='72', height='29').place(x=45, y=120)
    Label(screen1, text="Full Name:", font=("Open Sans", 11, 'bold'), fg='white',bg='#174873', anchor=W).place(x=150, y=160)
    Entry(screen1, textvar=fullname).place(x=300, y=160)
    Label(screen1, text="Email ID:", font=("Open Sans", 11, 'bold'), fg='white',bg='#174873', anchor=W).place(x=150, y=210)
    Entry(screen1, textvar=email).place(x=300, y=210)
    Label(screen1, text="Gender:", font=("Open Sans", 11, 'bold'), fg='white', bg='#174873',anchor=W).place(x=150, y=260)
    Radiobutton(screen1, text="Male", variable=gender, value=1,bg='#174873').place(x=300, y=260)
    Radiobutton(screen1, text="Female", variable=gender, value=2,bg='#174873').place(x=370, y=260)
    Label(screen1, text="University:", font=("Open Sans", 11, 'bold'), fg='white',bg='#174873', anchor=W).place(x=150, y=310)
    list1 = ['Mumbai University', 'Savitribai Phule Pune Univeristy','Gujarat Technological University', 'JNTU Kakinada', 'University of Delhi', 'Anna University']
    droplist = OptionMenu(screen1, university, *list1)
    droplist.config(width=17)
    university.set('--select your university--')
    droplist.place(x=300, y=305)
    Label(screen1, text="Password:", font=("Open Sans", 11, 'bold'), fg='white',bg='#174873', anchor=W).place(x=150, y=360)
    Entry(screen1, textvar=password, show="*").place(x=300, y=360)
    Label(screen1, text="Re-Password:", font=("Open Sans", 11, 'bold'), fg='white',bg='#174873', anchor=W).place(x=150, y=410)
    entry_4 = Entry(screen1, textvar=repassword, show="*")
    entry_4.place(x=300, y=410)
    Checkbutton(screen1, text="I accept all terms and conditions", variable=tnc,bg='#174873', font=("Open Sans", 9, 'bold'), fg='brown').place(x=190, y=450)
    Button(screen1, text='Submit', width=20, font=("Open Sans", 13, 'bold'), bg='brown',fg='white', command=register_user).place(x=195, y=490)

def register_user():
    if fullname.get() and email.get() and password.get() and repassword.get() and gender.get():
        if university.get() == "--select your university--": 
            Label(screen1, text="Please select your university", fg="red", font=("calibri", 11), width='30', anchor=W, bg='white').place(x=0, y=570)
            return
        else:
            if tnc.get():
                if re.match("^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email.get()):
                    if password.get() == repassword.get():
                        gender_value = 'male'
                        if gender.get() == 2:
                            gender_value = 'female'
                        connection = pymysql.connect(host="localhost", user="root", passwd="", database="edumate")
                        cursor = connection.cursor()
                        insert_query = "INSERT INTO student_details (fullname, email, password,gender, university) VALUES('"+ fullname.get() + "', '"+ email.get() + "', '"+ password.get() + "', '"+ gender_value + "', '"+ university.get() + "' );"
                        cursor.execute(insert_query)
                        connection.commit()
                        connection.close()
                        Label(screen1, text="Registration Sucess", fg="green", font=("calibri", 11), width='30', anchor=W, bg='white').place(x=0, y=570)
                        Button(screen1, text='Proceed to Login ->', width=20, font=("Open Sans", 9,'bold'), bg='brown', fg='white',command=screen1.destroy).place(x=170, y=565)
                    else:
                        Label(screen1, text="Password does not match", fg="red", font=("calibri", 11), width='30', anchor=W, bg='white').place(x=0, y=570)
                        return
                else:
                    Label(screen1, text="Please enter a valid email ID", fg="red", font=("calibri", 11), width='30', anchor=W, bg='white').place(x=0, y=570)
                    return
            else:
                Label(screen1, text="Please accept the agreement", fg="red",font=("calibri", 11), width='30', anchor=W, bg='white').place(x=0, y=570)
                return
    else:
        Label(screen1, text="Please fill all the details", fg="red",font=("calibri", 11), width='30', anchor=W, bg='white').place(x=0, y=570)
        return

                            
def main_screen():
    global screen,username_verify,password_verify
    screen = Tk()
    username_verify= StringVar()
    password_verify= StringVar()
    screen.title("EDUMATE")
    adjustWindow(screen)
    Label(screen,text="Edumate-Student Manager",width='40',height='2',font=("Calibri",22,'bold'),fg='white',bg='#d9660a').pack()
    Label(text="",bg='white').pack()
    Label(screen,text="",bg='#174873',width='65',height='19').place(x=65,y=95)
    Label(screen,text="Please enter details below to login",bg='#174873',fg='white').pack()
    Label(screen,text="",bg='#174873').pack()
    Label(screen,text="Username",font=("Open Sans",10,'bold'),bg='#174873',fg='white').pack()
    Entry(screen,textvar=username_verify).pack()
    Label(screen,text="",bg='#174873').pack()
    Label(screen,text="Password * ",font=("Open Sans",10,'bold'),bg='#174873',fg='white').pack()
    Entry(screen,textvar=password_verify,show="*").pack()
    Label(screen,text="",bg='#174873').pack()
    Button(screen,text="LOGIN",bg='#e79700',width=15,height=1,font=("Open Sans",13,'bold'),fg='white',command=login_verify).pack()
    Label(screen,text="",bg='#174873').pack()
    Button(screen,text="New User? Register Here",height='2',width='30',bg='#e79700',font=("Open Sans",10,'bold'),fg='white',command=register).pack()
    screen.mainloop()

main_screen()         