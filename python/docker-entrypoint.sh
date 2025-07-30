#!/bin/bash
set -e

wait_for_host_mysql() {
    echo "Waiting for MySQL on ${DB_HOST:-host.docker.internal}:${DB_PORT:-3306}..."
    
    local mysql_host="${DB_HOST:-host.docker.internal}"
    
    if [ "$mysql_host" = "host.docker.internal" ]; then
        if ! ping -c 1 host.docker.internal >/dev/null 2>&1; then
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
        sleep 2
    done
    
    if [ "$mysql_host" != "${DB_HOST:-host.docker.internal}" ]; then
        export DB_HOST="$mysql_host"
    fi
}

test_database_connection() {
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

setup_database() {
    python manage.py makemigrations --noinput || true
    python manage.py migrate --noinput
    
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

start_debug_mode() {
    echo "Starting Django with remote debugging..."
    echo "Web: http://localhost:8000 | Debug: localhost:6000 | Admin: admin/admin123"
    
    export DEBUG_MODE=true
    exec python manage.py runserver 0.0.0.0:8000
}

case "$1" in
    "debug"|"")
        wait_for_host_mysql
        test_database_connection
        setup_database
        start_debug_mode
        ;;
    "test-connection")
        wait_for_host_mysql
        test_database_connection
        echo "Connection test completed successfully"
        ;;
    "bash")
        exec /bin/bash
        ;;
    "manage")
        shift
        wait_for_host_mysql
        exec python manage.py "$@"
        ;;
    *)
        echo "Available commands:"
        echo "  debug (default) - Start Django in debug mode with remote debugging"
        echo "  test-connection - Test MySQL connection only"
        echo "  bash - Open bash shell"
        echo "  manage [args] - Run Django management commands"
        exit 1
        ;;
esac
