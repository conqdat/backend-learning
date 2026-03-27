# Phase 08: Network & OS - Lý Thuyết

> **Thời gian:** 3 tuần
> **Mục tiêu:** Hiểu networking và Linux fundamentals cho backend development
>
> **Tham khảo:** [roadmap.sh/linux](https://roadmap.sh/linux), [roadmap.sh/devops](https://roadmap.sh/devops)

---

## 📚 BÀI 0: LINUX FUNDAMENTALS

### 0.1 Linux Distribution

**Popular Distributions:**

| Distribution | Use Case | Package Manager |
|-------------|----------|-----------------|
| Ubuntu/Debian | Development, web servers | apt, apt-get |
| RHEL/CentOS | Enterprise servers | yum, dnf |
| SUSE Linux | Enterprise, SAP | zypper |
| Alpine | Containers, minimal | apk |
| Arch Linux | Development, learning | pacman |

---

### 0.2 Directory Hierarchy

```
/
├── bin/          # Essential binaries (ls, cp, mv)
├── boot/         # Boot loader files
├── dev/          # Device files
├── etc/          # Configuration files
├── home/         # User home directories
├── lib/          # Shared libraries
├── media/        # Removable media
├── mnt/          # Mount point
├── opt/          # Optional software
├── proc/         # Process information (virtual)
├── root/         # Root user home
├── run/          # Runtime data
├── sbin/         # System binaries (root only)
├── srv/          # Service data
├── sys/          # System information (virtual)
├── tmp/          # Temporary files
├── usr/          # User programs
│   ├── bin/      # User binaries
│   ├── lib/      # User libraries
│   └── local/    # Locally installed software
└── var/          # Variable data (logs, databases)
    ├── log/      # Log files
    └── www/      # Web server data
```

---

### 0.3 Shell & Terminal

**Common Shells:**
- `bash` - Default on most Linux distributions
- `zsh` - Modern shell with plugins (Oh My Zsh)
- `sh` - Bourne shell (POSIX standard)
- `fish` - Friendly interactive shell

**Terminal Knowledge:**
```bash
# Shell variables
echo $SHELL        # Current shell
echo $HOME         # Home directory
echo $PATH         # Search path for commands
echo $USER         # Current user
echo $PWD          # Current directory
echo $HOSTNAME     # Hostname

# Environment variables
export MY_VAR="value"
env                # List all environment variables
unset MY_VAR       # Remove variable

# Command history
history            # Show command history
!123               # Run command #123 from history
!!                 # Run last command
!$                 # Last argument of last command
Ctrl+R             # Search history (interactive)

# Command substitution
CURRENT_DATE=$(date)
FILES=$(ls -la | wc -l)

# Pipes and redirection
command1 | command2        # Pipe output
command > file.txt         # Redirect stdout (overwrite)
command >> file.txt        # Redirect stdout (append)
command 2> error.log       # Redirect stderr
command > output.txt 2>&1  # Redirect both stdout and stderr
command < input.txt        # Redirect stdin
```

---

### 0.4 Text Processing

```bash
# cut - Extract sections from lines
cut -d: -f1 /etc/passwd          # First field (username)
cut -d' ' -f1-3 file.txt         # Fields 1-3

# paste - Merge lines of files
paste file1.txt file2.txt
paste -d',' file1.txt file2.txt  # With delimiter

# sort - Sort lines
sort file.txt                    # Alphabetical
sort -n file.txt                 # Numeric
sort -r file.txt                 # Reverse
sort -u file.txt                 # Unique
sort -t: -k3 -n /etc/passwd      # Sort by 3rd field

# head/tail - First/last lines
head -n 20 file.txt              # First 20 lines
tail -n 20 file.txt              # Last 20 lines
tail -f /var/log/app.log         # Follow (real-time)
tail -F /var/log/app.log         # Follow with retry

# join - Join lines on common field
join -t: file1.txt file2.txt

# split - Split file into pieces
split -l 100 large.txt small_    # 100 lines per file
split -b 10M large.tar.gz part_  # 10MB per file

# tee - Read from stdin, write to stdout and file
command | tee output.txt         # Save and display
command | tee -a output.txt      # Append

# nl - Number lines
nl file.txt

# wc - Word count
wc file.txt                      # Lines, words, bytes
wc -l file.txt                   # Lines only
wc -w file.txt                   # Words only
wc -c file.txt                   # Bytes only

# uniq - Filter adjacent duplicate lines
sort file.txt | uniq             # Remove duplicates
sort file.txt | uniq -c          # Count occurrences
sort file.txt | uniq -d          # Show duplicates only

# grep - Search text
grep "error" file.txt                    # Basic search
grep -i "error" file.txt                 # Case insensitive
grep -r "TODO" src/                      # Recursive
grep -E "pattern1|pattern2" file.txt     # Extended regex
grep -v "exclude" file.txt               # Inverse match
grep -c "error" file.txt                 # Count matches
grep -n "error" file.txt                 # Show line numbers
grep -l "error" *.log                    # Files with matches
grep -A 3 "error" file.txt               # 3 lines after match
grep -B 3 "error" file.txt               # 3 lines before match
grep -C 3 "error" file.txt               # 3 lines context

# awk - Pattern scanning and processing
awk '{print $1}' file.txt                # Print first field
awk -F: '{print $1}' /etc/passwd         # Custom delimiter
awk '$3 > 1000 {print $1}' file.txt      # Condition
awk '{sum+=$1} END {print sum}' nums.txt # Sum
awk '{print NR": "$0}' file.txt          # Line numbers

# sed - Stream editor
sed 's/old/new/g' file.txt               # Replace all
sed 's/old/new/1' file.txt               # Replace first
sed -i 's/old/new/g' file.txt            # In-place edit
sed '/pattern/d' file.txt                # Delete lines
sed -n '5,10p' file.txt                  # Print lines 5-10
sed -n 's/pattern/replacement/p' file.txt # Print only matches
```

---

### 0.5 Process Management Deep Dive

```bash
# Process states
# R - Running/Runnable
# S - Sleeping (interruptible)
# D - Sleeping (uninterruptible, usually I/O)
# T - Stopped
# Z - Zombie (terminated but not reaped)

# Background/Foreground jobs
./long-running.sh &          # Run in background
jobs                         # List background jobs
fg %1                        # Bring job 1 to foreground
bg %1                        # Send job 1 to background
Ctrl+Z                       # Suspend current job
Ctrl+C                       # Kill current job

# Process signals
kill -l                      # List all signals
kill -TERM 1234              # Graceful terminate (SIGTERM, 15)
kill -KILL 1234              # Force kill (SIGKILL, 9)
kill -HUP 1234               # Reload config (SIGHUP, 1)
kill -INT 1234               # Interrupt (SIGINT, 2)
kill -USR1 1234              # User-defined signal 1

# Process priorities (nice values)
nice -n 10 ./slow.sh         # Run with lower priority
renice +5 -p 1234            # Change priority of running process
# Nice range: -20 (highest) to 19 (lowest)

# Process forking
# Parent creates child process with fork()
# Child gets copy of parent's memory space
# ps -ef --forest           # Show process tree
pstree -p                    # Show process tree with PIDs
```

---

### 0.6 User & Group Management

```bash
# User management
useradd -m john              # Create user with home directory
userdel -r john              # Delete user and home directory
usermod -aG sudo john        # Add user to sudo group
passwd john                  # Change user password
id john                      # Show user info
whoami                       # Current user
users                        # Logged in users
w                            # Who is logged in + what doing

# Group management
groupadd developers
groupdel developers
groups john                  # Show user's groups

# Permission management
chmod 755 script.sh          # rwxr-xr-x
chmod u+x script.sh          # Add execute for owner
chmod g-w file.txt           # Remove write for group
chmod o=r file.txt           # Others can only read
chmod a+x script.sh          # All can execute

# Special permissions
chmod u+s binary             # SetUID - run as owner
chmod g+s directory          # SetGID - inherit group
chmod +t /tmp                # Sticky bit - only owner can delete

# sudo
sudo command                 # Run as root
sudo -u postgres command     # Run as specific user
visudo                       # Edit sudoers file safely
```

---

### 0.7 Package Management

```bash
# APT (Debian/Ubuntu)
sudo apt update              # Update package list
sudo apt upgrade             # Upgrade packages
sudo apt install nginx       # Install package
sudo apt remove nginx        # Remove package
sudo apt purge nginx         # Remove + config files
sudo apt search keyword      # Search packages
apt list --installed         # List installed packages
apt show package             # Show package info

# YUM/DNF (RHEL/CentOS)
sudo yum update
sudo yum install nginx
sudo yum remove nginx
sudo yum search keyword
sudo yum list installed

# APK (Alpine)
apk update
apk add nginx
apk del nginx
apk search keyword

# Snap (Universal)
snap install package
snap remove package
snap list
snap refresh               # Update
```

---

### 0.8 Systemd (Service Management)

```bash
# Service management
systemctl start nginx              # Start service
systemctl stop nginx               # Stop service
systemctl restart nginx            # Restart service
systemctl reload nginx             # Reload config
systemctl status nginx             # Check status
systemctl enable nginx             # Enable at boot
systemctl disable nginx            # Disable at boot
systemctl is-active nginx          # Check if running
systemctl is-enabled nginx         # Check if enabled

# View logs
journalctl -u nginx                # Service logs
journalctl -u nginx -f             # Follow logs
journalctl -u nginx --since today  # Today's logs
journalctl -u nginx -n 50          # Last 50 lines

# Create custom service
# /etc/systemd/system/myapp.service
[Unit]
Description=My Spring Boot App
After=network.target

[Service]
Type=simple
User=appuser
WorkingDirectory=/opt/myapp
ExecStart=/usr/bin/java -jar /opt/myapp/app.jar
Restart=on-failure
Environment=SPRING_PROFILES_ACTIVE=prod

[Install]
WantedBy=multi-user.target

# Reload systemd and enable
systemctl daemon-reload
systemctl enable myapp
systemctl start myapp
```

---

### 0.9 Disk & Filesystem

```bash
# Disk information
df -h                      # Disk free (human readable)
df -i                      # Inode usage
du -sh directory/          # Directory size
du -ah | sort -rh | head -20   # Top 20 largest files

# Mount management
mount                      # Show mounted filesystems
umount /mnt/disk           # Unmount
mount -t nfs server:/path /mnt   # Mount NFS
lsblk                      # List block devices
blkid                      # Show block device UUIDs

# Filesystem info
cat /etc/fstab             # Mount points config
cat /proc/mounts           # Currently mounted

# Swap
free -h                    # Memory + swap
swapon --show              # Show swap
sudo swapon /dev/sda2      # Enable swap
sudo swapoff /dev/sda2     # Disable swap
```

---

### 0.10 Network Configuration

```bash
# Interface configuration
ip addr show               # Show IP addresses
ip link show               # Show network interfaces
ip route show              # Show routing table
ip neigh show              # Show ARP table

# Legacy commands
ifconfig                   # Interface config (deprecated)
route -n                   # Routing table (deprecated)
arp -a                     # ARP table (deprecated)

# DNS configuration
cat /etc/resolv.conf       # DNS servers
cat /etc/hosts             # Local hostname mappings
hostnamectl                # Hostname control
hostname myserver          # Set hostname

# Network troubleshooting
ping -c 4 google.com       # Test connectivity
traceroute google.com      # Trace route
mtr google.com             # Combined ping + traceroute
ss -tulpn                  # Listening ports
netstat -tulpn             # Legacy alternative
tcpdump -i eth0 port 80    # Packet capture
tcpdump -i eth0 -w capture.pcap  # Save to file

# SSH
ssh user@host              # SSH connect
ssh -i key.pem user@host   # With key
ssh -p 2222 user@host      # Custom port
scp file.txt user@host:/path   # Copy file
scp -r dir/ user@host:/path     # Copy directory
rsync -avz src/ dst/       # Sync files
```

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
