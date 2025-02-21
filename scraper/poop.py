from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def log_request_headers(request):
    headers = request['headers']
    print("Request Headers:", headers)

class Poop:
    """
    Poop Scraper
    Author: Sandy Pratama
    """
    def __init__(self, uri) -> None:
        self.url = uri
        self.driver = self._driver()
        self.content = self._content()

    def _driver(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--enable-unsafe-swiftshader')
        driver = webdriver.Chrome(options=options)
        driver.execute_cdp_cmd('Network.enable', {})
        return driver
    
    def _content(self) -> dict:
        driver = self.driver
        try:
            link = self.url.split("/e/")[1]
            driver.get(f"https://poop.name/dl2?poop_id={link}")
            download = driver.execute_script("return fetchDirectLink()")
            html = soup(driver.page_source, "html.parser")
            message = html.find("div", {"class": "w3-button"})
            return {
                "status": "true",
                "title": html.find("h1").text,
                "message": message.text,
                "link": download
            }
        except Exception as e:
            return {
                "status": "false",
                "message": e
            }
        finally:
            driver.quit()