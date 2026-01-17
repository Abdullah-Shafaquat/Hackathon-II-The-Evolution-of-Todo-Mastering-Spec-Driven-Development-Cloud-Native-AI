@echo off
REM Phase IV: Windows Deployment Script
REM Deploys the Todo Chatbot to Minikube using Helm

echo ==========================================
echo Phase IV: Deploying to Minikube (Windows)
echo ==========================================

REM Check if minikube is running
minikube status >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Minikube is not running.
    echo Run: minikube start --cpus=4 --memory=8192
    exit /b 1
)

REM Check if helm is installed
helm version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: helm is not installed.
    echo Install from: https://helm.sh/docs/intro/install/
    exit /b 1
)

echo.
echo Step 1: Setting Docker environment...
echo ----------------------------------------

REM Configure Docker to use Minikube's daemon
@FOR /f "tokens=*" %%i IN ('minikube docker-env --shell cmd') DO @%%i

echo.
echo Step 2: Building Docker images...
echo ----------------------------------------

cd backend
docker build -t todo-chatbot-backend:latest -f Dockerfile .
cd ..

cd frontend
docker build -t todo-chatbot-frontend:latest --build-arg NEXT_PUBLIC_API_URL=http://backend-service:8000 -f Dockerfile .
cd ..

echo.
echo Step 3: Deploying with Helm...
echo ----------------------------------------

helm upgrade --install todo-chatbot ./charts/todo-chatbot -f ./charts/todo-chatbot/values.local.yaml --namespace todo-app --create-namespace --wait --timeout 5m

echo.
echo Step 4: Checking deployment status...
echo ----------------------------------------

kubectl get pods -n todo-app
kubectl get svc -n todo-app

echo.
echo ==========================================
echo Deployment completed!
echo ==========================================
echo.
echo Access the application:
echo   minikube service todo-chatbot-frontend -n todo-app
echo.
echo Or get the URL:
echo   minikube service todo-chatbot-frontend -n todo-app --url
echo.

pause
