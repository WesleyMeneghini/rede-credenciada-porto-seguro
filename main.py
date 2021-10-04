from src.config import webBrowser
from src.site import app


if __name__ == '__main__':
    driver = webBrowser.browser()
    app.navegacao(driver=driver)
    driver.close()

