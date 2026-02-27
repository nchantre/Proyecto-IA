Docker: MySQL con dos bases de datos

Archivos añadidos:
- `Dockerfile` : imagen basada en `mysql:8.0` que copia scripts de inicialización.
- `docker-entrypoint-initdb.d/init-db.sql` : crea las bases de datos `ia-person` y `ia_person2` y un usuario `ia_user`.

Build y run (ejemplo):

1) Construir la imagen:

```powershell
docker build -t my-mysql-init .
```

2) Ejecutar el contenedor (usa el mismo comando que diste, cambiando la imagen):

```powershell
docker run --name some-mysql-5 \
  -e MYSQL_ROOT_PASSWORD=ejemplo124 \
  -v mysql_data_5:/var/lib/mysql \
  -v /mnt/c/BD-almacenamiento:/backup \
  -p 3315:3306 \
  -d my-mysql-init
```

Notas importantes:
- Los scripts en `docker-entrypoint-initdb.d` se ejecutan solo cuando la carpeta de datos (`/var/lib/mysql`) está vacía (primera inicialización del volumen). Para re-ejecutarlos borra el volumen `mysql_data_5` o usa un nuevo volumen.
- Ajusta contraseñas y nombres de usuario en `init-db.sql` según tu política de seguridad.
