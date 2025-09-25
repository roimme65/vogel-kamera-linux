#!/usr/bin/env python3
"""
SSH-Credentials Setup für SecureGitAutomation
Erstellt verschlüsselte SSH-Konfiguration mit Master-Password
"""
import json
import os
from pathlib import Path
from getpass import getpass
import sys

# Git-Automation importieren
sys.path.append(str(Path(__file__).parent))
from git_automation import SecureGitAutomation

def find_ssh_key():
    """Finde SSH-Key automatisch oder frage nach Pfad"""
    ssh_dir = Path.home() / '.ssh'
    
    # Automatische Suche
    key_names = ['id_ed25519', 'id_rsa', 'id_ecdsa']
    found_keys = []
    
    for key_name in key_names:
        key_path = ssh_dir / key_name
        if key_path.exists():
            found_keys.append(str(key_path))
    
    if found_keys:
        print("🔍 Gefundene SSH-Keys:")
        for i, key in enumerate(found_keys, 1):
            print(f"  {i}. {key}")
        
        if len(found_keys) == 1:
            choice = input(f"\n📁 SSH-Key verwenden '{found_keys[0]}'? (j/n): ").lower()
            if choice in ['j', 'ja', 'y', 'yes', '']:
                return found_keys[0]
        else:
            while True:
                try:
                    choice = input(f"\n📁 Welchen SSH-Key verwenden? (1-{len(found_keys)}): ")
                    idx = int(choice) - 1
                    if 0 <= idx < len(found_keys):
                        return found_keys[idx]
                    print("❌ Ungültige Auswahl")
                except ValueError:
                    print("❌ Bitte eine Zahl eingeben")
    
    # Manueller Pfad
    while True:
        key_path = input("📁 SSH-Key Pfad eingeben: ").strip()
        if Path(key_path).exists():
            return key_path
        print("❌ Datei nicht gefunden")

def setup_git_config():
    """Git-Konfiguration erfassen"""
    print("\n🔧 Git-Konfiguration")
    
    # Git-Name und Email abfragen
    try:
        import subprocess
        name_result = subprocess.run(['git', 'config', '--global', 'user.name'], 
                                   capture_output=True, text=True)
        email_result = subprocess.run(['git', 'config', '--global', 'user.email'], 
                                    capture_output=True, text=True)
        
        current_name = name_result.stdout.strip() if name_result.returncode == 0 else ""
        current_email = email_result.stdout.strip() if email_result.returncode == 0 else ""
        
    except:
        current_name = ""
        current_email = ""
    
    # Name
    if current_name:
        name = input(f"👤 Git-Name [{current_name}]: ").strip() or current_name
    else:
        name = input("👤 Git-Name: ").strip()
    
    # Email
    if current_email:
        email = input(f"📧 Git-Email [{current_email}]: ").strip() or current_email
    else:
        email = input("📧 Git-Email: ").strip()
    
    return name, email

def main():
    """Hauptsetup-Funktion"""
    print("🔐 SSH-Credentials Setup für SecureGitAutomation")
    print("=" * 60)
    
    # Prüfe ob Setup bereits existiert
    secrets_file = Path(__file__).parent / ".git_secrets_encrypted.json"
    if secrets_file.exists():
        choice = input("⚠️  Verschlüsselte Secrets existieren bereits. Überschreiben? (j/n): ")
        if choice.lower() not in ['j', 'ja', 'y', 'yes']:
            print("❌ Setup abgebrochen")
            return
    
    print("\n1️⃣  SSH-Key auswählen")
    ssh_key_path = find_ssh_key()
    print(f"✅ SSH-Key: {ssh_key_path}")
    
    print("\n2️⃣  SSH-Key Passphrase eingeben")
    ssh_passphrase = getpass("🔑 SSH-Key Passphrase: ")
    
    if not ssh_passphrase.strip():
        print("❌ Passphrase darf nicht leer sein")
        return
    
    print("\n3️⃣  Git-Konfiguration")
    git_name, git_email = setup_git_config()
    
    print("\n4️⃣  Master-Password für Verschlüsselung")
    master_password = getpass("🔐 Master-Password eingeben: ")
    master_password_confirm = getpass("🔐 Master-Password bestätigen: ")
    
    if master_password != master_password_confirm:
        print("❌ Passwörter stimmen nicht überein")
        return
    
    if len(master_password) < 8:
        print("❌ Master-Password muss mindestens 8 Zeichen lang sein")
        return
    
    print("\n5️⃣  Secrets verschlüsseln und speichern")
    
    # Secrets Dictionary erstellen
    secrets_data = {
        'ssh_key_path': ssh_key_path,
        'ssh_passphrase': ssh_passphrase,
        'git_name': git_name,
        'git_email': git_email
    }
    
    # SecureGitAutomation für Verschlüsselung verwenden
    try:
        # Temporäre Instanz erstellen
        automation = SecureGitAutomation()
        
        # Secrets verschlüsseln und speichern
        automation.master_password = master_password
        success = automation.save_secrets(secrets_data)
        
        if success:
            print("✅ Secrets erfolgreich verschlüsselt und gespeichert")
            print(f"📁 Datei: {secrets_file.absolute()}")
            
            print("\n6️⃣  Setup testen")
            # Test SSH-Agent Setup
            test_success, message = automation.setup_ssh_agent()
            if test_success:
                print(f"✅ SSH-Setup Test: {message}")
                print("\n🎉 Setup erfolgreich abgeschlossen!")
                print("\nNächste Schritte:")
                print("1. git_automation.py für automatische Commits/Push verwenden")
                print("2. Master-Password sicher aufbewahren")
                print("3. .git_secrets_encrypted.json NICHT in Git committen")
            else:
                print(f"❌ SSH-Setup Test fehlgeschlagen: {message}")
                print("⚠️  Setup wurde gespeichert, aber SSH funktioniert noch nicht")
        else:
            print("❌ Fehler beim Speichern der Secrets")
            
    except Exception as e:
        print(f"❌ Fehler beim Setup: {e}")
        return

if __name__ == "__main__":
    main()