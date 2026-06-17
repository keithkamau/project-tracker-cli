# Project Management CLI Tool

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Create data directory: `mkdir data`
3. Run: `python main.py`

## Commands

### Users

- Add user: `python main.py add-user --name "Alex" --email "alex@email.com"`
- List users: `python main.py list-users`

### Projects

- Add project: `python main.py add-project --user "Alex" --title "CLI Tool" --description "Build CLI" --due "2024-12-01"`
- List projects: `python main.py list-projects --user "Alex"`

### Tasks

- Add task: `python main.py add-task --project "CLI Tool" --title "Setup argparse" --assigned "Alex"`
- Complete task: `python main.py complete-task --project "CLI Tool" --task "Setup argparse"`
- List tasks: `python main.py list-tasks --project "CLI Tool"`

## Features

- User, project, and task management
- JSON file persistence
- Pretty-printed tables using tabulate
- Basic relationship tracking

## Known Issues

- No input validation for emails
- Data file path is hardcoded
- Limited error handling for edge cases