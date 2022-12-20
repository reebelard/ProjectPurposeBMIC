import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

import mysql.connector as pymysql
from PIL import Image, ImageTk

from db_handler import *

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
root.bind_all("<Button-1>", lambda event: event.widget.focus_set())
getval = ""
# BMI calculation
def BMI():
    global getval
    h = float(Height.get())
    w = float(Weight.get())

    # Convert HEIGHT into METER
    try:
        m = h / 100
        bmi = round(float(w / m**2), 1)
        label1.config(text=bmi)
    except ZeroDivisionError:
        messagebox.showerror(
            title="BMI Calculator", message="Height/Weight cannot be 0!"
        )

    if bmi <= 18.5:
        label2.config(text="Underweight!")
        label3.config(
            text=mycursor_fetch_any("bmi_vals", "bmi_getter", "name = 'Underweight'")[
                0
            ][0]
        )
        getval = "Underweight"

    elif bmi > 18.5 and bmi <= 25:
        label2.config(text="Normal!")
        label3.config(
            text=mycursor_fetch_any("bmi_vals", "bmi_getter", "name = 'Normal'")[0][0]
        )
        getval = "Normal"

    elif bmi > 25 and bmi <= 30:
        label2.config(text="Overweight!")
        label3.config(
            text=mycursor_fetch_any("bmi_vals", "bmi_getter", "name = 'Overweight'")[0][
                0
            ]
        )
        getval = "Overweight"

    else:
        label2.config(text="Obese!")
        label3.config(
            text=mycursor_fetch_any("bmi_vals", "bmi_getter", "name = 'Obese'")[0][0]
        )
        getval = "Obese"


# ICON
image_icon = ImageTk.PhotoImage(Image.open(ASSETS_PATH / "BMIcalcL.png"))
root.iconphoto(False, image_icon)

# TOP
top = ImageTk.PhotoImage(Image.open(ASSETS_PATH / "BMIcalc.png"))
top_image = tk.Label(root, image=top, background="#f0f1f5")
top_image.place(x=-38, y=-10)

# bottom BOX
tk.Label(root, width=72, height=18, bg="orange").pack(side="bottom")

# TWO BOXES
box = ImageTk.PhotoImage(Image.open(ASSETS_PATH / "box.png"))
tk.Label(root, image=box).place(x=20, y=100)
tk.Label(root, image=box).place(x=240, y=100)

# SCALE
scale = ImageTk.PhotoImage(Image.open(ASSETS_PATH / "scale.png"))
tk.Label(root, image=scale, bg="orange").place(x=-10, y=310)

# ###############SLIDER1#####################
current_value = tk.DoubleVar()


def get_current_value():
    return "{: .2f}".format(current_value.get())


def slider_changed(event):
    Height.set(get_current_value())

    size = int(float(Height.get()))
    img = Image.open(ASSETS_PATH / "Guy.png")
    resized_image = img.resize((50, 10+ size))
    photo2 = ImageTk.PhotoImage(resized_image)
    secondimage.config(image=photo2)
    secondimage.place(x=70, y=540 - size)
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

    # size = int(float(Weight.get()))
    # img = Image.open(ASSETS_PATH / "Guy.png")
    # resized_image = img.resize((50 + size, 550 - int(float(Height.get()))))
    # photo2 = ImageTk.PhotoImage(resized_image)
    # secondimage.config(image=photo2)
    # secondimage.place(x=70, y=int(float(Height.get())))
    # secondimage.image = photo2


def add_data():
    if float(Height.get()) == 0.00 or float(Weight.get()) == 0.00:
        messagebox.showerror(
            title="BMI Calculator",
            message="Weight/Height cannot be 0!",
        )
    else:
        tup = (BMIval.get(), Height.get(), Weight.get(), getval)
        bmi_update(tup)


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
BMIval = tk.StringVar(value="")
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
name_entry = tk.Entry(master=root, width=71, textvariable=BMIval, background="#B1ABD4", foreground="#000000", relief = "groove").place(x=20, y=60)

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
).place(x=320, y=360)

tk.Button(
    root,
    text="Update record",
    width=15,
    height=2,
    font="CalibriBold 10",
    bg="green",
    fg="white",
    command=add_data,
).place(x=320, y=320)

label1 = tk.Label(root, font="arial 60 bold", bg="orange", fg="#fff")
label1.place(x=125, y=305)

label2 = tk.Label(root, font="arial 20 bold", bg="orange", fg="#3b3a3a")
label2.place(x=280, y=430)

label3 = tk.Label(root, font="arial 10", bg="orange")
label3.place(x=200, y=500)

label4 = tk.Label(root, text="HEIGHT(cm)", font="BahnschriftBold 15", bg="white")
label4.place(x=75, y=115)

label5 = tk.Label(root, text="WEIGHT(kg)", font="BahnschriftBold 15", bg="white")
label5.place(x=285, y=115)

root.mainloop()