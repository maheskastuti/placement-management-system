import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Stuti16@PATNA",
    database="placement_management"
)

cursor = conn.cursor()

def add_students():
    while True:
        name = input("Enter Name: ")
        email = input("Enter Email: ")
        branch = input("Enter Branch: ")
        cgpa = float(input("Enter CGPA: "))

        query = """
        INSERT INTO students
        (name,email,branch,cgpa)
        VALUES(%s,%s,%s,%s)
        """

        values = (name, email, branch, cgpa)

        cursor.execute(query, values)

        conn.commit()

        choice = input("Add another student ? (y/n): ")

        if choice.lower() != 'y':
            break

    print("Student Added Successfully")

def view_students():

    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def update_student():

    student_id = int(input("Enter student id: "))
    new_cgpa = float(input("Enter new CGPA: "))

    query = """
    UPDATE students
    SET cgpa = %s
    WHERE student_id = %s
    """

    values = new_cgpa, student_id

    cursor.execute(query, values)

    conn.commit()

    if cursor.rowcount > 0:
       print("Student updated successfully")
    else:
       print("No student found with that ID")

def delete_student():

    student_id = int(input("Enter student id: "))

    query = """
    DELETE FROM students
    WHERE student_id = %s
    """

    values = (student_id,)

    cursor.execute(query, values)

    conn.commit()

    if cursor.rowcount > 0:
       print("Student deleted successfully")
    else:
       print("No student found with that ID")

def add_companies():

    while True:
        company_name = input("Enter name: ")
        package_lpa = float(input("Enter package: "))
        min_cgpa = float(input("Enter minimum cgpa: "))

        query = """
        INSERT INTO companies
        (company_name,package_lpa,min_cgpa)
        VALUES(%s,%s,%s)
        """

        values = (company_name, package_lpa, min_cgpa)

        cursor.execute(query, values)

        conn.commit()

        choice = input("Enter another company ? (y,n) ")
        if choice.lower() != 'y':
            break

    print("company added successfully")

def view_companies():

    cursor.execute("SELECT * FROM companies")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def update_company():

    company_id = int(input("Enter company_id: "))
    new_package_lpa = float(input("Enter new package: "))
    new_min_cgpa = float(input("Enter new min_cgpa: "))

    query = """
    UPDATE companies
    SET package_lpa = %s,
        min_cgpa = %s
    WHERE company_id = %s
    """

    values = (new_package_lpa,new_min_cgpa,company_id)

    cursor.execute(query,values)

    conn.commit()

    if cursor.rowcount>0:
        print("company updated successfully")
    else:
        print("no company with such id")

def delete_company():

    company_id = int(input("Enter company_id: "))

    query = """
    DELETE FROM companies
    WHERE company_id = %s
    """

    values = (company_id,)

    cursor.execute(query,values)

    conn.commit()

    if cursor.rowcount>0:
        print("company deleted successfully")
    else:
        print("company not found")

def add_jobs():

    while True:
        company_id = int(input("Enter company_id: "))

        check_query = """
        SELECT * FROM companies
        WHERE company_id = %s
        """

        cursor.execute(check_query, (company_id,))

        company = cursor.fetchone()

        if company is None:
            print("Company ID not found")
            continue

        role = input("Enter role: ")
        location = input("Enter location: ")

        query = """
        INSERT INTO jobs
        (company_id,role,location)
        VALUES(%s,%s,%s)
        """

        values = (company_id,role,location)

        cursor.execute(query,values)

        conn.commit()

        choice = input("Add another job ? (y/n)")
        if choice.lower() != 'y':
            break

    print("Job added successfully")

def view_jobs():

    query = """
    SELECT jobs.job_id,
           companies.company_name,
           jobs.role,
           jobs.location
    FROM jobs
    JOIN companies
    ON jobs.company_id = companies.company_id
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def update_job():

    job_id = int(input("Enter job id: "))
    new_location = input("enter new location: ")

    query = """
    UPDATE jobs
    SET location = %s
    WHERE job_id = %s
    """

    values = (new_location,job_id)

    cursor.execute(query,values)

    conn.commit()

    if cursor.rowcount > 0:
        print("Job updated successfully")
    else:
        print("Job_id not found")

def delete_job():

    job_id = int(input("Enter job_id: "))

    query = """
    DELETE FROM jobs
    WHERE job_id = %s
    """

    values = (job_id,)

    cursor.execute(query,values)

    conn.commit()

    if cursor.rowcount > 0:
        print("Job deleted successfully")
    else:
        print("Job_id not found")

def apply_job():

    while True:

        student_id = int(input("Enter student_id: "))

        cursor.execute(
            "SELECT * FROM students WHERE student_id = %s",
            (student_id,)
        )

        student = cursor.fetchone()

        if student is None:
            print("Student not found")
            continue

        job_id = int(input("Enter job_id: "))

        cursor.execute(
            "SELECT * FROM jobs WHERE job_id = %s",
            (job_id,)
        )

        job = cursor.fetchone()

        if job is None:
            print("Job not found")
            continue

        query = """
        INSERT INTO applications(student_id,job_id)
        VALUES(%s,%s)
        """

        values = (student_id,job_id)

        cursor.execute(query,values)

        conn.commit()

        choice = input("Add another application ? (y/n)")
        if choice.lower() != 'y':
            break

    print("Applied successfully")

def view_applications():

    query = """
    SELECT applications.application_id,
           students.name,
           companies.company_name,
           jobs.role,
           applications.status
    FROM applications 
    JOIN students
    On applications.student_id = students.student_id
    JOIN jobs
    On applications.job_id = jobs.job_id
    JOIN companies
    On jobs.company_id = companies.company_id
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def update_application_status():

    application_id = int(input("Enter application id: "))
    new_status = input("Enter new status: ")

    query = """
    UPDATE applications
    SET status = %s
    WHERE application_id = %s
    """

    values = (new_status,application_id)

    cursor.execute(query,values)

    conn.commit()

    if cursor.rowcount > 0:
        print("Application status updated successfully")
    else:
        print("Application not found")

while True:

    print("\n-----Placement Management System-----")
    print("1. Add Students")
    print("2. View Students")
    print("3. Update Student")
    print("4. Delete Student")
    print("5. Add companies")
    print("6. View companies")
    print("7. Update company")
    print("8. Delete company")
    print("9. Add jobs")
    print("10. View jobs")
    print("11. Update job")
    print("12. Delete job")
    print("13. Apply_job")
    print("14. View_applications")
    print("15. Update application status")
    print("16. Exit")

    choice = int(input("Enter choice: "))

    if choice == 1:
        add_students()

    elif choice == 2:
        view_students()

    elif choice == 3:
        update_student()

    elif choice == 4:
        delete_student()

    elif choice == 5:
        add_companies()

    elif choice == 6:
        view_companies()

    elif choice == 7:
        update_company()

    elif choice == 8:
        delete_company()

    elif choice == 9:
        add_jobs()

    elif choice == 10:
        view_jobs()

    elif choice == 11:
        update_job()

    elif choice == 12:
        delete_job()

    elif choice == 13:
        apply_job()

    elif choice == 14:
        view_applications()

    elif choice == 15:
        update_application_status()

    elif choice == 16:
        print("Thankyou!")
        break;
 
    else:
        print("Invalid choice")