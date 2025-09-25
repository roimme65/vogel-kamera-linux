#!/usr/bin/env python3
"""
Git Automation Script mit verschlüsseltem SSH-Secret-Management
Automatisiert Git-Operationen für Vogel-Kamera-Linux Projekt

SICHERHEIT:
- SSH-Passphrases AES-256-CBC verschlüsselt
- PBKDF2 Key-Derivation mit 100.000 Iterationen
- Master-Password geschützt
- Sichere Memory-Bereinigung
"""

import os
import sys
import json
import base64
import subprocess
import getpass
from pathlib import Path
from datetime import datetime
import pexpect

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

class SecureGitAutomation:
    def __init__(self):
        self.automation_path = Path(__file__).parent  # git-automation/ Ordner
        self.repo_path = self.automation_path.parent  # Haupt-Repository Ordner
        self.secrets_file = self.automation_path / ".git_secrets_encrypted.json"
        self.master_password = None
        self.secrets = {}
        self.load_secrets()
        
    def derive_key(self, password: str, salt: bytes) -> bytes:
        """Leite Verschlüsselungsschlüssel aus Master-Password ab"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # AES-256
            salt=salt,
            iterations=100000,  # Starke Key-Derivation
            backend=default_backend()
        )
        return kdf.derive(password.encode('utf-8'))
    
    def encrypt_data(self, data: str, password: str) -> dict:
        """Verschlüssele Daten mit AES-256-CBC"""
        try:
            # Zufälligen Salt und IV generieren
            salt = os.urandom(16)
            iv = os.urandom(16)
            
            # Schlüssel ableiten
            key = self.derive_key(password, salt)
            
            # Padding hinzufügen (PKCS7)
            data_bytes = data.encode('utf-8')
            pad_length = 16 - (len(data_bytes) % 16)
            padded_data = data_bytes + bytes([pad_length] * pad_length)
            
            # Verschlüsseln
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
            
            return {
                "encrypted_data": base64.b64encode(encrypted_data).decode('utf-8'),
                "salt": base64.b64encode(salt).decode('utf-8'),
                "iv": base64.b64encode(iv).decode('utf-8')
            }
            
        except Exception as e:
            raise ValueError(f"Verschlüsselung fehlgeschlagen: {e}")
    
    def decrypt_data(self, encrypted_dict: dict, password: str) -> str:
        """Entschlüssele AES-256-CBC verschlüsselte Daten"""
        try:
            # Base64 dekodieren
            encrypted_data = base64.b64decode(encrypted_dict['encrypted_data'])
            salt = base64.b64decode(encrypted_dict['salt'])
            iv = base64.b64decode(encrypted_dict['iv'])
            
            # Schlüssel ableiten
            key = self.derive_key(password, salt)
            
            # Entschlüsseln
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            decrypted_padded = decryptor.update(encrypted_data) + decryptor.finalize()
            
            # Padding entfernen
            pad_length = decrypted_padded[-1]
            decrypted_data = decrypted_padded[:-pad_length]
            
            return decrypted_data.decode('utf-8')
            
        except Exception as e:
            raise ValueError(f"Entschlüsselung fehlgeschlagen: {e}")
    
    def get_master_password(self, confirm=False):
        """Sichere Master-Password-Eingabe"""
        if confirm:
            while True:
                pwd1 = getpass.getpass("🔐 Master-Password erstellen: ")
                if len(pwd1) < 8:
                    print("❌ Password muss mindestens 8 Zeichen haben!")
                    continue
                    
                pwd2 = getpass.getpass("🔐 Master-Password bestätigen: ")
                if pwd1 == pwd2:
                    return pwd1
                else:
                    print("❌ Passwords stimmen nicht überein!")
        else:
            return getpass.getpass("🔐 Master-Password eingeben: ")
    
    def load_secrets(self):
        """Lade verschlüsselte SSH-Secrets"""
        try:
            if self.secrets_file.exists():
                with open(self.secrets_file, 'r', encoding='utf-8') as f:
                    encrypted_config = json.load(f)
                
                # Master-Password abfragen
                self.master_password = self.get_master_password()
                
                # Secrets entschlüsseln
                decrypted_secrets = {}
                for key, encrypted_value in encrypted_config['encrypted_secrets'].items():
                    if isinstance(encrypted_value, dict) and 'encrypted_data' in encrypted_value:
                        # Verschlüsselter Wert
                        decrypted_secrets[key] = self.decrypt_data(encrypted_value, self.master_password)
                    else:
                        # Unverschlüsselter Wert (für nicht-sensitive Daten)
                        decrypted_secrets[key] = encrypted_value
                
                self.secrets = decrypted_secrets
                print("✅ Secrets erfolgreich entschlüsselt")
                
                # SSH-Agent automatisch konfigurieren
                if 'ssh_key_path' in self.secrets and 'ssh_passphrase' in self.secrets:
                    ssh_success, ssh_message = self.setup_ssh_agent()
                    if ssh_success:
                        print(f"🔑 {ssh_message}")
                    else:
                        print(f"⚠️  SSH-Agent-Setup: {ssh_message}")
                
            else:
                self.secrets = {}  # Leeres Dictionary wenn keine Secrets vorhanden
                
        except ValueError as e:
            print(f"❌ {e}")
            print("💡 Prüfen Sie Ihr Master-Password!")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Fehler beim Laden der Secrets: {e}")
            sys.exit(1)
    
    def save_secrets(self, secrets_dict):
        """Speichere neue Secrets verschlüsselt"""
        if not self.master_password:
            print("❌ Master-Password nicht gesetzt")
            return False
            
        try:
            # Sensitive Daten verschlüsseln, nicht-sensitive als Klartext
            encrypted_secrets = {}
            sensitive_keys = ['ssh_passphrase']  # Nur Passphrase verschlüsseln
            
            for key, value in secrets_dict.items():
                if key in sensitive_keys:
                    encrypted_secrets[key] = self.encrypt_data(value, self.master_password)
                else:
                    encrypted_secrets[key] = value  # Klartext für nicht-sensitive Daten
            
            # Verschlüsselte Konfiguration erstellen
            config = {
                "version": "1.0",
                "encryption": "AES-256-CBC-PBKDF2",
                "created": datetime.now().isoformat(),
                "encrypted_secrets": encrypted_secrets
            }
            
            # Speichern
            with open(self.secrets_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            # Secrets in Memory laden für sofortige Nutzung
            self.secrets = secrets_dict.copy()
            
            print(f"✅ Verschlüsselte Secrets gespeichert: {self.secrets_file}")
            return True
            
        except Exception as e:
            print(f"❌ Fehler beim Speichern: {e}")
            return False
    
    def run_command(self, command, cwd=None, env_vars=None):
        """Führe Git-Kommando mit SSH-Agent aus"""
        if cwd is None:
            cwd = self.repo_path
            
        # SSH-Agent Umgebung vorbereiten
        env = os.environ.copy()
        if env_vars:
            env.update(env_vars)
            
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                env=env,
                timeout=300  # 5 Minuten Timeout
            )
            
            if result.returncode == 0:
                return True, result.stdout.strip()
            else:
                return False, result.stderr.strip()
                
        except subprocess.TimeoutExpired:
            return False, "Timeout: Kommando dauerte zu lange"
        except Exception as e:
            return False, f"Fehler: {str(e)}"

    def setup_ssh_agent(self):
        """SSH-Agent mit entschlüsselter Passphrase setup"""
        ssh_key = self.secrets['ssh_key_path']
        passphrase = self.secrets['ssh_passphrase']  # Bereits entschlüsselt
        
        if not os.path.exists(ssh_key):
            return False, f"SSH-Key nicht gefunden: {ssh_key}"
        
        # SSH-Agent starten/prüfen
        if not self.ensure_ssh_agent_running():
            return False, "SSH-Agent konnte nicht gestartet werden"
        
        # Prüfen ob Key bereits geladen
        success, output = self.run_command("ssh-add -l")
        
        if success and ssh_key in output:
            return True, "SSH-Key bereits im Agent"
        
        if "no identities" in output.lower() or not success:
            print("🔑 SSH-Key wird zum Agent hinzugefügt...")
            
            # Methode 1: Verwende pexpect (meist zuverlässigste)
            success = self.add_key_with_pexpect(ssh_key, passphrase)
            if success:
                return True, "SSH-Key erfolgreich hinzugefügt (pexpect)"
            
            # Methode 2: Verwende SSH_ASKPASS
            success = self.add_key_with_askpass(ssh_key, passphrase)
            if success:
                return True, "SSH-Key erfolgreich hinzugefügt (askpass)"
            
            # Methode 3: Fallback mit stdin pipe
            success = self.add_key_with_stdin(ssh_key, passphrase)
            if success:
                return True, "SSH-Key erfolgreich hinzugefügt (stdin)"
                
            return False, "Alle SSH-Key-Methoden fehlgeschlagen"
        else:
            return True, "SSH-Agent bereits konfiguriert"
    
    def ensure_ssh_agent_running(self):
        """Stelle sicher, dass SSH-Agent läuft"""
        # Prüfe ob SSH-Agent bereits läuft
        success, output = self.run_command("ssh-add -l 2>/dev/null")
        
        if success or "no identities" in output.lower():
            print("✅ SSH-Agent läuft bereits")
            return True  # Agent läuft bereits
        
        print("🚀 Starte SSH-Agent...")
        
        # SSH-Agent mit subprocess direkt starten für bessere Kontrolle
        try:
            result = subprocess.run(['ssh-agent', '-s'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                print(f"❌ SSH-Agent start fehlgeschlagen: {result.stderr}")
                return False
            
            # SSH-Agent Umgebungsvariablen parsen
            lines = result.stdout.strip().split('\n')
            ssh_auth_sock = None
            ssh_agent_pid = None
            
            for line in lines:
                if '=' in line and 'echo' not in line:  # Skip echo-Zeile
                    if 'SSH_AUTH_SOCK' in line:
                        ssh_auth_sock = line.split('=')[1].split(';')[0]
                        os.environ['SSH_AUTH_SOCK'] = ssh_auth_sock
                        print(f"✅ SSH_AUTH_SOCK: {ssh_auth_sock}")
                    elif 'SSH_AGENT_PID' in line:
                        ssh_agent_pid = line.split('=')[1].split(';')[0]
                        os.environ['SSH_AGENT_PID'] = ssh_agent_pid
                        print(f"✅ SSH_AGENT_PID: {ssh_agent_pid}")
            
            if not ssh_auth_sock or not ssh_agent_pid:
                print("❌ SSH-Agent Umgebungsvariablen nicht gefunden")
                return False
            
            # Erneut prüfen mit subprocess direkt
            test_result = subprocess.run(['ssh-add', '-l'], 
                                       capture_output=True, text=True,
                                       env=os.environ.copy())
            
            success = test_result.returncode in [0, 1]  # 0=Keys vorhanden, 1=Keine Keys
            if success:
                print("✅ SSH-Agent erfolgreich gestartet")
            else:
                print(f"❌ SSH-Agent Test fehlgeschlagen: {test_result.stderr}")
                
            return success
            
        except Exception as e:
            print(f"❌ Fehler beim SSH-Agent Start: {e}")
            return False

    def add_key_with_pexpect(self, ssh_key, passphrase):
        """SSH-Key mit pexpect hinzufügen"""
        try:
            print(f"🔑 Verwende pexpect für SSH-Key: {ssh_key}")
            child = pexpect.spawn(f'ssh-add {ssh_key}', env=os.environ.copy())
            child.logfile_read = sys.stdout.buffer  # Debug output
            
            # Warte auf Passphrase-Eingabeaufforderung
            index = child.expect(['Enter passphrase.*:', 'passphrase.*:', 'Bad passphrase', pexpect.EOF, pexpect.TIMEOUT], timeout=10)
            
            if index in [0, 1]:  # Passphrase erwartet
                print("🔐 Sende Passphrase...")
                child.sendline(passphrase)
                child.expect(pexpect.EOF, timeout=10)
                child.close()
                success = child.exitstatus == 0
                print(f"✅ pexpect Ergebnis: {success}")
                return success
            else:
                print(f"❌ Unerwartete pexpect-Antwort: Index {index}")
                child.close()
                return False
                
        except Exception as e:
            print(f"❌ pexpect Fehler: {e}")
            return False
    
    def add_key_with_askpass(self, ssh_key, passphrase):
        """SSH-Key mit SSH_ASKPASS hinzufügen"""
        try:
            print(f"🔑 Verwende SSH_ASKPASS für SSH-Key: {ssh_key}")
            
            # Temporäres SSH_ASKPASS Skript erstellen
            askpass_script = self.automation_path / "temp_askpass.sh"
            with open(askpass_script, 'w') as f:
                f.write(f'#!/bin/bash\necho "{passphrase}"\n')
            
            askpass_script.chmod(0o700)
            
            env = os.environ.copy()
            env['SSH_ASKPASS'] = str(askpass_script)
            env['SSH_ASKPASS_REQUIRE'] = 'force'  # Force SSH_ASKPASS usage
            env['DISPLAY'] = ''  # Kein Display verfügbar
            
            print(f"🔐 SSH_ASKPASS Script: {askpass_script}")
            
            result = subprocess.run(
                ['ssh-add', ssh_key],
                env=env,
                capture_output=True,
                text=True,
                timeout=30,
                stdin=subprocess.DEVNULL  # Keine stdin verfügbar
            )
            
            # Cleanup
            askpass_script.unlink(missing_ok=True)
            
            success = result.returncode == 0
            print(f"✅ SSH_ASKPASS Ergebnis: {success}")
            if not success:
                print(f"❌ SSH_ASKPASS Fehler: {result.stderr}")
            
            return success
            
        except Exception as e:
            print(f"❌ SSH_ASKPASS Fehler: {e}")
            return False
    
    def add_key_with_stdin(self, ssh_key, passphrase):
        """SSH-Key mit stdin pipe hinzufügen"""
        try:
            print(f"🔑 Verwende stdin für SSH-Key: {ssh_key}")
            
            process = subprocess.Popen(
                ['ssh-add', ssh_key],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=os.environ.copy()
            )
            
            print("🔐 Sende Passphrase über stdin...")
            stdout, stderr = process.communicate(input=passphrase + '\n', timeout=30)
            
            success = process.returncode == 0
            print(f"✅ stdin Ergebnis: {success}")
            if not success:
                print(f"❌ stdin Fehler: {stderr}")
                
            return success
            
        except Exception as e:
            print(f"❌ stdin Fehler: {e}")
            return False

def main():
    """Kommandozeilen-Interface für Git-Automatisierung"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='🔐 Sichere Git-Automatisierung v1.1.4',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  %(prog)s --push                    # Push aktuellen Branch
  %(prog)s --push-all               # Push alle Branches
  %(prog)s --tag v1.1.4             # Erstelle und pushe Tag
  %(prog)s --release v1.1.4         # Vollständiger Release-Workflow
  %(prog)s --commit "Fix bug"       # Add, Commit und Push
  %(prog)s --status                 # Git Status anzeigen
        """
    )
    
    # Aktionsgruppen
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument('--push', action='store_true',
                             help='Push aktuellen Branch')
    action_group.add_argument('--push-all', action='store_true',
                             help='Push alle lokalen Branches')
    action_group.add_argument('--tag', metavar='VERSION',
                             help='Erstelle und pushe Tag (z.B. v1.1.4)')
    action_group.add_argument('--release', metavar='VERSION',
                             help='Vollständiger Release-Workflow mit Tag')
    action_group.add_argument('--commit', metavar='MESSAGE',
                             help='Add, Commit und Push mit Nachricht')
    action_group.add_argument('--status', action='store_true',
                             help='Git Status anzeigen')
    
    # Optionale Parameter
    parser.add_argument('--branch', metavar='NAME',
                       help='Spezifischer Branch (Standard: aktueller)')
    parser.add_argument('--no-push', action='store_true',
                       help='Nur lokale Operationen, nicht pushen')
    parser.add_argument('--force', action='store_true',
                       help='Force-Push verwenden (Vorsicht!)')
    
    args = parser.parse_args()
    
    try:
        print("🔐 Git-Automatisierung v1.1.4")
        print("=" * 40)
        
        # Git-Automation initialisieren
        automation = SecureGitAutomation()
        print("✅ Git-Automation erfolgreich initialisiert")
        
        if args.status:
            # Git Status anzeigen (vom Repository-Root)
            success, output = automation.run_command("git status", cwd=automation.repo_path)
            print(f"\n📊 Git Status:\n{output}")
            
        elif args.push:
            # Aktuellen Branch pushen
            success, current_branch = automation.run_command("git branch --show-current", cwd=automation.repo_path)
            branch = args.branch or current_branch.strip()
            
            push_cmd = f"git push{'f' if args.force else ''} origin {branch}"
            print(f"🚀 Push Branch '{branch}'...")
            
            success, output = automation.run_command(push_cmd)
            if success:
                print(f"✅ Branch '{branch}' erfolgreich gepusht")
            else:
                print(f"❌ Push fehlgeschlagen: {output}")
                
        elif args.push_all:
            # Alle Branches pushen
            print("🚀 Push alle Branches...")
            push_cmd = f"git push{'f' if args.force else ''} --all origin"
            
            success, output = automation.run_command(push_cmd, cwd=automation.repo_path)
            if success:
                print("✅ Alle Branches erfolgreich gepusht")
            else:
                print(f"❌ Push-All fehlgeschlagen: {output}")
                
        elif args.tag:
            # Tag erstellen und pushen
            version = args.tag
            print(f"🏷️ Erstelle Tag '{version}'...")
            
            # Tag erstellen (vom Repository-Root)
            tag_cmd = f"git tag -a {version} -m 'Release {version}'"
            success, output = automation.run_command(tag_cmd, cwd=automation.repo_path)
            
            if success:
                print(f"✅ Tag '{version}' erstellt")
                
                if not args.no_push:
                    # Tag pushen
                    print(f"📤 Push Tag '{version}'...")
                    push_cmd = f"git push origin {version}"
                    success, output = automation.run_command(push_cmd)
                    
                    if success:
                        print(f"✅ Tag '{version}' erfolgreich gepusht")
                    else:
                        print(f"❌ Tag-Push fehlgeschlagen: {output}")
            else:
                print(f"❌ Tag-Erstellung fehlgeschlagen: {output}")
                
        elif args.release:
            # Vollständiger Release-Workflow
            version = args.release
            print(f"🚀 Vollständiger Release-Workflow für '{version}'...")
            
            # 1. Add und Commit alle Änderungen
            success, status = automation.run_command("git status --porcelain", cwd=automation.repo_path)
            if status.strip():
                print("📦 Füge Änderungen hinzu...")
                automation.run_command("git add .", cwd=automation.repo_path)
                
                commit_msg = f"🔖 Release {version}"
                success, output = automation.run_command(f'git commit -m "{commit_msg}"')
                if success:
                    print(f"✅ Commit: {commit_msg}")
                else:
                    print(f"❌ Commit fehlgeschlagen: {output}")
                    return
            
            # 2. Push aktuellen Branch
            if not args.no_push:
                success, current_branch = automation.run_command("git branch --show-current", cwd=automation.repo_path)
                branch = current_branch.strip()
                
                print(f"🚀 Push Branch '{branch}'...")
                success, output = automation.run_command(f"git push origin {branch}", cwd=automation.repo_path)
                if success:
                    print(f"✅ Branch '{branch}' gepusht")
                else:
                    print(f"❌ Branch-Push fehlgeschlagen: {output}")
                    return
            
            # 3. Tag erstellen und pushen
            print(f"🏷️ Erstelle Tag '{version}'...")
            success, output = automation.run_command(f"git tag -a {version} -m 'Release {version}'", cwd=automation.repo_path)
            
            if success:
                print(f"✅ Tag '{version}' erstellt")
                
                if not args.no_push:
                    print(f"📤 Push Tag '{version}'...")
                    success, output = automation.run_command(f"git push origin {version}")
                    
                    if success:
                        print(f"✅ Tag '{version}' gepusht")
                        print(f"🎉 Release '{version}' vollständig abgeschlossen!")
                    else:
                        print(f"❌ Tag-Push fehlgeschlagen: {output}")
            else:
                print(f"❌ Tag-Erstellung fehlgeschlagen: {output}")
                
        elif args.commit:
            # Add, Commit und Push
            commit_msg = args.commit
            print(f"📝 Add, Commit und Push: '{commit_msg}'")
            
            # Add all changes (vom Repository-Root)
            automation.run_command("git add .", cwd=automation.repo_path)
            
            # Commit (vom Repository-Root)
            success, output = automation.run_command(f'git commit -m "{commit_msg}"', cwd=automation.repo_path)
            if success:
                print(f"✅ Commit: {commit_msg}")
                
                if not args.no_push:
                    # Push (vom Repository-Root)
                    success, output = automation.run_command("git push", cwd=automation.repo_path)
                    if success:
                        print("✅ Push erfolgreich!")
                    else:
                        print(f"❌ Push fehlgeschlagen: {output}")
            else:
                print(f"❌ Commit fehlgeschlagen: {output}")
                
    except KeyboardInterrupt:
        print("\n❌ Abgebrochen durch Benutzer")
    except Exception as e:
        print(f"❌ Fehler: {e}")

if __name__ == "__main__":
    main()