FROM node:16-alpine


WORKDIR /usr/app
COPY ./ /usr/app
RUN npm install

CMD [ "node", "client_side_server.js" ]