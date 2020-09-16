FROM node:14.9.0-alpine3.11

COPY src/ /usr/src/app

WORKDIR /usr/src/app

RUN npm install -g nodemon
RUN npm install

ENV NODE_ENV=production
ENV MONGO_HOST=mongodb://mongodb:27017/
ENV MONGO_DATABASE=logintest
ENV PORT=3000

EXPOSE 3000

CMD [ "nodemon", "-L", "app.js" ]