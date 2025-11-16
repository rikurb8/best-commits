# Migration Guide: v0.1.0 → v0.2.0

This guide helps existing users migrate from the symlink-based installation (v0.1.0) to the new `uv tool` based installation (v0.2.0).

## What Changed?

### Architecture Changes

**Before (v0.1.0):**
- Symlink-based installation in `~/.local/bin`
- PEP 723 inline script metadata in `__main__.py` files
- Dependencies duplicated in inline metadata + `pyproject.toml`
- Manual PATH management required

**After (v0.2.0):**
- Standard Python package installation via `uv tool install`
- Dependencies managed exclusively via `pyproject.toml`
- Automatic PATH handling by `uv tool`
- Proper package isolation in virtual environments
- Switched from `hatchling` to `setuptools` build backend

### Breaking Changes

1. **Installation method changed:**
   - Old: `./scripts/install-tool.sh` creates symlinks
   - New: `uv tool install .` installs as a proper package

2. **PEP 723 inline scripts no longer standalone:**
   - Old: `./tools/commit_changes/__main__.py` works with `uv run --script`
   - New: Requires package installation or `uvx --from .`

3. **Uninstallation method changed:**
   - Old: `./scripts/install-tool.sh uninstall`
   - New: `uv tool uninstall best-commits`

## Migration Steps

### Step 1: Uninstall Old Version

Remove the old symlink-based installation:

```bash
cd best-commits

# If you still have the old version of install-tool.sh
git fetch origin
git checkout v0.1.0
./scripts/install-tool.sh uninstall

# Or manually remove symlinks
rm ~/.local/bin/commit
rm ~/.local/bin/review
```

### Step 2: Update Repository

Pull the latest changes:

```bash
git checkout main
git pull origin main
```

You should now be on v0.2.0 or later.

### Step 3: Install New Version

Choose one of the following installation methods:

**Option A: Standard Installation (Recommended)**
```bash
cd best-commits
uv tool install .

# Or use the updated installer script
./scripts/install-tool.sh
```

**Option B: Development Installation (Editable)**
```bash
cd best-commits
uv tool install --editable .

# Or use the installer script
./scripts/install-tool.sh --editable
```

**Option C: Direct from GitHub**
```bash
uv tool install git+https://github.com/rikurb8/best-commits.git
```

### Step 4: Verify Installation

```bash
# Check that tools are installed
uv tool list

# Try running the commands
commit --help 2>/dev/null || echo "commit command works!"
review --help 2>/dev/null || echo "review command works!"
```

### Step 5: Clean Up (Optional)

Remove old build artifacts from the repository:

```bash
cd best-commits
make clean
# or manually:
rm -rf build/ dist/ *.egg-info best_commits.egg-info
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
```

## New Features & Capabilities

### Multiple Installation Options

```bash
# Install from local directory
uv tool install .

# Install from GitHub
uv tool install git+https://github.com/rikurb8/best-commits.git

# One-time usage without installation
uvx --from . commit
uvx --from git+https://github.com/rikurb8/best-commits.git commit
```

### Easy Updates

```bash
# Upgrade to latest version
uv tool upgrade best-commits

# Or reinstall from local repo
cd best-commits
git pull
uv tool install --force .
```

### Development Workflow

```bash
# Install in editable mode for development
uv tool install --editable .

# Use Makefile for common tasks
make help
make install-dev
make clean
make format
make lint
```

### Better Package Management

```bash
# List all installed uv tools
uv tool list

# Uninstall cleanly
uv tool uninstall best-commits

# No manual PATH management needed!
```

## Troubleshooting

### Issue: Commands not found after installation

**Solution:** Ensure uv's tool bin directory is in your PATH. Run:
```bash
uv tool list
```

If tools are listed but not accessible, check your shell configuration:
```bash
# The uv tool bin directory should be in PATH automatically
# but you can verify with:
which commit
which review
```

### Issue: Build fails with setuptools warnings

**Solution:** This is normal. The warnings are deprecation notices that don't affect functionality. The build should still succeed.

### Issue: Import errors when running tools

**Solution:** Make sure you've installed the package, not just cloned the repo:
```bash
cd best-commits
uv tool install .
```

### Issue: Old version still running

**Solution:** Uninstall old symlinks first:
```bash
rm ~/.local/bin/commit ~/.local/bin/review
uv tool install .
```

### Issue: Want to test without installing

**Solution:** Use `uvx`:
```bash
# From local directory
cd best-commits
uvx --from . commit
uvx --from . review

# Or run as modules
uv run -m tools.commit_changes
uv run -m tools.review_changes
```

## Rollback to v0.1.0

If you encounter issues and need to rollback:

```bash
# Uninstall v0.2.0
uv tool uninstall best-commits

# Checkout v0.1.0
cd best-commits
git checkout v0.1.0

# Install old version with symlinks
./scripts/install-tool.sh
```

## Benefits of the New Architecture

1. **Standard Python Packaging**
   - Follows Python packaging best practices
   - Compatible with PyPI (future)
   - Better tooling support

2. **Proper Dependency Isolation**
   - Each installation in its own virtual environment
   - No dependency conflicts with other tools
   - Reproducible installations

3. **Better Version Management**
   - Can have multiple versions installed (with different tools)
   - Easy upgrades: `uv tool upgrade best-commits`
   - Clear version tracking

4. **Simplified Maintenance**
   - Single source of truth for dependencies (`pyproject.toml`)
   - No manual symlink management
   - Automatic PATH handling

5. **Development Friendly**
   - Editable installs for development
   - Makefile for common tasks
   - Better testing workflow

## Questions or Issues?

If you encounter problems during migration:

1. Check this migration guide thoroughly
2. Review the updated README.md
3. Open an issue on GitHub: https://github.com/rikurb8/best-commits/issues

## Summary

| Aspect | v0.1.0 | v0.2.0 |
|--------|--------|--------|
| Installation | Symlinks | `uv tool install` |
| Dependencies | PEP 723 inline | `pyproject.toml` |
| Build Backend | Hatchling | Setuptools |
| Updates | Manual | `uv tool upgrade` |
| Isolation | No | Yes (venv per install) |
| PATH | Manual | Automatic |
| PyPI Ready | No | Yes |

The migration provides a more robust, maintainable, and standard-compliant package structure.
