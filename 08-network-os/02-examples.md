# Phase 08: Network & OS - Ví Dụ Thực Tế

---

## 📁 BÀI 1: HTTP TROUBLESHOOTING

### Ví dụ 1.1: curl commands cho API debugging

```bash
# 1. GET request với headers
curl -X GET "https://api.example.com/users/1" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN"

# 2. POST request với JSON body
curl -X POST "https://api.example.com/users" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "secret123"
  }'

# 3. PUT request (update toàn bộ)
curl -X PUT "https://api.example.com/users/1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "email": "jane@example.com"
  }'

# 4. PATCH request (partial update)
curl -X PATCH "https://api.example.com/users/1" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newemail@example.com"
  }'

# 5. DELETE request
curl -X DELETE "https://api.example.com/users/1"

# 6. Verbose mode (xem request/response headers)
curl -v "https://api.example.com/users/1"

# 7. Save response to file
curl -o response.json "https://api.example.com/users/1"

# 8. Download with progress
curl -O https://example.com/large-file.zip

# 9. Follow redirects
curl -L "http://example.com"  # Redirects to HTTPS

# 10. Rate limit testing
for i in {1..100}; do
  curl -s -o /dev/null -w "%{http_code}\n" "https://api.example.com/users"
done
```

---

### Ví dụ 1.2: Debug HTTP issues

```bash
# Problem 1: SSL Certificate Error
curl: (60) SSL certificate problem: unable to get local issuer certificate

# Solution: Skip verification (development only!)
curl -k "https://api.example.com"

# Or use correct CA bundle
curl --cacert /path/to/ca-bundle.crt "https://api.example.com"


# Problem 2: Connection Timeout
curl: (28) Failed to connect to api.example.com port 443: Connection timed out

# Debug steps:
# 1. Check if server is reachable
ping api.example.com

# 2. Check if port is open
telnet api.example.com 443
nc -zv api.example.com 443

# 3. Check DNS resolution
nslookup api.example.com
dig api.example.com

# 4. Trace route
traceroute api.example.com


# Problem 3: 401 Unauthorized
# Check token
curl -v "https://api.example.com/users" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Look for:
# - Token expired?
# - Wrong token format?
# - Token scope insufficient?


# Problem 4: 403 Forbidden
# Authenticated but no permission
curl -v "https://api.example.com/admin/users" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Check:
# - User role has admin permission?
# - Resource access control?


# Problem 5: 500 Internal Server Error
# Server-side bug
curl -v "https://api.example.com/users" \
  -H "Content-Type: application/json" \
  -d '{"invalid": "data"}'

# Contact backend team with:
# - Request payload
# - Timestamp
# - Request ID (from X-Request-ID header)
```

---

## 📁 BÀI 2: NETWORK TROUBLESHOOTING

### Ví dụ 2.1: Network diagnostic commands

```bash
# 1. Check local network configuration
ip addr show
ifconfig eth0

# 2. Check default gateway
ip route show
netstat -rn

# 3. Check DNS configuration
cat /etc/resolv.conf

# 4. Test connectivity
ping -c 4 8.8.8.8          # Google DNS
ping -c 4 google.com       # DNS resolution test

# 5. Trace network path
traceroute google.com
mtr google.com             # Interactive traceroute

# 6. Check listening ports
netstat -tulpn
ss -tulpn                  # Modern alternative

# Example output:
# Proto Recv-Q Send-Q Local Address   Foreign Address  State   PID/Program
# tcp   0      0      0.0.0.0:8080    0.0.0.0:*        LISTEN  1234/java
# tcp   0      0      0.0.0.0:22      0.0.0.0:*        LISTEN  567/sshd

# 7. Check specific port
nc -zv localhost 8080      # Check if port is open
telnet localhost 8080      # Interactive connection

# 8. Monitor network traffic
tcpdump -i eth0 port 8080  # Capture packets on port 8080
tcpdump -i eth0 -n port 80 or port 443  # HTTP/HTTPS traffic

# 9. Bandwidth monitoring
iftop                        # Real-time bandwidth per connection
nethogs                      # Bandwidth per process

# 10. Network statistics
netstat -s                   # TCP/UDP statistics
cat /proc/net/dev           # Interface statistics
```

---

### Ví dụ 2.2: Debug Spring Boot connectivity issues

```bash
# Scenario 1: Application cannot connect to database

# Check if database is reachable
ping db-server.example.com

# Check if database port is open
nc -zv db-server.example.com 5432

# Check from inside container (if using Docker)
docker exec -it myapp bash
nc -zv postgres 5432

# Check connection string
curl -s "http://localhost:8080/actuator/env" | jq '.propertySources[].properties."spring.datasource.url"'

# Test database connection directly
psql -h db-server -U postgres -d mydb


# Scenario 2: Microservices cannot communicate

# Service A cannot reach Service B
# From Service A container:
curl -v http://service-b:8080/actuator/health

# Check service discovery
curl http://service-registry:8761/apps

# Check DNS resolution inside Kubernetes
kubectl run -it --rm debug --image=busybox --restart=Never -- nslookup service-b

# Check network policies (Kubernetes)
kubectl get networkpolicy
kubectl describe networkpolicy default


# Scenario 3: External API timeout

# Check API response time
curl -w "@curl-format.txt" -o /dev/null -s "https://api.external.com/endpoint"

# curl-format.txt:
#     time_namelookup:  %{time_namelookup}\n
#        time_connect:  %{time_connect}\n
#     time_appconnect:  %{time_appconnect}\n
#    time_pretransfer:  %{time_pretransfer}\n
#      time_redirect:  %{time_redirect}\n
# time_starttransfer:  %{time_starttransfer}\n
#                    ----------\n
#         time_total:  %{time_total}\n

# Output:
#     time_namelookup:  0.002s
#        time_connect:  0.045s
#     time_appconnect:  0.089s
#    time_pretransfer:  0.091s
#      time_redirect:  0.000s
# time_starttransfer:  0.156s
#                    ----------
#         time_total:  0.158s

# If time_total is high:
# - Check network latency
# - Check API server performance
# - Check firewall rules
```

---

## 📁 BÀI 3: LINUX PERFORMANCE TROUBLESHOOTING

### Ví dụ 3.1: Debug slow application

```bash
# Step 1: Check overall system health
uptime
# Output: 14:30:25 up 10 days,  3:45,  2 users,  load average: 0.52, 0.48, 0.44
# Load average > CPU cores = system overloaded

# Step 2: Check CPU usage
top
htop

# Look for:
# - High CPU processes
# - Load average
# - CPU idle percentage

# Step 3: Check memory usage
free -h
# Output:
#               total        used        free      shared  buff/cache   available
# Mem:           15Gi       8.2Gi       4.1Gi       256Mi       3.7Gi       6.5Gi

# If "available" is low:
# - Check for memory leaks
# - Check application heap size

# Step 4: Check disk I/O
iostat -x 1 5
# Look for:
# - %util > 80% = disk bottleneck
# - await = average I/O wait time

# Step 5: Check disk space
df -h
# If root partition is full:
# - Clean up logs: journalctl --vacuum-time=1d
# - Remove old kernels: apt autoremove

# Step 6: Check for zombie processes
ps aux | awk '$8 ~ /Z/'

# Step 7: Check open file descriptors
lsof -p $(pgrep java) | wc -l
# If close to ulimit:
ulimit -n  # Check limit

# Step 8: Check network connections
netstat -an | grep ESTABLISHED | wc -l
# High number of connections = possible connection leak
```

---

### Ví dụ 3.2: Analyze Java application

```bash
# Find Java process
ps aux | grep java
# Output: user  1234  5.2  8.5  2543216 176544 ?  Sl   10:30   2:34 java -jar app.jar

# Check JVM memory
jstat -gc 1234 1000 5
# Output every 1000ms, 5 times

# Check thread dump
jstack 1234 > thread-dump.txt
# Analyze for:
# - Deadlocks
# - Blocked threads
# - Long-running operations

# Check heap dump
jmap -dump:format=b,file=heap.hprof 1234
# Analyze with Eclipse MAT or VisualVM

# Monitor in real-time
jconsole 1234
jvisualvm

# Check GC logs (if enabled)
tail -f gc.log

# Check application logs
tail -f /var/log/app/application.log
grep -i "error" /var/log/app/application.log
grep -i "exception" /var/log/app/application.log

# Check slow requests (if using Spring Boot Actuator)
curl http://localhost:8080/actuator/metrics/http.server.requests
```

---

## 📁 BÀI 4: SHELL SCRIPTS FOR DEVOPS

### Ví dụ 4.1: Deployment automation

```bash
#!/bin/bash
# deploy.sh - Production deployment script

set -e  # Exit on error

# Configuration
APP_NAME="myapp"
APP_USER="appuser"
APP_HOME="/opt/$APP_NAME"
LOG_DIR="$APP_HOME/logs"
BACKUP_DIR="/backups/$APP_NAME"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Pre-deployment checks
log_info "Running pre-deployment checks..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    log_error "Please run as root"
    exit 1
fi

# Check if JAR file exists
if [ ! -f "target/$APP_NAME.jar" ]; then
    log_error "JAR file not found: target/$APP_NAME.jar"
    exit 1
fi

# Backup current version
log_info "Creating backup..."
mkdir -p "$BACKUP_DIR"
if [ -d "$APP_HOME" ]; then
    cp -r "$APP_HOME" "$BACKUP_DIR/$APP_NAME.$TIMESTAMP"
    log_info "Backup created: $BACKUP_DIR/$APP_NAME.$TIMESTAMP"
fi

# Stop application
log_info "Stopping application..."
systemctl stop "$APP_NAME"

# Deploy new version
log_info "Deploying new version..."
mkdir -p "$APP_HOME"
cp "target/$APP_NAME.jar" "$APP_HOME/"
cp "application-prod.yml" "$APP_HOME/"

# Set permissions
chown -R "$APP_USER:$APP_USER" "$APP_HOME"
chmod 755 "$APP_HOME"

# Start application
log_info "Starting application..."
systemctl start "$APP_NAME"

# Health check
log_info "Waiting for application to start..."
sleep 10

# Check if application is healthy
HEALTH_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/actuator/health)

if [ "$HEALTH_STATUS" = "200" ]; then
    log_info "Deployment successful! Application is healthy."
    exit 0
else
    log_error "Deployment failed! Health check returned: $HEALTH_STATUS"
    log_warn "Rolling back to previous version..."
    systemctl stop "$APP_NAME"
    rm -rf "$APP_HOME"
    cp -r "$BACKUP_DIR/$APP_NAME.$TIMESTAMP" "$APP_HOME"
    systemctl start "$APP_NAME"
    exit 1
fi
```

---

### Ví dụ 4.2: Monitoring script

```bash
#!/bin/bash
# monitor.sh - System monitoring script

LOG_FILE="/var/log/system-monitor.log"
ALERT_EMAIL="admin@example.com"

# Thresholds
CPU_THRESHOLD=80
MEMORY_THRESHOLD=80
DISK_THRESHOLD=90

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

check_cpu() {
    CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    CPU_INT=${CPU_USAGE%.*}

    if [ "$CPU_INT" -gt "$CPU_THRESHOLD" ]; then
        log "ALERT: CPU usage is ${CPU_USAGE}%"
        # Send alert (implement email/slack notification)
    else
        log "CPU usage: ${CPU_USAGE}%"
    fi
}

check_memory() {
    MEM_USAGE=$(free | grep Mem | awk '{printf("%.0f", $3/$2 * 100.0)}')

    if [ "$MEM_USAGE" -gt "$MEMORY_THRESHOLD" ]; then
        log "ALERT: Memory usage is ${MEM_USAGE}%"
    else
        log "Memory usage: ${MEM_USAGE}%"
    fi
}

check_disk() {
    DISK_USAGE=$(df -h / | tail -1 | awk '{print $5}' | cut -d'%' -f1)

    if [ "$DISK_USAGE" -gt "$DISK_THRESHOLD" ]; then
        log "ALERT: Disk usage is ${DISK_USAGE}%"
    else
        log "Disk usage: ${DISK_USAGE}%"
    fi
}

check_service() {
    SERVICE=$1
    if systemctl is-active --quiet "$SERVICE"; then
        log "Service $SERVICE: RUNNING"
    else
        log "ALERT: Service $SERVICE is NOT running"
    fi
}

# Main
log "=== System Health Check ==="
check_cpu
check_memory
check_disk
check_service "myapp"
check_service "nginx"
check_service "postgresql"
log "=== Health Check Complete ==="
```

---

## 📝 BÀI TẬP THỰC HÀNH

Xem `03-exercises.md` để làm bài tập!
