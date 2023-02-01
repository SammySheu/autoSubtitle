FROM mysql

COPY ./database_user.sql /docker-entrypoint-initdb.d

ENV MYSQL_ROOT_PASSWORD=my-secret-pw \
    MYSQL_DATABASE=maindb \
    MYSQL_USER=developer \
    MYSQL_PASSWORD=password