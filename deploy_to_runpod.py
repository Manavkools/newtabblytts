#!/usr/bin/env python3
"""
Automated deployment script for Sesame CSM 1B API to RunPod
This script automates Docker build, push, and RunPod deployment
"""
import os
import sys
import subprocess
import json
import time
import requests
from typing import Optional, Dict, Any

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_step(message: str, step: int = None):
    """Print formatted step message"""
    if step:
        print(f"\n{Colors.BOLD}{Colors.BLUE}[Step {step}]{Colors.END} {message}")
    else:
        print(f"\n{Colors.BLUE}{message}{Colors.END}")

def print_success(message: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_error(message: str):
    """Print error message"""
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def print_warning(message: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")

def check_command(command: str) -> bool:
    """Check if a command exists"""
    try:
        subprocess.run(['which', command], capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def run_command(command: list, check: bool = True, capture_output: bool = False) -> subprocess.CompletedProcess:
    """Run a shell command"""
    try:
        result = subprocess.run(
            command,
            check=check,
            capture_output=capture_output,
            text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed: {' '.join(command)}")
        if capture_output:
            print(e.stderr)
        raise

def main():
    """Main deployment flow"""
    print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}Sesame CSM 1B API - Automated Deployment{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}{'='*60}{Colors.END}\n")
    
    # Check Docker
    print_step("Checking Docker installation...")
    if not check_command('docker'):
        print_error("Docker is not installed")
        print("\nPlease install Docker Desktop:")
        print("  macOS: brew install --cask docker")
        print("  Or download from: https://docs.docker.com/desktop/install/mac-install/")
        return False
    
    try:
        run_command(['docker', 'info'], capture_output=True)
        print_success("Docker is installed and running")
    except:
        print_error("Docker daemon is not running")
        print("Please start Docker Desktop and try again")
        return False
    
    # Get Docker Hub credentials
    print_step("Docker Hub Authentication")
    username = os.getenv('DOCKERHUB_USERNAME')
    if not username:
        username = input("Enter your Docker Hub username: ").strip()
    
    if not username:
        print_error("Docker Hub username is required")
        return False
    
    # Login
    print("Logging into Docker Hub...")
    result = run_command(['docker', 'login', '-u', username], check=False)
    if result.returncode != 0:
        print_error("Docker login failed. Please check your credentials.")
        return False
    print_success("Logged into Docker Hub")
    
    # Build image
    image_name = f"{username}/sesame-csm-1b-api:latest"
    print_step(f"Building Docker image: {image_name}")
    print("This may take several minutes...")
    
    try:
        run_command(['docker', 'build', '-t', image_name, '.'], capture_output=True)
        print_success(f"Built {image_name}")
    except:
        print_error("Docker build failed")
        return False
    
    # Push image
    print_step(f"Pushing to Docker Hub: {image_name}")
    print("This may take several minutes...")
    
    try:
        run_command(['docker', 'push', image_name], capture_output=True)
        print_success(f"Pushed {image_name} to Docker Hub")
    except:
        print_error("Docker push failed")
        return False
    
    # RunPod deployment instructions
    print_step("RunPod Deployment Instructions", step=7)
    print(f"\nYour Docker image is ready: {Colors.GREEN}{image_name}{Colors.END}\n")
    print("To deploy on RunPod:")
    print(f"1. Go to: {Colors.BLUE}https://www.runpod.io/console/serverless{Colors.END}")
    print("2. Click 'New Endpoint'")
    print("3. Select 'Import from Docker Registry'")
    print(f"4. Enter: {Colors.GREEN}{image_name}{Colors.END}")
    print("\n5. Configure:")
    print("   - GPU: RTX 3090 or A100")
    print("   - Container Disk: 25GB")
    print("   - Max Workers: 5")
    print("   - Port: 8000")
    print("   - Environment Variables:")
    print("     PORT=8000")
    print("     MODEL_NAME=saishah/sesame-csm-1b")
    print("     DEVICE=cuda")
    
    print(f"\n{Colors.GREEN}Deployment preparation complete!{Colors.END}\n")
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nDeployment cancelled")
        sys.exit(1)

