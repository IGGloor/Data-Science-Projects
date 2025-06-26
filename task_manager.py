# ===== Importing external modules ===========
from datetime import datetime, date

# Global variable of current user
current_user = None

# ==== Login Section ====

# Method to check login details are correct in the user.txt file, handling errors
def check_login(username_input, password_input):
    try:
        # Open user file, split the lines and check each line against the login details
        with open("user.txt", "r") as file:
            for line in file:
                username, password = line.strip().split(', ')
                if username == username_input and password == password_input:
                    return True
    except ValueError:
        print("\nError: File contains improper formatting.\n")
    except FileNotFoundError:
        print("\nError: File 'user.txt' not found.\n")
    return False

# Method to save all usernames in one list 
def get_usernames():
    try:
        usernames = []
        with open("user.txt", "r") as file:
            for line in file:
                username, password = line.strip().split(", ")
                usernames.append(username)
    except FileNotFoundError:
        print("\nFile 'user.txt' not found.\n")
    return usernames

# Method to register new user
def reg_user():
    while True:
        # Get required details for a new user
        print("\nRegister a new user:")
        username = input("Username: ")
        password = input("Password: ")
        password_check = input("Confirm password: ")

        # Check username is unique (not already used) and that passwords match
        usernames = get_usernames()
        if username not in usernames:
            if password == password_check:
                try:
                    # Add to file, display success message and break the loop
                    with open("user.txt", "a") as file:
                        file.write(f"\n{username}, {password}")
                        print(f"\nRegistration successful! \nNew user created with name: {username}\n")
                except FileNotFoundError:
                    print("\nFile 'user.txt' not found.\n")
                break   
            else:
                print("\nPasswords do not match. Please try again.")
        else:
            print(f"\nUsername '{username}' is already in use. Please try again.")

# Method to add task
def add_task():
    while True:
        print("\nCreate a new task:")
        username = input("Username: ")
        
        # Check if username is valid
        usernames = get_usernames()
        if username not in usernames:
            print("\nUsername not valid. Please try again.\n")

        else:
            # If username is valid get other details
            title = input("Task Title: ")
            description = input("Task Description: ")
            # Ensure due date is a valid input (and can't be in the past)
            while True:
                date = input("Due date (YYYY-MM-DD): ")
                try:
                    due_date = datetime.strptime(date, "%Y-%m-%d").date()
                    if due_date < datetime.today().date():
                        print("\nDue date can't be in the past. Please try again.\n")
                    else:
                        break
                except ValueError:
                    print("\nInvalid date format. Please try again.\n")
            # Format dates for storage and better readability
            format_due_date = due_date.strftime("%d %b %Y")
            current_date = datetime.today().strftime("%d %b %Y")
            # Default status set to 'No'
            status = "No"

            # Save new task to the task.txt file
            try:
                with open("tasks.txt", "a+") as file:
                    file.seek(0) 
                    contents = file.read()
                    # Only add a new line if there is existing content (a user can delete all tasks so this code avoids an empty line 1 from occuring)
                    if contents.strip():
                        file.write(f"\n{username}, {title}, {description}, {format_due_date}, {current_date}, {status}")
                    else:
                        file.write(f"{username}, {title}, {description}, {format_due_date}, {current_date}, {status}")
                    print(f"\nNew task was successfully created for {username}!\n")

            except FileNotFoundError:
                print("\nFile 'tasks.txt' not found.\n")
            break

# Method to view all tasks
def view_all():
    print("\nAll assigned tasks:\n")
    # Track if there are any tasks
    any_tasks = False
    while True:
        try:
            # Read all lines in the file
            with open("tasks.txt", "r") as file:
                lines = file.readlines()
                # If there are no lines print appropiate message
                if not lines:
                    print("There are no tasks recorded yet.")
                    break
                # If the file has lines print each task
                else:
                    any_tasks = True
                    for i, line in enumerate(lines):
                        parts = line.strip().split(", ")
                        # Check if all task details are saved
                        if len(parts) != 6:
                            print(f"Line {i + 1} was skipped.")
                            continue
                        username, title, description, due_date, assigned_date, status = parts
                        print(
                            f'''------------------------------------------------------------------------
Task number:        {i + 1}
Task:               {title}
Assigned to:        {username}
Dated assigned:     {assigned_date}
Due date:           {due_date}
Task complete?      {status}
Task description:
{description}
------------------------------------------------------------------------'''
                    )
                break
        except FileNotFoundError:
            print("\nFile 'tasks.txt' not found.\n")
    return any_tasks

# Method to view current user's tasks
def view_mine():
    print("\nMy tasks:\n")
    # Track if there are any tasks for the user
    user_tasks = []
    try:
        # Read all lines in the file
        with open("tasks.txt", "r") as file:
            lines = file.readlines()

        # For each task of the current user: get the original index and task details
        for i, line in enumerate(lines):
            parts = line.strip().split(", ")
            username, title, description, due_date, assigned_date, status = parts
            if username == current_user:
                # Save each task and index to array
                user_tasks.append((i, parts))
                print(
                            f'''------------------------------------------------------------------------
Task number:        {i + 1}
Task:               {title}
Assigned to:        {username}
Dated assigned:     {assigned_date}
Due date:           {due_date}
Task complete?      {status}
Task description:
{description}
------------------------------------------------------------------------'''
                    )
        if not user_tasks:
            print("\nYou currently have no tasks.\n")
            return False
        
        while True:
            try:
                # Get user input for next steps
                task_number = int(input("To edit a task, please input the task number (enter '-1' to cancel): "))
                # Cancel if '-1' is selected
                if task_number == -1:
                    break
                # Match the task number to a user's specific tasks
                match = None
                for i, parts in user_tasks:
                    if i + 1 == task_number:
                        match = (i, parts)
                        break
                # If it isn't a valid task number for the user display appropraiate message
                if match is None:
                    print("Invalid task number. Please try again.")
                    continue

                # Get user choice for next steps - either edit or change status
                change_type = input("\nWould you like to update the task status to complete or edit task details (input 'complete' or 'edit'): ").lower()
                # Allow user to cancel here as well
                if change_type == '-1':
                    break
                #Code to change status to complete
                elif change_type == 'complete':
                    # Get index and parts for the selected task number
                    task_index, task_parts = match
                    # Get the current status
                    current_status = task_parts[5]
                    if current_status == "No":
                        # Update the task status from incomplete to complete
                        task_parts[5] = "Yes"
                        # Update the task line
                        lines[task_index] = ", ".join(task_parts) + "\n"
                        # Write all lines back to the file
                        with open("tasks.txt", "w") as file:
                            file.writelines(lines)
                        print(f"\nTask number {task_number} completion status successfully changed to 'Yes'.\n")
                    else:
                        # Assume that you can't change a completed tasks status
                        print("This task is already marked as completed.")
                    break
                #Code for editing a task
                elif change_type == 'edit':
                    # Get index and parts for the selected task number
                    task_index, task_parts = match
                    # Get the current status
                    current_status = task_parts[5]
                    # Can only edit incomplete tasks.
                    if current_status == "No":
                        while True:
                            edit_type =  input(
                        '''\nPlease select one of the following options:
n - edit who the task is assigned to
d - edit the due date of the task
b - edit both the assigned person and due date
: ''')
                            # Code for updating person responsible for the task
                            if edit_type == 'n':
                                try:
                                    # Get all valid usernames
                                    usernames = get_usernames() 
                                    username = input("Updated user responsible for the task: ")
                                    # if username is valid, update the task
                                    if username in usernames:
                                        task_parts[0] = username
                                        lines[task_index] = ", ".join(task_parts) + "\n"
                                        # Write all lines back to the file
                                        with open("tasks.txt", "w") as file:
                                            file.writelines(lines)
                                        print(f"\nThe task is now assigned to {username}.\n")
                                        return
                                    else:
                                        print("\nInvalid username provided. Please try again.\n")
                                except ValueError:
                                    print("\nUnable to update the user assigned to the task.\n")
                                
                            # Code for updating due date for the task
                            elif edit_type == 'd':
                                while True:
                                    new_date = input("Updated due date for the task (YYYY-MM-DD): ")
                                    try:
                                        due_date = datetime.strptime(new_date, "%Y-%m-%d").date()
                                        if due_date < datetime.today().date():
                                            print("\nDue date can't be in the past. Please try again.\n")
                                        else:
                                            # Format dates for strage and better readability
                                            updated_due_date = due_date.strftime("%d %b %Y")
                                            # Update the task status from incomplete to complete
                                            task_parts[3] = updated_due_date
                                            # Update the task line
                                            lines[task_index] = ", ".join(task_parts) + "\n"
                                            # Write all lines back to the file
                                            with open("tasks.txt", "w") as file:
                                                file.writelines(lines)
                                            print(f"\nTask due date is now {updated_due_date}\n")
                                            return 
                                    except ValueError:
                                        print("\nInvalid date format. Please try again.\n")
                                
                            # Code to update both the responsible person and due date
                            elif edit_type == 'b':
                                try:
                                    # Get all valid usernames
                                    usernames = get_usernames() 
                                    username = input("Updated user responsible for the task: ")
                                    # if username is valid, update the task
                                    if username in usernames:
                                        task_parts[0] = username
                                        lines[task_index] = ", ".join(task_parts) + "\n"
                                        # Write all lines back to the file
                                        with open("tasks.txt", "w") as file:
                                            file.writelines(lines)
                                        print(f"\nThe task is now assigned to {username}.\n")
                                        # Get new due date 
                                        new_date = input("Updated due date for the task (YYYY-MM-DD): ")
                                        due_date = datetime.strptime(new_date, "%Y-%m-%d").date()
                                        if due_date < datetime.today().date():
                                            print("\nDue date can't be in the past. Please try again.\n")
                                        else:
                                            # Format dates for strage and better readability
                                            updated_due_date = due_date.strftime("%d %b %Y")
                                            # Update the task status from incomplete to complete
                                            task_parts[3] = updated_due_date
                                            # Update the task line
                                            lines[task_index] = ", ".join(task_parts) + "\n"
                                            # Write all lines back to the file
                                            with open("tasks.txt", "w") as file:
                                                file.writelines(lines)
                                            print(f"\nTask due date is now {updated_due_date}\n")
                                            return 
                                    else:
                                        print("\nInvalid username provided. Please try again.\n")
                                    
                                except ValueError:
                                    print("Unable to process updates...")
                            else:
                                print("Please select a valid choice.")
                else:
                    print("\nInvalid input. Please try again.\n")
            except ValueError:
                print("Please enter a valid task number.")

    except FileNotFoundError:
        print("\nFile 'tasks.txt' not found.\n")
    return user_tasks

# Method to view completed tasks
def view_completed():
    print("\nAll completed tasks:\n")
    # Track if there are any completed tasks
    completed_tasks = False
    try:
        with open("tasks.txt", "r") as file:
            for line in file:
                username, title, description, due_date, assigned_date, status = line.strip().split(", ")
                if status == "Yes":
                    completed_tasks = True
                    print(
                            f'''------------------------------------------------------------------------
Task:               {title}
Assigned to:        {username}
Dated assigned:     {assigned_date}
Due date:           {due_date}
Task complete?      {status}
Task description:
{description}
------------------------------------------------------------------------'''
                    )
        if not completed_tasks:
            print("\nThere are no completed tasks yet.\n")
    except FileNotFoundError:
        print("\nFile 'tasks.txt' not found.\n")
    return completed_tasks

# Method to delete tasks
def delete_task():
    # Prompt user to select option for deleting (all tasks, completed tasks or a specific task)
    while True:
        delete_type = input(
                        '''\nPlease select one of the following options:
a - delete all tasks
c - delete all completed tasks
s - delete a specific task
: ''')
        # Code for an admin to delete all tasks listed
        if delete_type == "a":
            # Check if there are tasks to delete
            if view_all():
                try:
                    # Clear the file of all tasks
                        with open("tasks.txt", "w") as file:
                            pass
                        print("\nDelete successful!\n")
                except FileNotFoundError:
                    print("\nFile 'tasks.txt' not found.\n")
                break
            else:
                print("\nThere are no tasks to delete.\n")
                break
                
        # Code for an admin to delete only the completed tasks
        elif delete_type == "c":
            try:
                if view_completed():
                    print("\nThere are completed tasks.\n")
                    # Read all lines in the file
                    with open("tasks.txt", "r") as file:
                        lines = file.readlines()
                    # Write only the lines that have an incomplete status
                    with open("tasks.txt", "w") as file:
                        for line in lines:
                            # Split the line into it's task's values
                            username, title, description, due_date, assigned_date, status = line.strip().split(", ")
                            if status == "No":
                                file.write(f"{username}, {title}, {description}, {due_date}, {assigned_date}, {status}")
                    # Print success message
                    print("\nDelete successful! All completed tasks have been deleted.\n")
                    break
                else:
                    print("\nThere are no completed tasks to delete.\n")
                    break
            except FileNotFoundError:
                print("\nFile 'tasks.txt' not found.\n")
            break          
        
        # Code to delete a single specific task
        elif delete_type == "s":
            # If there are tasks to view - the available tasks will be printed
            if view_all():
                # Prompt user to input specific task number to delete
                while True:
                    try:
                        task_number = input("Input the task number you want to delete: ")
                        index = int(task_number) - 1
                        # Read all lines in the file
                        with open("tasks.txt", "r") as file:
                            lines = file.readlines()
                        # Delete the task number if it exists
                        if 0 <= index < len(lines):
                            del lines[index]
                        # Write only the lines that have an incomplete status
                        with open("tasks.txt", "w") as file:
                            file.writelines(lines)
                        # Print success message
                        print(f"\nDelete successful! Task number {task_number} has been deleted.\n")
                        break
                    except ValueError:
                        print("\nPlease select a valid task number.\n")
                    except FileNotFoundError:
                        print("\nFile 'tasks.txt' not found.\n")
            else:
                # No tasks available to select a delete
                print("\nThere are no tasks to delete.\n")
                break
        else:
            print("Please select a valid input.")
        break

# Method to generate reports
def generate_reports():
    # To generate the task report: call the 3 methods to get task total, incomplete tasks and overdue taks
    task_total = get_total_tasks()
    incomplete_tasks = get_incomplete_tasks()
    overdue_tasks = get_overdue_tasks()
    total_users = get_total_users()
    
    # If there are no tasks the reports can't be generated
    if task_total == 0:
        print("\nThere are no tasks to generate a report on.\n")
        return
    
    # If there are tasks generate the tasks report
    else:
        with open("task_overview.txt", "w") as file:
            overview = (
                f"Total tasks:                      {task_total}\n"
                f"Incomplete tasks:                 {incomplete_tasks}\n"
                f"Completed tasks:                  {task_total - incomplete_tasks}\n"
                f"Percentage of incomplete tasks:   {((incomplete_tasks/task_total)*100):.2f}%\n"
                f"Percentage of overdue tasks:      {((overdue_tasks/task_total)*100):.2f}%"
                )
            file.write(overview)
        print("\nNew report called 'task_overview.txt' was generated.\n")

        user_tasks = []

        if total_users > 0:
            usernames = get_usernames()
            for user in usernames:
                user_total = user_task_total(user)
                if user_total == 0:
                    user_overview = f"{user}, 0, 0, 0, 0, 0"
                else:
                    user_percentage_total = f"{((user_total/task_total)*100):.2f}"
                    user_incomplete = user_task_incomplete(user)
                    incomplete = f"{((user_incomplete/user_total)*100):.2f}"
                    complete = f"{(((user_total - user_incomplete)/user_total)*100):.2f}"
                    user_overdue = user_task_overdue(user)
                    overdue = f"{(((user_overdue)/user_total)*100):.2f}"
                    user_overview = f"{user}, {str(user_total)}, {user_percentage_total}, {complete}, {incomplete}, {overdue}"
                user_tasks.append(user_overview)

            with open("user_overview.txt", "w") as file:
                file.write(f"Total users: {total_users}\n")
                file.write(f"Total tasks: {task_total}\n")
                for user_overview in user_tasks:
                    file.write(f"{user_overview}\n")

        print("\nNew report called 'user_overview.txt' was generated.\n")
            
# Method to retrieve total tasks
def get_total_tasks():
    try:
        # Read tasks.txt to get total tasks
        with open("tasks.txt", "r") as file:
            task_total = 0
            for line in file:
                # Split the line into task's parts
                parts = line.strip().split(", ")
                if len(parts) == 6:
                    task_total += 1
        return task_total
    except FileNotFoundError:
        print("\nThe file 'tasks.txt' was not found.\n")
        return 0

# Method to get incomplete tasks
def get_incomplete_tasks():
    try:
        # Read tasks.txt to get total tasks
        with open("tasks.txt", "r") as file:
            incomplete_tasks = 0
            for line in file:
                # Split the line into task's parts
                parts = line.strip().split(", ")
                if len(parts) == 6:
                    status = parts[5]
                    if status == "No":
                        incomplete_tasks += 1
        return incomplete_tasks
    except FileNotFoundError:
        print("\nThe file 'tasks.txt' was not found.\n")
        return 0

# Method to get overdue tasks   
def get_overdue_tasks():
    try:
        # Read tasks.txt to get total tasks
        with open("tasks.txt", "r") as file:
            overdue_tasks = 0
            for line in file:
                # Split the line into task's parts
                parts = line.strip().split(", ")
                if len(parts) == 6:
                    status = parts[5]
                    if status == "No":
                        # Get due_date, check if overdue and update count
                        due_date = parts[3]
                        format_due_date = datetime.strptime(due_date, "%d %b %Y").date()
                        if format_due_date < datetime.today().date():
                            overdue_tasks += 1
            return overdue_tasks
    except FileNotFoundError:
        print("\nThe file 'tasks.txt' was not found.\n")
        return 0

# Method to get total number of users
def get_total_users():
    try:
        total_users = 0
        with open("user.txt", "r") as file:
            for line in file:
                total_users += 1
        return total_users
    except FileNotFoundError:
        print("\nThe file 'user.txt' was not found.\n")
        return 0

# Method to get total number of tasks assigned to a user
def user_task_total(user):
    try:
        with open("tasks.txt", "r") as file:
            user_task_total = 0
            for line in file:
                # Split the line into task's parts
                parts = line.strip().split(", ")
                if len(parts) == 6:
                    username = parts[0]
                    if username == user:
                        user_task_total += 1
            return user_task_total    
    except FileNotFoundError:
        print("\nThe file 'tasks.txt' was not found.\n")
        return 0

# Method to get total number of incomplete tasks assigned to a user
def user_task_incomplete(user):
    try:
        with open("tasks.txt", "r") as file:
            user_task_incomplete = 0
            for line in file:
                # Split the line into task's parts
                parts = line.strip().split(", ")
                if len(parts) == 6:
                    username = parts[0]
                    status = parts[5]
                    if username == user and status == 'No':
                        user_task_incomplete += 1
            return user_task_incomplete    
    except FileNotFoundError:
        print("\nThe file 'tasks.txt' was not found.\n")
        return 0


# Method to get total number of overdue tasks assigned to a user
def user_task_overdue(user):
    try:
        with open("tasks.txt", "r") as file:
            user_task_overdue = 0
            for line in file:
                # Split the line into task's parts
                parts = line.strip().split(", ")
                if len(parts) == 6:
                    username = parts[0]
                    status = parts[5]
                    date = parts[3]
                    if username == user and status == 'No':
                        due_date = datetime.strptime(date, "%d %b %Y").date()
                        if due_date < datetime.today().date():
                            user_task_overdue += 1
            return user_task_overdue   
    except FileNotFoundError:
        print("\nThe file 'tasks.txt' was not found.\n")
        return 0

# Method to view statistics (from reports generated)
def view_statistics():
    try:
        # Print the task_overview report
        with open("task_overview.txt", "r") as file:
            print("--------------------------------------------------------------------------------------------")
            print("\nTASK OVERVIEW REPORT:\n")
            for line in file:
                print(line)
            print("--------------------------------------------------------------------------------------------\n")    

        # Print the user_overview report
        with open("user_overview.txt", "r") as file:
            print("--------------------------------------------------------------------------------------------")
            print("\nUSER OVERVIEW REPORT:\n")
            for line in file:
                parts = line.strip().split(", ")
                if len(parts) == 6:
                    print(f'''\nSPECIFIC USER SUMMARY:
Username:                                   {parts[0]}
Total tasks:                                {parts[1]}
Percentage of all tasks assigned to user:   {parts[2]} %
Percentage of completed tasks:              {parts[3]} %
Percentage of incomplete tasks:             {parts[4]} %
Percentage of overdue tasks:                {parts[5]} %
'''                    )
                else:
                    print(line)
            print("--------------------------------------------------------------------------------------------")
    except FileNotFoundError:
        print("\nThe report files could not be found. Please ensure to generate reports first.\n")  

def login():
    global current_user
    while True:
        # Get user to input login details
        print("\nEnter login details: \n")
        username = input("Username: ")
        password = input("Password: ")

        # Call method to check login details
        if check_login(username, password):
            print(f"\nYou have successfully logged in as {username}!\n")
            current_user = username
            break
        else:
            print("\nLogin details are incorrect.\n")

while True:
    # If there is no current user, login method is called
    if current_user is None:
        login()
    # If there is a current user, determine which menu is displayed
    else:
        # If the current user is the admin display the admin specific menu, otherwise present a limited menu for other users
        if current_user == "admin":
            menu = input(
        '''Select one of the following options:
r - register a user
a - add task
va - view all tasks
vm - view my tasks
vc - view completed tasks
del - delete a task
ds - display statistics
gr - generate reports
l - logout
e - exit
: '''
    ).lower()
        
        else:
            menu = input(
        '''Select one of the following options:
a - add task
va - view all tasks
vm - view my tasks
l - logout
e - exit
: '''
    ).lower()

        if menu == 'r':
            # Call the reg_user method
            reg_user()        

        elif menu == 'a':
            # Call add task method
            add_task()

        elif menu == 'va':
            # Call view all method
            view_all()
       
        elif menu == 'vm':
            # Call view mine method
            view_mine()

        elif menu == 'vc':
            # Call view completed method
            view_completed()

        elif menu == 'del':
            # Call delete task method
            delete_task()
    
        elif menu == 'ds':
            view_statistics()

        elif menu == 'gr':
            generate_reports()

        elif menu == 'e':
            print(f"\nGoodbye {current_user}!\n")
            break

        elif menu == 'l':
            # I added the logout function to allow for different users to login and out without the program breaking
            print(f"\n{current_user} has been logged out.\n")
            # Reset the current user and continue from the start of the loop (which prompts the for new login details)
            current_user = None
            continue

        else:
            print("\nYou have entered an invalid input. Please try again.\n")