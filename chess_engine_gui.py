from tkinter import *
from tkinter.ttk import Combobox
import ctypes
import chess_engine

user32=ctypes.windll.user32
screensize=user32.GetSystemMetrics(0),user32.GetSystemMetrics(1)

window=Tk()

gui_size=470

window.title('ChessEngine')
window.geometry(str(gui_size)+"x"+str(gui_size)+"+"+str(screensize[0]//2-(gui_size//2))+"+"+str(screensize[1]//2-(gui_size//2)))

websites=["Chess.com","LiChess"]

def store_website():
    global my_website
    my_website=website.get()

def store_highlight():
    global my_highlight
    my_highlight=highlight.get("1.0","end-1c")
    if my_highlight.lower()=="on":my_highlight=True
    else:my_highlight=False

def store_bongcloud():
    global my_bongcloud
    my_bongcloud=bongcloud.get("1.0","end-1c")
    if my_bongcloud.lower()=="on":my_bongcloud=True
    else:my_bongcloud=False

def store_fen():
    global my_fen
    my_fen=fen.get("1.0","end-1c")
    if my_fen.lower()=="default" or my_fen=="":my_fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

def run_engine():
    global my_highlight
    global my_bongcloud
    global my_fen
    try:my_highlight
    except:my_highlight=False
    try:my_bongcloud
    except:my_bongcloud=False
    try:my_fen
    except:my_fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    status_label.config(text="ON")
    window.update()
    chess_engine.run(my_website,my_highlight,my_bongcloud,my_fen)
    status_label.config(text="OFF")

#Website Label
website_label=Label(window,text="Website",fg="black")
website_label.place(x=20,y=60)

#Status Label
status_label=Label(window,text="OFF",fg="red")
status_label.place(x=320,y=150)

#HighLight Label
highlight_label=Label(window,text="Highlight Move",fg="black")
highlight_label.place(x=20,y=130)

#Bongcloud Label
bongcloud_label=Label(window,text="Bongcloud",fg="black")
bongcloud_label.place(x=20,y=180)

#Fen Label
fen_label=Label(window,text="FEN Position",fg="black")
fen_label.place(x=0,y=300)

#Highlight Textbox
highlight=Text(window,height=1,width=15)
highlight.place(x=20,y=150)

#Bongcloud Textbox
bongcloud=Text(window,height=1,width=15)
bongcloud.place(x=20,y=200)

#Fen Textbox
fen=Text(window,height=1,width=60)
fen.place(x=0,y=320)



#Websites
website=Combobox(window,values=websites)
website.place(x=20,y=80)

#Website Confirm Button
website_confirm=Button(window,text="Change",command=store_website)
website_confirm.place(x=180,y=80)

#Highlight Confirm Button
highlight_confirm=Button(window,text="Change",command=store_highlight)
highlight_confirm.place(x=160,y=150)

#Bongcloud Confirm Button
website_confirm=Button(window,text="Change",command=store_bongcloud)
website_confirm.place(x=160,y=200)

#FEN Confirm Button
fen_confirm=Button(window,text="Change",command=store_fen)
fen_confirm.place(x=200,y=350)

#Start Button
start=Button(window,text="Start",command=run_engine)
start.place(x=290,y=40)

window.mainloop()
