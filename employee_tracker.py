# ==============================================================================
# 🏢 EMPLOYEE TRACKER 
# ==============================================================================
#
# This program lets you manage an employee roster from the terminal.
# It follows the EXACT same structure as the Habit Tracker you studied!
#
# CONCEPTS USED:
#   - Dictionaries  (storing employee records)
#   - Lists         (holding all employees)
#   - Functions     (reusable blocks of code)
#   - File I/O      (saving & loading with JSON)
#   - Loops         (showing menus, listing employees)
#   - Conditionals  (checking input, validating data)
#   - try/except    (handling bad input gracefully)
# ==============================================================================

import json        # For saving/loading data as a .json file
import os          # For checking if the data file exists
from datetime import datetime  # For recording the date an employee was added


# ==============================================================================
# PART 1: FILE HANDLING - SAVING & LOADING DATA
# Same idea as load_habits() and save_habits() in the habit tracker!
# ==============================================================================

DATA_FILE = "employees_data.json"  # The file where all employee data is stored


def load_employees():
    """
    Reads employee data from the JSON file.

    Think of it like: "Does my employee notebook exist?
    If yes, read it. If no, start with an empty list."

    RETURN VALUE: A list of employee dictionaries, or [] if file doesn't exist.
    """
    if os.path.exists(DATA_FILE):          # Does the file exist?
        with open(DATA_FILE, "r") as file: # Open in read mode
            return json.load(file)         # Parse JSON → Python list
    return []                              # First run: return empty list


def save_employees(employees):
    """
    Saves the employee list to the JSON file.

    PARAMETER: employees - The list of all employee records
    RETURN VALUE: Nothing (just writes the file)
    """
    with open(DATA_FILE, "w") as file:         # Open in write mode (creates if missing)
        json.dump(employees, file, indent=2)   # Python list → JSON text, nicely indented


# ==============================================================================
# PART 2: DISPLAY MENU
# Same as display_menu() in the habit tracker!
# ==============================================================================

def display_menu():
    """
    Prints the main menu options to the terminal.
    Nothing fancy — just print statements!
    """
    print("\n" + "=" * 50)
    print("🏢  EMPLOYEE TRACKER")
    print("=" * 50)
    print("1️⃣   Add a new employee")
    print("2️⃣   View all employees")
    print("3️⃣   Search employee by name")
    print("4️⃣   Update employee salary")
    print("5️⃣   Delete an employee")
    print("6️⃣   View salary summary")
    print("7️⃣   Exit")
    print("=" * 50)


# ==============================================================================
# PART 3: ADD AN EMPLOYEE
# Same structure as add_habit() — ask user, validate, store, save.
# ==============================================================================

def add_employee(employees):
    """
    Adds a new employee record to the list.

    STEP 1: Ask for name, department, and salary
    STEP 2: Validate the salary is a real number
    STEP 3: Create the employee dictionary
    STEP 4: Append to the list and save

    PARAMETER: employees - The list to add to
    """
    print("\n--- Add New Employee ---")

    name = input("Full name: ").strip()
    if not name:
        print("❌ Name cannot be empty!")
        return

    # Check for duplicate names (case-insensitive)
    # Any() returns True if ANY item in the loop matches
    if any(e["name"].lower() == name.lower() for e in employees):
        print(f"❌ An employee named '{name}' already exists!")
        return

    department = input("Department (e.g. Engineering, HR, Finance): ").strip()
    if not department:
        print("❌ Department cannot be empty!")
        return

    # Salary must be a valid positive number — use try/except to catch bad input
    try:
        salary = float(input("Monthly salary (₹): ").strip())
        if salary < 0:
            print("❌ Salary cannot be negative!")
            return
    except ValueError:
        # User typed something like "abc" instead of a number
        print("❌ Please enter a valid number for salary!")
        return

    # Build the employee record as a dictionary
    # Same idea as habits[habit_name] = { ... } in the habit tracker
    employee = {
        "id": len(employees) + 1,                          # Simple auto-increment ID
        "name": name,
        "department": department,
        "salary": round(salary, 2),
        "joined": datetime.now().strftime("%Y-%m-%d")       # Today's date
    }

    employees.append(employee)   # .append() adds the new record to the list
    save_employees(employees)    # Always save after making changes!
    print(f"\n✅ '{name}' added successfully!")


# ==============================================================================
# PART 4: VIEW ALL EMPLOYEES
# Same idea as view_progress() — loop through data and display it nicely.
# ==============================================================================

def view_employees(employees):
    """
    Displays all employees in a formatted table.

    STEP 1: Check if there are any employees
    STEP 2: Print a header row
    STEP 3: Loop through every employee and print their info

    PARAMETER: employees - The list to display
    """
    if not employees:   # "not employees" = the list is empty
        print("\n❌ No employees found. Add one first!")
        return

    print("\n" + "=" * 65)
    print(f"{'ID':<5} {'Name':<20} {'Department':<15} {'Salary (₹)':<15} {'Joined'}")
    print("=" * 65)

    # Loop through each employee dictionary in the list
    for emp in employees:
        # f-string with :<N aligns text to the left in N characters (padding)
        print(
            f"{emp['id']:<5} "
            f"{emp['name']:<20} "
            f"{emp['department']:<15} "
            f"{emp['salary']:>12,.2f}   "   # Right-align salary, 2 decimal places
            f"{emp['joined']}"
        )

    print("=" * 65)
    print(f"  Total employees: {len(employees)}")


# ==============================================================================
# PART 5: SEARCH BY NAME
# New feature: loop through employees and find a matching name.
# ==============================================================================

def search_employee(employees):
    """
    Searches for an employee by name (partial match supported).

    PARAMETER: employees - The list to search through
    """
    if not employees:
        print("\n❌ No employees to search!")
        return

    query = input("\nEnter name to search: ").strip().lower()

    # List comprehension: build a new list of employees whose name contains the query
    # This is a compact way of writing a for loop with an if condition
    results = [e for e in employees if query in e["name"].lower()]

    if not results:
        print(f"❌ No employees found matching '{query}'.")
        return

    print(f"\n🔍 Found {len(results)} result(s):")
    print("-" * 55)
    for emp in results:
        print(f"  👤 {emp['name']}  |  {emp['department']}  |  ₹{emp['salary']:,.2f}/mo  |  Since {emp['joined']}")


# ==============================================================================
# PART 6: UPDATE SALARY
# New feature: find an employee and change their salary value.
# ==============================================================================

def update_salary(employees):
    """
    Updates the monthly salary of an existing employee.

    STEP 1: Show the list
    STEP 2: Ask which employee to update (by number)
    STEP 3: Ask for the new salary
    STEP 4: Update the dictionary value and save

    PARAMETER: employees - The list to update
    """
    if not employees:
        print("\n❌ No employees to update!")
        return

    view_employees(employees)  # Show the list first so user can pick

    try:
        choice = int(input("\nEnter employee ID to update salary: ")) - 1
        if choice < 0 or choice >= len(employees):
            print("❌ Invalid ID!")
            return

        emp = employees[choice]   # Get the employee at that index
        print(f"  Current salary for {emp['name']}: ₹{emp['salary']:,.2f}")

        new_salary = float(input("  New monthly salary (₹): ").strip())
        if new_salary < 0:
            print("❌ Salary cannot be negative!")
            return

        old_salary = emp["salary"]
        emp["salary"] = round(new_salary, 2)  # Update the value inside the dictionary
        save_employees(employees)

        diff = new_salary - old_salary
        direction = "📈" if diff >= 0 else "📉"
        print(f"\n{direction} Salary updated! ₹{old_salary:,.2f} → ₹{new_salary:,.2f}")

    except ValueError:
        print("❌ Please enter a valid number!")
    except IndexError:
        print("❌ Invalid selection!")


# ==============================================================================
# PART 7: DELETE AN EMPLOYEE
# Same as delete_habit() — confirm before removing!
# ==============================================================================

def delete_employee(employees):
    """
    Removes an employee from the list after confirmation.

    We ask for confirmation (type the name) to avoid accidental deletion!

    PARAMETER: employees - The list to remove from
    """
    if not employees:
        print("\n❌ No employees to delete!")
        return

    view_employees(employees)

    try:
        choice = int(input("\nEnter employee ID to delete: ")) - 1
        if choice < 0 or choice >= len(employees):
            print("❌ Invalid ID!")
            return

        emp = employees[choice]
        confirm = input(f"  Type '{emp['name']}' to confirm deletion: ").strip()

        if confirm == emp["name"]:
            employees.pop(choice)    # .pop(index) removes item at that position

            # Re-assign IDs so they stay sequential after deletion
            for i, e in enumerate(employees):
                e["id"] = i + 1

            save_employees(employees)
            print(f"\n🗑️  '{emp['name']}' has been removed.")
        else:
            print("❌ Name didn't match. Deletion cancelled.")

    except ValueError:
        print("❌ Please enter a valid number!")
    except IndexError:
        print("❌ Invalid selection!")


# ==============================================================================
# PART 8: SALARY SUMMARY
# Like the stats bar in the web version — calculate totals and averages.
# ==============================================================================

def salary_summary(employees):
    """
    Displays a salary summary across all employees.

    Uses Python's built-in min(), max(), sum(), and len() functions.

    PARAMETER: employees - The list to analyze
    """
    if not employees:
        print("\n❌ No employee data to summarize!")
        return

    # Extract just the salaries into a list using list comprehension
    salaries = [e["salary"] for e in employees]

    total   = sum(salaries)
    average = total / len(salaries)
    highest = max(salaries)
    lowest  = min(salaries)

    # Find the employee objects for highest/lowest salary
    # next() returns the first match from a generator expression
    top_earner    = next(e for e in employees if e["salary"] == highest)
    lowest_earner = next(e for e in employees if e["salary"] == lowest)

    # Group employees by department and compute department totals
    # We build a dictionary: { "Engineering": total_salary, ... }
    dept_totals = {}
    for emp in employees:
        dept = emp["department"]
        dept_totals[dept] = dept_totals.get(dept, 0) + emp["salary"]
        # .get(key, default) returns 0 if department not in dict yet

    print("\n" + "=" * 50)
    print("📊  SALARY SUMMARY")
    print("=" * 50)
    print(f"  Total employees   : {len(employees)}")
    print(f"  Total payroll/mo  : ₹{total:>12,.2f}")
    print(f"  Average salary    : ₹{average:>12,.2f}")
    print(f"  Highest salary    : ₹{highest:>12,.2f}  ({top_earner['name']})")
    print(f"  Lowest salary     : ₹{lowest:>12,.2f}  ({lowest_earner['name']})")
    print("\n  --- By Department ---")
    for dept, total_sal in sorted(dept_totals.items()):
        print(f"  {dept:<20}: ₹{total_sal:>12,.2f}")
    print("=" * 50)


# ==============================================================================
# PART 9: MAIN PROGRAM LOOP
# Same as main() in the habit tracker — while True loop until user exits.
# ==============================================================================

def main():
    """
    The main function that runs the whole program.

    Uses a WHILE LOOP that keeps showing the menu until the user picks Exit.
    Each menu option calls a different function.
    """
    print("\n🚀 Welcome to the Employee Tracker!")
    print("   Your team data is saved in:", DATA_FILE)

    while True:                          # Loop forever until break
        employees = load_employees()     # Reload from file each iteration
        display_menu()

        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            add_employee(employees)
        elif choice == "2":
            view_employees(employees)
        elif choice == "3":
            search_employee(employees)
        elif choice == "4":
            update_salary(employees)
        elif choice == "5":
            delete_employee(employees)
        elif choice == "6":
            salary_summary(employees)
        elif choice == "7":
            print("\n👋 Goodbye! Employee data saved. See you next time!\n")
            break                        # Exits the while loop → program ends
        else:
            print("❌ Invalid choice! Please enter a number between 1 and 7.")


# ==============================================================================
# PART 10: ENTRY POINT
# ==============================================================================

# Only run main() if this file is run directly (not imported elsewhere)
if __name__ == "__main__":
    main()


# ==============================================================================
# SUMMARY — HOW THIS MAPS TO THE HABIT TRACKER
# ==============================================================================
#
# HABIT TRACKER          →   EMPLOYEE TRACKER
# ─────────────────────────────────────────────
# habits = {}            →   employees = []
# add_habit()            →   add_employee()
# mark_completed()       →   update_salary()
# view_progress()        →   view_employees() + salary_summary()
# delete_habit()         →   delete_employee()
# load_habits()          →   load_employees()
# save_habits()          →   save_employees()
# completed_dates list   →   salary, department, joined fields
#
# KEY NEW PYTHON CONCEPTS IN THIS FILE:
#
# any()   - Returns True if ANY item in a loop matches a condition
#           any(e["name"] == name for e in employees)
#
# List comprehension - Compact for loop that builds a list
#           salaries = [e["salary"] for e in employees]
#
# dict.get(key, default) - Safely get a value, use default if missing
#           dept_totals.get(dept, 0)
#
# next()  - Gets the first match from a search
#           next(e for e in employees if e["salary"] == highest)
#
# f-string alignment - :<N left-aligns, :>N right-aligns in N chars
#           f"{'Name':<20} {'Salary':>12}"
# ==============================================================================
