# 1. Create LICENSE (MIT)
cat << 'LICENSE_EOF' > LICENSE
MIT License

Copyright (c) 2026 TheDevErfan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
LICENSE_EOF

# 2. Create CONTRIBUTING.md
cat << 'CONTRIB_EOF' > CONTRIBUTING.md
# Contributing to Navix

First off, thank you for taking the time to contribute! ❤️

## How to Contribute
1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.
CONTRIB_EOF

# 3. Create CHANGELOG.md
cat << 'CHANGE_EOF' > CHANGELOG.md
# Changelog

All notable changes to this project will be documented in this file.

## [1.0.6] - 2026-03-30
- Initial public release of Navix framework.
- Added modular router architecture and FSM support.
- Included 10,000+ automated example patterns.
CHANGE_EOF

# 4. Create GitHub Actions Workflow for CI
mkdir -p .github/workflows
cat << 'CI_EOF' > .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt || true
    - name: Run lint or basic checks
      run: |
        python -c "import navix; print('Navix imported successfully')"
CI_EOF

# 5. Create Issue Templates
mkdir -p .github/ISSUE_TEMPLATE
cat << 'BUG_EOF' > .github/ISSUE_TEMPLATE/bug_report.md
---
name: Bug report
about: Create a report to help us improve Navix
title: ''
labels: bug
assignees: ''
---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. See error
BUG_EOF

cat << 'FEAT_EOF' > .github/ISSUE_TEMPLATE/feature_request.md
---
name: Feature request
about: Sugges

cat << 'EOF' > setup_enterprise.sh
# 1. Create LICENSE (MIT)
cat << 'LICENSE_EOF' > LICENSE
MIT License

Copyright (c) 2026 TheDevErfan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
LICENSE_EOF

# 2. Create CONTRIBUTING.md
cat << 'CONTRIB_EOF' > CONTRIBUTING.md
# Contributing to Navix

First off, thank you for taking the time to contribute! ❤️

## How to Contribute
1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.
CONTRIB_EOF

# 3. Create CHANGELOG.md
cat << 'CHANGE_EOF' > CHANGELOG.md
# Changelog

All notable changes to this project will be documented in this file.

## [1.0.6] - 2026-03-30
- Initial public release of Navix framework.
- Added modular router architecture and FSM support.
- Included 10,000+ automated example patterns.
CHANGE_EOF

# 4. Create GitHub Actions Workflow for CI
mkdir -p .github/workflows
cat << 'CI_EOF' > .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt || true
    - name: Run lint or basic checks
      run: |
        python -c "import navix; print('Navix imported successfully')"
CI_EOF

# 5. Create Issue Templates
mkdir -p .github/ISSUE_TEMPLATE
cat << 'BUG_EOF' > .github/ISSUE_TEMPLATE/bug_report.md
---
name: Bug report
about: Create a report to help us improve Navix
title: ''
labels: bug
assignees: ''
---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. See error
BUG_EOF

cat << 'FEAT_EOF' > .github/ISSUE_TEMPLATE/feature_request.md
---
name: Feature request
about: Suggest an idea for Navix
title: ''
labels: enhancement
assignees: ''
---

**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is.

**Describe the solution you'd like**
A clear and concise description of what you want to happen.
FEAT_EOF

echo "Enterprise structure generated successfully!"
