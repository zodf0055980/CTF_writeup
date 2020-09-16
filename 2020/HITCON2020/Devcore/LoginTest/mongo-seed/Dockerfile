FROM mongo

COPY init.json /init.json
CMD mongoimport --host mongodb --db logintest --collection users --type json --file /init.json --jsonArray