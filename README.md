# 🐦 Vogel-Kamera-Linux

Ferngesteuerte Kameraüberwachung für Vogelhäuser mit ### Basis-Aufnahme
```bash
python python-skripte/ai-had-kamera-remote-param-vogel-libcamera-single-AI-Modul.py \
    --duration 5 \
    --width 1920 \
    --height 1080
```

> 📺 **Video-Tutorial verfügbar:** [Setup & Erste Aufnahme](https://www.youtube.com/@vogel-kamera-linux) auf unserem YouTube-Kanalützter Objekterkennung.

## 📖 Überblick

Dieses Projekt ermöglicht die Fernsteuerung von Raspberry Pi-Kameras zur Überwachung von Vogelhäusern. Es bietet hochauflösende Video- und Audioaufnahmen mit KI-basierter Objekterkennung (YOLOv8) und automatischer Dateiorganisation.

### 🎬 YouTube-Kanal & Video-Tutorials

[![YouTube Channel](https://img.shields.io/badge/📺_YouTube_Kanal-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@vogel-kamera-linux)

**📱 QR-Code für mobilen Zugriff:**

![YouTube QR Code](assets/qr-youtube-channel.png)

| Video-Tutorial | Beschreibung |
|----------------|--------------|
| 🔧 **Setup & Installation** | Komplette Einrichtung Schritt-für-Schritt |
| 🐦 **Live Vogelerkennung** | KI-Objekterkennung in Aktion |
| ⚡ **Zeitlupe-Aufnahmen** | 120fps Slow-Motion Beispiele |
| 🛠️ **Troubleshooting** | Häufige Probleme und Lösungen |

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

### Konfiguration laden
Die Skripte laden automatisch Konfigurationsdaten aus Umgebungsvariablen oder der `.env`-Datei. Stellen Sie sicher, dass Sie die `.env`-Datei entsprechend dem [Konfigurationsabschnitt](#%EF%B8%8F-ssh-konfiguration) eingerichtet haben.

## 📂 Projektstruktur

```
vogel-kamera-linux/
├── README.md
├── LICENSE
├── CHANGELOG.md                                                    # Versionshistorie
├── .gitignore
└── python-skripte/
    ├── config.py                                                      # Konfigurationssystem
    ├── __version__.py                                                  # Versionsverwaltung
    ├── .env.example                                                    # Konfigurationsvorlage
    ├── ai-had-kamera-remote-param-vogel-libcamera-single-AI-Modul.py  # Hauptskript mit KI
    ├── ai-had-audio-remote-param-vogel-libcamera-single.py            # Audio-Aufnahme
    └── ai-had-kamera-remote-param-vogel-libcamera-zeitlupe.py         # Zeitlupe-Aufnahmen
```

## 🚀 Verwendung

### Version anzeigen
```bash
python python-skripte/ai-had-kamera-remote-param-vogel-libcamera-single-AI-Modul.py --version
```

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

### 1. Umgebungsvariablen konfigurieren
```bash
# Kopieren Sie die Beispiel-Konfiguration
cp python-skripte/.env.example python-skripte/.env

# Bearbeiten Sie die .env-Datei mit Ihren Daten
nano python-skripte/.env
```

Beispiel `.env`-Datei:
```bash
RPI_HOSTNAME=raspberrypi-5-ai-had
RPI_USERNAME=pi
SSH_KEY_PATH=~/.ssh/id_rsa_rpi
BASE_VIDEO_PATH=~/Videos/Vogelhaus
REMOTE_VIDEO_PATH=/home/pi/Videos/Vogelhaus
REMOTE_AUDIO_PATH=/home/pi/Audio/Kamerawagen
```

> 📺 **Video-Tutorial:** [Konfiguration & SSH-Setup](https://www.youtube.com/@vogel-kamera-linux) - Komplette Einrichtungsanleitung

### 2. **SSH-Schlüssel generieren** (falls noch nicht vorhanden):
```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa_rpi
```

### 3. **Öffentlichen Schlüssel auf Raspberry Pi kopieren**:
```bash
ssh-copy-id -i ~/.ssh/id_rsa_rpi.pub pi@raspberrypi-5-ai-had
```

### 4. **Hostname in /etc/hosts eintragen** (optional):
```bash
echo "192.168.1.XXX raspberrypi-5-ai-had" | sudo tee -a /etc/hosts
```

## 📁 Dateiorganisation

Die aufgenommenen Videos werden automatisch organisiert:
```
~/Videos/Vogelhaus/
├── AI-HAD/        # Hauptskript mit KI-Erkennung
├── Audio/         # Reine Audio-Aufnahmen  
└── Zeitlupe/      # Slow-Motion Videos
    └── 2025/
        └── 38/  # Kalenderwoche
            └── Montag__2025-09-23__14-30-15/
                └── Montag__2025-09-23__14-30-15__4096x2160.mp4
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
ssh -i ~/.ssh/id_rsa_rpi pi@raspberrypi-5-ai-had

# Konfiguration validieren:
python python-skripte/config.py
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

## 📋 Changelog

Alle Änderungen werden in [CHANGELOG.md](CHANGELOG.md) dokumentiert.

## 🔖 Versionen

- **Aktuelle Version:** v1.1.0
- **Entwicklungszweig:** `devel`
- **Stabile Releases:** [GitHub Releases](../../releases)
