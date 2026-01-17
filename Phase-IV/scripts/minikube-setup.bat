@echo off
REM Phase IV: Windows Minikube Setup Script
REM Sets up a local Kubernetes cluster with required addons

echo ==========================================
echo Phase IV: Minikube Cluster Setup (Windows)
echo ==========================================

REM Check if minikube is installed
minikube version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: minikube is not installed.
    echo Install from: https://minikube.sigs.k8s.io/docs/start/
    exit /b 1
)

REM Check if kubectl is installed
kubectl version --client >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: kubectl is not installed.
    echo Install from: https://kubernetes.io/docs/tasks/tools/
    exit /b 1
)

REM Check if Docker is running
docker info >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Docker is not running.
    echo Please start Docker Desktop and try again.
    exit /b 1
)

echo.
echo Step 1: Starting Minikube cluster...
echo ----------------------------------------

minikube start --cpus=4 --memory=8192 --disk-size=20gb --driver=docker

echo.
echo Step 2: Enabling required addons...
echo ----------------------------------------

minikube addons enable ingress
echo   - Ingress controller enabled

minikube addons enable metrics-server
echo   - Metrics server enabled

minikube addons enable dashboard
echo   - Dashboard enabled

echo.
echo Step 3: Cluster Information
echo ----------------------------------------

minikube status

echo.
echo ==========================================
echo Minikube cluster is ready!
echo ==========================================
echo.
echo Next steps:
echo   1. Run: deploy-local.bat
echo   2. Access dashboard: minikube dashboard
echo.

pause
