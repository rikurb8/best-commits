#!/bin/bash
# Install best-commits tools using uv tool install

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

print_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Install best-commits tools using uv tool install"
    echo ""
    echo "Options:"
    echo "  -e, --editable    Install in editable mode for development"
    echo "  -u, --uninstall   Uninstall the tools"
    echo "  -h, --help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                # Install normally"
    echo "  $0 --editable     # Install in editable mode"
    echo "  $0 --uninstall    # Uninstall"
}

check_uv() {
    if ! command -v uv &> /dev/null; then
        echo -e "${RED}Error: 'uv' is not installed${NC}"
        echo ""
        echo "Install uv from: https://docs.astral.sh/uv/"
        echo ""
        echo "Quick install:"
        echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
        echo ""
        exit 1
    fi
}

install_tools() {
    local editable=$1

    echo -e "${CYAN}=== Installing Best Commits Tools ===${NC}"
    echo ""

    cd "$PROJECT_ROOT"

    if [ "$editable" = true ]; then
        echo -e "${CYAN}Installing in editable mode (for development)...${NC}"
        echo ""
        uv tool install --editable .
    else
        echo -e "${CYAN}Installing...${NC}"
        echo ""
        uv tool install .
    fi

    local exit_code=$?

    if [ $exit_code -eq 0 ]; then
        echo ""
        echo -e "${GREEN}✓ Installation complete!${NC}"
        echo ""
        echo "Commands available:"
        echo "  commit    # Generate AI-powered commit messages"
        echo "  review    # Get AI code review feedback"
        echo ""
        echo "Update tools:"
        echo "  uv tool upgrade best-commits"
        echo ""
        echo "View installed tools:"
        echo "  uv tool list"
        echo ""
    else
        echo ""
        echo -e "${RED}✗ Installation failed${NC}"
        exit $exit_code
    fi
}

uninstall_tools() {
    echo -e "${CYAN}=== Uninstalling Best Commits Tools ===${NC}"
    echo ""

    uv tool uninstall best-commits

    local exit_code=$?

    if [ $exit_code -eq 0 ]; then
        echo ""
        echo -e "${GREEN}✓ Uninstallation complete!${NC}"
        echo ""
    else
        echo ""
        echo -e "${RED}✗ Uninstallation failed or package not found${NC}"
        exit $exit_code
    fi
}

main() {
    check_uv

    local editable=false
    local uninstall=false

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -e|--editable)
                editable=true
                shift
                ;;
            -u|--uninstall)
                uninstall=true
                shift
                ;;
            -h|--help)
                print_usage
                exit 0
                ;;
            *)
                echo -e "${RED}Unknown option: $1${NC}"
                echo ""
                print_usage
                exit 1
                ;;
        esac
    done

    if [ "$uninstall" = true ]; then
        uninstall_tools
    else
        install_tools $editable
    fi
}

main "$@"
