"""Verify the live Docker Compose API and frontend over published ports."""
import json
import urllib.request


def get(url):
    with urllib.request.urlopen(url, timeout=10) as response:
        return response.status, response.read().decode()


status, body = get("http://127.0.0.1:18080/api/health")
assert status == 200 and json.loads(body)["status"] == "ok"
status, body = get("http://127.0.0.1:13000/")
assert status == 200 and "Update CLI Test" in body
print("COMPOSE SMOKE OK")
