import random as random
import sqlite3


class CardGenerator:
    IIN = 400000

    def __init__(self):
        self.pin = str(random.sample([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 4)).strip("[]").replace(',', '').replace(' ', '')
        self.card_number = str(CardGenerator.luhn_algorithm(self)).strip("[]").replace(',', '').replace(' ', '')
        self.balance = 0
    def luhn_algorithm(self):
        card = [4, 0, 0, 0, 0, 0] + random.sample([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 9)
        temp = card.copy()
        index = 0
        for digit in temp:
            if (index + 1) % 2 != 0:
                temp[index] = digit * 2
            index += 1
        index = 0
        for digit in temp:
            if digit > 9:
                temp[index] = digit - 9
            index += 1
        total = sum(temp)
        card.append((total * 9) % 10)
        return card

    def get_card_number(self):
        return self.card_number

    def get_pin(self):
        return self.pin


class Bank:
    def __init__(self):
        self.Accounts = []
        self.Accounts_details = {}
        self.conn = sqlite3.connect('card.s3db')
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS card(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number TEXT NOT NULL,
            pin TEXT NOT NULL,
            balance INTEGER DEFAULT 0
            );
            ''')
        self.conn.commit()

    def run(self):
        while True:
            choice = input('1. Create an account \n2. Log into account\n0. Exit\n')
            if choice == '1':
                Bank.create_account(self)
            elif choice == '2':
                card = input('Enter your card number:\n')
                pin = input('Enter your PIN:\n')
                if Bank.check_account(self, card, pin):
                    print('You have successfully logged in!')
                    Bank.login(self, card)
                else:
                    print('Wrong card number or PIN!')
            else:
                print('Bye!')
                exit()

    def check_account(self, card_number, pin):
        self.cur.execute('SELECT * FROM card')
        bank_data = self.cur.fetchall()

        for a in bank_data:
            if a[1] == card_number:
                if a[2] == pin:
                    return True
                else:
                    return False

    def create_account(self):
        a = CardGenerator()
        self.cur.execute(f"INSERT INTO card(number, pin, balance) VALUES({a.get_card_number()}, {a.get_pin()}, {a.balance})")
        self.conn.commit()
        print('Your card number:')
        print(a.get_card_number() + '\n')
        print('Your card PIN:')
        print(a.get_pin() + '\n')

    def login(self, card_number):
        self.cur.execute(f'SELECT * FROM card WHERE number = {card_number}')
        card = self.cur.fetchall()
        while True:
            choice = input('''
            1. Balance
            2. Add income
            3. Do transfer
            4. Close account
            5. Log out
            0. Exit
            ''')
            if choice == '1':
                Bank.checkbal(self, card_number)
            elif choice == '2':
                income = int(input('Enter income:\n'))
                Bank.addmoney(self, card_number, income)
                self.conn.commit()
                print("Income was added!")
            elif choice == '3':
                transfercard = input('Transfer\nEnter card number:\n')
                Bank.transfer(self, card_number, transfercard)
                self.conn.commit()
            elif choice == '4':
                Bank.close(self, card_number)
                print('The account has been closed!')
                self.conn.commit()
                break
            elif choice == '5':
                print('You have successfully logged out!')
                break
            else:
                print('Bye!')
                exit()
    def checkbal(self, card_number):
        current_bal = self.cur.execute(f'SELECT balance FROM card WHERE number = {card_number}').fetchone()
        print(f'Balance: {current_bal[0]}')

    def addmoney(self, card_number, income):
        current_bal = self.cur.execute(f'SELECT balance FROM card WHERE number = {card_number}').fetchone()
        updated_bal = current_bal[0] + income
        self.cur.execute(f'UPDATE card SET balance = {updated_bal} WHERE number = {card_number}')


    def transfer(self, card_number, transfercard):
        if (card_number == transfercard):
            print("You can't transfer money to the same account!")
            return
        else:
            card = self.cur.execute('SELECT number FROM card;').fetchall()
            current_bal = self.cur.execute(f'SELECT balance FROM card WHERE number = {card_number}').fetchone()
            checksum = int(transfercard[-1])
            forsum = 0
            for i in range(len(transfercard) - 1):
                digit = int(transfercard[i])
                if (i % 2 == 0):
                    digit = 2 * digit
                if digit > 9:
                    digit = digit - 9
                forsum = forsum + digit

            if (forsum + checksum)% 10 != 0 :
                print("Probably you made a mistake in the card number. Please try again!")
            else:
                listofcard = []
                for i in card:
                    listofcard.append(i[0])
                if transfercard in listofcard:
                    transferamount = int(input('Enter how much money you want to transfer:\n'))
                    if transferamount > current_bal[0]:
                        print('Not enough money!')
                    else:
                        updated_bal = current_bal[0] - transferamount
                        current_bal2 = self.cur.execute(f'SELECT balance FROM card WHERE number = {transfercard}').fetchone()
                        updated_bal2 = current_bal2[0] + transferamount
                        self.cur.execute(f'UPDATE card SET balance = {updated_bal} WHERE number = {card_number}')
                        self.cur.execute(f'UPDATE card SET balance = {updated_bal2} WHERE number = {transfercard}')

                        print("Success!")
                else:
                    print("Such a card does not exist.")



    def close(self, card_number):
        self.cur.execute(f'DELETE FROM card WHERE number = {card_number};')



B = Bank()
B.run()
