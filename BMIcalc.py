import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from pathlib import Path
import mysql.connector as pymysql

ASSETS_PATH = Path(__file__).resolve().parent / "assets"

messagebox.showinfo(
    title="Welcome, User!",
    message="Welcome!\nBody Mass Index (BMI) is widely "
    + "used as an indicator of body fat content.\n",
)
messagebox.showinfo(
    title="Welcome, User!",
    message="If you want to calculate your BMI, you have to find out your "
    + "weight and height first. Once you know these values, "
    + "click OK and proceed",
)

root = tk.Tk()
root.title("BMI Calculator")
root.geometry("470x580+300+200")
root.resizable(False, False)
root.configure(bg="white")
root.focus_force()


# BMI calculation
def BMI():
    h = float(Height.get())
    w = float(Weight.get())

    # Convert HEIGHT into METER
    m = h / 100
    bmi = round(float(w / m**2), 1)
    label1.config(text=bmi)

    if bmi <= 18.5:
        label2.config(text="Underweight!")
        label3.config(text="You weigh lesser than an normal person!")

    elif bmi > 18.5 and bmi <= 25:
        label2.config(text="Normal!")
        label3.config(text="It indicates that you are Healthy!")

    elif bmi > 25 and bmi <= 30:
        label2.config(text="Overweight!")
        label3.config(
            text="It indicates that you are slightly \n Overweight! \n A"
            + "doctor may advise you to lose some \n weight to be Healthy and "
            + "risk-free from \n further Health complications."
        )

    else:
        label2.config(text="Obese!")
        label3.config(
            text="Your health may be at risk,\n if you do not " +
            "lose weight!"
        )



# ICON
image_icon = ImageTk.PhotoImage(Image.open(r"E:\Vedanthh\ICONS\BMIcalcL.png"))
root.iconphoto(False, image_icon)

# TOP
top = ImageTk.PhotoImage(Image.open(r"E:\Vedanthh\ICONS\BMIcalc.png"))
top_image = tk.Label(root, image=top, background="#f0f1f5")
top_image.place(x=-38, y=-10)

# bottom BOX
tk.Label(root, width=72, height=18, bg="orange").pack(side="bottom")

# TWO BOXES
box = ImageTk.PhotoImage(Image.open(r"E:\Vedanthh\ICONS\box.png"))
tk.Label(root, image=box).place(x=20, y=100)
tk.Label(root, image=box).place(x=240, y=100)

# SCALE
scale = ImageTk.PhotoImage(Image.open(r"E:\Vedanthh\ICONS\scale.png"))
tk.Label(root, image=scale, bg="orange").place(x=-10, y=310)

# ###############SLIDER1#####################
current_value = tk.DoubleVar()


def get_current_value():
    return "{: .2f}".format(current_value.get())


def slider_changed(event):
    Height.set(get_current_value())

    size = int(float(get_current_value()))
    img = Image.open(r"E:\Vedanthh\ICONS\Guy.png")
    resized_image = img.resize((50, 10 + size))
    photo2 = ImageTk.PhotoImage(resized_image)
    secondimage.config(image=photo2)
    secondimage.place(x=70, y=550 - size)
    secondimage.image = photo2


# COMMAND TO CHANGE BACKGROUND COLOR OF SCALE
style = ttk.Style()
style.configure("TScale", background="white")

slider = ttk.Scale(
    root,
    from_=0,
    to=220,
    orient="horizontal",
    style="TScale",
    command=slider_changed,
    variable=current_value,
)
slider.place(x=80, y=250)
#############################################

# @@@@@@@@@@@@@@@@@SLIDER2@@@@@@@@@@@@@@@@@@@@@
current_value2 = tk.DoubleVar()


def get_current_value2():
    return "{: .2f}".format(current_value2.get())


def slider_changed2(event):
    Weight.set(get_current_value2())


# COMMAND TO CHANGE BACKGROUND COLOR OF SCALE
style2 = ttk.Style()
style2.configure("TScale", background="white")

slider2 = ttk.Scale(
    root,
    from_=0,
    to=200,
    orient="horizontal",
    style="TScale",
    command=slider_changed2,
    variable=current_value2,
)
slider2.place(x=300, y=250)
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# ENTRY BOX
Height = tk.StringVar()
Weight = tk.StringVar()
height = tk.Entry(
    root,
    textvariable=Height,
    width=5,
    font="arial 50",
    bg="#fff",
    fg="#000",
    bd=0,
    justify="center",
)  # 'justify' TO align text in center
height.place(x=35, y=160)
Height.set(get_current_value())

weight = tk.Entry(
    root,
    textvariable=Weight,
    width=5,
    font="arial 50",
    bg="#fff",
    fg="#000",
    bd=0,
    justify="center",
)  # 'justify' TO align text in center
weight.place(x=255, y=160)
Weight.set(get_current_value2())

# MAN IMAGE
secondimage = tk.Label(root, bg="orange")
secondimage.place(x=70, y=530)

# CALLING BMI FUNCTION [Line 30] button for bmi calculation
tk.Button(
    root,
    text="View Report",
    width=15,
    height=2,
    font="CalibriBold 10",
    bg="green",
    fg="white",
    command=BMI,
).place(x=320, y=340)

#@@@@@@@@@@@@@@@@@@@@@@@@ ADD DATA @@@@@@@@@@@@@@@@@@@@@@@@@@@

def add_data():
    if height.get() == "" or weight == "":
        messagebox.showerror("Mysql Connection" "Enter the correct details.")
    else:
        sqlCon = pymysql.connect(host = 'localhost',user = 'root',password = 'root', database = 'bmicalc')
        cur = sqlCon.cursor()
        cur.execute("insert into bmicalc values(%s, %s)",(
            height.get(),
            weight.get(),
        ))
        sqlCon.commit()
        sqlCon.close()
        messagebox.showinfo("Mysql Connection" "Data inserted successfully.")

tk.Button(
    root,
    text="Update record",
    width=15,
    height=2,
    font="CalibriBold 10",
    bg="green",
    fg="white",
    command=add_data,
).place(x=320, y=300)



label1 = tk.Label(root, font="arial 60 bold", bg="orange", fg="#fff")
label1.place(x=125, y=305)

label2 = tk.Label(root, font="arial 20 bold", bg="orange", fg="#3b3a3a")
label2.place(x=280, y=430)

label3 = tk.Label(root, font="arial 10", bg="orange")
label3.place(x=200, y=500)

label4 = tk.Label(root, text="HEIGHT(cm)", font="BahnschriftBold 15",
                  bg="white")
label4.place(x=75, y=115)

label5 = tk.Label(root, text="WEIGHT(kg)", font="BahnschriftBold 15",
                  bg="white")
label5.place(x=285, y=115)

root.mainloop()




           