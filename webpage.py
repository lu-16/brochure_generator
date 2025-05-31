from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


class Webpage:
    def __init__(self, url):
        self.url = url
        self.title = ""
        self.body = ""
        self.content = ""
        self.links = []
        self.extract_text_from_url(url)

    def extract_text_from_url(self, url):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                options = webdriver.ChromeOptions()
                options.add_argument("--headless")  # Run in headless mode
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                driver = webdriver.Chrome(
                    service=Service(ChromeDriverManager().install()), options=options
                )
                driver.get(url)
                self.body = driver.page_source
                driver.quit()
                soup = BeautifulSoup(self.body, "html.parser")
                self.title = soup.title.string if soup.title else ""
                for irrelevant in soup.body(["script", "style", "img", "input"]):
                    irrelevant.decompose()
                self.content = soup.body.get_text(separator="\n", strip=True) if soup.body else ""
                self.links = [a["href"] for a in soup.find_all("a", href=True)]
                break  # Success, exit the retry loop
            except Exception as e:
                print(f"Error fetching {url} (attempt {attempt + 1}): {str(e)}")
                if attempt == max_retries - 1:
                    # On last attempt, re-raise or handle as needed
                    pass

    def __repr__(self):
        return f"Webpage(url={self.url}, title={self.title})"

    def __str__(self):
        return f"Webpage: {self.title} ({self.url})\nContent: {self.content[:100]}...\nLinks: {len(self.links)} found"
