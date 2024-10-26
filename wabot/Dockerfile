
FROM node:18

RUN apt-get update && apt-get install -y libnss3

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

CMD ["npm", "start"]
