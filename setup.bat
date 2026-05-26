@echo off
REM Setup script for POC API - Installs Maven and builds the project

setlocal enabledelayedexpansion

echo ========================================
echo POC API - Setup Script
echo ========================================
echo.

REM Check if Java is installed
java -version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Java is not installed or not in PATH
    echo Please install JDK 21 or later and add it to PATH
    pause
    exit /b 1
)

echo [OK] Java is installed
java -version
echo.

REM Check if Maven is installed
mvn --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Maven is not installed in PATH
    echo.
    echo To install Maven:
    echo 1. Download from: https://maven.apache.org/download.cgi
    echo 2. Extract to: C:\Maven (or your preference)
    echo 3. Add to PATH: C:\Maven\bin
    echo 4. Run 'mvn --version' to verify
    echo.
    pause
    exit /b 1
)

echo [OK] Maven is installed
mvn --version
echo.

REM Build the project
echo ========================================
echo Building POC API Project...
echo ========================================
echo.
mvn clean install -DskipTests

if errorlevel 1 (
    echo.
    echo ERROR: Build failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo [SUCCESS] Build completed!
echo ========================================
echo.
echo To run the application:
echo   mvn spring-boot:run
echo.
echo To run tests:
echo   mvn test
echo.
pause
