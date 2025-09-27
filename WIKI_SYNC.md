# 🔄 Wiki-Synchronisation

Automatische Synchronisation zwischen Haupt-Repository und GitHub Wiki über Softlink.

## 📁 Setup

Das `wiki-content/` Verzeichnis ist ein **Softlink** zum GitHub Wiki-Repository:

```bash
wiki-content -> ../vogel-kamera-linux.wiki
```

## 🚀 Verwendung

### Wiki-Änderungen pushen
```bash
# Automatische Synchronisation (Standard)
python3 wiki_sync.py

# Explizit pushen
python3 wiki_sync.py sync
```

### Wiki-Änderungen holen
```bash
# Aktuelle Wiki-Inhalte vom GitHub holen
python3 wiki_sync.py pull
```

## 🔄 Workflow

### 1. Wiki-Inhalte bearbeiten
```bash
# Dateien direkt im wiki-content/ bearbeiten
nano wiki-content/Installation-Guide.md

# Oder mit VS Code
code wiki-content/
```

### 2. Änderungen synchronisieren
```bash
# Automatisch committen und pushen
python3 wiki_sync.py

# Ausgabe:
# 🔄 Wiki-Synchronisation gestartet...
# 📝 Änderungen im Wiki gefunden:
# M  Installation-Guide.md
# ✅ Wiki-Änderungen erfolgreich gepusht!
```

### 3. Wiki auf GitHub prüfen
Die Änderungen sind sofort im GitHub Wiki verfügbar:
`https://github.com/roimme65/vogel-kamera-linux/wiki`

## 📋 Git-Integration

### .gitignore angepasst
```bash
# wiki-content/ ist jetzt ein Softlink - nicht ignorieren
# wiki-content/
```

### Softlink erstellen (Setup)
```bash
# Falls der Softlink neu erstellt werden muss:
rm -rf wiki-content
ln -sf ../vogel-kamera-linux.wiki wiki-content
```

## 🎯 Vorteile

- ✅ **Direkter Zugriff** auf Wiki-Inhalte vom Haupt-Repository
- ✅ **Einheitliche Bearbeitung** mit VS Code/Editor
- ✅ **Automatische Synchronisation** mit einem Befehl
- ✅ **Git-History** für Wiki-Änderungen
- ✅ **Keine doppelte Datenhaltung**

## 🔧 Troubleshooting

### Softlink reparieren
```bash
# Prüfen ob Softlink korrekt ist
ls -la wiki-content/

# Neu erstellen falls nötig
rm wiki-content
ln -sf ../vogel-kamera-linux.wiki wiki-content
```

### Wiki-Repository klonen (falls nicht vorhanden)
```bash
cd /media/imme/912f030f-2be4-4e28-9295-fb0ad95218c5/daten/git/
git clone https://github.com/roimme65/vogel-kamera-linux.wiki.git
```

### Manuelle Synchronisation
```bash
# In das Wiki-Verzeichnis wechseln
cd wiki-content/

# Änderungen prüfen
git status

# Manuell committen und pushen
git add .
git commit -m "Wiki-Update"
git push origin master
```