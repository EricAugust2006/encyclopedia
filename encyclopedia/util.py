import re
import os


from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    entries_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'entries')
    file_path = os.path.join(entries_dir, f"{title}.md")

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return file.read()
    else:
        return None
