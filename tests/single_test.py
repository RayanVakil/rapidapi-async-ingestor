"""Single isolated request after a 10s cooldown to check rate limit status."""
import time
import httpx

print("Waiting 10s for rate limit cooldown...")
time.sleep(10)

key = "76c836e9a4msh7ca748f4cd550f4p1c2cc8jsn75ba17b88de0"
headers = {
    "x-rapidapi-key": key,
    "x-rapidapi-host": "car-api2.p.rapidapi.com"
}

r = httpx.get(
    "https://car-api2.p.rapidapi.com/api/years",
    params={"make": "Subaru", "model": "Outback"},
    headers=headers
)

print(f"Status: {r.status_code}")
print(f"Rate Limit Remaining: {r.headers.get('x-ratelimit-requests-remaining', 'N/A')}")
print(f"Rate Limit Limit: {r.headers.get('x-ratelimit-requests-limit', 'N/A')}")
print(f"Body: {r.text[:500]}")
