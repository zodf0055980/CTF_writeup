FROM php:7.4.10-apache

# setup OS env
RUN apt update -y
RUN docker-php-ext-install mysqli
RUN docker-php-ext-enable mysqli

# setup web application
COPY ./src/ /var/www/html/

# setup flag
RUN echo "DEVCORE{flag}" > /flag
RUN chmod 0400 /flag
RUN chown root:root /flag
COPY readflag.c /readflag.c
RUN gcc -o /readflag /readflag.c
RUN chmod 4555 /readflag
