from .palavras import palavras_positivas, palavras_negativas

def classificarComentarios(comentarios):
    resultados = []
    for comentario in comentarios:
        total_positivas = sum(len(p.findall(comentario)) for p in palavras_positivas)
        total_negativas = sum(len(n.findall(comentario)) for n in palavras_negativas)

        if total_positivas > total_negativas:
            categoria = "POSITIVA"
        elif total_negativas > total_positivas:
            categoria = "NEGATIVA"
        else:
            categoria = "NEUTRA"
        resultados.append((comentario, categoria))
    return resultados