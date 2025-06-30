#!/usr/bin/env python3
"""
Startup script para sa ChatGPT Web Automation
Gi create nako ni para easy ra ang pag run sa web server
"""

import subprocess
import sys
import os
import time

def install_requirements():
    """Install required packages"""
    print("🔧 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def check_chrome():
    """Check if Chrome is installed"""
    print("🔍 Checking for Chrome installation...")
    try:
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

def create_directories():
    """Create necessary directories"""
    directories = ['templates', 'static']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Created directory: {directory}")

def main():
    """Main startup function"""
    print("🚀 ChatGPT Web Automation Startup")
    print("=" * 50)
    
    # Check Chrome
    if not check_chrome():
        print("\n❌ Please install Google Chrome and try again.")
        input("Press Enter to exit...")
        return
    
    # Create directories
    create_directories()
    
    # Install requirements
    print("\n📦 Checking dependencies...")
    try:
        import flask
        import flask_socketio
        print("✅ Flask dependencies already installed!")
    except ImportError:
        print("📦 Installing Flask dependencies...")
        if not install_requirements():
            print("\n❌ Setup failed. Please check the error messages above.")
            input("Press Enter to exit...")
            return
    
    print("\n✅ Setup completed successfully!")
    print("\n🌐 Starting web server...")
    print("📍 Server will be available at: http://localhost:3700")
    print("🛡️ Cloudflare bypass enabled")
    print("💻 Web interface ready!")
    print("\n" + "=" * 50)
    print("🔥 FEATURES:")
    print("   • Beautiful animated web interface")
    print("   • Real-time chat with ChatGPT")
    print("   • Cloudflare bypass technology")
    print("   • Human-like typing simulation")
    print("   • Status monitoring and logging")
    print("=" * 50)
    
    # Wait a moment
    time.sleep(2)
    
    # Start the web server
    try:
        print("\n🎯 Starting server on port 3700...")
        print("💡 Open your browser and go to: http://localhost:3700")
        print("⏹️  Press Ctrl+C to stop the server")
        print("\n" + "-" * 50)
        
        # Import and run the web server
        from web_server import app, socketio
        socketio.run(app, host='0.0.0.0', port=3700, debug=False)
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error running server: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure port 3700 is not in use")
        print("2. Check if all dependencies are installed")
        print("3. Verify Chrome is properly installed")
    finally:
        print("\n👋 Goodbye!")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
