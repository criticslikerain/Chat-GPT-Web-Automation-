#!/usr/bin/env python3
"""
Setup script for ChatGPT Selenium automation
This script will install dependencies and run the automation
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def check_chrome():
    """Check if Chrome is installed"""
    print("Checking for Chrome installation...")
    try:
        # Try to find Chrome executable
        import platform
        system = platform.system()
        
        if system == "Windows":
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            ]
        elif system == "Darwin":  # macOS
            chrome_paths = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
        else:  # Linux
            chrome_paths = ["/usr/bin/google-chrome", "/usr/bin/chromium-browser"]
        
        for path in chrome_paths:
            if os.path.exists(path):
                print("✅ Chrome found!")
                return True
        
        print("⚠️  Chrome not found in common locations.")
        print("Please make sure Google Chrome is installed.")
        return False
        
    except Exception as e:
        print(f"Error checking Chrome: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 ChatGPT Selenium Automation Setup")
    print("=" * 40)
    
    # Check Chrome
    if not check_chrome():
        print("\n❌ Please install Google Chrome and try again.")
        return
    
    # Install requirements
    if not install_requirements():
        print("\n❌ Setup failed. Please check the error messages above.")
        return
    
    print("\n✅ Setup completed successfully!")
    print("\nYou can now run the automation with:")
    print("  python chatgpt_automation_improved.py")
    
    # Ask if user wants to run now
    run_now = input("\nWould you like to run the automation now? (y/n): ").lower().strip()
    if run_now in ['y', 'yes']:
        print("\nStarting automation...")
        try:
            import chatgpt_automation_improved
            chatgpt_automation_improved.main()
        except Exception as e:
            print(f"Error running automation: {e}")

if __name__ == "__main__":
    main()
