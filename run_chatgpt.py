#!/usr/bin/env python3
"""
Simple runner for ChatGPT automation with verbose output
"""

print("🚀 ChatGPT Automation Starter")
print("=" * 40)

# Test basic imports first
print("Step 1: Testing imports...")
try:
    import sys
    print(f"✅ Python version: {sys.version}")
    
    from selenium import webdriver
    print("✅ Selenium imported")
    
    from selenium.webdriver.chrome.options import Options
    print("✅ Chrome options imported")
    
except Exception as e:
    print(f"❌ Import error: {e}")
    exit(1)

# Test Chrome installation
print("\nStep 2: Checking Chrome installation...")
import os
chrome_paths = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
]

chrome_found = False
for path in chrome_paths:
    if os.path.exists(path):
        print(f"✅ Chrome found at: {path}")
        chrome_found = True
        break

if not chrome_found:
    print("❌ Chrome not found. Please install Google Chrome first.")
    exit(1)

# Try to start Chrome
print("\nStep 3: Starting Chrome browser...")
try:
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    print("Creating Chrome driver...")
    driver = webdriver.Chrome(options=chrome_options)
    print("✅ Chrome started successfully!")
    
    print("Navigating to Google to test...")
    driver.get("https://www.google.com")
    print(f"✅ Page loaded: {driver.title}")
    
    print("Closing test browser...")
    driver.quit()
    print("✅ Test completed successfully!")
    
except Exception as e:
    print(f"❌ Chrome startup error: {e}")
    print("\nTrying alternative method...")
    
    try:
        print("Installing ChromeDriver automatically...")
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("✅ Chrome started with webdriver-manager!")
        
        driver.get("https://www.google.com")
        print(f"✅ Page loaded: {driver.title}")
        
        driver.quit()
        print("✅ Alternative method works!")
        
    except Exception as e2:
        print(f"❌ Alternative method failed: {e2}")
        print("\nPossible solutions:")
        print("1. Download ChromeDriver from: https://chromedriver.chromium.org/")
        print("2. Add ChromeDriver to your PATH")
        print("3. Make sure Chrome is updated to the latest version")
        exit(1)

print("\n" + "=" * 50)
print("🎉 SUCCESS! Chrome automation is working!")
print("=" * 50)

print("\n🔐 ChatGPT Login Setup")
print("=" * 30)
print("✅ Manual login mode - you will log in yourself")
print("The browser will open and wait for you to complete login")

print("\nNow starting the ChatGPT automation...")
print("Press Ctrl+C to stop at any time")
print("-" * 50)

# Import and run the main automation with manual login
try:
    from chatgpt_automation_simple import main
    main()
except KeyboardInterrupt:
    print("\n\n⏹️ Stopped by user")
except Exception as e:
    print(f"\n❌ Error running automation: {e}")
    import traceback
    traceback.print_exc()
