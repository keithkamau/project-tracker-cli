class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self._projects = []

    @property
    def projects(self):
        return self._projects

    def add_project(self, project):
        self._projects.append(project)

    def __str__(self):
        return f"User: {self.name} ({self.email})"