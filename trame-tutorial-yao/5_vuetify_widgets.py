"""
Python Vuetify Rules
Exposing Vuetify in Python was accomplished by making a few syntax changes.

1. We use CamelCase in our Python component’s name, while attribute hyphens become underscores. For example, the
   v-text-field component becomes VTextField, and the v-model attribute becomes v_model.

2. Strings, ints, floats, and booleans used to set attributes are assigned as normal like
   vuetify.VTextField(label="myLabel") for the "myLabel" String.

3. Variables used to set attributes are surrounded by parenthesis like vuetify.VTextField(label=("myLabel",)). The comma
   is used to provide an initial value like vuetify.VTextField(label=("myLabel", "Initial Label")).

4. Vuetify implicitly sets boolean properties. For example, if something is to be disabled, then one simply writes
   disabled. In our Python implementation, this is done explicitly like vuetify.VTextField(disabled=True).

5. For events, HTML uses the @ like @click="runMethod" to set the function to call upon a click event and double quotes
   on the String name of the function to run. In our Python version of Vuetify, we ignore the @ and use the reference to
   the function instead of a the String name of the function call like vuetify.VBtn(click=runMethod).

https://kitware.github.io/trame/docs/tutorial-html.html
"""
# -----------------------------------------------------------------------------
# PyVista pipeline
# -----------------------------------------------------------------------------
import sys

# sys.path.insert(0, "/home/yao/PythonProject/Yao_packages/trame-template/pyvista")
import vtk

import pyvista as pv

cone = vtk.vtkConeSource()
plotter = pv.Plotter()
actor = plotter.add_mesh(cone, color="tan", show_edges=True)

# -----------------------------------------------------------------------------
# Trame
# -----------------------------------------------------------------------------

from trame.app import get_server
from trame.widgets import vuetify

from pyvista.trame import PyVistaLocalView

server = get_server()
state, ctrl = server.state, server.controller


@state.change("resolution")
def update_resolution(resolution, **kwargs):
    cone.SetResolution(resolution)
    ctrl.view_update()


def reset_resolution():
    state.resolution = DEFAULT_RESOLUTION
    ctrl.view_update()


from trame.ui.vuetify import SinglePageWithDrawerLayout

with SinglePageWithDrawerLayout(server) as layout:
    layout.title.set_text("PyVista Sample")

    with layout.content:
        view = PyVistaLocalView(plotter)
        ctrl.on_server_ready.add(view.update)
        ctrl.view_update = (
            view.update
        )  # <-- Capture update method (will be useful later)
        ctrl.view_reset_camera = view.reset_camera  # <-- Capture reset_camera method

    # -----------------------------------------------------------------------------
    # Add Some components to the toolbar
    # -----------------------------------------------------------------------------
    with layout.toolbar:
        # The VSpacer Vuetify component pushes the extra space on the left side of the component.
        vuetify.VSpacer()

        # Let’s add a VSlider for adjusting the resolution, a VBtn with VIcon to reset the resolution to the default
        # value, and a vertical VDivider to separate our visualization GUI from the application GUI. The following is
        # added after the VSpacer component at the beginning of the with toolbar flow.
        DEFAULT_RESOLUTION = 6
        vuetify.VSlider(
            v_model=("resolution", DEFAULT_RESOLUTION),  # (var_name, initial_value)
            min=3,
            max=60,
            step=1,  # min/max/step
            hide_details=True,
            dense=True,  # presentation params
            style="max-width: 300px",  # css style
        )
        with vuetify.VBtn(icon=True, click=reset_resolution):
            vuetify.VIcon("mdi-restore")
        vuetify.VDivider(vertical=True, classes="mx-2")

        # The VSwitch component toggles between two different states. In this case, we will update a Vuetify variable
        # $vuetify.theme.dark. The hide_details and dense attribute creates a smaller, tighter switch.
        vuetify.VSwitch(
            v_model="$vuetify.theme.dark",
            hide_details=True,
            dense=True,
        )

        # The VBtn component is a button. We decorate the button with a VIcon component where the argument is a String
        # identifying the Material Design Icons instead of text in this case. The VBtn icon attribute provides proper
        # sizing and padding for the icon. Finally, the click attribute tells the application what method to call when
        # the button is pressed.
        with vuetify.VBtn(
            icon=True,
            click=ctrl.view_reset_camera,  # <-- Use that reset_camera (init order does not matter)
        ):
            vuetify.VIcon("mdi-crop-free")


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
