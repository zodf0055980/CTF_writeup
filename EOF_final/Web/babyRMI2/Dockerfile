FROM openjdk:8u111-alpine

RUN apk add --update curl 
RUN apk add --update sudo

COPY flag /flag
COPY src /src
RUN cd /src && javac -cp ".:deps/*" com/kaibro/rmi/Server.java /src/com/kaibro/rmi/RMIInterface.java

CMD ["/src/runServer.sh"]
