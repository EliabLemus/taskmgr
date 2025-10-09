#!/usr/bin/env python3
import asyncio, httpx, random, time, argparse

async def worker(queue, client, token, slow_percent, error_rate):
    headers = {"Authorization": f"Token {token}"} if token else {}
    while True:
        try:
            queue.get_nowait()
        except asyncio.QueueEmpty:
            return
        # Decide endpoint y retraso
        url = "/api/v1/tasks/" if random.random() > error_rate else "/api/v1/tasks/999999/"
        if random.random() < slow_percent:
            await asyncio.sleep(2)
        try:
            await client.get(url, headers=headers, timeout=10)
        finally:
            queue.task_done()

async def simulate(rps, duration, token, slow_percent, error_rate, base_url):
    total = rps * duration
    q = asyncio.Queue()
    for _ in range(total):
        q.put_nowait(None)
    async with httpx.AsyncClient(base_url=base_url) as client:
        tasks = [asyncio.create_task(worker(q, client, token, slow_percent, error_rate))
                 for _ in range(min(100, rps*2))]
        started = time.perf_counter()
        await q.join()
        elapsed = time.perf_counter() - started
        print(f"Dispatched {total} requests in {elapsed:.2f}s")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--rps", type=int, default=10, help="Solicitudes por segundo")
    p.add_argument("--duration", type=int, default=60, help="Duración (s)")
    p.add_argument("--error-rate", type=float, default=0.0, help="Proporción de errores 0-1")
    p.add_argument("--slow-percent", type=float, default=0.0, help="Proporción lentas 0-1")
    p.add_argument("--token", help="Token de autenticación")
    p.add_argument("--base-url", default="http://localhost:8000", help="URL base del API")
    args = p.parse_args()
    asyncio.run(simulate(args.rps, args.duration, args.token,
                         args.slow_percent, args.error_rate, args.base_url))
if __name__ == "__main__":
    main()
