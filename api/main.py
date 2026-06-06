from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import subprocess, json, datetime, os

app = FastAPI(title="SecureCloud Guardian")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

def run_trufflehog(repo_url):
    try:
        output = subprocess.check_output(
            f"/usr/bin/trufflehog github --repo {repo_url} --json",
            shell=True, stderr=subprocess.STDOUT
        ).decode("utf-8")
    except subprocess.CalledProcessError as e:
        output = e.output.decode("utf-8")
    findings = []
    for line in output.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            data = json.loads(line)
            if "SourceMetadata" in data:
                findings.append(data)
        except:
            pass
    return findings

@app.get("/")
def home():
    return {"status": "ok", "project": "SecureCloud Guardian"}

@app.get("/scan")
def scan(repo: str):
    findings = run_trufflehog(repo)
    verified = [f for f in findings if f.get("Verified")]
    os.makedirs("reports", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = f"reports/scan_{timestamp}.json"
    with open(report_path, "w") as f:
        json.dump(findings, f, indent=2)
    return {"repo": repo, "total": len(findings), "verified": len(verified), "findings": findings}

@app.get("/reports")
def list_reports():
    files = sorted(os.listdir("reports"), reverse=True) if os.path.exists("reports") else []
    return {"reports": files}
