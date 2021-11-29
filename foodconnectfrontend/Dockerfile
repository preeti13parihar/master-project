# pull official base image
FROM node:14.17.3-alpine
RUN apk update
RUN apk --no-cache add curl nano
# set working directory
WORKDIR /fc-ui

# add `/app/node_modules/.bin` to $PATH
ENV PATH /fc-ui/node_modules/.bin:$PATH

# install app dependencies
COPY package.json ./
COPY package-lock.json ./
RUN npm install --silent
RUN npm install react-scripts@3.4.1 -g --silent

# add app
COPY . ./

# start app
# CMD ["npm", "run", "dev"]
RUN npm run build


# STAGE 2 - build the final image using a nginx web server 
# distribution and copy the react build files
FROM nginx:alpine
COPY ./dist /usr/share/nginx/html
# needed this to make React Router work properly 
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.conf /etc/nginx/conf.d
# Expose port 80 for HTTP Traffic 
EXPOSE 80
# start the nginx web server
CMD ["nginx", "-g", "daemon off;"]