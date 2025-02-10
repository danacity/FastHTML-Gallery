from fasthtml.common import *

def interactable_elements(include_types=None):
    """Returns interact.js scripts based on specified types
    
    Args:
        include_types: List of strings specifying which interactable elements to include
                      Options: ['horizontal', 'vertical', 'panel']
    """
    base_script = Script(src="https://cdn.jsdelivr.net/npm/interactjs/dist/interact.min.js")
    
    scripts = {
        'horizontal': Script("""
            interact('.resizable')
            .resizable({
                edges: { right: true },
                listeners: {
                move: function (event) {
                    let target = event.target
                    let x = (parseFloat(target.getAttribute('data-x')) || 0)
                    target.style.width = `${event.rect.width}px`
                    target.setAttribute('data-x', x)
                }
                },
                modifiers: [
                interact.modifiers.restrictEdges({
                    min: { width: 200 },
                    max: { width: window.innerWidth - 200 }
                })
                ]
            });
        """),
        'vertical': Script("""
            interact('.resizable-height')
              .resizable({
                edges: { top: true },
                listeners: {
                  move: function (event) {
                    let target = event.target
                    let y = (parseFloat(target.getAttribute('data-y')) || 0)
                    target.style.height = `${event.rect.height}px`
                    target.setAttribute('data-y', y)
                  }
                },
                modifiers: [
                  interact.modifiers.restrictEdges({
                    min: { height: 200 },
                    max: { height: 500 }
                  })
                ]
            });
        """),
        'panel': Script("""
            interact('.panel-resizer')
            .resizable({
                edges: { left: true, right: true },
                listeners: {
                move: function (event) {
                    const target = event.target
                    const leftPanel = target.previousElementSibling;
                    const rightPanel = target.nextElementSibling;
                    
                    leftPanel.style.width = `${event.rect.left}px`
                    rightPanel.style.width = `${window.innerWidth - event.rect.right}px`
                }
                },
                modifiers: [
                interact.modifiers.restrictEdges({
                    inner: { left: 200, right: 200 }
                })
                ]
            });
        """)
    }
    
    if include_types is None:
        include_types = list(scripts.keys())
        
    return [base_script] + [scripts[t] for t in include_types if t in scripts]