code = """/usr/bin/trufflehog est la bonne version !
Maintenant on fixe le script permanent."""

# Sauvegarder la bonne commande
import subprocess, json, datetime, os

def scan_repo(repo_url):
    try:
        output = subprocess.check_output(
            f"/usr/bin/trufflehog github --repo {repo_url} --json",
            shell=True, stderr=subprocess.STDOUT
        ).decode('utf-8')
    except subprocess.CalledProcessError as e:
        output = e.output.decode('utf-8')
    
    findings = []
    for line in output.splitlines():
        line = line.strip()
        if not line.startswith('{'):
            continue
        try:
            data = json.loads(line)
            if 'SourceMetadata' in data:
                findings.append(data)
        except:
            pass
    return findings

open("scanner/trufflehog_scanner.py", "w").write(
    open("/dev/stdin").read()
)
