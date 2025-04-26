import re

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