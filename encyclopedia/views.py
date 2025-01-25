from django.shortcuts import render, redirect
import markdown2
from . import util
from difflib import get_close_matches
from django.core.exceptions import ValidationError
from django.http import HttpResponse
import os

def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry(request, title):
    content = util.get_entry(title)
    return render(
        request,
        "encyclopedia/entry.html",
        {"entry": title, "content": markdown2.markdown(content)},
    )


def search(request):
    query = request.GET.get("q").lower()
    entries = util.list_entries()

    # Verifica se a entrada exata existe
    if query in (entry.lower() for entry in entries):
        entry = next(entry for entry in entries if entry.lower() == query)
        return render(
            request,
            "encyclopedia/entry.html",
            {"entry": entry, "content": markdown2.markdown(util.get_entry(entry))},
        )

    # Se não encontrar uma entrada exata, procura por entradas semelhantes
    matching_entries = get_close_matches(query, entries, n=5, cutoff=0.6)

    return render(
        request,
        "encyclopedia/search_result.html",
        {
            "query": query,
            "entries": matching_entries,
            "suggestion": matching_entries[0] if matching_entries else None,
        },
    )

def create_page(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        # Verificar se o título já existe
        if util.get_entry(title):
            return render(request, "encyclopedia/create_page.html", {
                "message": "Já existe uma página com esse título."
            })
        
        # Defina o caminho para o diretório 'entries'
        entries_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'entries')
        
        # Certifique-se de que o diretório 'entries' exista
        if not os.path.exists(entries_dir):
            os.makedirs(entries_dir)
        
        # Caminho completo para o arquivo .md
        file_path = os.path.join(entries_dir, f"{title}.md")

        # Salvar o conteúdo no arquivo .md
        with open(file_path, "w") as file:
            file.write(content)

        return redirect(f"/wiki/{title}")  # Redirecionar para a página recém-criada

    return render(request, "encyclopedia/create_page.html")