from src.config import webBrowser


if __name__ == '__main__':
    driver = webBrowser.browser()
    driver.get("https://www.portoseguro.com.br/porto-seguro-saude/rede-referenciada")
    driver.close()

