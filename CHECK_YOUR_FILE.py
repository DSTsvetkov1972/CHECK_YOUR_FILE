import tkinter 
from functions import *
from params import *
from checks_manager import *

# создаём нужные для работы папки при первом запуске
#if not os.path.exists('.config'): os.makedirs('.config')
if not os.path.exists('template'): os.makedirs('template') 
if not os.path.exists('to_check'): os.makedirs('to_check') 
"""
# предлагаем залогиниться
if not os.path.exists(os.path.join('.config','.config')): 
    messagebox.showwarning(MSG_BOX_TITLE,'Залогиньтесь, пожалуйста!')
    Log_in(TK_TITLE)
"""
# 
root = tkinter.Tk()
TK_TITLE = "CHECK_YOU_FILE V.%s %s "%(1,os.path.join(os.path.abspath(os.curdir)))
#print(len("CHECK_YOU_FILE V.%s %s "%(1,os.path.join(os.path.abspath(os.curdir)))))
root.title(TK_TITLE)
root.geometry('%sx120'%(720 if len(os.path.abspath(os.curdir)) <= 80 else int(720/80*len(os.path.abspath(os.curdir)))))

mainmenu = tkinter.Menu(root)

#print(dir(mainmenu))

#--------------------------------------------



label_font = 14
label_width = 6
label_height = 1
label_anchor = 'e'

text_font = 'Arial 16'
text_width = 16
text_height = 1

r = 0
label_0 = tkinter.Label(root
                        #,bg="white"                                
                        ,height = label_height
                        ,width  = label_width 
                        ,font   = label_font
                        ,anchor = label_anchor
                        ,text= '')
label_0.grid(row = r, column = 0, sticky = 'w' )

r = 1
button_start = tkinter.Button(root
                        ,text = 'Проверить файлы'
                        ,font = 'Arial 18'
                        ,bg = 'light grey'
                        ,fg = 'green'
                        ,width = 24
                        ,justify='center'
                        #,bg = 'grey'
                        ,command = lambda: checks_launcher(mainmenu, label_get_new_version) 
                        )
button_start.grid(row=r,column=0,  padx = 5,  sticky='nw')
r = 2
label_1 = tkinter.Label(root
                        #,bg="white"                                
                        ,height = label_height
                        ,width  = label_width 
                        ,font   = label_font
                        ,anchor = label_anchor
                        ,text= '')
label_1.grid(row = r, column = 0)#, sticky = 'center' )
r = 3

label_get_new_version = tkinter.Label(root
                        ,fg='red'                                
                        ,height = label_height
                        ,width  = label_width*10
                        ,font   = 'Arial 10 underline'
                        ,anchor = 'w'
                        ,text= '')

label_get_new_version.grid(row = r, column = 0, sticky = 'w', padx= 10 )


root.config(menu=mainmenu)

mainmenu.add_command(label='Инструкция')
mainmenu.add_command(label='Контакты разработчиков', command = lambda: show_message(developers_message))
mainmenu.add_command(label="Подключиться", command = lambda: Log_in(mainmenu,label_get_new_version), foreground='red')

Log_in_check(mainmenu,label_get_new_version)

root.mainloop()
