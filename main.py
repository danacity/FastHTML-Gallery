from fasthtml.common import *
import configparser, os
from pathlib import Path
from utils import * 
from importlib import import_module
from monsterui.all import *

BASE_CONFIG = {
    'author_name': 'Efels',
    'base_name': 'FastHTML Gallery',
    'domain': 'gallery.efels.com',
    'twitter': '@efels',
    'description': 'A collection of FastHTML components and examples',
    'community_show_all': 'Show Full Community Gallery',
    'community_show_author': 'Show Efels Gallery Only',
    'animations_on': 'Turn Off Animations',
    'animations_off': 'Turn On Animations'
}

def get_site_config(show_community=False, animations_on=True):
    return {
        **BASE_CONFIG,
        'name': f"{BASE_CONFIG['base_name']}" if show_community else f"{BASE_CONFIG['author_name']}'s {BASE_CONFIG['base_name']}",
        'base_url': f"https://{BASE_CONFIG['domain']}",
        'community_default_on': show_community,
        'animations_default_on': animations_on
    }

def get_button_text(is_enabled, button_type):
    if button_type == 'community':
        key = 'community_show_author' if is_enabled else 'community_show_all'
    else:
        key = f'{button_type}_on' if is_enabled else f'{button_type}_off'
    return BASE_CONFIG[key]

def get_route(p): return '/'.join(Path(p).parts[1:])
def get_module_path(p,base_dir): return f'{base_dir}.{".".join(Path(p).parts[1:])}.app'

toggle_script = Script("""
    function toggleAnimations() {
        const images = document.querySelectorAll('.card-img-top');
        images.forEach(img => {
            if (img.src.endsWith('.gif')) {
                img.src = img.getAttribute('data-png');
            } else {
                img.setAttribute('data-png', img.src);
                img.src = img.src.replace('card_thumbnail.png', 'card_thumbnail.gif');
            }
        });
    }""")


application_routes = [Mount(f"/app/{get_route(root)}", import_module(get_module_path(root,'examples')).app) for root, dirs, files in os.walk('examples') if 'app.py' in files]

descr = 'A gallery of FastHTML components... (Version 1 leftover, not used in Version 2)'

# hdrs = (
#     *Socials(title='FastHTML Gallery', description=descr, site_name='gallery.fastht.ml', twitter_site='@isaac_flath', image=f'/social.png', url=''),
#     toggle_script,
#     *Theme.blue.headers(highlightjs=True),)

hdrs = (
    *interactable_elements(['horizontal']),  # Only include what we need
    *Socials(title=get_site_config()['name'], 
             description=BASE_CONFIG['description'], 
             site_name=BASE_CONFIG['domain'], 
             twitter_site=BASE_CONFIG['twitter'],
             image=f'/social.png', 
             url=f"https://{BASE_CONFIG['domain']}"),
    toggle_script,
    *Theme.blue.headers(highlightjs=True),)

app = FastHTML(routes=application_routes+ [Mount('/files', StaticFiles(directory='.')),], hdrs=hdrs, pico=False)

def NavBar(dir_path, info=True, active=''):
    nav_items = [
        Li(A("Back to Gallery", href="/")),
        Li(A("Split", href=f"/split/{dir_path.parts[1]}/{dir_path.parts[2]}"), cls='uk-active' if active == 'split' else ''),
        Li(A("Code", href=f"/code/{dir_path.parts[1]}/{dir_path.parts[2]}"), cls='uk-active' if active == 'code' else ''),
        Li(A("App",  href=f"/app/{dir_path.parts[1]}/{dir_path.parts[2]}"), cls='uk-active' if active == 'app' else '')]
    
    if info:nav_items.insert(1, Li(A("Info", href=f"/info/{dir_path.parts[1]}/{dir_path.parts[2]}"), cls='uk-active' if active == 'info' else ''))
        
    return NavBarContainer(
            NavBarLSide(H1(f"{dir_path.name.replace('_',' ').title()}"), cls="hidden md:block"),
            NavBarRSide(NavBarNav(*nav_items)))

@app.get('/code_view/{category}/{project}')
def code_view(category: str, project: str):
   dir_path = Path('examples')/category/project
   code_text = (dir_path/'app.py').read_text().strip()
   return Style("""
       body { margin: 0; padding: 20px; }
       .code-wrap { min-width: 1000px; }
       pre { margin: 0; }
   """), Div(Pre(Code(code_text, cls='language-python')), cls='code-wrap')


def CustomRange(*c, cls=(), **kwargs):
    svg = """<svg xmlns="https://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="">
      <circle cx="12" cy="12" r="12" fill="#9ca3af"/>
      <line x1="12" x2="12" y1="3" y2="21"></line>
      <polyline points="8 8 4 12 8 16"></polyline>
      <polyline points="16 16 20 12 16 8"></polyline>
    </svg>"""
    
    data_url = f"data:image/svg+xml;base64,{base64.b64encode(svg.encode()).decode()}"
    
    custom_cls = f"""
        h-10 my-4
        [&::-webkit-slider-thumb]:appearance-none 
        [&::-webkit-slider-thumb]:h-10 
        [&::-webkit-slider-thumb]:w-10 
        [&::-webkit-slider-thumb]:rounded-full 
        [&::-webkit-slider-thumb]:bg-[url('{data_url}')] 
        [&::-webkit-slider-thumb]:bg-cover
        [&::-webkit-slider-track]:appearance-none
        [&::-webkit-slider-track]:bg-transparent
        [&::-webkit-slider-track]:border-0
        appearance-none
        bg-transparent
        border-0
        outline-0
        focus:outline-none
        focus:ring-0
        focus:border-0
    """
    return Input(*c, cls=(custom_cls, cls), type='range', **kwargs)

@app.get('/split/{category}/{project}')
def split_view(category: str, project: str):
    dir_path = Path('examples')/category/project
    info = (dir_path/'info.md').exists()
    
    return (
        NavBar(dir_path, info=info, active='split'),
        Title(f"{dir_path.name} - Split View"),
        Div(
            Div(Iframe(src=f"/code_view/{category}/{project}/",
                      style="width: 100%; height: 100%; border: none;"), 
                id="code-section",
                style="height: calc(90vh); width: 50%; overflow: auto;"),  
            Div(Iframe(src=f"/app/{category}/{project}/",
                      style="width: 100%; height: calc(90vh); border: none;"),
                id="preview-section",
                style="height: calc(90vh); width: 50%;"),
            style="display: flex; width: 100%;"),
        Div(
            Div(CustomRange(min=20, max=80, value=50,
                     cls="w-full h-4 cursor-pointer [&::-webkit-slider-thumb]:w-8  [&::-webkit-slider-thumb]:h-8 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-gray-500",
                     oninput="updateSplit(this.value)"),
                style="width: 60%; margin: 0 20%;"),
            style="position: fixed; bottom: 0; left: 0; right: 0; margin: 0;",
            cls="mt-0 space-y-0"
        ),
        Script("""
            function updateSplit(value) {
                document.getElementById('code-section').style.width = value + '%';
                document.getElementById('preview-section').style.width = (100 - value) + '%';
            }
        """),
    )

@app.get('/code/{category}/{project}')
def application_code(category:str, project:str):
    dir_path = Path('examples')/category/project
    code_text = (dir_path/'app.py').read_text().strip()
    info = (dir_path/'info.md').exists()
    return  (NavBar(dir_path, info=info, active='code'), Title(f"{dir_path.name} - Code"), Container(Pre(Code(code_text, cls='language-python'))))
    
@app.get('/info/{category}/{project}')
def application_info(category:str, project:str):
    dir_path = Path('examples')/category/project
    md_text = (dir_path/'info.md').read_text()
    return (NavBar(dir_path, info=True, active='info'), Title(f"{dir_path.name} - Info"), Container(render_md(md_text)))

def component_meta(dir_path):
    metadata = configparser.ConfigParser()
    meta_path = dir_path/'metadata.ini'
    metadata.read(meta_path)
    if 'REQUIRED' not in metadata.sections():
        return {}
    meta = dict(metadata['REQUIRED'])
    return {'name': meta['componentname'],
            'description': meta['componentdescription'],
            'is_community': meta.get('ismainrepo','true').lower()=='true',
            'text_md_exists': (dir_path/'info.md').exists(),
            'dpath': f"{dir_path.parts[1]}/{dir_path.parts[2]}"}

def make_buttons(dpath, text_md_exists):
    return [A(Button("Split", cls=ButtonT.primary), href=f"/split/{dpath}"), 
            A(Button("Code", cls=ButtonT.secondary), href=f"/code/{dpath}"), 
            A(Button("App"), href=f"/app/{dpath}"), 
            A(Button("Info"), href=f"/info/{dpath}") if text_md_exists else None]

def ImageCard(dir_path, animations_on=True):
    meta = component_meta(dir_path)
    img_type = 'gif' if animations_on else 'png'
    return Card(A(Img(src=f"/files/{dir_path}/card_thumbnail.{img_type}", 
                      style="width: 100%; height: 350px; object-fit: cover;", 
                      loading="lazy", 
                      cls="card-img-top"), 
                      href=f"/split/{meta['dpath']}"), 
                Div(P(meta['name'], cls=(TextT.bold, TextT.lg)), 
                    render_md(P(meta['description'])), style="height: 150px; overflow: auto;"), 
                footer=DivFullySpaced(*make_buttons(meta['dpath'], meta['text_md_exists'])))

directories = [Path(f"examples/{x}") for x in ['dynamic_user_interface_(htmx)','visualizations','widgets','svg','todo_series','applications']]

def is_example_dir(d, show_community=True):
    if not (d.is_dir() and not d.name.startswith('_') and (d/'metadata.ini').exists()):
        return False
    meta = component_meta(d)
    return True if show_community else not meta['is_community']

@app.get("/")
def homepage(show_community: bool=False, animations_on: bool=True):
    site_config = get_site_config(show_community, animations_on)
    all_cards = []
    for section in directories:
        cards = [ImageCard(dir, animations_on) for dir in sorted(section.iterdir()) if is_example_dir(dir, show_community)]
        if cards:
            all_cards.append(Section(Details(Summary(H1(section.name.replace('_',' ').title(), cls='mt-6 mb-4 pb-2 text-center text-3xl font-bold border-b-2 border-gray-300')), 
                                             Grid(*cards, cols_min=1, cols_sm=1, cols_md=2, cols_lg=3, cols_xl=3), cls='pt-6', open=True)))
    return (NavBarContainer(NavBarLSide(H1(site_config['name'])), 
                            NavBarRSide(A(Button(get_button_text(animations_on,'animations')), href=f"/?show_community={show_community}&animations_on={not animations_on}"), 
                                        A(Button(get_button_text(show_community,'community')), href=f"/?show_community={not show_community}&animations_on={animations_on}"), 
                                        A(Button("Table View"), href=f"/table?show_community={show_community}&animations_on={animations_on}"))), 
            Container(*all_cards))

def TableRow(dir_path):
    meta = component_meta(dir_path)
    return Tr(Td(meta['name']), Td(render_md(meta['description'])), Td(DivLAligned(*make_buttons(meta['dpath'], meta['text_md_exists']), cls='uk-table-shrink')))

def SectionTable(section, show_community=True):
    section_id = f"section-{section.name}"
    rows = [TableRow(dir) for dir in sorted(section.iterdir()) if is_example_dir(dir, show_community)]
    if not rows: return None
    return Section(Details(
            Summary(H1(section.name.replace('_',' ').title(), 
                       cls='mt-6 mb-4 pb-2 text-center text-3xl font-bold border-b-2 border-gray-300 cursor-pointer')), 
            Table(
                Thead(Tr(map(Th, ("Component", "Description", "Actions")))),
                Tbody(*rows), cls=(TableT.middle, TableT.divider, TableT.hover, TableT.sm)), 
                id=section_id, open=True), cls='py-2')

@app.get("/table")
def table_view(show_community: bool=False, animations_on: bool=True):
    site_config = get_site_config(show_community, animations_on)
    return (NavBarContainer(NavBarLSide(H1(f"{site_config['name']} - Table View")), NavBarRSide(A(Button(get_button_text(animations_on,'animations')), href=f"/table?show_community={show_community}&animations_on={not animations_on}"), A(Button(get_button_text(show_community,'community')), href=f"/table?show_community={not show_community}&animations_on={animations_on}"), A(Button("Card View"), href=f"/?show_community={show_community}&animations_on={animations_on}"))), Container(*[SectionTable(section, show_community) for section in directories if SectionTable(section, show_community)]))

serve()