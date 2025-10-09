#!/usr/bin/env python3
import re, sys, json, redis, os

def parse(path):
    metrics = {}
    with open(path) as f:
        text = f.read()
    patterns = {
        "Requests per second": ("ab_requests_per_sec", float),
        "Time per request": ("ab_latency_avg_ms", lambda v: float(v) * 1000),
        "Failed requests": ("ab_failed_requests", int),
    }
    for line in text.splitlines():
        for key, (name, cast) in patterns.items():
            if key in line:
                value = line.split(":")[1].split()[0]
                metrics[name] = cast(value)
    return metrics

def main():
    log = sys.argv[1]
    r = redis.Redis.from_url(os.environ.get("REDIS_URL", "redis://redis:6379/0"))
    metrics = parse(log)
    # Guardar en Redis en un hash
    if metrics:
        r.hmset("ab_metrics", metrics)
    print(json.dumps(metrics, indent=2))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: parse_ab_results.py <archivo_log_ab>")
        sys.exit(1)
    main()
