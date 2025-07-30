#!/usr/bin/env python
import os
import sys
import debugpy

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        if os.environ.get('RUN_MAIN') != 'true':
            try:
                debugpy.listen(("0.0.0.0", 6000))
                print("Debug server listening on 0.0.0.0:6000")
                print("Connect VS Code debugger to continue...")
                print(f"Working directory: {os.getcwd()}")
                print(f"Python path: {sys.path}")
            except (RuntimeError, Exception) as e:
                print(f"Debug setup error: {e}")
    main()
