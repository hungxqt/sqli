#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import debugpy

def main():
    """Run administrative tasks."""
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
                print("Attach VS Code debugger to continue...")

                # debugpy.wait_for_client()
            except (RuntimeError, Exception) as e:
                print(f"Debug setup error: {e}")
    main()
