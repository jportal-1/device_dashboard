FROM node:22.5-bookworm-slim AS build

COPY . /frontend
WORKDIR /frontend/deviceapp
RUN npm install
RUN npm install -g @angular/cli
RUN NG_CLI_ANALYTICS=false ng build --configuration=production

FROM nginx:1.27.0-bookworm
RUN rm -rf /usr/share/nginx/html/*
COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=build /frontend/deviceapp/dist/deviceapp/* /usr/share/nginx/html/
