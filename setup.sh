#!/bin/bash
# Setup script for POC API - Installs Maven and builds the project

echo "========================================"
echo "POC API - Setup Script"
echo "========================================"
echo

# Check if Java is installed
if ! command -v java &> /dev/null; then
    echo "ERROR: Java is not installed or not in PATH"
    echo "Please install JDK 21 or later"
    exit 1
fi

echo "[OK] Java is installed"
java -version
echo

# Check if Maven is installed
if ! command -v mvn &> /dev/null; then
    echo "[WARNING] Maven is not installed in PATH"
    echo
    echo "To install Maven:"
    echo "1. Download from: https://maven.apache.org/download.cgi"
    echo "2. Extract to: /opt/maven (or your preference)"
    echo "3. Add to PATH: export PATH=\$PATH:/opt/maven/bin"
    echo "4. Run 'mvn --version' to verify"
    echo
    exit 1
fi

echo "[OK] Maven is installed"
mvn --version
echo

# Build the project
echo "========================================"
echo "Building POC API Project..."
echo "========================================"
echo
mvn clean install -DskipTests

if [ $? -ne 0 ]; then
    echo
    echo "ERROR: Build failed"
    exit 1
fi

echo
echo "========================================"
echo "[SUCCESS] Build completed!"
echo "========================================"
echo
echo "To run the application:"
echo "  mvn spring-boot:run"
echo
echo "To run tests:"
echo "  mvn test"
echo
