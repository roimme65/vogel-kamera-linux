# 📚 Wiki-Sync Verzeichnis

Dieses Verzeichnis enthält alle Tools für die GitHub Wiki-Synchronisation.

## 📁 Dateien

| Datei | Beschreibung |
|-------|--------------|
| `wiki_sync.py` | **Haupt-Skript** für Wiki-Synchronisation |
| `wiki_sync_legacy.py` | Legacy-Version für ältere Python-Versionen |
| `README.md` | Diese Dokumentation |

## 🚀 Verwendung

### Standard-Verwendung (Push)
```bash
cd wiki-sync/
python3 wiki_sync.py
```

### Wiki-Updates holen
```bash
cd wiki-sync/
python3 wiki_sync.py pull
```

### Hilfe
```bash
cd wiki-sync/
python3 wiki_sync.py help
```

## 🔧 Funktionsweise

Das Skript:
1. Arbeitet vom `wiki-sync/` Verzeichnis aus
2. Findet das Haupt-Repository ein Verzeichnis höher (`..`)
3. Nutzt den `wiki-content` Softlink für Wiki-Zugriff
4. Synchronisiert Änderungen mit GitHub Wiki

## 🔗 Pfad-Struktur

```
vogel-kamera-linux/
├── wiki-content/          # ← Softlink zu ../vogel-kamera-linux.wiki
└── wiki-sync/            # ← Aktuelles Verzeichnis
    ├── wiki_sync.py      # ← Haupt-Skript
    └── README.md         # ← Diese Datei
```

## ⚠️ Wichtige Hinweise

- **Immer vom wiki-sync/ Verzeichnis ausführen**
- Das Skript passt automatisch die Pfade an
- Der `wiki-content` Softlink muss existieren
- Git-Credentials müssen konfiguriert sein

---

**Zurück zur Hauptdokumentation:** [../README.md](../README.md)