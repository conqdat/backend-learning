# Phase 06.7: Git & GitHub - Ví Dụ Thực Tế

---

## 📁 BÀI 1: GIT COMMANDS NÂNG CAO

### Ví dụ 1.1: Debug với Git

```bash
# Xem lịch sử commit với graph
git log --oneline --graph --all --decorate

# Xem ai đã sửa file nào, khi nào
git blame -L 10,20 src/main/java/UserService.java

# Xem thay đổi giữa 2 commits
git diff abc123 def456

# Xem thay đổi của một file cụ thể
git diff HEAD~1 src/main/java/UserService.java

# Tìm commit làm file bị thay đổi
git log -p --follow -S "methodName" -- src/main/java/UserService.java

# Xem file ở version cũ
git show abc123:src/main/java/UserService.java

# Phục hồi file về version cũ
git checkout abc123 -- src/main/java/UserService.java

# Tìm commit gây bug (binary search)
git bisect start
git bisect bad HEAD          # Current version has bug
git bisect good v1.0.0       # Old version works
# Git sẽ checkout các commits trung gian, test và báo good/bad
git bisect reset             # Finish
```

### Ví dụ 1.2: Fix mistakes

```bash
# Undo last commit, keep changes
git reset --soft HEAD~1

# Undo last commit, discard changes
git reset --hard HEAD~1

# Amend last commit (add more changes)
git add forgotten-file.txt
git commit --amend --no-edit

# Revert a commit (create new commit that undoes)
git revert abc123

# Recover deleted branch
git reflog
git checkout -b recovered-branch abc123

# Recover lost commit after reset
git reflog
git reset --hard HEAD@{1}

# Stash changes
git stash                    # Save changes
git stash list               # List stashes
git stash pop                # Apply and remove
git stash apply stash@{1}    # Apply specific stash
git stash drop stash@{1}     # Delete specific stash

# Stash with message
git stash push -m "WIP: login feature"
```

### Ví dụ 1.3: Rewrite history

```bash
# Interactive rebase
git rebase -i HEAD~5

# Editor opens:
# pick  a1b2c3d  feat: Add user registration
# pick  d4e5f6g  fix: Fix validation bug
# pick  h7i8j9k  test: Add unit tests
# pick  l1m2n3o  docs: Update README
# pick  p4q5r6s  refactor: Clean up code

# Commands:
# p, pick = use commit
# r, reword = use commit, but edit message
# e, edit = use commit, but stop for amending
# s, squash = use commit, but meld into previous
# f, fixup = like squash, but discard message
# d, drop = remove commit

# Squash commits into one
git rebase -i HEAD~3
# Change pick → squash for commits 2 and 3

# Split a commit into multiple
git rebase -i abc123
# Change pick → edit for the commit to split
git reset HEAD~1
# Stage and commit changes separately
git add file1.txt
git commit -m "First part"
git add file2.txt
git commit -m "Second part"
git rebase --continue
```

---

## 📁 BÀI 2: GITHUB WORKFLOWS

### Ví dụ 2.1: PR Review Workflow

```yaml
# .github/workflows/pr-review.yml
name: PR Review Automation

on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]

jobs:
  auto-label:
    runs-on: ubuntu-latest
    steps:
    - name: Auto-label PRs
      uses: actions/labeler@v5
      with:
        repo-token: "${{ secrets.GITHUB_TOKEN }}"

    - name: Add size label
      uses: codelytv/pr-size-labeler@v1
      with:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        xs_max_size: '10'
        s_max_size: '100'
        m_max_size: '500'
        l_max_size: '1000'

  check-list:
    runs-on: ubuntu-latest
    steps:
    - name: Check PR has description
      uses: actions/github-script@v7
      with:
        script: |
          const pr = context.payload.pull_request;
          if (!pr.body || pr.body.trim() === '') {
            core.setFailed('PR description is empty!');
          }

    - name: Check PR has assignee
      uses: actions/github-script@v7
      with:
        script: |
          const pr = context.payload.pull_request;
          if (!pr.assignee && !pr.assignees.length) {
            core.setFailed('PR has no assignee!');
          }

  notify-team:
    runs-on: ubuntu-latest
    if: github.event.action == 'opened'
    steps:
    - name: Notify on Slack
      uses: slackapi/slack-github-action@v1
      with:
        payload: |
          {
            "text": "New PR: ${{ github.event.pull_request.title }}",
            "blocks": [
              {
                "type": "section",
                "text": {
                  "type": "mrkdwn",
                  "text": "*New PR: ${{ github.event.pull_request.title }}*\nAuthor: ${{ github.event.pull_request.user.login }}\n${{ github.event.pull_request.html_url }}"
                }
              }
            ]
          }
      env:
        SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

### Ví dụ 2.2: Auto-merge Bot

```yaml
# .github/workflows/auto-merge.yml
name: Auto-merge Dependabot

on:
  pull_request:
    branches: [main]

jobs:
  auto-merge:
    runs-on: ubuntu-latest
    if: github.actor == 'dependabot[bot]'
    steps:
    - name: Enable auto-merge
      run: gh pr merge --auto --squash "$PR_URL"
      env:
        PR_URL: ${{ github.event.pull_request.html_url }}
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

    - name: Approve PR
      run: gh pr review --approve "$PR_URL"
      env:
        PR_URL: ${{ github.event.pull_request.html_url }}
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## 📁 BÀI 3: DEPENDABOT CONFIG

```yaml
# .github/dependabot.yml
version: 2
updates:
  # Java dependencies
  - package-ecosystem: "gradle"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "09:00"
      timezone: "Asia/Ho_Chi_Minh"
    open-pull-requests-limit: 10
    labels:
      - "dependencies"
      - "java"
    reviewers:
      - "backend-team"
    commit-message:
      prefix: "chore(deps)"

  # GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    labels:
      - "dependencies"
      - "ci"
    commit-message:
      prefix: "chore(ci)"

  # Docker
  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"
    labels:
      - "dependencies"
      - "docker"
```

---

## 📁 BÀI 4: GITHUB LABELER

```yaml
# .github/labeler.yml
# Auto-label PRs based on file paths

backend:
  - changed-files:
    - any-glob-to-any-file: 'src/main/java/**/*'
    - any-glob-to-any-file: 'src/main/resources/**/*'

frontend:
  - changed-files:
    - any-glob-to-any-file: 'src/main/webapp/**/*'
    - any-glob-to-any-file: 'src/main/javascript/**/*'

database:
  - changed-files:
    - any-glob-to-any-file: 'src/main/resources/db/**/*'
    - any-glob-to-any-file: '**/*.sql'

documentation:
  - changed-files:
    - any-glob-to-any-file: '**/*.md'
    - any-glob-to-any-file: 'docs/**/*'

configuration:
  - changed-files:
    - any-glob-to-any-file: '**/*.yml'
    - any-glob-to-any-file: '**/*.yaml'
    - any-glob-to-any-file: '**/*.properties'

tests:
  - changed-files:
    - any-glob-to-any-file: 'src/test/**/*'

security:
  - changed-files:
    - any-glob-to-any-file: 'src/main/java/**/security/**/*'
    - any-glob-to-any-file: '**/pom.xml'
    - any-glob-to-any-file: '**/build.gradle'
```

---

## 📁 BÀI 5: CODE QUALITY AUTOMATION

### Ví dụ 5.1: SonarQube Integration

```yaml
# .github/workflows/sonarqube.yml
name: SonarQube Analysis

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  sonarqube:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      with:
        fetch-depth: 0  # Shallow clones should be disabled

    - name: Setup Java
      uses: actions/setup-java@v4
      with:
        distribution: 'temurin'
        java-version: '17'
        cache: 'gradle'

    - name: Build and analyze
      run: |
        ./gradlew build sonarqube \
          -Dsonar.projectKey=my-project \
          -Dsonar.host.url=${{ secrets.SONAR_HOST_URL }} \
          -Dsonar.token=${{ secrets.SONAR_TOKEN }}

    - name: Check quality gate
      uses: sonarsource/sonarqube-quality-gate-action@master
      with:
        timeout: 5
      env:
        SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
        SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
```

### Ví dụ 5.2: Code Coverage Enforcement

```yaml
# .github/workflows/coverage.yml
name: Code Coverage Check

on:
  pull_request:
    branches: [main]

jobs:
  coverage:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Setup Java
      uses: actions/setup-java@v4
      with:
        distribution: 'temurin'
        java-version: '17'
        cache: 'gradle'

    - name: Run tests with coverage
      run: ./gradlew test jacocoTestReport

    - name: Enforce coverage
      uses: madrapps/jacoco-report@v1.6.1
      with:
        paths: ${{ github.workspace }}/build/reports/jacoco/test/jacocoTestReport.xml
        token: ${{ secrets.GITHUB_TOKEN }}
        min-coverage-overall: 80
        min-coverage-changed-files: 80
        title: 'Code Coverage Report'
        update-comment: true
```

---

## 📁 BÀI 6: RELEASE AUTOMATION

### Ví dụ 6.1: Conventional Commits Release

```yaml
# .github/workflows/release.yml
name: Automated Releases

on:
  push:
    branches: [main]

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      issues: write
      pull-requests: write

    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      with:
        fetch-depth: 0

    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20'

    - name: Install semantic-release
      run: npm install -g semantic-release @semantic-release/git @semantic-release/changelog

    - name: Run semantic-release
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      run: npx semantic-release
```

```json
// .releaserc.json
{
  "branches": ["main"],
  "plugins": [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    [
      "@semantic-release/changelog",
      {
        "changelogFile": "CHANGELOG.md"
      }
    ],
    [
      "@semantic-release/git",
      {
        "assets": ["CHANGELOG.md", "pom.xml"],
        "message": "chore(release): ${nextRelease.version} [skip ci]"
      }
    ],
    "@semantic-release/github"
  ]
}
```

### Ví dụ 6.2: Manual Release with Approval

```yaml
# .github/workflows/manual-release.yml
name: Manual Release

on:
  workflow_dispatch:
    inputs:
      version_type:
        description: 'Version type (patch/minor/major)'
        required: true
        default: 'patch'
        type: choice
        options:
          - patch
          - minor
          - major

jobs:
  create-release:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      with:
        fetch-depth: 0

    - name: Setup Git config
      run: |
        git config user.name "GitHub Actions"
        git config user.email "actions@github.com"

    - name: Bump version
      run: |
        VERSION_TYPE=${{ github.event.inputs.version_type }}
        CURRENT_VERSION=$(grep "^version=" gradle.properties | cut -d'=' -f2)

        if [ "$VERSION_TYPE" == "major" ]; then
          NEW_VERSION=$(echo $CURRENT_VERSION | awk -F. '{print ($1+1)".0.0"}')
        elif [ "$VERSION_TYPE" == "minor" ]; then
          NEW_VERSION=$(echo $CURRENT_VERSION | awk -F. '{print $1"."($2+1)".0"}')
        else
          NEW_VERSION=$(echo $CURRENT_VERSION | awk -F. '{print $1"."$2"."($3+1)}')
        fi

        sed -i "s/^version=.*/version=$NEW_VERSION/" gradle.properties
        echo "NEW_VERSION=$NEW_VERSION" >> $GITHUB_ENV

    - name: Create release commit
      run: |
        git add gradle.properties
        git commit -m "chore(release): v${{ env.NEW_VERSION }}"
        git tag "v${{ env.NEW_VERSION }}"
        git push origin main --tags

    - name: Create GitHub Release
      uses: actions/create-release@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        tag_name: "v${{ env.NEW_VERSION }}"
        release_name: "Release v${{ env.NEW_VERSION }}"
        draft: false
        prerelease: false
        generate_release_notes: true
```

---

## 📁 BÀI 7: MONOREPO VỚI NX

### Ví dụ 7.1: NX Workspace Setup

```bash
# Create NX workspace
npx create-nx-workspace@latest backend-monorepo \
  --preset=gradle \
  --name=backend-services \
  --nxCloud=skip

# Structure:
# backend-monorepo/
# ├── apps/
# │   ├── user-service/
# │   ├── order-service/
# │   └── payment-service/
# ├── libs/
# │   ├── common-utils/
# │   ├── database/
# │   └── security/
# ├── tools/
# └── nx.json
```

### Ví dụ 7.2: Affected Commands

```bash
# Run tests only for affected projects
nx affected --target=test --base=origin/main

# Build affected projects
nx affected --target=build --base=origin/main

# Lint affected projects
nx affected --target=lint --base=origin/main

# See what projects are affected by changes
nx affected:graph --base=origin/main

# Run commands for specific project
nx test order-service
nx build user-service

# Run commands with parallelism
nx run-many --target=test --all --parallel=4
```

### Ví dụ 7.3: CI with NX

```yaml
# .github/workflows/ci-monorepo.yml
name: CI Monorepo

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  detect-changes:
    runs-on: ubuntu-latest
    outputs:
      user-service: ${{ steps.changes.outputs.user-service }}
      order-service: ${{ steps.changes.outputs.order-service }}
      payment-service: ${{ steps.changes.outputs.payment-service }}
    steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0

    - uses: dorny/paths-filter@v3
      id: changes
      with:
        filters: |
          user-service:
            - 'apps/user-service/**'
            - 'libs/common-utils/**'
            - 'libs/database/**'
          order-service:
            - 'apps/order-service/**'
            - 'libs/common-utils/**'
            - 'libs/database/**'
          payment-service:
            - 'apps/payment-service/**'
            - 'libs/common-utils/**'
            - 'libs/security/**'

  test-user-service:
    needs: detect-changes
    if: ${{ needs.detect-changes.outputs.user-service == 'true' }}
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-java@v4
      with:
        distribution: 'temurin'
        java-version: '17'
        cache: 'gradle'
    - run: ./gradlew :apps:user-service:test

  test-order-service:
    needs: detect-changes
    if: ${{ needs.detect-changes.outputs.order-service == 'true' }}
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-java@v4
      with:
        distribution: 'temurin'
        java-version: '17'
        cache: 'gradle'
    - run: ./gradlew :apps:order-service:test
```

---

## 🔗 TÀI LIỆU THAM KHẢO

1. [Pro Git Book](https://git-scm.com/book/en/v2)
2. [GitHub Actions Documentation](https://docs.github.com/en/actions)
3. [Conventional Commits](https://www.conventionalcommits.org/)
4. [NX Documentation](https://nx.dev/)
