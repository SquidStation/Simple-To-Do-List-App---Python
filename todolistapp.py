"""

*****TODO_LIST_APP***

    1.The app will ask for user to add task(s) on first run
    2.Store the data in memory (csv) file.
    3.Retrieve data from memory(csv)
    4.List all tasks with their status alongside.
    5.Delete a task
    6.Mark a task complete
    7.Update a task

"""
import csv

def main():
    initializeApp()


def initializeApp():

    #Display stored tasks
    print(f"\n****Your Tasks List*****\n")
    fetchTasks()

    #Display app guidelines
    guides = (f"\nAdd New Task: Enter 1", "Add More Tasks: Enter 2","Delete a Task: Enter 3", "Update a Task: Enter 4\n")
    for guide in guides:
        print(guide)
    
    choice = int(input("Enter Choice: "))
    if choice == 1:
        writeTasks()
    elif choice == 2:
        writeTasks()
    elif choice == 3:
        #get task id from user(remeber to validate data)
        taskId = int(input("Enter Task Number: "))
        deleteTasks(taskId)
    elif choice == 4:
        #get task id for task to edit
        taskId = int(input("Enter Task Number: "))
        editTasks(taskId)
    else:
        print(f"\nInvalid Input, Try again\n")
        

def writeTasks():

    #get task from the user
    taskname = input("Enter name of task: ")

    #Write user input
    with open("todolist.csv", "a") as file:
        writer = csv.DictWriter(file, fieldnames=["taskname"])
        #check first whether key fieldname exist in csv file
        if writer.fieldnames is None:
            writer.writeheader() 
        else:
            writer.writerow({"taskname": taskname})
        print("Task added!")


def fetchTasks():
    savedtasks = []
    
    # retrieve data from memory
    with open("todolist.csv") as file:
        tasks = csv.DictReader(file)
        for row in tasks:
            savedtasks.append({"taskname": row['taskname']})
    
    for index, storedtask in enumerate(savedtasks):
        print(f"{index+1}: {storedtask['taskname']}")


# function to delete tasks
def deleteTasks(taskindex):

    savedtasks = []

    #retreive stored tasks 
    with open("todolist.csv") as file:
        tasks = csv.DictReader(file)
        for row in tasks:
            savedtasks.append({"taskname": row['taskname']})

    #search for item to delete
    for index, savedtask in enumerate(savedtasks):
        if index+1 == taskindex:
            savedtasks.remove(savedtask)
            print(f"({savedtask['taskname']}) Deleted!")

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
    for index, savedTask in enumerate(savedTasks):
        if index+1 == taskindex:
            taskUpdate = input("Enter New Name: ")
            updatedTask = {"taskname": taskUpdate}
            savedTasks[index] = updatedTask
            print(f"{savedTask['taskname']} Updated to {taskUpdate}!")

    
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