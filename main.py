import argparse
import sys
import re
from models.user import User
from models.project import Project
from models.task import Task
from utils.file_handler import load_data, save_data, get_data_path
from tabulate import tabulate

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_name(name):
    if not name or len(name.strip()) < 2:
        return False
    return True

def main():
    parser = argparse.ArgumentParser(description="Project Management CLI Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # User commands
    user_parser = subparsers.add_parser("add-user", help="Add a new user")
    user_parser.add_argument("--name", required=True, help="User name")
    user_parser.add_argument("--email", required=True, help="User email")

    list_users = subparsers.add_parser("list-users", help="List all users")

    # Project commands
    proj_parser = subparsers.add_parser("add-project", help="Add a new project")
    proj_parser.add_argument("--user", required=True, help="Owner name")
    proj_parser.add_argument("--title", required=True, help="Project title")
    proj_parser.add_argument("--description", default="", help="Project description")
    proj_parser.add_argument("--due", default="No deadline", help="Due date")

    list_proj = subparsers.add_parser("list-projects", help="List all projects")
    list_proj.add_argument("--user", help="Filter by user")

    # Task commands
    task_parser = subparsers.add_parser("add-task", help="Add a task")
    task_parser.add_argument("--project", required=True, help="Project title")
    task_parser.add_argument("--title", required=True, help="Task title")
    task_parser.add_argument("--assigned", default="Unassigned", help="Assigned user")

    complete_parser = subparsers.add_parser("complete-task", help="Mark task as complete")
    complete_parser.add_argument("--project", required=True, help="Project title")
    complete_parser.add_argument("--task", required=True, help="Task title")

    list_tasks = subparsers.add_parser("list-tasks", help="List tasks")
    list_tasks.add_argument("--project", required=True, help="Project title")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        data = load_data()
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    users = data.get("users", [])
    projects = data.get("projects", [])
    tasks = data.get("tasks", [])

    if args.command == "add-user":
        if not validate_name(args.name):
            print("Error: Name must be at least 2 characters long.")
            return
        if not validate_email(args.email):
            print("Error: Invalid email format. Use format: user@domain.com")
            return
        if any(u["name"].lower() == args.name.lower() for u in users):
            print(f"Error: User '{args.name}' already exists.")
            return
        users.append({"name": args.name, "email": args.email})
        try:
            save_data({"users": users, "projects": projects, "tasks": tasks})
            print(f"User '{args.name}' added successfully.")
        except Exception as e:
            print(f"Error saving data: {e}")

    elif args.command == "list-users":
        if not users:
            print("No users found. Add one with: python main.py add-user --name NAME --email EMAIL")
            return
        print(tabulate(users, headers="keys", tablefmt="grid"))

    elif args.command == "add-project":
        if not validate_name(args.title):
            print("Error: Project title must be at least 2 characters long.")
            return
        user_exists = any(u["name"] == args.user for u in users)
        if not user_exists:
            print(f"Error: User '{args.user}' not found. Create user first.")
            return
        if any(p["title"].lower() == args.title.lower() for p in projects):
            print(f"Error: Project '{args.title}' already exists.")
            return
        projects.append({
            "title": args.title,
            "user": args.user,
            "description": args.description,
            "due_date": args.due
        })
        try:
            save_data({"users": users, "projects": projects, "tasks": tasks})
            print(f"Project '{args.title}' added for user '{args.user}'.")
        except Exception as e:
            print(f"Error saving data: {e}")

    elif args.command == "list-projects":
        filtered = projects
        if args.user:
            filtered = [p for p in projects if p["user"].lower() == args.user.lower()]
            if not filtered:
                print(f"No projects found for user '{args.user}'.")
                return
        if not filtered:
            print("No projects found.")
            return
        print(tabulate(filtered, headers="keys", tablefmt="grid"))

    elif args.command == "add-task":
        if not validate_name(args.title):
            print("Error: Task title must be at least 2 characters long.")
            return
        project_exists = any(p["title"] == args.project for p in projects)
        if not project_exists:
            print(f"Error: Project '{args.project}' not found.")
            return
        task_exists = any(t["project"] == args.project and t["title"].lower() == args.title.lower() for t in tasks)
        if task_exists:
            print(f"Error: Task '{args.title}' already exists in project '{args.project}'.")
            return
        tasks.append({
            "project": args.project,
            "title": args.title,
            "status": "Pending",
            "assigned_to": args.assigned
        })
        try:
            save_data({"users": users, "projects": projects, "tasks": tasks})
            print(f"Task '{args.title}' added to project '{args.project}'.")
        except Exception as e:
            print(f"Error saving data: {e}")

    elif args.command == "complete-task":
        task_found = False
        for task in tasks:
            if task["project"] == args.project and task["title"].lower() == args.task.lower():
                if task["status"] == "Completed":
                    print(f"Task '{args.task}' is already completed.")
                    return
                task["status"] = "Completed"
                task_found = True
                break
        if task_found:
            try:
                save_data({"users": users, "projects": projects, "tasks": tasks})
                print(f"Task '{args.task}' marked as completed.")
            except Exception as e:
                print(f"Error saving data: {e}")
        else:
            print(f"Error: Task '{args.task}' not found in project '{args.project}'.")

    elif args.command == "list-tasks":
        filtered = [t for t in tasks if t["project"].lower() == args.project.lower()]
        if not filtered:
            print(f"No tasks found for project '{args.project}'. Add one with: python main.py add-task --project \"{args.project}\" --title TITLE")
            return
        print(tabulate(filtered, headers="keys", tablefmt="grid"))

if __name__ == "__main__":
    main()