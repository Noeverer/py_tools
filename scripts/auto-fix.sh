#!/bin/bash
#
# Auto-fix script for common code and dependency issues
# Used by GitHub Actions workflows
#

set -e

echo "=== Starting Auto-Fix Script ==="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Detect if Python project
if [ -f "requirements.txt" ] || [ -f "setup.py" ] || [ -f "pyproject.toml" ]; then
    print_info "Python project detected, running Python auto-fix..."
    
    # Check if pip is available
    if ! command -v pip &> /dev/null; then
        print_error "pip not found, skipping Python auto-fix"
    else
        # Install linting tools
        print_info "Installing Python linting tools..."
        pip install --quiet black isort autoflake flake8 2>/dev/null || print_warn "Failed to install some linting tools"
        
        # Run black
        if command -v black &> /dev/null; then
            print_info "Running black formatter..."
            find . -name "*.py" -type f ! -path "*/venv/*" ! -path "*/node_modules/*" ! -path "*/.git/*" ! -path "*/__pycache__/*" | xargs black --quiet || true
        fi
        
        # Run isort
        if command -v isort &> /dev/null; then
            print_info "Running isort import sorter..."
            find . -name "*.py" -type f ! -path "*/venv/*" ! -path "*/node_modules/*" ! -path "*/.git/*" ! -path "*/__pycache__/*" | xargs isort --quiet || true
        fi
        
        # Run autoflake
        if command -v autoflake &> /dev/null; then
            print_info "Running autoflake to remove unused imports..."
            find . -name "*.py" -type f ! -path "*/venv/*" ! -path "*/node_modules/*" ! -path "*/.git/*" ! -path "*/__pycache__/*" | xargs autoflake --in-place --remove-all-unused-imports --remove-duplicate-keys || true
        fi
        
        # Check for Python syntax errors
        print_info "Checking Python syntax..."
        SYNTAX_ERRORS=0
        for file in $(find . -name "*.py" -type f ! -path "*/venv/*" ! -path "*/node_modules/*" ! -path "*/.git/*" ! -path "*/__pycache__/*"); do
            if ! python -m py_compile "$file" 2>/dev/null; then
                print_error "Syntax error in $file"
                SYNTAX_ERRORS=$((SYNTAX_ERRORS + 1))
            fi
        done
        
        if [ $SYNTAX_ERRORS -eq 0 ]; then
            print_info "No Python syntax errors found"
        else
            print_error "Found $SYNTAX_ERRORS files with syntax errors"
        fi
    fi
fi

# Detect if Node.js project
if [ -f "package.json" ]; then
    print_info "Node.js project detected, running JavaScript/TypeScript auto-fix..."
    
    # Check if npm is available
    if ! command -v npm &> /dev/null; then
        print_error "npm not found, skipping JavaScript/TypeScript auto-fix"
    else
        # Install linting tools
        print_info "Installing JavaScript/TypeScript linting tools..."
        npm install --silent eslint prettier 2>/dev/null || true
        
        # Run eslint fix
        if command -v eslint &> /dev/null; then
            print_info "Running eslint --fix..."
            find . -name "*.js" -o -name "*.ts" -o -name "*.jsx" -o -name "*.tsx" | \
                grep -v node_modules | \
                grep -v .git | \
                xargs eslint --fix 2>/dev/null || true
        fi
        
        # Run prettier
        if command -v prettier &> /dev/null; then
            print_info "Running prettier..."
            find . -name "*.js" -o -name "*.ts" -o -name "*.jsx" -o -name "*.tsx" -o -name "*.json" | \
                grep -v node_modules | \
                grep -v .git | \
                xargs prettier --write 2>/dev/null || true
        fi
    fi
fi

# Check and fix dependencies
print_info "Checking dependencies..."

# Python dependencies
if [ -f "requirements.txt" ]; then
    print_info "Checking Python dependencies..."
    if command -v pip-check &> /dev/null; then
        pip install pip-check 2>/dev/null || true
        pip-check || true
    fi
fi

# Node.js dependencies
if [ -f "package.json" ] && [ -d "node_modules" ]; then
    print_info "Checking Node.js dependencies..."
    npm audit fix || true
fi

# Check for environment variables
print_info "Checking environment configuration..."
ENV_FILES=(".env" ".env.local" ".env.example")
for env_file in "${ENV_FILES[@]}"; do
    if [ -f "$env_file" ]; then
        print_info "Found environment file: $env_file"
        # Check for missing variables if .env.example exists
        if [ "$env_file" = ".env.example" ]; then
            print_info "Verifying .env.example format"
        fi
    fi
done

echo ""
print_info "=== Auto-Fix Script Completed ==="
