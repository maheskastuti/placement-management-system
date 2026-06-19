# Placement Management System

## Overview

Placement Management System is a Python and MySQL based project that helps manage campus placement activities.

The system allows administrators to:

* Manage student records
* Manage company records
* Manage job postings
* Track job applications
* Update application status
* Check student eligibility based on company CGPA criteria

---

## Features

### Student Management

* Add Student
* View Students
* Update Student Details
* Delete Student

### Company Management

* Add Company
* View Companies
* Update Company
* Delete Company

### Job Management

* Add Job Openings
* View Jobs
* Update Job Details
* Delete Jobs

### Application Management

* Apply for Jobs
* View Applications
* Update Application Status

### Eligibility Checker

* Displays all students eligible for a company based on minimum CGPA requirements.

---

## Technologies Used

* Python
* MySQL
* MySQL Connector/Python

---

## Database Tables

### Students

* student_id
* name
* email
* branch
* cgpa

### Companies

* company_id
* company_name
* package_lpa
* min_cgpa

### Jobs

* job_id
* company_id
* role
* location

### Applications

* application_id
* student_id
* job_id
* status

---

## How to Run

1. Install Python
2. Install MySQL
3. Create the database and tables
4. Install MySQL Connector

```bash
pip install mysql-connector-python
```

5. Update database credentials in the code.
6. Run:

```bash
python placement.py
```

---

## Learning Outcomes

This project helped in understanding:

* Python Functions
* CRUD Operations
* MySQL Database Connectivity
* SQL Queries
* Joins
* Foreign Keys
* Database Design
* Placement Workflow Management

---

## Future Improvements

* Placement Statistics Dashboard
* Search Functionality
* User Authentication
* Exception Handling
* GUI using Tkinter
* Web Version using Flask/Django

---

## Author

Stuti Maheska

Stuti Maheska
