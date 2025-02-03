class ToDoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)
        print(f'Added task: "{task}"')

    def remove_task(self, task_number):
        if 0 <= task_number < len(self.tasks):
            removed_task = self.tasks.pop(task_number)
            print(f'Removed task: "{removed_task}"')
        else:
            print(f'Task number {task_number} is out of range.')

    def display_tasks(self):
        if not self.tasks:
            print("Your to-do list is empty.")
        else:
            print("Your to-do list:")
            for i, task in enumerate(self.tasks, start=1):  # Fixed the syntax and typo
                print(f"{i}. {task}")

def main():
    todo_list = ToDoList()

    while True:
        print("\nOptions:")
        print("1. Add a task")
        print("2. Remove a task")
        print("3. View all tasks")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            task = input("Enter the task: ")
            todo_list.add_task(task)  # Corrected `taskl` to `task`
        elif choice == '2':
            task_number = int(input("Enter the task number to remove: ")) - 1
            todo_list.remove_task(task_number)
        elif choice == '3':
            todo_list.display_tasks()
        elif choice == '4':
            print("Exiting the to-do list app. Goodbye!")  # Corrected "Existing" to "Exiting"
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()