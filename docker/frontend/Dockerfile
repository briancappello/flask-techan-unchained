FROM node:22-trixie

# https://debiansupport.com/mirrors/
# RUN sed -i -e 's/deb.debian.org/archive.debian.org/g' /etc/apt/sources.list

RUN apt-get update && \
    apt-get install -y jq inotify-tools && \
    rm -fr /var/lib/apt/lists/*

WORKDIR /home/node

RUN chown -R node:node $(npm config get prefix)/lib/node_modules
RUN chown -R node:node $(npm config get prefix)/bin
RUN chown -R node:node $(npm config get prefix)/share

COPY package.json .
COPY package-lock.json .
COPY vite.config.js .
COPY docker/frontend/entrypoint.sh .
RUN chown -R node:node /home/node

# very important for npm install to work!
USER node

RUN npm install

COPY frontend /home/node/frontend
COPY static /home/node/static

EXPOSE 8888
ENTRYPOINT ["bash", "entrypoint.sh"]
