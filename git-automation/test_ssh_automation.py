#!/usr/bin/env python3
"""
Test SSH-Automatisierung mit SecureGitAutomation
"""
import os
import sys
import subprocess
from pathlib import Path

# Git-Automation importieren
sys.path.append(str(Path(__file__).parent))
from git_automation import SecureGitAutomation

def test_ssh_agent_standalone():
    """Test SSH-Agent Start ohne Klasse"""
    print("=== Test: SSH-Agent Standalone ===")
    
    # Umgebung zurücksetzen
    for var in ['SSH_AUTH_SOCK', 'SSH_AGENT_PID']:
        if var in os.environ:
            del os.environ[var]
    
    # SSH-Agent starten
    result = subprocess.run(['ssh-agent', '-s'], capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ SSH-Agent start fehlgeschlagen")
        return False
    
    # Umgebungsvariablen parsen
    lines = result.stdout.strip().split('\n')
    for line in lines:
        if '=' in line and 'echo' not in line:
            if 'SSH_AUTH_SOCK' in line:
                sock_value = line.split('=')[1].split(';')[0]
                os.environ['SSH_AUTH_SOCK'] = sock_value
                print(f"✅ SSH_AUTH_SOCK: {sock_value}")
            elif 'SSH_AGENT_PID' in line:
                pid_value = line.split('=')[1].split(';')[0]
                os.environ['SSH_AGENT_PID'] = pid_value
                print(f"✅ SSH_AGENT_PID: {pid_value}")
    
    # Test ssh-add -l
    test_result = subprocess.run(['ssh-add', '-l'], capture_output=True, text=True)
    print(f"✅ ssh-add -l: Exit-Code {test_result.returncode} (0=Keys vorhanden, 1=Keine Keys)")
    print(f"   Ausgabe: '{test_result.stdout.strip()}'")
    
    return test_result.returncode in [0, 1]

def test_git_automation_class():
    """Test SecureGitAutomation Klasse SSH-Agent-Methoden"""
    print("\n=== Test: SecureGitAutomation Klasse ===")
    
    try:
        automation = SecureGitAutomation()
        
        # SSH-Agent ensure test
        result = automation.ensure_ssh_agent_running()
        print(f"✅ ensure_ssh_agent_running(): {result}")
        
        if result:
            print(f"✅ SSH_AUTH_SOCK: {os.environ.get('SSH_AUTH_SOCK', 'Nicht gesetzt')}")
            print(f"✅ SSH_AGENT_PID: {os.environ.get('SSH_AGENT_PID', 'Nicht gesetzt')}")
            
            # Test ssh-add über run_command
            success, output = automation.run_command("ssh-add -l")
            print(f"✅ run_command('ssh-add -l'): Success={success}, Output='{output.strip()}'")
        
        return result
        
    except Exception as e:
        print(f"❌ Fehler beim Testen der Klasse: {e}")
        return False

def find_ssh_key():
    """Suche nach SSH-Keys"""
    print("\n=== SSH-Key Suche ===")
    
    ssh_dir = Path.home() / '.ssh'
    if not ssh_dir.exists():
        print("❌ ~/.ssh Verzeichnis nicht gefunden")
        return None
    
    # Gängige SSH-Key-Namen
    key_names = ['id_rsa', 'id_ed25519', 'id_ecdsa']
    
    for key_name in key_names:
        key_path = ssh_dir / key_name
        if key_path.exists():
            print(f"✅ SSH-Key gefunden: {key_path}")
            return str(key_path)
    
    print("❌ Kein SSH-Key gefunden")
    return None

def main():
    """Haupttest-Funktion"""
    print("🔑 SSH-Automatisierung Test")
    print("=" * 50)
    
    # Test 1: Standalone SSH-Agent
    standalone_ok = test_ssh_agent_standalone()
    
    # Test 2: Git-Automation Klasse
    class_ok = test_git_automation_class()
    
    # Test 3: SSH-Key suchen
    ssh_key = find_ssh_key()
    
    # Zusammenfassung
    print("\n" + "=" * 50)
    print("📊 Test-Zusammenfassung:")
    print(f"✅ SSH-Agent Standalone: {'OK' if standalone_ok else 'FEHLER'}")
    print(f"✅ SecureGitAutomation: {'OK' if class_ok else 'FEHLER'}")
    print(f"✅ SSH-Key vorhanden: {'OK' if ssh_key else 'FEHLER'}")
    
    if standalone_ok and class_ok:
        print("\n🎉 SSH-Automatisierung funktioniert!")
        print("Nächster Schritt: Verschlüsselte Secrets einrichten")
    else:
        print("\n❌ SSH-Automatisierung hat Probleme")
        
    return standalone_ok and class_ok

if __name__ == "__main__":
    main()