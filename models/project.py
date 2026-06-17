class Project:
    def __init__(self, title, description="", due_date="No deadline"):
        if not title or len(title.strip()) < 2:
            raise ValueError("Project title must be at least 2 characters")
        self.title = title
        self.description = description
        self.due_date = due_date
        self._tasks = []

    @property
    def tasks(self):
        return self._tasks

    def add_task(self, task):
        if any(t.title == task.title for t in self._tasks):
            raise ValueError(f"Task '{task.title}' already exists in this project")
        self._tasks.append(task)

    def __str__(self):
        return f"Project: {self.title} (Due: {self.due_date})"