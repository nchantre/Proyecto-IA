FROM mysql:8.0

# Definimos una contraseña por defecto; puede sobrescribirse con -e MYSQL_ROOT_PASSWORD
ENV MYSQL_ROOT_PASSWORD=ejemplo124

# Copiamos los scripts de inicialización que crearán las bases de datos al arrancar
COPY docker-entrypoint-initdb.d /docker-entrypoint-initdb.d

VOLUME ["/var/lib/mysql"]
EXPOSE 3306

CMD ["mysqld"]
