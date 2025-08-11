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
    guides = (f"\nEnter 1 to add new task", "Enter 2, to add more tasks\n")
    for guide in guides:
        print(guide)
    
    choice = int(input("Enter Choice: "))
    if choice == 1:
        writeTasks()
    elif choice == 2:
        writeTasks()
    else:
        print(f"\nInvalid Input, Try again\n")
        

def writeTasks():

    #get task from the user
    taskname = input("Enter name of task: ")

    with open("todolist.csv", "a") as file:
        writer = csv.DictWriter(file, fieldnames=["taskname"])
        writer.writerow({"taskname": taskname})
        print("Task added!")


def fetchTasks():
    storedtasks = []
    
    # retrieve data from memory
    with open("todolist.csv") as file:
        tasks = csv.DictReader(file)
        for row in tasks:
            storedtasks.append({"taskname": row['taskname']})
    
    for index, storedtask in enumerate(storedtasks):
        print(f"{index+1}: {storedtask['taskname']}")



def deletTasks(taskindex):
    ...

def editTasks(taskindex):
    ...

if __name__ == "__main__":
    main()