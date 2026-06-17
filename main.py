import argparse
import sys
from models.user import User
from models.project import Project
from models.task import Task
from utils.file_handler import load_data, save_data
from tabulate import tabulate

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

    data = load_data()
    users = data.get("users", [])
    projects = data.get("projects", [])
    tasks = data.get("tasks", [])

    if args.command == "add-user":
        if any(u["name"] == args.name for u in users):
            print(f"User '{args.name}' already exists.")
            return
        users.append({"name": args.name, "email": args.email})
        save_data({"users": users, "projects": projects, "tasks": tasks})
        print(f"User '{args.name}' added successfully.")

    elif args.command == "list-users":
        if not users:
            print("No users found.")
            return
        print(tabulate(users, headers="keys", tablefmt="grid"))

    elif args.command == "add-project":
        if not any(u["name"] == args.user for u in users):
            print(f"User '{args.user}' not found.")
            return
        if any(p["title"] == args.title for p in projects):
            print(f"Project '{args.title}' already exists.")
            return
        projects.append({
            "title": args.title,
            "user": args.user,
            "description": args.description,
            "due_date": args.due
        })
        save_data({"users": users, "projects": projects, "tasks": tasks})
        print(f"Project '{args.title}' added for user '{args.user}'.")

    elif args.command == "list-projects":
        filtered = projects
        if args.user:
            filtered = [p for p in projects if p["user"] == args.user]
        if not filtered:
            print("No projects found.")
            return
        print(tabulate(filtered, headers="keys", tablefmt="grid"))

    elif args.command == "add-task":
        if not any(p["title"] == args.project for p in projects):
            print(f"Project '{args.project}' not found.")
            return
        tasks.append({
            "project": args.project,
            "title": args.title,
            "status": "Pending",
            "assigned_to": args.assigned
        })
        save_data({"users": users, "projects": projects, "tasks": tasks})
        print(f"Task '{args.title}' added to project '{args.project}'.")

    elif args.command == "complete-task":
        task_found = False
        for task in tasks:
            if task["project"] == args.project and task["task"] == args.task:
                task["status"] = "Completed"
                task_found = True
                break
        if task_found:
            save_data({"users": users, "projects": projects, "tasks": tasks})
            print(f"Task '{args.task}' marked as completed.")
        else:
            print("Task not found.")

    elif args.command == "list-tasks":
        filtered = [t for t in tasks if t["project"] == args.project]
        if not filtered:
            print(f"No tasks found for project '{args.project}'.")
            return
        print(tabulate(filtered, headers="keys", tablefmt="grid"))

if __name__ == "__main__":
    main()