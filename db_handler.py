import mysql.connector
import tkinter.messagebox

# password = open("password.txt").readline()
mydb = mysql.connector.connect(
    host="localhost", user="root", password="veds", database="bmi"
)

mycursor = mydb.cursor()


def mycursor_fetch_any(field, name, cond):
    mycursor.execute(f"select {field} from {name} where {cond}")
    return mycursor.fetchall()


def bmi_update(tup: tuple):
    mycursor.execute(f"insert into bmi values(%s, %s, %s, %s)", tup)
    mydb.commit()
    tkinter.messagebox.showinfo(
        title="BMI Calculator",
        message="Data inserted successfully.",
    )
