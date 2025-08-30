#!/usr/bin/env python3
"""
Script de automatización de correos para Tavolo Casa
Automatiza el envío de correos masivos a listas de destinatarios
"""

import smtplib
import ssl
import csv
import json
import logging
import time
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import List, Dict, Optional
import os

class TavoloCasaEmailSender:
    def __init__(self, config_file: str = "config.json"):
        """
        Inicializa el enviador de correos de Tavolo Casa
        
        Args:
            config_file: Ruta al archivo de configuración
        """
        self.config = self.load_config(config_file)
        self.setup_logging()
        
    def load_config(self, config_file: str) -> Dict:
        """Carga la configuración desde archivo JSON"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.error(f"Archivo de configuración {config_file} no encontrado")
            raise
        except json.JSONDecodeError:
            logging.error(f"Error al parsear archivo de configuración {config_file}")
            raise
    
    def setup_logging(self):
        """Configura el sistema de logging"""
        log_file = f"email_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        logging.info("Sistema de correos Tavolo Casa iniciado")
    
    def load_email_list(self, file_path: str) -> List[Dict[str, str]]:
        """
        Carga la lista de correos desde un archivo CSV
        
        Args:
            file_path: Ruta al archivo CSV con los correos
            
        Returns:
            Lista de diccionarios con información de contactos
            
        Formato esperado del CSV:
        email,nombre,apellido,empresa
        """
        contacts = []
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('email') and '@' in row['email']:
                        contacts.append({
                            'email': row['email'].strip(),
                            'nombre': row.get('nombre', '').strip(),
                            'apellido': row.get('apellido', '').strip(),
                            'empresa': row.get('empresa', '').strip()
                        })
            logging.info(f"Cargados {len(contacts)} contactos desde {file_path}")
            return contacts
        except FileNotFoundError:
            logging.error(f"Archivo {file_path} no encontrado")
            raise
        except Exception as e:
            logging.error(f"Error al cargar lista de correos: {e}")
            raise
    
    def load_template(self, template_file: str) -> str:
        """Carga la plantilla HTML del correo"""
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            logging.error(f"Plantilla {template_file} no encontrada")
            raise
    
    def personalize_email(self, template: str, contact: Dict[str, str]) -> str:
        """
        Personaliza el correo con los datos del contacto
        
        Args:
            template: Plantilla HTML del correo
            contact: Datos del contacto
            
        Returns:
            HTML personalizado
        """
        # Variables disponibles para personalización
        variables = {
            '{{NOMBRE}}': contact.get('nombre', 'Estimado/a cliente'),
            '{{APELLIDO}}': contact.get('apellido', ''),
            '{{EMPRESA}}': contact.get('empresa', ''),
            '{{NOMBRE_COMPLETO}}': f"{contact.get('nombre', '')} {contact.get('apellido', '')}".strip(),
            '{{FECHA}}': datetime.now().strftime('%d de %B de %Y'),
            '{{AÑO}}': str(datetime.now().year)
        }
        
        personalized = template
        for placeholder, value in variables.items():
            personalized = personalized.replace(placeholder, value)
            
        return personalized
    
    def create_message(self, to_email: str, subject: str, html_content: str, 
                      attachments: Optional[List[str]] = None) -> MIMEMultipart:
        """
        Crea el mensaje de correo
        
        Args:
            to_email: Dirección de destino
            subject: Asunto del correo
            html_content: Contenido HTML del correo
            attachments: Lista de rutas de archivos adjuntos
            
        Returns:
            Mensaje MIME configurado
        """
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f"{self.config['sender_name']} <{self.config['sender_email']}>"
        message["To"] = to_email
        
        # Agregar contenido HTML
        html_part = MIMEText(html_content, "html", "utf-8")
        message.attach(html_part)
        
        # Agregar archivos adjuntos si existen
        if attachments:
            for file_path in attachments:
                if os.path.isfile(file_path):
                    with open(file_path, "rb") as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                    
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {os.path.basename(file_path)}'
                    )
                    message.attach(part)
                    
        return message
    
    def send_email(self, message: MIMEMultipart, to_email: str) -> bool:
        """
        Envía un correo individual
        
        Args:
            message: Mensaje MIME configurado
            to_email: Dirección de destino
            
        Returns:
            True si el envío fue exitoso, False en caso contrario
        """
        try:
            context = ssl.create_default_context()
            
            with smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port']) as server:
                server.starttls(context=context)
                server.login(self.config['sender_email'], self.config['sender_password'])
                
                # Enviar mensaje como string
                text = message.as_string()
                server.sendmail(self.config['sender_email'], to_email, text)
                
            logging.info(f"Correo enviado exitosamente a {to_email}")
            return True
            
        except Exception as e:
            logging.error(f"Error al enviar correo a {to_email}: {e}")
            return False
    
    def send_bulk_emails(self, email_list_file: str, template_file: str, 
                        subject: str, attachments: Optional[List[str]] = None,
                        delay_seconds: int = 2):
        """
        Envía correos masivos a toda la lista
        
        Args:
            email_list_file: Archivo CSV con la lista de correos
            template_file: Archivo HTML con la plantilla del correo
            subject: Asunto del correo
            attachments: Lista de archivos adjuntos
            delay_seconds: Segundos de espera entre envíos
        """
        # Cargar datos
        contacts = self.load_email_list(email_list_file)
        template = self.load_template(template_file)
        
        # Estadísticas
        total_contacts = len(contacts)
        sent_count = 0
        failed_count = 0
        
        logging.info(f"Iniciando envío masivo a {total_contacts} contactos")
        
        for i, contact in enumerate(contacts, 1):
            try:
                # Personalizar correo
                personalized_html = self.personalize_email(template, contact)
                
                # Crear mensaje
                message = self.create_message(
                    contact['email'], 
                    subject, 
                    personalized_html, 
                    attachments
                )
                
                # Enviar correo
                if self.send_email(message, contact['email']):
                    sent_count += 1
                    print(f"✅ [{i}/{total_contacts}] Enviado a {contact['email']}")
                else:
                    failed_count += 1
                    print(f"❌ [{i}/{total_contacts}] Falló envío a {contact['email']}")
                
                # Pausa entre envíos para evitar ser marcado como spam
                if i < total_contacts:
                    time.sleep(delay_seconds)
                    
            except Exception as e:
                failed_count += 1
                logging.error(f"Error procesando contacto {contact.get('email', 'unknown')}: {e}")
                print(f"❌ [{i}/{total_contacts}] Error con {contact.get('email', 'unknown')}")
        
        # Resumen final
        print(f"\n📊 RESUMEN DEL ENVÍO:")
        print(f"Total contactos: {total_contacts}")
        print(f"Enviados exitosamente: {sent_count}")
        print(f"Fallos: {failed_count}")
        print(f"Tasa de éxito: {(sent_count/total_contacts)*100:.1f}%")
        
        logging.info(f"Envío masivo completado. Éxito: {sent_count}/{total_contacts}")

def main():
    """Función principal para ejecutar el script"""
    try:
        # Inicializar el enviador
        sender = TavoloCasaEmailSender()
        
        # Configurar parámetros del envío
        email_list_file = "lista_correos.csv"
        template_file = "plantilla_correo.html"
        subject = "🛏️ Descubre el mejor descanso con Tavolo Casa - Ofertas especiales"
        attachments = []  # Agregar rutas de archivos si es necesario
        
        # Verificar que los archivos existen
        if not os.path.exists(email_list_file):
            print(f"❌ Error: No se encuentra el archivo {email_list_file}")
            print("Por favor, crea este archivo con las direcciones de correo")
            return
            
        if not os.path.exists(template_file):
            print(f"❌ Error: No se encuentra el archivo {template_file}")
            print("Por favor, crea este archivo con la plantilla HTML")
            return
        
        # Confirmar envío
        print("🚀 SISTEMA DE CORREOS TAVOLO CASA")
        print("="*50)
        print(f"📧 Archivo de correos: {email_list_file}")
        print(f"📝 Plantilla: {template_file}")
        print(f"📋 Asunto: {subject}")
        
        confirm = input("\n¿Deseas proceder con el envío? (s/n): ").lower().strip()
        
        if confirm in ['s', 'si', 'sí', 'y', 'yes']:
            sender.send_bulk_emails(
                email_list_file=email_list_file,
                template_file=template_file,
                subject=subject,
                attachments=attachments,
                delay_seconds=2
            )
        else:
            print("Envío cancelado por el usuario")
            
    except Exception as e:
        logging.error(f"Error en función principal: {e}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
