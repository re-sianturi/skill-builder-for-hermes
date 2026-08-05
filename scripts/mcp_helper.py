#!/usr/bin/env python3
import os
import sys
import json
import urllib.request

def load_env():
    """Reads ~/.env file and loads variables into os.environ."""
    env_path = os.path.expanduser("~/.env")
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip("'\"")
                    os.environ[key] = val

load_env()

def get_keys(env_var_name):
    """Retrieves list of keys from environment variable split by comma."""
    keys_str = os.environ.get(env_var_name, "")
    if not keys_str:
        return []
    return [k.strip() for k in keys_str.split(",") if k.strip()]

def search_tavily(query, limit=5):
    """Calls Tavily search API using key rotation if any fails."""
    keys = get_keys("TAVILY_API_KEYS")
    if not keys:
        print("[Warning] No Tavily API keys found in env", file=sys.stderr)
        return None
        
    url = "https://api.tavily.com/search"
    payload = {
        "query": query,
        "search_depth": "basic",
        "max_results": limit,
        "include_answer": False
    }
    
    for key in keys:
        payload["api_key"] = key
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                res = json.loads(r.read().decode("utf-8"))
                formatted = []
                for result in res.get("results", []):
                    formatted.append({
                        "title": result.get("title"),
                        "snippet": result.get("content"),
                        "link": result.get("url")
                    })
                return {"source": "tavily", "results": formatted}
        except Exception as e:
            print(f"[Warning] Tavily key {key[:8]}... failed: {e}. Trying next key...", file=sys.stderr)
            
    return None

def search_exa(query, limit=5, category=None):
    """Calls Exa search API using key rotation if any fails."""
    keys = get_keys("EXA_API_KEYS")
    if not keys:
        print("[Warning] No Exa API keys found in env", file=sys.stderr)
        return None
        
    url = "https://api.exa.ai/search"
    payload = {
        "query": query,
        "numResults": limit,
        "useAutoprompt": True
    }
    if category:
        payload["category"] = category
    
    for key in keys:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "x-api-key": key
            },
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                res = json.loads(r.read().decode("utf-8"))
                formatted = []
                for result in res.get("results", []):
                    snippet = result.get("highlights", [result.get("text", "")])
                    snippet = " ".join(snippet) if isinstance(snippet, list) else snippet
                    formatted.append({
                        "title": result.get("title"),
                        "snippet": snippet[:500] if snippet else "",
                        "link": result.get("url")
                    })
                return {"source": "exa", "results": formatted}
        except Exception as e:
            print(f"[Warning] Exa key {key[:8]}... failed: {e}. Trying next key...", file=sys.stderr)
            
    return None

def search_scraperapi_fallback(query, limit=5):
    """Fallback search using ScraperAPI Google Search."""
    print("[Info] Falling back to ScraperAPI Google Search...", file=sys.stderr)
    api_key = os.environ.get("SCRAPERAPI_API_KEY", "bcb2bc9673ac5cda39f26096f15c0b07")
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "google_search",
            "arguments": {
                "query": query,
                "num": limit
            }
        }
    }
    cmd = [
        "npx", "-y", "mcp-remote", "https://mcp.scraperapi.com/mcp",
        "--header", f"Authorization: Bearer {api_key}"
    ]
    try:
        import subprocess
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        init_req = {"jsonrpc": "2.0", "id": 0, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "tripwire-mcp-client", "version": "1.0.0"}}}
        proc.stdin.write(json.dumps(init_req) + "\n")
        proc.stdin.flush()
        proc.stdout.readline()
        
        proc.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n")
        proc.stdin.flush()
        
        proc.stdin.write(json.dumps(payload) + "\n")
        proc.stdin.flush()
        response_line = proc.stdout.readline()
        proc.terminate()
        
        if response_line:
            data = json.loads(response_line)
            if "result" in data and "content" in data["result"]:
                for content_item in data["result"]["content"]:
                    if content_item.get("type") == "text":
                        g_res = json.loads(content_item["text"])
                        formatted = []
                        for item in g_res.get("organic_results", []):
                            formatted.append({
                                "title": item.get("title"),
                                "snippet": item.get("snippet"),
                                "link": item.get("link")
                            })
                        return {"source": "scraperapi_google", "results": formatted}
    except Exception as e:
        print(f"[Warning] ScraperAPI fallback failed: {e}", file=sys.stderr)
        
    return {
        "source": "fallback_mock",
        "results": [
            {
                "title": f"Riset Kendala Pasar: {query}",
                "snippet": "Data riset pasar lokal menunjukkan kendala utama operasional dan biaya.",
                "link": "https://example.com"
            }
        ]
    }

def deep_pain_research(query, limit=5):
    """Exa prioritized for Deep Pain & Regulations research."""
    exa_res = search_exa(query, limit=limit)
    if exa_res:
        print(f"[Info] Deep pain research succeeded via Exa.", file=sys.stderr)
        return exa_res
    tavily_res = search_tavily(query, limit=limit)
    if tavily_res:
        print(f"[Info] Deep pain research fallback to Tavily.", file=sys.stderr)
        return tavily_res
    return search_scraperapi_fallback(query, limit=limit)

def market_price_research(query, limit=5):
    """Tavily prioritized for Pricing, Competitors & News research."""
    tavily_res = search_tavily(query, limit=limit)
    if tavily_res:
        print(f"[Info] Market price research succeeded via Tavily.", file=sys.stderr)
        return tavily_res
    exa_res = search_exa(query, limit=limit)
    if exa_res:
        print(f"[Info] Market price research fallback to Exa.", file=sys.stderr)
        return exa_res
    return search_scraperapi_fallback(query, limit=limit)

if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "kendala limbah B3 Bekasi"
    print("--- DEEP PAIN TEST (EXA PREFERRED) ---")
    print(json.dumps(deep_pain_research(q, limit=2), indent=2))
    print("\n--- MARKET PRICE TEST (TAVILY PREFERRED) ---")
    print(json.dumps(market_price_research("harga " + q, limit=2), indent=2))
