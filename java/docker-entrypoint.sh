#!/bin/bash

echo "Starting Java SQLi Labs..."

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
        echo "Starting Tomcat with Java debug on port 9001..."
        export MAVEN_OPTS="-Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=0.0.0.0:9001"
        exec mvn tomcat7:run
        ;;
    *)
        echo "Starting Tomcat normally..."
        exec mvn tomcat7:run
        ;;
esac
