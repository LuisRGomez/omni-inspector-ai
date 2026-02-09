# Comandos Utiles SSH MCP

Una vez configurado tu servidor SSH MCP, puedes usar estos comandos en lenguaje natural con Kiro:

## Gestion de Archivos y Directorios

```
"Lista los archivos en /var/www"
"Muestra el contenido del directorio /home"
"Crea un directorio llamado backups en /opt"
"Elimina el archivo /tmp/test.txt"
"Muestra el contenido del archivo /etc/hosts"
"Busca archivos .log en /var/log"
"Comprime el directorio /var/www en un archivo tar.gz"
```

## Monitoreo del Sistema

```
"Muestra el uso de disco"
"Verifica el uso de memoria RAM"
"Muestra los procesos en ejecucion"
"Verifica la carga del CPU"
"Muestra el uptime del servidor"
"Verifica cuanto espacio libre hay en disco"
"Muestra las conexiones de red activas"
```

## Gestion de Servicios

```
"Verifica si nginx esta corriendo"
"Reinicia el servicio apache2"
"Detiene el servicio mysql"
"Inicia el servicio docker"
"Muestra el estado de todos los servicios"
"Verifica los logs de nginx"
"Habilita el servicio ssh al inicio"
```

## Gestion de Paquetes

```
"Actualiza la lista de paquetes"
"Instala python3-pip"
"Actualiza todos los paquetes del sistema"
"Busca el paquete nginx"
"Desinstala apache2"
"Verifica que version de node esta instalada"
```

## Usuarios y Permisos

```
"Lista todos los usuarios del sistema"
"Crea un usuario llamado developer"
"Cambia los permisos de /var/www a 755"
"Muestra quien esta conectado al servidor"
"Verifica los grupos del usuario admin"
"Cambia el propietario de /var/www a www-data"
```

## Red y Conectividad

```
"Muestra la configuracion de red"
"Verifica la IP del servidor"
"Haz ping a google.com"
"Muestra las reglas del firewall"
"Verifica los puertos abiertos"
"Muestra la tabla de enrutamiento"
```

## Logs y Diagnostico

```
"Muestra los ultimos 20 logs del sistema"
"Verifica los logs de error de apache"
"Muestra los logs de autenticacion SSH"
"Busca errores en los logs del kernel"
"Muestra los logs de cron"
```

## Base de Datos (si tienes MySQL/PostgreSQL)

```
"Verifica si MySQL esta corriendo"
"Muestra las bases de datos"
"Haz un backup de la base de datos miapp"
"Verifica el estado de PostgreSQL"
"Muestra los usuarios de MySQL"
```

## Docker (si tienes Docker instalado)

```
"Lista los contenedores de Docker"
"Muestra las imagenes de Docker"
"Inicia el contenedor web"
"Detiene todos los contenedores"
"Muestra los logs del contenedor nginx"
"Verifica el uso de recursos de Docker"
```

## Git y Desarrollo

```
"Clona el repositorio https://github.com/user/repo en /opt"
"Actualiza el repositorio en /var/www/app"
"Muestra el estado de git en /opt/proyecto"
"Verifica la version de git instalada"
```

## Backups y Compresion

```
"Crea un backup de /var/www en /backups"
"Comprime el directorio /home/user/docs"
"Descomprime el archivo backup.tar.gz"
"Copia /var/www a /backups/www-backup"
```

## Seguridad

```
"Muestra los intentos fallidos de login SSH"
"Verifica las reglas de iptables"
"Lista los puertos abiertos"
"Muestra los procesos que escuchan en puertos"
"Verifica las conexiones SSH activas"
```

## Tareas Programadas (Cron)

```
"Muestra las tareas cron del usuario"
"Lista todas las tareas cron del sistema"
"Verifica los logs de cron"
```

## Rendimiento

```
"Muestra los procesos que mas CPU consumen"
"Verifica los procesos que mas memoria usan"
"Muestra el uso de disco por directorio"
"Verifica el I/O del disco"
```

---

## Consejos

1. **Se especifico**: Cuanto mas claro seas, mejor sera el resultado
2. **Usa rutas completas**: Especifica rutas absolutas cuando sea posible
3. **Verifica antes de ejecutar**: Para comandos destructivos, pide primero ver que se va a hacer
4. **Combina comandos**: Puedes pedir multiples acciones en una sola instruccion

---

## Ejemplos de Comandos Complejos

```
"Busca todos los archivos .log mayores a 100MB en /var/log y muestrame sus tamaños"

"Verifica si nginx esta corriendo, si no lo esta, inicialo y muestrame los logs"

"Crea un backup de /var/www, comprimelo y muestrame el tamaño del archivo resultante"

"Lista los 10 procesos que mas memoria consumen y muestrame sus PIDs"

"Busca en los logs de apache los errores 500 de las ultimas 24 horas"
```

---

## Nota Importante

Recuerda que estos comandos se ejecutaran en tu servidor remoto con los permisos del usuario configurado. Si necesitas ejecutar comandos con sudo, asegurate de haber configurado `--sudoPassword` en tu archivo de configuracion MCP.
