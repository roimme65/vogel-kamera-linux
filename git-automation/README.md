# 🔐 Git-Automatisierung

Automatisierte Git-Operationen mit verschlüsselten SSH-Credentials für das Vogel-Kamera-Linux Projekt.

## 📁 Ordnerstruktur

```
git-automation/
├── git_automation.py           # Haupt-Automatisierungsklasse
├── setup_ssh_credentials.py    # Einmalige Einrichtung
├── test_ssh_automation.py      # SSH-Agent Tests
├── test_full_automation.py     # Vollständige Integration Tests
├── git_automation_requirements.txt  # Python-Abhängigkeiten
├── README_git_automation.md    # Detaillierte Dokumentation
└── .git_secrets_encrypted.json # Verschlüsselte Credentials (nach Setup)
```

## 🚀 Schnellstart

1. **In den Git-Automation Ordner wechseln:**
   ```bash
   cd git-automation/
   ```

2. **Abhängigkeiten installieren:**
   ```bash
   pip install -r git_automation_requirements.txt
   ```

3. **SSH-Credentials einrichten:**
   ```bash
   python3 setup_ssh_credentials.py
   ```

4. **System testen:**
   ```bash
   python3 test_full_automation.py
   ```

## 💡 Verwendung

```python
import sys
sys.path.append("git-automation/")
from git_automation import SecureGitAutomation

# Automatisierung starten
automation = SecureGitAutomation()
# Master-Password wird einmalig abgefragt
# Git-Operationen können jetzt ausgeführt werden
```

## 🔒 Sicherheit

- **AES-256-CBC Verschlüsselung** für SSH-Passphrases
- **Master-Password** schützt alle Credentials  
- **Automatischer SSH-Agent** ohne manuelle Passphrase-Eingabe
- **Sichere Memory-Bereinigung** nach Operationen

## 📖 Vollständige Dokumentation

Siehe [`README_git_automation.md`](README_git_automation.md) für detaillierte Informationen.

---

**Erstellt für das Vogel-Kamera-Linux Projekt** 📸🐦