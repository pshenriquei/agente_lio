import requests
from bs4 import BeautifulSoup

def baixar_documentacao_lio():
    url = "https://developercielo.github.io/manual/lio-local"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Erro ao baixar a documentação")

    soup = BeautifulSoup(response.text, "html.parser")
    
    # Remove navegação, scripts e estilos
    for tag in soup(["nav", "script", "style", "footer", "header"]):
        tag.decompose()
    
    # Extrai só o texto visível
    texto = soup.get_text(separator="\n", strip=True)
    
    return texto

if __name__ == "__main__":
    texto = baixar_documentacao_lio()

    with open("documento_lio.txt", "w", encoding="utf-8") as f:
        f.write(texto)

    print("✅ Documentação salva em documento_lio.txt")
