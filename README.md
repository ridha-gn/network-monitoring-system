# 🌐 Cloud-Based Network Monitoring System

## 🎯 Overview
A real-time network monitoring system built with Python, Prometheus, Grafana, and Docker. Monitors network latency, port status, HTTP response times, and system metrics.

## 🛠️ Tech Stack
- **Monitoring:** Prometheus + Custom Python Scripts
- **Visualization:** Grafana
- **Containerization:** Docker
- **Metrics:** Network latency, Port status, HTTP performance, System metrics

## 🚀 Features
- Real-time latency monitoring (Google DNS, CloudFlare, GitHub)
- Port status checking for critical services (HTTP, HTTPS, SSH)
- HTTP response time measurements
- System performance monitoring (CPU, memory, load)
- Beautiful Grafana dashboards with auto-refresh
- Containerized deployment with Docker


## 🏗️ Architecture
Network Devices → Python Monitor → Prometheus → Grafana → Real-time Dashboard
📊 Metrics Collected
Network Latency: 8.8.8.8, 1.1.1.1, github.com

Port Status: google.com:80, google.com:443, github.com:80, localhost:22

HTTP Response Times: google.com, github.com, httpbin.org

System Metrics: CPU, memory, disk, load average

🎯 Skills Demonstrated
Docker containerization

Prometheus metrics collection

Grafana dashboard creation

Python automation

Network monitoring

DevOps practices
