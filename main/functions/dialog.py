from tkinter import *

def messagebox(message, title="PCCP"):
    root = Tk()
    root.title(title)
    root.minsize(300,150)    #初期画面サイズ(widthxheight)
    label = Label(root, text=message)
    label.pack(padx=10, pady=10)
    button = Button(root, text="OK", width=20, bg="lightgray", command=root.quit)
    button.pack(side="bottom",padx=10, pady=10)
    root.mainloop()

def println(message):
    print(message)