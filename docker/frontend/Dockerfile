FROM node:14-bullseye

# https://debiansupport.com/mirrors/
# RUN sed -i -e 's/deb.debian.org/archive.debian.org/g' /etc/apt/sources.list

RUN apt-get update && \
    apt-get install -y jq inotify-tools python && \
    rm -fr /var/lib/apt/lists/*

RUN npm install -g npm@8

WORKDIR /home/node
RUN git clone https://github.com/briancappello/techan.js.git && \
    cd techan.js && \
    cat package.json | jq 'del(.devDependencies)' > package-new.json && \
    cp package-new.json package.json && \
    npm link && \
    cd /home/node && \
    chown -R node:node /home/node

# very important for npm install to work!
USER node

COPY package.json .
RUN npm install
RUN npm link techan

COPY frontend /home/node/frontend
COPY static /home/node/static

RUN npm run build:dll
EXPOSE 8888
CMD ["npm", "run", "start"]
