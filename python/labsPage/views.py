from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from labsPage.models import User, Email

def home(request):
    """Home page view"""
    return render(request, 'home.html')

def setup_db_view(request):
    logs = []
    action = request.GET.get('action')  # No default action - user must choose

    # Only perform database operations if an action is specified
    if action:
        try:
            if action == 'reset':
                # Only reset/clear the database
                User.objects.all().delete()
                Email.objects.all().delete()
                
                # Reset auto-increment counters for MySQL
                with connection.cursor() as cursor:
                    try:
                        user_table = User._meta.db_table
                        email_table = Email._meta.db_table
                        
                        cursor.execute(f"ALTER TABLE {user_table} AUTO_INCREMENT = 1")
                        cursor.execute(f"ALTER TABLE {email_table} AUTO_INCREMENT = 1")
                        logs.append("MySQL auto-increment counters reset successfully")
                            
                    except Exception as e:
                        logs.append(f"Warning: Could not reset auto-increment counters: {str(e)}")
                
                logs.append("Database reset completed - All data removed and IDs reset")
                
            elif action == 'setup':
                # Reset data and auto-increment counters
                User.objects.all().delete()
                Email.objects.all().delete()
                
                # Reset auto-increment counters for MySQL
                with connection.cursor() as cursor:
                    try:
                        user_table = User._meta.db_table
                        email_table = Email._meta.db_table
                        
                        cursor.execute(f"ALTER TABLE {user_table} AUTO_INCREMENT = 1")
                        cursor.execute(f"ALTER TABLE {email_table} AUTO_INCREMENT = 1")
                        logs.append("MySQL auto-increment counters reset successfully")
                            
                    except Exception as e:
                        logs.append(f"Warning: Could not reset auto-increment counters: {str(e)}")
                
                logs.append("Database cleanup completed - Existing data removed and IDs reset")

                # Insert into users
                users = [
                    ("Dumb", "Dumb"), ("Angelina", "I-kill-you"),
                    ("Dummy", "p@ssword"), ("secure", "crappy"),
                    ("stupid", "stupidity"), ("superman", "genious"),
                    ("batman", "mob!le"), ("admin", "admin"),
                    ("admin1", "admin1"), ("admin2", "admin2"),
                    ("admin3", "admin3"), ("dhakkan", "dumbo"),
                    ("admin4", "admin4"),
                ]
                for u, p in users:
                    User.objects.create(username=u, password=p)
                logs.append("Successfully populated 'users' table with 13 test accounts")

                # Insert into emails
                emails = [
                    "Dumb@dhakkan.com", "Angel@iloveu.com",
                    "Dummy@dhakkan.local", "secure@dhakkan.local",
                    "stupid@dhakkan.local", "superman@dhakkan.local",
                    "batman@dhakkan.local", "admin@dhakkan.com"
                ]
                for e in emails:
                    Email.objects.create(email_id=e)
                logs.append("Successfully populated 'emails' table with 8 test records")
            
        except Exception as e:
            logs.append(f"Error during database operation: {str(e)}")

    return render(request, 'setup-db.html', {'logs': logs, 'action': action})

def view_users(request):
    """View all users in the database"""
    users = User.objects.all()
    return render(request, 'view-users.html', {'users': users})

def reset_db_view(request):
    """Reset database - clear all data and reset auto-increment counters"""
    logs = []
    
    try:
        # Get counts before deletion
        user_count = User.objects.count()
        email_count = Email.objects.count()
        
        # Reset data
        User.objects.all().delete()
        Email.objects.all().delete()
        logs.append(f"Deleted {user_count} users and {email_count} emails from database")
        
        # Reset auto-increment counters for MySQL
        with connection.cursor() as cursor:
            try:
                # Get the actual table names from Django's meta
                user_table = User._meta.db_table
                email_table = Email._meta.db_table
                
                # For MySQL - reset auto-increment counters
                cursor.execute(f"ALTER TABLE {user_table} AUTO_INCREMENT = 1")
                cursor.execute(f"ALTER TABLE {email_table} AUTO_INCREMENT = 1")
                logs.append("MySQL auto-increment counters reset to 1")
                    
            except Exception as e:
                logs.append(f"Warning: Could not reset auto-increment counters: {str(e)}")
        
        logs.append("Database reset completed successfully")
        
    except Exception as e:
        logs.append(f"Error during database reset: {str(e)}")

    return render(request, 'reset-db.html', {'logs': logs})
