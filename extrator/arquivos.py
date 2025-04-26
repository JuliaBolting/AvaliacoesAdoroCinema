import os

diretorio = 'arquivosTXT'
os.makedirs(diretorio, exist_ok=True)

def salvarArquivo(nome, conteudo):
    caminho = os.path.join(diretorio, nome)
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    return caminho
