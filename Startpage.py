from tkinter import *
from tkinter import messagebox
import FractalAlpha
from math import *
from random import randint

class MainPage(Tk):
        
    running = True

    def __init__(self,number):
        #initialise tkinter
        Tk.__init__(self)
        status = number

        #initial parameters (name, width, height etc.)
        self.title("Creative Alpha Grahics - Fractal Explorer Alpha")  
        self.width= 1500   
        self.height = 1000
        self.geometry('{}x{}'.format(self.width, self.height))
        self.margin = 3
        self.pressed = False
        self.track = ''
        self.zoom_or = ''
        self.configure(cursor="mouse")
        self.mainframe = Frame(self, bg= "white")
        self.mainframe.pack(side= "left", expand=True,fill="both")

        #background canvas        
        self.canvas = Canvas(self.mainframe, width=1440, height=1000, bg='#D8E2E7') #Bg of the drawing board 
        self.canvas.pack(fill="both", expand=True)
        self.scaler_in = 1.1
        self.scaler_out = 0.9
        self.xsb = Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.ysb = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)
        self.canvas.configure(scrollregion=(0, 0, self.width, self.height))

        #background picture
        self.logo = PhotoImage(file="Artwork/bg.png")
        self.canvas.create_image(0,0,anchor="nw",image=self.logo)
        self.welcome= PhotoImage(file = 'Artwork/logo.png')
        self.movingwelcome = self.canvas.create_image(750,1500,image=self.welcome)
        #portrait pictures
        self.portrait1 = PhotoImage(file="artwork/Mila.gif")
        self.portrait2 = PhotoImage(file="artwork/Ke.gif")
        self.portrait3 = PhotoImage(file="artwork/Vanh.gif")
        self.portrait4 = PhotoImage(file="artwork/Sandesh.gif")
        self.rollingportrait1 = self.canvas.create_image(-750,480,image=self.portrait1)
        self.rollingportrait2 = self.canvas.create_image(500,1500,image=self.portrait2)
        self.rollingportrait3 = self.canvas.create_image(1000,1500,image=self.portrait3)
        self.rollingportrait4 = self.canvas.create_image(2250,480,image=self.portrait4)
        #loading animation if starting up for first time
        if status == 1: 
        #hats and carts
            self.hatleft = PhotoImage(file="artwork/hatleft.png")
            self.hatright = PhotoImage(file="artwork/hatright.png")
            self.hatleftreverse = PhotoImage(file="artwork/hatleftreverse.png")
            self.hatrightreverse = PhotoImage(file="artwork/hatrightreverse.png")
            self.boatleft = PhotoImage(file="artwork/boatleft.png")
            self.boatright = PhotoImage(file="artwork/boatright.png")
            self.canvas.coords(self.rollingportrait1,-750,480)
            self.canvas.coords(self.rollingportrait2,500,500)
            self.canvas.coords(self.rollingportrait3,1000,500)
            self.canvas.coords(self.rollingportrait4,2250,480)
            self.rollinghatleft = self.canvas.create_image(475,395,image=self.hatleft) 
            self.rollinghatright = self.canvas.create_image(1020,395,image=self.hatright)
            self.rollingboatleft =self.canvas.create_image(-720,530,image=self.boatleft)
            self.rollingboatright =self.canvas.create_image(2220,530,image=self.boatright)
            loading = self.canvas.create_text(775,565,text="Brewing tea, please wait!",font=("Helvetica",16))           
            direction = 1
            self.images = list()
            for i in range (1,50,1):
                number = "Artwork/Loading" + "//" + str(i) + ".png"
                self.images.append(PhotoImage(file=number))
            self.loadinggif = self.canvas.create_image((600,560), image=self.images[0])
            self.animate(0)
            global running
            running = True
            while running:
                c = self.canvas.coords(self.movingwelcome)
                self.canvas.update()
                check1 = self.canvas.coords(self.rollingportrait1)
                check2 = self.canvas.coords(self.rollingportrait2)
                check3 = self.canvas.coords(self.rollingportrait3)
                check4 = self.canvas.coords(self.rollingportrait4)
                if c[1] >= 250:
                    self.canvas.move(self.movingwelcome,0,-0.75)
                    y1 = -c[1]+730
                    x1 = sin(y1*0.02)*100+500
                    self.canvas.coords(self.rollingportrait2,x1,y1)
                    y2 = -c[1]+730
                    x2 = -sin(y2*0.02)*100+1000
                    self.canvas.coords(self.rollingportrait3,x2,y2)
                    y3 = -c[1]+730
                    x3 = sin(y3*0.02)*100+490
                    self.canvas.coords(self.rollinghatleft,x3,y3-85)
                    y4 = -c[1]+730
                    x4 = -sin(y4*0.02)*100+1005
                    self.canvas.coords(self.rollinghatright,x4,y4-85)
                    d = self.canvas.coords(self.rollingboatleft)
                    self.canvas.move(self.rollingboatleft,0.7*direction,0)
                    self.canvas.move(self.rollingboatright,-0.7*direction,0)
                    d2 = self.canvas.coords(self.rollingportrait1)
                    if d[0] > 200:
                        direction = -1.5
                        self.canvas.itemconfig(self.rollingboatleft, image=self.boatright)
                        self.canvas.itemconfig(self.rollingboatright, image=self.boatleft)
                    if d2[0] <= 220:             
                        self.canvas.move(self.rollingportrait1, 0.7, 0)
                        self.canvas.move(self.rollingportrait4, -0.7, 0)                    
                elif c[1] < 250.5:
                    self.canvas.itemconfig(self.rollinghatleft, image=self.hatleftreverse)
                    self.canvas.itemconfig(self.rollinghatright, image= self.hatrightreverse)
                    self.canvas.move(self.rollinghatleft,0,0.75)
                    self.canvas.move(self.rollinghatright,0,0.75)
                    self.canvas.itemconfig(loading,text="Launching program, get ready!")
                    c2 = self.canvas.coords(self.rollinghatleft)
                    if c2[1] > 1200:
                        running = False
                        self.canvas.delete(loading)
                        self.canvas.delete(self.loadinggif)
                        self.canvas.delete(self.rollingboatleft)
                        self.canvas.delete(self.rollingboatright)
                        self.canvas.delete(self.rollinghatleft)
                        self.canvas.delete(self.rollinghatright)
                if round(c[1],0) == 1000:
                    self.canvas.itemconfig(loading,text="Gathering cookies, hold on!")
                if round(c[1],0) == 750:
                    self.canvas.itemconfig(loading,text="Reading memes, almost done!")
                if round(c[1],0) == 500:
                    self.canvas.itemconfig(loading,text="Adding sugar and milk, last step!")
        #skip animation if returning from main program
        elif status == 2:
            self.canvas.coords(self.movingwelcome,750,250)
            self.canvas.coords(self.rollingportrait1,220,480)
            self.canvas.coords(self.rollingportrait2,485,480)
            self.canvas.coords(self.rollingportrait3,1015,480)
            self.canvas.coords(self.rollingportrait4,1280,480)
                                   
        self.startbutton = PhotoImage(file = 'Artwork/startbutton.png')
        self.button1 = self.canvas.create_image(750,500,image=self.startbutton)
        self.canvas.tag_bind(self.button1, "<ButtonPress-1>", self.openpage)
        
        creditsbutton = PhotoImage(file = 'Artwork/credits.png')
        self.button2= Button(self.canvas, borderwidth=0, command=self.opencredits, image = creditsbutton, highlightthickness = 0, bd = 0)

        self.exitphoto = PhotoImage(file = 'Artwork/exit.png')
        self.button3= Button(self.canvas, borderwidth=0, command=self.yesno, image = self.exitphoto, highlightthickness = 2, bd = 0)

        self.button2.pack(padx = 3,pady = (885,0) ,side="left")
        self.button3.pack(padx= (0,50),pady= (885,0),side="right")
        
        self.mainloop()

    #open main program
    def openpage(self,event):
        self.destroy()
        FractalAlpha.MainWindow() 
    #animation function
    def animate(self,i):
        i = (i + 1) % 49
        self.canvas.itemconfig(self.loadinggif, image=self.images[i])
        self.canvas.after(10, self.animate, i)
        
    #confirm box
    def yesno(self):
        result = messagebox.askquestion("Exit the program", "Are You Sure?", icon='warning')
        if result == 'yes':
            self.destroy()
        else:
            pass
        
    #open credit page
    def opencredits(self):
        #remove button box
        self.canvas.delete(self.button1)
        self.button2.pack_forget()
        self.button3.pack_forget()
        self.canvas.delete(self.rollingportrait1)
        self.canvas.delete(self.rollingportrait2)
        self.canvas.delete(self.rollingportrait3)
        self.canvas.delete(self.rollingportrait4)
        #add exit button
        self.button4 = Button(self.canvas, borderwidth=0, command=self.returntostart,image=self.exitphoto,highlightthickness = 2, bd = 0)
        self.button4.pack(padx=50,pady=37,side="right",anchor=SE)
        #open credit file
        fp = open ("Docs/credits.txt",encoding="ascii")
        statictext=fp.read()
        fp.close()
        #create credit roll
        self.rollingtext = self.canvas.create_text(500,1600,text=statictext,font=("Helvetica",16))
        #create portrait roll
        self.rollingportrait1 = self.canvas.create_image(1250,600,image=self.portrait1)
        self.rollingportrait2 = self.canvas.create_image(1100,750,image=self.portrait2)
        self.rollingportrait3 = self.canvas.create_image(950,600,image=self.portrait3)
        self.rollingportrait4 = self.canvas.create_image(1100,450,image=self.portrait4)
        self.hatleft = PhotoImage(file="artwork/hatleft.png")
        self.hatright = PhotoImage(file="artwork/hatright.png")
        self.boatleft = PhotoImage(file="artwork/boatleft.png")
        self.boatright = PhotoImage(file="artwork/boatright.png")
        self.rollinghatleft1 = self.canvas.create_image(randint(50,1450),-80,image=self.hatleft)
        self.rollinghatleft2 = self.canvas.create_image(randint(50,1450),-80,image=self.hatleft)
        self.rollinghatleft3 = self.canvas.create_image(randint(50,1450),-80,image=self.hatleft)
        self.rollinghatright1 = self.canvas.create_image(randint(50,1450),-80,image=self.hatright)
        self.rollinghatright2 = self.canvas.create_image(randint(50,1450),-80,image=self.hatright)
        self.rollinghatright3 = self.canvas.create_image(randint(50,1450),-80,image=self.hatright)
        self.rollingboatleft1 = self.canvas.create_image(-100,randint(50,950),image=self.boatleft)
        self.rollingboatleft2 = self.canvas.create_image(-100,randint(50,950),image=self.boatleft)
        self.rollingboatleft3 = self.canvas.create_image(-100,randint(50,950),image=self.boatleft)
        self.rollingboatright1 = self.canvas.create_image(1600,randint(50,950),image=self.boatright)
        self.rollingboatright2 = self.canvas.create_image(1600,randint(50,950),image=self.boatright)
        self.rollingboatright3 = self.canvas.create_image(1600,randint(50,950),image=self.boatright)
        #static values for object rotation
        n = 3600
        radius = 150
        dtheta = 2*pi/n
        xc = 1200 - radius
        yc = 600
        ya,yb = 0,0
        theta1 = 0
        speed1,speed2,speed3,speed4,speed5,speed6 = 0,0,0,0,0,0
        #rotating portraits and rolling credits
        global running
        running = True
        while running == True:
            coord = self.canvas.coords(self.rollingtext)
            ycoord = coord[1]
            #auto termination condition    
            if ycoord == -750:             
                self.returntostart()
            #calculating portrait coordinate in rotation
            else:
                theta1 += dtheta*2
                theta2 = theta1+pi/2
                theta3 = theta1+pi
                theta4 = theta1+pi*1.5
                x1 = radius*cos(theta1) + xc
                x2 = radius*cos(theta2) + xc
                x3 = radius*cos(theta3) + xc
                x4 = radius*cos(theta4) + xc
                y1 = radius*sin(theta1) + yc
                y2 = radius*sin(theta2) + yc
                y3 = radius*sin(theta3) + yc
                y4 = radius*sin(theta4) + yc
                ya = ya + 1
                xa = sin(ya/75)
                yb = yb - 1
                xb = sin(yb/75)
                self.canvas.move(self.rollinghatleft1, xa, 1*speed1)
                self.canvas.move(self.rollinghatleft2, xa, 1*speed2)
                self.canvas.move(self.rollinghatleft3, xa, 1*speed3)
                self.canvas.move(self.rollinghatright1, xb, 1*speed4)
                self.canvas.move(self.rollinghatright2, xb, 1*speed5)
                self.canvas.move(self.rollinghatright3, xb, 1*speed6)
                self.canvas.move(self.rollingboatleft1, 1*speed1, 0)
                self.canvas.move(self.rollingboatleft2, 1*speed2, 0)
                self.canvas.move(self.rollingboatleft3, 1*speed3, 0)
                self.canvas.move(self.rollingboatright1, -1*speed4, 0)
                self.canvas.move(self.rollingboatright2, -1*speed5, 0)
                self.canvas.move(self.rollingboatright3, -1*speed6, 0)
                
                if ycoord == 1600:
                    speed1 = 1
                elif ycoord == 1350:
                    speed4 = 1
                elif ycoord == 1100:
                    speed2 = 1
                elif ycoord == 850:
                    speed5 = 1
                elif ycoord == 600:
                    speed3 = 1
                elif ycoord == 350:
                    speed6 = 1
                                   
             #moving canvas objects
                self.canvas.coords(self.rollingportrait1,x1,y1)
                self.canvas.coords(self.rollingportrait2,x2,y2)
                self.canvas.coords(self.rollingportrait3,x3,y3)
                self.canvas.coords(self.rollingportrait4,x4,y4)            
                self.canvas.move(self.rollingtext,0,-0.5)
                self.canvas.update()
    #return to main page
    def returntostart(self):
        global running
        running = False
        self.canvas.delete(self.rollingtext)
        self.canvas.delete(self.rollinghatleft1)
        self.canvas.delete(self.rollinghatleft2)
        self.canvas.delete(self.rollinghatleft3)
        self.canvas.delete(self.rollinghatright1)
        self.canvas.delete(self.rollinghatright2)
        self.canvas.delete(self.rollinghatright3)
        self.canvas.delete(self.rollingboatleft1)
        self.canvas.delete(self.rollingboatleft2)
        self.canvas.delete(self.rollingboatleft3)
        self.canvas.delete(self.rollingboatright1)
        self.canvas.delete(self.rollingboatright2)
        self.canvas.delete(self.rollingboatright3)
        self.button4.pack_forget()
        self.button1 = self.canvas.create_image(750,500,image=self.startbutton)
        self.canvas.tag_bind(self.button1, "<ButtonPress-1>", self.openpage)
        self.button2.pack(padx = 3,pady = (885,0) ,side="left")
        self.button3.pack(padx= (0,50),pady= (885,0),side="right")
        self.canvas.coords(self.rollingportrait1,220,480)
        self.canvas.coords(self.rollingportrait2,485,480)
        self.canvas.coords(self.rollingportrait3,1015,480)
        self.canvas.coords(self.rollingportrait4,1280,480)

#calling itself
#MainPage(2)
