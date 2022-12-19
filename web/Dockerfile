FROM node:19.3.0-alpine3.16

WORKDIR /web

ENV PATH /web/node_modules/.bin:$PATH

EXPOSE 3000

COPY package.json package-lock.json ./

RUN npm install --silent

COPY . ./

CMD ["npm", "start"]
