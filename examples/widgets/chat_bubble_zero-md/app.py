from fasthtml.common import *
from monsterui.all import *
from functools import partial
from fasthtml.components import Zero_md

'''
This is mainly just a rework of the  work of Isaac Flath blog post on rendering markdown in FastHTML using zero-md
-  https://isaac-flath.github.io/website/posts/boots/FasthtmlTutorial.html

if your intersted in other chatbox exampes, you can check out the following:
- https://gallery.fastht.ml/split/widgets/chat_bubble
- https://fasthtml-docs.demo.clace.io/tutorials/by_example.html#full-example-3---chatbot-example-with-daisyui-components
- ollama - https://gist.github.com/zhibor/6822d53214892f1c35b2161dc4c5128c
- HTML/CSS information about Chat Boxes -  https://strobecorp.com/html-chat-box/
'''

conversation = {
    "messages": [
        {
          "role": "user",
          "content": "Could you assist me in resolving the remaining two errors in my code? I've managed to correct one already."
        },
        {
          "role": "assistant",
          "content": "I'm glad to hear you've made progress and resolved one of the issues! Let's review your existing code to proceed further:\n\n```python\nprint(\"Starting up server...')\nprnt(\"local server is listening on port 8080\")\n```\nCould you specify which error you've addressed and share the updated code snippet? This will help us pinpoint and resolve the other problems more efficiently."
        },
        {
          "role": "user",
          "content": "Here is the corrected line: print(\"Starting up server...\")"
        },
        {
          "role": "assistant",
          "content": "Excellent work on correcting that error! Now let's analyze the other line in your code. Here's what it looks like now:\n\n```python\nprint(\"Starting up server...\")\nprnt(\"local server is listening on port 8080\")\n```\nCan you examine the second line and identify any discrepancies?\n\nReflect on the print functions we usually use in Python. Does anything in that line seem incorrect?"
        }
    ]
}

def render_local_md(md, css = ''):
    css_template = Template(Style(css), data_append=True)
    return Zero_md(css_template, Script(md, type="text/markdown"))

css = '.markdown-body {background-color: unset !important; color: unset !important;}'
_render_local_md = partial(render_local_md, css=css)

def ChatMessage(msg, render_md_fn=lambda x: x):
    md = render_md_fn(msg['content'])
    is_user = msg['role'] == 'user'
    
    return Div(
        Div(
            Div(msg['role'], cls="text-sm text-muted-foreground mb-2"),
            Div(md, 
                cls=f"p-4 rounded-lg shadow-sm {'bg-primary text-primary-foreground' if is_user else 'bg-secondary text-secondary-foreground'}"
            ),
            cls="inline-block max-w-3xl"
        ),
        cls=f"flex {'justify-end' if is_user else 'justify-start'} mb-4"
    )

hdrs = Theme.blue.headers() + [
    Script(type="module", src="https://cdn.jsdelivr.net/npm/zero-md@3?register")
]
app, rt = fast_app(hdrs=hdrs)

@rt
def index():
    chatbox = [ChatMessage(msg, render_md_fn=_render_local_md) for msg in conversation['messages']]
    
    return Container(
        Div(
            *chatbox,
            cls="p-4"
        ),
        cls="max-w-4xl mx-auto"
    )

if __name__ == "__main__":
    serve()