# 🐦 Vogel-Kamera-Linux

Ferngesteuerte Kameraüberwachung für Vogelhäuser mit KI-gestützter Objekterkennung.

## 📖 Überblick

Dieses Projekt ermöglicht die Fernsteuerung von Raspberry Pi-Kameras zur Überwachung von Vogelhäusern. Es bietet hochauflösende Video- und Audioaufnahmen mit KI-basierter Objekterkennung (YOLOv8) und automatischer Dateiorganisation.

## ✨ Features

- 🎥 **Hochauflösende Videoaufnahme** (bis zu 4K)
- 🎵 **Synchrone Audioaufnahme** über USB-Mikrofon
- 🤖 **KI-Objekterkennung** mit YOLOv8 für Vogelerkennung
- 🌐 **Remote-Steuerung** über SSH
- 📁 **Automatische Dateiorganisation** nach Jahr/Woche
- ⚙️ **Flexible Konfiguration** über Kommandozeilenparameter
- 📊 **Fortschrittsanzeige** während der Aufnahme
- 🔄 **Automatische Video-/Audio-Synchronisation**

## 🛠️ Voraussetzungen

### Hardware
- Raspberry Pi 5 mit Kamera-Modul
- USB-Mikrofon für Audioaufnahme
- Stabile Netzwerkverbindung

### Software
- Python 3.8+
- SSH-Zugang zum Raspberry Pi
- libcamera/rpicam-vid auf dem Raspberry Pi

### Python-Abhängigkeiten
```bash
pip install paramiko scp tqdm
```

## 📂 Projektstruktur

```
vogel-kamera-linux/
├── README.md
├── LICENSE
└── python-skripte/
    ├── ai-had-kamera-remote-param-vogel-libcamera-single-AI-Modul.py  # Hauptskript mit KI
    ├── ai-had-audio-remote-param-vogel-libcamera-single.py            # Audio-Aufnahme
    └── ai-had-kamera-remote-param-vogel-libcamera-zeitlupe.py         # Zeitlupe-Aufnahmen
```

## 🚀 Verwendung

### Basis-Aufnahme
```bash
python ai-had-kamera-remote-param-vogel-libcamera-single-AI-Modul.py \
    --duration 5 \
    --width 1920 \
    --height 1080
```

### Erweiterte Konfiguration
```bash
python ai-had-kamera-remote-param-vogel-libcamera-single-AI-Modul.py \
    --duration 10 \
    --width 4096 \
    --height 2160 \
    --codec h264 \
    --autofocus_mode continuous \
    --rotation 180 \
    --fps 30 \
    --cam 0
```

### Parameter-Übersicht

| Parameter | Beschreibung | Standard | Optionen |
|-----------|--------------|----------|----------|
| `--duration` | Aufnahmedauer in Minuten | **erforderlich** | 1-∞ |
| `--width` | Video-Breite | 4096 | 640-4096 |
| `--height` | Video-Höhe | 2160 | 480-2160 |
| `--codec` | Video-Codec | h264 | h264, h265 |
| `--autofocus_mode` | Autofokus-Modus | continuous | continuous, manual |
| `--autofocus_range` | Autofokus-Bereich | macro | macro, full |
| `--hdr` | HDR-Modus | off | auto, off |
| `--rotation` | Bildrotation | 180 | 0, 90, 180, 270 |
| `--fps` | Bildrate | 15 | 1-60 |
| `--cam` | Kamera-ID | 1 | 0, 1 |
| `--roi` | Region of Interest | - | x,y,w,h |

## ⚙️ SSH-Konfiguration

1. **SSH-Schlüssel generieren** (falls noch nicht vorhanden):
```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa_ai-had
```

2. **Öffentlichen Schlüssel auf Raspberry Pi kopieren**:
```bash
ssh-copy-id -i ~/.ssh/id_rsa_ai-had.pub roimme@raspberrypi-5-ai-had
```

3. **Hostname in /etc/hosts eintragen**:
```bash
echo "192.168.1.XXX raspberrypi-5-ai-had" | sudo tee -a /etc/hosts
```

## 📁 Dateiorganisation

Die aufgenommenen Videos werden automatisch organisiert:
```
~/Videos/Vogelhaus/AI-HAD/
└── 2025/
    └── 38/  # Kalenderwoche
        └── Montag__2025-09-23__14-30-15/
            ├── Montag__2025-09-23__14-30-15__4096x2160.mp4
            └── (temporäre Zwischendateien werden automatisch gelöscht)
```

## 🤖 KI-Objekterkennung

Das Hauptskript nutzt YOLOv8 für die Echtzeit-Objekterkennung:
- **Automatische Vogelerkennung** während der Aufnahme
- **Optimierte Inferenz** auf Raspberry Pi 5
- **Konfigurierbare Erkennungsparameter**

## 🔧 Problembehandlung

### Audio-Gerät nicht gefunden
```bash
# Auf dem Raspberry Pi prüfen:
arecord -l
```

### SSH-Verbindungsprobleme
```bash
# Verbindung testen:
ssh -i ~/.ssh/id_rsa_ai-had roimme@raspberrypi-5-ai-had
```

### Kamera-Probleme
```bash
# Kamera-Status prüfen:
rpicam-hello --list-cameras
```

## 📄 Lizenz

Siehe [LICENSE](LICENSE) Datei für Details.

## 🤝 Beitragen

1. Fork des Repositories
2. Feature-Branch erstellen
3. Änderungen commiten
4. Pull Request erstellen

## 📞 Support

Bei Fragen oder Problemen bitte ein Issue erstellen.
