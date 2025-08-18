"""

*****TODO_LIST_APP***

    1.The app will ask for user to add task(s) on first run
    2.Store the data in memory (csv) file.
    3.Retrieve saved data (csv)
    4.List all tasks with their status alongside.
    5.Delete a task
    6.Mark a task complete
    7.Update a task
    8.Validate input data from the user
    9.Gracefully handle all user related or system errors

"""
import csv

def main():
    initializeApp()


def initializeApp():

    #Display stored tasks
    print(f"\n****Your To Do List Below*****\n")
    fetchTasks()

    #Display app guidelines
    print(f"\n***Select Option Below To Proceed***")
    guides = (f"\nAdd New Task: Enter 1", "Delete a Task: Enter 2","Update a Task: Enter 3", "Delete All Tasks: Enter 4 \n")
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
        else:
            print(f"\nSelected Option Not Available, Try again\n")
    
    except ValueError:
        print("\n Error: Only a number is allowed\n")
        

def writeTasks():

    #Write a new task
    writeNewTask()


    #Continue adding more tasks from user on demand.

    print(f"\n*****To add more tasks enter 'Y or y' for Yes and 'N/n' for No*****\n")

    while True:
        moretasks = input("Add more tasks?: ")
        if moretasks.lower() == 'y':
            writeNewTask()
        elif moretasks.lower() == 'n':
            print("\nThank you for using my todo list app...\n")
            break
        else: 
            print("\nInvalid Input, Please Try Again\n")
            break

        
#Function that writes new tasks
def writeNewTask():

    #get task from the user
    taskname = input(f"\nEnter name of task: ")

    #Write user input
    with open("todolist.csv", "a") as file:
        writer = csv.DictWriter(file, fieldnames=["taskname"])
        #check first whether key fieldname exist in csv file
        if writer.fieldnames is None:
            writer.writeheader() 
        else:
            writer.writerow({"taskname": taskname})
        print(f"\n***{taskname} - Task added!***\n")

# Function to list ass saved events
def fetchTasks():
    savedtasks = []
    
    # retrieve data from memory
    with open("todolist.csv") as file:
        tasks = csv.DictReader(file)
        for row in tasks:
            savedtasks.append({"taskname": row['taskname']})

    #if list empty let user know its empty
    if len(savedtasks) == 0:
        print("\nYour task list is empty\n")
    else:
        for index, storedtask in enumerate(savedtasks):
            print(f"Id {index+1}: {storedtask['taskname']}")

# Function to delete all events
def deleteAllTasks():
    #write the key header for our csv file 
    with open("todolist.csv", 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["taskname"])
        writer.writeheader()
    
    print("\nAll tasks Deleted!\n")

# Function to delete specific tasks
def deleteTasks(taskindex):

    savedtasks = []

    #retreive stored tasks 
    with open("todolist.csv") as file:
        tasks = csv.DictReader(file)
        for row in tasks:
            savedtasks.append({"taskname": row['taskname']})

    #search for item to delete
    task_found = None
    for index, savedtask in enumerate(savedtasks):
        if index+1 == taskindex:
            savedtasks.remove(savedtask)
            task_found = savedtask
            break 
    
    if task_found:
        print(f"\n({savedtask['taskname']}) Deleted!\n")
    else:
        print(f"\nTask Doesn't Exist\n")


    with open('todolist.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["taskname"])
        writer.writeheader()
    #rewrite updated data to memory
    for savedtask in savedtasks:
        with open('todolist.csv', 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["taskname"])
            writer.writerow({ "taskname": savedtask['taskname']})

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
            taskUpdate = input("\nEnter New Name: ")
            updatedTask = {"taskname": taskUpdate}
            savedTasks[index] = updatedTask
            task_found = savedTask
            task_updated = taskUpdate
            
    #Let user know if item is deleted
    if task_found:
        print(f"\n'{task_found['taskname']}' Updated to '{task_updated}'!\n")
    else:
        print(f"\nTask Doesn't Exist\n")
    
    #Before saving data make sure key header is written in csv file
    with open("todolist.csv", 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['taskname'])
        writer.writeheader()

    #Save updated data to memory
    for savedTask in savedTasks:
        with open("todolist.csv", 'a') as file:
            writer = csv.DictWriter(file, fieldnames=["taskname"])
            writer.writerow({"taskname": savedTask['taskname']})


if __name__ == "__main__":
    main()