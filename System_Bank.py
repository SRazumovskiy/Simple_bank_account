import random
import string
import sqlite3

conn = sqlite3.connect('first_database.sqlite')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS card (
id INTEGER PRIMARY KEY AUTOINCREMENT, number TEXT NOT NULL, pin TEXT NOT NULL, balance INTEGER DEFAULT 0)''')
conn.commit()

class Bank:

    def counting(self):
        numbers = string.digits
        self.card_num = list('400000' + ''.join(random.choice(numbers) for i in range (9)))
        list_1 = []
        
        for self.n in self.card_num:
            self.a = int(self.n)
            list_1.append(self.a)
        self.even = list_1[1::2]
        self.odd = list_1[0::2]
        list_2 = []
        
        for self.c in self.odd:
            self.e = int(self.c) * 2
            if self.e > 9:
                self.e -= 9
            list_2.append(self.e)
        
        if (sum(list_2) + sum(self.even)) % 10 != 0:
            self.last_digit = str((10 - ((sum(list_2) + sum(self.even)) % 10)))
            self.number = ''.join(self.card_num) + self.last_digit
        else:
            self.number = ''.join(self.card_num) + '0'
        self.pin = ''.join(random.choice(numbers) for i in range(4))

    def luhn_algorithm_test(self, n):
        self.n = list(self.card_digits)
        self.numers_odd = list(self.n[0::2])
        self.numers_even = list(self.n[1::2])
        list_1 = []
        list_2 = []

        for self.numers in self.numers_odd:
            self.nume = int(self.numers) * 2
            if self.nume > 9:
                self.nume -= 9
            list_1.append(self.nume)

        for test_even in self.numers_even:
            self.even = int(test_even)
            list_2.append(self.even)

        return (sum(list_1) + sum(list_2)) % 10 == 0

    def new_account(self):
        print("\nYour card has been created", "Your card is the first one that was created", "Your card number:", sep = '\n')
        self.counting()
        print(f'{self.number}')
        print("Your card PIN:")
        print(f'{self.pin}\n')
        
        cur.execute("INSERT INTO card (number, pin, balance) VALUES (?, ?, ?)", (self.number, self.pin, 0))
        conn.commit()
        
        self.menu()      

    def log_in(self):
        cur.execute("SELECT number, pin FROM card WHERE id =:n ", {"n": 1})
        pos = cur.fetchall()
        print('\nEnter your card number: ')

        self.num = input()
        print('Enter your pin: ')

        self.pasw = input()

        if self.num != pos[0][0] or self.pasw != pos[0][1]:
            print('\nWrong card number or PIN!\n')
            self.menu()

        else:
            print('\nYou have successfully logged in!\n')
            self.account()

    def balance(self):
        cur.execute("SELECT balance FROM card WHERE id =:n ", {"n": 1})
        peas = cur.fetchone() 
        self.money = [*peas]
        self.result = self.money[0]

        print(f'\nBalance: {self.result}\n')
        self.account()

    def close(self):
        print("\nThe account has been closed!\n")
        cur.execute("DELETE FROM card WHERE id =:n", {'n': 1})
        conn.commit()
        self.menu()
            
    def account(self):
        print('''1. Balance
2. Add income
3. Transfer
4. Close account
5. Log out
0. Exit''')
        self.action_2 = input()
        while True:
            if self.action_2 == "1":
                self.balance()

            elif self.action_2 == "2":
                self.add_income()

            elif self.action_2 == "3":
                self.transfer()

            elif self.action_2 == "4":
                self.close()

            elif self.action_2 == "5":
                print("\nLogging out\n")
                
            elif self.action_2 == "0":
                print("\nBye!\n")
            break

    def balance(self):
        cur.execute("SELECT balance FROM card WHERE id = ?", (1,))
        peas = cur.fetchone() 
        self.money = [*peas]
        self.result = self.money[0]
        print(f'\nBalance: {self.result}\n')
        self.account()

    def add_income(self):
        cur.execute("SELECT balance FROM card WHERE id =:n ", {"n": 1})
        peas = cur.fetchone() 
        self.money = [*peas]
        self.result = self.money[0]

        print('\nEnter income: ')
        peas = int(input())
        money = peas + self.result

        cur.execute("UPDATE card SET balance =:m WHERE id =:n ", {'n': 1, 'm': money})
        conn.commit()
        print("\nSuccessfully added!\n")
        self.account()

    def transfer(self):
        cur.execute("SELECT balance FROM card WHERE id =:n ", {"n": 1})
        peas = cur.fetchone() 
        self.money = [*peas]
        self.result = self.money[0]

        cur.execute("SELECT number FROM card WHERE id =:n ", {"n": 1})
        num = cur.fetchone()
        n = num[0]
        
        print("\nTransfer", "\nEnter card number:")
        self.card_digits = input()

        if self.luhn_algorithm_test(self.card_digits) is True:
            cur.execute("SELECT COUNT (1) FROM card WHERE number =:n ", {'n': self.card_digits})
            a = cur.fetchone()
            b = [*a]
            if 0 in b:
                print("\nSuch a card does not exist.\n")
                self.account()
            
            elif self.card_digits == n:
                print("\nYou can't transfer money to the same account!\n")
                self.account()
            
            else:
                print("\nEnter how much money you want to transfer:")
                self.receiver = input()
                self.receive = int(self.receiver)

                if self.receive <= self.result:
                    print("\nSuccess!\n")

                    peas_1 = self.result - self.receive
                    peas_2 = self.receive

                    cur.execute("UPDATE card SET balance =:m WHERE id =:n ", {'n': 1, 'm': peas_1})
                    conn.commit()

                    cur.execute("UPDATE card SET balance =:m WHERE number =:n", {'n': self.card_digits, 'm': peas_2})
                    conn.commit()

                    self.account()
            
                elif self.receive > self.result:
                    print("\nNot enough money\n")
                    self.account()                    

        else:
            print("\nProbably you made mistake in the card number. Please try again!\n")
            self.account()

    def menu(self):
        print(f'''1. Create an account
2. Log into account
0. Exit''')
        self.action = input()
        
        while True:
            if self.action == str(1):
                self.new_account()
                
            elif self.action == str(2):
                self.log_in()
                
            elif self.action == str(0):
                print('\nBye!\n')
                
            break

user = Bank()
user.menu()