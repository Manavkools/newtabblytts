#!/bin/bash

# Complete end-to-end deployment script for Sesame CSM 1B API
# This script handles Docker setup, build, push, and RunPod deployment

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Sesame CSM 1B - Complete Deployment${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Step 1: Check and install Docker if needed
check_docker() {
    echo -e "${BLUE}[Step 1]${NC} Checking Docker installation..."
    
    if command -v docker &> /dev/null; then
        if docker info &> /dev/null; then
            echo -e "${GREEN}✓ Docker is installed and running${NC}"
            return 0
        else
            echo -e "${YELLOW}⚠ Docker is installed but daemon is not running${NC}"
            echo "Please start Docker Desktop and run this script again"
            exit 1
        fi
    else
        echo -e "${YELLOW}⚠ Docker is not installed${NC}"
        echo ""
        echo "Please install Docker Desktop:"
        echo "  macOS: https://docs.docker.com/desktop/install/mac-install/"
        echo "  Or run: brew install --cask docker"
        echo ""
        read -p "Press Enter after installing Docker, or Ctrl+C to exit..."
        
        # Check again
        if command -v docker &> /dev/null; then
            echo -e "${GREEN}✓ Docker is now installed${NC}"
            return 0
        else
            echo -e "${RED}✗ Docker installation not detected${NC}"
            exit 1
        fi
    fi
}

# Step 2: Get Docker Hub credentials
get_credentials() {
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
    echo "$DOCKERHUB_PASSWORD" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin 2>/dev/null || \
    docker login -u "$DOCKERHUB_USERNAME"
}

# Step 3: Build Docker image
build_image() {
    echo -e "\n${BLUE}[Step 3]${NC} Building Docker image..."
    
    IMAGE_NAME="${DOCKERHUB_USERNAME}/sesame-csm-1b-api:latest"
    
    echo "Building image: $IMAGE_NAME"
    echo "This may take several minutes..."
    
    docker build -t "$IMAGE_NAME" . || {
        echo -e "${RED}✗ Docker build failed${NC}"
        exit 1
    }
    
    echo -e "${GREEN}✓ Image built successfully${NC}"
    echo "$IMAGE_NAME"
}

# Step 4: Push to Docker Hub
push_image() {
    local image_name=$1
    echo -e "\n${BLUE}[Step 4]${NC} Pushing to Docker Hub..."
    
    echo "Pushing $image_name"
    echo "This may take several minutes depending on image size..."
    
    docker push "$image_name" || {
        echo -e "${RED}✗ Docker push failed${NC}"
        exit 1
    }
    
    echo -e "${GREEN}✓ Image pushed successfully${NC}"
}

# Step 5: Get RunPod configuration
get_runpod_config() {
    echo -e "\n${BLUE}[Step 5]${NC} RunPod Configuration"
    
    # Check for API key
    if [ -z "$RUNPOD_API_KEY" ]; then
        echo "RunPod API Key not found in environment"
        echo "You can get your API key from: https://www.runpod.io/console/settings/api-keys"
        read -p "Enter your RunPod API key (or press Enter to skip API deployment): " RUNPOD_API_KEY
    fi
    
    if [ -z "$RUNPOD_API_KEY" ]; then
        echo -e "${YELLOW}⚠ Skipping API deployment - will provide manual instructions${NC}"
        return 1
    fi
    
    # Endpoint configuration
    ENDPOINT_NAME="${ENDPOINT_NAME:-sesame-csm-1b-tts}"
    GPU_TYPE="${GPU_TYPE:-RTX 3090}"
    MAX_WORKERS="${MAX_WORKERS:-5}"
    CONTAINER_DISK="${CONTAINER_DISK:-25}"
    
    echo -e "${GREEN}✓ RunPod configuration ready${NC}"
    return 0
}

# Step 6: Deploy via RunPod API (if available)
deploy_runpod_api() {
    local image_name=$1
    echo -e "\n${BLUE}[Step 6]${NC} Deploying to RunPod via API..."
    
    # Use Python script for API deployment
    python3 deploy_to_runpod.py --image "$image_name" --api-key "$RUNPOD_API_KEY" \
        --endpoint-name "$ENDPOINT_NAME" --gpu-type "$GPU_TYPE" \
        --max-workers "$MAX_WORKERS" --container-disk "$CONTAINER_DISK" || {
        echo -e "${YELLOW}⚠ API deployment failed, using manual method${NC}"
        return 1
    }
    
    return 0
}

# Step 7: Manual deployment instructions
show_manual_instructions() {
    local image_name=$1
    echo -e "\n${BLUE}[Step 7]${NC} Manual Deployment Instructions"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    echo "1. Go to: https://www.runpod.io/console/serverless"
    echo "2. Click 'New Endpoint'"
    echo "3. Select 'Import from Docker Registry'"
    echo -e "4. Enter: ${GREEN}$image_name${NC}"
    echo ""
    echo "5. Configure Settings:"
    echo "   - Endpoint Name: sesame-csm-1b-tts"
    echo "   - GPU Type: RTX 3090 or A100"
    echo "   - Container Disk: 25GB"
    echo "   - Max Workers: 5"
    echo "   - Port: 8000"
    echo ""
    echo "6. Environment Variables:"
    echo "   - PORT=8000"
    echo "   - MODEL_NAME=saishah/sesame-csm-1b"
    echo "   - DEVICE=cuda"
    echo ""
    echo "7. Click 'Create Endpoint'"
    echo ""
    echo -e "${BLUE}========================================${NC}"
}

# Main execution
main() {
    # Check Docker
    check_docker
    
    # Get credentials
    get_credentials
    
    # Build image
    IMAGE_NAME=$(build_image)
    
    # Push image
    push_image "$IMAGE_NAME"
    
    echo -e "\n${GREEN}✓ Docker image is ready and pushed!${NC}"
    echo -e "   Image: ${BLUE}$IMAGE_NAME${NC}\n"
    
    # RunPod deployment
    if get_runpod_config; then
        if deploy_runpod_api "$IMAGE_NAME"; then
            echo -e "\n${GREEN}✓ Deployment complete!${NC}"
            echo ""
            echo "Your endpoint should be available shortly."
            echo "Check RunPod console for your endpoint URL."
        else
            show_manual_instructions "$IMAGE_NAME"
        fi
    else
        show_manual_instructions "$IMAGE_NAME"
    fi
    
    echo -e "\n${GREEN}========================================${NC}"
    echo -e "${GREEN}Deployment Process Complete!${NC}"
    echo -e "${GREEN}========================================${NC}\n"
}

# Run main function
main

