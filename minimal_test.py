print("Starting minimal test...")

try:
    print("Importing selenium...")
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    print("Imports successful!")
    
    print("Setting up Chrome options...")
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    print("Chrome options set!")
    
    print("Installing ChromeDriver...")
    service = Service(ChromeDriverManager().install())
    print("ChromeDriver installed!")
    
    print("Launching Chrome...")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print("Chrome launched successfully!")
    
    print("Navigating to Google...")
    driver.get("https://www.google.com")
    print(f"Page title: {driver.title}")
    
    print("Waiting 3 seconds...")
    import time
    time.sleep(3)
    
    print("Closing browser...")
    driver.quit()
    print("Test completed successfully!")
    
except Exception as e:
    print(f"Error occurred: {e}")
    import traceback
    traceback.print_exc()
