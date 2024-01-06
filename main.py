from utils import *

while True:
    print("""
Выберите операцию
1. Создать счет
2. Пополнить баланс
3. Снять деньги
4. Перевести деньги
5. Проверить баланс
6. Выйти
          """)
    
    choice = input('Выберите операцию: ')
    if choice == '1':
        create_account()
    elif choice == '2':
        deposit()
    elif choice == '3':
        withdraw()
    elif choice == '4':
        transfer()
    elif choice == '5':
        balance()
    elif choice == '6':
        break
    else:
        print("Неверный выбор")
    