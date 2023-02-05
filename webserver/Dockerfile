FROM nginx:latest

WORKDIR /webserver

COPY . ./

EXPOSE 80 443

CMD ["nginx", "-c", "/webserver/nginx.conf"]