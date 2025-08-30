#!/usr/bin/env python3
"""
Script de configuración inicial para el sistema de correos Tavolo Casa
Ayuda a configurar y verificar el sistema antes del primer uso
"""

import json
import os
import sys
import getpass
from email.utils import parseaddr
import smtplib
import ssl

def print_banner():
    """Muestra el banner de bienvenida"""
    print("="*60)
    print("🏠 SISTEMA DE CORREOS TAVOLO CASA")
    print("   Configuración Inicial")
    print("="*60)
    print()

def get_smtp_config(provider):
    """Retorna configuración SMTP según el proveedor"""
    configs = {
        "gmail": {
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "instructions": "Para Gmail necesitas una contraseña de aplicación. Ve a tu cuenta de Google > Seguridad > Contraseñas de aplicaciones"
        },
        "outlook": {
            "smtp_server": "smtp-mail.outlook.com",
            "smtp_port": 587,
            "instructions": "Para Outlook/Hotmail usa tu contraseña normal"
        },
        "yahoo": {
            "smtp_server": "smtp.mail.yahoo.com", 
            "smtp_port": 587,
            "instructions": "Para Yahoo necesitas una contraseña de aplicación"
        }
    }
    return configs.get(provider)

def validate_email(email):
    """Valida formato de email"""
    parsed = parseaddr(email)
    return '@' in parsed[1] and '.' in parsed[1].split('@')[1]

def test_smtp_connection(config):
    """Prueba la conexión SMTP"""
    try:
        print("🔍 Probando conexión SMTP...")
        context = ssl.create_default_context()
        
        with smtplib.SMTP(config['smtp_server'], config['smtp_port']) as server:
            server.starttls(context=context)
            server.login(config['sender_email'], config['sender_password'])
            
        print("✅ Conexión SMTP exitosa!")
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión SMTP: {e}")
        return False

def setup_configuration():
    """Configuración interactiva inicial"""
    print_banner()
    
    print("📧 CONFIGURACIÓN DE CORREO ELECTRÓNICO")
    print("-" * 40)
    
    # Email del remitente
    while True:
        sender_email = input("Ingresa tu email de Tavolo Casa (ej: info@tavolocasa.com): ").strip()
        if validate_email(sender_email):
            break
        print("❌ Email inválido. Inténtalo de nuevo.")
    
    # Nombre del remitente
    sender_name = input("Nombre del remitente (por defecto: Tavolo Casa): ").strip()
    if not sender_name:
        sender_name = "Tavolo Casa"
    
    # Proveedor de email
    print("\n🌐 PROVEEDOR DE EMAIL")
    print("1. Gmail")
    print("2. Outlook/Hotmail") 
    print("3. Yahoo")
    print("4. Otro (configuración manual)")
    
    while True:
        choice = input("Selecciona tu proveedor (1-4): ").strip()
        if choice in ['1', '2', '3', '4']:
            break
        print("❌ Selección inválida. Elige 1, 2, 3 o 4.")
    
    providers = {'1': 'gmail', '2': 'outlook', '3': 'yahoo'}
    
    if choice in providers:
        provider = providers[choice]
        smtp_config = get_smtp_config(provider)
        print(f"\n💡 {smtp_config['instructions']}")
        smtp_server = smtp_config['smtp_server']
        smtp_port = smtp_config['smtp_port']
    else:
        print("\n⚙️ CONFIGURACIÓN MANUAL")
        smtp_server = input("Servidor SMTP: ").strip()
        while True:
            try:
                smtp_port = int(input("Puerto SMTP (por defecto 587): ") or "587")
                break
            except ValueError:
                print("❌ Puerto inválido. Debe ser un número.")
    
    # Contraseña
    print(f"\n🔐 Ingresa la contraseña para {sender_email}")
    if choice == '1':  # Gmail
        print("⚠️  Recuerda: Para Gmail usa la contraseña de aplicación, no tu contraseña normal")
    
    sender_password = getpass.getpass("Contraseña: ")
    
    # Crear configuración
    config = {
        "sender_email": sender_email,
        "sender_name": sender_name,
        "sender_password": sender_password,
        "smtp_server": smtp_server,
        "smtp_port": smtp_port,
        "company_info": {
            "name": "Tavolo Casa",
            "website": "https://tavolocasa.com",
            "phone": "655 586 462",
            "description": "La tienda del confort - Especialistas en artículos para el descanso",
            "products": [
                "Cojines",
                "Almohadas", 
                "Edredones",
                "Rellenos",
                "Artículos para mascotas"
            ]
        },
        "email_settings": {
            "delay_between_emails": 2,
            "max_retries": 3,
            "batch_size": 50
        }
    }
    
    # Probar conexión
    print("\n🔗 PRUEBA DE CONEXIÓN")
    if test_smtp_connection(config):
        # Guardar configuración
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        
        print("✅ Configuración guardada exitosamente!")
        return True
    else:
        print("❌ Error en la configuración. Verifica tus credenciales.")
        retry = input("¿Quieres intentar de nuevo? (s/n): ").lower().strip()
        if retry in ['s', 'si', 'sí']:
            return setup_configuration()
        return False

def verify_files():
    """Verifica que todos los archivos necesarios existen"""
    print("\n📁 VERIFICACIÓN DE ARCHIVOS")
    print("-" * 30)
    
    required_files = [
        'config.json',
        'plantilla_correo.html',
        'email_sender.py'
    ]
    
    all_good = True
    for file_name in required_files:
        if os.path.exists(file_name):
            print(f"✅ {file_name}")
        else:
            print(f"❌ {file_name} - FALTA")
            all_good = False
    
    # Verificar lista de correos
    if os.path.exists('lista_correos.csv'):
        print("✅ lista_correos.csv")
    else:
        print("⚠️  lista_correos.csv - No encontrado")
        print("   Puedes usar 'lista_correos_ejemplo.csv' como referencia")
    
    return all_good

def main():
    """Función principal del setup"""
    try:
        print_banner()
        
        # Verificar si ya existe configuración
        if os.path.exists('config.json'):
            print("⚠️  Ya existe un archivo config.json")
            recreate = input("¿Quieres recrear la configuración? (s/n): ").lower().strip()
            if recreate not in ['s', 'si', 'sí']:
                print("Manteniendo configuración existente...")
            else:
                os.remove('config.json')
                if not setup_configuration():
                    return
        else:
            if not setup_configuration():
                return
        
        # Verificar archivos
        if verify_files():
            print("\n🎉 ¡CONFIGURACIÓN COMPLETADA!")
            print("\nPasos siguientes:")
            print("1. Crea tu archivo 'lista_correos.csv' con los destinatarios")
            print("2. Personaliza 'plantilla_correo.html' si lo deseas")
            print("3. Ejecuta 'python email_sender.py' para enviar correos")
            print("\n📖 Lee el README.md para más información detallada")
        else:
            print("\n❌ Faltan archivos necesarios. Verifica la instalación.")
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Configuración cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante la configuración: {e}")

if __name__ == "__main__":
    main()
