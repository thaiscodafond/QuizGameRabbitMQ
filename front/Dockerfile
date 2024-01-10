FROM node:16-alpine as BUILDER

COPY ./package.json ./package.json

RUN npm i

FROM nginx:alpine

COPY --from=BUILDER ./node_modules ./node_modules
COPY . /usr/share/nginx/html