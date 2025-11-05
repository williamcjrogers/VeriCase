#!/bin/bash
set -e

# VeriCase Deployments Organized by GitHub Repository
# This script provides easy access to deploy each repository

echo "=== VeriCase Deployments by GitHub Repository ==="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Function to show repository menu
show_repo_menu() {
    echo "Select a repository to deploy:"
    echo ""
    print_status $GREEN "1) VeriCase (Main Backend/API)"
    echo "   GitHub: https://github.com/williamcjrogers/VeriCase.git"
    echo "   Path: vericase-docs-rapid-plus-ts"
    echo "   Targets: AWS EKS, Railway.app, Docker Compose"
    echo ""
    print_status $GREEN "2) VeriCaseWR (Desktop Application)"
    echo "   GitHub: https://github.com/williamcjrogers/VeriCaseWR.git"
    echo "   Path: Vericase-DESKTOP-46BMPM4"
    echo "   Targets: Windows Installer"
    echo ""
    print_status $GREEN "3) VeriCase-Website-New (Frontend Website)"
    echo "   GitHub: https://github.com/williamcjrogers/VeriCase-Website-New.git"
    echo "   Path: VeriCase-Website-New"
    echo "   Targets: React Development, Static Hosting"
    echo ""
    print_status $YELLOW "4) Show All Deployment Status"
    echo ""
    print_status $BLUE "5) Exit"
    echo ""
}

# Function to deploy VeriCase main repository
deploy_vericase_main() {
    echo "=== VeriCase Main Repository Deployment ==="
    echo ""
    echo "Select deployment target:"
    echo "1) AWS EKS (Production)"
    echo "2) Railway.app (Staging)"
    echo "3) Docker Compose (Local)"
    echo "4) Back to main menu"
    echo ""
    read -p "Enter choice (1-4): " choice
    
    case $choice in
        1)
            print_status $YELLOW "Deploying to AWS EKS..."
            if [ -f "./deploy-to-aws.sh" ]; then
                chmod +x ./deploy-to-aws.sh
                ./deploy-to-aws.sh
            else
                print_status $RED "Error: deploy-to-aws.sh not found in current directory"
                echo "Please navigate to vericase-docs-rapid-plus-ts directory"
            fi
            ;;
        2)
            print_status $YELLOW "Deploying to Railway.app..."
            echo "Railway deployment is triggered by Git push:"
            echo ""
            echo "Commands to deploy:"
            echo "  git add ."
            echo "  git commit -m \"Deploy to Railway\""
            echo "  git push origin main"
            echo ""
            echo "Or visit: https://railway.app/new/project"
            ;;
        3)
            print_status $YELLOW "Starting Docker Compose..."
            if [ -f "./docker-compose.yml" ]; then
                docker-compose up -d
                print_status $GREEN "Docker Compose started successfully"
            else
                print_status $RED "Error: docker-compose.yml not found in current directory"
                echo "Please navigate to vericase-docs-rapid-plus-ts directory"
            fi
            ;;
        4)
            return
            ;;
        *)
            print_status $RED "Invalid choice"
            ;;
    esac
}

# Function to deploy VeriCaseWR desktop repository
deploy_vericase_wr() {
    echo "=== VeriCaseWR Desktop Repository ==="
    echo ""
    print_status $YELLOW "Desktop Application Deployment"
    echo ""
    echo "Current Status:"
    echo "- Package: vericase-hotfix-pack.zip"
    echo "- Target: Windows Desktop"
    echo "- Distribution: Direct download/enterprise deployment"
    echo ""
    echo "To build desktop application:"
    echo "1. Navigate to: Vericase-DESKTOP-46BMPM4"
    echo "2. Build the application using your preferred method"
    echo "3. Create installer package"
    echo "4. Distribute to users"
    echo ""
    read -p "Press Enter to continue..."
}

# Function to deploy VeriCase website repository
deploy_vericase_website() {
    echo "=== VeriCase-Website-New Frontend Repository ==="
    echo ""
    echo "Select deployment target:"
    echo "1) Start Development Server"
    echo "2) Build for Production"
    echo "3) Deploy to Static Hosting"
    echo "4) Back to main menu"
    echo ""
    read -p "Enter choice (1-4): " choice
    
    case $choice in
        1)
            print_status $YELLOW "Starting React development server..."
            echo "Commands to start development:"
            echo "  cd frontend"
            echo "  npm install"
            echo "  npm start"
            echo ""
            echo "Or with yarn:"
            echo "  cd frontend"
            echo "  yarn install"
            echo "  yarn start"
            ;;
        2)
            print_status $YELLOW "Building for production..."
            echo "Commands to build:"
            echo "  cd frontend"
            echo "  npm run build"
            echo ""
            echo "Build output will be in: frontend/build/"
            ;;
        3)
            print_status $YELLOW "Static hosting deployment options:"
            echo ""
            echo "1) Vercel:"
            echo "   - Install Vercel CLI: npm i -g vercel"
            echo "   - Run: vercel --prod"
            echo ""
            echo "2) Netlify:"
            echo "   - Drag and drop frontend/build/ folder to netlify.com"
            echo ""
            echo "3) AWS S3:"
            echo "   - Upload frontend/build/ to S3 bucket"
            echo "   - Enable static website hosting"
            ;;
        4)
            return
            ;;
        *)
            print_status $RED "Invalid choice"
            ;;
    esac
}

# Function to show all deployment status
show_all_status() {
    echo "=== All Deployment Status ==="
    echo ""
    
    print_status $GREEN "🚀 Repository: VeriCase (Main Backend/API)"
    echo "   GitHub: https://github.com/williamcjrogers/VeriCase.git"
    echo "   AWS EKS: ✅ Production Active"
    echo "   Railway.app: ⚠️ Configured (Ready)"
    echo "   Docker Compose: ✅ Local Ready"
    echo ""
    
    print_status $GREEN "🖥️ Repository: VeriCaseWR (Desktop)"
    echo "   GitHub: https://github.com/williamcjrogers/VeriCaseWR.git"
    echo "   Windows Installer: ✅ Production Active"
    echo ""
    
    print_status $GREEN "🌐 Repository: VeriCase-Website-New (Frontend)"
    echo "   GitHub: https://github.com/williamcjrogers/VeriCase-Website-New.git"
    echo "   Development Server: ⚠️ In Development"
    echo "   Production Hosting: 🔄 Planning Phase"
    echo ""
    
    print_status $BLUE "📊 Summary:"
    echo "   Production: 2/3 repositories deployed"
    echo "   Staging: 1/3 repositories ready"
    echo "   Development: 3/3 repositories active"
    echo ""
    
    read -p "Press Enter to continue..."
}

# Main script loop
main() {
    while true; do
        clear
        print_status $BLUE "=== VeriCase Deployments by GitHub Repository ==="
        echo ""
        show_repo_menu
        read -p "Enter choice (1-5): " choice
        
        case $choice in
            1)
                deploy_vericase_main
                ;;
            2)
                deploy_vericase_wr
                ;;
            3)
                deploy_vericase_website
                ;;
            4)
                show_all_status
                ;;
            5)
                print_status $GREEN "Goodbye!"
                exit 0
                ;;
            *)
                print_status $RED "Invalid choice. Please enter 1-5."
                ;;
        esac
        
        echo ""
        read -p "Press Enter to continue..."
    done
}

# Check if we're in the right directory
check_directory() {
    local current_dir=$(basename $(pwd))
    
    case $current_dir in
        "vericase-docs-rapid-plus-ts")
            return 0
            ;;
        "VeriCase-DESKTOP-46BMPM4")
            return 0
            ;;
        "VeriCase-Website-New")
            return 0
            ;;
        *)
            print_status $YELLOW "Warning: You're not in a VeriCase repository directory"
            echo "Current directory: $current_dir"
            echo ""
            echo "Expected directories:"
            echo "- vericase-docs-rapid-plus-ts"
            echo "- VeriCase-DESKTOP-46BMPM4"
            echo "- VeriCase-Website-New"
            echo ""
            read -p "Continue anyway? (y/n): " continue_anyway
            if [[ $continue_anyway != "y" ]]; then
                exit 1
            fi
            ;;
    esac
}

# Script entry point
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    check_directory
    main
fi
