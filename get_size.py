from appJar import gui
from tkinter import PhotoImage
app=gui("Grid Size")
app.setSize("250x150")
app.setResizable(canResize=False)
icon ="icon.ico"
app.setIcon(icon)
app.setFont(12)
app.addMessage("choice","Choose the size of the grid")
app.setMessageWidth("choice", 200)
SIZE=0
def size_3(btn):
    global SIZE
    SIZE=3
    app.stop(event=True)       

def size_15(btn):
    global SIZE
    SIZE=15
    app.stop(event=True)

def get_grid_size():
    global SIZE
    return SIZE

app.addButton("3x3", size_3)
app.addButton("15x15", size_15)
app.go()

    



