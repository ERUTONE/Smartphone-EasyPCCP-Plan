FROM node
WORKDIR /projects
RUN npm install -g @angular/cli
EXPOSE 4200
