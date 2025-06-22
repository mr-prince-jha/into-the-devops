#!/usr/bin/env bash

# CI Script for Into The DevOps Repository
# Author: H A R S H A A
# Description: Performs various checks and validations on the repository content

# Strict mode settings
set -euo pipefail
IFS=$'\n\t'

# Color codes for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# Script variables
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_DIR="$(dirname "${SCRIPT_DIR}")"
readonly MAX_LINE_LENGTH=100
readonly PYTHON_MIN_VERSION="3.6"

# Log functions
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1" >&2; }
log_error() { echo -e "${RED}[ERROR]${NC} $1" >&2; }

# Check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Verify system requirements
check_requirements() {
    log_info "Checking system requirements..."
    
    # Check Python version
    if ! command_exists python3; then
        log_error "Python 3 is required but not installed."
        exit 1
    fi

    local python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    if ! awk -v ver="$python_version" -v req="$PYTHON_MIN_VERSION" 'BEGIN{exit(!(ver>=req))}'; then
        log_error "Python version must be >= $PYTHON_MIN_VERSION (found: $python_version)"
        exit 1
    fi

    # Check for flake8
    if ! command_exists flake8; then
        log_error "flake8 is required but not installed. Install with: pip install flake8"
        exit 1
    }

    log_success "All requirements satisfied"
}

# Find all markdown files
find_markdown_files() {
    log_info "Locating markdown files..."
    local md_files=($(find "${PROJECT_DIR}" -name "*.md" -not -path "${PROJECT_DIR}/tests/*"))
    
    if [ ${#md_files[@]} -eq 0 ]; then
        log_warning "No markdown files found!"
        return 1
    fi
    
    echo "${md_files[@]}"
}

# Run syntax lint on markdown files
check_markdown_syntax() {
    local file="$1"
    local relative_path="${file#$PROJECT_DIR/}"
    
    log_info "Checking syntax: $relative_path"
    if ! python3 "${PROJECT_DIR}/tests/syntax_lint.py" "$file" > /dev/null; then
        log_error "Syntax check failed for: $relative_path"
        return 1
    fi
    return 0
}

# Run PEP8 checks
check_pep8() {
    log_info "Running PEP8 checks..."
    if ! flake8 --max-line-length=$MAX_LINE_LENGTH .; then
        log_error "PEP8 check failed"
        return 1
    fi
    return 0
}

# Check for broken links in markdown files
check_broken_links() {
    local file="$1"
    local relative_path="${file#$PROJECT_DIR/}"
    
    log_info "Checking links in: $relative_path"
    
    # Find all markdown links and verify they exist
    local links=($(grep -o '\[.*\](\([^)]*\))' "$file" | sed 's/.*(\(.*\))/\1/'))
    for link in "${links[@]}"; do
        # Skip external URLs
        if [[ $link =~ ^https?:// ]]; then
            continue
        fi
        
        # Check if internal link exists
        if [[ $link == /* ]]; then
            link="${PROJECT_DIR}${link}"
        else
            link="$(dirname "$file")/${link}"
        fi
        
        if [[ ! -e "$link" ]]; then
            log_warning "Broken link found in $relative_path: $link"
        fi
    done
}

# Main execution function
main() {
    local error_count=0
    local warning_count=0
    
    echo "================================================"
    log_info "Starting CI checks for Into The DevOps"
    echo "================================================"
    
    # Check requirements first
    check_requirements
    
    # Process markdown files
    local md_files=($(find_markdown_files))
    local total_files=${#md_files[@]}
    local current=0
    
    echo "------------------------------------------------"
    log_info "Processing $total_files markdown files..."
    echo "------------------------------------------------"
    
    for file in "${md_files[@]}"; do
        ((current++))
        echo -ne "\rProgress: [$current/$total_files]"
        
        if ! check_markdown_syntax "$file"; then
            ((error_count++))
        fi
        
        check_broken_links "$file"
    done
    echo # New line after progress
    
    echo "------------------------------------------------"
    log_info "Running code style checks..."
    echo "------------------------------------------------"
    
    if ! check_pep8; then
        ((error_count++))
    fi
    
    echo "================================================"
    log_info "CI Check Summary"
    echo "------------------------------------------------"
    echo "Files processed: $total_files"
    echo "Errors found: $error_count"
    echo "Warnings found: $warning_count"
    echo "================================================"
    
    if [ $error_count -gt 0 ]; then
        log_error "CI checks failed with $error_count errors"
        exit 1
    fi
    
    log_success "All CI checks passed successfully!"
    exit 0
}

# Trap errors
trap 'echo -e "\n${RED}Script failed${NC}: line $LINENO with exit code $?" >&2' ERR

# Run main function
main "$@"
