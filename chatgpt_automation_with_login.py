import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class ChatGPTAutomationWithLogin:
    def __init__(self, headless=False):
        """
        Initialize the ChatGPT automation bot with login capability
        
        Args:
            headless (bool): Whether to run browser in headless mode
        """
        self.driver = None
        self.headless = headless
        self.setup_driver()
    
    def setup_driver(self):
        """Setup Chrome WebDriver - tries multiple approaches"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")
        
        # Add other useful options
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        print("Attempting to start Chrome browser...")
        
        try:
            # Try method 1: Use system ChromeDriver (if available)
            print("Method 1: Trying system ChromeDriver...")
            self.driver = webdriver.Chrome(options=chrome_options)
            print("✅ Chrome started successfully with system driver!")
            
        except Exception as e1:
            print(f"Method 1 failed: {e1}")
            
            try:
                # Try method 2: Use webdriver-manager
                print("Method 2: Trying webdriver-manager...")
                from webdriver_manager.chrome import ChromeDriverManager
                from selenium.webdriver.chrome.service import Service
                
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                print("✅ Chrome started successfully with webdriver-manager!")
                
            except Exception as e2:
                print(f"Method 2 failed: {e2}")
                print("❌ Could not start Chrome browser.")
                raise Exception("Failed to start Chrome browser")
        
        # Set up anti-detection
        if self.driver:
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
    def visit_chatgpt(self):
        """Navigate to ChatGPT website"""
        print("Visiting ChatGPT...")
        self.driver.get("https://chat.openai.com")
        
        # Wait for the page to load
        time.sleep(5)
        print("✅ ChatGPT page loaded!")
        
    def login(self, email, password):
        """
        Attempt to login to ChatGPT automatically
        
        Args:
            email (str): Email address
            password (str): Password
            
        Returns:
            bool: True if login successful, False otherwise
        """
        if not email or not password:
            print("⚠️ No credentials provided, skipping auto-login")
            return False
            
        print("🔐 Attempting automatic login...")
        
        try:
            # Look for login button
            login_selectors = [
                "button[data-testid='login-button']",
                "a[href*='login']",
                "button:contains('Log in')",
                "[data-testid='login']",
                "button[class*='login']"
            ]
            
            login_button = None
            for selector in login_selectors:
                try:
                    login_button = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    print(f"✅ Found login button with selector: {selector}")
                    break
                except TimeoutException:
                    continue
            
            if not login_button:
                # Try to find login button by text
                try:
                    login_button = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Log in')]"))
                    )
                    print("✅ Found login button by text")
                except TimeoutException:
                    print("⚠️ Could not find login button, you may already be logged in")
                    return True
            
            # Click login button
            if login_button:
                login_button.click()
                print("🔘 Clicked login button")
                time.sleep(3)
            
            # Enter email
            print("📧 Entering email...")
            email_selectors = [
                "input[type='email']",
                "input[name='email']",
                "input[id='email']",
                "input[placeholder*='email']"
            ]
            
            email_field = None
            for selector in email_selectors:
                try:
                    email_field = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except TimeoutException:
                    continue
            
            if email_field:
                email_field.clear()
                email_field.send_keys(email)
                print("✅ Email entered")
                time.sleep(1)
            else:
                print("❌ Could not find email field")
                return False
            
            # Click continue/next button
            continue_selectors = [
                "button[type='submit']",
                "button:contains('Continue')",
                "button:contains('Next')",
                "[data-testid='continue-button']"
            ]
            
            continue_button = None
            for selector in continue_selectors:
                try:
                    continue_button = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except TimeoutException:
                    continue
            
            if not continue_button:
                # Try by text
                try:
                    continue_button = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue')]"))
                    )
                except TimeoutException:
                    pass
            
            if continue_button:
                continue_button.click()
                print("🔘 Clicked continue button")
                time.sleep(3)
            
            # Enter password
            print("🔒 Entering password...")
            password_selectors = [
                "input[type='password']",
                "input[name='password']",
                "input[id='password']"
            ]
            
            password_field = None
            for selector in password_selectors:
                try:
                    password_field = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except TimeoutException:
                    continue
            
            if password_field:
                password_field.clear()
                password_field.send_keys(password)
                print("✅ Password entered")
                time.sleep(1)
            else:
                print("❌ Could not find password field")
                return False
            
            # Submit login form
            submit_selectors = [
                "button[type='submit']",
                "button:contains('Log in')",
                "button:contains('Sign in')",
                "[data-testid='login-button']"
            ]
            
            submit_button = None
            for selector in submit_selectors:
                try:
                    submit_button = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except TimeoutException:
                    continue
            
            if not submit_button:
                # Try by text
                try:
                    submit_button = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Log in')]"))
                    )
                except TimeoutException:
                    # Try pressing Enter on password field
                    password_field.send_keys(Keys.RETURN)
                    print("🔘 Pressed Enter to submit")
            
            if submit_button:
                submit_button.click()
                print("🔘 Clicked login submit button")
            
            # Wait for login to complete
            print("⏳ Waiting for login to complete...")
            time.sleep(5)
            
            # Check if we're logged in by looking for chat interface
            try:
                WebDriverWait(self.driver, 10).until(
                    lambda driver: "chat.openai.com" in driver.current_url and 
                    ("chat" in driver.current_url or "conversation" in driver.current_url)
                )
                print("✅ Login successful!")
                return True
            except TimeoutException:
                print("⚠️ Login may have failed or requires additional verification")
                return False
                
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
    
    def wait_for_input_ready(self, timeout=30):
        """Wait for the input field to be ready"""
        print("Looking for input field...")
        try:
            # Try different possible selectors for the input field
            selectors = [
                "textarea[placeholder*='Message']",
                "textarea[data-id='root']", 
                "#prompt-textarea",
                "textarea",
                "[contenteditable='true']",
                "div[contenteditable='true']"
            ]
            
            for selector in selectors:
                try:
                    element = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    print(f"✅ Found input field with selector: {selector}")
                    return element
                except TimeoutException:
                    continue
            
            raise TimeoutException("Could not find input field")
            
        except TimeoutException:
            print("❌ Timeout waiting for input field to be ready")
            print("Current page title:", self.driver.title)
            print("Current URL:", self.driver.current_url)
            return None

    def send_message(self, message):
        """
        Send a message to ChatGPT

        Args:
            message (str): The message to send
        """
        print(f"📝 Sending message: {message}")

        # Wait for input field to be ready
        input_field = self.wait_for_input_ready()
        if not input_field:
            print("❌ Could not find input field")
            return False

        # Clear any existing text and send the message
        input_field.clear()
        time.sleep(0.5)

        # Type the message
        input_field.send_keys(message)

        # Wait a moment for the text to be entered
        time.sleep(1)

        # Send the message (usually Enter key)
        input_field.send_keys(Keys.RETURN)

        print("✅ Message sent!")
        return True

    def wait_for_response(self, timeout=60):
        """
        Wait for ChatGPT to respond and return the response text

        Args:
            timeout (int): Maximum time to wait for response

        Returns:
            str: The response text from ChatGPT
        """
        print("⏳ Waiting for ChatGPT response...")

        try:
            # Wait a moment for the response to start generating
            time.sleep(3)

            # Look for response containers
            response_selectors = [
                "[data-message-author-role='assistant']",
                ".markdown",
                "[class*='response']",
                "[class*='message']",
                "div[class*='group']"
            ]

            start_time = time.time()
            last_response_length = 0
            stable_count = 0

            while time.time() - start_time < timeout:
                for selector in response_selectors:
                    try:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        if elements:
                            # Get the last response (most recent)
                            last_response = elements[-1]
                            response_text = last_response.text.strip()

                            if response_text and len(response_text) > 10:
                                # Check if response has stopped growing (indicating completion)
                                if len(response_text) == last_response_length:
                                    stable_count += 1
                                    if stable_count >= 3:  # Response stable for 3 checks
                                        print("✅ Response received and appears complete!")
                                        return response_text
                                else:
                                    stable_count = 0
                                    last_response_length = len(response_text)
                                    print(f"📝 Response growing... ({len(response_text)} characters)")
                    except Exception as e:
                        continue

                time.sleep(2)  # Wait before checking again

            print("⏰ Timeout waiting for response")
            return "No response received within timeout period"

        except Exception as e:
            print(f"❌ Error waiting for response: {e}")
            return f"Error: {e}"

    def ask_question(self, question):
        """
        Ask a question to ChatGPT and get the response

        Args:
            question (str): The question to ask

        Returns:
            str: ChatGPT's response
        """
        if self.send_message(question):
            return self.wait_for_response()
        else:
            return "Failed to send message"

    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            print("🔒 Browser closed")

def main(email=None, password=None):
    """Main function to run the ChatGPT automation with login"""
    bot = None
    try:
        print("🚀 Starting ChatGPT Automation with Login...")

        # Initialize the bot
        bot = ChatGPTAutomationWithLogin(headless=False)

        # Visit ChatGPT
        bot.visit_chatgpt()

        # Attempt automatic login if credentials provided
        if email and password:
            login_success = bot.login(email, password)
            if not login_success:
                print("\n⚠️ Automatic login failed or requires manual intervention")
                print("Please complete login manually in the browser")
                print("Press Enter when ready to continue...")
                input()
        else:
            # Manual login
            print("\n" + "="*50)
            print("🔑 MANUAL LOGIN REQUIRED")
            print("="*50)
            print("1. If you need to log in to ChatGPT, please do so now")
            print("2. Complete any CAPTCHA if required")
            print("3. Make sure you're on the main chat page")
            print("4. Press Enter when ready to continue...")
            print("="*50)
            input()

        # Interactive loop
        print("\n🤖 ChatGPT Automation Ready!")
        print("Type your questions below (or 'quit' to exit)")
        print("-" * 50)

        while True:
            user_question = input("\n💬 Your question: ")

            if user_question.lower() in ['quit', 'exit', 'q']:
                break

            if user_question.strip():
                print("\n" + "="*60)
                print(f"❓ QUESTION: {user_question}")
                print("="*60)

                response = bot.ask_question(user_question)

                print(f"\n🤖 CHATGPT RESPONSE:")
                print("-" * 60)
                print(response)
                print("="*60)
            else:
                print("⚠️  Please enter a valid question.")

    except KeyboardInterrupt:
        print("\n\n⏹️  Script interrupted by user")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if bot:
            bot.close()
        print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()
