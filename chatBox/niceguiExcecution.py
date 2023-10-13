# import your nicegui as ui
from nicegui import ui
import nicegui as ng
import sys
from time import sleep


def flowchart(chart):
    print('t')
    ui.mermaid(chart)


if __name__ in {"__main__", "__mp_main__"}:
    app = ng.app
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        flowchart(arg)
        print('f')
    else:
        print('fail')
    print('u')
    ui.run(reload=False)
    sleep(10)
    app.shutdown()