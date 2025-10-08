"""
Prompt Version Management Script

This script helps you create and manage prompt versions easily.

Usage:
    python prompts/create_version.py v2          # Create v2 from current version
    python prompts/create_version.py v2 --from v1  # Create v2 from v1
    python prompts/create_version.py --list      # List all versions
    python prompts/create_version.py --current   # Show current version
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

# Get the prompts directory
PROMPTS_DIR = Path(__file__).parent

def list_versions():
    """List all available prompt versions."""
    print("\n📋 Available Prompt Versions:\n")
    
    versions = []
    for file in PROMPTS_DIR.glob("system_prompt_v*.txt"):
        version = file.stem.replace("system_prompt_", "")
        size = file.stat().st_size
        modified = datetime.fromtimestamp(file.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        versions.append((version, size, modified, file))
    
    if not versions:
        print("No prompt versions found.")
        return
    
    # Sort by version number
    versions.sort(key=lambda x: int(x[0].replace("v", "")))
    
    # Display table
    print(f"{'Version':<10} {'Size':<10} {'Modified':<20} {'Path'}")
    print("-" * 70)
    for version, size, modified, file in versions:
        print(f"{version:<10} {size:<10} {modified:<20} {file.name}")
    
    print()

def get_current_version():
    """Get the currently active prompt version from config."""
    try:
        # Import from parent directory
        sys.path.insert(0, str(PROMPTS_DIR.parent))
        from config.settings import PROMPT_VERSION
        return PROMPT_VERSION
    except Exception as e:
        print(f"Warning: Could not read current version from config: {e}")
        return None

def show_current():
    """Show the current active prompt version and its content."""
    version = get_current_version()
    
    if not version:
        print("Could not determine current version.")
        return
    
    print(f"\n✅ Current Active Version: {version}\n")
    
    prompt_file = PROMPTS_DIR / f"system_prompt_{version}.txt"
    
    if not prompt_file.exists():
        print(f"❌ Error: Prompt file {prompt_file} not found!")
        return
    
    print("Content:")
    print("-" * 70)
    with open(prompt_file, "r", encoding="utf-8") as f:
        print(f.read())
    print("-" * 70)
    print()

def create_version(new_version: str, from_version: str = None):
    """
    Create a new prompt version.
    
    Args:
        new_version: The new version to create (e.g., "v2")
        from_version: The version to copy from (defaults to current)
    """
    # Ensure version starts with 'v'
    if not new_version.startswith("v"):
        new_version = f"v{new_version}"
    
    # Determine source version
    if from_version is None:
        from_version = get_current_version()
        if not from_version:
            print("❌ Error: Could not determine current version.")
            print("Please specify source version with --from")
            return False
    
    if not from_version.startswith("v"):
        from_version = f"v{from_version}"
    
    # Check if source exists
    source_file = PROMPTS_DIR / f"system_prompt_{from_version}.txt"
    if not source_file.exists():
        print(f"❌ Error: Source version {from_version} not found at {source_file}")
        return False
    
    # Check if target already exists
    target_file = PROMPTS_DIR / f"system_prompt_{new_version}.txt"
    if target_file.exists():
        response = input(f"⚠️  Version {new_version} already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return False
    
    # Copy the file
    try:
        shutil.copy2(source_file, target_file)
        print(f"\n✅ Created {new_version} from {from_version}")
        print(f"   File: {target_file}")
        print(f"\nNext steps:")
        print(f"1. Edit {target_file} with your changes")
        print(f"2. Update config/settings.py: PROMPT_VERSION = \"{new_version}\"")
        print(f"3. Test the new prompt")
        print(f"4. Document your changes in prompts/README.md")
        return True
    except Exception as e:
        print(f"❌ Error creating version: {e}")
        return False

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    command = sys.argv[1]
    
    if command == "--list":
        list_versions()
    
    elif command == "--current":
        show_current()
    
    elif command == "--help" or command == "-h":
        print(__doc__)
    
    else:
        # Assume it's a version to create
        new_version = command
        from_version = None
        
        # Check for --from flag
        if "--from" in sys.argv:
            from_index = sys.argv.index("--from")
            if from_index + 1 < len(sys.argv):
                from_version = sys.argv[from_index + 1]
        
        create_version(new_version, from_version)

if __name__ == "__main__":
    main()

