from .palavras import palavras_positivas, palavras_negativas

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
