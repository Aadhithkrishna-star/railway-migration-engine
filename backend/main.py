import os
import json
import shutil
import subprocess
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Railway Migration Engine Core")

# Enable CORS so your frontend can communicate with the backend privately or publicly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MigrationRequest(BaseModel):
    github_url: str

def analyze_repo(repo_path: str) -> dict:
    analysis = {
        "framework": "unknown",
        "has_docker": False,
        "database_required": None,
        "start_command": None
    }
    
    if os.path.exists(os.path.join(repo_path, "Dockerfile")):
        analysis["has_docker"] = True

    pkg_json_path = os.path.exists(os.path.join(repo_path, "package.json"))
    if pkg_json_path:
        with open(os.path.join(repo_path, "package.json"), "r") as f:
            try:
                data = json.load(f)
                deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                if "next" in deps:
                    analysis["framework"] = "nextjs"
                    analysis["start_command"] = "npm run start"
                elif "express" in deps:
                    analysis["framework"] = "express"
                    analysis["start_command"] = "node index.js"
                else:
                    analysis["framework"] = "nodejs"
            except:
                pass

    if os.path.exists(os.path.join(repo_path, "requirements.txt")):
        analysis["framework"] = "python"
        with open(os.path.join(repo_path, "requirements.txt"), "r") as f:
            content = f.read().lower()
            if "django" in content:
                analysis["framework"] = "django"
            elif "fastapi" in content:
                analysis["framework"] = "fastapi"

    all_files_str = ""
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file in ["package.json", "requirements.txt", "Gemfile", "go.mod"]:
                try:
                    with open(os.path.join(root, file), "r", errors="ignore") as f:
                        all_files_str += f.read().lower()
                except:
                    pass

    if "postgres" in all_files_str or "pg" in all_files_str:
        analysis["database_required"] = "postgresql"
    elif "redis" in all_files_str:
        analysis["database_required"] = "redis"
    elif "mongo" in all_files_str:
        analysis["database_required"] = "mongodb"

    return analysis

def generate_railway_blueprint(analysis: dict, github_url: str) -> dict:
    services = {}
    
    app_service = {
        "source": {
            "repo": github_url
        },
        "variables": {
            "PORT": "3000"
        }
    }
    
    if not analysis["has_docker"]:
        app_service["build"] = {
            "builder": "NIXPACKS"
        }
    
    if analysis["database_required"] == "postgresql":
        services["postgres-db"] = {
            "image": "postgres:15",
            "variables": {
                "POSTGRES_DB": "railway_migration",
                "POSTGRES_PASSWORD": "rootpassword"
            }
        }
        app_service["variables"]["DATABASE_URL"] = "${{ postgres-db.POSTGRES_URL }}"

    services["target-application"] = app_service

    return {
        "version": 2,
        "services": services
    }

@app.post("/api/analyze")
async def target_migration_endpoint(request: MigrationRequest):
    temp_dir = f"/tmp/repo_{os.urandom(4).hex()}"
    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", request.github_url, temp_dir],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        
        analysis_results = analyze_repo(temp_dir)
        railway_template = generate_railway_blueprint(analysis_results, request.github_url)
        
        return {
            "success": True,
            "detected_stack": analysis_results,
            "railway_blueprint": railway_template
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
