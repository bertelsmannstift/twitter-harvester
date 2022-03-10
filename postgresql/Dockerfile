#FROM postgres:9.6
FROM postgres:14
MAINTAINER Open Knowledge

# Allow connections; we don't map out any ports so only linked docker containers can connect
RUN echo "host all  all    0.0.0.0/0  md5" >> /var/lib/postgresql/data/pg_hba.conf

# Customize default user/pass/db
# ENV POSTGRES_DB $POSTGRES_DB
# ENV POSTGRES_USER $POSTGRES_USER
ARG POSTGRES_PASSWORD

# Include table setup scripts
ADD ./postgresql/docker-entrypoint-initdb.d /docker-entrypoint-initdb.d
