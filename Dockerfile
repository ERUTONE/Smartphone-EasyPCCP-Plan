FROM node:12.18.3
WORKDIR /projects
RUN npm install -g @angular/cli
EXPOSE 4200
