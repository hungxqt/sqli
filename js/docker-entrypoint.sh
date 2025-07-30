#!/bin/sh

echo "Starting JavaScript SQLi Labs..."

wait_for_mysql() {
    echo "Waiting for MySQL to be ready..."
    while ! nc -z $DB_HOST $DB_PORT; do
        echo "MySQL is not ready yet. Waiting 2 seconds..."
        sleep 2
    done
    echo "MySQL is ready!"
}

wait_for_mysql

case "$1" in
    debug)
        echo "Starting Node.js in debug mode on port 9002..."
        exec node --inspect=0.0.0.0:9002 app.js
        ;;
    *)
        echo "Starting Node.js normally..."
        exec node app.js
        ;;
esac
