#!/usr/bin/env python3
import time
import subprocess
import socket
import requests
from prometheus_client import start_http_server, Gauge

# Create metrics - FIXED: No labels for latency, labels for others
LATENCY = Gauge('network_latency_ms', 'Network latency in milliseconds', ['target'])
PORT_STATUS = Gauge('port_status', 'Port status', ['target', 'port'])
HTTP_RESPONSE_TIME = Gauge('http_response_time_ms', 'HTTP response time in ms', ['url'])

def ping_host(host="8.8.8.8"):
    """Measure ping latency"""
    try:
        result = subprocess.run(
            ['ping', '-c', '3', '-W', '5', host],
            capture_output=True, text=True, timeout=10
        )
        if 'avg' in result.stdout:
            for line in result.stdout.split('\n'):
                if 'avg' in line:
                    return float(line.split('=')[1].split('/')[1])
    except Exception as e:
        print(f"❌ Ping error to {host}: {e}")
    return 0

def check_port(host, port):
    """Check if port is open"""
    try:
        start_time = time.time()
        with socket.create_connection((host, port), timeout=5):
            connect_time = (time.time() - start_time) * 1000
            return 1, connect_time
    except socket.error as e:
        return 0, 0

def measure_http_response(url):
    """Measure HTTP response time"""
    try:
        start_time = time.time()
        response = requests.get(url, timeout=10)
        response_time = (time.time() - start_time) * 1000
        return response_time
    except Exception as e:
        print(f"❌ HTTP error for {url}: {e}")
        return 0

def collect_metrics():
    """Collect all network metrics"""
    print("\n" + "="*50)
    print(f"🕐 Collecting metrics at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)
    
    # Ping latency to multiple targets - FIXED: Use labels correctly
    targets = ["8.8.8.8", "1.1.1.1", "github.com"]
    for target in targets:
        latency = ping_host(target)
        LATENCY.labels(target=target).set(latency)  # Now this works with labels
        print(f"📡 Latency to {target}: {latency:.2f}ms")
    
    # Check common ports
    port_checks = [
        ("google.com", 80),
        ("google.com", 443),
        ("github.com", 80),
        ("github.com", 443),
        ("localhost", 22),
    ]
    
    for host, port in port_checks:
        status, connect_time = check_port(host, port)
        PORT_STATUS.labels(target=host, port=str(port)).set(status)
        status_text = "✅ OPEN" if status else "❌ CLOSED"
        time_text = f" ({connect_time:.1f}ms)" if status else ""
        print(f"🔌 Port {port} on {host}: {status_text}{time_text}")
    
    # HTTP response times
    websites = [
        "http://google.com",
        "http://github.com",
        "http://httpbin.org/status/200"
    ]
    
    for url in websites:
        response_time = measure_http_response(url)
        HTTP_RESPONSE_TIME.labels(url=url).set(response_time)
        print(f"🌐 {url}: {response_time:.1f}ms")

if __name__ == '__main__':
    print("🚀 Starting Network Monitor...")
    print("📊 Metrics will be available at: http://localhost:8000/metrics")
    print("⏱️  Collecting metrics every 15 seconds...")
    print("🛑 Press Ctrl+C to stop\n")
    
    start_http_server(8000)
    
    try:
        while True:
            collect_metrics()
            time.sleep(15)
    except KeyboardInterrupt:
        print("\n👋 Stopping network monitor...")
