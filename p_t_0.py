from tkinter import*
from tkinter import font
from tkinter import Scrollbar
from tkinter import filedialog, colorchooser
from tkinter.messagebox import showinfo

class R_W_P():
    def __init__(self):
        self.screen=Tk()
        self.screen.title("Rudimentary Word Processor")
        self.width=800
        self.height=500
        self.screen_width=self.screen.winfo_screenwidth()
        self.screen_height=self.screen.winfo_screenheight()
        self.screen.geometry("{}x{}+{}+{}".format(self.width, self.height, (self.screen_width-self.width)//2, (self.screen_height-self.height)//2))
        self.screen.configure(bg="white")
        self.color_text="black"
        self.font_text="arial"
        self.size="10"
        self.style="normal"
        self.screen.bind("<Control-x>",lambda e:self.c_c("cut",e))
        self.screen.bind("<Control-c>", lambda e:self.c_c("copy", e))
        self.screen.bind("<Control-v>",lambda e:self.paste_text(e))
        self.paste=""
        self.name_file="New"
        self.my_menu=Menu(self.screen)
        self.screen.config(menu=self.my_menu)
        self.menu_option=Menu(self.my_menu,tearoff=False)
        self.my_menu.add_cascade(label="Options",menu=self.menu_option)
        self.menu_option.add_command(label="New",command=self.new_file)
        self.menu_option.add_command(label="Open",command=self.open_file)
        self.menu_option.add_command(label="Save",command=self.save_file)
        self.menu_option.add_command(label="Save as",command=self.save_file_as)
        self.menu_option.add_separator()
        self.menu_option.add_command(label="Exit",command=self.screen.quit)
        self.menu_edit=Menu(self.my_menu,tearoff=False)
        self.my_menu.add_cascade(label="Edit",menu=self.menu_edit)
        self.menu_edit.add_command(label="Cup  (ctrl+x)",command=lambda:self.c_c("cup",False))
        self.menu_edit.add_command(label="Copy  (ctrl+c)",command=lambda:self.c_c("copy",False))
        self.menu_edit.add_command(label="Paste  (ctrl+v)",command=lambda:self.paste_text(False))
        self.menu_edit.add_separator()
        self.menu_edit.add_command(label="Undo  (ctrl+z)",command=lambda:self.t1.edit_undo())
        self.menu_edit.add_command(label="Redo  (ctrl+y)",command=lambda:self.t1.edit_redo())
        self.menu_fonts=Menu(self.my_menu,tearoff=False)
        self.my_menu.add_cascade(label="Fonts",menu=self.menu_fonts)
        self.list_fonts=list(font.families())
        for font_name in self.list_fonts:self.menu_fonts.add_command(label=font_name, command=lambda f=font_name: self.fonts(f, self.size, self.style))
        self.menu_style=Menu(self.my_menu,tearoff=False)
        self.my_menu.add_cascade(label="Style",menu=self.menu_style)
        self.list_style=["normal","bold","underline","italic"]
        for style in self.list_style:self.menu_style.add_command(label=style,command=lambda s=style:self.fonts(self.font_text,self.size,s))
        self.my_menu.add_command(label="Colors",command=lambda:self.color())
        self.menu_size=Menu(self.my_menu,tearoff=False)
        self.my_menu.add_cascade(label="Size",menu=self.menu_size)
        for size in range(2,52,2):self.menu_size.add_command(label=str(size),command=lambda s=size:self.fonts(self.font_text,s,self.style))
        self.mode_state="Dark"
        self.menu_mode=Menu(self.my_menu,tearoff=False)
        self.my_menu.add_cascade(label="Mode",menu=self.menu_mode)
        self.menu_mode.add_command(label=f"{self.mode_state}",command=lambda:self.mode())
        self.my_menu.add_command(label="About", command=lambda:self.about())
        self.my_menu.add_command(label="Help", command=lambda:self.help_fun())
        self.y_scroll=Scrollbar(self.screen,orient=VERTICAL)
        self.y_scroll.pack(side=RIGHT,fill=Y)
        self.t1=Text(self.screen,bg="white",font=(self.font_text,self.size,self.style),undo=True,selectbackground="black",selectforeground="white",yscrollcommand=self.y_scroll.set,height=1)
        self.t1.pack(fill=BOTH,expand=1)
        self.y_scroll.config(command=self.t1.yview)
        self.l1=Label(self.screen,text=f"Font {self.font_text}, Size {self.size}, Style {self.style}, Color {self.color_text}, File {self.name_file}",bg="white",anchor=N)
        self.l1.pack(side=BOTTOM)
    def color(self):
        self.color_text=colorchooser.askcolor()[1]
        self.t1.configure(foreground=self.color_text)
        self.l1.configure(text=f"Font {self.font_text}, Size {self.size}, Style {self.style}, Color {self.color_text}, File {self.name_file}")
    def fonts(self,font,size,style):
        self.font_text=font
        self.size=size
        self.style=style
        self.t1.configure(font=(self.font_text,self.size,self.style))
        self.l1.configure(text=f"Font {self.font_text}, Size {self.size}, Style {self.style}, Color {self.color_text}, File {self.name_file}")
    def c_c(self,c,e):
        try:
            if e:self.paste=self.screen.clipboard_get()
            if c=="cup":
                self.paste=self.t1.selection_get()
                self.t1.delete("sel.first","sel.last")
                self.screen.clipboard_clear()
                self.screen.clipboard_append(self.paste)
            if c=="copy":
                self.paste=self.t1.selection_get()
                self.screen.clipboard_clear()
                self.screen.clipboard_append(self.paste)
        except:
            if e:self.paste=self.screen.clipboard_get()
            if c=="cup":
                self.paste=self.t1.get("1.0",END)
                self.t1.delete("1.0",END)
                self.screen.clipboard_clear()
                self.screen.clipboard_append(self.paste)
            if c=="copy":
                self.paste=self.t1.get("1.0",END)
                self.screen.clipboard_clear()
                self.screen.clipboard_append(self.paste)
    def paste_text(self,e):
        if e:self.paste=self.screen.clipboard_get()
        else:
            self.position=self.t1.index(INSERT)
            self.t1.insert(self.position,self.paste)
    def new_file(self):
        self.t1.delete("1.0",END)
        self.color_text="black"
        self.font_text="arial"
        self.size="10"
        self.style="normal"
        self.paste=""
        self.name_file="New"
        self.t1.configure(font=(self.font_text,self.size,self.style),foreground=self.color_text)
        self.l1.configure(text=f"Font {self.font_text}, Size {self.size}, Style {self.style}, Color {self.color_text}, File {self.name_file}")
    def open_file(self):
        self.new_file()
        self.file_open=filedialog.askopenfilename(title="Open File",filetypes=(("Text Files","*.txt"),("All Files","*.*")))
        if self.file_open is None:return
        self.name_file="Open"
        with open(self.file_open,"r") as f:
            self.file_read=f.read()
        formats,content_text=self.get_parameters_open(self.file_read)
        self.fonts(formats['font'],
                    formats['size'],
                    formats['style'])
        self.color_text=formats['color']
        self.t1.configure(foreground=self.color_text)
        self.l1.configure(text=f"Font {self.font_text}, Size {self.size}, Style {self.style}, Color {self.color_text}, File {self.name_file}")
        self.t1.insert("1.0",content_text)
    def save_file(self):
        try:
            self.name_file="Save"
            formats=self.get_parameters_save()
            with open(self.file_open,"w") as f:
                for p, v in formats.items():
                    f.write(f"{p}:{v}\n")
                f.write("\n\n")
                f.write(self.t1.get("1.0",END))
        except:self.save_file_as()
    def save_file_as(self):
        self.file_save=filedialog.asksaveasfile(defaultextension=".*",filetypes=(("Text Files","*.txt"),("All Files","*.*")))
        text=self.t1.get("1.0",END)
        if self.file_save is None:return
        self.name_file="Save as"
        formats=self.get_parameters_save()
        with open(self.file_save.name,"w") as f:
            for p, v in formats.items():
                f.write(f"{p}:{v}\n")
            f.write("\n\n")
            f.write(text)
    def get_parameters_save(self):
        f=self.font_text
        s=self.size
        st=self.style
        c=self.color_text
        p_f={"font":f,
            "size":s,
            "style":st,
            "color":c}
        return p_f
    def get_parameters_open(self, content):
        metadatos, content_text = content.split("\n\n", 1)
        content_text=content_text.strip()
        parameters = {}
        for line in metadatos.splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                parameters[key.strip()] = value.strip()
        return parameters, content_text
    def mode(self):
        if self.mode_state=="Dark":
            if self.color_text=="black":self.color_text="white"
            else:self.color_text=self.color_text
            self.screen.configure(bg="black")
            self.t1.configure(bg="black",foreground=self.color_text,selectbackground="white",selectforeground="black")
            self.l1.configure(bg="black",foreground="white")
            self.l1.configure(text=f"Font {self.font_text}, Size {self.size}, Style {self.style}, Color {self.color_text}, File {self.name_file}")
            self.mode_state="Light"
        else:
            self.screen.configure(bg="white")
            if self.color_text=="white":self.color_text="black"
            else:self.color_text=self.color_text
            self.t1.configure(bg="white",foreground=self.color_text,selectbackground="black",selectforeground="white")
            self.l1.configure(bg="white",foreground="black")
            self.l1.configure(text=f"Font {self.font_text}, Size {self.size}, Style {self.style}, Color {self.color_text}, File {self.name_file}")
            self.mode_state="Dark"
        self.menu_mode.entryconfigure(0, label=f"{self.mode_state}")
    def about(self):
        showinfo("About", 
                """This is a simple text editor.
                \nDeveloped by: Esteban Matias Cancino
                \nVersion: 1.0
                \nstatus: in progress""")
    def help_fun(self):
        showinfo("Help", """
                / \__
                (    @\___
                /         O
                /   (_____/
                /_____/   U
                """)
if __name__=="__main__":
    R_W_P()
    mainloop()