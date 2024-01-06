import psycopg2
import os
from dotenv import load_dotenv
from random import randint
load_dotenv()
conn_params = {
    'dbname' : os.getenv('dbname'),
    'user' : os.getenv('user'),
    'password' : os.getenv('password'),
    'host' : os.getenv('host'), 
    'port' : os.getenv('port')
}

conn = psycopg2.connect(**conn_params)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS clients(
               client_id SERIAL PRIMARY KEY,
               firstname VARCHAR(50),
               lasttname VARCHAR(50),
               middlename VARCHAR(50),
               account_number BIGINT UNIQUE
);
               """)

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
               transaction_id SERIAL PRIMARY KEY,
               account_number BIGINT,
               amount NUMERIC,  
               type VARCHAR(50),
               FOREIGN KEY (account_number) REFERENCES clients(account_number)
);
               """)
conn.commit()

def create_account():
    try:
        firstname = input('Введите имя: ')
        lastname = input('Введите фамилию: ')
        middlename = input('Введите отчество: ')
        account_number = 11800000000 + randint(0, 99999999)

        cursor.execute(f"""INSERT INTO clients (firstname, lasttname, middlename, account_number) VALUES ('{firstname}', '{lastname}', '{middlename}', {account_number})
                    """)
        conn.commit()
        print(f"Счет создан. Номер счета: {account_number}")
    except Exception as e:
        print(f"Ошибка! аккаунт не был создан: {e}")

def deposit():
    try:
        account_number = int(input(f'Введите номер счета: '))
        amount = float(input("Введите сумму пополнения: "))
        cursor.execute(f"""INSERT INTO transactions (account_number, amount, type)
                    VALUES ({account_number}, {amount}, 'deposit')""")
        conn.commit()
        print("Счет пополнен.")
    except Exception as e:
            print(f"Ошибка! счет не был пополнен: {e}")


def check_balance(amount, account_number):
    cursor.execute(f"SELECT sum(amount) FROM transactions WHERE account_number = {account_number}")
    balance = cursor.fetchall()[0][0]
    return balance >= amount


def withdraw():
    account_number = int(input(f'Введите номер счета: '))
    amount = float(input("Введите сумму пополнения: "))
    if check_balance(amount, account_number):
        cursor.execute(f"""INSERT INTO transactions (account_number, amount, type)
                    VALUES ({account_number}, {-amount}, 'deposit')""")
        conn.commit()
    else:
        print("Не достаточно денег на балансе")

def transfer():
    from_acc = int(input(f'Введите номер вашего счета: '))
    to_acc = int(input(f'Введите номер счета получателя: '))
    amount = float(input("Введите сумму пополнения: "))

    if check_balance(amount, from_acc):
        cursor.execute(f"""INSERT INTO transactions (account_number, amount, type)
                    VALUES ({from_acc}, {-amount}, 'transfer out')""")
        cursor.execute(f"""INSERT INTO transactions (account_number, amount, type)
                    VALUES ({to_acc}, {amount}, 'transfer in')""")
        conn.commit()
        print("Перевод выполнен")
    else:
        print("Не достаточно денег на балансе")

def balance():
    account_number = int(input(f'Введите номер счета: '))
    cursor.execute(f"SELECT sum(amount) FROM transactions WHERE account_number = {account_number}")
    balance = cursor.fetchall()[0][0]
    print(balance)
