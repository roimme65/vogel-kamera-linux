#!/usr/bin/env python3
"""
Wiki Synchronisation Script
Synchronisiert Änderungen zwischen Haupt-Repository und GitHub Wiki
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, cwd=None):
    """Führe Shell-Befehl aus"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, 
                              capture_output=True, text=True, check=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def sync_wiki():
    """Synchronisiere Wiki-Änderungen"""
    
    # Pfade
    repo_root = Path(__file__).parent
    wiki_path = repo_root / "wiki-content"
    
    print("🔄 Wiki-Synchronisation gestartet...")
    
    # 1. Prüfe ob Wiki-Link existiert
    if not wiki_path.is_symlink():
        print("❌ wiki-content ist kein Softlink!")
        return False
        
    wiki_target = wiki_path.resolve()
    print(f"📁 Wiki-Pfad: {wiki_target}")
    
    # 2. Git-Status im Wiki prüfen
    success, status = run_command("git status --porcelain", cwd=wiki_target)
    if not success:
        print(f"❌ Git-Status Fehler: {status}")
        return False
        
    if status.strip():
        print("📝 Änderungen im Wiki gefunden:")
        print(status)
        
        # 3. Wiki-Änderungen committen und pushen
        success, _ = run_command("git add .", cwd=wiki_target)
        if not success:
            print("❌ Git add fehlgeschlagen")
            return False
            
        commit_msg = "📝 Wiki-Update: Synchronisation vom Haupt-Repository"
        success, _ = run_command(f'git commit -m "{commit_msg}"', cwd=wiki_target)
        if not success:
            print("❌ Git commit fehlgeschlagen")
            return False
            
        success, _ = run_command("git push origin master", cwd=wiki_target)
        if not success:
            print("❌ Git push fehlgeschlagen")
            return False
            
        print("✅ Wiki-Änderungen erfolgreich gepusht!")
    else:
        print("✅ Keine Änderungen im Wiki")
    
    return True

def pull_wiki():
    """Hole aktuelle Wiki-Änderungen"""
    
    repo_root = Path(__file__).parent
    wiki_path = repo_root / "wiki-content"
    wiki_target = wiki_path.resolve()
    
    print("🔄 Wiki-Pull gestartet...")
    
    success, _ = run_command("git pull origin master", cwd=wiki_target)
    if success:
        print("✅ Wiki aktualisiert")
    else:
        print("❌ Wiki-Pull fehlgeschlagen")
    
    return success

if __name__ == "__main__":
    print("🐦 Vogel-Kamera-Linux Wiki Sync v1.0")
    print(f"📁 Working Directory: {os.getcwd()}")
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "pull":
            pull_wiki()
        elif sys.argv[1] == "sync" or sys.argv[1] == "push":
            sync_wiki()
        else:
            print("❌ Unbekanntes Argument!")
            print("Usage: python3 wiki_sync.py [pull|sync|push]")
            print("  pull  - Wiki-Änderungen von GitHub holen")
            print("  sync  - Lokale Änderungen zum GitHub Wiki pushen") 
            print("  push  - Alias für sync")
            print("  (ohne Argument) - Standard: sync")
    else:
        # Default: Sync
        sync_wiki()