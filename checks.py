import pandas as pd
import os
import shutil
import datetime
from tkinter import messagebox
from functions import get_df_of_click

def Order_id_check (**kwargs):
    check_name = 'заказ'
    if kwargs == {}:
        return check_name
    to_check_df,column_number,check_type = kwargs['to_check_df'],kwargs['column_number'],kwargs['check_type']
    
    result = []
    if check_type == check_name:
        column_name= to_check_df[column_number][0]
        order_id_sql = """SELECT DISTINCT toString(order__id)  AS order_id FROM bpm__order WHERE order_id IN ('31093623','31041765')"""
        order_id_df = get_df_of_click(order_id_sql)
 ###########################################################       
        to_check_df = to_check_df[column_number].apply(str)
############################################################

        compare_df = pd.merge(
            to_check_df,
            order_id_df['order_id'],
            how = 'left',
            left_on = column_number,
            right_on = 'order_id'
        )
        for row in list(compare_df.iterrows())[1:]:
            if pd.isna(row[1][column_number]) or row[1][column_number] == '': 
                result.append((True,
                            'Столбец: %s Cтрока: %s Колонка: `%s` Значение: %s - ПОЛЕ НЕ ЗАПОЛНЕНО!'%(column_number+1,
                                                                                    column_name,
                                                                                    row[0]+1,
                                                                                    row[1][column_number])))
            elif pd.isna(row[1]['order_id']) or row[1]['order_id'] == '':
                result.append((False,
                        'Столбец: %s Cтрока: %s Колонка: `%s` Значение: %s - ТАКОЙ ЗАКАЗ НЕ СУЩЕСТВУЕТ!'%(column_number+1,
                                                                                        row[0]+1,
                                                                                        column_name,
                                                                                        row[1][column_number])))
            else:
                result.append((True,
                        'Столбец: %s Cтрока: %s Колонка: `%s` Значение: %s - ОК!'%(column_number+1,
                                                                row[0]+1,
                                                                column_name,
                                                                row[1][column_number])))
    return result
"""
to_check_df = pd.read_excel(r'to_check\\ЦКП_Доп.Расходы_РКС (Апрель).xlsx',header = None).fillna('')
template_df = pd.read_excel(r'template\\Шаблон.xlsx',header = None).fillna('')
res_list = [x[1] for x in Order_id_check(to_check_df=to_check_df,
                                         column_number=4,
                                         check_type='заказ') ]
print('\n'.join(res_list))
#print(Order_id_check())
"""


def Container_number_check (**kwargs):
    check_name = 'контейнер'
    if kwargs == {}:
        return check_name
    to_check_df,column_number,check_type = kwargs['to_check_df'],kwargs['column_number'],kwargs['check_type']
  
    result = []
    if check_type == check_name:
        column_name = to_check_df[column_number][0]
        container_sql = """
            SELECT 
                container_number
            FROM
                audit._containers_from_cittrans
        """
        container_df = get_df_of_click(container_sql)  
        #print(container_df)

        compare_df = pd.merge(
            to_check_df,
            container_df['container_number'],
            how = 'left',
            left_on = column_number,
            right_on = 'container_number'
        )
        
        #print(compare_df)

        for row in list(compare_df.iterrows())[1:]:
            #print(row[1][column_number])

            if pd.isna(row[1][column_number]) or row[1][column_number] == '': 
                result.append((True,
                                'Столбец: %s Строка: %s Колонка: `%s` - ПОЛЕ НЕ ЗАПОЛНЕНО!'%(column_number+1,
                                                                                           row[0]+1,
                                                                                           column_name,
                                                                                           )))
                    
            elif pd.isna(row[1]['container_number']):
                result.append((False,
                        'Столбец: %s Cтрока: %s Колонока: `%s` Значение: %s - ТАКОЙ КОНТЕЙНЕР НЕ СУЩЕСТВУЕТ!'%(column_number+1,
                                                                                                        column_name,
                                                                                                        row[0]+1,
                                                                                                        row[1][column_number])))
            else:
                result.append((True,
                        'Столбец: %s Строка: %s Колонка: `%s` Значение: %s - ок!'%(column_number+1,
                                                                                row[0]+1,
                                                                                column_name,
                                                                                row[1][column_number])))
    return result
"""
to_check_df = pd.read_excel(r'Проверяем.xlsx',header = None)
template_df = pd.read_excel(r'Шаблон.xlsx',header = None)
res_list = [x[1] for x in Container_number_check(to_check_df,7) if not x[0]]
print('\n'.join(res_list))
"""

def Esu_id_check (**kwargs):
    check_name = 'esu'
    if kwargs == {}:
        return check_name
    to_check_df,column_number,check_type = kwargs['to_check_df'],kwargs['column_number'],kwargs['check_type']
  
    result = []
    if check_type == check_name:
        column_name = to_check_df[column_number][0]
        esu_id_sql = """
                SELECT DISTINCT
                    esu_id
                FROM
                    dict_service_details
        """
        esu_id_df = get_df_of_click(esu_id_sql)
        #print(container_df)

        compare_df = pd.merge(
            to_check_df,
            esu_id_df['esu_id'],
            how = 'left',
            left_on = column_number,
            right_on = 'esu_id'
        )
        
        #print(compare_df)

        for row in list(compare_df.iterrows())[1:]:
            #print(row[1][column_number])

            if pd.isna(row[1][column_number]) or row[1][column_number] == '': 
                result.append((True,
                        'Столбец: %s Строка: %s Колонка: `%s` Значение: %s - ПОЛЕ НЕ ЗАПОЛЕНО!'%(column_number+1,
                                                                                                        column_name,
                                                                                                        row[0]+1,
                                                                                                        row[1][column_number])))
            elif pd.isna(row[1]['esu_id']):
                result.append((False,
                        'Столбец: %s Строка: %s Колонка: `%s` Значение: %s - ТАКОГО ESU_ID НЕ СУЩЕСТВУЕТ!'%(column_number+1,
                                                                                                        row[0]+1,
                                                                                                        column_name,
                                                                                                        row[1][column_number])))
            else:
                result.append((True,
                        'Столбец: %s Строка: %s Колонка: `%s` Значение: %s - ок!'%(column_number+1,
                                                                                row[0]+1,
                                                                                column_name,
                                                                                row[1][column_number])))
    return result
"""
to_check_df = pd.read_excel(r'Проверяем.xlsx',header = None)
template_df = pd.read_excel(r'Шаблон.xlsx',header = None)
res_list = [x[1] for x in Esu_id_check('esu',to_check_df,5) ]
print('\n'.join(res_list))
"""

def Epu_id_check (**kwargs):
    check_name = 'epu'
    if kwargs == {}:
        return check_name
    to_check_df,column_number,check_type = kwargs['to_check_df'],kwargs['column_number'],kwargs['check_type']
  
    result = []
    if check_type == check_name:
        column_name = to_check_df[column_number][0]
        epu_id_sql = """
                SELECT DISTINCT
                    epu_id
                FROM
                    dict_service_details
            """
        epu_id_df = get_df_of_click(epu_id_sql)
        #print(container_df)

        compare_df = pd.merge(
            to_check_df,
            epu_id_df['epu_id'],
            how = 'left',
            left_on = column_number,
            right_on = 'epu_id'
        )
        
        #print(compare_df)

        for row in list(compare_df.iterrows())[1:]:
            #print(row[1][column_number])

            if pd.isna(row[1][column_number]) or row[1][column_number] == '': 
                result.append((True,
                        'Столбец: %s Строка: %s Колонка: `%s` Значение: %s - ПОЛЕ НЕ ЗАПОЛЕНО!'%(column_number+1,
                                                                                                column_name,
                                                                                                row[0]+1,
                                                                                                row[1][column_number])))
            elif pd.isna(row[1]['epu_id']):
                result.append((False,
                        'Столбец: %s Строка: %s Колонка:`%s` Значение: %s - ТАКОГО EPU_ID НЕ СУЩЕСТВУЕТ!'%(column_number+1,
                                                                                            row[0]+1,
                                                                                            column_name,
                                                                                            row[1][column_number])))
            else:
                result.append((True,
                        'Столбец: %s Строка: %s Колонка: `%s` Значение %s - ок!'%(column_number+1,
                                                                            column_name,
                                                                            row[0]+1,
                                                                            row[1][column_number])))
    return result
'''
to_check_df = pd.read_excel(r'to_check\Проверяем.xlsx',header = None).fillna('')
template_df = pd.read_excel(r'template\Шаблон.xlsx',header = None)
print(Epu_id_check('epu',to_check_df,0))
res_list = [x[1] for x in Epu_id_check('epu',to_check_df,0) ]
print('\n'.join(res_list))
'''


def Is_number_check (**kwargs):
    check_name = 'число'
    if kwargs == {}:
        return check_name
    to_check_df,column_number,check_type = kwargs['to_check_df'],kwargs['column_number'],kwargs['check_type']
  
    result = []
    if check_type == check_name:
        column_name = to_check_df[column_number][0]

        compare_se = to_check_df[column_number].apply(lambda x:(x,
                                                                type(x) == type(1) or type(x) == type(1.2)))
        #print(compare_se)

        row_number = 1
        for row in list(compare_se)[1:]:
            row_number += 1
            #print(row)#[1][column_number])
        
            if pd.isna(row[0]) or row[0] == '':
                result.append((True,
                        'Столбец: %s Строка: %s Колонка: `%s` - ПОЛЕ НЕ ЗАПОЛЕНО!'%(column_number+1,
                                                                                row_number,
                                                                                column_name
                                                                                )))
            elif row[1]:
                result.append((True,
                        'Столбец: %s Строка: %s Колонка: `%s` Значение: %s - ок!'%(column_number+1,
                                                                            row_number,
                                                                            column_name,
                                                                            row[0]
                                                                            )))
            else:    
                result.append((False,
                        'Столбец: %s Строка: %s Колонка: `%s` Значение: %s - ЧИСЛОВОЕ ПОЛЕ СОДЕРЖИТ НЕЧИСЛОВОЕ ЗНАЧЕНИЕ!'%(column_number+1,
                                                                                                    row_number,
                                                                                                    column_name,
                                                                                                    row[0])))
    return result
"""
to_check_df = pd.read_excel(r'Проверяем.xlsx',header = None)
template_df = pd.read_excel(r'Шаблон.xlsx',header = None)
res_list = [x[1] for x in Is_number_check('число',to_check_df,1)]
print('\n'.join(res_list))
"""

def Is_integer_check (**kwargs):
    check_name = 'целое'
    if kwargs == {}:
        return check_name
    to_check_df,column_number,check_type = kwargs['to_check_df'],kwargs['column_number'],kwargs['check_type']
  
    result = []
    #print(to_check_df[column_number][0])
    if check_type == check_name:
        column_name = to_check_df[column_number][0]
        compare_se = to_check_df[column_number].apply(lambda x:(x,
                                                                type(x) == type(1)))
        row_number = 1
        for row in list(compare_se)[1:]:
            row_number += 1
            #print(row)#[1][column_number])
        
            if pd.isna(row[0]) or row[0] == '':
                result.append((True,
                        'Столбец: %s Строка: %s Колонка: `%s` - ПОЛЕ НЕ ЗАПОЛЕНО!'%(column_number+1,
                                                                                    row_number,
                                                                                    column_name
                                                                                    )))
            elif row[1]:
                result.append((True,
                        'Столбец: %s Строка: %s Колонка: `%s` Значение: %s - ок!'%(column_number+1,
                                                                                row_number,    
                                                                                column_name,
                                                                                row[0])))
            else:    
                result.append((False,
                        'Столбец: %s Строка: %s Колонка: `%s` Значение: %s - ЗНАЧЕНИЕ ПОЛЯ НЕ ЦЕЛОЕ ЧИСЛО!'%(column_number+1,
                                                                                        row_number,
                                                                                        column_name,
                                                                                        row[0])))

    return result
"""
to_check_df = pd.read_excel(r'Проверяем.xlsx',header = None)
template_df = pd.read_excel(r'Шаблон.xlsx',header = None)
res_list = [x[1] for x in Is_integer_check('целое',to_check_df,8)]
print('\n'.join(res_list))
"""

def Is_date_check (**kwargs):
    check_name = 'дата'
    if kwargs == {}:
        return check_name
    to_check_df,column_number,check_type = kwargs['to_check_df'],kwargs['column_number'],kwargs['check_type']
  
    result = []    
    if check_type == check_name:
        column_name = to_check_df[column_number][0]
        compare_se = to_check_df[column_number].apply(lambda x:(x,str(type(x)) == "<class 'datetime.datetime'>"))
        #print(compare_se)
        row_number = 1
        for row in list(compare_se)[1:]:
            row_number += 1
            #print(row)#[1][column_number])
        
            if pd.isna(row[0]) or row[0] == '':
                result.append((True,
                        'Столбец: %s Строка: %s Колонка: `%s` - ПОЛЕ НЕ ЗАПОЛЕНО!'%(column_number+1,
                                                                                    row_number,
                                                                                    column_name
                                                                                    )))
            elif row[1]:
                result.append((True,
                        'Столбец: %s Строка: %s Колонка: `%s` Значение: %s значение является датой - ок!'%(column_number+1,
                                                                                                        row_number,
                                                                                                        column_name,
                                                                                                        row[0])))
            else:    
                result.append((False,
                        'Столбец: %s Строка: %s Колонка: `%s` Значение: %s - НЕ ЯВЛЯЕТСЯ ДАТОЙ!'%(column_number+1,
                                                                                        row_number,                                                                                          
                                                                                        column_name,
                                                                                        row[0])))

    return result
"""
to_check_df = pd.read_excel(r'Проверяем.xlsx',header = None)
template_df = pd.read_excel(r'Шаблон.xlsx',header = None)
res_list = [x[1] for x in Is_date_check('дата',to_check_df,14)]
print('\n'.join(res_list))
"""