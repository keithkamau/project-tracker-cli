class Task:
    def __init__(self, title, assigned_to="Unassigned"):
        if not title or len(title.strip()) < 2:
            raise ValueError("Task title must be at least 2 characters")
        self.title = title
        self.status = "Pending"
        self.assigned_to = assigned_to

    def complete(self):
        if self.status == "Completed":
            raise ValueError("Task is already completed")
        self.status = "Completed"

    def __str__(self):
        return f"Task: {self.title} [{self.status}]"