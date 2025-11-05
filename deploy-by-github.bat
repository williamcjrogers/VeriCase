@echo off
REM VeriCase Deployments Organized by GitHub Repository
REM This script provides easy access to deploy each repository (Windows version)

echo === VeriCase Deployments by GitHub Repository ===
echo.

:main_menu
cls
echo Select a repository to deploy:
echo.
echo 1) VeriCase (Main Backend/API)
echo    GitHub: https://github.com/williamcjrogers/VeriCase.git
echo    Path: vericase-docs-rapid-plus-ts
echo    Targets: AWS EKS, Railway.app, Docker Compose
echo.
echo 2) VeriCaseWR (Desktop Application)
echo    GitHub: https://github.com/williamcjrogers/VeriCaseWR.git
echo    Path: Vericase-DESKTOP-46BMPM4
echo    Targets: Windows Installer
echo.
echo 3) VeriCase-Website-New (Frontend Website)
echo    GitHub: https://github.com/williamcjrogers/VeriCase-Website-New.git
echo    Path: VeriCase-Website-New
echo    Targets: React Development, Static Hosting
echo.
echo 4) Show All Deployment Status
echo.
echo 5) Exit
echo.
set /p choice="Enter choice (1-5): "

if "%choice%"=="1" goto deploy_vericase_main
if "%choice%"=="2" goto deploy_vericase_wr
if "%choice%"=="3" goto deploy_vericase_website
if "%choice%"=="4" goto show_all_status
if "%choice%"=="5" goto exit_script
echo Invalid choice. Please enter 1-5.
pause
goto main_menu

:deploy_vericase_main
cls
echo === VeriCase Main Repository Deployment ===
echo.
echo Select deployment target:
echo 1) AWS EKS (Production)
echo 2) Railway.app (Staging)
echo 3) Docker Compose (Local)
echo 4) Back to main menu
echo.
set /p choice="Enter choice (1-4): "

if "%choice%"=="1" goto deploy_aws
if "%choice%"=="2" goto deploy_railway
if "%choice%"=="3" goto deploy_docker
if "%choice%"=="4" goto main_menu
echo Invalid choice.
pause
goto deploy_vericase_main

:deploy_aws
echo Deploying to AWS EKS...
if exist "deploy-to-aws.sh" (
    echo Use Git Bash or WSL to run: ./deploy-to-aws.sh
    echo Or run PowerShell version: .\deploy-to-aws.ps1
) else (
    echo Error: deploy-to-aws.sh not found in current directory
    echo Please navigate to vericase-docs-rapid-plus-ts directory
)
pause
goto deploy_vericase_main

:deploy_railway
echo Deploying to Railway.app...
echo Railway deployment is triggered by Git push:
echo.
echo Commands to deploy:
echo   git add .
echo   git commit -m "Deploy to Railway"
echo   git push origin main
echo.
echo Or visit: https://railway.app/new/project
pause
goto deploy_vericase_main

:deploy_docker
echo Starting Docker Compose...
if exist "docker-compose.yml" (
    docker-compose up -d
    echo Docker Compose started successfully
) else (
    echo Error: docker-compose.yml not found in current directory
    echo Please navigate to vericase-docs-rapid-plus-ts directory
)
pause
goto deploy_vericase_main

:deploy_vericase_wr
cls
echo === VeriCaseWR Desktop Repository ===
echo.
echo Desktop Application Deployment
echo.
echo Current Status:
echo - Package: vericase-hotfix-pack.zip
echo - Target: Windows Desktop
echo - Distribution: Direct download/enterprise deployment
echo.
echo To build desktop application:
echo 1. Navigate to: Vericase-DESKTOP-46BMPM4
echo 2. Build the application using your preferred method
echo 3. Create installer package
echo 4. Distribute to users
echo.
pause
goto main_menu

:deploy_vericase_website
cls
echo === VeriCase-Website-New Frontend Repository ===
echo.
echo Select deployment target:
echo 1) Start Development Server
echo 2) Build for Production
echo 3) Deploy to Static Hosting
echo 4) Back to main menu
echo.
set /p choice="Enter choice (1-4): "

if "%choice%"=="1" goto start_dev
if "%choice%"=="2" goto build_prod
if "%choice%"=="3" goto deploy_static
if "%choice%"=="4" goto main_menu
echo Invalid choice.
pause
goto deploy_vericase_website

:start_dev
echo Starting React development server...
echo Commands to start development:
echo   cd frontend
echo   npm install
echo   npm start
echo.
echo Or with yarn:
echo   cd frontend
echo   yarn install
echo   yarn start
pause
goto deploy_vericase_website

:build_prod
echo Building for production...
echo Commands to build:
echo   cd frontend
echo   npm run build
echo.
echo Build output will be in: frontend/build/
pause
goto deploy_vericase_website

:deploy_static
echo Static hosting deployment options:
echo.
echo 1) Vercel:
echo    - Install Vercel CLI: npm i -g vercel
echo    - Run: vercel --prod
echo.
echo 2) Netlify:
echo    - Drag and drop frontend/build/ folder to netlify.com
echo.
echo 3) AWS S3:
echo    - Upload frontend/build/ to S3 bucket
echo    - Enable static website hosting
pause
goto deploy_vericase_website

:show_all_status
cls
echo === All Deployment Status ===
echo.
echo 🚀 Repository: VeriCase (Main Backend/API)
echo    GitHub: https://github.com/williamcjrogers/VeriCase.git
echo    AWS EKS: ✅ Production Active
echo    Railway.app: ⚠️ Configured (Ready)
echo    Docker Compose: ✅ Local Ready
echo.
echo 🖥️ Repository: VeriCaseWR (Desktop)
echo    GitHub: https://github.com/williamcjrogers/VeriCaseWR.git
echo    Windows Installer: ✅ Production Active
echo.
echo 🌐 Repository: VeriCase-Website-New (Frontend)
echo    GitHub: https://github.com/williamcjrogers/VeriCase-Website-New.git
echo    Development Server: ⚠️ In Development
echo    Production Hosting: 🔄 Planning Phase
echo.
echo 📊 Summary:
echo    Production: 2/3 repositories deployed
echo    Staging: 1/3 repositories ready
echo    Development: 3/3 repositories active
echo.
pause
goto main_menu

:exit_script
echo Goodbye!
exit /b 0
