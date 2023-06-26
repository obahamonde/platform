FROM node:14.15.4-alpine3.12

WORKDIR /app

COPY package.json /app

RUN npm install

EXPOSE 8080

COPY . /app

CMD ["npm", "run", "dev"]