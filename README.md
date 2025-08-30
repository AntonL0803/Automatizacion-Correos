# 📧 Sistema de Automatización de Correos - Tavolo Casa

Sistema completo para automatizar el envío de correos masivos para Tavolo Casa, la tienda del confort especializada en productos para el descanso.

## 🚀 Características

- ✅ Envío masivo personalizado de correos
- ✅ Plantillas HTML profesionales y responsivas
- ✅ Personalización automática con datos del destinatario
- ✅ Soporte para archivos adjuntos
- ✅ Sistema de logging y control de errores
- ✅ Configuración flexible para diferentes proveedores de email
- ✅ Protección anti-spam con retrasos configurables
- ✅ Estadísticas de envío en tiempo real

## 📁 Estructura de Archivos

```
ProyectoTavoloCasaGmail/
├── email_sender.py          # Script principal
├── config.json             # Configuración de credenciales
├── plantilla_correo.html    # Plantilla HTML del correo
├── lista_correos_ejemplo.csv # Ejemplo de lista de correos
├── setup.py                # Asistente de configuración
├── README.md               # Esta documentación
└── requirements.txt        # Dependencias de Python
```

## 🛠️ Instalación

### 1. Requisitos Previos
- Python 3.7 o superior
- Cuenta de correo con acceso SMTP habilitado

### 2. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 3. Configuración Inicial
Ejecuta el asistente de configuración:
```bash
python setup.py
```

Este script te guiará para:
- Configurar tus credenciales de email
- Probar la conexión SMTP
- Verificar que todos los archivos estén en su lugar

## 📋 Preparar Lista de Correos

Crea un archivo CSV llamado `lista_correos.csv` con el siguiente formato:

```csv
email,nombre,apellido,empresa
juan.perez@email.com,Juan,Pérez,Empresa ABC
maria.garcia@gmail.com,María,García,Decoraciones XYZ
carlos.rodriguez@outlook.com,Carlos,Rodríguez,Hogar y Confort
```

### Campos del CSV:
- **email** (obligatorio): Dirección de correo electrónico
- **nombre** (opcional): Nombre del destinatario
- **apellido** (opcional): Apellido del destinatario  
- **empresa** (opcional): Nombre de la empresa

## 🎯 Uso del Sistema

### Envío Básico
```bash
python email_sender.py
```

### Personalización en la Plantilla
La plantilla HTML admite las siguientes variables:

- `{{NOMBRE}}` - Nombre del destinatario
- `{{APELLIDO}}` - Apellido del destinatario
- `{{EMPRESA}}` - Empresa del destinatario
- `{{NOMBRE_COMPLETO}}` - Nombre y apellido completos
- `{{FECHA}}` - Fecha actual
- `{{AÑO}}` - Año actual

## ⚙️ Configuración para Gmail

### Paso a Paso para Gmail:

1. **Habilitar verificación en dos pasos**:
   - Ve a tu cuenta de Google
   - Seguridad → Verificación en 2 pasos
   - Actívala si no está habilitada

2. **Generar contraseña de aplicación**:
   - Ve a Seguridad → Contraseñas de aplicaciones
   - Selecciona "Correo" y tu dispositivo
   - Copia la contraseña de 16 caracteres generada

3. **Configurar el sistema**:
   - Ejecuta `python setup.py`
   - Usa tu email de Gmail
   - **IMPORTANTE**: Usa la contraseña de aplicación, NO tu contraseña normal

### Otros Proveedores

#### Outlook/Hotmail
```json
{
    "smtp_server": "smtp-mail.outlook.com", 
    "smtp_port": 587
}
```

#### Yahoo Mail
```json
{
    "smtp_server": "smtp.mail.yahoo.com",
    "smtp_port": 587
}
```

## 📊 Monitoreo y Logging

El sistema genera automáticamente:
- **Progreso en consola**: Muestra cada envío en tiempo real
- **Archivo de log**: `email_log_YYYYMMDD_HHMMSS.log`
- **Estadísticas finales**: Resumen completo al finalizar

Ejemplo de salida:
```
✅ [1/50] Enviado a juan.perez@email.com
✅ [2/50] Enviado a maria.garcia@gmail.com
❌ [3/50] Falló envío a email_invalido@

📊 RESUMEN DEL ENVÍO:
Total contactos: 50
Enviados exitosamente: 48
Fallos: 2
Tasa de éxito: 96.0%
```

## 🚨 Límites y Consideraciones

### Límites de Gmail
- **Cuentas gratuitas**: 500 correos/día
- **Google Workspace**: 2,000 correos/día
- **Recomendación**: No más de 50 correos/hora

### Protección Anti-Spam
- Retraso de 2 segundos entre envíos (configurable)
- Personalización de contenido para cada destinatario
- Logging completo para auditoría

## 🛡️ Cumplimiento Legal

**IMPORTANTE**: Este sistema debe usarse responsablemente:

- ✅ **Consentimiento**: Solo envía a personas que han dado su consentimiento
- ✅ **RGPD**: Cumple con el Reglamento General de Protección de Datos
- ✅ **Opt-out**: Incluye siempre opción de cancelar suscripción
- ✅ **Identificación**: El remitente debe estar claramente identificado

## 🐛 Solución de Problemas

### "Authentication failed"
- Verifica que uses contraseña de aplicación para Gmail
- Comprueba que 2FA esté habilitado
- Revisa usuario y contraseña

### "Connection refused"
- Verifica la configuración SMTP
- Comprueba tu conexión a internet
- Algunos ISP bloquean puertos SMTP

### Correos en SPAM
- Aumenta el retraso entre envíos
- Personaliza más el contenido
- Verifica configuración SPF/DKIM del dominio

### "File not found"
- Asegúrate de que `lista_correos.csv` existe
- Verifica que `plantilla_correo.html` está presente
- Ejecuta `python setup.py` para verificar archivos

## 📱 Contacto Tavolo Casa

- 📧 **Email**: info@tavolocasa.com
- 📞 **Teléfono**: 655 586 462
- 🌐 **Web**: https://tavolocasa.com

---

**Sistema desarrollado para Tavolo Casa - La tienda del confort** 🏠✨

*Especialistas en cojines, almohadas, edredones, rellenos y artículos para mascotas*
