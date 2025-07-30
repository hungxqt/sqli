FROM openjdk:11-jdk-slim

RUN apt-get update && apt-get install -y \
    maven \
    netcat-traditional \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pom.xml .
RUN mvn dependency:go-offline -B

COPY . .

RUN chmod +x /app/docker-entrypoint.sh

EXPOSE 8000 9001

ENTRYPOINT ["/app/docker-entrypoint.sh"]

CMD ["debug"]
