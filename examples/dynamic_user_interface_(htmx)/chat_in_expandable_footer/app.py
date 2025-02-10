from fasthtml.common import *
from monsterui.all import *
from functools import partial
import json
import yaml
from datetime import datetime, date
from pathlib import Path
from utils import interactable_elements

hdrs = Theme.blue.headers() + [
   MarkdownJS(),
   HighlightJS(langs=['python', 'javascript', 'html', 'css']),
   *interactable_elements(['horizontal', 'vertical'])
]

app, rt = fast_app(hdrs=hdrs)


def load_mock_data():
   data_dir = Path("data")
   with open(data_dir / "conversation.json", "r") as f:
       conversation = json.load(f)
   
   def build_file_system(path):
       result = {}
       for item in path.iterdir():
           if item.is_file():
               result[item.name] = item.read_text()
           else:
               result[item.name] = build_file_system(item)
       return result
   
   file_system = build_file_system(data_dir / "files")
   return conversation, file_system

@rt('/file/{filename}')
def get_file(filename: str):
   conversation, file_system = load_mock_data()
   
   def find_file(structure, target):
       for name, contents in structure.items():
           if name == target and isinstance(contents, str):
               return contents
           elif isinstance(contents, dict):
               result = find_file(contents, target)
               if result is not None:
                   return result
       return None
   
   content = find_file(file_system, filename)
   return Div(
       render_md(content),
       cls="p-4"
   ) if content else "File not found"

def ChatMessage(msg):
   is_user = msg['role'] == 'user'
   rendered_content = render_md(msg['content'], 
       class_map={
           'p': 'text-sm leading-tight my-0',
           'pre': 'my-0 p-0',
           'code': 'text-xs inline-block p-0 bg-background'
       })
   
   return Div(
       DivLAligned(
           DiceBearAvatar(msg['role'], h=12, w=12),
           Div(rendered_content, 
               cls=f"p-1.5 rounded {'bg-primary text-primary-foreground' if is_user else 'bg-secondary text-secondary-foreground'}"
           ),
           cls="max-w-3xl items-start"
       ),
       cls=f"flex {'justify-end' if is_user else 'justify-start'} mb-0.5 px-4"
   )
@rt
def index():
   conversation, _ = load_mock_data()
   chatbox = [ChatMessage(msg) for msg in conversation['messages']]
   
   return Container(
       Div(cls="flex flex-col", style="height: calc(100vh - 50px)")(
           Div(cls="flex-grow overflow-y-auto min-h-[200px]")(
               H1("Main Content", )
           ),
           Div(cls="bg-secondary/10 border-t border-t-primary/50 resizable-height", 
               style="height: 300px; min-height: 150px; position: fixed; bottom: 0; left: 0; right: 0")(
               Div(cls="flex h-full flex-col bg-secondary/10")(
                   TabContainer(
                       Li(A("Global Chat", href='#', cls='uk-active, bg-card')),
                       Li(A("Document Chat", href='#')),
                       Li(A("Element Chat", href='#')),
                       uk_switcher='connect: #chat-content',
                       cls="bg-card",
                       alt=False
                   ),
                   Ul(id="chat-content", cls="uk-switcher flex-grow bg-card/20 overflow-y-auto")(
                       Li(Div(*chatbox, cls="p-0 space-y-1")),
                       Li(Div("Document Chat Content", cls="p-2")),
                       Li(Div("Element Chat Content", cls="p-2"))
                   ),
                   Div(cls="border-t border-t-primary/50 p-2 bg-card flex gap-2")(
                       Input(type="text", placeholder="Type a message...", cls="flex-grow p-2 rounded bg-secondary/90 border"),
                       Button("Send", cls="bg-primary text-primary-foreground hover:bg-primary/90 px-4 rounded")
                   )
               )
           )
       )
   )
if __name__ == "__main__":
   serve()
