from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.views.decorators.clickjacking import xframe_options_deny, xframe_options_sameorigin
from labsPage.models import User, Email

def home(request):
    """Home page view"""
    return render(request, 'index.html')

def setup_db_view(request):
    logs = []
    action = request.GET.get('action')  # No default action - user must choose

    # Always check current database status
    try:
        user_count = User.objects.count()
        email_count = Email.objects.count()
        db_status = {
            'user_count': user_count,
            'email_count': email_count,
            'has_data': user_count > 0 or email_count > 0
        }
    except Exception as e:
        db_status = {
            'user_count': 0,
            'email_count': 0,
            'has_data': False,
            'error': str(e)
        }

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

    # Update database status after any operations
    try:
        user_count = User.objects.count()
        email_count = Email.objects.count()
        db_status = {
            'user_count': user_count,
            'email_count': email_count,
            'has_data': user_count > 0 or email_count > 0
        }
    except Exception as e:
        db_status = {
            'user_count': 0,
            'email_count': 0,
            'has_data': False,
            'error': str(e)
        }

    return render(request, 'setup-db.html', {'logs': logs, 'action': action, 'db_status': db_status})

def view_users(request):
    """View all users in the database"""
    users = User.objects.all()
    return render(request, 'view-users.html', {'users': users})

def view_emails(request):
    """View all emails in the database"""
    emails = Email.objects.all()
    return render(request, 'view-emails.html', {'emails': emails})

# Lab 1: UNION-based SQL Injection
def union_lab(request):
    user_id = request.GET.get('id')
    
    if not user_id:
        return render(request, 'union.html', {
            'results': [],
            'query_executed': None,
            'error': None,
            'user_id': None
        })

    query = f"SELECT id, username, password FROM {User._meta.db_table} WHERE id = {user_id}"
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
        
        return render(request, 'union.html', {
            'results': results,
            'query_executed': query,
            'error': None,
            'user_id': user_id
        })
    except Exception as e:
        return render(request, 'union.html', {
            'results': [],
            'query_executed': query,
            'error': str(e),
            'user_id': user_id
        })

# Lab 2: Error/Reflect-based SQL Injection
def reflect_lab(request):
    username = request.GET.get('username')
    
    if not username:
        return render(request, 'reflect.html', {
            'result': None,
            'query_executed': None,
            'error': None,
            'username': None
        })

    query = f"SELECT id, username, password FROM {User._meta.db_table} WHERE username = '{username}'"
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
        
        return render(request, 'reflect.html', {
            'result': result,
            'query_executed': query,
            'error': None,
            'username': username
        })
    except Exception as e:
        return render(request, 'reflect.html', {
            'result': None,
            'query_executed': query,
            'error': str(e),
            'username': username
        })

# Lab 3: Boolean-based Blind SQL Injection
def boolean_lab(request):
    user_id = request.GET.get('id')
    
    if not user_id:
        return render(request, 'boolean.html', {
            'result': None,
            'query_executed': None,
            'error': None,
            'user_id': None
        })

    query = f"SELECT COUNT(*) FROM {User._meta.db_table} WHERE id = {user_id}"
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            count = cursor.fetchone()[0]
            result = "True" if count > 0 else "False"
        
        return render(request, 'boolean.html', {
            'result': result,
            'query_executed': query,
            'error': None,
            'user_id': user_id
        })
    except Exception as e:
        return render(request, 'boolean.html', {
            'result': None,
            'query_executed': query,
            'error': str(e),
            'user_id': user_id
        })

# Lab 4: Time-based Blind SQL Injection
def time_lab(request):
    user_id = request.GET.get('id')
    
    if not user_id:
        return render(request, 'time.html', {
            'result': None,
            'query_executed': None,
            'error': None,
            'user_id': None
        })

    query = f"SELECT id, username FROM {User._meta.db_table} WHERE id = {user_id}"
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            cursor.fetchone()  # Execute but don't process result
    except Exception as e:
        # Suppress errors
        pass
    
    return render(request, 'time.html', {
        'result': 'query executed',
        'query_executed': query,
        'error': None,
        'user_id': user_id
    })

def lab_unified(request):
    """Unified SQL Injection Lab - All injection types in one interface"""
    lab_type = request.GET.get('type', '')
    
    if lab_type == 'union':
        return union_lab(request)
    elif lab_type == 'reflect':
        return reflect_lab(request)
    elif lab_type == 'boolean':
        return boolean_lab(request)
    elif lab_type == 'time':
        return time_lab(request)
    else:
        return home(request)

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
