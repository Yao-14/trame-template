# -----------------------------------------------------------------------------
# PyVista pipeline
# -----------------------------------------------------------------------------
import sys

sys.path.insert(0, "/home/yao/PythonProject/Yao_packages/trame-template/pyvista")
import pyvista as pv

cone = pv.Cone()
plotter = pv.Plotter()
plotter.add_mesh(cone, color="tan", show_edges=True)

# -----------------------------------------------------------------------------
# Trame
# -----------------------------------------------------------------------------

from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout

# Import vuetify from trame to provides access to trame's vuetify widgets
from trame.widgets import vuetify

# Import PyVistaLocalView from pyvista.trame to provides access to trame's PyVistaLocalView widgets
from pyvista.trame import PyVistaLocalView

server = get_server()
ctrl = server.controller

with SinglePageLayout(server) as layout:
    layout.title.set_text("Hello trame")

    with layout.content:
        with vuetify.VContainer(
            fluid=True,
            classes="pa-0 fill-height",
        ):
            view = PyVistaLocalView(plotter)

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
