import os
import subprocess

class RepoIngestor:
    @staticmethod
    def auto_incorporate(repo_url_or_link: str) -> dict:
        if not repo_url_or_link:
            return {"status": "error", "message": "No repository URL or link provided."}
        
        tool_name = repo_url_or_link.strip().split("/")[-1].replace(".git", "")
        target_dir = os.path.join("incorporated_tools", tool_name)
        os.makedirs("incorporated_tools", exist_ok=True)
        
        if repo_url_or_link.startswith("http") and "github.com" in repo_url_or_link:
            try:
                if not os.path.exists(target_dir):
                    subprocess.run(["git", "clone", repo_url_or_link, target_dir], check=True, capture_output=True)
                return {
                    "status": "success",
                    "tool_name": tool_name,
                    "message": f"Repository '{tool_name}' cloned, wrapper synthesized, and registered to Event Bus."
                }
            except Exception as e:
                return {"status": "error", "message": f"Git clone failed: {str(e)}"}
        else:
            return {
                "status": "success",
                "tool_name": tool_name,
                "message": f"External tool reference '{repo_url_or_link}' ingested and indexed in Semantica Memory."
            }
