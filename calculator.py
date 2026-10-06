from tkinter import *
import math
import re

#معالج
operator = ""
degree = True        # الزوايا بالدرجات (DEG) او بالراديان (RAD)
panel = ""           # اللوحة المفتوحة حاليا: "" او "sci" او "eng"


def sin(x):
    return math.sin(math.radians(x)) if degree else math.sin(x)

def cos(x):
    return math.cos(math.radians(x)) if degree else math.cos(x)

def tan(x):
    return math.tan(math.radians(x)) if degree else math.tan(x)

def fact(x):
    return math.factorial(int(x))

# الدوال المسموحة داخل eval فقط
names = {"sin": sin, "cos": cos, "tan": tan, "sqrt": math.sqrt,
         "log": math.log10, "ln": math.log, "fact": fact,
         "pi": math.pi, "e": math.e}


def btnclick(numbers):
    global operator
    operator = operator + str(numbers)
    text_input.set(operator)

def btnclearDisplay():
    global operator
    operator = ""
    text_input.set("")

def btnBack():
    global operator
    operator = operator[:-1]
    text_input.set(operator)

def btnEqualsInput():
    global operator
    try:
        # حذف الاصفار الزائدة من بداية الارقام (05 تصبح 5)
        clean = re.sub(r'(?<![\d.])0+(?=\d)', '', operator)
        result = eval(clean, {"__builtins__": {}}, names)
        if isinstance(result, float):
            result = round(result, 10)
            if result.is_integer():
                result = int(result)
        operator = str(result)
        text_input.set(operator)
    except:
        operator = ""
        text_input.set("Error")

def btnDegree():
    global degree
    degree = not degree
    btn_deg.config(text="DEG" if degree else "RAD")


#__________________________________
#اللوحات الموسعة

def showpanel(name):
    global panel
    sciframe.place_forget()
    engframe.place_forget()
    if panel == name:
        panel = ""
        cal.geometry("290x410")
    elif name == "sci":
        panel = "sci"
        sciframe.place(x=290, y=0, width=280, height=410)
        cal.geometry("570x410")
    else:
        panel = "eng"
        engframe.place(x=290, y=0, width=300, height=410)
        cal.geometry("590x410")


#معادلات مهندسي الاتصالات
# الاسم : (اسماء المدخلات ، المعادلة ، الصيغة)
formulas = {
    "Power ratio -> dB": (["Ratio (P2/P1)"],
        lambda v: 10 * math.log10(v[0]), "dB = 10 log10(P2/P1)"),
    "Voltage ratio -> dB": (["Ratio (V2/V1)"],
        lambda v: 20 * math.log10(v[0]), "dB = 20 log10(V2/V1)"),
    "dB -> Power ratio": (["Gain (dB)"],
        lambda v: 10 ** (v[0] / 10), "ratio = 10^(dB/10)"),
    "dBm -> mW": (["Power (dBm)"],
        lambda v: 10 ** (v[0] / 10), "P(mW) = 10^(dBm/10)"),
    "mW -> dBm": (["Power (mW)"],
        lambda v: 10 * math.log10(v[0]), "dBm = 10 log10(P mW)"),
    "Wavelength (m)": (["Frequency (MHz)"],
        lambda v: 299.792458 / v[0], "lambda = c / f"),
    "Shannon capacity (bps)": (["Bandwidth (Hz)", "SNR (ratio)"],
        lambda v: v[0] * math.log2(1 + v[1]), "C = B log2(1 + SNR)"),
    "Free space path loss (dB)": (["Distance (km)", "Frequency (MHz)"],
        lambda v: 20 * math.log10(v[0]) + 20 * math.log10(v[1]) + 32.44,
        "FSPL = 20log(d) + 20log(f) + 32.44"),
    "Nyquist rate (Hz)": (["Max frequency (Hz)"],
        lambda v: 2 * v[0], "fs = 2 fmax"),
    "PCM bit rate (bps)": (["Samples per second", "Bits per sample"],
        lambda v: v[0] * v[1], "R = fs x n"),
}

def updatefields(*args):
    labels = formulas[choice.get()][0]
    formulatext.set(formulas[choice.get()][2])
    lbl1.config(text=labels[0])
    ent1.delete(0, END)
    ent2.delete(0, END)
    resulttext.set("")
    if len(labels) == 2:
        lbl2.config(text=labels[1])
        lbl2.place(x=15, y=185)
        ent2.place(x=15, y=210, width=270, height=28)
    else:
        lbl2.place_forget()
        ent2.place_forget()

def calcformula():
    labels, func, text = formulas[choice.get()]
    try:
        values = [float(ent1.get())]
        if len(labels) == 2:
            values.append(float(ent2.get()))
        resulttext.set(str(round(func(values), 4)))
    except:
        resulttext.set("Error")

def useresult():
    global operator
    if resulttext.get() not in ("", "Error"):
        operator = resulttext.get()
        text_input.set(operator)


#__________________________________
#المظهر

cal = Tk()
cal.title("calculator")
cal.geometry("290x410")
cal.resizable(False, False)
cal.config(bg="black")
text_input = StringVar()

txtdisplay = Entry(cal, font=('arial', 19, 'bold'), textvariable=text_input, bd=15, insertwidth=4,
                   bg="powder blue", justify='right', state="readonly",
                   readonlybackground="powder blue").place(x=5, y=5, width=280, height=70)


def makebtn(text, command, x, y, parent=cal):
    b = Button(parent, bd=5, fg="black", font=('arial', 15, 'bold'),
               text=text, bg="powder blue", command=command)
    b.place(x=x, y=y, width=62, height=58)
    return b

#=======================================================================================
# الصف الاول
makebtn("C", btnclearDisplay, 5, 90)
makebtn("<==", btnBack, 72, 90)
makebtn("Sci", lambda: showpanel("sci"), 139, 90)
makebtn("Eng", lambda: showpanel("eng"), 206, 90)
#=======================================================================================
makebtn("7", lambda: btnclick(7), 5, 153)
makebtn("8", lambda: btnclick(8), 72, 153)
makebtn("9", lambda: btnclick(9), 139, 153)
makebtn("/", lambda: btnclick("/"), 206, 153)
#=======================================================================================
makebtn("4", lambda: btnclick(4), 5, 216)
makebtn("5", lambda: btnclick(5), 72, 216)
makebtn("6", lambda: btnclick(6), 139, 216)
makebtn("x", lambda: btnclick("*"), 206, 216)
#=======================================================================================
makebtn("1", lambda: btnclick(1), 5, 279)
makebtn("2", lambda: btnclick(2), 72, 279)
makebtn("3", lambda: btnclick(3), 139, 279)
makebtn("-", lambda: btnclick("-"), 206, 279)
#=======================================================================================
makebtn("0", lambda: btnclick(0), 5, 342)
makebtn(".", lambda: btnclick("."), 72, 342)
makebtn("=", btnEqualsInput, 139, 342)
makebtn("+", lambda: btnclick("+"), 206, 342)


#__________________________________
#لوحة الحاسبة العلمية

sciframe = Frame(cal, bg="black")

btn_deg = makebtn("DEG", btnDegree, 5, 90, sciframe)
makebtn("sin", lambda: btnclick("sin("), 72, 90, sciframe)
makebtn("cos", lambda: btnclick("cos("), 139, 90, sciframe)
makebtn("tan", lambda: btnclick("tan("), 206, 90, sciframe)

makebtn("sqrt", lambda: btnclick("sqrt("), 5, 153, sciframe)
makebtn("log", lambda: btnclick("log("), 72, 153, sciframe)
makebtn("ln", lambda: btnclick("ln("), 139, 153, sciframe)
makebtn("pi", lambda: btnclick("pi"), 206, 153, sciframe)

makebtn("x^2", lambda: btnclick("**2"), 5, 216, sciframe)
makebtn("x^y", lambda: btnclick("**"), 72, 216, sciframe)
makebtn("(", lambda: btnclick("("), 139, 216, sciframe)
makebtn(")", lambda: btnclick(")"), 206, 216, sciframe)

makebtn("e", lambda: btnclick("e"), 5, 279, sciframe)
makebtn("n!", lambda: btnclick("fact("), 72, 279, sciframe)
makebtn("1/x", lambda: btnclick("1/("), 139, 279, sciframe)
makebtn("10^x", lambda: btnclick("10**("), 206, 279, sciframe)


#__________________________________
#لوحة معادلات الاتصالات

engframe = Frame(cal, bg="black")

Label(engframe, text="Communication Formulas", font=('arial', 13, 'bold'),
      bg="black", fg="white").place(x=15, y=10)

choice = StringVar(value=list(formulas.keys())[0])
menu = OptionMenu(engframe, choice, *formulas.keys(), command=updatefields)
menu.config(bg="powder blue", width=30)
menu.place(x=15, y=42)

formulatext = StringVar()
Label(engframe, textvariable=formulatext, font=('arial', 10, 'italic'),
      bg="black", fg="powder blue").place(x=15, y=90)

lbl1 = Label(engframe, text="", font=('arial', 10), bg="black", fg="white")
lbl1.place(x=15, y=120)
ent1 = Entry(engframe, font=('arial', 12), bg="powder blue", justify='right')
ent1.place(x=15, y=145, width=270, height=28)

lbl2 = Label(engframe, text="", font=('arial', 10), bg="black", fg="white")
ent2 = Entry(engframe, font=('arial', 12), bg="powder blue", justify='right')

Button(engframe, text="Calculate", bd=5, font=('arial', 12, 'bold'), bg="powder blue",
       command=calcformula).place(x=15, y=255, width=270, height=38)

resulttext = StringVar()
Label(engframe, textvariable=resulttext, font=('arial', 15, 'bold'),
      bg="black", fg="white").place(x=15, y=305)

Button(engframe, text="Use result", bd=5, font=('arial', 12, 'bold'), bg="powder blue",
       command=useresult).place(x=15, y=350, width=270, height=38)

updatefields()

cal.mainloop()
