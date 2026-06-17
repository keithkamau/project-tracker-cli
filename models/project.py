class Project:
    def __init__(self, title, description="", due_date="No deadline"):
        self.title = title
        self.description = description
        self.due_date = due_date
        self._tasks = []

    @property
    def tasks(self):
        return self._tasks

    def add_task(self, task):
        self._tasks.append(task)

    def __str__(self):
        return f"Project: {self.title} (Due: {self.due_date})"