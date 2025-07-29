from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.views.decorators.clickjacking import xframe_options_deny, xframe_options_sameorigin
from labsPage.models import User, Email

def home(request):
    """Home page view"""
    return render(request, 'home.html')

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

def lab_unified(request):
    """Unified SQL Injection Lab - All injection types in one interface"""
    result = None
    results = None
    error = None
    query_executed = None
    lab_type = request.GET.get('type', 'string')
    
    # String-based injection (Lab 1)
    if lab_type == 'string':
        username = request.GET.get('username', '')
        if username:
            try:
                raw_query = f"SELECT id, username, password FROM {User._meta.db_table} WHERE username = '{username}'"
                query_executed = raw_query
                
                with connection.cursor() as cursor:
                    cursor.execute(raw_query)
                    result = cursor.fetchone()
                    
            except Exception as e:
                error = str(e)
        
        context = {
            'lab_type': lab_type,
            'username': username,
            'result': result,
            'error': error,
            'query_executed': query_executed
        }
    
    # Numeric injection (Lab 2)
    elif lab_type == 'numeric':
        user_id = request.GET.get('id', '')
        if user_id:
            try:
                raw_query = f"SELECT id, username, password FROM {User._meta.db_table} WHERE id = {user_id}"
                query_executed = raw_query
                
                with connection.cursor() as cursor:
                    cursor.execute(raw_query)
                    result = cursor.fetchone()
                    
            except Exception as e:
                error = str(e)
        
        context = {
            'lab_type': lab_type,
            'user_id': user_id,
            'result': result,
            'error': error,
            'query_executed': query_executed
        }
    
    # Search-based injection (Lab 3)
    elif lab_type == 'search':
        search_term = request.GET.get('search', '')
        if search_term:
            try:
                raw_query = f"SELECT id, username, password FROM {User._meta.db_table} WHERE username LIKE '%{search_term}%'"
                query_executed = raw_query
                
                with connection.cursor() as cursor:
                    cursor.execute(raw_query)
                    results = cursor.fetchall()
                    
            except Exception as e:
                error = str(e)
        
        context = {
            'lab_type': lab_type,
            'search_term': search_term,
            'results': results,
            'error': error,
            'query_executed': query_executed
        }
    
    # Login-based injection (Lab 4)
    elif lab_type == 'login':
        username = request.POST.get('username', '') or request.GET.get('username', '')
        password = request.POST.get('password', '') or request.GET.get('password', '')
        
        if username and password:
            try:
                raw_query = f"SELECT id, username, password FROM {User._meta.db_table} WHERE username = '{username}' AND password = '{password}'"
                query_executed = raw_query
                
                with connection.cursor() as cursor:
                    cursor.execute(raw_query)
                    result = cursor.fetchone()
                    
            except Exception as e:
                error = str(e)
        
        context = {
            'lab_type': lab_type,
            'username': username,
            'password': password,
            'result': result,
            'error': error,
            'query_executed': query_executed
        }
    
    # Blind SQL Injection (Advanced Lab 1)
    elif lab_type == 'blind':
        user_id = request.GET.get('id', '')
        if user_id:
            try:
                raw_query = f"SELECT id, username FROM {User._meta.db_table} WHERE id = {user_id}"
                query_executed = raw_query
                
                with connection.cursor() as cursor:
                    cursor.execute(raw_query)
                    result = cursor.fetchone()
                    # For blind injection, we only show if result exists or not
                    result = "User exists" if result else "User not found"
                    
            except Exception as e:
                error = str(e)
        
        context = {
            'lab_type': lab_type,
            'user_id': user_id,
            'result': result,
            'error': error,
            'query_executed': query_executed
        }
    
    # Time-based SQL Injection (Advanced Lab 2)
    elif lab_type == 'time':
        user_id = request.GET.get('id', '')
        if user_id:
            try:
                raw_query = f"SELECT id, username FROM {User._meta.db_table} WHERE id = {user_id}"
                query_executed = raw_query
                
                import time
                start_time = time.time()
                
                with connection.cursor() as cursor:
                    cursor.execute(raw_query)
                    result = cursor.fetchone()
                    
                end_time = time.time()
                execution_time = round((end_time - start_time) * 1000, 2)  # Convert to milliseconds
                
                result = f"Query executed in {execution_time}ms"
                    
            except Exception as e:
                error = str(e)
        
        context = {
            'lab_type': lab_type,
            'user_id': user_id,
            'result': result,
            'error': error,
            'query_executed': query_executed
        }
    
    # Union-based SQL Injection (Advanced Lab 3)
    elif lab_type == 'union':
        user_id = request.GET.get('id', '')
        if user_id:
            try:
                raw_query = f"SELECT id, username, password FROM {User._meta.db_table} WHERE id = {user_id}"
                query_executed = raw_query
                
                with connection.cursor() as cursor:
                    cursor.execute(raw_query)
                    results = cursor.fetchall()
                    
            except Exception as e:
                error = str(e)
        
        context = {
            'lab_type': lab_type,
            'user_id': user_id,
            'results': results,
            'error': error,
            'query_executed': query_executed
        }
    
    # Boolean-based Blind SQL Injection (Advanced Lab 4)
    elif lab_type == 'boolean':
        user_id = request.GET.get('id', '')
        if user_id:
            try:
                raw_query = f"SELECT COUNT(*) FROM {User._meta.db_table} WHERE id = {user_id}"
                query_executed = raw_query
                
                with connection.cursor() as cursor:
                    cursor.execute(raw_query)
                    count = cursor.fetchone()[0]
                    result = "True" if count > 0 else "False"
                    
            except Exception as e:
                error = str(e)
        
        context = {
            'lab_type': lab_type,
            'user_id': user_id,
            'result': result,
            'error': error,
            'query_executed': query_executed
        }
    
    # Reflect Echo Injection
    elif lab_type == 'reflect':
        username = request.GET.get('username', '')
        if username:
            try:
                raw_query = f"SELECT id, username, password FROM {User._meta.db_table} WHERE username = '{username}'"
                query_executed = raw_query
                
                with connection.cursor() as cursor:
                    cursor.execute(raw_query)
                    result = cursor.fetchone()
                    
            except Exception as e:
                error = str(e)
        
        context = {
            'lab_type': lab_type,
            'username': username,
            'result': result,
            'error': error,
            'query_executed': query_executed
        }
    
    else:
        # Default to union lab if invalid type
        context = {
            'lab_type': 'union',
            'user_id': '',
            'result': None,
            'error': None,
            'query_executed': None
        }
    
    return render(request, 'lab-unified.html', context)

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
