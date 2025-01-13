from tkinter import*
from tkinter import font,Scrollbar,filedialog, colorchooser
from tkinter.messagebox import showinfo
class R_W_P():
    def __init__(self):
        self.screen=Tk()
        self.screen.title("Rudimentary Word Processor")
        self.width,self.height=800,500
        self.screen_width=self.screen.winfo_screenwidth()
        self.screen_height=self.screen.winfo_screenheight()
        self.screen.geometry("{}x{}+{}+{}".format(self.width, self.height, (self.screen_width-self.width)//2, (self.screen_height-self.height)//2))
        self.screen.configure(bg="white")
        self.default_values()
        self.screen.bind("<Control-x>",lambda e:self.c_c_p("cut",e))
        self.screen.bind("<Control-c>", lambda e:self.c_c_p("copy", e))
        self.screen.bind("<Control-v>",lambda e:self.c_c_p("paste",e))
        self.my_menu=Menu(self.screen)
        self.screen.config(menu=self.my_menu)
        self.menu_option=Menu(self.my_menu,tearoff=False)
        self.my_menu.add_cascade(label="Options",menu=self.menu_option)
        self.create_menus(self.menu_option,New=lambda:self.default_values(True),Open=self.open_file,Save=self.save_file,Save_as=self.save_file_as,separator=None,Exit=self.screen.quit)
        self.menu_edit=Menu(self.my_menu,tearoff=False)
        self.my_menu.add_cascade(label="Edit",menu=self.menu_edit)
        self.menu_edit.add_command(label="Cup  (ctrl+x)",command=lambda:self.c_c_p("cup",False))
        self.menu_edit.add_command(label="Copy  (ctrl+c)",command=lambda:self.c_c_p("copy",False))
        self.menu_edit.add_command(label="Paste  (ctrl+v)",command=lambda:self.c_c_p("paste",False))
        self.menu_edit.add_separator()
        self.menu_edit.add_command(label="Undo  (ctrl+z)",command=lambda:self.t1.edit_undo())
        self.menu_edit.add_command(label="Redo  (ctrl+y)",command=lambda:self.t1.edit_redo())
        self.menu_fonts=Menu(self.my_menu,tearoff=False)
        self.my_menu.add_cascade(label="Fonts",menu=self.menu_fonts)
        for font_name in list(font.families()):self.menu_fonts.add_command(label=font_name, command=lambda f=font_name: self.fonts(f, self.size, self.style))
        self.menu_style=Menu(self.my_menu,tearoff=False)
        self.my_menu.add_cascade(label="Style",menu=self.menu_style)
        for style in ["normal","bold","underline","italic"]:self.menu_style.add_command(label=style,command=lambda s=style:self.fonts(self.font_text,self.size,s))
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
    def create_menus(self,menu,**kwargs):
        for key, value in kwargs.items():
            menu.add_command(label=key,command=value) if key!="separator" else menu.add_separator()
    def color(self):
        self.color_text=colorchooser.askcolor()[1]
        self.config_text()
    def fonts(self,font,size,style,color_change=False,color=(0,0,0),change_text=True):
        self.font_text=font
        self.size=size
        self.style=style
        if color_change:self.color_text=color
        if change_text:self.config_text()
    def c_c_p(self,c,e):
        try:self.copy_or_cut_paste(c,e,"sel.first","sel.last")
        except:self.copy_or_cut_paste(c,e,"1.0",END,True)
    def copy_or_cut_paste(self,c,e,init=None,end=None,error=False):
        if e:self.paste=self.screen.clipboard_get()
        def repeat(c,init=None,end=None,error=False):
            if error:
                if c=="cup":self.paste=self.t1.get(init,end)
                self.t1.delete(init,end)
            if not error:self.paste=self.t1.selection_get()
            if c=="cup" and not error:self.t1.delete(init,end)
            self.screen.clipboard_clear()
            self.screen.clipboard_append(self.paste)
        if c=="cup":repeat(c,init,end,error)
        if c=="copy":repeat(c)
        if c=="paste":
            self.position=self.t1.index(INSERT)
            self.t1.insert(self.position,self.paste)
    def default_values(self,name_file="New",new=False):
        self.fonts("arial","10","normal",True,"black",False)
        self.paste=""
        self.name_file=name_file
        if new:self.t1.delete("1.0",END),self.config_text()
    def open_file(self):
        self.default_values("Open",True)
        self.file_open=filedialog.askopenfilename(title="Open File",filetypes=(("Text Files","*.txt"),("All Files","*.*")))
        if self.file_open is None:return
        with open(self.file_open,"r") as f:self.file_read=f.read()
        formats,content_text=self.get_parameters_open(self.file_read)
        self.fonts(formats['font'],formats['size'],formats['style'],True,formats['color'])
        self.t1.insert("1.0",content_text)
    def save_file(self):
        try:self.repeat_in_saves("Save")
        except:self.save_file_as()
    def save_file_as(self):
        self.file_save=filedialog.asksaveasfile(defaultextension=".*",filetypes=(("Text Files","*.txt"),("All Files","*.*")))
        if self.file_save is None:return
        self.repeat_in_saves("Save as")
    def repeat_in_saves(self,name_file):
        self.name_file=name_file
        formats=self.get_parameters_save()
        with open(self.file_save.name if self.name_file=="Save as" else self.file_open,"w") as f:
            for p, v in formats.items():f.write(f"{p}:{v}\n")
            f.write("\n\n")
            f.write(self.t1.get("1.0",END))
    def get_parameters_save(self):
        p_f={"font":self.font_text,
            "size":self.size,
            "style":self.style,
            "color":self.color_text}
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
        self.mode_dark_white(*("black","white","Light") if self.mode_state=="Dark" else ("white","black","Dark"))
        self.menu_mode.entryconfigure(0, label=f"{self.mode_state}")
    def mode_dark_white(self,color:str,color2:str,mode:str):
        self.color_text=color2 if self.color_text==color else self.color_text
        self.screen.configure(bg=color)
        self.config_text(color,color2)
        self.mode_state=mode
    def config_text(self,color=None,color2=None):
        try:
            self.t1.configure(bg=color,font=(self.font_text,self.size,self.style),foreground=self.color_text,selectbackground=color2,selectforeground=color)
            self.l1.configure(text=f"Font {self.font_text}, Size {self.size}, Style {self.style}, Color {self.color_text}, File {self.name_file}",bg=color,foreground=color2)
        except:self.default_values(),self.config_text()
    def about(self):
        showinfo("About", 
                """This is a simple text editor.
                \nDeveloped by: Esteban Matias Cancino
                \nVersion: 2.0
                \nstatus: in progress""")
    def help_fun(self):
        showinfo("Help", """
                / \__
                (    @\___
                /         O
                /   (_____/
                /_____/
                """)
if __name__=="__main__":R_W_P(),mainloop()