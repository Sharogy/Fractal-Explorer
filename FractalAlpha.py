from tkinter import *
from tkinter import messagebox
from math import *
from random import randint
import Startpage
from Libraries import C
from Libraries.matrix import Matrix as mx
from Libraries.Hoverclass import createToolTip
from Libraries.convexhull import convexhull
from Libraries.colors import color_gradient
from Libraries.errors import WrongFractalOutline

# Mainwindow of our program
class MainWindow(Tk):
    running = True

    def __init__(self):
        # initialise tkinter
        Tk.__init__(self)

        # initial window setup
        # initial parameters (name, width, height etc.)
        self.title("Creative Alpha Grahics - Fractal Explorer Alpha")
        self.width = 1500
        self.height = 1000
        self.geometry('{}x{}'.format(self.width, self.height))
        self.margin = 3
        self.pressed = False
        self.pressed2 = False
        self.track = ''
        self.zoom_or = ''
        # initial math variables
        self.last_angle = 0
        self.last_c = 0
        self.last_c2 = 0
        self.select = 1
        self.color = []
        self.color2 = []
        self.oldalpha = 0
        self.secret = 0
        # mouse = PhotoImage(file="arrowheart.gif")
        self.configure(cursor="mouse")

    # initial frame setup
        # base frames
        left = Frame(self, borderwidth=2, relief="solid", bg='#7FB7D5')  # color of the left GB
        right = Frame(self, borderwidth=2, relief="solid", bg='skyblue')
        box1 = Frame(right, borderwidth=3, relief="ridge")
        box2 = Frame(right, borderwidth=3, relief="ridge")
        self.box3 = Frame(right, borderwidth=3, relief="ridge")

        left.pack(side="left", expand=True, fill="both", padx=(5, 1))
        right.pack(side="right", fill="both", padx=(1, 5))
        box1.pack(expand=True, fill="both", padx=10, pady=10)
        box2.pack(expand=True, fill="both", padx=10, pady=(0, 0))
        self.box3.pack(expand=True, fill="both", padx=10, pady=10)

        # canvas setup
        self.canvas = Canvas(left, width=1200, height=1000, bg='#D8E2E7')  # Bg of the drawing board
        self.canvas.pack(fill="both", expand=True)
        self.scaler_in = 1.1
        self.scaler_out = 0.9
        self.xsb = Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.ysb = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)
        self.canvas.configure(scrollregion=(0, 0, self.width, self.height))
    # top right box setup
        # boxes for input values in top right box
        minileft = Frame(box1, borderwidth=1, relief="raised")
        miniright = Frame(box1, borderwidth=1, relief="raised")

        # entry box and labels for input values
        variablestext = PhotoImage(file='Artwork/variables.gif')
        self.label2 = Label(box1, image=variablestext, anchor=S)
        self.label3 = Label(minileft, text="Iteration N", font=("Helvetica", 10))
        self.label4 = Label(miniright, text='Initial Constant C', font=("Helvetica", 10))
        self.label5 = Label(minileft, text='Rotation α', font=("Helvetica", 10))
        self.label6 = Label(minileft, text="MS delay", font=("Helvetica", 10))
        self.label7 = Label(minileft, text='P Tree α', font=("Helvetica", 10))
        self.label8 = Label(minileft, text='K neighbors', font=("Helvetica", 10))
        self.maxiter = Entry(minileft, width=10, justify=CENTER)
        self.maxiter.insert(INSERT, "5000")  # enters an initial value
        self.constant = Entry(miniright, width=20, justify=CENTER)
        self.constant.insert(INSERT, "Please enter a value")  # sets initial text
        self.constant.config(fg="red")
        self.angle = Entry(minileft, width=10, justify=CENTER)
        self.angle.insert(INSERT, 'pi/4')  # enters an initial value
        self.msdelay = Entry(minileft, width=10, justify=CENTER)
        self.msdelay.insert(INSERT, '25')  # enters an initial value
        self.pythangle = Entry(minileft, width=10, justify=CENTER)
        self.pythangle.insert(INSERT, '45')
        self.k = Entry(minileft, width=10, justify=CENTER)
        self.k.insert(INSERT, '50')

        # packing input value entries
        self.label2.pack(pady=5)
        self.label3.pack(pady=2)
        self.maxiter.pack(pady=1, padx=10)
        self.label4.pack(pady=2)
        self.constant.pack(pady=5)
        self.label5.pack(pady=2)
        self.angle.pack(pady=1)
        self.label6.pack(pady=2)
        self.msdelay.pack(pady=1)
        self.label7.pack(pady=2)
        self.pythangle.pack(pady=1)
        self.label8.pack(pady=2)
        self.k.pack(pady=(1,0))
    # constant button group setup
        # interesting curlicue constant button group
        buttongroup1 = Frame(miniright, relief="raised")
        buttongroup2 = Frame(miniright, relief="raised")
        buttongroup3 = Frame(miniright, relief="raised")
        buttongroup4 = Frame(miniright, relief="raised")

        # buttons in group 1
        self.bt1g1 = Button(buttongroup1, text='1', borderwidth=2, fg="#09547A", command=lambda: self.set_text("1", 1),font=("Helvetica", 10))
        self.bt2g1 = Button(buttongroup1, text='e', borderwidth=2, fg="#09547A", command=lambda: self.set_text("e", 1),font=("Helvetica", 10))
        self.bt3g1 = Button(buttongroup1, text='π', borderwidth=2, fg="#09547A", command=lambda: self.set_text("pi", 1),font=("Helvetica", 10))
        self.bt4g1 = Button(buttongroup1, text='γ', borderwidth=2, fg="#09547A", command=lambda: self.set_text("C.EM", 1),font=("Helvetica", 10))
        self.bt5g1 = Button(buttongroup1, text='φ', borderwidth=2, fg="#09547A", command=lambda: self.set_text("C.GR", 1),font=("Helvetica", 10))
        self.bt6g1 = Button(buttongroup1, text='K', borderwidth=2, fg="#09547A", command=lambda: self.set_text("C.KH", 1),font=("Helvetica", 10))
        # buttons in group 2
        self.bt1g2 = Button(buttongroup2, text='+', borderwidth=2, fg="#09547A", command=lambda: self.set_text("+", 2),font=("Helvetica", 10))
        self.bt2g2 = Button(buttongroup2, text='-', borderwidth=2, fg="#09547A", command=lambda: self.set_text("-", 2),font=("Helvetica", 10))
        self.bt3g2 = Button(buttongroup2, text='*', borderwidth=2, fg="#09547A", command=lambda: self.set_text("*", 2),font=("Helvetica", 10))
        self.bt4g2 = Button(buttongroup2, text='/', borderwidth=2, fg="#09547A", command=lambda: self.set_text("/", 2),font=("Helvetica", 10))
        self.bt5g2 = Button(buttongroup2, text='Clr', borderwidth=2, fg="#09547A", command=lambda: self.constant.delete(0, 'end'), font=("Helvetica", 10))
        # buttons in group 3
        self.bt1g3 = Button(buttongroup3, text='α', borderwidth=2, fg="#09547A", command=lambda: self.set_text("C.FA", 1), font=("Helvetica", 10))
        self.bt2g3 = Button(buttongroup3, text='δ', borderwidth=2, fg="#09547A", command=lambda: self.set_text("C.FB", 1), font=("Helvetica", 10))
        self.bt3g3 = Button(buttongroup3, text='√2', borderwidth=2, fg="#09547A", command=lambda: self.set_text("sqrt(2)", 1), font=("Helvetica", 10))
        self.bt4g3 = Button(buttongroup3, text='ln(2)', borderwidth=2, fg="#09547A", command=lambda: self.set_text("log(2,e)", 1), font=("Helvetica", 10))
        self.bt5g3 = Button(buttongroup3, text='G', borderwidth=2, fg="#09547A", command=lambda: self.set_text("C.GA", 1), font=("Helvetica", 10))
        # buttons in group 4
        self.bt1g4 = Button(buttongroup4, text='Ω', borderwidth=2, fg="#09547A", command=lambda: self.set_text("C.OM", 1), font=("Helvetica", 10))
        self.bt2g4 = Button(buttongroup4, text='ζ', borderwidth=2, fg="#09547A", command=lambda: self.set_text("C.RZ", 1), font=("Helvetica", 10))
        self.bt3g4 = Button(buttongroup4, text='A', borderwidth=2, fg="#09547A", command=lambda: self.set_text("C.GK", 1), font=("Helvetica", 10))
        self.bt4g4 = Button(buttongroup4, text='λ', borderwidth=2, fg="#09547A", command=lambda: self.set_text("C.CO", 1), font=("Helvetica", 10))
        self.bt5g4 = Button(buttongroup4, text='F', borderwidth=2, fg="#09547A", command=lambda: self.set_text("C.FR", 1), font=("Helvetica", 10))
        self.bt6g4 = Button(buttongroup4, text='g', borderwidth=2, fg="#09547A", command=lambda: self.set_text("C.GC", 1), font=("Helvetica", 10))

        # packing input value boxes
        minileft.pack(side="left", expand=True, fill="both")
        miniright.pack(side="right", expand=True, fill="both")
        buttongroup1.pack(side="top", fill=X)
        buttongroup2.pack(side="top", fill=X)
        buttongroup3.pack(side="top", fill=X)
        buttongroup4.pack(side="top", fill=X)
        # packing buttons in group 1
        self.bt1g1.pack(side="left", pady=(10, 1), padx=(5, 1))
        self.bt2g1.pack(side="left", pady=(10, 1), padx=1)
        self.bt3g1.pack(side="left", pady=(10, 1), padx=1)
        self.bt4g1.pack(side="left", pady=(10, 1), padx=1)
        self.bt5g1.pack(side="left", pady=(10, 1), padx=1)
        self.bt6g1.pack(side="left", pady=(10, 1), padx=1)
        # packing buttons in group 2
        self.bt1g2.pack(side="left", pady=1, padx=(5, 1))
        self.bt2g2.pack(side="left", pady=1, padx=1)
        self.bt3g2.pack(side="left", pady=1, padx=1)
        self.bt4g2.pack(side="left", pady=1, padx=1)
        self.bt5g2.pack(side="left", pady=1, padx=1)
        # packing buttons in group 3
        self.bt1g3.pack(side="left", pady=(1), padx=(5, 1))
        self.bt2g3.pack(side="left", pady=(1), padx=1)
        self.bt3g3.pack(side="left", pady=(1), padx=1)
        self.bt4g3.pack(side="left", pady=(1), padx=1)
        self.bt5g3.pack(side="left", pady=(1), padx=1)
        # packing buttons in group 4
        self.bt1g4.pack(side="left", pady=(1, 10), padx=(5, 1))
        self.bt2g4.pack(side="left", pady=(1, 10), padx=(1))
        self.bt3g4.pack(side="left", pady=(1, 10), padx=(1))
        self.bt4g4.pack(side="left", pady=(1, 10), padx=(1))
        self.bt5g4.pack(side="left", pady=(1, 10), padx=(1))
        self.bt6g4.pack(side="left", pady=(1, 10), padx=(1))
    #erase button
        self.erasebutton = Button(miniright, text="Erase Canvas", fg="#09547A", command = self.erase, font=("Helvetica", 12))
        self.erasebutton.pack(pady= (10,0))

    # rightside middle box setup
        # button group for rightside middle box
        featext = PhotoImage(file='Artwork/fea.gif')
        self.label1 = Label(box2, image=featext)
        minileft2 = Frame(box2, borderwidth=0, relief="raised")
        miniright2 = Frame(box2, borderwidth=0, relief="raised")
        miniright2top = Frame(miniright2, borderwidth=0, relief="solid")
        self.miniright2middle = Frame(miniright2, borderwidth=0, relief="solid")
        miniright2bottom = Frame(miniright2, borderwidth=0, relief="solid")

        # packing buttongroup for rightside middle box
        self.label1.pack(pady=5)
        minileft2.pack(side="left", expand=True, fill="both")
        miniright2.pack(side="left", expand=True, fill="both")
        miniright2top.pack(pady = 5, fill=X)
        self.miniright2middle.pack(pady = 5, fill=X)
        miniright2bottom.pack(pady = (5,0),  fill=X)
        

        # buttons for rightside middle box
        clockimage = PhotoImage(file="artwork/clock.png")
        anticlockimage = PhotoImage(file="artwork/anticlock.png")
        conveximage = PhotoImage(file="artwork/convex.png")
        self.concaveimage = PhotoImage(file="artwork/concave.png")
        pauseimage = PhotoImage(file="artwork/pause.png")
        stopimage = PhotoImage(file="artwork/stop.png")
        
        self.btn1 = Button(minileft2, text="Draw Curlicue", fg="#09547A", command=self.continue_drawing, font=("Helvetica", 12))
        self.btn2 = Button(minileft2, text='Parallel', fg="#09547A", command=self.draw_p, font=("Helvetica", 12))
        self.btn3 = Button(minileft2, text='Generator', fg="#09547A", command=self.Curli_gen, font=("Helvetica", 12))
        self.btn4 = Button(miniright2top, image=clockimage, fg="#09547A", command = lambda: self.rotate_canvas(1), font=("Helvetica", 12))
        self.btn5 = Button(miniright2top, image=anticlockimage, fg="#09547A", command = lambda: self.rotate_canvas(2), font=("Helvetica", 12))
        self.btn6 = Button(self.miniright2middle, image=conveximage, fg="#09547A", command= lambda: self.outline(), font=("Helvetica", 12))
        self.btn8 = Button(miniright2bottom, image=pauseimage, fg="#09547A", command=self.pause, font=("Helvetica", 12))
        self.btn9 = Button(miniright2bottom, image=stopimage, fg="#09547A", command=self.stop, font=("Helvetica", 12))

        # packing main buttons in right middle box
        self.btn1.pack(pady=5)
        self.btn2.pack(pady=5)
        self.btn3.pack(pady=(5,0))
        self.btn4.pack(padx = (25,5), pady=0, side="left")
        self.btn5.pack(padx = (0,5), side="left")
        self.btn6.pack(padx = (25,5), pady=0, side="left")
        self.btn8.pack(padx = (25,5), pady=0, side="left")
        self.btn9.pack(padx = (0,5), side="left")

    # right side bottom box setup
        # buttons for right side bottom box
        extrastext = PhotoImage(file='Artwork/extras.gif')
        self.label10 = Label(self.box3, image=extrastext)
        self.btn11 = Button(self.box3, text="Draw Sierpenski Triangle", fg="#09547A", command=self.draw_Sier, font=("Helvetica", 12))
        self.btn12 = Button(self.box3, text='Draw Pythagoras Tree', fg="#09547A", command=self.draw_Pytha, font=("Helvetica", 12))
        self.btn13 = Button(self.box3, text='Pythagoras Tree generator', fg="#09547A", command=self.Pytha_gen, font=("Helvetica", 12))
        self.btn14 = Button(self.box3, text='Exit to Start', fg="#09547A", command=self.yesno, font=("Helvetica", 12))
        self.minibottom = Frame(self.box3, borderwidth=0, relief="solid")

        # packing buttons for right side box3
        self.label10.pack(pady=5)
        self.btn11.pack(pady=5)
        self.btn12.pack(pady=5)
        self.btn13.pack(pady=5)
        self.btn14.pack(pady=(5,0))
        self.minibottom.pack(side="left", expand=True, fill="both")

        # minicanvas for animation
        self.canvasmini = Canvas(self.minibottom, width=80, height=80)  # Bg of the drawing board
        self.canvasmini.pack(expand=True, fill="both")

        # loading animation
        images = list()
        for i in range(1, 61, 1):
            number = "Artwork\Snowflake" + "\\" + str(i) + ".png"
            images.append(PhotoImage(file=number))
        self.animation = self.canvasmini.create_image((60, 60), image=images[0])
        self.animate(0, images, self.animation)

        images2 = list()
        for i in range(1, 361, 1):
            number = "Artwork\Spiraltriangle" + "\\" + str(i) + ".png"
            images2.append(PhotoImage(file=number))
        self.animation2 = self.canvasmini.create_image((180, 60), image=images2[0])
        self.animate(0, images2, self.animation2)

        #SECRET CAVE
        self.canvasmini.tag_bind(self.animation2, "<ButtonPress-1>", self.unleash)

    # Hidden canvas setup
        # splitscreen
        self.canvas2 = Canvas(left, width=600, height=1000, bg='#D8E2E7')  # Bg of the drawing board
        self.xsb2 = Scrollbar(self, orient="horizontal", command=self.canvas2.xview)
        self.ysb2 = Scrollbar(self, orient="vertical", command=self.canvas2.yview)
        self.canvas2.configure(yscrollcommand=self.ysb2.set, xscrollcommand=self.xsb2.set)

    # canvas label setup
        # canvas drawingboard label
        self.drawboard = PhotoImage(file='Artwork/drawboard.png')
        self.label20 = Label(self.canvas, image=self.drawboard, borderwidth=0)
        self.label20['bg'] = self.label20.master['bg']
        self.label21 = Label(self.canvas2, image=self.drawboard, borderwidth=0, bg='#D8E2E7')
        self.label20.pack(padx=126, pady=10, side="top")
        self.label21.pack(padx=126, pady=10, side="top")

        # canvas constant C label (including multi canvas support)
        self.cc = StringVar()
        self.cc2 = StringVar()
        self.cc.set("C = " + "####")
        self.cc2.set("C = " + "####")
        self.labelcc = Label(self.canvas, textvariable=self.cc, font=("Helvetica", 16), bg='#D8E2E7')
        self.labelcc2 = Label(self.canvas2, textvariable=self.cc2, font=("Helvetica", 16), bg='#D8E2E7')
        self.labelcc.pack(side="top", padx=(950, 0), pady=(850, 0))

        # canvas iteration N label
        self.iter = StringVar()
        self.iter.set("I = " + "####")
        self.labeliter = Label(self.canvas, textvariable=self.iter, font=("Helvetica", 16), bg='#D8E2E7')
        self.labeliter.pack(side="right", padx=(0, 10), pady=(0, 0))

        # canvas temperature label (including multi canvas support)
        self.temp = StringVar()
        self.temp2 = StringVar()
        self.temp.set("T = " + "####")
        self.temp2.set("T = " + "####")
        self.labeltemp = Label(self.canvas, textvariable=self.temp, font=("Helvetica", 16), bg='#D8E2E7')
        self.labeltemp2 = Label(self.canvas2, textvariable=self.temp2, font=("Helvetica", 16), bg='#D8E2E7')
        self.labeltemp.pack(side="right", padx=(0, 10), pady=(0, 0))

        # canvas progress status label
        self.status = StringVar()
        self.status2 = StringVar()
        self.status.set("Ready to draw")
        self.status2.set("Ready to draw")
        self.labelst = Label(self.canvas, textvariable=self.status, font=("Helvetica", 16), bg='#D8E2E7')
        self.labelst2 = Label(self.canvas2, textvariable=self.status2, font=("Helvetica", 16), bg='#D8E2E7')
        self.labelst.pack(pady=(0, 0))
        
        #canvas active status label
        self.active = Label(self.canvas, text="Active", font=("Helvetica", 16), bg='#D8E2E7')
        self.active2 = Label(self.canvas2, text="Active", font=("Helvetica", 16), bg='#D8E2E7')

    # Extra setup
        # Vertices of the Sierpinski triangle at the 1st iteration
        self.x1 = 700
        self.y1 = 200
        self.x2 = 100
        self.y2 = 800
        self.x3 = self.x1 + abs(self.x1 - self.x2)
        self.y3 = self.y2
        self.centroid = [(self.x1 + self.x2 + self.x3) / 3, (self.y1 + self.y2 + self.y3) / 3]
        self.centroid2 = []

    # Hover information
        # hovertext for buttons in buttongroup 1-4 in top right box1
        createToolTip(self.bt1g1, "constant number 1")
        createToolTip(self.bt2g1, "Euler's constant")
        createToolTip(self.bt3g1, "Archimedes' constant")
        createToolTip(self.bt4g1, "Euler–Mascheroni constant")
        createToolTip(self.bt5g1, "Golden ratio")
        createToolTip(self.bt6g1, "Khinchin's constant")

        createToolTip(self.bt1g2, "Addition")
        createToolTip(self.bt2g2, "Subtraction")
        createToolTip(self.bt3g2, "Multiplication")
        createToolTip(self.bt4g2, "Division")
        createToolTip(self.bt5g2, "Clear inputs")

        createToolTip(self.bt1g3, "Feigenbaum constant α")
        createToolTip(self.bt2g3, "Feigenbaum constant δ")
        createToolTip(self.bt3g3, "Squareroot of 2")
        createToolTip(self.bt4g3, "Natural log of 2")
        createToolTip(self.bt5g3, "Gauss's constant")

        createToolTip(self.bt1g4, "Omega constant")
        createToolTip(self.bt2g4, "Apéry's constant")
        createToolTip(self.bt3g4, "Glaisher-Kinkelin cosntant")
        createToolTip(self.bt4g4, "Conway's constant")
        createToolTip(self.bt5g4, "Fransén–Robinson constant")
        createToolTip(self.bt6g4, "Catalan's constant")

        # hovertext for all main functions in right middle box2
        createToolTip(self.btn1, "Draws Curlicue Fractal with Iteration N and Constant C,\non repeated click, if the same Constant C is used,\nit will continue the fractal where the previous one stopped,\notherwise it draws a new one.")
        createToolTip(self.btn2, "Draw multiple Curlicue Fractals\nside by side at the same time.")
        createToolTip(self.btn3, "Continuously generating Curlicue Fractals, starting\nwith constant 0 with a small increment all the way up\nto 2pi with additional time delay in microseconds.")
        createToolTip(self.btn4, "Rotate the Curlicue Fractal clockwise \non the canvas by rotation angle α")
        createToolTip(self.btn5, "Rotate the Curlicue Fractal anticlockwise \non the canvas by rotation angle α")
        createToolTip(self.btn6, "Draw an convex outer boundry for the Fractal.")
        createToolTip(self.btn8, "Pauze the Curlicue Generator.")
        createToolTip(self.btn9, "Stops the Curlicue Generator.")
        # hovertext for all main functions in right bottom box3
        createToolTip(self.btn11, "Draws Sierpenski triangle with Iteration N")
        createToolTip(self.btn12, "Draws modified Pythagoras Tree with Tree angle α")
        createToolTip(self.btn13, "Continuously generating Pythagoras Tree, starting\nwith angle 0 with a small increment of 0.5 degree all the way\nup to 90 with additional time delay in microseconds")
        createToolTip(self.btn14, "Return to startmenu")

        #self.enable()
        self.mainloop()

    # calculate coordinate before autolocate (diagnostic purpose only)
    def recalibrate(self):
        Xcoord = []
        Ycoord = []
        for item in self.canvas.find_all():
            Xcoord.append(self.canvas.coords(item)[0])  # collection of all x coordinates of the fractal
            Ycoord.append(self.canvas.coords(item)[1])  # collection of all y coordinates of the fractal
        for i in range(0, len(Xcoord)):
            if Yscale > Xscale:
                Xcoord[i] = Xcoord[i] * 0.85 / Yscale
                Ycoord[i] = Ycoord[i] * 0.85 / Yscale
            if Xscale > Yscale:
                Xcoord[i] = Xcoord[i] * 0.85 / Xscale
                Ycoord[i] = Ycoord[i] * 0.85 / Xscale
        return Xcoord, Ycoord

#active frame function
    def selection(self, number):
        if number == 1:
            self.active.pack(side="left",padx=(5,0))
            self.active2.pack_forget()
        elif number == 2:
            self.active2.pack(side="left",padx=(5,0))
            self.active.pack_forget()

# MOUSE BUTTON SECTION
    # mouse zooming function
    def zoomer(self, event):
        widget = str(event.widget).split(".!")[-1]
        if widget =="canvas":            
            if event.delta > 0:
                self.canvas.scale("all", event.x, event.y, self.scaler_in, self.scaler_in)
            elif event.delta < 0:
                self.canvas.scale("all", event.x, event.y, self.scaler_out, self.scaler_out)
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        elif widget=="canvas2":
            if event.delta > 0:
                self.canvas2.scale("all", event.x, event.y, self.scaler_in, self.scaler_in)
            elif event.delta < 0:
                self.canvas2.scale("all", event.x, event.y, self.scaler_out, self.scaler_out)
            self.canvas2.configure(scrollregion=self.canvas2.bbox("all"))
            
    # create the anchor point for mouse
    def move_start(self, event):
        widget = str(event.widget).split(".!")[-1]
        if widget == "canvas":
            self.canvas.scan_mark(event.x, event.y)
            self.select = 1
            self.selection(self.select)
            #print(event.x, event.y)
        elif widget == "canvas2":
            self.canvas2.scan_mark(event.x, event.y)
            self.select = 2
            self.selection(self.select)
            #print(event.x, event.y)

    def pressed(self, event):
        widget = str(event.widget).split(".!")[-1]
        if widget == "canvas":
            self.pressed = not self.pressed
            self.canvas.scan_mark(event.x, event.y)
            #print(event.x, event.y)
        else:
            self.pressed2 = not self.pressed2
            self.canvas2.scan_mark(event.x, event.y)
            #print(event.x, event.y)

    # dragging the frame relative to the anchor point
    def move(self, event):
        widget = str(event.widget).split(".!")[-1]
        if widget == "canvas":
            self.canvas.scan_dragto(event.x, event.y, gain=1)
        else:
            self.canvas2.scan_dragto(event.x, event.y, gain=1)

    def move2(self, event):
        widget = str(event.widget).split(".!")[-1]
        if widget == "canvas":
            if self.pressed:
                self.canvas.scan_dragto(event.x, event.y, gain=1)
        else:
            if self.pressed2:
                self.canvas2.scan_dragto(event.x, event.y, gain=1)

    # *Note: Due to a bug with moving the canvas while it is being drawn, every drawing function is set up with self.enable and self.disable to block mouse movements while the fractal is being drawn. this will not be necessary once the bug is fixed.
    # binds mouse buttons to the canvas
    def enable(self,widget="canvas"):
        if widget == "canvas":
            self.status.set("Ready to draw")
            self.canvas.bind("<MouseWheel>", self.zoomer)
            self.canvas.bind("<ButtonPress-1>", self.move_start)
            self.canvas.bind("<B1-Motion>", self.move)
            self.canvas.bind("<ButtonPress-2>", self.pressed)
            self.canvas.bind("<Motion>", self.move2)
        else:
            self.status2.set("Ready to draw")
            self.canvas2.bind("<MouseWheel>", self.zoomer)
            self.canvas2.bind("<ButtonPress-1>", self.move_start)
            self.canvas2.bind("<B1-Motion>", self.move)
            self.canvas2.bind("<ButtonPress-2>", self.pressed)
            self.canvas2.bind("<Motion>", self.move2)

    # unbinds mouse buttons to the canvas
    def disable(self,widget="canvas"):
        if widget == "canvas":
            self.status.set("Drawing In Progress")
            self.canvas.bind("<MouseWheel>", lambda x: x)
            self.canvas.bind("<ButtonPress-1>", lambda x: x)
            self.canvas.bind("<B1-Motion>", lambda x: x)
            self.canvas.bind("<ButtonPress-2>", lambda x: x)
            self.canvas.bind("<Motion>", lambda x: x)
        else:
            self.status2.set("Drawing In Progress")
            self.canvas2.bind("<MouseWheel>", lambda x: x)
            self.canvas2.bind("<ButtonPress-1>", lambda x: x)
            self.canvas2.bind("<B1-Motion>", lambda x: x)
            self.canvas2.bind("<ButtonPress-2>", lambda x: x)
            self.canvas2.bind("<Motion>", lambda x: x)

# INTERFACE FUNCTIONS
    # function to change the constant entry box
    def set_text(self, text, settype):            
        if self.constant.get() == "Please enter a value":
            self.constant.delete(0, 'end')
            self.constant.insert(END, text + ' ')
            self.constant.config(fg='black')
        else:
            if settype ==1:
                self.constant.insert(END, text + ' ')
            else:
                oldtext = self.constant.get()
                index = len(oldtext)
                self.constant.delete(index-1)
                self.constant.insert(END, text)
        return

    # confirm box for return to startpage
    def yesno(self):
        result = messagebox.askquestion("Return to Startpage", "Are You Sure?", icon='warning')
        if result == 'yes':
            self.destroy()
            Startpage.MainPage(2)
        else:
            pass

    # animation function for canvas
    def animate(self, i, im, gif):
        i = (i + 1) % len(im)
        self.canvasmini.itemconfig(gif, image=im[i])
        self.canvasmini.after(10, self.animate, i, im, gif)

    #erasing canvas
    def erase(self):
        self.last_angle = 0
        self.last_c = 0
        self.last_c2 = 0
        self.oldalpha = 0
        self.canvas.delete("all")
        self.canvas2.delete("all")

# CURLICUE SUPPORT FUNCTIONS
    # fractal zooming function
    def capture(self, x, y, x_scale, y_scale, widget):
        widget.scale("all", x, y, x_scale, y_scale)
        widget.configure(scrollregion=widget.bbox("all"))

    # fractal locating function
    def auto_locate(self, widget):
        scale = self.curli_center(widget, widget.winfo_width() / 2)
        xscale, yscale = scale[2:]
        if (xscale > 1) or (yscale > 1):
            if xscale > yscale:
                self.capture(0, 0, (1 / xscale) * 0.85, (1 / xscale) * 0.85, widget)
            else:
                self.capture(0, 0, (1 / yscale) * 0.85, (1 / yscale) * 0.85, widget)
        else:
            self.capture(0, 0, 1, 1, widget)

    # tracks the fractal movement and moves the center of the screen to the current fractal segment that is being drawn
    def shift_to_center(self, x, y, widget):
        spec_mat = mx.special(1, 2)
        vector = mx.array([[widget.winfo_width() / 2 - x, widget.winfo_width() / 2 - y]]).T * spec_mat
        for item in widget.find_all():
            x1, y1, x2, y2 = widget.coords(item)
            old_coords = mx.array([[x1, x2],
                                   [y1, y2]])
            new_coords = old_coords + vector
            widget.coords(item, *new_coords.tolist())

    # function to calculate the fractal center and fractal size relative to the canvas size
    def curli_center(self, widget, width):
        Xcoord = []
        Ycoord = []
        for item in widget.find_all():
            Xcoord.append(widget.coords(item)[0])  # collection of all x coordinates of the fractal
            Ycoord.append(widget.coords(item)[1])  # collection of all y coordinates of the fractal
        Xpos = max(Xcoord)  # maximum of x
        Xneg = min(Xcoord)  # minimum of x
        Ypos = max(Ycoord)  # maximum of y
        Yneg = min(Ycoord)  # minimum of y
        Xmid = (Xpos + Xneg) / 2  # center of x
        Ymid = (Ypos + Yneg) / 2  # center of y
        Xscale = abs((Xpos - Xmid) / width)  # x scale factor
        Yscale = abs((Ypos - Ymid) / 500)  # y scale factor
        return Xmid, Ymid, Xscale, Yscale

    # Rotation function
    def rotate_canvas(self,direction,alpha = float(0)):
        # multi canvas support
        try:
            if self.select == 1:
                canvasobj = self.canvas
            else:
                canvasobj = self.canvas2
            canvasobj.delete('outline')
            #determine fractal center to rotate
            newcenter = self.curli_center(canvasobj, canvasobj.winfo_width() / 2)
            self.centroid = [newcenter[0], newcenter[1]]    
            try:
                alpha = eval(self.angle.get())  # gets the rotation angle from entry box
                if direction == 2:
                    alpha = -alpha
                rotation_matrix = mx.array([[cos(alpha), -sin(alpha)],
                                            [sin(alpha), cos(alpha)]])  # create rotation matrix  # vector for center points
                for item in canvasobj.find_all():
                    try:
                        special_mat = mx.special(1, 2)
                        x1, y1, x2, y2 = canvasobj.coords(item)
                        old_coords = mx.array([[x1, x2],  # current coordinate x,y
                                               [y1, y2]])
                    except ValueError:
                        special_mat = mx.special(1, 4)
                        x1, y1, x2, y2, x3, y3, x4, y4 = canvasobj.coords(item)
                        old_coords = mx.array([[x1, x2, x3, x4],
                                               [y1, y2, y3, y4]])
                    vector = mx.array([[self.centroid[0], self.centroid[1]]]).T * special_mat
                    translated_coords = old_coords - vector #shift to the origin
                    rotated_coords = rotation_matrix * translated_coords  # apply matrix transformation
                    new_coords = rotated_coords + vector  # move the new coordinate back to center
                    new_coords = new_coords.tolist()
                    canvasobj.coords(item, *new_coords)  # draw new canvas
                self.oldalpha = self.oldalpha + alpha #remember the angle the canvas has been rotated
                if alpha == 0:
                    raise ValueError
            except NameError:
                messagebox.showwarning("Warning", "The rotation input is a string.")
            except SyntaxError:
                messagebox.showwarning("Warning", "The rotation input is wrong.")
            except ValueError:
                messagebox.showwarning("Warning", "Empty rotation.")
        except ValueError:
            messagebox.showwarning("Warning", "Nothing to rotate.")

    # draws outline of the fractal
    def outline(self): 
        coordlist = []
        #multi canvas
        if self.select == 1:
            canvasobj = self.canvas
            widget = "canvas"
        else:
            canvasobj = self.canvas2
            widget = "canvas2"
        canvasobj.delete('outline')
        self.disable(widget)
        #convex or concave
        try:
            for item in canvasobj.find_all():
                coordlist.append((canvasobj.coords(item)[0], canvasobj.coords(item)[1]))  # collection of all x coordinates of the fractal
            hull = convexhull(coordlist)
            self.color = color_gradient('#00FF00','#FF0000',int(len(hull)/2+1))
            self.color2 = color_gradient('#FF0000','#00FF00',int(len(hull)/2))
            for i in range(0, len(self.color2)):
                self.color.append(self.color2[i])
            for i in range(0, len(hull)-1):
                canvasobj.create_line(hull[i][0],hull[i][1],hull[i+1][0],hull[i+1][1],tag='outline',width=3,fill=self.color[i])
                self.after(50, canvasobj.update())
            canvasobj.create_line(hull[-1][0],hull[-1][1],hull[0][0],hull[0][1],tag='outline',width=3,fill=self.color[-1])                

            fractalsegment = sqrt(pow(coordlist[0][0] - coordlist[1][0], 2) + pow(coordlist[0][1] - coordlist[1][1], 2))
            curvelength = fractalsegment * len(coordlist)

            hullsegment = []
            for i in range(0, len(hull) - 1):
                hullsegment.append(sqrt(pow(hull[i][0] - hull[i + 1][0], 2) + pow(hull[i][1] - hull[i + 1][1], 2)))
            hullsegment.append(sqrt(pow(hull[0][0] - hull[-1][0], 2) + pow(hull[0][1] - hull[-1][1], 2)))
            hulllength = sum(hullsegment)

            temp = 1 / log((2 * curvelength / (2 * curvelength - hulllength)), e)
            tstr = str('{0: >#06.5f}'.format(temp))
            if self.select == 1:
                self.temp.set("T = " + tstr)
            else:
                self.temp2.set("T = " + tstr)
            self.enable(widget)
        except:
            messagebox.showwarning('Warning', 'Invalid drawing.')

# Experimental function used in continuous drawing

    # calculates the starting point for the next fractal in curlicue group drawing
    @property
    def last_p(self):
        lst = []
        for item in self.canvas.find_all():
            lst.append(self.canvas.coords(item))
        if len(lst) >= 1:
            return lst[-1][2], lst[-1][3]
        else:
            return 600, 500

    # calculates the number of iteration of the fractal
    @property
    def num_obj(self):
        lst = []
        for item in self.canvas.find_all():
            lst.append(item)
        if len(lst) >= 1:
            return len(lst)
        else:
            return 1
            # continuous drawing function

    def continue_drawing(self):
        self.track = 'c'
        self.disable()
        self.canvas.delete("outline")
        self.canvas.delete("outline2")
        self.repack()
        self.canvas.configure(scrollregion=(0, 0, self.width, self.height))
        try:
            iterat = int(self.maxiter.get())
            if iterat < 1:
                raise ValueError
            else:
                try:
                    c = eval(self.constant.get())
                    # if current constant matches last constant, set type to continuous draw.
                    if self.last_c == c:
                        # set starting position as the end position of the previous fractal.
                        x, y = self.last_p[0], self.last_p[1]
                        type_ = 'cont'                        
                    # if not, set type to new drawing.
                    else:
                        self.canvas.delete('all')
                        x, y = 600, 500
                        type_ = 'normal'
                        self.last_angle = 0
                    # returns the number of object, which is equal to the starting iteration for continous draw
                    start = self.num_obj
                    c = eval(self.constant.get())
                    # set current constant display and temperature
                    cstr = str(c)
                    self.cc.set("C = " + cstr)
                    self.temp.set("T = " + "####")
                    # collect info on the first line of the fractal
                    coord = self.canvas.coords("segment")
                    if coord:
                        # calculate the length of the first line segment
                        segment = sqrt(pow(coord[0] - coord[2], 2) + pow(coord[1] - coord[3], 2))
                        # continue drawing curlicue with all the modified parameters.
                        self.Curli_all(iterat, c, start, self.last_angle, type_, segment, x, y)
                    else:
                        # draw new curlicue if first line segment doesnt exist.
                        self.Curli_all(iterat, c, start, self.last_angle, type_, 12, x, y)
                    if type(c) == str:
                        raise NameError
                except ValueError as v:
                    c = 0
                    messagebox.showwarning("Warning", "The Constant C input is wrong.")
                except NameError as n:
                    c = 0
                    messagebox.showwarning("Warning", "The Constant C input is a string.")
                except UnboundLocalError:
                    c = 0
                    messagebox.showwarning("Warning", "Error")
                except SyntaxError as s:
                    c = 0
                    messagebox.showwarning("Warning", "The Constant C input is wrong.")
                except TypeError as t:
                    c = 0
                    messagebox.showwarning("Warning", "The Constant C input is wrong.")
        except ValueError as v:
            c = 0
            messagebox.showwarning("Warning", "The iteration N input is wrong.")
        self.enable()
        # auto locate the fractal
        self.auto_locate(self.canvas)
        # store the current constant for later use.
        self.last_c = c

    # function to draw curlicue recursivesly
    def curli(self, level):
        # get initial constant from entry box, using eval() allows user to enter a variety of input (not sure if it is a good idea)
        try:
            c = eval(self.constant.get())
            cstr = str('{0: >#016.15f}'.format(c))
            self.cc.set("C = " + cstr)
            self.temp.set("T = " + "####")
            # z=(z+2*math.pi*(i+1)*self.c)%(2*math.pi)
            if level == 0:  # angle = 0 if n = 0
                return 0
            elif level == 1:  # angle = 2*pi*c if n = 1, take module of 2 pi for simplicity
                return (2 * pi * c) % (2 * pi)
            else:  # angle for nth iteration
                return self.curli(level - 1) + (2 * pi * level * c) % (2 * pi)
        except ValueError:
            messagebox.showwarning("Warning", "The Constant C input is wrong.")
        except NameError:
            messagebox.showwarning("Warning", "The Constant C input is a string.")
        except UnboundLocalError:
            messagebox.showwarning("Warning", "Error")
        except SyntaxError:
            messagebox.showwarning("Warning", "The Constant C input is wrong.")
        except TypeError:
            messagebox.showwarning("Warning", "The Constant C input is wrong.")

            # curlicue drawing function

    def Curli_all(self, iterat, constantc, start, angle, type_, linelength, x=None, y=None):
        self.track = 'c'
        if type_ == 'cont':
            start += 1
        cstr = str('{0: >#016.15f}'.format(constantc))
        self.cc.set("C = " + cstr)
        self.temp.set("T = " + "####")
        colors = ['black', 'rosybrown', 'red', 'sienna', 'tan', 'gold', 'olivedrab', 'darkgreen', 'lightseagreen','darkcyan', 'deepskyblue', 'navy', 'darkorchid', 'mediumvioletred']  # color options for the fractal
        threshold = iterat // len(colors) + 1  # coloring the curlicue fractal based on number of iterations. Example:
        # chooses whether ot use recursive or iterative function (note, when continueing to draw,
        # even the smallest iteration will require recursive function to recalculate every previous step,
        # therefore exceed recursive depth limit.
        if iterat > 900 or type_ == 'cont':
            rad = angle+self.oldalpha  #adjust the angle for the canvas rotation
        else:
            rad = self.curli(angle)  # angle of the line segment being drawn
        self.oldalpha = 0
        line_length = linelength  # length of the line segment
        coordlist = []
        # starting point x y.
        end_x = x
        end_y = y

        for i in range(start, iterat + start):  # drawing line by line using endpoint of the previous line as the startpoint of the next line
            color = (i - start) // threshold
            istr = str(i)
            self.iter.set("I = " + istr)
            next_x = end_x
            next_y = end_y
            end_x = next_x + line_length * cos(rad)
            end_y = next_y + line_length * sin(rad)
            # tracking function
            situa = (next_x <= 50) or (next_x >= 1150) or (next_y <= 50) or (
            next_y >= 950)  # checks if the current line segment is beyond the canvas boundry
            if situa and (type_ == 'normal' or type_ == 'cont'):
                self.shift_to_center(next_x, next_y,
                                     self.canvas)  # if beyond the boundry is true, shift the screen center to the current line segment
                for item in self.canvas.find_all():
                    coordlist.append(self.canvas.coords(item))
                next_x, next_y = coordlist[-1][-2], coordlist[-1][-1]  # transform canvas coordinate
                end_x = (next_x + line_length * cos(rad))  # calculate new coordinate
                end_y = (next_y + line_length * sin(rad))
            # store the first line segment as a seperate entity to be called upon.
            if i == 1:
                self.canvas.create_line(next_x, next_y, end_x, end_y, fill=colors[color], tag="segment")  # draw line
            else:
                self.canvas.create_line(next_x, next_y, end_x, end_y, fill=colors[color], tag="line")
            # chooses whether ot use recursive or iterative function
            if iterat > 900 or type_ == 'cont':
                rad += (2 * pi * (i) * constantc) % (2 * pi)
            else:
                rad = self.curli(i)  # calculate angle for next line
            # export the current radian angle to a variable for later use.
            self.last_angle = rad
            # disable canvas update for every line drawn, if using the generator.
            if type_ != 'gen':
                self.canvas.update()

# Parallel drawing section
    # split screen setup
    def split(self):
        self.canvas.pack_forget()
        self.labelcc.pack_forget()
        self.labelst.pack_forget()
        self.labeliter.pack_forget()
        self.labeltemp.pack_forget()
        self.active.pack_forget()
        self.active2.pack_forget()
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.configure(width=600)
        self.canvas.configure(scrollregion=(0, 0, 600, self.height))
        self.canvas2.pack(side="right", fill="both", padx=(3, 0), expand=True)
        self.canvas2.configure(scrollregion=(0, 0, 600, self.height))
        self.labelcc.pack(side="top", padx=(250, 0), pady=(850, 0))
        self.labelcc2.pack(side="top", padx=(250, 0), pady=(850, 0))
        self.labeltemp.pack(side="right", padx=(0, 30), pady=(0, 0))
        self.labeltemp2.pack(side="right", padx=(0, 30), pady=(0, 0))
        self.labelst.pack(side="right", padx=(0,90), pady=(0, 0))
        self.labelst2.pack(side="right", padx=(0,90), pady=(0, 0))

    # restore original setup
    def repack(self):
        self.canvas.pack_forget()
        self.canvas2.pack_forget()
        self.canvas.pack(fill="both", expand=True)
        self.labelcc2.pack_forget()
        self.labeltemp.pack_forget()
        self.labeltemp2.pack_forget()
        self.labelst.pack_forget()
        self.labelst2.pack_forget()
        self.labelcc.pack(side="top", padx=(950, 0), pady=(850, 0))
        self.labeliter.pack(side="right", padx=(0, 10), pady=(0, 0))
        self.labeltemp.pack(side="right", padx=(0, 10), pady=(0, 0))
        self.labelst.pack(side="right", padx=(0, 320), pady=(0, 0))

    # calling parallel drawing function
    def draw_p(self):
        self.canvas.delete("all")
        self.canvas2.delete("all")
        # prevents continuous drawing in parallel window
        self.last_c = 0
        try:
            iterat = int(self.maxiter.get())
            if iterat < 1:
                raise ValueError
            try:
                nlst = []
                cs = self.constant.get().rstrip().split(' ')
                for i in cs:
                    nlst.append(eval(i))
                if len(nlst) != 2:
                    raise ValueError
                xs = [300, 300]
                ys = [500, 500]
                self.split()
                self.disable()
                self.disable("canvas2")
                self.parallel_draw(iterat, nlst, xs, ys)
                self.auto_locate(self.canvas)
                self.auto_locate(self.canvas2)
                self.enable()
                self.enable("canvas2")
            except ValueError as v:
                c = 0
                messagebox.showwarning("Warning", "The Constant C input is wrong, enter input in the following format: 'c1 c2'")
            except NameError as n:
                c = 0
                messagebox.showwarning("Warning", "The Constant C input is a string.")
            except UnboundLocalError:
                c = 0
                messagebox.showwarning("Warning", "Error")
            except SyntaxError as s:
                c = 0
                messagebox.showwarning("Warning", "The Constant C input is wrong.")
            except TypeError as t:
                c = 0
                messagebox.showwarning("Warning", "The Constant C input is wrong.")            
        except ValueError as v:
            messagebox.showwarning("Warning", "The iteration N input is wrong.")
        except Exception:
            messagebox.showwarning("Warning", "The iteration number is too high.")

    # parallel drawing function
    def parallel_draw(self, iterat, constantc, xs=None, ys=None):
        colors = ['black', 'rosybrown', 'red', 'sienna', 'tan', 'gold', 'olivedrab', 'darkgreen', 'lightseagreen',
                  'darkcyan', 'deepskyblue', 'navy', 'darkorchid', 'mediumvioletred']
        line_length = 8  # length of the line segment
        c1, c2 = constantc
        cstr = str('{0: >#016.15f}'.format(c1))
        self.cc.set("C = " + cstr)
        cstr2 = str('{0: >#016.15f}'.format(c2))
        self.cc2.set("C = " + cstr2)
        threshold = iterat // len(colors) + 1
        x1, x2 = xs
        y1, y2 = ys
        rad1, rad2, rad3, rad4 = 0, 0, 0, 0
        end_x1 = x1 + line_length * cos(rad1)
        end_y1 = y1 + line_length * sin(rad1)
        end_x2 = x2 + line_length * cos(rad2)
        end_y2 = y2 + line_length * sin(rad2)
        coordlist = []
        coordlist2 = []
        for i in range(1, iterat + 1):
            color = i // threshold
            next_x1 = end_x1
            next_y1 = end_y1
            end_x1 = next_x1 + line_length * cos(rad1)
            end_y1 = next_y1 + line_length * sin(rad1)
            next_x2 = end_x2
            next_y2 = end_y2
            end_x2 = next_x2 + line_length * cos(rad2)
            end_y2 = next_y2 + line_length * sin(rad2)
            # tracking function Canvas left
            situa = (next_x1 <= 50) or (next_x1 >= 550) or (next_y1 <= 50) or (next_y1 >= 950)  # checks if the current line segment is beyond the canvas boundry
            if situa:
                self.shift_to_center(next_x1, next_y1, self.canvas)  # if beyond the boundry is true, shift the screen center to the current line segment
                for item in self.canvas.find_all():
                    coordlist.append(self.canvas.coords(item))
                next_x1, next_y1 = coordlist[-1][-2], coordlist[-1][-1]  # transform canvas coordinate
                end_x1 = (next_x1 + line_length * cos(rad1))  # calculate new coordinate
                end_y1 = (next_y1 + line_length * sin(rad1))
            # tracking function Canvas right
            situa2 = (next_x2 <= 50) or (next_x2 >= 550) or (next_y2 <= 50) or (next_y2 >= 950)  # checks if the current line segment is beyond the canvas boundry
            if situa2:
                self.shift_to_center(next_x2, next_y2, self.canvas2)  # if beyond the boundry is true, shift the screen center to the current line segment
                for item in self.canvas2.find_all():
                    coordlist2.append(self.canvas2.coords(item))
                next_x2, next_y2 = coordlist2[-1][-2], coordlist2[-1][-1]  # transform canvas coordinate
                end_x2 = (next_x2 + line_length * cos(rad2))  # calculate new coordinate
                end_y2 = (next_y2 + line_length * sin(rad2))

            self.canvas.create_line(next_x1, next_y1, end_x1, end_y1, fill=colors[color], tag="1")
            self.canvas2.create_line(next_x2, next_y2, end_x2, end_y2, fill=colors[color], tag="2")

            rad1 += (2 * pi * (i) * c1) % (2 * pi)
            rad2 += (2 * pi * (i) * c2) % (2 * pi)
            self.canvas.update()
            self.canvas2.update()

    # curlicue generator
    def Curli_gen(self):
        self.track = 'c'
        self.canvas.delete('all')
        self.repack()
        self.canvas.configure(scrollregion=(0, 0, self.width, self.height))
        self.disable()
        try:
            delay = eval(self.msdelay.get())
            if type(delay) == float:
                delay = int(round(delay, 0))
            try:
                iterations = int(self.maxiter.get())
                global running
                running = True  # global tag
                start = int(self.last_c2 * 1000)
                for i in range(start, 6283):
                    if running == True:
                        x, y = self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2
                        self.canvas.delete('all')
                        self.last_c2 = (i / 1000) + (1 / randint(1999, 24989))
                        self.after(delay, self.Curli_all(iterations, self.last_c2, 1, 0, 'gen', 7, x, y))
                        self.canvas.update()
                    else:
                        pass
                if iterations < 0:
                    raise ValueError
            except ValueError as v:
                messagebox.showwarning("Warning", "The iteration N input is wrong.")
        except ValueError as v:
            messagebox.showwarning("Warning", "The iteration N input is wrong.")
        except NameError as n:
            messagebox.showwarning("Warning", "The MS delay input is a string.")
        except SyntaxError as s:
            messagebox.showwarning("Warning", "The MS delay input is not a digit.")

    # pauze generator
    def pause(self):
        global running  # changes the global tag
        running = False
        self.enable()

    # stops generator
    def stop(self):
        global running  # changes the global tag
        running = False
        self.last_c2 = 0
        self.enable()

# EXTRA SECTION
    # Function to draw sierpenski triangle
    def draw_Sier(self):
        self.canvas.delete('all')
        self.repack()
        self.canvas.configure(scrollregion=(0, 0, self.width, self.height))
        self.track = 'sier'
        self.cc.set("C = " + "####")
        self.temp.set("T = " + "####")
        try:
            level = eval(self.maxiter.get())
            if type(level) == str:
                raise NameError
            elif type(level) == float:
                level = round(level, 0)
            elif level < 0:
                raise Exception
            elif level > 10:
                raise ValueError
            else:
                self.disable()
                self.color = color_gradient('#0000FF','#FF0000',level)
                self.recursion_Sier(level, self.x1, self.y1, self.x2, self.y2, self.x3, self.y3)
                self.enable()
        except ValueError:
            messagebox.showwarning("Warning", "The iteration N input is too high (0<=N<=10).")
        except Exception:
            messagebox.showwarning("Warning", "The iteration N input is wrong.")
        except NameError:
            messagebox.showwarning("Warning", "The iteration N input is a string.")
        except SyntaxError:
            messagebox.showwarning("Warning", "The iteration N input is a wrong.")

    # recursive definition of sierpenski triangle
    def recursion_Sier(self, level, x1, y1, x2, y2, x3, y3):
        if level <= 1:
            self.canvas.create_line(x1, y1, x2, y2,fill = self.color[level])
            self.canvas.create_line(x2, y2, x3, y3,fill = 'green')
            self.canvas.create_line(x3, y3, x1, y1,fill = self.color[-level])
            self.canvas.update()
        else:
            level -= 1
            middle_x1 = (x1 + x2) / 2
            middle_y1 = (y1 + y2) / 2
            middle_x2 = (x2 + x3) / 2
            middle_y2 = (y2 + y3) / 2
            middle_x3 = (x3 + x1) / 2
            middle_y3 = (y3 + y1) / 2
            self.recursion_Sier(level, x1, y1, middle_x1, middle_y1, middle_x3, middle_y3)
            self.recursion_Sier(level, middle_x1, middle_y1, x2, y2, middle_x2, middle_y2)
            self.recursion_Sier(level, middle_x3, middle_y3, middle_x2, middle_y2, x3, y3)
            
#function to draw pythagoras tree (not perfect)
    def draw_Pytha(self):
        self.canvas.delete('all')
        self.track = 'pytha'
        self.cc.set("C = "+"####")
        self.temp.set("T = "+"####")
        self.repack()
        self.canvas.configure(scrollregion=(0, 0, self.width, self.height))
        coordlist = []
        xcoord =[]
        ycoord =[]
        x1, y1 = 500, 700
        x2, y2 = 700, 700
        x3, y3 = 700, 900
        x4, y4 = 500, 900
        try:
            iterat = int(self.maxiter.get())
            if iterat < 1:
                raise ValueError
            elif iterat > 16:
                raise Exception
            try:
                alpha = float(self.pythangle.get())
                alpha = radians(-alpha)
                self.disable()
                self.color = color_gradient('#69ff51','#5d1a0b',iterat)
                type_ = 'norm'
                self.canvas.configure(scrollregion=(0, 0, self.width, self.height))
                self.recursion_Pythago(x1, y1, x2, y2, x3, y3, x4, y4, iterat, alpha, type_)
                self.enable()
            except ValueError:
                messagebox.showwarning("Warning", "The P Tree alpha input is wrong.")
            except NameError:
                messagebox.showwarning("Warning", "The rotation input is a string.")
        except ValueError as v:
            messagebox.showwarning("Warning", "The iteration N input is wrong.")
        except Exception:
            messagebox.showwarning("Warning", "The iteration number is too high.")
            
#recursive definition of pythagoras tree (not perfect)
    def recursion_Pythago(self, x1, y1, x2, y2, x3, y3, x4, y4, level, alpha, type_):
        spec_mat = mx.special(1, 4)        
        if level > 0:          
            self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4, fill=self.color[level-1])
            if type_ == 'norm':
                self.canvas.update()
            org_mat = mx.array([[x1, x2, x3, x4],  # Original coordinate matrix of the square
                                [y1, y2, y3, y4]])
            rotation_matrix_1 = mx.array([[cos(alpha)**2, -cos(alpha)*sin(alpha)],  #Rotation and scale matrix for the first upper left square
                                          [cos(alpha)*sin(alpha), cos(alpha)**2]])
            rotation_matrix_2 = mx.array([[sin(alpha)**2, cos(alpha)*sin(alpha)],
                                          [-cos(alpha)*sin(alpha), sin(alpha)**2]])
            translated_mat = org_mat
            rotated_mat_1 = rotation_matrix_1 * translated_mat + mx.array([[0, 1]]).T * spec_mat
            rotated_mat_2 = rotation_matrix_2 * translated_mat + mx.array([[cos(alpha) ** 2, 1 + cos(alpha)*sin(alpha)]]).T * spec_mat
            shift_vec_1 = mx.array([[x1 - rotated_mat_1[0][3], y1 - rotated_mat_1[1][3]]]) #shifting vector for the upper left square
            shift_mat_1 = shift_vec_1.T * spec_mat
            shift_vec_2 = mx.array([[x2 - rotated_mat_2[0][2], y2 - rotated_mat_2[1][2]]])
            shift_mat_2 = shift_vec_2.T * spec_mat
            new_coords_1 = (rotated_mat_1 + shift_mat_1).tolist()
            new_coords_2 = (rotated_mat_2 + shift_mat_2).tolist()
            x1_1, y1_1, x2_1, y2_1, x3_1, y3_1, x4_1, y4_1 = new_coords_1
            x1_2, y1_2, x2_2, y2_2, x3_2, y3_2, x4_2, y4_2 = new_coords_2
            self.recursion_Pythago(x1_1, y1_1, x2_1, y2_1, x3_1, y3_1, x4_1, y4_1, level - 1, alpha, type_)
            self.recursion_Pythago(x1_2, y1_2, x2_2, y2_2, x3_2, y3_2, x4_2, y4_2, level - 1, alpha, type_)
                                           
    def Pytha_gen(self):
        self.canvas.delete('all')
        self.repack()
        self.track = 'pytha'
        self.cc.set("C = " + "####")
        self.temp.set("T = " + "####")
        self.canvas.configure(scrollregion=(0, 0, self.width, self.height))
        try:
            iterat = int(self.maxiter.get())
            if iterat < 1:
                raise ValueError
            elif iterat > 10:
                raise Exception
            try:
                delay = eval(self.msdelay.get())
                if type(delay) == float:
                    delay = int(round(delay, 0))
                x1, y1 = 537, 700
                x2, y2 = 662, 700
                x3, y3 = 662, 825
                x4, y4 = 537, 825
                self.disable()
                global running
                running = True
                while running:
                    for i in range(0, 720, 1):
                        if not running:
                            pass
                        else:
                            self.canvas.delete('all')
                            alpha = radians(-(i/2))
                            self.color = color_gradient('#69ff51','#5d1a0b',iterat)
                            type_ = 'gen'
                            self.after(delay, self.recursion_Pythago(x1, y1, x2, y2, x3, y3, x4, y4, iterat, alpha, type_))
                            self.canvas.update()
                self.enable()
            except NameError:
                messagebox.showwarning("Warning", "The MS delay input is a string.")
            except SyntaxError:
                messagebox.showwarning("Warning", "The MS delay input is not a digit.")
        except ValueError as v:
            messagebox.showwarning("Warning", "The iteration N input is wrong.")
        except Exception:
            messagebox.showwarning("Warning", "The iteration number is too high.")

#SECRET CAVE, AKA EXTRA MODULES NEEDED
    def unleash(self,event):
        result = messagebox.askquestion("SECRET LEVEL", "Are You Sure you want to unleash the beast?", icon='warning')
        try:
            from Libraries.concavehull import concavehull
            from Libraries.print3D import P3D
            if result == 'yes':
                if self.secret == 0:
                    self.secret =1
                    self.btn7 = Button(self.miniright2middle, image=self.concaveimage, fg="#09547A", command= self.concave, font=("Helvetica", 12))
                    self.btn7.pack(padx = (0,5), side="left")
                    createToolTip(self.btn7, "Draw an concave outer boundry for the Fractal.\nWARNING: the function is extremely slow \nwith low value of K") 
                    self.btn10 = Button(self.box3, text='3D Vector display', fg="#09547A", command=self.D3D, font=("Helvetica", 12))
                    createToolTip(self.btn10, "Display the fractal on the canvas in a 3d vector field.")
                    self.label10.pack_forget()
                    self.btn11.pack_forget()
                    self.btn12.pack_forget()
                    self.btn13.pack_forget()
                    self.btn14.pack_forget()
                    self.minibottom.pack_forget()
                    self.label10.pack(pady=5)
                    self.btn10.pack(pady=5)
                    self.btn11.pack(pady=5)
                    self.btn12.pack(pady=5)
                    self.btn13.pack(pady=5)
                    self.btn14.pack(pady=(5,0))
                    self.minibottom.pack(side="left", expand=True, fill="both")                     
                elif self.secret ==1:
                    messagebox.showwarning("Warning","Secret Level is already activated.")           
            else:
                pass
        except:
            messagebox.showwarning("Warning", "Your powerlevel is too low")
        
        
    def D3D(self):
        from Libraries.print3D import P3D 
        coordlist = []
        for item in self.canvas.find_all():
            coordlist.append(self.canvas.coords(item))
        with open("Docs\quivercoord.txt", "w") as fp:  # stores x and y coordinate for 3d printing
            for i in coordlist:
                fp.writelines(
                    '{}, {}, {}, {} \n'.format(i[0], i[1], i[2], i[3]))  # formating coordinates for easy reading later
        P3D()

    def concave(self):
        from Libraries.concavehull import concavehull
        coordlist = []
        #multi canvas
        if self.select == 1:
            canvasobj = self.canvas
            widget = "canvas"
        else:
            canvasobj = self.canvas2
            widget = "canvas2"
        canvasobj.delete('outline')
        self.disable(widget)
        try:
            if self.track == 'sier' or self.track == 'pytha':
                raise WrongFractalOutline
            k = int(self.k.get())
            if k < 3:
                raise ValueError
            else:
                for item in canvasobj.find_all():
                    coordlist.append([canvasobj.coords(item)[0], canvasobj.coords(item)[1]])
                hull = concavehull(coordlist, k)
                self.color = color_gradient('#00FF00','#FF0000',int(len(hull)/2+1))
                self.color2 = color_gradient('#FF0000','#00FF00',int(len(hull)/2))
                for i in range(0, len(self.color2)):
                    self.color.append(self.color2[i])
                for i in range(len(hull) - 1):
                    canvasobj.create_line(hull[i][0], hull[i][1], hull[i + 1][0], hull[i + 1][1], width=3, tag='outline',fill=self.color[i])
                    self.after(30, canvasobj.update())
        except ValueError:
            messagebox.showwarning('Warning', 'K must be greater than or equal to 3')
        except:
            messagebox.showwarning('Warning', 'Invalid drawing.')
        self.enable(widget)

# creates the mainwindow
#MainWindow()
