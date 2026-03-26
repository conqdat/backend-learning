# Phase 06.7: Git & GitHub cho Backend Developers

> **Thời gian:** 2 tuần
> **Mục tiêu:** Master Git workflow, GitHub Actions CI/CD, code review best practices

---

## 📚 BÀI 1: GIT FUNDAMENTALS

### 1.1 Git Internals - Hiểu bản chất

```
Git = Content-addressable filesystem + VCS

Core objects:
┌─────────────────────────────────────────────────────────────┐
│  1. Blob (Binary Large Object)                              │
│     - Content của file                                      │
│     - SHA-1 hash của content làm identifier                 │
│     - Example: echo "hello" | git hash-object -w --stdin   │
├─────────────────────────────────────────────────────────────┤
│  2. Tree                                                    │
│     - Directory structure                                   │
│     - Chứa blobs và trees con                               │
│     - Giống như folder hierarchy                            │
├─────────────────────────────────────────────────────────────┤
│  3. Commit                                                  │
│     - Snapshot của tree                                     │
│     - Metadata: author, committer, message, parent(s)       │
│     - SHA-1 hash của commit làm identifier                  │
├─────────────────────────────────────────────────────────────┤
│  4. Ref (Reference)                                         │
│     - Pointer to commit                                     │
│     - Branches, HEAD, tags                                  │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Git Object Model

```
Commit Structure:

┌─────────────────────────────────────────────────────────────┐
│  Commit: a1b2c3d4...                                        │
│  ├─ tree: e5f6g7h8... (root directory)                     │
│  │   ├─ blob: 1234... (README.md)                          │
│  │   ├─ tree: 5678... (src/)                               │
│  │   │   ├─ blob: abcd... (Main.java)                      │
│  │   │   └─ blob: efgh... (Utils.java)                     │
│  │   └─ blob: 9012... (pom.xml)                            │
│  ├─ parent: 9z8y7x6w... (previous commit)                  │
│  ├─ author: John <john@example.com> 1234567890 +0700       │
│  └─ committer: Jane <jane@example.com> 1234567895 +0700    │
└─────────────────────────────────────────────────────────────┘

Branch = Pointer to Commit:

  main ──────► [commit a1b2c3d]

  feature ───► [commit e5f6g7h]
                   │
                   └─ parent: [commit a1b2c3d] ◄── main
```

---

## 📚 BÀI 2: BRANCHING STRATEGIES

### 2.1 Git Flow (Classic)

```
┌─────────────────────────────────────────────────────────────────┐
│                    GIT FLOW                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  main (production-ready)                                        │
│  │                                                               │
│  │───release/v1.0─────► merge ────► tag v1.0.0                 │
│  │        ▲                                                   │
│  │        │ merge                                             │
│  │  develop────────────────────────────────────                │
│  │    │     │                                                  │
│  │    │     ├──feature/login───────► merge                    │
│  │    │     ├──feature/signup──────► merge                    │
│  │    │     └──feature/api─────────► merge                    │
│  │    │                                                       │
│  │  hotfix/bugfix──────► merge ────► tag v1.0.1               │
│                                                                  │
│  Branch types:                                                  │
│  - main/master: Production releases only                       │
│  - develop: Integration branch                                 │
│  - feature/*: New features (from develop)                      │
│  - release/*: Release preparation                              │
│  - hotfix/*: Production bug fixes (from main)                  │
└─────────────────────────────────────────────────────────────────┘
```

**Commands:**

```bash
# Setup Git Flow
git flow init

# Start feature
git flow feature start login
git flow feature finish login

# Start release
git flow release start 1.0.0
git flow release finish 1.0.0

# Hotfix
git flow hotfix start bugfix-1
git flow hotfix finish bugfix-1
```

### 2.2 GitHub Flow (Simpler)

```
┌─────────────────────────────────────────────────────────────────┐
│                    GITHUB FLOW                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  main (always deployable)                                       │
│  │                                                               │
│  ├───feature/login──────PR──────► merge                        │
│  │                                                               │
│  ├───feature/signup─────PR──────► merge                        │
│  │                                                               │
│  └───bugfix/fix-123─────PR──────► merge                        │
│                                                                  │
│  Workflow:                                                       │
│  1. Branch from main                                             │
│  2. Make changes + commit                                        │
│  3. Open Pull Request                                            │
│  4. Code review + CI checks                                      │
│  5. Merge to main                                                │
│  6. Deploy                                                       │
└─────────────────────────────────────────────────────────────────┘
```

### 2.3 Trunk-Based Development

```
┌─────────────────────────────────────────────────────────────────┐
│              TRUNK-BASED DEVELOPMENT                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  main/trunk (developers commit directly)                        │
│  │                                                               │
│  ├──►c1──►c2──►c3──►c4──►c5──►c6 (commits)                     │
│  │     │              │                                        │
│  │     │              └─ short-lived branch (< 1 day)          │
│  │     │                                                        │
│  │     └─ Feature flags cho incomplete features                │
│                                                                  │
│  Benefits:                                                       │
│  - Fast feedback                                                 │
│  - Small commits                                                 │
│  - No merge hell                                                 │
│  - Requires: CI, testing, feature flags                         │
└─────────────────────────────────────────────────────────────────┘
```

### 2.4 So sánh các strategies

| Aspect | Git Flow | GitHub Flow | Trunk-Based |
|--------|----------|-------------|-------------|
| Complexity | High | Low | Medium |
| Release frequency | Low | Medium | High |
| Team size | Large | Small-Medium | Small-Medium |
| CI/CD requirement | Optional | Recommended | Required |
| Feature flags | Optional | Optional | Required |

---

## 📚 BÀI 3: REBASING vs MERGING

### 3.1 Merge

```
Before merge:
  main:    A ─── B ─── C
                      \
  feature:              D ─── E

After merge (merge commit):
  main:    A ─── B ─── C ─── F (merge commit)
                      \     /
  feature:              D ─── E

Pros:
- Preserves complete history
- Shows when feature was integrated
- Non-destructive

Cons:
- Extra merge commits
- History can get messy
```

### 3.2 Rebase

```
Before rebase:
  main:    A ─── B ─── C
                      \
  feature:              D ─── E

After rebase:
  main:    A ─── B ─── C
                          \
  feature:                  D' ─── E'

After merge (fast-forward):
  main/feature: A ─── B ─── C ─── D' ─── E'

Pros:
- Linear history
- No extra merge commits
- Clean history

Cons:
- Rewrites history (dangerous on shared branches)
- Can lose context
```

### 3.3 When to use what?

```
✅ DO Rebase:
- Local feature branch before PR
- Keeping branch up to date with main

✅ DO Merge:
- Integrating feature to main
- Hotfixes to production

❌ DON'T Rebase:
- Shared/public branches
- After someone else based work on your branch
```

### 3.4 Interactive Rebase

```bash
# Squash multiple commits
git rebase -i HEAD~3

# Editor opens:
pick    a1b2c3d  Add login form
pick    d4e5f6g  Fix login validation
pick    h7i8j9k  Add login tests

# Change to:
reword  a1b2c3d  Add login form
fixup   d4e5f6g  Fix login validation
fixup   h7i8j9k  Add login tests

# Result: Single commit with combined changes
```

---

## 📚 BÀI 4: GIT HOOKS

### 4.1 Available Hooks

```
┌─────────────────────────────────────────────────────────────────┐
│                    GIT HOOKS                                     │
├─────────────────────────────────────────────────────────────────┤
│  Client-side:                                                   │
│  - pre-commit: Before commit (linting, formatting)             │
│  - prepare-commit-msg: Before editor opens                     │
│  - commit-msg: After message entered (validate message)        │
│  - post-commit: After commit (notifications)                   │
│  - pre-push: Before push (run tests)                           │
│                                                                  │
│  Server-side:                                                   │
│  - pre-receive: Before accepting push                          │
│  - update: Similar to pre-receive, per branch                  │
│  - post-receive: After push (deploy, notify)                   │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Example: Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running pre-commit checks..."

# Check for trailing whitespace
if git diff --cached --check | grep -q "trailing whitespace"; then
    echo "❌ Trailing whitespace found!"
    exit 1
fi

# Run linter
echo "Running linter..."
./gradlew checkstyleMain checkstyleTest

if [ $? -ne 0 ]; then
    echo "❌ Linter failed!"
    exit 1
fi

# Run tests
echo "Running tests..."
./gradlew test

if [ $? -ne 0 ]; then
    echo "❌ Tests failed!"
    exit 1
fi

echo "✅ All checks passed!"
exit 0
```

### 4.3 Example: Commit-msg Hook

```bash
#!/bin/bash
# .git/hooks/commit-msg

commit_msg=$(cat "$1")

# Check commit message format: feat/fix/docs/style/refactor/test/chore: description
if ! echo "$commit_msg" | grep -qE "^(feat|fix|docs|style|refactor|test|chore): .{1,50}$"; then
    echo "❌ Invalid commit message format!"
    echo ""
    echo "Expected format: <type>: <description>"
    echo "Types: feat, fix, docs, style, refactor, test, chore"
    echo ""
    echo "Examples:"
    echo "  feat: Add user authentication"
    echo "  fix: Resolve NPE in OrderService"
    echo "  docs: Update README with setup instructions"
    exit 1
fi

# Check for signed-off-by
if ! echo "$commit_msg" | grep -q "Signed-off-by:"; then
    echo "⚠️  Adding Signed-off-by..."
    echo "" >> "$1"
    echo "Signed-off-by: $(git config user.name) <$(git config user.email)>" >> "$1"
fi

exit 0
```

---

## 📚 BÀI 5: GITHUB ACTIONS CI/CD

### 5.1 Workflow Components

```
┌─────────────────────────────────────────────────────────────────┐
│              GITHUB ACTIONS ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Workflow (.github/workflows/ci.yml)                            │
│  │                                                               │
│  ├── on: push/pull_request/schedule                             │
│  │                                                               │
│  ├── jobs:                                                       │
│  │   │                                                           │
│  │   ├── build:                                                  │
│  │   │   ├── runs-on: ubuntu-latest                             │
│  │   │   ├── steps:                                             │
│  │   │   │   ├── checkout                                       │
│  │   │   │   ├── setup-java                                     │
│  │   │   │   └── run: ./gradlew build                           │
│  │   │   └── outputs: artifact path                             │
│  │   │                                                           │
│  │   └── test:                                                   │
│  │       ├── needs: build                                       │
│  │       └── steps: ...                                         │
│                                                                  │
│  Key Concepts:                                                   │
│  - Workflow: Automated process                                   │
│  - Job: Set of steps                                             │
│  - Step: Individual task                                         │
│  - Action: Reusable step                                         │
│  - Runner: Machine executing workflow                            │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Example: Spring Boot CI Pipeline

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  JAVA_VERSION: '17'
  GRADLE_VERSION: '8.5'

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Setup Java
      uses: actions/setup-java@v4
      with:
        distribution: 'temurin'
        java-version: ${{ env.JAVA_VERSION }}
        cache: 'gradle'

    - name: Setup Gradle
      uses: gradle/gradle-build-action@v3

    - name: Build with Gradle
      run: ./gradlew build -x test

    - name: Upload build artifacts
      uses: actions/upload-artifact@v4
      with:
        name: build-libs
        path: build/libs/

  test:
    runs-on: ubuntu-latest
    needs: build

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Setup Java
      uses: actions/setup-java@v4
      with:
        distribution: 'temurin'
        java-version: ${{ env.JAVA_VERSION }}
        cache: 'gradle'

    - name: Run unit tests
      run: ./gradlew test

    - name: Upload test results
      uses: actions/upload-artifact@v4
      if: always()
      with:
        name: test-results
        path: build/test-results/

    - name: Upload coverage report
      uses: actions/upload-artifact@v4
      if: always()
      with:
        name: coverage-report
        path: build/reports/jacoco/

  code-quality:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Setup Java
      uses: actions/setup-java@v4
      with:
        distribution: 'temurin'
        java-version: ${{ env.JAVA_VERSION }}
        cache: 'gradle'

    - name: Run code quality checks
      run: ./gradlew checkstyleMain checkstyleTest spotbugsMain

    - name: Upload checkstyle report
      uses: actions/upload-artifact@v4
      if: always()
      with:
        name: checkstyle-report
        path: build/reports/checkstyle/

  security-scan:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Setup Java
      uses: actions/setup-java@v4
      with:
        distribution: 'temurin'
        java-version: ${{ env.JAVA_VERSION }}
        cache: 'gradle'

    - name: Run OWASP dependency check
      run: ./gradlew dependencyCheckAnalyze

    - name: Upload security report
      uses: actions/upload-artifact@v4
      if: always()
      with:
        name: security-report
        path: build/reports/dependency-check/
```

---

### 5.3 Example: CD Pipeline

```yaml
# .github/workflows/cd.yml
name: CD Pipeline

on:
  push:
    branches: [main]
    tags:
      - 'v*'

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  docker-build-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Login to Container Registry
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    - name: Build and push Docker image
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: |
          ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
        cache-from: type=gha
        cache_to: type=gha,mode=max

    - name: Generate SBOM
      uses: anchore/sbom-action@v0
      with:
        format: spdx-json
        output-file: sbom.spdx.json

    - name: Upload SBOM
      uses: actions/upload-artifact@v4
      with:
        name: sbom
        path: sbom.spdx.json

  deploy-staging:
    needs: docker-build-push
    runs-on: ubuntu-latest
    environment: staging

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Setup kubectl
      uses: azure/setup-kubectl@v3

    - name: Configure kubeconfig
      run: |
        mkdir -p ~/.kube
        echo "${{ secrets.KUBECONFIG_STAGING }}" | base64 -d > ~/.kube/config

    - name: Deploy to staging
      run: |
        kubectl set image deployment/order-service \
          order-service=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
          -n staging
        kubectl rollout status deployment/order-service -n staging

    - name: Run smoke tests
      run: |
        curl -f http://staging.example.com/actuator/health || exit 1

  deploy-production:
    needs: [docker-build-push, deploy-staging]
    runs-on: ubuntu-latest
    environment: production

    if: startsWith(github.ref, 'refs/tags/v')

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Setup kubectl
      uses: azure/setup-kubectl@v3

    - name: Configure kubeconfig
      run: |
        echo "${{ secrets.KUBECONFIG_PROD }}" | base64 -d > ~/.kube/config

    - name: Deploy to production
      run: |
        kubectl set image deployment/order-service \
          order-service=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.ref_name }} \
          -n production
        kubectl rollout status deployment/order-service -n production --timeout=300s
```

---

## 📚 BÀI 6: CODE REVIEW BEST PRACTICES

### 6.1 Pull Request Template

```markdown
<!-- .github/PULL_REQUEST_TEMPLATE.md -->

## Description
<!-- Describe what changes were made and why -->

## Type of change
- [ ] 🐛 Bug fix (non-breaking change)
- [ ] ✨ New feature (non-breaking change)
- [ ] 💥 Breaking change (requires migration)
- [ ] 📝 Documentation update
- [ ] 🧹 Code cleanup/refactoring

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing performed

## Checklist
- [ ] Code follows project guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated (if needed)
- [ ] No new warnings introduced

## Related Issues
Fixes #123
Related to #456

## Screenshots (if applicable)
<!-- Add screenshots for UI changes -->

## Deployment Notes
<!-- Any special deployment considerations -->
```

### 6.2 Code Review Guidelines

```
┌─────────────────────────────────────────────────────────────────┐
│              CODE REVIEW CHECKLIST                               │
├─────────────────────────────────────────────────────────────────┤
│  ✅ Functionality:                                              │
│     - Does it work as intended?                                 │
│     - Edge cases handled?                                       │
│     - Error handling adequate?                                  │
│                                                                  │
│  ✅ Code Quality:                                               │
│     - Follows coding standards                                  │
│     - DRY (no duplication)                                      │
│     - Clear variable/method names                               │
│     - Methods do one thing                                      │
│                                                                  │
│  ✅ Testing:                                                    │
│     - Tests cover happy path                                    │
│     - Tests cover edge cases                                    │
│     - Tests are meaningful (not just for coverage)             │
│                                                                  │
│  ✅ Security:                                                   │
│     - No hardcoded credentials                                  │
│     - Input validation                                          │
│     - SQL injection prevention                                  │
│     - XSS prevention                                            │
│                                                                  │
│  ✅ Performance:                                                │
│     - No obvious inefficiencies                                 │
│     - Database queries optimized                                │
│     - Caching used appropriately                                │
│                                                                  │
│  ✅ Documentation:                                              │
│     - README updated                                            │
│     - API docs updated                                          │
│     - Complex logic commented                                   │
└─────────────────────────────────────────────────────────────────┘
```

### 6.3 Review Feedback Examples

```
❌ Bad feedback:
"Fix this"
"This is wrong"
"Why did you do it this way?"

✅ Good feedback:
"Consider using Optional.orElseThrow() here for clearer intent."

"Line 45: This could cause NPE if user is null.
Suggestion: return user.map(User::getName).orElse("Guest")"

"I notice we're creating a new ArrayList here. Could we use
Collections.emptyList() instead to avoid unnecessary allocation?"

"🤔 Curious why we chose HashMap over ConcurrentHashMap here?
Is this accessed by multiple threads?"
```

---

## 📚 TÓM TẮT PHASE 06.7

1. ✅ Git internals (blobs, trees, commits, refs)
2. ✅ Branching strategies (Git Flow, GitHub Flow, Trunk-Based)
3. ✅ Rebase vs Merge - when to use each
4. ✅ Git hooks for automation
5. ✅ GitHub Actions CI/CD pipelines
6. ✅ Code review best practices

---

## 🔜 TIẾP THEO

Xem `02-examples.md` để xem ví dụ thực tế!
