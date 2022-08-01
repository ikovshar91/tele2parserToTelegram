from pyrogram import Client
import pandas as pd
import warnings
import os
import pyodbc

app = Client("my_account")
homedir = os.path.expanduser('~')

con_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};' \
             f'DBQ={homedir}\\Desktop\\telegram\\1234.accdb;'

conn = pyodbc.connect(con_string)
cursor = conn.cursor()
print("Connected To Database")

query = 'SELECT * FROM telegram'
warnings.simplefilter("ignore")

def fxn():
    warnings.warn("deprecated", DeprecationWarning)


@app.on_message()
async def my_handler(client, message):
    #print(message.chat.id) ## Проверить id - чата
    if message.chat.id == 2115225854:
        index = pd.read_sql('SELECT MAX(code) from telegram', conn)
        td = {'Код': index,'Дата': str(message.date), 'Имя': str(message.from_user.first_name), 'Сообщение' : str(message.text)}
        warnings.simplefilter("ignore")

        max_index = int(index['Expr1000'])
        sql = 'INSERT INTO telegram ("code","date_","name_","text_") VALUES (?,?,?,?)'
        cursor.execute(sql, (max_index+1, str(message.date), str(message.from_user.first_name), str(message.text)))
        conn.commit()
        print(f'Data inserted: {td}')

app.run()