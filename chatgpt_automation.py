import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class ChatGPTAutomation:
    def __init__(self, headless=False):
        """
        Initialize the ChatGPT automation bot
        
        Args:
            headless (bool): Whether to run browser in headless mode
        """
        self.driver = None
        self.headless = headless
        self.setup_driver()
    
    def setup_driver(self):
        """Setup Chrome WebDriver with appropriate options"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")
        
        # Add other useful options
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Initialize the driver
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
    def visit_chatgpt(self):
        """Navigate to ChatGPT website"""
        print("Visiting ChatGPT...")
        self.driver.get("https://chat.openai.com")
        
        # Wait for the page to load
        time.sleep(3)
        
    def wait_for_input_ready(self, timeout=30):
        """Wait for the input field to be ready"""
        try:
            # Try different possible selectors for the input field
            selectors = [
                "textarea[placeholder*='Message']",
                "textarea[data-id='root']",
                "#prompt-textarea",
                "textarea",
                "[contenteditable='true']"
            ]
            
            for selector in selectors:
                try:
                    element = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    print(f"Found input field with selector: {selector}")
                    return element
                except TimeoutException:
                    continue
            
            raise TimeoutException("Could not find input field")
            
        except TimeoutException:
            print("Timeout waiting for input field to be ready")
            return None
    
    def send_message(self, message):
        """
        Send a message to ChatGPT
        
        Args:
            message (str): The message to send
        """
        print(f"Sending message: {message}")
        
        # Wait for input field to be ready
        input_field = self.wait_for_input_ready()
        if not input_field:
            print("Could not find input field")
            return False
        
        # Clear any existing text and send the message
        input_field.clear()
        input_field.send_keys(message)
        
        # Wait a moment for the text to be entered
        time.sleep(1)
        
        # Send the message (usually Enter key or click send button)
        input_field.send_keys(Keys.RETURN)
        
        return True
    
    def wait_for_response(self, timeout=60):
        """
        Wait for ChatGPT to respond and return the response text
        
        Args:
            timeout (int): Maximum time to wait for response
            
        Returns:
            str: The response text from ChatGPT
        """
        print("Waiting for ChatGPT response...")
        
        try:
            # Wait for the response to appear
            # Look for the response container
            response_selectors = [
                "[data-message-author-role='assistant']",
                ".markdown",
                "[class*='response']",
                "[class*='message']"
            ]
            
            start_time = time.time()
            while time.time() - start_time < timeout:
                for selector in response_selectors:
                    try:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        if elements:
                            # Get the last response (most recent)
                            last_response = elements[-1]
                            response_text = last_response.text.strip()
                            
                            if response_text and len(response_text) > 10:  # Ensure it's a substantial response
                                print("Response received!")
                                return response_text
                    except:
                        continue
                
                time.sleep(2)  # Wait before checking again
            
            print("Timeout waiting for response")
            return "No response received within timeout period"
            
        except Exception as e:
            print(f"Error waiting for response: {e}")
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

def main():
    """Main function to run the ChatGPT automation"""
    bot = None
    try:
        # Initialize the bot
        bot = ChatGPTAutomation(headless=False)  # Set to True for headless mode
        
        # Visit ChatGPT
        bot.visit_chatgpt()
        
        # Wait for user to potentially log in manually
        print("\nIf you need to log in to ChatGPT, please do so now.")
        print("Press Enter when ready to continue...")
        input()
        
        # Interactive loop
        while True:
            user_question = input("\nEnter your question for ChatGPT (or 'quit' to exit): ")
            
            if user_question.lower() in ['quit', 'exit', 'q']:
                break
            
            if user_question.strip():
                print("\n" + "="*50)
                response = bot.ask_question(user_question)
                print("ChatGPT Response:")
                print("-" * 30)
                print(response)
                print("="*50)
            else:
                print("Please enter a valid question.")
    
    except KeyboardInterrupt:
        print("\nScript interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if bot:
            bot.close()
        print("Browser closed. Goodbye!")

if __name__ == "__main__":
    main()
