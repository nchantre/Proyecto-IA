-- init-db.sql
-- Este script se ejecuta solo la primera vez que MySQL inicializa el volumen de datos.

CREATE DATABASE IF NOT EXISTS `ia-person` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS `ia_person2` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Opcional: crear un usuario con acceso a ambas bases (modifica contraseña si lo deseas)
CREATE USER IF NOT EXISTS 'ia_user'@'%' IDENTIFIED BY 'ia_pass';
GRANT ALL PRIVILEGES ON `ia-person`.* TO 'ia_user'@'%';
GRANT ALL PRIVILEGES ON `ia_person2`.* TO 'ia_user'@'%';
FLUSH PRIVILEGES;
