"""

*****TODO_LIST_APP***

    1.The app will ask for user to add task(s) on first run √
    2.Store the data in memory (To local csv file). √
    3.Retrieve saved data (Trom local csv file) √
    4.List all tasks with their status alongside.
    5.Delete a task √
    6.Mark a task complete
    7.Update a task √
    8.Validate input data from the user √
    9.Gracefully handle all user related or system errors
    10. Add timestamps to each to do list item and sort the items √

"""
import csv
from datetime import datetime
import os

def main():
    initializeApp()


def initializeApp():

    #Display stored tasks
    print(f"\n****Your To Do List Items:****\n")
    fetchTasks()

    #Display app guidelines
    print(f"\n***Select Option Below To Proceed***")
    guides = (f"\nAdd New Task: Enter 1", "Delete a Task: Enter 2","Update a Task: Enter 3", "Delete All Tasks: Enter 4", "Complete Task: Enter 5 \n")
    for guide in guides:
        print(guide)
    
    
    #Handle input error using try and except
    try:
        choice = int(input("Enter Choice: "))
        if choice == 1:
            writeTasks()
        elif choice == 2:
            #get task id from user(remeber to validate data)
            taskId = int(input("\nEnter Task ID/Number To Delete: "))
            deleteTasks(taskId)
        elif choice == 3:
            #get task id for task to edit
            taskId = int(input("\nEnter Task ID/Number To Edit: "))
            editTasks(taskId)
        elif choice == 4:
            #Delete All Tasks
            deleteAllTasks()
        elif choice == 5:
            #Complete a task
            taskId = int(input(f"\nEnter Task ID/Number to Mark Complete: "))
            completeTask(taskId)
        else:
            print(f"\nSelected Option Not Available, Try again\n")
    
    except ValueError:
        print("\nError: Special characters, letters and decimals numbers NOT allowed \n")
        

def writeTasks():

    #Write a new task
    writeNewTask()


    #Continue adding more tasks from user on demand.

    print(f"\n*****Add more tasks? Enter 'y/yes' for YES OR 'n/no' for NO*****\n")

    while True:
        moretasks = input("Add more tasks?: ")
        if moretasks.lower() == 'y' or moretasks.lower() == 'yes':
            writeNewTask()
        elif moretasks.lower() == 'n' or moretasks.lower() == 'no':
            print("\nThank you for using my todo list app...\n")
            break
        else: 
            print("\nInvalid Input, Please Try Again\n")
            break

        
#Function that writes new tasks
def writeNewTask():

    #get task from the user
    taskname = input(f"\nEnter name of task: ")

    #get task time from the user
    tasktime = input(f"\nEnter task time(Day-Month-Year Hour:Minute AM/PM): ")
    date_format = f'%m-%d-%Y %I:%M %p' 
    #convert user string time to a datetime object
    tasktime_obj = datetime.strptime(tasktime, date_format)

    #add a task status(default will be pending)
    task_status = "Pending"
    fields = ["taskname","tasktime","taskstatus"]
    file_exists= os.path.isfile("todolist.csv")
    file_empty = os.path.getsize("todolist.csv") == 0 if file_exists else True

    #Write user input
    with open("todolist.csv", "a", newline='') as file:
        writer = csv.DictWriter(file, fieldnames= fields)
        #check first whether key fieldname exist in csv file
        if file_empty:
            writer.writeheader()
        writer.writerow({"taskname":taskname, "tasktime": tasktime_obj, "taskstatus": task_status})
        print(f"\n***{taskname} - Task added!***\n")

# Function to list all saved to-do-list events
def fetchTasks():
    savedtasks = []
    
    # Read data from memory and save to a local variable(savedtasks)
    with open("todolist.csv") as file:
        tasks = csv.DictReader(file)
        for row in tasks:
            savedtasks.append({"taskname": row['taskname'], "tasktime": row['tasktime'], "taskstatus": row['taskstatus']})

    #sort fetched to-do-list using timestamp
    savedtasks.sort(key=lambda x: datetime.strptime(x['tasktime'], "%Y-%d-%m %H:%M:%S"))

    #if to-do-list empty let user know its empty
    if len(savedtasks) == 0:
        print("\nYour task list is empty!\n")
    else:
        for index, storedtask in enumerate(savedtasks):
            date_format = f'%Y-%d-%m %H:%M:%S'
            storedTime_obj = storedtask['tasktime']
            tasktime_obj = datetime.strptime(storedTime_obj , date_format)
            #match users localtime display format
            formated_time = tasktime_obj.strftime('%a %b %d, %Y %I:%M:%S %p')
            print(f"Id {index+1}: -> {storedtask['taskname']} on {formated_time} ({storedtask['taskstatus']})")

    #write the local sorted to-do-list to memory hence everytime the program is launched it sorts the stored csv file
    fields = ["taskname","tasktime","taskstatus"]
    #variables to check if csv file exists and whether its empty
    file_exists= os.path.isfile("todolist.csv")
    file_empty = os.path.getsize("todolist.csv") == 0 if file_exists else True

    #Force a clean rewrite of the csv file afresh
    with open('todolist.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
    
    # loop through the new sorted to-do-list and add all to stored csv memory
    for savedtask in savedtasks:
        with open('todolist.csv', 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writerow({"taskname": savedtask['taskname'], "tasktime": savedtask['tasktime'], "taskstatus": savedtask['taskstatus']})


# Function to delete all events
def deleteAllTasks():
    #write the key header for our csv file 
    fields = ["taskname","tasktime","taskstatus"] #header keys array/list
    with open("todolist.csv", 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
    
    print("\nAll tasks Deleted!\n")

# Function to delete specific tasks
def deleteTasks(taskindex):

    savedtasks = []

    #retreive stored tasks 
    with open("todolist.csv") as file:
        tasks = csv.DictReader(file)
        for row in tasks:
            savedtasks.append({"taskname": row['taskname'], "tasktime": row['tasktime'], "taskstatus": row['taskstatus']})
            

    #search for item to delete
    task_found = None
    for index, savedtask in enumerate(savedtasks):
        #if current task position in the list matches the entered task id
        if index+1 == taskindex:
            savedtasks.remove(savedtask)
            task_found = savedtask
            break 
    
    if task_found:
        print(f"\n({savedtask['taskname']}) Deleted!\n")
    else:
        print(f"\nTask Doesn't Exist\n")

    #write the remaining tasks to memory
    fields = ["taskname","tasktime","taskstatus"] #header keys array/list
    with open('todolist.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames= fields)
        writer.writeheader()
    #rewrite updated data to memory
    for savedtask in savedtasks:
        with open('todolist.csv', 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writerow({"taskname": savedtask['taskname'], "tasktime": savedtask['tasktime'], "taskstatus": savedtask['taskstatus']})

#Function to edit/modify a task details
def editTasks(taskindex):

    savedTasks = []

    #get stored data
    with open("todolist.csv") as file:
        tasks = csv.DictReader(file)
        for row in tasks:
            savedTasks.append(row) 

    #Find item to edit
    task_found = None
    task_updated = None

    for index, savedTask in enumerate(savedTasks):
        if index+1 == taskindex:
            #get updated task details
            taskNameUpdate = input("\nEnter New Name: ")
            #get new time and date from user
            taskTimeUpdate = input("\nEnter New time (Day-Month-Year Hour:Minute AM/PM): ")
            date_format = f'%m-%d-%Y %I:%M %p' 
            #convert user string time to a datetime object
            tasktime_obj = datetime.strptime(taskTimeUpdate, date_format) 
            #add a task status(default will be pending)
            task_status = "Pending"
            #variable dictionary with all the updated details
            updatedTask = {"taskname": taskNameUpdate, "tasktime":tasktime_obj, "taskstatus":task_status}
            savedTasks[index] = updatedTask
            task_found = savedTask
            task_updated = taskNameUpdate
            
    #Let user know if item is updated
    if task_found:
        print(f"\n'{task_found['taskname']}' Updated to '{task_updated}'!\n")
    else:
        print(f"\nTask Doesn't Exist\n")
    
    #Before saving data make sure key header is written in csv file
    fields = ["taskname","tasktime","taskstatus"] #header keys array/list
    with open("todolist.csv", 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()

    #Save updated data to memory
    for savedtask in savedTasks:
        with open("todolist.csv", 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writerow({"taskname": savedtask['taskname'], "tasktime": savedtask['tasktime'], "taskstatus": savedtask['taskstatus']})

#Fucntion to Mark a task complete
def completeTask(taskindex):

    #array to save all tasks that will be retrieved from memory
    savedTasks = []

    #get stored data from memory
    with open("todolist.csv") as file:
        tasks = csv.DictReader(file)
        for row in tasks:
            savedTasks.append(row)
    
    #find item to mark complete flags
    task_found = None
    task_completed = None

    for index, savedTask in enumerate(savedTasks):
        if index+1 == taskindex:
             #get current task status
             task_completed = savedTasks[index]['taskname']
             task_found = savedTask
             taskstatus = savedTasks[index]['taskstatus']  
             if taskstatus == 'Pending':   
                savedTasks[index]['taskstatus'] = 'Completed'
                 
    #Save updated data to memory
    fields = ["taskname","tasktime","taskstatus"] #header keys array/list

    if task_found:
        #rewrite file fieldnames
        with open('todolist.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
        #save all data to memory
        for savedtask in savedTasks:
            with open('todolist.csv', 'a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fields)
                writer.writerow({"taskname": savedtask['taskname'], "tasktime": savedtask['tasktime'], "taskstatus": savedtask['taskstatus']})
        #notify user task is completed
        print(f'\n{task_completed} Completed!\n')
    else:
        print("\nTask Not Found, Please Try Again\n")

if __name__ == "__main__":
    main()