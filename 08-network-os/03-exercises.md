# Phase 08: Network & OS - Bài Tập Thực Hành

> **Thời gian:** 2-3 giờ
> **Mục tiêu:** Thành thạo Linux commands và network troubleshooting

---

## 📝 BÀI TẬP 1: LINUX COMMANDS PRACTICE (1 giờ)

### Đề bài

Thực hành các lệnh Linux sau trên server hoặc WSL:

### Part 1: File System Operations

```bash
# 1. Tạo cấu trúc thư mục
mkdir -p backend-learning/{00-java-core,01-spring-boot}/{theory,examples,exercises}

# 2. Tạo files rỗng
touch backend-learning/00-java-core/README.md
touch backend-learning/00-java-core/01-theory.md

# 3. Copy files
cp backend-learning/00-java-core/01-theory.md backend-learning/00-java-core/01-theory-backup.md

# 4. Di chuyển file
mv backend-learning/00-java-core/01-theory-backup.md backend-learning/00-java-core/backup/

# 5. Tìm files
find backend-learning -name "*.md"
find backend-learning -type f -size +10KB

# 6. Xem nội dung
cat backend-learning/00-java-core/README.md
head -n 20 backend-learning/00-java-core/01-theory.md
tail -f backend-learning/00-java-core/01-theory.md  # Follow mode

# 7. Search text
grep -r "HashMap" backend-learning/
grep -r "TODO" backend-learning/ --include="*.java"

# 8. Đếm số dòng
wc -l backend-learning/**/*.md

# 9. Xem cây thư mục
tree backend-learning/  # Nếu chưa có: sudo apt install tree

# 10. Xóa files và thư mục
rm backend-learning/00-java-core/backup/*
rmdir backend-learning/00-java-core/backup
```

---

### Part 2: Process Management

```bash
# 1. Xem tất cả processes
ps aux

# 2. Lọc processes Java
ps aux | grep java

# 3. Xem process theo PID
ps -p <PID> -o pid,ppid,user,%cpu,%mem,cmd

# 4. Tìm process theo tên
pgrep -f "spring-boot"

# 5. Xem tree processes
pstree -p

# 6. Interactive process viewer
top
htop  # Nếu chưa có: sudo apt install htop

# 7. Xem process chi tiết
cat /proc/<PID>/status
cat /proc/<PID>/cmdline

# 8. Nice value (priority)
renice -n 10 -p <PID>  # Giảm priority

# 9. Kill processes
kill <PID>             # SIGTERM
kill -9 <PID>          # SIGKILL
pkill -f "java"        # Kill by name

# 10. Chạy background
java -jar app.jar &
nohup java -jar app.jar > app.log 2>&1 &
```

---

### Part 3: Network Commands

```bash
# 1. Check network interfaces
ip addr show
ifconfig  # Nếu chưa có: sudo apt install net-tools

# 2. Check routing table
ip route show
netstat -rn

# 3. DNS lookup
nslookup google.com
dig google.com
dig +short google.com

# 4. Test connectivity
ping -c 4 google.com
ping -c 4 8.8.8.8

# 5. Trace route
traceroute google.com

# 6. Check listening ports
netstat -tulpn
ss -tulpn

# 7. Check specific port
nc -zv localhost 8080
telnet localhost 8080

# 8. HTTP requests
curl https://api.example.com/users
curl -X POST -d '{"name":"John"}' http://localhost:8080/api/users
curl -v http://localhost:8080/actuator/health

# 9. Download files
wget https://example.com/file.zip
curl -O https://example.com/file.zip

# 10. Network statistics
netstat -s
cat /proc/net/dev
```

---

### Part 4: System Information

```bash
# 1. OS info
uname -a
cat /etc/os-release
lsb_release -a

# 2. CPU info
lscpu
cat /proc/cpuinfo
nproc

# 3. Memory info
free -h
cat /proc/meminfo

# 4. Disk info
df -h
du -sh /var/log/

# 5. Uptime
uptime
w

# 6. Disk usage top 10
du -ah /var | sort -rh | head -10

# 7. Find large files
find / -type f -size +500M 2>/dev/null

# 8. Check open files
lsof -i :8080
lsof -p <PID>
```

---

### Cách submit

```markdown
## Linux Commands Practice Report

### Part 1: File System
- [ ] Created directory structure
- [ ] Created and moved files
- [ ] Used find and grep commands

### Part 2: Process Management
- [ ] Listed and filtered processes
- [ ] Used top/htop
- [ ] Killed processes

### Part 3: Network Commands
- [ ] Checked network interfaces
- [ ] Tested connectivity
- [ ] Made HTTP requests with curl

### Part 4: System Information
- [ ] Checked CPU, memory, disk info
- [ ] Found large files

### Screenshots/Output:
(Dán output của các commands quan trọng)
```

---

## 📝 BÀI TẬP 2: NETWORK TROUBLESHOOTING (1 giờ)

### Đề bài

**Scenario 1:** Application không thể connect đến database

```bash
# 1. Kiểm tra database có reachable không
ping db-server.example.com

# 2. Kiểm tra port có mở không
nc -zv db-server.example.com 5432
telnet db-server.example.com 5432

# 3. Check DNS resolution
nslookup db-server.example.com
dig db-server.example.com

# 4. Trace network path
traceroute db-server.example.com

# 5. Check firewall rules (nếu có access)
sudo iptables -L -n | grep 5432

# 6. Test connection trực tiếp
psql -h db-server.example.com -U postgres -d mydb
```

**Scenario 2:** API response chậm

```bash
# 1. Measure response time
curl -w "@curl-format.txt" -o /dev/null -s https://api.example.com/endpoint

# curl-format.txt content:
#     time_namelookup:  %{time_namelookup}\n
#        time_connect:  %{time_connect}\n
#     time_appconnect:  %{time_appconnect}\n
#    time_pretransfer:  %{time_pretransfer}\n
#      time_redirect:  %{time_redirect}\n
# time_starttransfer:  %{time_starttransfer}\n
#                    ----------\n
#         time_total:  %{time_total}\n

# 2. Check network latency
ping -c 10 api.example.com

# 3. Check packet loss
mtr api.example.com

# 4. Capture packets
sudo tcpdump -i eth0 port 443 -w capture.pcap

# 5. Analyze với Wireshark (local)
# Mở file capture.pcap trong Wireshark
```

**Scenario 3:** Port conflict

```bash
# 1. Check port đang được sử dụng
netstat -tulpn | grep 8080
ss -tulpn | grep 8080
lsof -i :8080

# 2. Tìm process đang giữ port
sudo lsof -i :8080

# 3. Kill process nếu cần
sudo kill -9 <PID>

# 4. Or change application port
# Edit application.properties: server.port=8081
```

---

## 📝 BÀI TẬP 3: SHELL SCRIPTING (1 giờ)

### Đề bài

**Bài 1:** Viết script backup database

```bash
#!/bin/bash
# backup.sh - Backup PostgreSQL database

# Configuration
DB_NAME="myapp"
DB_USER="postgres"
BACKUP_DIR="/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Create backup
pg_dump -U "$DB_USER" "$DB_NAME" > "$BACKUP_DIR/$DB_NAME.$TIMESTAMP.sql"

# Compress backup
gzip "$BACKUP_DIR/$DB_NAME.$TIMESTAMP.sql"

# Remove old backups
find "$BACKUP_DIR" -name "$DB_NAME.*.sql.gz" -mtime +$RETENTION_DAYS -delete

echo "Backup completed: $BACKUP_DIR/$DB_NAME.$TIMESTAMP.sql.gz"
```

**Bài 2:** Viết script health check

```bash
#!/bin/bash
# health-check.sh - Check application health

# Configuration
APP_NAME="myapp"
PORT=8080
HEALTH_ENDPOINT="/actuator/health"

# Check if service is running
if systemctl is-active --quiet "$APP_NAME"; then
    echo "✓ Service $APP_NAME is running"
else
    echo "✗ Service $APP_NAME is NOT running"
    exit 1
fi

# Check if port is listening
if nc -z localhost $PORT; then
    echo "✓ Port $PORT is open"
else
    echo "✗ Port $PORT is closed"
    exit 1
fi

# Check health endpoint
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$PORT$HEALTH_ENDPOINT)

if [ "$RESPONSE" = "200" ]; then
    echo "✓ Health endpoint returned 200"
    exit 0
else
    echo "✗ Health endpoint returned $RESPONSE"
    exit 1
fi
```

**Bài 3:** Viết script deploy đơn giản

```bash
#!/bin/bash
# deploy.sh - Simple deployment script

set -e  # Exit on error

APP_NAME="myapp"
APP_HOME="/opt/$APP_NAME"

echo "Starting deployment..."

# Stop application
echo "Stopping application..."
systemctl stop "$APP_NAME"

# Backup
echo "Creating backup..."
cp -r "$APP_HOME" "/backups/$APP_NAME-$(date +%Y%m%d_%H%M%S)"

# Deploy new version
echo "Deploying new version..."
cp target/*.jar "$APP_HOME/"

# Start application
echo "Starting application..."
systemctl start "$APP_NAME"

# Health check
sleep 5
if systemctl is-active --quiet "$APP_NAME"; then
    echo "✓ Deployment successful!"
    exit 0
else
    echo "✗ Deployment failed!"
    exit 1
fi
```

---

## ✅ CHECKLIST HOÀN THÀNH PHASE 08

- [ ] Thực hành được file system commands
- [ ] Thực hành được process management
- [ ] Thực hành được network commands
- [ ] Thực hành được system monitoring
- [ ] Debug được network connectivity issues
- [ ] Viết được shell scripts đơn giản
- [ ] Hiểu được HTTP troubleshooting flow

---

## 📤 CÁCH SUBMIT

1. Push scripts lên GitHub
2. Tạo file `NETWORK_OS_REPORT.md` với:
   - Link GitHub với các scripts
   - Output của các commands
   - Khó khăn gặp phải

---

## 🔜 SAU KHI HOÀN THÀNH

Submit xong, unlock Phase 09: System Design!
