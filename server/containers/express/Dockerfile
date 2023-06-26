FROM node:14-alpine

WORKDIR /app

COPY package.json package.json

RUN npm install

COPY . .

EXPOSE 8080

CMD ["npm","run","dev"]
