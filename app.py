#!/usr/bin/env python3
"""
CSV Processor - Lychee
A GUI and CLI interface for CSV processing modules
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """Print application banner"""
    print("🍃" + "="*50)
    print("🍃 CSV Processor - Lychee")
    print("🍃" + "="*50)

def get_modules():
    """Get available modules"""
    return {
        "1": ("Table in", "table_fix.py", "csv"),
        "2": ("Regex Replace", "regex_replace.py", "csv"),
        "3": ("NCM Check", "ncm_check.py", "csv"),
        "4": ("NCM Valid Generator", "ncm_valid_generator.py", "json"),
        "5": ("Date Fix", "date_fix.py", "csv"),
        "6": ("Table Out", "table_out.py", "csv")
    }

def show_menu():
    """Show main menu"""
    modules = get_modules()
    print("\n📋 Available Modules:")
    print("-" * 30)
    for key, (name, script, file_type) in modules.items():
        print(f"{key}. {name} ({file_type.upper()} files)")
    print("7. 📁 Open files folder")
    print("8. ❌ Exit")
    print("-" * 30)

def get_file_input(file_type):
    """Get file input from user with drag and drop support"""
    while True:
        print(f"\n📂 Enter path to {file_type.upper()} file:")
        print("💡 TIP: You can drag and drop the file into this terminal")
        file_path = input("📁 File path: ").strip()
        
        if not file_path:
            print("❌ Please enter a file path")
            continue
        
        # Clean up drag-and-drop file paths
        file_path = clean_file_path(file_path)
            
        if not os.path.exists(file_path):
            print("❌ File does not exist")
            print(f"🔍 Tried: {file_path}")
            continue
            
        if not file_path.lower().endswith(f'.{file_type}'):
            print(f"❌ File must be a {file_type.upper()} file")
            continue
            
        return file_path

def clean_file_path(file_path):
    """Clean file path from drag and drop operations"""
    # Remove surrounding quotes (single or double)
    file_path = file_path.strip('\'"')
    
    # Handle escaped spaces and special characters (common in drag-drop)
    file_path = file_path.replace('\\ ', ' ')
    
    # Remove file:// prefix if present (some systems add this)
    if file_path.startswith('file://'):
        file_path = file_path[7:]
    
    # Handle Windows paths with forward slashes
    if os.name == 'nt' and '/' in file_path:
        file_path = file_path.replace('/', '\\')
    
    # Expand user path (~)
    file_path = os.path.expanduser(file_path)
    
    # Convert to absolute path
    file_path = os.path.abspath(file_path)
    
    return file_path

def run_module(module_name, script_name, file_path):
    """Run a module with the given file"""
    print(f"\n🚀 Running {module_name}...")
    print("-" * 40)
    
    try:
        script_path = os.path.join("modules", script_name)
        
        if not os.path.exists(script_path):
            print(f"❌ Module {script_name} not found!")
            return
        
        # Try to use a relative path for the file argument
        base_dir = os.path.dirname(os.path.abspath(__file__))
        try:
            rel_file_path = os.path.relpath(file_path, base_dir)
        except Exception:
            rel_file_path = file_path
        
        # Run the module with relative file path
        result = subprocess.run(
            ["python", script_path, rel_file_path],
            cwd=base_dir,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            print(f"✅ {module_name} completed successfully!")
        else:
            print(f"❌ {module_name} failed with error code {result.returncode}")
            
    except subprocess.TimeoutExpired:
        print(f"❌ {module_name} timed out after 5 minutes")
    except KeyboardInterrupt:
        print(f"\n⚠️  {module_name} was interrupted by user")
    except Exception as e:
        print(f"❌ Error running {module_name}: {str(e)}")

def open_files_folder():
    """Open the files output folder"""
    files_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files")
    
    try:
        if not os.path.exists(files_path):
            os.makedirs(files_path)
            print(f"📁 Created files folder: {files_path}")
        
        if os.name == 'nt':
            os.startfile(files_path)
        elif os.name == 'posix':
            if sys.platform == 'darwin':
                subprocess.run(['open', files_path])
            else:
                subprocess.run(['xdg-open', files_path])
        else:
            print(f"📍 Files are saved in: {files_path}")
            return
        
        print(f"📁 Opened files folder: {files_path}")
    except Exception as e:
        print(f"❌ Could not open files folder: {str(e)}")
        print(f"📍 Files are saved in: {files_path}")

def try_gui():
    try:
        if os.name == 'posix':
            if not os.environ.get('DISPLAY') and not os.environ.get('WAYLAND_DISPLAY'):
                return False

        import subprocess
        result = subprocess.run(
            ["python", "app_gui.py"],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            timeout=5
        )
        return result.returncode == 0
        
    except Exception:
        return False

def main():
    print_banner()
    
    print("🔍 Checking for GUI support...")
    if try_gui():
        return
    
    print("💻 Running in CLI mode")
    
    modules = get_modules()
    
    while True:
        show_menu()
        
        try:
            choice = input("\n👉 Select option (1-8): ").strip()
            
            if choice == "8":
                print("\n👋 Goodbye!")
                break
            elif choice == "7":
                open_files_folder()
                input("\nPress Enter to continue...")
                continue
            elif choice in modules:
                module_name, script_name, file_type = modules[choice]
                
                file_path = get_file_input(file_type)
                run_module(module_name, script_name, file_path)
                
                input("\nPress Enter to continue...")
            else:
                print("❌ Invalid option. Please select 1-8.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
