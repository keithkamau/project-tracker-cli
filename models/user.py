import re

class User:
    def __init__(self, name, email):
        if not name or len(name.strip()) < 2:
            raise ValueError("Name must be at least 2 characters")
        if not self._validate_email(email):
            raise ValueError("Invalid email format")
        self.name = name
        self.email = email
        self._projects = []

    def _validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @property
    def projects(self):
        return self._projects

    def add_project(self, project):
        if any(p.title == project.title for p in self._projects):
            raise ValueError(f"Project '{project.title}' already exists for this user")
        self._projects.append(project)

    def __str__(self):
        return f"User: {self.name} ({self.email})"