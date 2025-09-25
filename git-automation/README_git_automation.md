# 🔐 Sichere Git-Automatisierung

Automatisierte Git-Operationen mit AES-256 verschlüsselten SSH-Credentials.

## ✨ Features

- **🔒 AES-256-CBC Verschlüsselung** mit PBKDF2 Key-Derivation
- **🚀 Automatischer SSH-Agent** mit drei Fallback-Methoden
- **🔑 Sichere Passphrase-Behandlung** ohne Klartext-Speicherung
- **🛡️ Master-Password Schutz** für alle Credentials
- **🧹 Secure Memory Cleanup** nach Operationen

## 📁 Dateien

| Datei | Beschreibung |
|-------|--------------|
| `git_automation.py` | Haupt-Automatisierungsklasse mit AES-Verschlüsselung |
| `setup_ssh_credentials.py` | Einmalige Einrichtung der verschlüsselten Credentials |
| `test_ssh_automation.py` | Test der SSH-Agent-Funktionalität |
| `test_full_automation.py` | Vollständiger Integrationstest |
| `.git_secrets_encrypted.json` | Verschlüsselte Credentials (wird erstellt) |

## 🚀 Schnellstart

### 1. Abhängigkeiten installieren

```bash
cd git-automation/
pip install -r git_automation_requirements.txt
```

### 2. SSH-Credentials einrichten

```bash
cd git-automation/
python3 setup_ssh_credentials.py
```

Das Setup-Skript führt Sie durch:
- SSH-Key Auswahl (automatische Erkennung)
- SSH-Key Passphrase eingeben
- Git-Konfiguration (Name, Email)
- Master-Password für Verschlüsselung

### 3. Funktionalität testen

```bash
cd git-automation/

# SSH-Agent Test
python3 test_ssh_automation.py

# Vollständiger Integrationstest
python3 test_full_automation.py
```

### 4. Git-Automatisierung verwenden

```python
import sys
from pathlib import Path

# Git-Automation importieren
sys.path.append("git-automation/")
from git_automation import SecureGitAutomation

# Automatisierung initialisieren
automation = SecureGitAutomation()

# SSH-Agent setup (automatisch bei Git-Operationen)
success, message = automation.setup_ssh_agent()

# Git-Operationen ausführen (werden im Repository-Root ausgeführt)
automation.run_command("git add .")
automation.run_command('git commit -m "Automatischer Commit"')
automation.run_command("git push")
```

## 🔧 Konfiguration

### Verschlüsselte Secrets

Die Datei `.git_secrets_encrypted.json` enthält:

```json
{
  "encrypted_data": "...",  // AES-256-CBC verschlüsselte Daten
  "salt": "...",           // PBKDF2 Salt (Base64)
  "iv": "..."              // AES Initialization Vector (Base64)
}
```

**⚠️ Wichtig:** Diese Datei NICHT in Git committen!

### Unterstützte Secrets

- `ssh_key_path`: Pfad zum SSH-Private-Key
- `ssh_passphrase`: SSH-Key Passphrase
- `git_name`: Git-Benutzername
- `git_email`: Git-Email-Adresse

## 🛡️ Sicherheitsfeatures

### Verschlüsselung

- **AES-256-CBC**: Symmetrische Verschlüsselung
- **PBKDF2-SHA256**: Key-Derivation mit 100.000 Iterationen
- **Cryptographically secure random**: Salt und IV-Generierung

### SSH-Agent Integration

Drei Fallback-Methoden für SSH-Key-Hinzufügung:

1. **pexpect**: Python-expect Automatisierung (bevorzugt)
2. **SSH_ASKPASS**: Umgebungsvariablen-basiert
3. **stdin**: Direct pipe Fallback

### Memory Security

- Sichere Passwort-Bereinigung nach Verwendung
- Automatisches Cleanup von Secrets im Arbeitsspeicher

## 🔍 Debugging

### SSH-Agent Probleme

```bash
# SSH-Agent Status prüfen
ssh-add -l

# SSH-Verbindung zu GitHub testen
ssh -T git@github.com

# Environment-Variablen prüfen
echo $SSH_AUTH_SOCK
echo $SSH_AGENT_PID
```

### Verschlüsselung debuggen

```python
# Secrets manuell entschlüsseln
automation = SecureGitAutomation()
# Master-Password wird interaktiv abgefragt
print(automation.secrets)
```

## 📋 Anforderungen

- Python 3.7+
- `cryptography >= 41.0.0`
- `pexpect >= 4.8.0`
- SSH-Key mit Passphrase
- Git-Repository mit Remote

## 🚨 Sicherheitshinweise

1. **Master-Password sicher aufbewahren** - ohne Passwort sind Secrets unbrauchbar
2. **`.git_secrets_encrypted.json` nicht committen** - lokale Datei!
3. **SSH-Key zu GitHub/GitLab hinzufügen** - für Remote-Operationen
4. **Regelmäßige Backups** der verschlüsselten Secrets-Datei

## 🎯 Anwendungsfälle

- **Automatisierte Releases**: Version-Updates und Tags
- **CI/CD Integration**: Sichere Git-Operationen in Pipelines
- **Batch-Operationen**: Multiple Repository-Updates
- **Entwickler-Workflows**: Vereinfachte Git-Kommandos

## 🔄 Version Management Integration

Das System integriert sich perfekt mit dem bestehenden Version-Management:

```python
# Version update + automatischer Push
automation = SecureGitAutomation()
automation.run_command("git add version.py __version__.py README.md")
automation.run_command('git commit -m "🔖 Version v1.1.4"')
automation.run_command("git push")
automation.run_command("git tag v1.1.4")
automation.run_command("git push origin v1.1.4")
```

---

**Erstellt für das Vogel-Kamera-Linux Projekt** 📸🐦