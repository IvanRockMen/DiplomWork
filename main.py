from PIL import Image, ImageMode, ImageTk
from math import exp, pow, sqrt
import sys, os
from tkinter import Menu, Tk, Label, Canvas, YES, BOTH, NW, Entry, DoubleVar, Button, messagebox, Frame
from tkinter.ttk import Progressbar
from tkinter.filedialog import askopenfilename, asksaveasfilename

class Program:
    
    def __init__(self):
        self.window = None

        self.k = 20.0
        self.deltaT = 0.2
        self.t = 10.0

        self.k_val = None
        self.deltaT_val = None
        self.t_val = None
        self.img_label = None
        self.progress = None
        self.img = None
        self.pixels = None
        self.interImage = None

    def initGUI(self):
        self.window = Tk()
        self.window.title("Diffusion image filter")
        self.window.geometry("500x700")
        menu = Menu(self.window)
        new_item = Menu(menu)
        new_item.add_command(label = "Открыть изображение", command=self.open_image)
        new_item.add_separator()
        new_item.add_command(label = "Сохранить изображение", command=self.save_image)
        menu.add_cascade(label = "Файл", menu = new_item)
        about_item = Menu(menu)
        about_item.add_command(label = "О программе", command=self.about_program)
        menu.add_cascade(label="Помощь", menu=about_item)

        img_frame = Frame(self.window)
        img_frame.pack()
        self.img_label = Label(img_frame, image = self.interImage)
        self.img_label.pack(pady = 15)
        k_frame = Frame(self.window)
        k_frame.pack()
        k_label = Label(k_frame)
        k_label.config(text="k = ")
        k_label.pack(side="left")
        self.k_val = DoubleVar(self.window)
        k_text = Entry(k_frame, textvariable = self.k_val)
        k_text.pack()

        deltaT_frame = Frame(self.window)
        deltaT_frame.pack(pady = 15)
        deltaT_label = Label(deltaT_frame)
        deltaT_label.config(text="deltaT = ")
        deltaT_label.pack(side="left")
        self.deltaT_val = DoubleVar(self.window)
        deltaT_text = Entry(deltaT_frame, textvariable = self.deltaT_val)
        deltaT_text.pack()

        t_frame = Frame(self.window)
        t_frame.pack(pady = 10)
        t_label = Label(t_frame)
        t_label.config(text="t = ")
        t_label.pack(side="left")
        self.t_val = DoubleVar(self.window)
        t_text = Entry(t_frame, textvariable = self.t_val)
        t_text.pack()

        start_frame = Frame(self.window)
        start_frame.pack(pady = 15)

        self.progress = Progressbar(start_frame)
        self.progress.pack(side="left")
        
        start_button = Button(start_frame, text = "Запустить фильтрацию", command=self.start_filter)
        start_button.pack(padx = 25)
        
        self.window.config(menu=menu)
        self.window.mainloop()

    def g(self, x):
        return exp(-pow(x, 2)/(self.k*self.k))

    def about_program(self):
        messagebox.showinfo(title="О программе", message="Программа по диффузионной фильтрации шумов на изображении")

    def open_image(self):
        input_link = askopenfilename(initialdir=os.getcwd(), title="please choose image:", filetypes=(("png files", ".png"), ("jpeg files", "jpg"),("bitmap files", ".bmp") ))
        self.img = Image.open(input_link)
        self.img = self.img.convert("L")
        self.pixels = self.img.load()
        self.interImage = ImageTk.PhotoImage(image=self.img, size=(210, 120))
        self.img_label.config(image = self.interImage)
        self.window.update()
        del input_link
    

    def save_image(self):
        image = Image.new(mode="L", size=(self.img.width, self.img.height))
        for i in range(self.img.width):
            for j in range(self.img.height):
                image.putpixel(xy=(i,j), value=self.pixels[i,j])

        output_link = asksaveasfilename(initialdir=os.getcwd(), title="please choose image:", filetypes=(("png files", ".png"), ("jpeg files", "jpg"),("bitmap files", ".bmp") ), defaultextension=".jpg")
        
        image.save(output_link)
        
        del image

    def start_filter(self):

        self.k = float(self.k_val.get())
        self.deltaT = float(self.deltaT_val.get())
        self.t = float(self.t_val.get())

        if(self.img == None or self.pixels == None):
            messagebox.showerror("Image not opened", "please open image")
            return
        
        self.algorithm(img = self.img, pixels = self.pixels)

        self.interImage = ImageTk.PhotoImage(image=self.img, size=(210, 120))
        self.img_label.config(image = self.interImage)
        self.window.update()

        messagebox.showinfo("Filtration was completed", "Фильтрация успешно завершена")
        



    def algorithm(self, img, pixels):
        level = 0
        
        step = self.t / self.deltaT


        while level < self.t:
            for i in range(1, img.width-1):
                for j in range(1, img.height-1):
                    I_x = (pixels[i+1, j] - pixels[i-1,j])/2
                    I_y = (pixels[i, j+1]-pixels[i,j-1])/2
                    I_xx = pixels[i+1,j]-2*pixels[i,j]+pixels[i-1, j]
                    I_yy = pixels[i, j+1] - 2*pixels[i,j] + pixels[i,j-1]
                    I_xy = pixels[i+1, j] - 2*pixels[i,j] + pixels[i, j-1]
                    rg = self.g(I_x*I_x+I_y*I_y)
                    f_x = (rg*rg)/(self.k*self.k)*(I_x*I_xx + I_y*I_xy)
                    f_y = (rg*rg)/(self.k*self.k)*(I_x*I_xy + I_y*I_yy)
                    pixels[i,j] = round(pixels[i,j] + self.deltaT*(rg*(I_xx+I_yy)+f_x*I_x+f_y*I_y))
            

            level += self.deltaT
            self.progress.step(step)

        self.progress.step(step)
        del rg, I_x, I_y, I_xx, I_yy, I_xy, f_x, f_y


if __name__ == "__main__":
    program = Program()
    program.initGUI()