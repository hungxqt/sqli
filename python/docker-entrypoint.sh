#!/bin/bash
set -e

echo "========================================"
echo "  Python Django SQLi Lab - Host MySQL  "
echo "========================================"

# Function to wait for host MySQL
wait_for_host_mysql() {
    echo "Waiting for MySQL on host machine (${DB_HOST:-host.docker.internal}:${DB_PORT:-3306})..."
    
    # Try different host resolution methods
    local mysql_host="${DB_HOST:-host.docker.internal}"
    
    # On Linux, try to use host.docker.internal or fallback to gateway IP
    if [ "$mysql_host" = "host.docker.internal" ]; then
        # Check if host.docker.internal is available
        if ! ping -c 1 host.docker.internal >/dev/null 2>&1; then
            echo "host.docker.internal not available, trying gateway IP..."
            # Get the gateway IP (Docker host)
            local gateway_ip=$(ip route | awk '/default/ { print $3; exit }')
            if [ -n "$gateway_ip" ]; then
                mysql_host="$gateway_ip"
                echo "Using gateway IP: $gateway_ip"
            else
                echo "Warning: Could not determine host IP, using host.docker.internal anyway"
                mysql_host="host.docker.internal"
            fi
        fi
    fi
    
    local retries=0
    local max_retries=60
    
    while ! nc -z "$mysql_host" "${DB_PORT:-3306}"; do
        retries=$((retries + 1))
        if [ $retries -gt $max_retries ]; then
            echo "ERROR: MySQL on host machine is not available after $max_retries attempts"
            echo "Please ensure:"
            echo "1. MySQL is running on your host machine"
            echo "2. MySQL is configured to accept connections from Docker containers"
            echo "3. Firewall allows connections on port ${DB_PORT:-3306}"
            echo ""
            echo "MySQL Configuration Tips:"
            echo "- Edit my.cnf/my.ini: bind-address = 0.0.0.0"
            echo "- Grant privileges: GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'password';"
            echo "- Check if MySQL is listening: netstat -tulpn | grep 3306"
            exit 1
        fi
        echo "MySQL is unavailable - sleeping (attempt $retries/$max_retries)"
        sleep 2
    done
    
    echo "MySQL on host machine is up - continuing"
    
    # Update DB_HOST environment variable if we changed it
    if [ "$mysql_host" != "${DB_HOST:-host.docker.internal}" ]; then
        export DB_HOST="$mysql_host"
    fi
}

# Function to test database connection
test_database_connection() {
    echo "Testing database connection..."
    python << EOF
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python.settings')
django.setup()

from django.db import connection
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print(f"Database connection successful: {result}")
except Exception as e:
    print(f"Database connection failed: {e}")
    print("Please check your MySQL configuration on the host machine")
    exit(1)
EOF
}

# Function to setup database
setup_database() {
    echo "Setting up database..."
    
    # Run migrations
    python manage.py makemigrations --noinput || true
    python manage.py migrate --noinput
    
    # Create superuser if it doesn't exist
    python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists: admin/admin123')
EOF
}

# Function to start debug mode
start_debug_mode() {
    echo ""
    echo "Starting Django in DEBUG mode with remote debugging..."
    echo "Debug server listening on: 0.0.0.0:6000"
    echo "Web server listening on: 0.0.0.0:8000"
    echo "MySQL connection: ${DB_HOST:-host.docker.internal}:${DB_PORT:-3306}"
    echo ""
    echo "VS Code Remote Debugging:"
    echo "1. Set breakpoints in your Python code"
    echo "2. Use 'Python: Remote Attach' configuration" 
    echo "3. Connect to localhost:6000"
    echo ""
    echo "Access URLs:"
    echo "   - Web App: http://localhost:8000"
    echo "   - Admin: http://localhost:8000/admin (admin/admin123)"
    echo ""
    
    export DEBUG_MODE=true
    exec python manage.py runserver 0.0.0.0:8000
}

# Function to start development mode
start_dev_mode() {
    echo "Starting Django in DEVELOPMENT mode..."
    echo "Web server listening on: 0.0.0.0:8000"
    echo "MySQL connection: ${DB_HOST:-host.docker.internal}:${DB_PORT:-3306}"
    
    export DEBUG_MODE=false
    exec python manage.py runserver 0.0.0.0:8000
}

# Function to start production mode
start_production_mode() {
    echo "Starting Django in PRODUCTION mode..."
    echo "Collecting static files..."
    python manage.py collectstatic --noinput
    
    echo "Starting Gunicorn server..."
    exec gunicorn python.wsgi:application \
        --bind 0.0.0.0:8000 \
        --workers 3 \
        --log-level info \
        --access-logfile - \
        --error-logfile -
}

# Function to show connection info
show_connection_info() {
    echo "Connection Information:"
    echo "   - Database Host: ${DB_HOST:-host.docker.internal}"
    echo "   - Database Port: ${DB_PORT:-3306}"
    echo "   - Database Name: ${DB_NAME:-django}"
    echo "   - Database User: ${DB_USER:-root}"
    echo "   - Debug Mode: ${DEBUG_MODE:-true}"
    echo ""
}

# Main execution
show_connection_info

case "$1" in
    "debug")
        wait_for_host_mysql
        test_database_connection
        setup_database
        start_debug_mode
        ;;
    "dev")
        wait_for_host_mysql
        test_database_connection
        setup_database
        start_dev_mode
        ;;
    "production")
        wait_for_host_mysql
        test_database_connection
        setup_database
        start_production_mode
        ;;
    "test-connection")
        wait_for_host_mysql
        test_database_connection
        echo "Connection test completed successfully"
        ;;
    "bash")
        exec /bin/bash
        ;;
    "python")
        shift
        exec python "$@"
        ;;
    "manage")
        shift
        wait_for_host_mysql
        exec python manage.py "$@"
        ;;
    *)
        if [ -z "$1" ]; then
            # Default behavior
            wait_for_host_mysql
            test_database_connection
            setup_database
            start_debug_mode
        else
            # Execute custom command
            exec "$@"
        fi
        ;;
esac
