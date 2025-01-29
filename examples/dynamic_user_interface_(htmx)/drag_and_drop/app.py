from fasthtml.common import *
from monsterui.all import *

hdrs = Theme.blue.headers()

app, rt = fast_app(hdrs=hdrs)

@rt
def index():
    return Container(
        Div(
            H1("Drag and Drop Demo", cls="text-5xl font-bold mb-6"),
            Div(
                *[Div(f"Item {i}", 
                      cls="bg-blue-500 rounded-lg p-8 text-white hover:cursor-grab") 
                  for i in range(1, 9)],
                cls="grid gap-2 grid-cols-2 md:grid-cols-4 sortable"
            )
        ),
        Script("""
            import {Sortable} from 'https://cdn.jsdelivr.net/npm/sortablejs@1.15.0/modular/sortable.esm.js';
            proc_htmx('.sortable', e => Sortable.create(e, {
                animation: 500,
                ghostClass: 'opacity-50'
            }));
        """, type='module')
    )
