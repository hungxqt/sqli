FROM openjdk:17-jdk-alpine

# Install Maven
RUN apk add --no-cache maven

# Set working directory
WORKDIR /app

# Copy pom.xml and download dependencies
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code
COPY src ./src

# Build the application
RUN mvn clean package -DskipTests

# Expose ports
EXPOSE 8080
EXPOSE 9003

# Set default debug options (can be overridden by environment variable)
ENV JAVA_DEBUG_OPTS=""

# Run the application with conditional debug support
CMD java $JAVA_DEBUG_OPTS -jar target/stored-procedure-sqli-1.0.0.jar
