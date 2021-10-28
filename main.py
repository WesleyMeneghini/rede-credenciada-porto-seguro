from datetime import datetime

from src.config import webBrowser
from src.services import apiWhats
from src.site import app


if __name__ == '__main__':
    formatHorario = "%d/%m/%Y, %H:%M:%S"
    mensagem = f"Inicio do script rede credenciada *(Porto Seguro)*: {datetime.now().strftime(formatHorario)}"
    apiWhats.sendMessageLog(message=mensagem, number="5511987168989")

    driver = webBrowser.browser()
    app.navegacao(driver=driver)

    mensagem = f"Final do processo - rede credenciada *(Porto Seguro)*: {datetime.now().strftime(formatHorario)}"
    apiWhats.sendMessageLog(message=mensagem, number="5511987168989")

    driver.close()

