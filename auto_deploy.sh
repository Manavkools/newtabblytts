#!/bin/bash

# Complete automated deployment script for Sesame CSM 1B API
# This script handles everything from Docker installation to RunPod deployment

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${BOLD}${BLUE}========================================${NC}"
echo -e "${BOLD}${BLUE}Sesame CSM 1B - Complete Deployment${NC}"
echo -e "${BOLD}${BLUE}========================================${NC}\n"

# Step 1: Install Docker if needed
install_docker() {
    echo -e "${BLUE}[Step 1]${NC} Checking Docker installation..."
    
    if command -v docker &> /dev/null; then
        if docker info &> /dev/null 2>&1; then
            echo -e "${GREEN}✓ Docker is installed and running${NC}"
            return 0
        else
            echo -e "${YELLOW}⚠ Docker is installed but daemon is not running${NC}"
            echo "Starting Docker..."
            
            # Try to open Docker Desktop on macOS
            if [[ "$OSTYPE" == "darwin"* ]]; then
                open -a Docker 2>/dev/null || true
                echo "Please start Docker Desktop manually and press Enter to continue..."
                read
            else
                sudo systemctl start docker 2>/dev/null || true
            fi
            
            # Wait for Docker to start
            for i in {1..30}; do
                if docker info &> /dev/null 2>&1; then
                    echo -e "${GREEN}✓ Docker is now running${NC}"
                    return 0
                fi
                sleep 2
            done
            
            echo -e "${RED}✗ Docker daemon failed to start${NC}"
            return 1
        fi
    else
        echo -e "${YELLOW}⚠ Docker is not installed${NC}"
        
        if [[ "$OSTYPE" == "darwin"* ]]; then
            echo "Installing Docker Desktop via Homebrew..."
            if command -v brew &> /dev/null; then
                echo "This will install Docker Desktop (large download, ~500MB)..."
                read -p "Continue? (y/n): " -n 1 -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    brew install --cask docker
                    echo -e "${GREEN}✓ Docker Desktop installed${NC}"
                    echo "Opening Docker Desktop..."
                    open -a Docker
                    echo "Please wait for Docker Desktop to start, then press Enter..."
                    read
                    
                    # Wait for Docker to be ready
                    for i in {1..60}; do
                        if docker info &> /dev/null 2>&1; then
                            echo -e "${GREEN}✓ Docker is ready${NC}"
                            return 0
                        fi
                        sleep 2
                    done
                    
                    echo -e "${RED}✗ Docker failed to start. Please start it manually.${NC}"
                    return 1
                else
                    echo "Installation cancelled"
                    return 1
                fi
            else
                echo "Please install Docker Desktop manually:"
                echo "  https://docs.docker.com/desktop/install/mac-install/"
                return 1
            fi
        else
            echo "Please install Docker manually:"
            echo "  https://docs.docker.com/get-docker/"
            return 1
        fi
    fi
}

# Step 2: Get Docker Hub credentials
get_docker_credentials() {
    echo -e "\n${BLUE}[Step 2]${NC} Docker Hub Configuration"
    
    if [ -z "$DOCKERHUB_USERNAME" ]; then
        read -p "Enter your Docker Hub username: " DOCKERHUB_USERNAME
    fi
    
    if [ -z "$DOCKERHUB_USERNAME" ]; then
        echo -e "${RED}✗ Docker Hub username is required${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ Using Docker Hub username: $DOCKERHUB_USERNAME${NC}"
    
    # Login to Docker Hub
    echo "Logging into Docker Hub..."
    if [ -n "$DOCKERHUB_PASSWORD" ]; then
        echo "$DOCKERHUB_PASSWORD" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin 2>/dev/null
    else
        docker login -u "$DOCKERHUB_USERNAME"
    fi
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Successfully logged into Docker Hub${NC}"
    else
        echo -e "${RED}✗ Docker Hub login failed${NC}"
        exit 1
    fi
}

# Step 3: Build Docker image
build_image() {
    echo -e "\n${BLUE}[Step 3]${NC} Building Docker image..."
    
    IMAGE_NAME="${DOCKERHUB_USERNAME}/sesame-csm-1b-api:latest"
    
    echo "Building: $IMAGE_NAME"
    echo "This will take several minutes (5-15 minutes depending on your connection)..."
    echo ""
    
    if docker build -t "$IMAGE_NAME" .; then
        echo -e "${GREEN}✓ Image built successfully${NC}"
        echo "$IMAGE_NAME"
    else
        echo -e "${RED}✗ Docker build failed${NC}"
        exit 1
    fi
}

# Step 4: Push to Docker Hub
push_image() {
    local image_name=$1
    echo -e "\n${BLUE}[Step 4]${NC} Pushing to Docker Hub..."
    
    echo "Pushing: $image_name"
    echo "This will take several minutes depending on image size and upload speed..."
    echo ""
    
    if docker push "$image_name"; then
        echo -e "${GREEN}✓ Image pushed successfully to Docker Hub${NC}"
    else
        echo -e "${RED}✗ Docker push failed${NC}"
        exit 1
    fi
}

# Step 5: Display RunPod deployment instructions
show_runpod_instructions() {
    local image_name=$1
    echo -e "\n${BLUE}[Step 5]${NC} Deploy to RunPod"
    echo -e "${BOLD}${BLUE}========================================${NC}"
    echo ""
    echo -e "Your Docker image is ready: ${GREEN}$image_name${NC}"
    echo ""
    echo "To deploy on RunPod:"
    echo ""
    echo -e "1. ${BOLD}Open RunPod Console${NC}"
    echo "   https://www.runpod.io/console/serverless"
    echo ""
    echo -e "2. ${BOLD}Create New Endpoint${NC}"
    echo "   - Click 'New Endpoint' button (top right)"
    echo "   - Select 'Import from Docker Registry'"
    echo "   - Enter Docker image: ${GREEN}$image_name${NC}"
    echo ""
    echo -e "3. ${BOLD}Configure Settings${NC}"
    echo "   - Endpoint Name: sesame-csm-1b-tts"
    echo "   - GPU Type: RTX 3090 or A100 (recommended)"
    echo "   - Container Disk: 25 GB"
    echo "   - Max Workers: 5"
    echo "   - Port: 8000"
    echo ""
    echo -e "4. ${BOLD}Environment Variables${NC}"
    echo "   Add these in the environment variables section:"
    echo "   - PORT=8000"
    echo "   - MODEL_NAME=saishah/sesame-csm-1b"
    echo "   - DEVICE=cuda"
    echo ""
    echo -e "5. ${BOLD}Deploy${NC}"
    echo "   - Click 'Create Endpoint'"
    echo "   - Wait 2-5 minutes for deployment"
    echo ""
    echo -e "6. ${BOLD}Get Your Endpoint URL${NC}"
    echo "   - After deployment, RunPod will show your endpoint URL"
    echo "   - Format: https://YOUR_ENDPOINT_ID.api.runpod.ai"
    echo ""
    echo -e "${BOLD}${BLUE}========================================${NC}"
    echo ""
    echo -e "${GREEN}Test your API:${NC}"
    echo ""
    echo "curl -X POST 'https://YOUR_ENDPOINT_ID.api.runpod.ai/generate' \\"
    echo "     -H 'Content-Type: application/json' \\"
    echo "     -d '{\"text\": \"Hello world!\"}' \\"
    echo "     --output audio.wav"
    echo ""
}

# Main execution
main() {
    # Install/check Docker
    if ! install_docker; then
        exit 1
    fi
    
    # Get Docker Hub credentials
    get_docker_credentials
    
    # Build image
    IMAGE_NAME=$(build_image)
    
    # Push image
    push_image "$IMAGE_NAME"
    
    echo ""
    echo -e "${GREEN}✓ Docker image is ready and available on Docker Hub!${NC}"
    echo -e "   Image: ${BLUE}$IMAGE_NAME${NC}"
    echo ""
    
    # Show RunPod deployment instructions
    show_runpod_instructions "$IMAGE_NAME"
    
    echo -e "${GREEN}${BOLD}Deployment preparation complete!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Deploy on RunPod using the instructions above"
    echo "2. Wait for deployment to complete (2-5 minutes)"
    echo "3. Test your endpoint with the curl command shown above"
    echo ""
}

# Run main function
main

