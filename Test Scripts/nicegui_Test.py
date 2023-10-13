from nicegui import ui

ui.mermaid('''
graph LR;
    A --> B;
    A --> C;
''')

if __name__ in {"__main__", "__mp_main__"}:
    ui.run()