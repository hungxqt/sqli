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
    php artisan migrate:status > /dev/null 2>&1 || {
        echo "Database connection failed. Please check your MySQL configuration."
        exit 1
    }
    echo "Database connection successful"
}

setup_database() {
    php artisan migrate --force
    echo "Database setup completed"
}

start_debug_mode() {
    echo "Starting Laravel with Xdebug..."
    echo "Web: http://localhost:8000 | Debug: localhost:9003"
    
    export APP_ENV=local
    export APP_DEBUG=true
    exec php artisan serve --host=0.0.0.0 --port=8000
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
    "artisan")
        shift
        wait_for_host_mysql
        exec php artisan "$@"
        ;;
    *)
        echo "Available commands:"
        echo "  debug (default) - Start Laravel in debug mode with Xdebug"
        echo "  test-connection - Test MySQL connection only"
        echo "  bash - Open bash shell"
        echo "  artisan [args] - Run Laravel artisan commands"
        exit 1
        ;;
esac
