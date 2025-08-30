#!/usr/bin/env python3
"""
Script de prueba para el sistema de correos Tavolo Casa
Permite enviar un correo de prueba a una dirección específica
"""

import sys
import os
from email_sender import TavoloCasaEmailSender

def send_test_email():
    """Envía un correo de prueba"""
    print("🧪 ENVÍO DE CORREO DE PRUEBA - TAVOLO CASA")
    print("="*50)
    
    try:
        # Pedir email de destino
        test_email = input("Ingresa el email para la prueba: ").strip()
        
        if '@' not in test_email:
            print("❌ Email inválido")
            return
        
        # Verificar archivos necesarios
        if not os.path.exists('config.json'):
            print("❌ No se encuentra config.json. Ejecuta 'python setup.py' primero.")
            return
            
        if not os.path.exists('plantilla_correo.html'):
            print("❌ No se encuentra plantilla_correo.html")
            return
        
        # Inicializar el enviador
        sender = TavoloCasaEmailSender()
        
        # Crear contacto de prueba
        test_contact = {
            'email': test_email,
            'nombre': 'Cliente',
            'apellido': 'de Prueba',
            'empresa': 'Empresa Test'
        }
        
        # Cargar plantilla
        template = sender.load_template('plantilla_correo.html')
        
        # Personalizar correo
        personalized_html = sender.personalize_email(template, test_contact)
        
        # Crear mensaje
        subject = "🧪 Correo de Prueba - Tavolo Casa"
        message = sender.create_message(test_email, subject, personalized_html)
        
        # Enviar
        print(f"📤 Enviando correo de prueba a {test_email}...")
        
        if sender.send_email(message, test_email):
            print("✅ ¡Correo de prueba enviado exitosamente!")
            print(f"📧 Revisa la bandeja de entrada de {test_email}")
        else:
            print("❌ Error al enviar el correo de prueba")
            print("💡 Revisa el archivo de log para más detalles")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    send_test_email()
