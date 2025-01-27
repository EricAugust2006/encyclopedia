from turtle import title
from django.shortcuts import render, redirect
from django.urls import reverse
import markdown2
from . import util
from difflib import get_close_matches
from django.core.exceptions import ValidationError
from django.http import HttpResponse
import os
import random

def index(request): # renderiza a pagina index.html
    return render(request, "encyclopedia/index.html", { # renderiza a pagina index.html
        "entries": util.list_entries() # pega a lista de titulos
        })


def entry(request, title): # renderiza a pagina entry.html
    content = util.get_entry(title) # pega o conteudo do arquivo .md
    return render( request, "encyclopedia/entry.html", { # renderiza a pagina entry.html
        "entry": title,  # passa o titulo da pagina
        "content": markdown2.markdown(content) # renderiza o conteudo da pagina
        },
    )


def search(request): # renderiza a pagina search.html
    query = request.GET.get("q").lower() # pega o que foi digitado na barra de pesquisa
    entries = util.list_entries() # pega a lista de titulos

    # Verifica se a entrada exata existe
    if query in (entry.lower() for entry in entries): # verifica se a entrada exata existe
        entry = next(entry for entry in entries if entry.lower() == query) # pega o titulo da entrada exata
        return render( request, "encyclopedia/entry.html", { # renderiza a pagina entry.html
            "entry": entry, "content": markdown2.markdown(util.get_entry(entry)) # renderiza a pagina entry.html com o conteudo da entrada
            },
        )

    # Se não encontrar uma entrada exata, procura por entradas semelhantes
    matching_entries = get_close_matches(query, entries, n=5, cutoff=0.6)

    return render(request, "encyclopedia/search_result.html", { # renderiza a pagina search_result.html
    # parte obvia ja
            "query": query, 
            "entries": matching_entries,
            "suggestion": matching_entries[0] if matching_entries else None,
        },
    )

def create_page(request):
    if request.method == "POST": # verifica se o metodo é post
        title = request.POST.get("title") # pega titulo
        content = request.POST.get("content") # pega conteudo

        if util.get_entry(title): # verifica se o titulo existe
            return render(request, "encyclopedia/create_page.html", { # renderiza a pagina create_page.html
                "message": "Já existe uma página com esse título." # mensagem de erro
            })
        
        # Define o caminho para o diretório 'entries'
        entries_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'entries')
        
        if not os.path.exists(entries_dir): # verifica se o diretório 'entries' existe
            os.makedirs(entries_dir) #se nao, cria
        
        file_path = os.path.join(entries_dir, f"{title}.md") # caminho completo para o arquivo .md

        with open(file_path, "w") as file: # abre o arquivo .md 
            file.write(content) # escreve o conteudo

        return redirect(f"/wiki/{title}")  # redireciona para a página recém-criada

    return render(request, "encyclopedia/create_page.html")

def edit_page(request, title):
    if title in util.list_entries(): ## aqui verifica se o titulo existe
        if request.method == "POST":       ## aqui verifica se o o metodo é post
            new_content = request.POST.get("content") ## aqui verifica se o conteudo foi recebido
            util.save_entry(title, new_content) ## aqui salva o conteudo no arquivo .md
            print(new_content)
            return redirect(reverse("entry", args=[title])) ## aqui redireciona para a pagina editada com o nome entry da url e o argumento title que significa o titulo da pagina ex: /wiki/Entrada
        # se o metodo nao for post, renderiza a pagina edit_page.html
        else:
            content = util.get_entry(title) ## aqui pega o conteudo do arquivo .md
            print(content)
            return render(request, "encyclopedia/edit_page.html", { ## aqui renderiza a pagina edit_page.html
                "title": title,
                "content": content,
            })
    print("Page not found.")        
    return render(request, "encyclopedia/error.html", {
        "message": "Page not found."
        })

def random_page(request):
    entries = util.list_entries() # aqui pega a lista de titulos
    if not entries:  # se nao houver titulos
        return render(request, "encyclopedia/error.html", {
            "message": "Nenhuma página encontrada."
            })
    random_title = random.choice(entries) # aqui pega um titulo aleatorio da lista
    return redirect(f"/wiki/{random_title}") # aqui redireciona para a pagina
        
def delete_page(request, title):
    if title in util.list_entries():
        os.remove(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'entries', f"{title}.md"))
        return redirect(reverse("index"))
    return render(request, "encyclopedia/delete_page.html")