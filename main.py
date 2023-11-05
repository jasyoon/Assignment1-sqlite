import csv
import sqlite3

conn = sqlite3.connect('/Users/jyoon/Documents/CPSC 408/Assignment1.db')
mycursor = conn.cursor()

def import_data():
    with open('/Users/jyoon/Documents/CPSC 408/students.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        mycursor.execute(f'CREATE TABLE IF NOT EXISTS Student(StudentId INTEGER PRIMARY KEY,'
                            'FirstName TEXT,'
                            'LastName TEXT,'
                            'GPA REAL,'
                            'Major TEXT,'
                            'FacultyAdvisor TEXT DEFAULT NULL,'
                            'Address TEXT,'
                            'City TEXT,'
                            'State TEXT,'
                            'ZipCode TEXT,'
                            'MobilePhoneNumber TEXT,'
                            'isDeleted INTEGER DEFAULT 0);')

        for column in reader:
            values = (column['FirstName'], column['LastName'], column['GPA'], column['Major'], column['Address'], column['City'], column['State'], column['ZipCode'], column['MobilePhoneNumber'])
            mycursor.execute(f'INSERT INTO Student(FirstName, LastName, GPA, Major, Address, City, State, ZipCode, MobilePhoneNumber) VALUES(?,?,?,?,?,?,?,?,?)', values)

            conn.commit()

def display_all_students():
    mycursor.execute(f'SELECT * FROM Student')
    students = mycursor.fetchall()

    for student in students:
        if student[11] != 1:
            print("Student ID:", student[0])
            print("First Name:", student[1])
            print("Last Name:", student[2])
            print("GPA:", student[3])
            print("Major:", student[4])
            print("Faculty Advisor:", student[5])
            print("Address:", student[6])
            print("City:", student[7])
            print("State:", student[8])
            print("ZipCode:", student[9])
            print("Mobile Phone Number:", student[10])
            print()

def add_new_student(fname, lname, gpa, major, advisor, address, city, state, zipcode, phone):
    mycursor.execute(f'INSERT INTO Student (FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (fname, lname, gpa, major, advisor, address, city, state, zipcode, phone))
    conn.commit()

def update_student(sid, major, advisor, phone):
    mycursor.execute(f'UPDATE Student SET Major = ?, FacultyAdvisor = ?, MobilePhoneNumber = ? WHERE StudentId = ?',
                     (major, advisor, phone, sid))
    conn.commit()
def delete_student(sid):
    mycursor.execute(f'UPDATE Student SET isDeleted = 1 WHERE StudentId = ?', (sid,))
    conn.commit()

def search_student(major, gpa, city, state, advisor):
    query = f'SELECT * FROM Student WHERE 1=1'

    values = []

    if major != 'N/A':
        query += " AND Major = ?"
        values.append(major)
    if gpa != 'N/A':
        query += " AND GPA = ?"
        values.append(float(gpa))
    if city != 'N/A':
        query += " AND City = ?"
        values.append(city)
    if state != 'N/A':
        query += " AND State = ?"
        values.append(state)
    if advisor != 'N/A':
        query += " AND FacultyAdvisor = ?"
        values.append(advisor)

    mycursor.execute(query, values)
    students = mycursor.fetchall()

    if not students:
        print("No students found matching the criteria.")
    else:
        print("Here are the students who fall under your search queries. ")
        print("")
        for student in students:
            if student[11] != 1:
                print("Student ID:", student[0])
                print("First Name:", student[1])
                print("Last Name:", student[2])
                print("GPA:", student[3])
                print("Major:", student[4])
                print("Faculty Advisor:", student[5])
                print("Address:", student[6])
                print("City:", student[7])
                print("State:", student[8])
                print("ZipCode:", student[9])
                print("Mobile Phone Number:", student[10])
                print()

def choice_two():
    fname = input("Enter first name: ")
    lname = input("Enter last name: ")
    gpa = input("Enter GPA: ")
    try:
        gpa = float(gpa)  # Validate GPA as a float
    except ValueError:
        print("Invalid GPA. Please enter a valid numeric value for GPA.")
        return
    major = input("Enter major: ")
    advisor = input("Enter faculty advisor: ")
    address = input("Enter address: ")
    city = input("Enter city: ")
    state = input("Enter state: ")
    zipcode = input("Enter zipcode: ")
    try:
        zipcode = int(zipcode)
    except ValueError:
        print("Invalid zipcode. Please enter a valid numeric value for the zipcode.")
    phone = input("Enter mobile phone number: ")

    add_new_student(fname, lname, gpa, major, advisor, address, city, state, zipcode, phone)

def choice_three():
    sid = input("Enter the Student ID to update: ")
    try:
        sid = int(sid)
    except ValueError:
        print("Invalid Student ID. Please enter a valid numeric value.")
        return
    major = input("Enter new major: ")
    advisor = input("Enter new faculty advisor: ")
    phone = input("Enter new mobile phone number: ")
    update_student(sid, major, advisor, phone)

def choice_four():
    sid = input("Enter the Student ID to delete: ")
    try:
        sid = int(sid)
    except ValueError:
        print("Invalid Student ID. Please enter a valid numeric value.")
        return
    delete_student(sid)

def choice_five():
    major = input("Enter major (or 'N/A' to skip): ")
    gpa = input("Enter GPA (or 'N/A' to skip): ")
    try:
        gpa = float(gpa)  # Validate GPA as a float
    except ValueError:
        print("Invalid GPA. Please enter a valid numeric value for GPA.")
        return
    city = input("Enter city (or 'N/A' to skip): ")
    state = input("Enter state (or 'N/A' to skip): ")
    advisor = input("Enter faculty advisor (or 'N/A' to skip): ")
    search_student(major, gpa, city, state, advisor)
def menu():
    while True:
        print("Welcome to the Student Database")
        print("Below are the possible functions with their option number:")
        print("1. Display All Students")
        print("2. Add New Student")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Search Students")
        print("6. Exit")

        choice = input("Enter your desired option number: ")

        if choice == '1':
            display_all_students()
        elif choice == '2':
            choice_two()
        elif choice == '3':
            choice_three()
        elif choice == '4':
            choice_four()
        elif choice == '5':
            choice_five()
        elif choice == '6':
            print("Exiting the application.")
            break
        else:
            print("Invalid option. Please choose a valid option (1-6).")


import_data()

menu()
mycursor.close()


