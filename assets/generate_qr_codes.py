#!/usr/bin/env python3
"""
QR-Code Generator für Vogel-Kamera-Linux YouTube-Videos
Automatische Erstellung von QR-Codes für verschiedene Video-Tutorials
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
    
    # In assets Ordner speichern
    filepath = f'assets/{filename}'
    img.save(filepath)
    
    print(f'✅ {description}')
    print(f'   📄 Datei: {filepath}')
    print(f'   🔗 URL: {url}')
    print()

def main():
    """Hauptfunktion - Erstelle alle QR-Codes"""
    print("🎬 Vogel-Kamera-Linux QR-Code Generator")
    print("=" * 50)
    
    # Stelle sicher, dass assets Ordner existiert
    os.makedirs('assets', exist_ok=True)
    
    # Base YouTube Channel URL
    base_url = "https://www.youtube.com/@vogel-kamera-linux"
    
    # QR-Codes für verschiedene Zwecke erstellen
    qr_codes = [
        {
            'url': base_url,
            'filename': 'qr-youtube-channel.png',
            'description': 'YouTube-Kanal QR-Code erstellt'
        },
        {
            'url': f"{base_url}/playlists",
            'filename': 'qr-playlists.png', 
            'description': 'Playlists QR-Code erstellt'
        },
        {
            'url': f"{base_url}?sub_confirmation=1",
            'filename': 'qr-subscribe.png',
            'description': 'Abonnieren QR-Code erstellt'
        }
    ]
    
    # Erstelle alle QR-Codes
    for qr_data in qr_codes:
        create_qr_code(**qr_data)
    
    print("🎯 Alle QR-Codes erfolgreich erstellt!")
    print("📁 Speicherort: assets/")
    print()
    print("💡 Nächste Schritte:")
    print("1. Erstellen Sie Videos und notieren Sie die YouTube-Video-IDs")
    print("2. Erstellen Sie spezifische QR-Codes für einzelne Videos")
    print("3. Aktualisieren Sie die README.md mit den Video-Links")

if __name__ == "__main__":
    main()