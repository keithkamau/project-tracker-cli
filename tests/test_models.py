import pytest
from models.user import User
from models.project import Project
from models.task import Task

def test_user_creation():
    user = User("Alice", "alice@email.com")
    assert user.name == "Alice"
    assert user.email == "alice@email.com"

def test_project_creation():
    project = Project("Test Project", "A test", "2024-12-31")
    assert project.title == "Test Project"
    assert project.description == "A test"
    assert project.due_date == "2024-12-31"
def test_task_creation():
    task = Task("Test Task")
    assert task.status == "Pending"
    task.complete()
    assert task.status == "Completed"

def test_user_project_relationship():
    user = User("Bob", "bob@email.com")
    project = Project("Bob's Project")
    user.add_project(project)
    assert len(user.projects) == 1

def test_project_task_relationship():
    project = Project("Task Project")
    task = Task("First Task")
    project.add_task(task)
    assert len(project.tasks) == 1