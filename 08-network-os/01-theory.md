# Phase 08: Network & OS - Lý Thuyết

> **Thời gian:** 2 tuần
> **Mục tiêu:** Hiểu networking và Linux fundamentals cho backend development

---

## 📚 BÀI 1: HTTP/HTTPS FUNDAMENTALS

### 1.1 HTTP Methods

| Method | Idempotent | Safe | Description |
|--------|-----------|------|-------------|
| GET | ✅ | ✅ | Retrieve resource |
| POST | ❌ | ❌ | Create resource |
| PUT | ✅ | ❌ | Update/Replace resource |
| PATCH | ❌ | ❌ | Partial update |
| DELETE | ✅ | ❌ | Delete resource |
| OPTIONS | ✅ | ✅ | Get supported methods |
| HEAD | ✅ | ✅ | Get headers only |

**Idempotent:** Gọi nhiều lần vẫn cùng kết quả
**Safe:** Không thay đổi state server

---

### 1.2 HTTP Status Codes

```
1xx - Informational
  101 Switching Protocols (WebSocket upgrade)

2xx - Success
  200 OK
  201 Created (sau POST)
  204 No Content (sau DELETE)

3xx - Redirection
  301 Moved Permanently
  302 Found (temporary redirect)
  304 Not Modified (cache)

4xx - Client Error
  400 Bad Request
  401 Unauthorized (not authenticated)
  403 Forbidden (authenticated but no permission)
  404 Not Found
  409 Conflict (duplicate resource)
  422 Unprocessable Entity (validation error)
  429 Too Many Requests (rate limit)

5xx - Server Error
  500 Internal Server Error
  502 Bad Gateway
  503 Service Unavailable
  504 Gateway Timeout
```

---

### 1.3 HTTP Headers

**Request Headers:**
```http
GET /api/users/1 HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json
Accept: application/json
User-Agent: Mozilla/5.0
X-Request-ID: 12345678-1234-1234-1234-123456789012
```

**Response Headers:**
```http
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 1234
Cache-Control: max-age=3600
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
```

---

### 1.4 HTTPS & TLS Handshake

```
Client                              Server
  │                                    │
  │──── ClientHello ─────────────────►│
  │     (TLS version, ciphers)         │
  │                                    │
  │◄─── ServerHello ──────────────────│
  │     (Selected TLS, cert)           │
  │                                    │
  │──── Verify Cert ─────────────────►│
  │     (Check CA, expiry)             │
  │                                    │
  │──── Pre-Master Secret ───────────►│
  │     (Encrypted with server pub key)│
  │                                    │
  │◄─── Finished ◄────────────────────│
  │     (Encrypted with session key)   │
  │                                    │
  │◄─── Finished ─────────────────────►│
  │     (Secure connection established)│
```

---

## 📚 BÀI 2: TCP/IP & NETWORKING

### 2.1 OSI Model

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 7: Application                                        │
│           HTTP, FTP, SMTP, DNS                              │
├─────────────────────────────────────────────────────────────┤
│ Layer 6: Presentation                                       │
│           SSL/TLS, Encryption                               │
├─────────────────────────────────────────────────────────────┤
│ Layer 5: Session                                            │
│           RPC, NetBIOS                                      │
├─────────────────────────────────────────────────────────────┤
│ Layer 4: Transport                                          │
│           TCP (reliable), UDP (fast)                        │
├─────────────────────────────────────────────────────────────┤
│ Layer 3: Network                                            │
│           IP, Routers, ICMP                                 │
├─────────────────────────────────────────────────────────────┤
│ Layer 2: Data Link                                          │
│           Ethernet, Switches, MAC addresses                 │
├─────────────────────────────────────────────────────────────┤
│ Layer 1: Physical                                           │
│           Cables, Hubs, Signals                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 2.2 TCP 3-Way Handshake

```
Client                              Server
  │                                    │
  │──── SYN (seq=1000) ──────────────►│
  │     (I want to connect)            │
  │                                    │
  │◄─── SYN-ACK (seq=2000, ack=1001) ─│
  │     (OK, I acknowledge)            │
  │                                    │
  │──── ACK (seq=1001, ack=2001) ────►│
  │     (Connection established)       │
  │                                    │
  │◄════════ Data Transfer ═══════════►│
  │                                    │
  │──── FIN ─────────────────────────►│
  │     (I want to close)              │
  │                                    │
  │◄─── FIN-ACK ──────────────────────│
  │     (Connection closed)            │
```

---

### 2.3 DNS Resolution

```
User types: https://example.com

1. Browser cache check
   └─► Not found

2. OS cache check (DNS resolver service)
   └─► Not found

3. Query DNS Resolver (ISP/Google 8.8.8.8)
   └─► Not found in cache

4. Query Root Server (.)
   └─► Refers to .com TLD server

5. Query TLD Server (.com)
   └─► Refers to example.com authoritative server

6. Query Authoritative Server
   └─► Returns IP: 93.184.216.34

7. Cache result & return to browser

8. Browser connects to 93.184.216.34:443
```

---

### 2.4 Load Balancing Algorithms

```
                    ┌──────────────┐
                    │ Load Balancer│
                    └──────┬───────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
   ┌─────────┐       ┌─────────┐       ┌─────────┐
   │ Server 1│       │ Server 2│       │ Server 3│
   │  CPU 80%│       │  CPU 30%│       │  CPU 50%│
   └─────────┘       └─────────┘       └─────────┘
```

**Algorithms:**

| Algorithm | Description | Use Case |
|-----------|-------------|----------|
| Round Robin | Distribute equally | Homogeneous servers |
| Least Connections | Send to server with fewest active connections | Long-running requests |
| IP Hash | Same client → same server | Session affinity |
| Weighted | Based on server capacity | Heterogeneous servers |
| Least Response Time | Fastest responding server | Performance-critical |

---

## 📚 BÀI 3: LINUX COMMANDS

### 3.1 Process Management

```bash
# Xem processes đang chạy
ps aux
top
htop  # Interactive

# Tìm process
ps aux | grep java
pgrep -f "spring-boot"

# Kill process
kill 1234          # SIGTERM (graceful)
kill -9 1234       # SIGKILL (force)
pkill -f "java"    # Kill by name

# Chạy background
java -jar app.jar &
nohup java -jar app.jar &

# Xem process tree
pstree

# Resource usage
top
htop
vmstat 1 5         # Memory, CPU stats
```

---

### 3.2 File System

```bash
# Navigation
pwd                  # Print working directory
ls -la              # List all files (including hidden)
cd /path/to/dir
cd ..               # Go up one level
cd ~                # Go home

# File operations
touch file.txt       # Create empty file
mkdir mydir          # Create directory
mkdir -p a/b/c       # Create nested directories
cp source dest       # Copy
mv source dest       # Move/Rename
rm file.txt          # Remove
rm -rf directory     # Remove directory (CAREFUL!)

# View file content
cat file.txt         # Display entire file
head -n 10 file.txt  # First 10 lines
tail -n 10 file.txt  # Last 10 lines
tail -f app.log      # Follow log file (real-time)
less file.txt        # View with pagination

# Search
grep "error" app.log           # Search text
grep -r "TODO" src/            # Recursive search
find . -name "*.java"          # Find files
find . -type f -size +100M     # Find large files
```

---

### 3.3 Network Commands

```bash
# Check network interfaces
ifconfig
ip addr show

# Check connectivity
ping google.com
ping -c 4 google.com      # 4 packets only

# Trace route
traceroute google.com
tracepath google.com

# Check ports
netstat -tulpn            # All listening ports
ss -tulpn                 # Modern alternative
netstat -an | grep 8080   # Check specific port

# DNS lookup
nslookup google.com
dig google.com
dig google.com ANY        # All records
dig +short google.com     # Short output

# HTTP requests
curl https://api.example.com/users
curl -X POST -d '{"name":"John"}' https://api.example.com/users
curl -H "Authorization: Bearer token" https://api.example.com/users
curl -v https://api.example.com    # Verbose (see headers)

wget https://example.com/file.zip  # Download file

# Network statistics
netstat -s              # Protocol statistics
iftop                   # Bandwidth usage (interactive)
nmap -p 80,443 host.com # Port scan
```

---

### 3.4 System Information

```bash
# OS info
uname -a                # Kernel info
cat /etc/os-release     # OS distribution
lsb_release -a          # Ubuntu/Debian

# Disk usage
df -h                   # Disk free (human readable)
du -sh directory/       # Directory size
du -ah | sort -rh | head -10  # Top 10 largest files

# Memory
free -h                 # Memory usage
cat /proc/meminfo       # Detailed memory info

# CPU
lscpu                   # CPU architecture
cat /proc/cpuinfo       # Detailed CPU info
nproc                   # Number of processors

# Uptime
uptime                  # System uptime + load average
w                       # Who is logged in
```

---

### 3.5 Permissions

```bash
# View permissions
ls -la
# -rwxr-xr-x 1 user user 1234 Jan 1 12:00 file.txt
#    ^^^^^^^^
#    r=read, w=write, x=execute
#    Owner: rwx, Group: r-x, Others: r-x

# Change permissions
chmod +x script.sh           # Add execute
chmod -x script.sh           # Remove execute
chmod 755 script.sh          # rwxr-xr-x
chmod 644 file.txt           # rw-r--r--
chmod -R 755 directory/      # Recursive

# Change owner
chown user:group file.txt
chown -R user:group directory/

# Change group
chgrp developers project/
```

---

## 📚 BÀI 4: SHELL SCRIPTING

### 4.1 Basic Script

```bash
#!/bin/bash

# Variables
NAME="John"
echo "Hello, $NAME"

# Command line arguments
echo "First arg: $1"
echo "Second arg: $2"
echo "All args: $@"
echo "Script name: $0"
echo "Number of args: $#"

# Conditional
if [ -f "file.txt" ]; then
    echo "File exists"
elif [ -d "directory" ]; then
    echo "Directory exists"
else
    echo "Neither exists"
fi

# Comparison
if [ $a -eq $b ]; then    # Equal
    echo "Equal"
fi

if [ $a -gt $b ]; then    # Greater than
    echo "a > b"
fi

if [ "$str1" = "$str2" ]; then
    echo "Strings equal"
fi

# File tests
[ -f file.txt ]    # Is regular file
[ -d directory ]   # Is directory
[ -e path ]        # Exists
[ -r file ]        # Readable
[ -w file ]        # Writable
[ -x file ]        # Executable
```

---

### 4.2 Loops

```bash
#!/bin/bash

# For loop
for i in 1 2 3 4 5; do
    echo "Number: $i"
done

# Range
for i in {1..5}; do
    echo "Number: $i"
done

# Files
for file in *.java; do
    echo "Processing: $file"
done

# While loop
counter=0
while [ $counter -lt 5 ]; do
    echo "Counter: $counter"
    ((counter++))
done

# Read file line by line
while IFS= read -r line; do
    echo "Line: $line"
done < file.txt
```

---

### 4.3 Functions

```bash
#!/bin/bash

# Define function
greet() {
    local name=$1
    echo "Hello, $name"
}

# Call function
greet "John"

# Function with return
add() {
    local sum=$(($1 + $2))
    echo $sum
}

result=$(add 5 3)
echo "Result: $result"

# Check exit status
if command -v java &> /dev/null; then
    echo "Java is installed"
else
    echo "Java is NOT installed"
fi
```

---

### 4.4 Practical Scripts

```bash
#!/bin/bash
# deploy.sh - Simple deployment script

APP_NAME="myapp"
APP_HOME="/opt/$APP_NAME"
LOG_FILE="$APP_HOME/logs/app.log"

echo "Starting deployment of $APP_NAME..."

# Stop application
echo "Stopping application..."
systemctl stop $APP_NAME

# Backup current version
echo "Creating backup..."
cp -r $APP_HOME "${APP_HOME}.backup.$(date +%Y%m%d_%H%M%S)"

# Deploy new version
echo "Deploying new version..."
cp target/*.jar $APP_HOME/

# Start application
echo "Starting application..."
systemctl start $APP_NAME

# Check status
sleep 5
if systemctl is-active --quiet $APP_NAME; then
    echo "Deployment successful!"
    exit 0
else
    echo "Deployment failed!"
    echo "Check logs: $LOG_FILE"
    exit 1
fi
```

```bash
#!/bin/bash
# health-check.sh - Health check script

HOST="localhost"
PORT="8080"
TIMEOUT=5

echo "Health check for $HOST:$PORT"

# Check if port is open
if nc -z -w $TIMEOUT $HOST $PORT; then
    echo "✓ Port $PORT is open"
else
    echo "✗ Port $PORT is closed"
    exit 1
fi

# Check health endpoint
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
    --max-time $TIMEOUT \
    "http://$HOST:$PORT/actuator/health")

if [ "$RESPONSE" = "200" ]; then
    echo "✓ Health endpoint returned 200"
    exit 0
else
    echo "✗ Health endpoint returned $RESPONSE"
    exit 1
fi
```

---

## 📝 TÓM TẮT PHASE 08

1. ✅ HTTP methods, status codes, headers
2. ✅ HTTPS/TLS handshake
3. ✅ TCP/IP 3-way handshake
4. ✅ DNS resolution process
5. ✅ Load balancing algorithms
6. ✅ Linux commands (process, file, network)
7. ✅ Shell scripting basics

---

## 🔜 TIẾP THEO

Đọc `02-examples.md` để xem ví dụ thực tế!
