import subprocess
import requests
import time
import psycopg2
from psycopg2 import OperationalError
from datetime import datetime

# Sites a serem monitorados
targets = ["https://www.google.com", "https://www.youtube.com", "https://www.rnp.br"]

# Função para ping
def ping_host(host):
    result = subprocess.run(["ping", "-c", "4", host], capture_output=True, text=True)
    if result.returncode != 0:
        return None, None
    loss = None
    avg = None
    for line in result.stdout.split("\n"):
        if "packet loss" in line:
            loss = line.strip().split(",")[2].split()[0].replace("%", "")
        if "rtt min/avg/max" in line or "min/avg/max/mdev" in line:
            avg = line.strip().split("=")[1].split("/")[1]
    return avg, loss

# Função para HTTP
def check_http(url):
    try:
        start = time.time()
        response = requests.get(url, timeout=5)
        elapsed = time.time() - start
        return response.status_code, round(elapsed * 1000, 2)
    except Exception:
        return None, None

# Armazenar dados no banco
def store_data(conn, host, rtt, loss, http_code, http_time):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO metrics (timestamp, host, rtt_ms, loss_pct, http_status, http_time_ms)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (datetime.utcnow(), host, rtt, loss, http_code, http_time))
        conn.commit()

# Conectar ao banco com tentativas
def connect_with_retry():
    for attempt in range(10):
        try:
            return psycopg2.connect(
                host="db",
                database="monitoramento",
                user="user",
                password="pass"
            )
        except OperationalError:
            print(f"[{datetime.utcnow()}] Tentativa {attempt + 1}/10: banco ainda não está pronto.")
            time.sleep(5)
    raise Exception("Não foi possível conectar ao banco após várias tentativas.")

# Função principal
def main():
    conn = connect_with_retry()

    while True:
        for url in targets:
            host = url.replace("https://", "")
            rtt, loss = ping_host(host)
            code, http_time = check_http(url)
            print(f"[{datetime.utcnow()}] {host} → RTT={rtt}ms | Loss={loss}% | HTTP={code} | Time={http_time}ms")
            store_data(conn, host, rtt, loss, code, http_time)
        time.sleep(60)

if __name__ == "__main__":
    main()
