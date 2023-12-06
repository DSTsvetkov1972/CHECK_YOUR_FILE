import pandas as pd
import os
import datetime
import winsound
import tkinter 
from tkinter import messagebox
from clickhouse_driver import Client
import functions as fn
import checks
from params import *

def checks_manager(file_to_check):   
    #print(file_to_check)         
    to_check_df = pd.read_excel(file_to_check,header = None).fillna('')
    template_df = pd.read_excel(os.path.join(os.path.abspath(os.curdir),'template','Шаблон.xlsx'),header = None).fillna('')
    checks_result_list = []

    #-----------------------------------------------------------------------------#
    # проверяем чтобы количество столбцов в шаблоне и проверяемом файле совпадало #
    #-----------------------------------------------------------------------------#
    #print('проверяем чтобы количество столбцов в шаблоне и проверяемом файле совпадало')
    #print(len(to_check_df.columns),len(template_df.columns),sep='\n')
    if len(to_check_df.columns) != len(template_df.columns): 
        checks_result_list.append((False,'Количество столбцов в проверяемом файле (%s) и шаблоне (%s) не совпадает!'%(len(to_check_df.columns),len(template_df.columns))))

    #-----------------------------------------------------------------------------#
    #   проверяем, чтобы имена столбцов в шаблоне и проверяемом файле совпадали   #
    #-----------------------------------------------------------------------------#
        #print('проверяем, чтобы имена столбцов в шаблоне и проверяемом файле совпадали')
        
    elif [column_name_check_result for column_name_check_result in fn.Column_name_check(to_check_df,template_df) if not column_name_check_result[0]] != []:
        checks_result_list = checks_result_list + fn.Column_name_check(to_check_df,template_df)
    else:
        for column_number in range(0,len(to_check_df.columns)):
            #print(column_number+1,template_df[column_number][0],template_df[column_number][1],template_df[column_number][2])
            if template_df[column_number][1] != 'нет' or template_df[column_number][2] != 'нет':
             
                check_in_checks_list = ('' if template_df[column_number][1] in  fn.available_checks_list()  else '\n'+ '-'*96 +'\nВНИМАНИЕ: ТАКОЙ ПРОВЕРКИ НЕТ В СПИСКЕ ПОДДЕРЖИВАЕМЫХ ЭТОЙ ВЕРИСЕЙ ПРОГРАММЫ!\nДОСТУПНЫ: %s'%(', '.join(fn.available_checks_list()))+'\n'+'-'*96)
                checks_result_list.append((False,'\nСтолбец: %s Обазательное: %s Проверка: %s'%(str(column_number+1),template_df[column_number][2],template_df[column_number][1]) + check_in_checks_list)                    
                                          )               
            column_name = template_df[column_number][0]
     #       print(column_name)
        # print('','*'*50,column_name,'*'*50,sep='\n')

    #-----------------------------------------------------------------------------#
    #                    проверка заполнения обязательного поля                   #
    #-----------------------------------------------------------------------------#
            #print('проверка заполнения обязательного поля')
            required_field = template_df[column_number][2]
            if required_field == 'да':
                required_fields_check_result = [required_field_check_result for required_field_check_result in  fn.Required_fields_check(to_check_df,column_number) if not required_field_check_result[0]]
                checks_result_list = checks_result_list + required_fields_check_result

    #-----------------------------------------------------------------------------#
    #                     проверки                                                #
    #-----------------------------------------------------------------------------#
            #print('проверки')    
            check_type  = template_df[column_number][1]
            for check_function_name, check_function in checks.__dict__.items():
                if (callable(check_function) 
                    and 'check' in check_function_name): 
                    #and check_function_name == 'Esu_id_check'):
                        #print(check_function_name)
                        check_result = check_function(to_check_df=to_check_df,
                                                      column_number=column_number,
                                                      check_type=check_type)
                        #print(check_result)
                        checks_result_list = checks_result_list + check_result
            

    #-----------------------------------------------------------------------------#
    #                     подготовка вывода                                       #
    #-----------------------------------------------------------------------------#

    output_list = [x[1] for x in checks_result_list if not x[0]]
    #checks_results_dir = os.path.join(os.path.abspath(os.curdir),'checks_results')
                        
    if output_list == [(False,'\n')]:
        return('Результат: ФАЙЛ ПОЛНОСТЬЮ СООТВЕТСТВУЕТ ШАБЛОНУ!')
    else:
        return('\n'.join(output_list))



  #  winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS) 

def checks_launcher (mainmenu,label_get_new_version):

    # Проверяем наличие шаблона
    if not os.path.exists(os.path.join(os.path.abspath(os.curdir),'template','Шаблон.xlsx')): 
        messagebox.showerror(MSG_BOX_TITLE,'В папке template не найден файл Шаблон.xlsx!')
        return
    # Проверяем наличие файлов для проверки
    files_to_check_list = []
    for root_dir, dirs, files in os.walk('to_check'):
        for file in files:
            file_to_check = os.path.join(os.path.abspath(os.curdir),root_dir,file)
            if not(file_to_check[-5:] != '.xlsx' or '~' in file_to_check): 
                files_to_check_list.append(file_to_check)
    if files_to_check_list == []: 
        messagebox.showwarning(MSG_BOX_TITLE,'В папке to_check нет экселевских файлов!')
        return

    
###################################################################################################   
    if fn.Log_in_check(mainmenu, label_get_new_version, show_message_if_ok = False):
        root = tkinter.Tk()
        root.title(MSG_BOX_TITLE)
        root.geometry('1440x720')

        info_text = tkinter.Text(root, height = 700, width = 1420)

        info_text.bind("<Control-KeyPress>", fn.keys)

        
        info_text.pack(padx=10,pady=10)
        
        #return
        checked_files_qty = 0
        for root_dir, dirs, files in os.walk('to_check'):
            
            for file in files:
                file_to_check = os.path.join(os.path.abspath(os.curdir),root_dir,file)
                #print(file_to_check[-5:])
                if file_to_check[-5:] != '.xlsx' or '~' in file_to_check: 
                    continue
                output = '='*120 + '\n' + file_to_check + '\n' + '='*120+ '\n' + checks_manager(file_to_check) + '\n'*2
                info_text.insert('1.0', output)
                checked_files_qty += 1

        info_text.configure(state='disabled') 
        sql = """
                CREATE OR REPLACE TABLE audit._check_your_file
                ENGINE = Memory()
                AS 
                (SELECT 
                    *
                FROM
                    audit._check_your_file
                UNION ALL
                SELECT
                    '%s Пользователь: %s Проверено файлов: %s' AS log_info
                )
            """%(datetime.datetime.now().strftime('%d-%m-%Y %H-%M-%S'),fn.get_params()[3],checked_files_qty)
        #print(sql)
        fn.execute_sql_click(sql)  
        winsound.MessageBeep(type=winsound.MB_OK)
        root.mainloop() 
             

#checks_launcher ()           