from fasthtml.common import *
from monsterui.all import *

hdrs = Theme.blue.headers()
app, rt = fast_app(hdrs=hdrs, live=True)

def make_folder(name, items=None):
    return Div(
        Div(
            Span("⋮", cls="text-secondary-foreground/50 mr-1 cursor-move handle"),
            Span("▾ " + name, 
                cls="cursor-pointer",
                hx_on_click="this.textContent = this.textContent.startsWith('▾') ? '▸ ' + this.textContent.slice(2) : '▾ ' + this.textContent.slice(2); this.parentElement.nextElementSibling.classList.toggle('hidden')"
            ),
            cls="p-2 bg-secondary/20 text-secondary-foreground flex items-center",
        ),
        Div(*items, cls="ml-4 sortable") if items else "",
        cls="folder"
    )

def make_file(name):
    return Div(
        Span("⋮", cls="text-primary/50 mr-1 cursor-move handle"),
        name,
        cls="p-2 bg-primary/10 text-primary flex items-center"
    )

@rt('/toggle-nav')
def toggle_nav(show: str):
    show = show.lower() == 'true'
    file_system = Div(
        make_folder("Documents", [
            make_file("note1.txt"),
            make_folder("Projects", [
                make_file("project1.py"),
                make_file("readme.md")
            ]),
        ]),
        make_folder("Images", [
            make_file("photo1.jpg"),
            make_file("photo2.jpg")
        ]),
        cls="sortable"
    )
    
    return Div(
        NavContainer(
            NavHeaderLi("File System"),
            file_system,
            uk_nav=True,
            cls="bg-card p-4 w-64 min-h-screen border-r"
        ) if show else '',
        id="nav-content"
    )

@rt
def index():
    return Container(
        Div(
            Button("☰", cls="p-2",
                hx_get="/toggle-nav?show=true",
                hx_target="#nav-content",
                hx_swap="outerHTML"
            ),
            H1("File System", cls="text-2xl font-bold ml-4"),
            cls="w-full p-4 border-b bg-card flex items-center"
        ),
        DivLAligned(
            DivCentered(id="nav-content"),
            cls="flex"
        ),
        Script("""
            import Sortable from 'https://cdn.jsdelivr.net/npm/sortablejs@1.15.0/modular/sortable.esm.js';
            proc_htmx('.sortable', e => Sortable.create(e, {
                group: 'nested',
                animation: 150,
                fallbackOnBody: true,
                swapThreshold: 0.65,
                ghostClass: 'opacity-50',
                handle: '.handle'
            }));
        """, type='module'),
        cls="min-h-screen flex flex-col"
    )

serve()
