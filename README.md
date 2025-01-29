# FastHTML-Gallery Theme

This is a fork of the amazing [FastHTML-Gallery](https://github.com/AnswerDotAI/FastHTML-Gallery) by Isaac Flath and AnswerDotAI team. The goal for this project was to allows FastHTML developers to showcase their components alongside community examples on their own blog or website. This way people that find your work can easiely see the work of the community. 

## Why This Fork?

This theme was created to help FastHTML developers showcase their work. It provides:
- A way to distinguish between your components and community examples
- Customizable site configuration(what you want the buttons to say and the annimation defaults)
- Easy integration with your existing blog or website

## Setup

To install the dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Customize the gallery by modifying the `BASE_CONFIG` in `main.py`:

```python
BASE_CONFIG = {
    'author_name': 'YourName',        # Your name or handle
    'base_name': 'FastHTML Gallery',  # Site title
    'domain': 'your.domain.com',      # Your domain
    'twitter': '@yourhandle',         # Your Twitter handle
    'description': 'Your description', # Site description
    
    # Button text customization
    'community_show_all': 'Show Full Community Gallery',   # Text when showing all examples
    'community_show_author': 'Show Your Gallery Only',     # Text when showing your examples
    'animations_on': 'Turn Off Animations',                # Text when animations are on
    'animations_off': 'Turn On Animations'                 # Text when animations are off
}
```

## Running

To run the project:

```bash
python main.py
```

## Contributing

### Adding Your Examples

1. Create an app that serves as an example. Make sure you can say in 1 simple sentence what the example is illustrating.
2. Create a new folder in an appropriate directory (e.g. `examples/widgets/` or `examples/visualizations/`) for your example.
3. Create an `app.py` file.  Things to know:
    + Use route names or relative paths, not absolute paths. This is because the app will be submounted.
    + The root route will be what is shown in the gallery
4. Add necessary metadata:
    + `card_thumbnail.png` and `card_thumbnail.gif` for the main page card
    + **Tip**: Add extra padding on the sides of your thumbnails and gifs so they display properly if you don't they may appear cropped, you might also need to clear your browers cached images and files
    + `metadata.ini` with component information
    + `info.md` (optional for examples, required for apps) for additional documentation
5. Run `python main.py` and verify everything looks correct

## Credit

This project is a fork of [FastHTML-Gallery](https://github.com/AnswerDotAI/FastHTML-Gallery) by Isaac Flath. The original gallery showcases common patterns in FastHTML apps including chat bubbles, cascading dropdowns, interactive charts, and more.

## Support

If you have any suggestions for improving this theme, please open an issue or submit a pull request. You can also find help on the FastHTML discord server.