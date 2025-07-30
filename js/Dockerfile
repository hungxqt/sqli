FROM node:18-alpine

RUN apk add --no-cache \
    mysql-client \
    netcat-openbsd

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN chmod +x /app/docker-entrypoint.sh

EXPOSE 3000 9002

ENTRYPOINT ["/app/docker-entrypoint.sh"]

CMD ["debug"]
