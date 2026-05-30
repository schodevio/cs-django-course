```zsh
# New project
uv init

# Add dependency
uv add django

# Sync dependencies
uv sync

# Create Django project files
uv run django-admin startproject django_project .

# Run Django commands
uv run manage.py runserver
uv run manage.py startapp blog

uv run manage.py makemigrations
uv run manage.py migrate

uv run manage.py shell
```
