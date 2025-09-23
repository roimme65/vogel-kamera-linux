# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
und dieses Projekt befolgt [Semantic Versioning](https://semver.org/lang/de/).

## [Unreleased]
### Geplant
- GUI-Interface für einfachere Bedienung
- Automatische Backup-Funktionalität
- Erweiterte KI-Modelle (YOLOv9/v10)
- Web-Dashboard für Remote-Monitoring

## [1.1.2] - 2025-09-23
### Hinzugefügt
- **🔧 GitHub Issue Templates:** Deutsche Bug Report und Feature Request Templates
- **📋 Repository-spezifische Anpassungen:** Hardware-spezifische Abschnitte für Pi/Kamera
- **🤝 Community-Engagement:** Strukturierte Nutzen-Bewertung und Akzeptanzkriterien
- **📁 .gitignore Update:** Wiki-Content Verzeichnis ausgeschlossen für besseres Repository-Management

### Verbessert
- **📝 Issue Template Struktur:** Emoji-Icons und bessere Kategorisierung
- **🎯 Feature Request Process:** Priorisierung und Implementierungs-Bereitschaft
- **🐛 Bug Report Qualität:** Detaillierte System-Informationen und Reproduktionsschritte
- **🌍 Lokalisierung:** Vollständige deutsche Übersetzung aller Templates

### Technisch
- Neue .github/ISSUE_TEMPLATE/ Struktur implementiert
- Repository-spezifische Anpassungen für Vogel-Kamera-Linux
- Automatische Label-Zuweisung für Issues
- Verbesserte Community-Beitrag-Workflows

## [1.1.1] - 2025-09-23
### Behoben
- **🔧 Kritischer Bugfix:** .env-Datei wird jetzt korrekt geladen
- **📦 Dependencies:** Fehlende python-dotenv Abhängigkeit hinzugefügt
- **🛠️ Konfigurationssystem:** Vollständig funktionsfähig gemacht
- **✅ Skript-Funktionalität:** Alle Skripte getestet und lauffähig

### Hinzugefügt
- **📦 requirements.txt** für einfache Dependency-Installation
- **🔧 Verbesserte Installationsanweisungen** in README.md
- **✅ Konfigurationsvalidierung** funktioniert korrekt

### Technisch
- python-dotenv>=1.0.0 als neue Abhängigkeit
- Automatisches Laden der .env-Datei beim Import
- Verbesserte Fehlerbehandlung im Konfigurationssystem

## [1.1.0] - 2025-09-23
### Hinzugefügt
- **🎬 YouTube-Integration:**
  - YouTube-Kanal Sektion in README.md
  - QR-Code für mobilen Zugriff auf Videos
  - Video-Tutorial Verweise in der Dokumentation
  - Automatischer QR-Code Generator (`generate_qr_codes.py`)

- **📱 QR-Code System:**
  - Hauptkanal QR-Code (`qr-youtube-channel.png`)
  - Playlists QR-Code (`qr-playlists.png`) 
  - Abonnieren QR-Code (`qr-subscribe.png`)
  - QR-Code Anleitung (`QR-CODE-ANLEITUNG.md`)

- **🔧 Konfigurationsverbesserungen:**
  - Zentrales Konfigurationssystem implementiert
  - Sichere `.env`-basierte Konfiguration
  - Automatische Konfigurationsvalidierung
  - Entfernung aller hardcodierten persönlichen Daten

- **📚 Dokumentation:**
  - Erweiterte README.md mit YouTube-Integration
  - Vollständige Projektstruktur dokumentiert
  - Video-Tutorial Verweise hinzugefügt
  - Konfigurationsanleitung verbessert

### Geändert
- Alle Python-Skripte verwenden jetzt das zentrale Konfigurationssystem
- SSH-Verbindungsdetails über Umgebungsvariablen konfigurierbar
- Pfade für Video/Audio-Speicherung konfigurierbar
- .gitignore erweitert um `.venv/` und weitere Python-Dateien

### Sicherheit
- **🔒 Sichere Veröffentlichung:** Alle persönlichen Daten entfernt
- Konfiguration über `.env`-Dateien (nicht im Repository)
- SSH-Schlüssel-Pfade konfigurierbar
- Validierung warnt vor fehlender Konfiguration

## [1.0.0] - 2025-09-23
### Hinzugefügt
- **Hauptfunktionalitäten:**
  - 🎥 Hochauflösende Videoaufnahme (bis 4K) mit Raspberry Pi 5
  - 🎵 Synchrone Audioaufnahme über USB-Mikrofon
  - 🤖 KI-Objekterkennung mit YOLOv8 für Vogelerkennung
  - 🌐 SSH-basierte Remote-Steuerung
  - 📁 Automatische Dateiorganisation nach Jahr/Kalenderwoche

- **Drei spezialisierte Skripte:**
  - `ai-had-kamera-remote-param-vogel-libcamera-single-AI-Modul.py` - Haupt-Aufnahmeskript mit KI
  - `ai-had-audio-remote-param-vogel-libcamera-single.py` - Spezialisierte Audio-Aufnahme
  - `ai-had-kamera-remote-param-vogel-libcamera-zeitlupe.py` - Zeitlupe-Aufnahmen (120fps+)

- **Konfigurationssystem:**
  - Zentrales `config.py` für alle Einstellungen
  - `.env.example` Vorlage für sichere Konfiguration
  - Automatische Konfigurationsvalidierung
  - Umgebungsvariablen-Support

- **Sicherheit & Best Practices:**
  - Keine hardcodierten persönlichen Daten
  - MIT-Lizenz mit Haftungsausschluss
  - Vollständige `.gitignore` für sensible Dateien
  - SSH-Schlüssel-Authentifizierung

- **Benutzerfreundlichkeit:**
  - Kommandozeilen-Interface mit umfassenden Parametern
  - Fortschrittsanzeige während Aufnahme (tqdm)
  - Versionsinformationen (`--version`)
  - Umfassende Fehlerbehandlung
  - Signal-Handler für sauberes Beenden (Ctrl+C)

- **Technische Features:**
  - Multi-Threading für parallele Video/Audio-Verarbeitung
  - Automatische FFmpeg-Konvertierung zu MP4
  - USB-Audio-Gerät Auto-Erkennung
  - Flexible Auflösungs- und Codec-Unterstützung
  - ROI (Region of Interest) Support
  - HDR-Modi und erweiterte Kamera-Einstellungen

### Dokumentation
- Vollständige README.md mit Setup-Anweisungen
- Parameter-Übersichtstabelle
- Troubleshooting-Sektion
- SSH-Konfigurationsanleitung
- Projektstruktur-Dokumentation

### Technische Spezifikationen
- **Python:** >= 3.8
- **Betriebssystem:** Linux, Raspberry Pi OS
- **Hardware:** Raspberry Pi 5 + Kamera-Modul + USB-Mikrofon
- **Abhängigkeiten:** paramiko, scp, tqdm, ffmpeg
- **Kamera-Software:** libcamera/rpicam-vid

### Dateiorganisation
```
~/Videos/Vogelhaus/
├── AI-HAD/        # KI-gestützte Aufnahmen
├── Audio/         # Reine Audio-Aufnahmen  
└── Zeitlupe/      # Slow-Motion Videos
    └── YYYY/MM/Wochentag__YYYY-MM-DD__HH-MM-SS/
```

---

## Versionierungsschema

- **Major Version (X.0.0):** Breaking Changes, API-Änderungen
- **Minor Version (0.X.0):** Neue Features, rückwärtskompatibel  
- **Patch Version (0.0.X):** Bugfixes, kleine Verbesserungen

## Entwicklungsrichtlinien

### Für Mitwirkende
1. Fork des Repositories erstellen
2. Feature-Branch von `devel` erstellen
3. Änderungen implementieren und testen
4. CHANGELOG.md entsprechend aktualisieren
5. Pull Request gegen `devel` erstellen

### Release-Prozess
1. Version in `__version__.py` aktualisieren
2. CHANGELOG.md mit finalen Änderungen aktualisieren
3. Git-Tag erstellen: `git tag -a v1.0.0 -m "Release v1.0.0"`
4. Tag pushen: `git push origin v1.0.0`
5. Release auf GitHub erstellen

---

**Hinweis:** Vor Version 1.0.0 können breaking changes in Minor-Versionen auftreten.