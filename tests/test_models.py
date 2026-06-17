import pytest
from models.user import User
from models.project import Project
from models.task import Task

def test_user_creation():
    user = User("Alice", "alice@email.com")
    assert user.name == "Alice"
    assert user.email == "alice@email.com"

def test_user_empty_name():
    with pytest.raises(ValueError):
        User("", "alice@email.com")

def test_user_invalid_email():
    with pytest.raises(ValueError):
        User("Alice", "invalid-email")

def test_project_creation():
    project = Project("Test Project", "A test", "2024-12-31")
    assert project.title == "Test Project"
    assert project.description == "A test"

def test_project_empty_title():
    with pytest.raises(ValueError):
        Project("")

def test_task_creation():
    task = Task("Test Task")
    assert task.status == "Pending"
    task.complete()
    assert task.status == "Completed"

def test_task_complete_twice():
    task = Task("Test")
    task.complete()
    with pytest.raises(ValueError):
        task.complete()

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

def test_duplicate_project():
    user = User("Test", "test@email.com")
    project1 = Project("Same")
    user.add_project(project1)
    project2 = Project("Same")
    with pytest.raises(ValueError):
        user.add_project(project2)