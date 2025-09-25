#!/usr/bin/env python3
"""
QR-Code Generator für LinuxDay.at 2025 Veranstaltung
Automatische Erstellung von QR-Codes für Veranstaltung und Vortrag
"""

import qrcode
import os

def create_qr_code(url, filename, description):
    """Erstelle einen QR-Code für eine gegebene URL"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    
    qr.add_data(url)
    qr.make(fit=True)
    
    # QR-Code als Bild erstellen
    img = qr.make_image(fill_color='black', back_color='white')
    
    # Speichern
    img.save(filename)
    
    print(f'✅ {description}')
    print(f'   📄 Datei: {filename}')
    print(f'   🔗 URL: {url}')
    print()

def main():
    """Hauptfunktion - Erstelle LinuxDay.at QR-Codes"""
    print("🐧 LinuxDay.at 2025 QR-Code Generator")
    print("=" * 50)
    
    # QR-Codes für LinuxDay.at erstellen
    qr_codes = [
        {
            'url': 'https://www.linuxday.at/',
            'filename': 'qr-linuxday-website.png',
            'description': 'LinuxDay.at Website QR-Code erstellt'
        },
        {
            'url': 'https://www.linuxday.at/automatisierte-vogelbeobachtung-mit-raspberry-pi-python-und-ki',
            'filename': 'qr-vortrag-vogelbeobachtung.png', 
            'description': 'Vortrag "Automatisierte Vogelbeobachtung" QR-Code erstellt'
        }
    ]
    
    # Erstelle alle QR-Codes
    for qr_data in qr_codes:
        create_qr_code(**qr_data)
    
    print("🎯 Alle LinuxDay.at QR-Codes erfolgreich erstellt!")
    print("📅 Veranstaltung: 27. September 2025")
    print("🎤 Vortrag: Automatisierte Vogelbeobachtung mit Raspberry Pi, Python und KI")

if __name__ == "__main__":
    main()