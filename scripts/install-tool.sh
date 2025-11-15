#!/bin/bash
# Install best-commits tools globally by creating symlinks in ~/.local/bin

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

# Installation directory (user's local bin)
INSTALL_DIR="${HOME}/.local/bin"

# Available tools
TOOLS=("commit" "review")

print_usage() {
    echo "Usage: $0 [COMMAND] [TOOL]"
    echo ""
    echo "Install or uninstall best-commits tools globally"
    echo ""
    echo "Commands:"
    echo "  install [TOOL]     - Install tools (default command)"
    echo "  uninstall [TOOL]   - Uninstall/remove tools"
    echo ""
    echo "Available tools:"
    echo "  commit    - AI-powered commit message generator"
    echo "  review    - AI-powered code review tool"
    echo "  all       - All tools (default)"
    echo ""
    echo "Examples:"
    echo "  $0                    # Install all tools"
    echo "  $0 install commit     # Install only commit tool"
    echo "  $0 uninstall review   # Uninstall review tool"
    echo "  $0 uninstall all      # Uninstall all tools"
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

install_tool() {
    local tool_name=$1
    local tool_dir=$(get_tool_dir "$tool_name")

    if [ -z "$tool_dir" ]; then
        echo -e "${RED}Error: Unknown tool '$tool_name'${NC}"
        return 1
    fi

    local source_path="${PROJECT_ROOT}/tools/${tool_dir}/__main__.py"
    local target_path="${INSTALL_DIR}/${tool_name}"

    # Check if source exists
    if [ ! -f "$source_path" ]; then
        echo -e "${RED}Error: Source file not found: $source_path${NC}"
        return 1
    fi

    # Create install directory if it doesn't exist
    if [ ! -d "$INSTALL_DIR" ]; then
        echo -e "${CYAN}Creating directory: $INSTALL_DIR${NC}"
        mkdir -p "$INSTALL_DIR"
    fi

    # Remove existing symlink or file if it exists
    if [ -L "$target_path" ] || [ -f "$target_path" ]; then
        echo -e "${YELLOW}Removing existing installation: $target_path${NC}"
        rm "$target_path"
    fi

    # Create symlink
    echo -e "${CYAN}Creating symlink: $target_path -> $source_path${NC}"
    ln -s "$source_path" "$target_path"

    # Make executable
    chmod +x "$source_path"

    echo -e "${GREEN}✓ Successfully installed '$tool_name'${NC}"
}

uninstall_tool() {
    local tool_name=$1
    local target_path="${INSTALL_DIR}/${tool_name}"

    if [ ! -e "$target_path" ]; then
        echo -e "${YELLOW}Tool '$tool_name' is not installed${NC}"
        return 0
    fi

    echo -e "${CYAN}Removing: $target_path${NC}"
    rm "$target_path"
    echo -e "${GREEN}✓ Successfully uninstalled '$tool_name'${NC}"
}

check_path() {
    if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
        echo ""
        echo -e "${YELLOW}⚠ Warning: $INSTALL_DIR is not in your PATH${NC}"
        echo -e "${YELLOW}Add this line to your ~/.bashrc, ~/.zshrc, or equivalent:${NC}"
        echo -e "${CYAN}export PATH=\"\$HOME/.local/bin:\$PATH\"${NC}"
        echo ""
    fi
}

check_uv() {
    if ! command -v uv &> /dev/null; then
        echo -e "${YELLOW}⚠ Warning: 'uv' is not installed${NC}"
        echo -e "${YELLOW}Install uv from: https://docs.astral.sh/uv/getting-started/installation/${NC}"
        echo ""
    fi
}

main() {
    # Parse arguments
    local command="${1:-install}"
    local target="${2:-all}"

    # Handle legacy single-arg usage
    if [ "$command" = "-h" ] || [ "$command" = "--help" ]; then
        print_usage
        exit 0
    elif [ "$command" != "install" ] && [ "$command" != "uninstall" ]; then
        # If first arg is not a command, treat it as a tool name for install
        target="$command"
        command="install"
    fi

    if [ "$target" = "-h" ] || [ "$target" = "--help" ]; then
        print_usage
        exit 0
    fi

    # Execute command
    case "$command" in
        install)
            echo -e "${CYAN}=== Best Commits Tool Installer ===${NC}"
            echo ""

            # Check prerequisites
            check_uv

            # Install requested tools
            if [ "$target" = "all" ]; then
                for tool in "${TOOLS[@]}"; do
                    install_tool "$tool"
                done
            else
                install_tool "$target"
            fi

            echo ""
            check_path

            echo -e "${GREEN}Installation complete!${NC}"
            echo ""
            echo "Usage:"
            echo "  commit    # Generate AI-powered commit messages"
            echo "  review    # Get AI code review feedback"
            echo ""
            ;;

        uninstall)
            echo -e "${CYAN}=== Best Commits Tool Uninstaller ===${NC}"
            echo ""

            # Uninstall requested tools
            if [ "$target" = "all" ]; then
                for tool in "${TOOLS[@]}"; do
                    uninstall_tool "$tool"
                done
            else
                uninstall_tool "$target"
            fi

            echo ""
            echo -e "${GREEN}Uninstallation complete!${NC}"
            echo ""
            ;;

        *)
            echo -e "${RED}Error: Unknown command '$command'${NC}"
            echo ""
            print_usage
            exit 1
            ;;
    esac
}

main "$@"
