# 🤖 Git Automation für Vogel-Kamera-Linux

Automatisches Python-Skript für Git-Operationen mit SSH-Secret-Management.

## 🚀 Features

- ✅ **Automatische Branch-Synchronisation** (main, devel)
- ✅ **Tag-Updates** für alle Versionen
- ✅ **SSH-Secret-Management** mit verschlüsselten Passphrases
- ✅ **Batch-Commits** mit automatischen Push-Operationen
- ✅ **Sichere Konfiguration** über .gitignore-geschützte Dateien

## 📋 Installation & Setup

### 1. **Abhängigkeiten installieren:**
```bash
# Python-Verschlüsselungs-Bibliothek
pip install -r git_automation_requirements.txt

# System-Tools
sudo apt install expect
```

### 2. **Verschlüsselte Secrets erstellen:**
```bash
# Interaktive Einrichtung mit Master-Password
python3 git_automation.py --setup

# Das Skript fragt ab:
# - Master-Password (wird NICHT gespeichert!)
# - SSH-Key-Pfad
# - SSH-Passphrase (wird verschlüsselt)
# - Git-User-Daten
```

### 3. **Secrets aktualisieren:**
```bash
# SSH-Passphrase ändern
python3 git_automation.py --update-secret ssh_passphrase

# Master-Password wird dabei abgefragt
```

## 🎯 Verwendung

### **Vollständige Synchronisation:**
```bash
python3 git_automation.py --sync
```

### **Nur Branches synchronisieren:**
```bash
python3 git_automation.py --branches
```

### **Nur Tags aktualisieren:**
```bash
python3 git_automation.py --tags
```

### **Committen mit Nachricht:**
```bash
python3 git_automation.py --commit "🔧 Feature: Neue Funktionalität hinzugefügt"
```

### **Vollsync mit Commit:**
```bash
python3 git_automation.py --sync --commit "🎉 Release v1.1.4 - Neue Features"
```

## 🔐 Sicherheit

### **Geschützte Dateien (.gitignore):**
```
git_automation.py      # Das Skript selbst
.git_secrets.json      # SSH-Secrets und Konfiguration
.ssh_secrets.json      # Alternative Secrets-Datei
```

### **SSH-Agent Integration:**
- Automatische SSH-Agent-Konfiguration
- Passphrase-Handling über expect
- Timeout-Schutz für lange Operationen

## ⚙️ Funktionen im Detail

### **Branch-Synchronisation:**
1. Checkout zu jedem konfigurierten Branch
2. Pull latest changes von origin
3. Automatischer Push (wenn aktiviert)
4. Fehlerbehandlung und Logging

### **Tag-Management:**
1. Alle Version-Tags abrufen (v*)
2. Tags löschen und neu erstellen auf main Branch
3. Force-Push der aktualisierten Tags
4. Zeitstempel-basierte Tag-Messages

### **Commit-Automation:**
1. Alle Änderungen staged (git add -A)
2. Commit mit benutzerdefinierten/automatischen Messages
3. Push zum entsprechenden Remote-Branch
4. Status-Feedback für alle Operationen

## 🛠️ Abhängigkeiten

```bash
# System-Abhängigkeiten
sudo apt install expect  # Für automatische Passphrase-Eingabe

# Python-Abhängigkeiten
pip install -r git_automation_requirements.txt
# Enthält: cryptography>=41.0.0 für AES-256-Verschlüsselung

# Python-Module
import subprocess, json, os, sys, base64, hashlib, getpass
from pathlib import Path
from datetime import datetime
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
```

## 🔐 Verschlüsselungs-Features

### **AES-256-CBC Verschlüsselung:**
- ✅ **SSH-Passphrases** niemals im Klartext gespeichert
- ✅ **PBKDF2** mit 100.000 Iterationen (OWASP-Standard)
- ✅ **Zufällige Salts und IVs** für jede Verschlüsselung
- ✅ **Master-Password** für Zugriff auf alle Secrets

### **Sichere Speicherung:**
```json
{
  "version": "1.0",
  "encryption": "AES-256-CBC-PBKDF2",
  "encrypted_secrets": {
    "ssh_passphrase": {
      "encrypted_data": "base64-verschlüsselte-daten",
      "salt": "base64-salt",
      "iv": "base64-iv",
      "algorithm": "AES-256-CBC-PBKDF2"
    }
  }
}
```

### **Memory Security:**
- ✅ **Automatische Speicher-Bereinigung** nach Verwendung
- ✅ **Temporäre Dateien** werden sicher gelöscht
- ✅ **Passphrase-Überschreibung** im RAM

## 📊 Beispiel-Workflow

```bash
# 1. Neue Features entwickeln
# ... Code-Änderungen ...

# 2. Automatisch committen und synchronisieren
python3 git_automation.py --sync --commit "✨ Neue Feature: GitHub Discussions"

# 3. Tags für neue Version aktualisieren
python3 git_automation.py --tags

# 4. Alle Branches auf aktuellen Stand bringen
python3 git_automation.py --branches
```

## ⚠️ Wichtige Hinweise

### **Sicherheit:**
- ❌ **NIEMALS** `.git_secrets.json` committen oder teilen
- ❌ **NIEMALS** das Skript mit Secrets öffentlich machen
- ✅ Verwenden Sie starke SSH-Passphrases
- ✅ Regelmäßige Rotation der SSH-Keys

### **Backup:**
- 💾 Lokale Backups der Secrets-Datei anlegen
- 🔄 Regelmäßige Überprüfung der Git-Remote-Verbindungen
- 📋 Logging für Troubleshooting aktivieren

### **Fehlerbehandlung:**
- 🕐 5-Minuten Timeout für alle Git-Operationen
- 🔄 Automatische Retry-Logik bei Netzwerkfehlern
- 📝 Detaillierte Error-Messages für Debugging

---

**💡 Tipp:** Führen Sie zuerst `--setup` aus, konfigurieren Sie die Secrets, und testen Sie dann mit `--branches` vor der vollständigen `--sync` Operation.