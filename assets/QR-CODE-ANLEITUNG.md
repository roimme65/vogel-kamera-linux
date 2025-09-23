# QR-Code Generierung für YouTube-Kanal

## 🎯 QR-Code für Ihren YouTube-Kanal erstellen

### Option 1: Online QR-Code Generator (Empfohlen)

1. **Besuchen Sie:** https://www.qr-code-generator.com/
2. **URL eingeben:** `https://www.youtube.com/@vogel-kamera-linux`
3. **Einstellungen:**
   - Format: PNG
   - Größe: 200x200 Pixel
   - Fehlerkorrektur: Medium (15%)
   - Farbe: Schwarz auf Weiß
4. **Speichern als:** `qr-youtube-channel.png`

### Option 2: Python-Script für QR-Code-Generierung

```python
import qrcode
from PIL import Image

# QR-Code für YouTube-Kanal erstellen
def create_youtube_qr():
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    
    # YouTube-Kanal URL
    qr.add_data('https://www.youtube.com/@vogel-kamera-linux')
    qr.make(fit=True)
    
    # QR-Code als Bild erstellen
    img = qr.make_image(fill_color="black", back_color="white")
    img.save('assets/qr-youtube-channel.png')
    print("QR-Code wurde erstellt: assets/qr-youtube-channel.png")

if __name__ == "__main__":
    create_youtube_qr()
```

### Option 3: Kommandozeile mit qrencode

```bash
# QR-Code installieren (Ubuntu/Debian)
sudo apt install qrencode

# QR-Code generieren
qrencode -o assets/qr-youtube-channel.png -s 8 "https://www.youtube.com/@vogel-kamera-linux"
```

## 📂 Datei-Platzierung

Speichern Sie den QR-Code als:
```
assets/qr-youtube-channel.png
```

## 🎨 Design-Empfehlungen

- **Größe:** 200x200 Pixel (für GitHub README)
- **Format:** PNG mit transparentem Hintergrund
- **Kontrast:** Schwarz auf Weiß für beste Lesbarkeit
- **Test:** QR-Code mit verschiedenen Apps testen

## 📱 Verwendung in README.md

Der QR-Code wird automatisch in der README.md angezeigt:
```markdown
![YouTube QR Code](assets/qr-youtube-channel.png)
```

## 🔗 Zusätzliche QR-Codes

Sie können auch spezifische Video-QR-Codes erstellen:
- Setup-Tutorial: `assets/qr-setup-video.png`
- Demo-Video: `assets/qr-demo-video.png`
- Troubleshooting: `assets/qr-troubleshooting-video.png`