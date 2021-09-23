from src.config import webBrowser
from src.site import index


if __name__ == '__main__':
    driver = webBrowser.browser()
    index.navegacao(driver=driver)
    # driver.close()

