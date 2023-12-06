import pandas as pd
import ctypes
import os
import shutil
import datetime
import tkinter
import pyperclip
from tkinter import messagebox
from clickhouse_driver import Client
from datetime import datetime
from params import *
from cryptography.fernet import Fernet



def available_checks_list():
    import checks
    checks_list=[]
    for check_function_name, check_function in checks.__dict__.items():
        if callable(check_function) and 'check' in check_function_name:
            checks_list.append(check_function())
    return checks_list

def Get_clipboard(text_container):
    try:
        clipboard_content = pyperclip.paste()
    except:
        clipboard_content = '???'
        
    text_container.delete('1.0', tkinter.END)        
    text_container.insert("1.0", clipboard_content)     

def get_df_of_click(query: str):
        params = get_params()
        connection=Client(host   = params[0],
                        port     = params[1],
                        database = params[2],
                        user     = params[3],
                        password = params[4],
                        secure=True,verify=False)
        with connection:
            return connection.query_dataframe(query)
        


def execute_sql_click(query: str):    
        params = get_params()
        connection=Client(host   = params[0],
                        port     = params[1],
                        database = params[2],
                        user     = params[3],
                        password = params[4],
                        secure=True,verify=False)
        connection.execute(query)

def Column_name_check(to_check_df,template_df):
    columns_in_template_and_to_check = sorted(list(set(list(to_check_df.columns) + list(template_df.columns))))
    result = []
    for column_number in columns_in_template_and_to_check:
        try:
            to_check_column_name = to_check_df[column_number][0]
            if pd.isna(to_check_column_name): to_check_column_name=''
        except:
            to_check_column_name = ''
        
        try:
            template_column_name = template_df[column_number][0]
            if pd.isna(template_column_name): template_column_name=''
        except:
            template_column_name = ''

        if to_check_column_name == template_column_name:
            result.append((True,'Столбец %s - ок'%(column_number+1)))
        else:
            result.append( (False,
                '\nСтолбец %s\nНЕ СОВПАДАЮТ НАЗВАНИЯ СТОЛБЦОВ!\nВ шаблоне: `%s`\nВ проверяемоЙ таблице: `%s`'%((column_number+1),
                                                                        template_column_name,
                                                                        to_check_column_name
                                                                        )))
    return result
"""
to_check_df = pd.read_excel(r'to_check\Проверяем_1.xlsx',header = None)
template_df = pd.read_excel(r'template\Шаблон.xlsx',header = None)
res_list = [x[1] for x in Column_name_check(to_check_df,template_df) if not x[0]]
print(Column_name_check(to_check_df,template_df) )
print('\n'.join(res_list))
"""

def Get_template ():
    backup_file = 'Проверяем_%s.xlsx'%(datetime.now().strftime('%Y-%m-%d_%X')).replace(':','-')
    #print(backup_file)
    
    if 'Шаблон.xlsx' in list(os.walk('.'))[0][2]:
        shutil.copy('Проверяем.xlsx',backup_file)
        shutil.copy('Шаблон.xlsx','Проверяем.xlsx')
        #print(list(os.walk('.'))[0][2])
        messagebox.showinfo(title=MSGBOX_TITLE,
            message='Файл "Проверяем.xlsx" из шаблона создан. Предыдущий файл сохранен в %s'%(backup_file))
    else:
        messagebox.showerror(title = MSGBOX_TITLE, message = 'Файл Шаблон.xlsx отсутствует в рабочей папке!')
#Get_template ()

def Required_fields_check(to_check_df,column_number):
    #print('*'*50,to_check_df[0][1],'*'*50,sep='\n')
    column_name = to_check_df[column_number][0]
    #print('*'*50,column_name,'*'*50,sep='\n')
    result = []
    for row in list(to_check_df.iterrows())[1:]:
        #print(row[1][column_number])
        if pd.isna(row[1][column_number]) or row[1][column_number] == '' or row[1][column_number] == ' ':
            result.append((False,
                        'Столбец: %s Строка: %s Колонка: `%s` - ОБЯЗАТЕЛЬНОЕ ПОЛЕ НЕ ЗАПОЛНЕНО!'%(column_number+1,
                                                                                                row[0]+1,
                                                                                                column_name,
                                                                                                )))
        else:
            result.append((True,
                        'Столбец: %s Строка: %s Колонка: `%s` обязательное поле - ок!'%(column_number+1,
                                                                                        row[0]+1,
                                                                                        column_name
                                                                                        )))
    return result

"""
to_check_df = pd.read_excel(r'to_check/Проверяем.xlsx',header = None)
template_df = pd.read_excel(r'template/Шаблон.xlsx',header = None)
res_list = [x[1] for x in Required_fields_check(to_check_df,0) if not x[0] ]
print(res_list)
print('\n'.join(res_list))
"""

def keys(event): # Функция чтобы работала вставка из буфера в русской раскладке
    import ctypes
    u = ctypes.windll.LoadLibrary("user32.dll")
    pf = getattr(u, "GetKeyboardLayout")
    if hex(pf(0)) == '0x4190419':
        keyboard_layout = 'ru'
    if hex(pf(0)) == '0x4090409':
        keyboard_layout = 'en'

    if keyboard_layout == 'ru':
        if event.keycode==86:
            event.widget.event_generate("<<Paste>>")
        elif event.keycode==67: 
            event.widget.event_generate("<<Copy>>")    
        elif event.keycode==88: 
            event.widget.event_generate("<<Cut>>")    
        elif event.keycode==65535: 
            event.widget.event_generate("<<Clear>>")
        elif event.keycode==65: 
            event.widget.event_generate("<<SelectAll>>")

def get_params():
        params = open(os.path.join('.config')).read()
        decoded_text = Fernet(b'lXgjsyWLG2R-nAWC1vBkz-FWFzeWFi-71rNMiO2ON40=').decrypt(params).decode('utf-8')
        return(decoded_text.split('\n'))
 

def get_last_version(label_get_new_version):
    sql = """
        SELECT 
            max(version) new_version,
            argMax(message,version) new_version_message
        FROM
            (SELECT 
                toInt64OrNull(
                    replace(
                        splitByChar('|',log_info )[1],
                        'version',
                        ''
                    )
                ) as version,
                splitByChar('|',log_info )[2] AS message
            FROM 
                audit._check_your_file 
            WHERE 
                log_info LIKE '%version%')
        """

    last_version_info = get_df_of_click(sql)
    #return(last_version_info)
    last_version_number  = last_version_info['new_version'][0]
    last_version_message = last_version_info['new_version_message'][0]

    if last_version_number > version:
        label_get_new_version.config(text = 'Версия %s доступна для скачивания'%last_version_number)
        label_get_new_version.bind('<Button-1>', lambda x:show_message(last_version_message))
    else:
        label_get_new_version.config(text = '')
        label_get_new_version.unbind('<Button-1>')


#print(get_last_version())

def connection_settings_file_creator(CLICK_HOST,
                                     CLICK_PORT,
                                     CLICK_DBNAME,
                                     CLICK_USER,
                                     CLICK_PWD,
                                     root,
                                     mainmenu,
                                     label_get_new_version):
    try: 
        #print('aaaa connection_settings_file_creator')
        connection=Client(host=CLICK_HOST,
                port = CLICK_PORT,
                database=CLICK_DBNAME,
                user=CLICK_USER,
                password=CLICK_PWD,
                secure=True,verify=False)
        #print('bbbb connection_settings_file_creator')        
        print(CLICK_HOST,
            CLICK_PORT,
            CLICK_DBNAME,
            CLICK_USER,
            CLICK_PWD,sep='\n')
        if connection.query_dataframe('SELECT 777 AS a')['a'][0] == 777:
            params = ('%s\n%s\n%s\n%s\n%s')%(CLICK_HOST,CLICK_PORT,CLICK_DBNAME,CLICK_USER,CLICK_PWD)
        with open (os.path.join('.config'),'wb') as config_file:
            encoded_text = Fernet(b'lXgjsyWLG2R-nAWC1vBkz-FWFzeWFi-71rNMiO2ON40=').encrypt(params.encode('utf-8'))
            config_file.write(encoded_text)
            # делаем файл с конфигурацией скрытым
            FILE_ATTRIBUTE_HIDDEN = 0x02
            SetFileAttributes = ctypes.windll.kernel32.SetFileAttributesW
            GetLastError = ctypes.windll.kernel32.GetLastError

            filename = ".config"
            if not SetFileAttributes(filename, FILE_ATTRIBUTE_HIDDEN):
                errcode = GetLastError()       
                print("Не удалось скрыть файл. Код ошибки: " + str(errcode))
            else:   
                print("Файл скрыт успешно.")            
        root.destroy() 
        Log_in_check(mainmenu, label_get_new_version)  
        """  
        messagebox.showinfo(MSG_BOX_TITLE, 'Удалось подключиться к DWH!')
        filemenu = tkinter.Menu(mainmenu, tearoff=0)
        filemenu.add_command(label="Проверить соединение", command = lambda: Log_in_check(root,mainmenu))
        filemenu.add_command(label="Сменить пользователя", command = lambda: Log_in(root,mainmenu))
        filemenu.add_command(label="Выйти", command = lambda: Log_out(root,mainmenu))
        mainmenu.delete(3)
        mainmenu.add_cascade(label=get_params()[3],menu = filemenu, foreground = 'green') 
        """
    except:
        messagebox.showerror(MSG_BOX_TITLE, 'Не удалось подключиться к DWH!\nПроверьте параметры и повторите попрытку!', parent = root)

def Log_in(mainmenu,label_get_new_version):
    def on_closing():
        mainmenu.entryconfig(3, state = 'normal')
        root.destroy()

    mainmenu.entryconfig(3, state = 'disabled')

    root = tkinter.Tk()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.title(MSG_BOX_TITLE)
    root.geometry('720x264')

    label_font = 18
    label_width = 12
    label_height = 1
    label_anchor = 'e'

    text_font = 'Arial 16'
    text_width = 42
    text_height = 1

    r = 0
    label_0 = tkinter.Label(root
                            #,bg="white"                                
                            ,height = label_height
                            ,width  = label_width 
                            ,font   = label_font
                            ,anchor = label_anchor
                            ,text=' ')
    label_0.grid(row = r, column = 0, sticky = 'w' )

    r = 1
    label_host = tkinter.Label(root
                            #,bg="white"
                            ,height = label_height
                            ,width  = label_width 
                            ,font   = label_font
                            ,anchor = label_anchor
                            ,text='HOST')
    label_host.grid(row = r, column = 0, sticky = 'w' )

    text_host = tkinter.Text(root
                            ,font = text_font                         
                            ,height = text_height  
                            ,width= text_width
                            ,fg = 'blue'
                            )
    text_host.grid(row=r,column=1, padx = 5, sticky = 'w' )
    text_host.bind("<Control-KeyPress>", keys)

    r = 2
    label_port = tkinter.Label(root
                            #,bg="white"                                
                            ,height = label_height
                            ,width  = label_width 
                            ,font   = label_font
                            ,anchor = label_anchor
                            ,text='PORT')
    label_port.grid(row = r, column = 0, sticky = 'w')

    text_port = tkinter.Text(root
                            ,font = text_font                         
                            ,height = text_height  
                            ,width= text_width
                            ,fg = 'blue')
    text_port.grid(row=r,column=1, padx = 5, sticky = 'w')
    text_port.bind("<Control-KeyPress>", keys)

    r = 3
    label_dbname = tkinter.Label(root
                            #,bg="white"                                
                            ,height = label_height
                            ,width  = label_width 
                            ,font   = label_font
                            ,anchor = label_anchor
                            ,text='DBNAME')
    label_dbname.grid(row = r, column = 0, sticky = 'w')

    text_dbname = tkinter.Text(root
                            ,font = text_font                         
                            ,height = text_height  
                            ,width= text_width
                            ,fg = 'blue')
    text_dbname.grid(row=r,column=1, padx = 5, sticky = 'w')
    text_dbname.bind("<Control-KeyPress>", keys)
    
    r = 4
    label_user = tkinter.Label(root
                            #,bg="white"                                
                            ,height = label_height
                            ,width  = label_width 
                            ,font   = label_font
                            ,anchor = label_anchor
                            ,text='USER')
    label_user.grid(row = r, column = 0, sticky = 'w')

    text_user = tkinter.Text(root
                            ,font = text_font                         
                            ,height = text_height  
                            ,width= text_width
                            ,fg = 'blue')
    text_user.grid(row=r,column=1, padx = 5, sticky = 'w')
    text_user.bind("<Control-KeyPress>", keys) 
    
    r = 5
    label_password = tkinter.Label(root
                            #,bg="white"                                
                            ,height = label_height
                            ,width  = label_width 
                            ,font   = label_font
                            ,anchor = label_anchor
                            ,text='PASSWORD')
    label_password.grid(row = r, column = 0, sticky = 'w')

    entry_password = tkinter.Entry(root
                            ,font = text_font                         
                            ,width= text_width
                            ,fg = 'blue'
                            ,show = "●"
                            )
    entry_password.grid(row=r,column=1, padx = 5, sticky = 'w')
    entry_password.bind("<Control-KeyPress>", keys)   
    
    r = 6
    label_3 = tkinter.Label(root
                            #,bg="white"                                
                            ,height = label_height
                            ,width  = label_width 
                            ,font   = label_font
                            ,anchor = label_anchor
                            ,text=' ')
    label_3.grid(row = r, column = 0, sticky = 'w')       
    
    r = 7
    button_start = tkinter.Button(root
                            ,text = 'Подключиться'
                            ,font = 'Arial 18'
                            ,bg = 'light grey'
                            ,fg = 'green'
                            ,width = 34
                            ,justify='center'
                            #,bg = 'grey'

                            ,command = lambda: connection_settings_file_creator(text_host.get('1.0',tkinter.END).strip(),
                                                                                text_port.get('1.0',tkinter.END).strip(),
                                                                                text_dbname.get('1.0',tkinter.END).strip(),
                                                                                text_user.get('1.0',tkinter.END).strip(),
                                                                                entry_password.get().strip(),
                                                                                root,
                                                                                mainmenu,
                                                                                label_get_new_version)              
                            )
    button_start.grid(row=r,column=1, rowspan=1, padx = 5, columnspan= 2, sticky='n')
    
    r = 8
    label_5 = tkinter.Label(root
                            #,bg="white"                                
                            ,height = label_height
                            ,width  = label_width 
                            ,font   = label_font
                            ,anchor = label_anchor
                            ,text='')
    label_5.grid(row = r, column = 0, sticky = 'w')

    root.mainloop()


def Log_in_check(mainmenu, label_get_new_version, show_message_if_ok = True):
    if not os.path.exists(os.path.join('.config')): 
        messagebox.showwarning(MSG_BOX_TITLE,'Подключитесь, пожалуйста!')
        #root.title(TK_TITLE)
        #filemenu = tkinter.Menu(mainmenu, tearoff=0)
        mainmenu.delete(3)
        mainmenu.add_command(label="Подключиться", command = lambda: Log_in(mainmenu,label_get_new_version), foreground='red')
        return False
    else:
        filemenu = tkinter.Menu(mainmenu, tearoff=0)
        filemenu.add_command(label="Проверить соединение", command = lambda: Log_in_check(mainmenu,label_get_new_version))
        filemenu.add_command(label="Сменить пользователя", command = lambda: Log_in(mainmenu,label_get_new_version))
        filemenu.add_command(label="Выйти", command = lambda: Log_out(mainmenu,label_get_new_version))
    params = get_params()
    #print(params)
    try:
        connection=Client(host=params[0],
                port = int(params[1]),
                database=params[2],
                user=params[3],
                password=params[4],
                secure=True,verify=False)
        """
        connection=Client(host='rc1a-rgjcum1ijv22bo62.mdb.yandexcloud.net',
                port = 9440,
                database='history',
                user='cvetkov_d',
                password='NdKVRepY1eUWq35Tk22d',
                secure=True,verify=False)
        """
        #print((params[0]),int(params[1]),params[2],params[3],params[4],sep='\n')  
        #print(connection.query_dataframe('SELECT 777 AS a')['a'][0])      

        if connection.query_dataframe('SELECT 777 AS a')['a'][0] == 777:
            #root.title(TK_TITLE + ' ' + params[3])
            mainmenu.delete(3)
            mainmenu.add_cascade(label=get_params()[3],menu = filemenu, foreground = 'green')  
            get_last_version(label_get_new_version)
            if show_message_if_ok: 
                messagebox.showinfo(MSG_BOX_TITLE,"Соединение установлено!")
            return True
        else:
            mainmenu.delete(3)
            mainmenu.add_cascade(label=get_params()[3],menu = filemenu, foreground = 'red')   
            messagebox.showerror(MSG_BOX_TITLE,"Нет соединения с базой данных!\nВозможно не работает интернет или проблемы на стороне сервера.")
            return False
    except:
        mainmenu.delete(3)
        mainmenu.add_cascade(label=get_params()[3],menu = filemenu, foreground = 'red')         
        messagebox.showerror(MSG_BOX_TITLE,"Нет соединения с базой данных!\nВозможно не работает интернет или проблемы на стороне сервера.")    
        return False

def Log_out(mainmenu, label_get_new_version):
    if os.path.exists(os.path.join('.config')):
        os.remove(os.path.join('.config')) 
        #print(dir(mainmenu))
        mainmenu.delete(3)
        mainmenu.add_command(label="Подключиться", command = lambda: Log_in(mainmenu, label_get_new_version), foreground='red')
        messagebox.showwarning(MSG_BOX_TITLE,'Вы вышли из аккаунта!')        
    else:
        messagebox.showwarning(MSG_BOX_TITLE,'А Вы и не были подключены!')

def show_message(message):
    root = tkinter.Tk()
    root.title(MSG_BOX_TITLE)
    root.geometry('380x160')


    developers_info_text = tkinter.Text(root,wrap=tkinter.WORD)

    developers_info_text.bind("<Control-KeyPress>", keys)
    developers_info_text.insert('1.0', message)
    developers_info_text.configure(state='disabled')
    developers_info_text.pack()
    root.mainloop() 



#show_developers_info()   
# 

#execute_sql_click("SELECT 1") 