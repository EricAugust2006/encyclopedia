from django.shortcuts import render
import markdown2
from . import util


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

    for entry in entries:
        if entry.lower() == query:
            return render(
                request,
                "encyclopedia/entry.html",
                {"entry": entry, "content": markdown2.markdown(util.get_entry(entry)) },
            )
        # matching_entries = [entry for entry in entries if query in entry.lower()]
        # return render(
        #     request,
        #     "encyclopedia/search_result.html",
        #     {"query": query, "entries": matching_entries},
        # )
