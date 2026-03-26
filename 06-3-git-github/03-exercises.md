# Phase 06.7: Git & GitHub - Bài Tập Thực Hành

> **Thời gian:** 2-3 giờ
> **Mục tiêu:** Thực hành Git workflow, GitHub Actions, code review

---

## 📝 BÀI TẬP 1: GIT BRANCHING WORKFLOW (45 phút)

### Đề bài

Thực hành Git Flow workflow cho feature development

### Phần 1: Setup repository

```bash
# 1. Tạo repository mới (hoặc dùng existing)
mkdir git-practice
cd git-practice
git init

# 2. Tạo initial commit
echo "# Git Practice" > README.md
git add README.md
git commit -m "chore: Initial commit"

# 3. Tạo develop branch
git checkout -b develop
git push -u origin develop
```

### Phần 2: Feature development

```bash
# 1. Tạo feature branch từ develop
git checkout develop
git checkout -b feature/user-authentication

# 2. Tạo một số files giả lập
mkdir -p src/main/java/com/example/security
touch src/main/java/com/example/security/JwtTokenProvider.java
touch src/main/java/com/example/security/SecurityConfig.java

# 3. Commit với message đúng chuẩn
git add .
git commit -m "feat: Add JWT token provider"

git add .
git commit -m "feat: Add Spring Security configuration"

git add .
git commit -m "test: Add unit tests for JwtTokenProvider"

# 4. Rebase interactive để squash commits
git rebase -i HEAD~3

# Squash 3 commits thành 1 commit duy nhất
# Kết quả: "feat: Add user authentication module"

# 5. Update với develop mới nhất
git fetch origin
git rebase origin/develop

# 6. Push feature branch
git push -u origin feature/user-authentication
```

### Phần 3: Merge vào develop

```bash
# 1. Checkout develop
git checkout develop

# 2. Pull latest
git pull origin develop

# 3. Merge feature branch (no fast-forward)
git merge --no-ff feature/user-authentication

# 4. Push develop
git push origin develop

# 5. Delete feature branch
git branch -d feature/user-authentication
git push origin --delete feature/user-authentication
```

### Checklist hoàn thành

- [ ] Tạo được feature branch từ develop
- [ ] Commit với message đúng convention
- [ ] Squash commits với interactive rebase
- [ ] Merge với --no-ff flag
- [ ] Delete feature branch sau merge

---

## 📝 BÀI TẬP 2: GIT CONFLICT RESOLUTION (30 phút)

### Đề bài

Thực hành resolve merge conflicts

### Phần 1: Tạo conflict

```bash
# Terminal 1
git checkout develop
echo "// Line 1" > src/main/java/App.java
echo "// Line 2" >> src/main/java/App.java
echo "// Line 3" >> src/main/java/App.java
git add .
git commit -m "feat: Add App.java"
git push origin develop

# Tạo feature branch 1
git checkout -b feature/login
echo "// Line 2 - Modified by login team" > src/main/java/App.java
git add .
git commit -m "feat: Login team modification"

# Terminal 2 (tạo conflict)
git checkout develop
git checkout -b feature/signup
echo "// Line 2 - Modified by signup team" > src/main/java/App.java
git add .
git commit -m "feat: Signup team modification"
```

### Phần 2: Resolve conflict

```bash
# Checkout feature/login
git checkout feature/login

# Try to merge develop (will cause conflict)
git merge develop

# Output:
# CONFLICT (content): Merge conflict in src/main/java/App.java
# Automatic merge failed; fix conflicts and then commit the result.

# Xem conflict
cat src/main/java/App.java

# Output sẽ thấy:
# // Line 1
# <<<<<<< HEAD
# // Line 2 - Modified by login team
# =======
# // Line 2 - Modified by signup team
# >>>>>>> develop

# Edit file để resolve conflict
cat > src/main/java/App.java << 'EOF'
// Line 1
// Line 2 - Merged: Login + Signup functionality
// Line 3
EOF

# Add và commit
git add src/main/java/App.java
git commit -m "merge: Resolve conflict between login and signup"

# Push
git push origin feature/login
```

### Checklist hoàn thành

- [ ] Tạo được merge conflict
- [ ] Resolve conflict thành công
- [ ] Commit merge result

---

## 📝 BÀI TẬP 3: GITHUB ACTIONS CI PIPELINE (1 giờ)

### Đề bài

Tạo CI pipeline cho Spring Boot project

### Phần 1: Tạo workflow cơ bản

**Yêu cầu:** Tạo file `.github/workflows/ci.yml` với:

```yaml
# TODO: Complete CI pipeline
name: CI Pipeline

on:
  push:
    branches: [___]
  pull_request:
    branches: [___]

jobs:
  build:
    runs-on: ___
    steps:
    - name: ___
      uses: ___

    - name: Setup Java
      uses: ___

    - name: Build with Gradle
      run: ___

  test:
    runs-on: ___
    needs: ___
    steps:
    - name: ___
      # TODO: Add test steps
```

### Phần 2: Thêm code quality checks

```yaml
# TODO: Thêm job cho code quality
code-quality:
  runs-on: ubuntu-latest
  steps:
  # TODO: Add checkstyle, spotbugs steps
```

### Phần 3: Thêm coverage report

```yaml
# TODO: Thêm job cho coverage
coverage:
  runs-on: ubuntu-latest
  steps:
  # TODO: Run jacocoTestReport
  # TODO: Upload coverage artifact
```

### Phần 4: Test với matrix

```yaml
# TODO: Test với nhiều Java versions
test-matrix:
  runs-on: ubuntu-latest
  strategy:
    matrix:
      java: [___, ___, ___]
  steps:
  # TODO: Setup Java với matrix version
```

### Checklist hoàn thành

- [ ] CI workflow chạy thành công
- [ ] Build job passes
- [ ] Test job passes
- [ ] Code quality checks passes
- [ ] Coverage report được upload

---

## 📝 BÀI TẬP 4: PULL REQUEST WORKFLOW (30 phút)

### Đề bài

Thực hành PR workflow hoàn chỉnh

### Phần 1: Tạo PR

```bash
# 1. Tạo feature branch
git checkout develop
git checkout -b feature/product-crud

# 2. Tạo commits
mkdir -p src/main/java/com/example/product
touch src/main/java/com/example/product/{Product,ProductController,ProductService}.java

git add .
git commit -m "feat: Add Product entity"

git add .
git commit -m "feat: Add ProductService with CRUD operations"

git add .
git commit -m "feat: Add ProductController REST endpoints"

git push -u origin feature/product-crud
```

### Phần 2: Tạo Pull Request

**Trên GitHub:**

1. Navigate to repository
2. Click "Compare & pull request"
3. Fill in PR template:

```markdown
## Description
Add Product CRUD functionality with REST API endpoints

## Type of change
- [x] ✨ New feature

## Testing
- [x] Unit tests added (15 tests)
- [x] Integration tests added (5 tests)

## Checklist
- [x] Code follows guidelines
- [x] Self-review completed
- [x] Documentation updated

## Related Issues
Fixes #42
```

4. Add reviewers
5. Add labels (feature, backend, api)

### Phần 3: Code Review

**Reviewer checklist:**

```
✅ Code architecture:
- Controllers call Service, not Repository directly
- Proper exception handling
- DTO pattern used for API responses

✅ Testing:
- Unit tests cover edge cases
- Integration tests for API endpoints
- Mock external dependencies

✅ Code style:
- Naming conventions followed
- No magic numbers
- Methods < 25 lines

✅ Security:
- @PreAuthorize for protected endpoints
- Input validation with @Valid
- No SQL injection risks
```

### Phần 4: Address feedback và merge

```bash
# 1. Fetch review comments
# 2. Make changes on feature branch
git add .
git commit -m "fix: Address PR feedback - add null checks"

git push origin feature/product-crud

# 3. After approval, merge (squash and merge recommended)
# 4. Delete branch sau merge
```

### Checklist hoàn thành

- [ ] PR created với description đầy đủ
- [ ] Reviewers assigned
- [ ] CI checks passes
- [ ] Feedback addressed
- [ ] PR merged
- [ ] Branch deleted

---

## 📝 BÀI TẬP 5: GIT HOOKS AUTOMATION (30 phút)

### Đề bài

Tạo git hooks cho project

### Phần 1: Pre-commit hook

**Yêu cầu:** Tạo `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# TODO: Implement pre-commit hook

# 1. Check for trailing whitespace
# 2. Check for TODO/FIXME comments
# 3. Run linter (nếu có)
# 4. Run tests (optional, có thể chậm)

echo "✅ Pre-commit checks passed!"
exit 0
```

### Phần 2: Commit-msg hook

**Yêu cầu:** Tạo `.git/hooks/commit-msg`:

```bash
#!/bin/bash
# TODO: Implement commit-msg hook

# Validate commit message format:
# - Must start with: feat, fix, docs, style, refactor, test, chore
# - Format: <type>: <description>
# - Description length: 1-50 characters

# Example valid:
# feat: Add user authentication
# fix: Resolve NPE in OrderService

# Example invalid:
# added new feature
# FIX STUFF!!!
```

### Phần 3: Pre-push hook

**Yêu cầu:** Tạo `.git/hooks/pre-push`:

```bash
#!/bin/bash
# TODO: Implement pre-push hook

# 1. Run tests
# 2. Check current branch (prevent push to main)
# 3. Check commit message format

echo "✅ Pre-push checks passed!"
exit 0
```

### Checklist hoàn thành

- [ ] Pre-commit hook hoạt động
- [ ] Commit-msg hook validate message
- [ ] Pre-push hook prevent bad pushes

---

## 📝 BÀI TẬP 6: GIT BLAME & DEBUGGING (15 phút)

### Đề bài

Sử dụng Git để debug và investigate code

### Bài tập:

```bash
# 1. Tìm ai đã viết line gây bug
git blame -L 42,42 src/main/java/UserService.java

# 2. Xem commit đó thay đổi những gì
git show <commit-hash>

# 3. Tìm commit introduce bug (dùng bisect)
git bisect start
git bisect bad HEAD
git bisect good v1.0.0
# Test và report good/bad cho đến khi tìm được commit

git bisect reset

# 4. Tìm commit sửa một specific method
git log -p -S "methodName" -- src/main/java/UserService.java

# 5. Xem lịch sử file với graph
git log --oneline --graph --follow src/main/java/UserService.java
```

### Checklist hoàn thành

- [ ] Sử dụng được git blame
- [ ] Sử dụng được git bisect
- [ ] Tìm được commit history của file

---

## ✅ CHECKLIST HOÀN THÀNH PHASE 06.7

- [ ] Thực hành Git Flow workflow
- [ ] Resolve merge conflicts thành công
- [ ] Tạo CI pipeline với GitHub Actions
- [ ] Thực hành PR workflow hoàn chỉnh
- [ ] Tạo git hooks (pre-commit, commit-msg, pre-push)
- [ ] Sử dụng git blame, bisect để debug
- [ ] Squash commits với interactive rebase
- [ ] Code review với checklist

---

## 📤 CÁCH SUBMIT

1. Push repository lên GitHub với:
   - `.github/workflows/ci.yml`
   - `.git/hooks/` (hoặc docs về hooks)
   - Commit history thể hiện workflow đúng
2. Tạo file `GIT_GITHUB_REPORT.md` với:
   - Link GitHub repository
   - Screenshot CI pipeline runs
   - Screenshot PR đã merge
   - Khó khăn gặp phải

---

## 🔜 SAU KHI HOÀN THÀNH

Submit xong, học tiếp Phase sau!
