import random
import time
from datetime import datetime, timedelta

# Configuration du fichier généré
OUTPUT_FILE = "data/access.log"
NUM_LINES = 10000

IP_POOL = [
    "192.168.1.12", "10.0.0.45", "172.16.0.88", "192.168.1.15", 
    "203.0.113.195", "198.51.100.14", "81.56.23.11", "92.104.12.89"
]

USERS = ["-", "-", "-", "admin", "jdoe", "mdupont"]

ENDPOINTS = [
    ("/index.html", "GET", 200, 4500),
    ("/api/v1/products", "GET", 200, 3200),
    ("/api/v1/products", "POST", 201, 850),
    ("/login", "POST", 200, 1200),
    ("/cart/checkout", "POST", 500, 450),
    ("/images/logo.png", "GET", 304, 0),
    ("/missing-page", "GET", 404, 230),
    ("/admin/settings", "GET", 403, 310),
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X)",
    "curl/7.88.1"
]

REFERRERS = [
    "https://www.google.com",
    "https://example.com/index.html",
    "https://example.com/login",
    "-"
]

now = datetime.now()
start_date = now - timedelta(days=7)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for _ in range(NUM_LINES):
        # Date aléatoire répartie sur la semaine écoulée
        random_seconds = random.randint(0, 7 * 86400)
        log_time = start_date + timedelta(seconds=random_seconds)
        time_str = log_time.strftime("%d/%b/%Y:%H:%M:%S +0200")
        
        ip = random.choice(IP_POOL)
        user = random.choice(USERS)
        path, method, status, bytes_size = random.choice(ENDPOINTS)
        
        # Ajustement réaliste du volume de bytes et variation statut HTTP
        if status == 200:
            bytes_size += random.randint(-200, 500)
        if random.random() < 0.05: # 5% de pannes aléatoires
            status = 500
            bytes_size = 512

        agent = random.choice(USER_AGENTS)
        referrer = random.choice(REFERRERS)
        
        # Format Apache Combined
        log_entry = f'{ip} - {user} [{time_str}] "{method} {path} HTTP/1.1" {status} {bytes_size} "{referrer}" "{agent}"\n'
        f.write(log_entry)

print(f"Fichier '{OUTPUT_FILE}' généré avec succès ({NUM_LINES} lignes).")