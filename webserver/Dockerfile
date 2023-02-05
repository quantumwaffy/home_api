FROM nginx:latest

WORKDIR /webserver

COPY nginx.conf /etc/nginx/templates/nginx.conf.template

EXPOSE 80 443

CMD ["nginx"]