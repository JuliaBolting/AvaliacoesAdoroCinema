import requests
from bs4 import BeautifulSoup

def extrairSinopseFilme(filme):
    url = f"https://www.adorocinema.com/filmes/{filme}/"
    html = requests.get(url).text
    bs = BeautifulSoup(html, 'html.parser')
    sinopse_div = bs.find('div', class_="content-txt")
    return sinopse_div.get_text(strip=True) if sinopse_div else "Sinopse não encontrada."

def extrairComentariosFilme(filme, n):
    comentarios = []
    for i in range(1, n+1):
        url = f"https://www.adorocinema.com/filmes/{filme}/criticas/espectadores/?page={i}"
        html = requests.get(url).text
        bs = BeautifulSoup(html, 'html.parser')
        comentarios_tag = bs.find_all('div', class_="content-txt review-card-content")
        for c in comentarios_tag:
            comentarios.append(c.get_text(strip=True))
    return comentarios
