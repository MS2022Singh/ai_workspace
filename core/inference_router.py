# core/inference_router.py
import urllib.request
import json
import logging
from core.event_bus import bus

class InferenceRouter:
    def __init__(self):
        self.providers = {
            "ollama": "http://localhost:11434/api/generate",
            "vllm": "http://localhost:8000/v1/completions",
            "sglang": "http://localhost:30000/v1/completions",
            "litellm": "http://localhost:4000/v1/completions"
        }
        self.active_provider = "ollama"

    def set_provider(self, provider_name):
        if provider_name in self.providers:
            self.active_provider = provider_name
            bus.publish("PROVIDER_CHANGED", {"provider": provider_name})
            return True
        return False

    def route_request(self, prompt, model="qwen2.5:latest"):
        endpoint = self.providers.get(self.active_provider)
        payload = json.dumps({"model": model, "prompt": prompt, "stream": False}).encode("utf-8")
        
        bus.publish("INFERENCE_STARTED", {"provider": self.active_provider, "model": model})
        
        try:
            req = urllib.request.Request(endpoint, data=payload, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=5) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                bus.publish("INFERENCE_COMPLETED", {"status": "SUCCESS"})
                return res_data
        except Exception as e:
            bus.publish("INFERENCE_FAILED", {"error": str(e)})
            logging.warning(f"Inference provider {self.active_provider} unavailable: {e}")
            return {"error": f"Provider {self.active_provider} offline or unreachable", "details": str(e)}

router = InferenceRouter()
