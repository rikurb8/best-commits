#!/bin/bash
# Install best-commits tools using uv tool install
#
# Each tool is installed independently from its subdirectory.

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

TOOLS=("commit" "review")

print_usage() {
    echo "Usage: $0 [OPTIONS] [TOOL]"
    echo ""
    echo "Install best-commits tools using uv tool install"
    echo ""
    echo "Options:"
    echo "  -e, --editable    Install in editable mode for development"
    echo "  -u, --uninstall   Uninstall the tools"
    echo "  -h, --help        Show this help message"
    echo ""
    echo "Tools:"
    echo "  commit            Install only commit tool"
    echo "  review            Install only review tool"
    echo "  all               Install all tools (default)"
    echo ""
    echo "Examples:"
    echo "  $0                # Install all tools"
    echo "  $0 commit         # Install only commit tool"
    echo "  $0 --editable     # Install all tools in editable mode"
    echo "  $0 -e commit      # Install commit tool in editable mode"
    echo "  $0 --uninstall    # Uninstall all tools"
    echo "  $0 -u review      # Uninstall only review tool"
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

get_tool_dir() {
    local tool_name=$1
    case "$tool_name" in
        commit)
            echo "commit_changes"
            ;;
        review)
            echo "review_changes"
            ;;
        *)
            echo ""
            ;;
    esac
}

get_package_name() {
    local tool_name=$1
    case "$tool_name" in
        commit)
            echo "best-commits-commit"
            ;;
        review)
            echo "best-commits-review"
            ;;
        *)
            echo ""
            ;;
    esac
}

install_tool() {
    local tool_name=$1
    local editable=$2
    local tool_dir=$(get_tool_dir "$tool_name")
    local package_name=$(get_package_name "$tool_name")

    if [ -z "$tool_dir" ]; then
        echo -e "${RED}Error: Unknown tool '$tool_name'${NC}"
        return 1
    fi

    local tool_path="$PROJECT_ROOT/tools/$tool_dir"

    if [ ! -d "$tool_path" ]; then
        echo -e "${RED}Error: Tool directory not found: $tool_path${NC}"
        return 1
    fi

    echo -e "${CYAN}Installing $tool_name...${NC}"

    if [ "$editable" = true ]; then
        uv tool install --editable "$tool_path"
    else
        uv tool install "$tool_path"
    fi

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Successfully installed '$tool_name'${NC}"
    else
        echo -e "${RED}✗ Failed to install '$tool_name'${NC}"
        return 1
    fi
}

uninstall_tool() {
    local tool_name=$1
    local package_name=$(get_package_name "$tool_name")

    if [ -z "$package_name" ]; then
        echo -e "${RED}Error: Unknown tool '$tool_name'${NC}"
        return 1
    fi

    echo -e "${CYAN}Uninstalling $tool_name...${NC}"

    uv tool uninstall "$package_name" 2>/dev/null

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Successfully uninstalled '$tool_name'${NC}"
    else
        echo -e "${YELLOW}! Tool '$tool_name' was not installed${NC}"
    fi
}

install_all_tools() {
    local editable=$1
    local failed=0

    echo -e "${CYAN}=== Installing Best Commits Tools ===${NC}"
    echo ""

    for tool in "${TOOLS[@]}"; do
        install_tool "$tool" "$editable"
        if [ $? -ne 0 ]; then
            failed=1
        fi
        echo ""
    done

    if [ $failed -eq 0 ]; then
        echo -e "${GREEN}✓ All tools installed successfully!${NC}"
        echo ""
        echo "Commands available:"
        echo "  commit    # Generate AI-powered commit messages"
        echo "  review    # Get AI code review feedback"
        echo ""
        echo "Update tools:"
        echo "  uv tool upgrade best-commits-commit"
        echo "  uv tool upgrade best-commits-review"
        echo ""
        echo "View installed tools:"
        echo "  uv tool list"
        echo ""
    else
        echo -e "${RED}✗ Some tools failed to install${NC}"
        exit 1
    fi
}

uninstall_all_tools() {
    echo -e "${CYAN}=== Uninstalling Best Commits Tools ===${NC}"
    echo ""

    for tool in "${TOOLS[@]}"; do
        uninstall_tool "$tool"
    done

    echo ""
    echo -e "${GREEN}✓ Uninstallation complete!${NC}"
    echo ""
}

main() {
    check_uv

    local editable=false
    local uninstall=false
    local tool=""

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
            commit|review|all)
                tool=$1
                shift
                ;;
            *)
                echo -e "${RED}Unknown option: $1${NC}"
                echo ""
                print_usage
                exit 1
                ;;
        esac
    done

    # Default to all tools if not specified
    if [ -z "$tool" ]; then
        tool="all"
    fi

    if [ "$uninstall" = true ]; then
        if [ "$tool" = "all" ]; then
            uninstall_all_tools
        else
            echo -e "${CYAN}=== Uninstalling Best Commits Tools ===${NC}"
            echo ""
            uninstall_tool "$tool"
            echo ""
            echo -e "${GREEN}✓ Uninstallation complete!${NC}"
        fi
    else
        if [ "$tool" = "all" ]; then
            install_all_tools $editable
        else
            echo -e "${CYAN}=== Installing Best Commits Tools ===${NC}"
            echo ""
            install_tool "$tool" $editable
            echo ""
            echo -e "${GREEN}✓ Installation complete!${NC}"
            echo ""
            echo "Command available: $tool"
            echo ""
        fi
    fi
}

main "$@"
