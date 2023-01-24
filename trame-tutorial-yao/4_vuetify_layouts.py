# -----------------------------------------------------------------------------
# Three basic GUI layouts objects
# https://kitware.github.io/trame/docs/tutorial-layouts.html
# -----------------------------------------------------------------------------

from trame.app import get_server
from trame.widgets import vtk, vuetify

server = get_server()
ctrl = server.controller

# -----------------------------------------------------------------------------
# VAppLayout: The VAppLayout is really a blank canvas to add your desired Vuetify components.
# -----------------------------------------------------------------------------

from trame.ui.vuetify import VAppLayout

with VAppLayout(server) as layout:
    with layout.root:
        with vuetify.VContainer(
            fluid=True,
            classes="pa-0 fill-height",
        ):
            view = vtk.VtkLocalView()
            ctrl.on_server_ready.add(view.update)

# -----------------------------------------------------------------------------
# SinglePageLayout: The SinglePageLayout extends the VAppLayout with a few predefined components such as icon, title, toolbar, content, and footer.
# -----------------------------------------------------------------------------

from trame.ui.vuetify import SinglePageLayout

with SinglePageLayout(server) as layout:
    layout.title.set_text("Hello trame")

    with layout.content:
        with vuetify.VContainer(
            fluid=True,
            classes="pa-0 fill-height",
        ):
            view = vtk.VtkLocalView()
            ctrl.on_server_ready.add(view.update)

# -----------------------------------------------------------------------------
# SinglePageWithDrawerLayout: The SinglePageWithDrawerLayout extends the SinglePageLayout with a drawer.
# -----------------------------------------------------------------------------

from trame.ui.vuetify import SinglePageWithDrawerLayout

with SinglePageWithDrawerLayout(server) as layout:
    layout.title.set_text("Hello trame")

    with layout.content:
        with vuetify.VContainer(
            fluid=True,
            classes="pa-0 fill-height",
        ):
            view = vtk.VtkLocalView()
            ctrl.on_server_ready.add(view.update)
