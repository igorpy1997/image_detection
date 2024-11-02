# client/Dockerfile
FROM nginx:alpine

COPY ../api/templates/client.html /usr/share/nginx/html/index.html
COPY . /usr/share/nginx/html/

EXPOSE 80
