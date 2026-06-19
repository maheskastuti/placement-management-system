import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD",
    database="placement_management"
)

cursor = conn.cursor()


#  HELPER FUNCTIONS


def get_int(prompt):
    """Keep asking until user enters a valid integer."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid number.")

def get_float(prompt):
    """Keep asking until user enters a valid float."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")

def print_separator():
    print("-" * 45)


#  STUDENTS


def add_students():
    while True:
        name   = input("Enter Name   : ")
        email  = input("Enter Email  : ")
        branch = input("Enter Branch : ")
        cgpa   = get_float("Enter CGPA   : ")

        query = """
        INSERT INTO students (name, email, branch, cgpa)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (name, email, branch, cgpa))
        conn.commit()

        choice = input("Add another student? (y/n): ")
        if choice.lower() != 'y':
            break

    print("Student(s) added successfully.")

def view_students():
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    print_separator()
    print(f"{'ID':<5} {'Name':<15} {'Email':<25} {'Branch':<10} {'CGPA'}")
    print_separator()
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<15} {row[2]:<25} {row[3]:<10} {row[4]}")
    print_separator()

def update_student():
    student_id = get_int("Enter student ID : ")
    new_cgpa   = get_float("Enter new CGPA   : ")

    cursor.execute("UPDATE students SET cgpa = %s WHERE student_id = %s",
                   (new_cgpa, student_id))
    conn.commit()

    if cursor.rowcount > 0:
        print("Student updated successfully.")
    else:
        print("No student found with that ID.")

def delete_student():
    student_id = get_int("Enter student ID: ")

    cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
    conn.commit()

    if cursor.rowcount > 0:
        print("Student deleted successfully.")
    else:
        print("No student found with that ID.")


#  COMPANIES


def add_companies():
    while True:
        company_name = input("Enter Company Name  : ")
        package_lpa  = get_float("Enter Package (LPA) : ")
        min_cgpa     = get_float("Enter Minimum CGPA  : ")

        cursor.execute(
            "INSERT INTO companies (company_name, package_lpa, min_cgpa) VALUES (%s, %s, %s)",
            (company_name, package_lpa, min_cgpa)
        )
        conn.commit()

        choice = input("Add another company? (y/n): ")
        if choice.lower() != 'y':
            break

    print("Company(s) added successfully.")

def view_companies():
    cursor.execute("SELECT * FROM companies")
    rows = cursor.fetchall()
    print_separator()
    print(f"{'ID':<5} {'Company':<20} {'Package(LPA)':<15} {'Min CGPA'}")
    print_separator()
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<20} {row[2]:<15} {row[3]}")
    print_separator()

def update_company():
    company_id      = get_int("Enter company ID    : ")
    new_package_lpa = get_float("Enter new package   : ")
    new_min_cgpa    = get_float("Enter new min CGPA  : ")

    cursor.execute(
        "UPDATE companies SET package_lpa = %s, min_cgpa = %s WHERE company_id = %s",
        (new_package_lpa, new_min_cgpa, company_id)
    )
    conn.commit()

    if cursor.rowcount > 0:
        print("Company updated successfully.")
    else:
        print("Company not found.")

def delete_company():
    company_id = get_int("Enter company ID: ")

    cursor.execute("DELETE FROM companies WHERE company_id = %s", (company_id,))
    conn.commit()

    if cursor.rowcount > 0:
        print("Company deleted successfully.")
    else:
        print("Company not found.")


#  JOBS


def add_jobs():
    while True:
        company_id = get_int("Enter company ID: ")

        cursor.execute("SELECT * FROM companies WHERE company_id = %s", (company_id,))
        if cursor.fetchone() is None:
            print("Company ID not found. Try again.")
            continue

        role     = input("Enter role     : ")
        location = input("Enter location : ")

        cursor.execute(
            "INSERT INTO jobs (company_id, role, location) VALUES (%s, %s, %s)",
            (company_id, role, location)
        )
        conn.commit()

        choice = input("Add another job? (y/n): ")
        if choice.lower() != 'y':
            break

    print("Job(s) added successfully.")

def view_jobs():
    query = """
    SELECT jobs.job_id,
           companies.company_name,
           jobs.role,
           jobs.location
    FROM jobs
    JOIN companies ON jobs.company_id = companies.company_id
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    print_separator()
    print(f"{'JobID':<7} {'Company':<20} {'Role':<20} {'Location'}")
    print_separator()
    for row in rows:
        print(f"{row[0]:<7} {row[1]:<20} {row[2]:<20} {row[3]}")
    print_separator()

def update_job():
    job_id       = get_int("Enter job ID       : ")
    new_location = input("Enter new location : ")

    cursor.execute("UPDATE jobs SET location = %s WHERE job_id = %s",
                   (new_location, job_id))
    conn.commit()

    if cursor.rowcount > 0:
        print("Job updated successfully.")
    else:
        print("Job ID not found.")

def delete_job():
    job_id = get_int("Enter job ID: ")

    cursor.execute("DELETE FROM jobs WHERE job_id = %s", (job_id,))
    conn.commit()

    if cursor.rowcount > 0:
        print("Job deleted successfully.")
    else:
        print("Job ID not found.")


#  APPLICATIONS


def apply_job():
    while True:
        student_id = get_int("Enter student ID: ")

        cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
        if cursor.fetchone() is None:
            print("Student not found.")
            continue

        job_id = get_int("Enter job ID: ")

        cursor.execute("SELECT * FROM jobs WHERE job_id = %s", (job_id,))
        if cursor.fetchone() is None:
            print("Job not found.")
            continue

        # ── FEATURE 5: Prevent duplicate applications ──
        cursor.execute(
            "SELECT * FROM applications WHERE student_id = %s AND job_id = %s",
            (student_id, job_id)
        )
        if cursor.fetchone() is not None:
            print("This student has already applied for this job.")
        else:
            cursor.execute(
                "INSERT INTO applications (student_id, job_id) VALUES (%s, %s)",
                (student_id, job_id)
            )
            conn.commit()
            print("Applied successfully.")

        choice = input("Add another application? (y/n): ")
        if choice.lower() != 'y':
            break

def view_applications():
    query = """
    SELECT applications.application_id,
           students.name,
           companies.company_name,
           jobs.role,
           applications.status
    FROM applications
    JOIN students  ON applications.student_id = students.student_id
    JOIN jobs      ON applications.job_id     = jobs.job_id
    JOIN companies ON jobs.company_id         = companies.company_id
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    print_separator()
    print(f"{'AppID':<7} {'Student':<15} {'Company':<20} {'Role':<20} {'Status'}")
    print_separator()
    for row in rows:
        print(f"{row[0]:<7} {row[1]:<15} {row[2]:<20} {row[3]:<20} {row[4]}")
    print_separator()

def update_application_status():
    application_id = get_int("Enter application ID: ")
    new_status     = input("Enter new status (Applied / Selected / Rejected): ")

    cursor.execute(
        "UPDATE applications SET status = %s WHERE application_id = %s",
        (new_status, application_id)
    )
    conn.commit()

    if cursor.rowcount > 0:
        print("Application status updated successfully.")
    else:
        print("Application not found.")


#  FEATURE 1 – ELIGIBILITY CHECKER (improved output)


def eligibility_checker():
    company_id = get_int("Enter company ID: ")

    cursor.execute(
        "SELECT company_name, min_cgpa FROM companies WHERE company_id = %s",
        (company_id,)
    )
    company = cursor.fetchone()

    if company is None:
        print("Company not found.")
        return

    company_name = company[0]
    min_cgpa     = company[1]

    cursor.execute(
        "SELECT student_id, name, cgpa FROM students WHERE cgpa >= %s",
        (min_cgpa,)
    )
    eligible_students = cursor.fetchall()

    print_separator()
    print(f"  Company      : {company_name}")
    print(f"  Minimum CGPA : {min_cgpa}")
    print_separator()

    if not eligible_students:
        print("  No eligible students found.")
    else:
        print("  Eligible Students:")
        for student in eligible_students:
            print(f"    ID: {student[0]},  Name: {student[1]},  CGPA: {student[2]}")

    print_separator()


#  FEATURE 2 – PLACEMENT STATISTICS DASHBOARD


def placement_statistics():
    # Total counts
    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM companies")
    total_companies = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM jobs")
    total_jobs = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM applications")
    total_applications = cursor.fetchone()[0]

    # Status-wise counts
    cursor.execute("SELECT COUNT(*) FROM applications WHERE status = 'Selected'")
    selected = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM applications WHERE status = 'Rejected'")
    rejected = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM applications WHERE status = 'Applied'")
    applied = cursor.fetchone()[0]

    # Unique students who got selected
    cursor.execute("SELECT COUNT(DISTINCT student_id) FROM applications WHERE status = 'Selected'")
    placed_students = cursor.fetchone()[0]

    # Top hiring company
    cursor.execute("""
        SELECT companies.company_name, COUNT(applications.application_id) AS total
        FROM applications
        JOIN jobs      ON applications.job_id     = jobs.job_id
        JOIN companies ON jobs.company_id         = companies.company_id
        GROUP BY companies.company_name
        ORDER BY total DESC
        LIMIT 1
    """)
    top_company_row = cursor.fetchone()
    top_company = f"{top_company_row[0]} ({top_company_row[1]} applications)" if top_company_row else "N/A"

    print_separator()
    print("PLACEMENT STATISTICS DASHBOARD")
    print_separator()
    print(f"  Total Students          : {total_students}")
    print(f"  Total Companies         : {total_companies}")
    print(f"  Total Jobs              : {total_jobs}")
    print(f"  Total Applications      : {total_applications}")
    print_separator()
    print(f"  Applications - Applied  : {applied}")
    print(f"  Applications - Selected : {selected}")
    print(f"  Applications - Rejected : {rejected}")
    print_separator()
    print(f"  Students Placed         : {placed_students}")
    print(f"  Top Hiring Company      : {top_company}")
    print_separator()


#  FEATURE 3 – SEARCH FEATURES


def search_student_by_id():
    student_id = get_int("Enter student ID to search: ")

    cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
    row = cursor.fetchone()

    print_separator()
    if row:
        print(f"  ID     : {row[0]}")
        print(f"  Name   : {row[1]}")
        print(f"  Email  : {row[2]}")
        print(f"  Branch : {row[3]}")
        print(f"  CGPA   : {row[4]}")
    else:
        print("Student not found.")
    print_separator()

def search_company_by_name():
    name = input("Enter company name (or part of it): ")

    cursor.execute(
        "SELECT * FROM companies WHERE company_name LIKE %s",
        (f"%{name}%",)
    )
    rows = cursor.fetchall()

    print_separator()
    if rows:
        print(f"{'ID':<5} {'Company':<20} {'Package(LPA)':<15} {'Min CGPA'}")
        print_separator()
        for row in rows:
            print(f"{row[0]:<5} {row[1]:<20} {row[2]:<15} {row[3]}")
    else:
        print("No company found with that name.")
    print_separator()

def search_jobs_by_location():
    location = input("Enter location to search: ")

    query = """
    SELECT jobs.job_id,
           companies.company_name,
           jobs.role,
           jobs.location
    FROM jobs
    JOIN companies ON jobs.company_id = companies.company_id
    WHERE jobs.location LIKE %s
    """
    cursor.execute(query, (f"%{location}%",))
    rows = cursor.fetchall()

    print_separator()
    if rows:
        print(f"{'JobID':<7} {'Company':<20} {'Role':<20} {'Location'}")
        print_separator()
        for row in rows:
            print(f"{row[0]:<7} {row[1]:<20} {row[2]:<20} {row[3]}")
    else:
        print("No jobs found in that location.")
    print_separator()


#  MAIN MENU


while True:

    print("\n" + "=" * 45)
    print("PLACEMENT MANAGEMENT SYSTEM")
    print("=" * 45)
    print("  --- Students ---")
    print("  1.  Add Student")
    print("  2.  View Students")
    print("  3.  Update Student")
    print("  4.  Delete Student")
    print("  --- Companies ---")
    print("  5.  Add Company")
    print("  6.  View Companies")
    print("  7.  Update Company")
    print("  8.  Delete Company")
    print("  --- Jobs ---")
    print("  9.  Add Job")
    print("  10. View Jobs")
    print("  11. Update Job")
    print("  12. Delete Job")
    print("  --- Applications ---")
    print("  13. Apply for Job")
    print("  14. View Applications")
    print("  15. Update Application Status")
    print("  --- Tools ---")
    print("  16. Eligibility Checker")
    print("  17. Placement Statistics")
    print("  18. Search Student by ID")
    print("  19. Search Company by Name")
    print("  20. Search Jobs by Location")
    print("  --- ")
    print("  21. Exit")
    print("=" * 45)

    choice = get_int("Enter choice: ")

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
        eligibility_checker()
    elif choice == 17:
        placement_statistics()
    elif choice == 18:
        search_student_by_id()
    elif choice == 19:
        search_company_by_name()
    elif choice == 20:
        search_jobs_by_location()
    elif choice == 21:
        print("\n  Thank you! Goodbye.")
        break
    else:
        print("Invalid choice. Please try again.")


