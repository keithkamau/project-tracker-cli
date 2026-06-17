# Project Management CLI Tool

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run: `python main.py`
3. Optional: Set custom data directory with `export PROJECTS_DATA_DIR=/your/path`

## Features

- Email validation with regex
- Configurable data storage location via environment variable
- Atomic file writes to prevent corruption
- Backup of corrupted data files
- Input validation for names and titles
- Duplicate detection for users, projects, and tasks
- Helpful error messages and usage hints

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

## Error Handling

- Validates email format using regex
- Prevents duplicate entries
- Handles corrupted/missing data files gracefully
- Creates automatic backups when data files are corrupted
- Provides clear error messages for all failure cases

## Known Issues

- Large datasets may be slow (in-memory storage)
- No concurrency support