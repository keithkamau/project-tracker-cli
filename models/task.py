class Task:
    def __init__(self, title, assigned_to="Unassigned"):
        self.title = title
        self.status = "Pending"
        self.assigned_to = assigned_to

    def complete(self):
        self.status = "Completed"

    def __str__(self):
        return f"Task: {self.title} [{self.status}]"