import sqlite3


conn = sqlite3.connect('banking.db')
cursor = conn.cursor()

##DELETED CODE THAT CREATE THE ACCOUNT DATABASE SINCE IT ONLY NEEDS TO BE CREATED ONCE
cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT,
        balance REAL
    )
''')
conn.commit()

def username_exists(username):
    cursor.execute("SELECT * FROM accounts WHERE username = ?", (username,))
    return cursor.fetchone() is not None


def password_matches(username, password):
    cursor.execute("SELECT * FROM accounts WHERE username = ?", (username,))
    account = cursor.fetchone()
    if account is not None:
        return account[2] == password
    return False

while True:
    logged_in = False
    current_user = None


    while logged_in == False:
        choice = ''
        while choice != "create" and choice != "sign in":
            choice = input("Would you like to create a new account, sign in to an existing account, or exit the program? ")
            if choice.lower() == "create":
                while logged_in == False:
                    print("Creating a new account...")
                    new_username = input("Enter a username: ")
                    if not username_exists(new_username):
                        new_password = input("Enter a password: ")
                        if len(new_username) < 5:
                            print("Username must be at least 5 characters long. Please try again.")
                            continue
                        if len(new_password) < 8:
                            print("Password must be at least 8 characters long. Please try again.")
                            continue
                        cursor.execute("INSERT INTO accounts (username, password, balance) VALUES (?, ?, 0.0)", (new_username, new_password))
                        conn.commit()
                        print("Account created successfully.")
                        logged_in = True
                        current_user = new_username
                        break
                    else:
                        print("Username already exists. Please choose a different username.")  
            elif choice.lower() == "sign in":
                while logged_in == False:
                    print("Signing in to an existing account...")
                    username = input("Enter your username: ")
                    password = input("Enter your password: ")
                    if password_matches(username, password):
                        print("Password matches! You are now signed in.")
                        logged_in = True
                        current_user = username
                        break
                    else:
                        print("Incorrect password. Please try again.")
                        break
            if choice.lower() == "exit":
                print("Exiting the program...")
                conn.close()
                exit()

            # Code to sign in would go here


    while logged_in:
        print(f"\n--- {current_user}'s Dashboard ---")
        step1 = input("What would you like to do? (deposit, withdraw, check balance, delete account, change password, check all accounts, or sign out) ")
        if step1.lower() == "check balance":
            cursor.execute("SELECT balance FROM accounts WHERE username = ?", (current_user,))
            balance = cursor.fetchone()[0]
            print(f"Your current balance is: ${balance:.2f}")
        elif step1.lower() == "deposit":
            amount = float(input("Enter the amount to deposit: "))
            if amount != int:
                print("Please enter a number ")
            cursor.execute("UPDATE accounts SET balance = balance + ? WHERE username = ?", (amount, current_user))
            conn.commit()
            print(f"Deposited ${amount:.2f} successfully.")
        elif step1.lower() == "withdraw":
            amount = float(input("Enter the amount to withdraw: "))
            cursor.execute("SELECT balance FROM accounts WHERE username = ?", (current_user,))
            balance = cursor.fetchone()[0]
            if amount > balance:
                print("Insufficient funds. Withdrawal failed.")
            elif amount != int:
                print("Please enter a number ")
            else:
                cursor.execute("UPDATE accounts SET balance = balance - ? WHERE username = ?", (amount, current_user))
                conn.commit()
                print(f"Withdrew ${amount:.2f} successfully.")
        elif step1.lower() == "sign out":
            print("Signing out...")
            logged_in = False
        elif step1.lower() == "delete account":
            confirm = input("Are you sure you want to delete your account? This action cannot be undone. (yes/no) ")
            if confirm.lower() == "yes":
                cursor.execute("DELETE FROM accounts WHERE username = ?", (current_user,))
                conn.commit()
                print("Account deleted successfully.")
                logged_in = False
            else:
                print("Account deletion cancelled.")
        elif step1.lower() == "change password":
            new_password = input("Enter your new password: ")
            if len(new_password) < 8:
                print("Password must be at least 8 characters long. Please try again.")
            else:
                cursor.execute("UPDATE accounts SET password = ? WHERE username = ?", (new_password, current_user))
                conn.commit()
                print("Password changed successfully.")
        elif step1.lower() == "check all accounts":
            cursor.execute("SELECT username, balance FROM accounts")
            accounts = cursor.fetchall()
            print("All accounts:")
            for account in accounts:
                print(f"  Username: {account[0]}, Balance: ${account[1]:.2f}")
        else:
            print("Invalid choice. Please enter 'deposit', 'withdraw', 'check balance', or 'sign out'.")

    conn.close()
