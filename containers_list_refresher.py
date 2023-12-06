#import pandas as pd
#import os
#import shutil
#import datetime
import win10toast
 
from tkinter import messagebox
from clickhouse_driver import Client
from datetime import datetime

CLICK_HOST = "rc1a-rgjcum1ijv22bo62.mdb.yandexcloud.net"
CLICK_PORT = 9440
CLICK_DBNAME="history"
CLICK_USER = "cvetkov_d"
CLICK_PWD = "NdKVRepY1eUWq35Tk22d"

sql = """
CREATE OR REPLACE TABLE audit._containers_from_cittrans
ENGINE = Memory()
AS (
SELECT DISTINCT 
	container_number,
	now() AS ceated_at
FROM (
	SELECT 
	    `number`AS container_number
	FROM 
	    dict_container
	UNION DISTINCT
	    SELECT DISTINCT 
	        container_number 
	    FROM 
	        cittrans__container_oper_v3
    )
)
"""
#messagebox.showinfo("containers_list_refresher","стартовало")
start = datetime.now()
connection=Client(host=CLICK_HOST,
                    port = CLICK_PORT,
                    database=CLICK_DBNAME,
                    user=CLICK_USER,
                    password=CLICK_PWD,
                    secure=True,verify=False)

toaster = win10toast.ToastNotifier()
toaster.show_toast('Старт',
                   'Обновение audit._containers_from_cittrans\n%s'%(start.strftime("%x %H:%M:%S")))
print(sql)
print(connection)
connection.execute(sql)
finish = datetime.now()
#toaster = win10toast.ToastNotifier()
toaster.show_toast('Готово',
                   'Обновение audit._containers_from_cittrans\n%s\nОбработка длилась: %s'%(finish.strftime("%x %H:%M:%S"),str(finish-start)[:7]))
