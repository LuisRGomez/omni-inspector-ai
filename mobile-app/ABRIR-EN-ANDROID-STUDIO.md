# 🚀 Abrir Proyecto en Android Studio

## MÉTODO FÁCIL Y RÁPIDO

### Paso 1: Abrir Android Studio
1. Abre Android Studio
2. Click en "Open"
3. Navega a: `C:\Users\TitoGomez\Desktop\talos forencing\mobile-app\android`
4. Selecciona la carpeta `android`
5. Click "OK"

### Paso 2: Esperar Sync
- Android Studio sincronizará el proyecto automáticamente
- Esto tarda 2-3 minutos
- Verás una barra de progreso abajo

### Paso 3: Conectar Celular o Emulador

#### Opción A: Celular Real (RECOMENDADO)
1. Conecta tu celular por USB
2. Habilita "Depuración USB" en el celular
3. Acepta el permiso en el celular
4. Verás tu celular en el dropdown de Android Studio

#### Opción B: Emulador
1. Click en "Device Manager" (ícono de celular)
2. Click "Create Device"
3. Selecciona un dispositivo (ej: Pixel 5)
4. Selecciona una imagen del sistema (ej: API 33)
5. Click "Finish"

### Paso 4: Ejecutar
1. Click en el botón verde "Run" (▶️)
2. O presiona Shift+F10
3. Espera 2-5 minutos (primera vez)
4. ¡La app se instalará y abrirá automáticamente!

## VENTAJAS DE ESTE MÉTODO

✅ **Más rápido** - No necesitas comandos
✅ **Visual** - Ves todo en la interfaz
✅ **Debugging** - Puedes ver logs en tiempo real
✅ **Hot reload** - Cambios se reflejan rápido
✅ **Emulador incluido** - No necesitas celular

## GENERAR APK DESDE ANDROID STUDIO

### Para APK de Prueba:
1. Menu: Build > Build Bundle(s) / APK(s) > Build APK(s)
2. Espera 2-3 minutos
3. Click en "locate" cuando termine
4. ¡APK listo!

### Para APK de Producción:
1. Menu: Build > Generate Signed Bundle / APK
2. Selecciona "APK"
3. Click "Next"
4. Crea un keystore nuevo (o usa uno existente)
5. Click "Next" > "Finish"
6. ¡APK firmado listo!

## LOGS EN TIEMPO REAL

En Android Studio verás:
- Logcat (logs de la app)
- Errores de compilación
- Warnings
- Mensajes de debug

Busca por "Omni" o "AWS" para ver logs específicos.

## SHORTCUTS ÚTILES

- **Run:** Shift+F10
- **Debug:** Shift+F9
- **Stop:** Ctrl+F2
- **Logcat:** Alt+6
- **Build:** Ctrl+F9

## TROUBLESHOOTING

### "Gradle sync failed"
- File > Invalidate Caches > Invalidate and Restart

### "SDK not found"
- File > Project Structure > SDK Location
- Verifica que apunte a: `C:\Users\TitoGomez\AppData\Local\Android\Sdk`

### "Device offline"
- Desconecta y reconecta el celular
- Revoca permisos USB y acepta de nuevo

## 🎯 RESULTADO

Con Android Studio:
- Compilas más rápido
- Ves errores en tiempo real
- Debuggeas fácilmente
- Generas APK con un click

**¡Mucho más fácil que la línea de comandos!**
