import sqlite3

conn = sqlite3.connect('contact_book.db')
cursor = conn.cursor()


def list_items(items: list):
    for item in items:
        print('name-> {} \t phone-> {} \t email-> {} \t address-> {}'.format(
            item[0], item[1], item[2], item[3]))
    print('\n')


def show_all():
    SQL = """SELECT * FROM contacts"""
    cursor.execute(SQL)
    print('\n')
    list_items(cursor.fetchall())


def search():
    operation = '\nSearch by:\n1) name 2) number\n>>> '
    usr_inp = int(input(operation))
    if usr_inp == 1:
        val = input('type full name/chunks of the name: ')
        SQL = "SELECT * FROM contacts WHERE Name LIKE '%"+val+"%'"
        cursor.execute(SQL)
        list_items(cursor.fetchall())
    elif usr_inp == 2:
        val = input('type full number/chunks of the number): ')
        SQL = "SELECT * FROM contacts WHERE Phone LIKE '%"+val+"%'"
        cursor.execute(SQL)
        list_items(cursor.fetchall())
    else:
        print('wrong input\n')


def get_credentials() -> '(name,phone,email,address)':
    while True:
        name = str(input('Name: '))
        while True:
            number = int(input('phone: '))
            if len(str(number)) == 10:
                break
            else:
                print('wrong number, try again: ')

        email = str(input('email: '))
        while True:
            address = str(input('address: '))
            if len(address) == 0:
                break
            elif len(address) > 10:
                break
            else:
                print('too short, try again: ')
        print('\nname: {}, phone: {}, email: {}, address: {}\n'.format(
            name, number, email, address))
        while True:
            confirm = input('conform(y/n): ')
            if confirm == 'y' or confirm == 'Y':
                return name, number, email, address
            elif confirm == 'n' or confirm == 'N':
                print('not saved\n')
                break
            else:
                print('invalid input, try again')
        break


def save():
    details = get_credentials()
    SQL = """INSERT INTO contacts(Name,Phone,email,Address) VALUES (?,?,?,?)"""
    cursor.execute(SQL, details)
    conn.commit()
    print("saved !\n")


def update():
    usr_inp = input('\nwhom you want to update: ')
    SQL = "SELECT Name FROM contacts WHERE Name == '"+usr_inp+"'"
    cursor.execute(SQL)
    result = cursor.fetchall()
    if result:
        details = get_credentials()
        SQL = """UPDATE contacts
        SET
        Name = ?,
        Phone = ?,
        email = ?,
        Address = ?
        WHERE Name ='"""+usr_inp+"'"
        cursor.execute(SQL, details)
        conn.commit()
        print('updated!\n')
    else:
        print('name not present\n')


def delete():
    usr_inp = input('give the name to delete it: ')
    SQL = "SELECT Name FROM contacts WHERE Name == '"+usr_inp+"'"
    cursor.execute(SQL)
    result = cursor.fetchall()
    if result:
        SQL = "DELETE FROM contacts WHERE Name == '"+usr_inp+"'"
        cursor.execute(SQL)
        conn.commit()
        print('Deleted!\n')
    else:
        print('There is no "%s" in contact\n' % usr_inp)


def commands() -> '1)show 2)search 3)save 4)update 5)delete':
    print('choose from the options:')
    operation = '1) Show all contacts\n2) Search\n3) Save\n4) Update\n5) Delete\n>>> '
    while True:
        usr_inp = int(input(operation))
        if usr_inp == 1:
            show_all()
        elif usr_inp == 2:
            search()
        elif usr_inp == 3:
            save()
        elif usr_inp == 4:
            update()
        elif usr_inp == 5:
            delete()
        else:
            print('\nwrong input, try again')



print("""
+-+-+-+-+-+-+-+ +-+-+-+-+
|c|o|n|t|a|c|t| |b|o|o|k|
+-+-+-+-+-+-+-+ +-+-+-+-+""")

while True:
    commands()
    conn.close()
