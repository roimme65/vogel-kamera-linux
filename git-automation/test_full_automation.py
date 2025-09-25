#!/usr/bin/env python3
"""
Test der vollständigen Git-Automatisierung
"""
import sys
from pathlib import Path
from getpass import getpass

# Git-Automation importieren
sys.path.append(str(Path(__file__).parent))
from git_automation import SecureGitAutomation

def test_full_automation():
    """Teste vollständige Git-Automatisierung"""
    print("🚀 Test: Vollständige Git-Automatisierung")
    print("=" * 50)
    
    try:
        # SecureGitAutomation initialisieren
        automation = SecureGitAutomation()
        
        print("1️⃣  SSH-Agent Setup testen...")
        ssh_success, ssh_message = automation.setup_ssh_agent()
        print(f"   SSH-Setup: {ssh_message}")
        
        if not ssh_success:
            print("❌ SSH-Setup fehlgeschlagen - Abbruch")
            return False
        
        print("\n2️⃣  Git-Status prüfen...")
        status_success, status_output = automation.run_command("git status --porcelain")
        
        if status_success:
            if status_output.strip():
                print(f"   📝 Unversionierte Änderungen vorhanden:")
                for line in status_output.strip().split('\n')[:5]:  # Max 5 Zeilen
                    print(f"      {line}")
                if len(status_output.strip().split('\n')) > 5:
                    print("      ...")
            else:
                print("   ✅ Repository ist sauber (keine Änderungen)")
        else:
            print(f"   ❌ Git-Status Fehler: {status_output}")
            return False
        
        print("\n3️⃣  Remote-Verbindung testen...")
        remote_success, remote_output = automation.run_command("git remote -v")
        
        if remote_success and remote_output.strip():
            print("   📡 Git-Remotes:")
            for line in remote_output.strip().split('\n'):
                print(f"      {line}")
        else:
            print("   ⚠️  Keine Git-Remotes konfiguriert")
        
        print("\n4️⃣  SSH-Verbindung zu GitHub testen...")
        ssh_test_success, ssh_test_output = automation.run_command("ssh -T git@github.com")
        
        # SSH zu GitHub gibt immer exit code 1 zurück, aber mit erfolgreicher Nachricht
        if "successfully authenticated" in ssh_test_output:
            print("   ✅ SSH-Verbindung zu GitHub erfolgreich")
        else:
            print(f"   ❌ SSH-Verbindung Test: {ssh_test_output}")
            print("   ⚠️  Möglicherweise SSH-Key nicht zu GitHub hinzugefügt")
        
        print("\n📊 Test-Zusammenfassung:")
        print(f"✅ SSH-Agent Setup: {'OK' if ssh_success else 'FEHLER'}")
        print(f"✅ Git-Status: {'OK' if status_success else 'FEHLER'}")
        print(f"✅ Git-Remotes: {'OK' if remote_success else 'FEHLER'}")
        print(f"✅ SSH zu GitHub: {'OK' if 'successfully authenticated' in ssh_test_output else 'FEHLER'}")
        
        return ssh_success and status_success
        
    except Exception as e:
        print(f"❌ Fehler beim Test: {e}")
        return False

def demo_commit_and_push():
    """Demo für Commit und Push (nur simulation)"""
    print("\n" + "=" * 50)
    print("🎯 Demo: Automatischer Commit & Push")
    print("=" * 50)
    
    choice = input("Soll eine Demo-Änderung committed und gepusht werden? (j/n): ")
    if choice.lower() not in ['j', 'ja', 'y', 'yes']:
        print("Demo übersprungen")
        return
    
    try:
        automation = SecureGitAutomation()
        
        # Demo-Datei erstellen
        demo_file = automation.repo_path / "automation_test.txt"
        demo_content = "Git-Automatisierung Test\nZeitpunkt: " + str(Path(__file__).stat().st_mtime)
        
        with open(demo_file, 'w') as f:
            f.write(demo_content)
        
        print(f"📝 Demo-Datei erstellt: {demo_file}")
        
        # Git Add
        add_success, add_output = automation.run_command(f"git add {demo_file}")
        if add_success:
            print("✅ Git Add erfolgreich")
        else:
            print(f"❌ Git Add fehlgeschlagen: {add_output}")
            return
        
        # Git Commit
        commit_msg = "Test: Git-Automatisierung Demo"
        commit_success, commit_output = automation.run_command(f'git commit -m "{commit_msg}"')
        
        if commit_success:
            print(f"✅ Git Commit erfolgreich: {commit_msg}")
        else:
            print(f"❌ Git Commit fehlgeschlagen: {commit_output}")
            return
        
        # Git Push (mit SSH-Agent)
        push_choice = input("🚀 Git Push ausführen? (j/n): ")
        if push_choice.lower() in ['j', 'ja', 'y', 'yes']:
            push_success, push_output = automation.run_command("git push")
            
            if push_success:
                print("✅ Git Push erfolgreich!")
                print("🎉 Vollständige Git-Automatisierung funktioniert!")
            else:
                print(f"❌ Git Push fehlgeschlagen: {push_output}")
        else:
            print("Git Push übersprungen")
            
        # Cleanup
        demo_file.unlink(missing_ok=True)
        automation.run_command(f"git reset --soft HEAD~1")  # Commit rückgängig
        print("🧹 Demo-Änderungen bereinigt")
        
    except Exception as e:
        print(f"❌ Demo Fehler: {e}")

def main():
    """Haupttest-Funktion"""
    print("🔐 Git-Automatisierung Volltest")
    print("=" * 50)
    
    # Test 1: Vollständige Automatisierung
    automation_ok = test_full_automation()
    
    if automation_ok:
        # Test 2: Demo Commit & Push
        demo_commit_and_push()
    else:
        print("\n❌ Grundlegende Tests fehlgeschlagen")
        print("Führe zuerst 'python3 setup_ssh_credentials.py' aus")

if __name__ == "__main__":
    main()