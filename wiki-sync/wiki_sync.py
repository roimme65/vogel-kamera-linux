#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wiki Sync Script fuer Vogel-Kamera-Linux
=========================================
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, cwd=None):
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, 
                              capture_output=True, text=True, check=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, f"Fehler: {e.stderr}"
    except Exception as e:
        return False, f"Unerwarteter Fehler: {str(e)}"

def sync_wiki():
    # Pfade (ein Verzeichnis hoeher wegen wiki-sync/)
    repo_root = Path(__file__).parent.parent
    wiki_path = repo_root / "wiki-content"
    
    print("Wiki-Synchronisation gestartet...")
    print(f"Repository Root: {repo_root}")
    
    if not wiki_path.is_symlink():
        print("FEHLER: wiki-content ist kein Softlink!")
        return False
        
    wiki_target = wiki_path.resolve()
    print(f"Wiki-Pfad: {wiki_target}")
    
    success, status = run_command("git status --porcelain", cwd=wiki_target)
    if not success:
        print(f"FEHLER Git-Status: {status}")
        return False
        
    if status.strip():
        print("Aenderungen gefunden:")
        print(status)
        
        success, _ = run_command("git add .", cwd=wiki_target)
        if not success:
            print("FEHLER: Git add fehlgeschlagen")
            return False
            
        commit_msg = "Wiki-Update: Synchronisation (wiki-sync)"
        success, _ = run_command(f'git commit -m "{commit_msg}"', cwd=wiki_target)
        if not success:
            print("FEHLER: Git commit fehlgeschlagen")
            return False
            
        success, _ = run_command("git push origin master", cwd=wiki_target)
        if not success:
            print("FEHLER: Git push fehlgeschlagen")
            return False
            
        print("ERFOLG: Wiki gepusht!")
    else:
        print("Keine Aenderungen im Wiki")
    
    return True

def pull_wiki():
    repo_root = Path(__file__).parent.parent
    wiki_path = repo_root / "wiki-content"
    wiki_target = wiki_path.resolve()
    
    print("Wiki-Pull gestartet...")
    
    success, _ = run_command("git pull origin master", cwd=wiki_target)
    if success:
        print("ERFOLG: Wiki aktualisiert")
    else:
        print("FEHLER: Wiki-Pull fehlgeschlagen")
    
    return success

def main():
    print("Vogel-Kamera-Linux Wiki Sync v1.1")
    print(f"Working Directory: {os.getcwd()}")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command == "pull":
            success = pull_wiki()
        elif command in ["sync", "push"]:
            success = sync_wiki()
        else:
            print("Usage: python3 wiki_sync.py [pull|sync|push]")
            return False
    else:
        success = sync_wiki()
    
    print("=" * 50)
    print("ERFOLG!" if success else "FEHLER!")
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
