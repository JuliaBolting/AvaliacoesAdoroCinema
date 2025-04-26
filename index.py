import tkinter as tk
from tkinter import messagebox, scrolledtext
import os
import re
import requests
from bs4 import BeautifulSoup

diretorio = 'arquivosTXT'
os.makedirs(diretorio, exist_ok=True)

palavras_positivas = [
    re.compile(r"\bbom\b", re.IGNORECASE),
    re.compile(r"\blegal\w*\b", re.IGNORECASE),
    re.compile(r"\binteressante\b", re.IGNORECASE),
    re.compile(r"\bdivertid\w+\b", re.IGNORECASE),
    re.compile(r'\bam\w+\b', re.IGNORECASE),
    re.compile(r'\bgost\w+\b', re.IGNORECASE),
    re.compile(r"\bador\w+\b", re.IGNORECASE),
    re.compile(r"\bincrível\b", re.IGNORECASE),
    re.compile(r"\bimpressionante\b", re.IGNORECASE),
    re.compile(r"\brecomendo\b", re.IGNORECASE)
]

palavras_negativas = [
    re.compile(r"\bruim\b", re.IGNORECASE),
    re.compile(r"\bpessim\w+\b", re.IGNORECASE),
    re.compile(r"\bchat\w+\b", re.IGNORECASE),
    re.compile(r"\bterrível\b", re.IGNORECASE),
    re.compile(r"\bsem graça\b", re.IGNORECASE),
    re.compile(r"\bfraco\b", re.IGNORECASE),
    re.compile(r"\bmau\b", re.IGNORECASE),
    re.compile(r"\birritante\b", re.IGNORECASE),
    re.compile(r"\bdá raiva\b", re.IGNORECASE),
    re.compile(r"\bfrustrante\b", re.IGNORECASE),
    re.compile(r"\bdecepcionante\b", re.IGNORECASE),
]

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

def salvarArquivo(nome, conteudo):
    caminho = os.path.join(diretorio, nome)
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    return caminho

def classificarComentarios(comentarios):
    resultados = []
    for comentario in comentarios:
        positiva = any(p.search(comentario) for p in palavras_positivas)
        negativa = any(n.search(comentario) for n in palavras_negativas)
        if positiva and not negativa:
            categoria = "POSITIVA"
        elif negativa and not positiva:
            categoria = "NEGATIVA"
        else:
            categoria = "NEUTRA"
        resultados.append((comentario, categoria))
    return resultados

def extrairTudo():
    filme = entrada_filme.get().strip()
    paginas = entrada_paginas.get().strip()
    if not filme or not paginas.isdigit():
        messagebox.showwarning("Aviso", "Preencha código do filme e número de páginas válidos!")
        return
    n_paginas = int(paginas)

    sinopse = extrairSinopseFilme(filme)
    caminho_sinopse = salvarArquivo(f"{filme}_sinopse.txt", sinopse)
    comentarios = extrairComentariosFilme(filme, n_paginas)
    caminho_comentarios = salvarArquivo(f"{filme}_comentarios.txt", "\n\n".join(comentarios))

    resultados = classificarComentarios(comentarios)
    total = len(resultados)
    pos = sum(1 for _, c in resultados if c=="POSITIVA")
    neg = sum(1 for _, c in resultados if c=="NEGATIVA")
    neu = sum(1 for _, c in resultados if c=="NEUTRA")

    comentarios_classificados = "\n\n".join([f"[{categoria}] {comentario}" for comentario, categoria in resultados])
    caminho_classificados = salvarArquivo(f"{filme}_comentarios_classificados.txt", comentarios_classificados)

    texto_extraido.config(state="normal")
    texto_extraido.delete('1.0', tk.END)
    texto_extraido.insert(tk.END, f"Sinopse salva em: {caminho_sinopse}\n")
    texto_extraido.insert(tk.END, f"Comentários salvos em: {caminho_comentarios}\n")
    texto_extraido.insert(tk.END, f"Classificados salvos em: {caminho_classificados}\n\n")
    texto_extraido.insert(tk.END, f"Resumo da Classificação:\n")
    texto_extraido.insert(tk.END, f"Total: {total}\n")
    texto_extraido.insert(tk.END, f"POSITIVOS: {pos} ({pos/total*100:.2f}%)\n")
    texto_extraido.insert(tk.END, f"NEGATIVOS: {neg} ({neg/total*100:.2f}%)\n")
    texto_extraido.insert(tk.END, f"NEUTROS: {neu} ({neu/total*100:.2f}%)\n\n")
    texto_extraido.insert(tk.END, f"Sinopse:\n{sinopse}\n\n")
    for comentario, categoria in resultados:
        texto_extraido.insert(tk.END, f"[{categoria}] {comentario}\n\n", categoria)
    texto_extraido.config(state="disabled")
    messagebox.showinfo("Sucesso", "Arquivos extraídos e classificados com sucesso!")

janela = tk.Tk()
janela.title("Extrator de Filmes - AdoroCinema")
janela.geometry('800x600')
janela.config(bg="#f0f0f0")

frame_topo = tk.Frame(janela, bg="#f0f0f0")
frame_topo.pack(pady=10)
label1 = tk.Label(frame_topo, text="Código do Filme:", font=("Arial", 12), bg="#f0f0f0")
label1.grid(row=0, column=0, padx=5, pady=5, sticky='e')
entrada_filme = tk.Entry(frame_topo, width=30, font=("Arial", 12))
entrada_filme.grid(row=0, column=1, padx=5, pady=5)
label2 = tk.Label(frame_topo, text="Nº de Páginas:", font=("Arial", 12), bg="#f0f0f0")
label2.grid(row=1, column=0, padx=5, pady=5, sticky='e')
entrada_paginas = tk.Entry(frame_topo, width=10, font=("Arial", 12))
entrada_paginas.grid(row=1, column=1, padx=5, pady=5, sticky='w')

dr_frame = tk.Frame(janela, bg="#f0f0f0")
btn_extrair = tk.Button(dr_frame, text="Extrair Sinopse e Classificar comentários", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=extrairTudo)
btn_extrair.pack(padx=10)
dr_frame.pack(pady=10)

texto_extraido = scrolledtext.ScrolledText(janela, wrap=tk.WORD, width=90, height=25, font=("Arial", 12))
texto_extraido.pack(padx=10, pady=10)
texto_extraido.config(state="disabled")

texto_extraido.tag_configure("POSITIVA", foreground="green", justify='right', font=("Arial", 12), lmargin1=150, lmargin2=150, rmargin=10, spacing3=10)
texto_extraido.tag_configure("NEGATIVA", foreground="red", justify='left', font=("Arial", 12), lmargin1=10, lmargin2=10, rmargin=150, spacing3=10)
texto_extraido.tag_configure("NEUTRA", foreground="gray", justify='center', font=("Arial", 12), lmargin1=80, lmargin2=80, rmargin=80, spacing3=10)

janela.mainloop()

