try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

import io

from trame.widgets import vuetify

import pyvista as pv
from pyvista import BasePlotter

from .utils import button, checkbox

# -----------------------------------------------------------------------------
# Common Callback-ToolBar&Container
# -----------------------------------------------------------------------------


def vuwrap(func):
    """Call view_update in trame to synchronize changes to a view."""

    def wrapper(self, *args, **kwargs):
        ret = func(self, *args, **kwargs)
        self._ctrl.view_update()
        return ret

    return wrapper


class Viewer:
    """Internal wrapper to sync trame view with Plotter."""

    def __init__(self, plotter, server, suppress_rendering=False):
        """Initialize Viewer."""
        state, ctrl = server.state, server.controller
        self._server = server
        self._ctrl = ctrl
        self._state = state

        self.plotter = plotter
        self.plotter.suppress_rendering = suppress_rendering

        # State variable names
        self.SHOW_UI = f"{plotter._id_name}_show_ui"
        self.GRID = f"{plotter._id_name}_grid_visibility"
        self.OUTLINE = f"{plotter._id_name}_outline_visibility"
        self.EDGES = f"{plotter._id_name}_edge_visibility"
        self.AXIS = f"{plotter._id_name}_axis_visiblity"
        self.SCREENSHOT = f"{plotter._id_name}_download_screenshot"
        self.SERVER_RENDERING = f"{plotter._id_name}_use_server_rendering"

        # controller
        ctrl.get_render_window = lambda: self.plotter.render_window

        # Listen to state changes
        self._state.change(self.GRID)(self.on_grid_visiblity_change)
        self._state.change(self.OUTLINE)(self.on_outline_visiblity_change)
        self._state.change(self.EDGES)(self.on_edge_visiblity_change)
        self._state.change(self.AXIS)(self.on_axis_visiblity_change)
        self._state.change(self.SERVER_RENDERING)(self.on_rendering_mode_change)
        # Listen to events
        self._ctrl.trigger(self.SCREENSHOT)(self.screenshot)

    @vuwrap
    def on_edge_visiblity_change(self, **kwargs):
        """Toggle edge visibility for all actors."""
        value = self._state[self.GRID]
        for _, actor in self.plotter.actors.items():
            if isinstance(actor, pv.Actor):
                actor.prop.show_edges = value

    @vuwrap
    def view_isometric(self):
        """View isometric."""
        self.plotter.view_isometric()
        self._ctrl.view_push_camera(force=True)

    @vuwrap
    def view_yz(self):
        """View YZ plane."""
        self.plotter.view_yz()
        self._ctrl.view_push_camera(force=True)

    @vuwrap
    def view_xz(self):
        """View XZ plane."""
        self.plotter.view_xz()
        self._ctrl.view_push_camera(force=True)

    @vuwrap
    def view_xy(self):
        """View XY plane."""
        self.plotter.view_xy()
        self._ctrl.view_push_camera(force=True)

    @vuwrap
    def reset_camera(self):
        """Reset the camera."""
        # self.plotter.reset_camera()
        self._ctrl.view_reset_camera(force=True)

    @vuwrap
    def on_grid_visiblity_change(self, **kwargs):
        """Handle axes grid visibility."""
        if self._state[self.GRID]:
            self.plotter.show_grid()
        else:
            self.plotter.remove_bounds_axes()

    @vuwrap
    def on_outline_visiblity_change(self, **kwargs):
        """Handle outline visibility."""
        if self._state[self.OUTLINE]:
            self.plotter.add_bounding_box(reset_camera=False)
        else:
            self.plotter.remove_bounding_box()

    @vuwrap
    def on_axis_visiblity_change(self, **kwargs):
        """Handle outline visibility."""
        if self._state[self.AXIS]:
            self.plotter.show_axes()
        else:
            self.plotter.hide_axes()

    @vuwrap
    def on_rendering_mode_change(self, **kwargs):
        """Handle any configurations when the render mode changes between client and server."""
        if not self._state[self.SERVER_RENDERING]:
            self._ctrl.view_push_camera(force=True)

    @property
    def actors(self):
        """Get dataset actors."""
        return {k: v for k, v in self.plotter.actors.items() if isinstance(v, pv.Actor)}

    @vuwrap
    def screenshot(self):
        """Take screenshot and add attachament."""
        self.plotter.render()
        buffer = io.BytesIO()
        self.plotter.screenshot(filename=buffer)
        buffer.seek(0)
        return self._server.protocol.addAttachment(memoryview(buffer.read()))


# -----------------------------------------------------------------------------
# GUI- standard ToolBar
# -----------------------------------------------------------------------------


def ui_standard_toolbar(
    server,
    plotter: BasePlotter,
    mode: Literal["trame", "server", "client"] = "trame",
    default_server_rendering: bool = True,
):
    """
    Generate standard ToolBar for Spateo UI.

    Args:
        server: The trame server.
        plotter: The PyVista plotter to connect with the UI.
        mode: The UI view mode. Options are:

            * ``'trame'``: Uses a view that can switch between client and server rendering modes.
            * ``'server'``: Uses a view that is purely server rendering.
            * ``'client'``: Uses a view that is purely client rendering (generally safe without a virtual frame buffer)
        default_server_rendering: Whether to use server-side or client-side rendering on-start when using the ``'trame'`` mode.

    Returns:
        None.
    """
    if mode != "trame":
        default_server_rendering = mode == "server"

    viewer = Viewer(plotter=plotter, server=server, suppress_rendering=mode == "client")

    # Pushes the extra space on the left side of the component.
    vuetify.VSpacer()

    # Whether to toggle the theme between light and dark
    checkbox(
        model="$vuetify.theme.dark",
        icons=("mdi-lightbulb-off-outline", "mdi-lightbulb-outline"),
        tooltip=f"Toggle theme",
    )
    # Server rendering options
    if mode == "trame":
        checkbox(
            model=(viewer.SERVER_RENDERING, default_server_rendering),
            icons=("mdi-lan-connect", "mdi-lan-disconnect"),
            tooltip=f"Toggle rendering mode ({{{{ {viewer.SERVER_RENDERING} ? 'remote' : 'local' }}}})",
        )
    # Whether to save the image
    button(
        # Must use single-quote string for JS here
        click=f"utils.download('screenshot.png', trigger('{viewer.SCREENSHOT}'), 'image/png')",
        icon="mdi-file-png-box",
        tooltip="Save screenshot",
    )

    # Whether to add outline
    vuetify.VDivider(vertical=True, classes="mx-1")
    checkbox(
        model=(viewer.OUTLINE, False),
        icons=("mdi-cube", "mdi-cube-off"),
        tooltip=f"Toggle bounding box ({{{{ {viewer.OUTLINE} ? 'on' : 'off' }}}})",
    )
    # Whether to add grid
    checkbox(
        model=(viewer.GRID, False),
        icons=("mdi-ruler-square", "mdi-ruler-square"),
        tooltip=f"Toggle ruler ({{{{ {viewer.GRID} ? 'on' : 'off' }}}})",
    )
    # Whether to add axis legend
    checkbox(
        model=(viewer.AXIS, False),
        icons=("mdi-axis-arrow-info", "mdi-axis-arrow-info"),
        tooltip=f"Toggle axis ({{{{ {viewer.AXIS} ? 'on' : 'off' }}}})",
    )

    # Reset camera
    vuetify.VDivider(vertical=True, classes="mx-1")
    button(
        click=viewer.reset_camera,
        icon="mdi-arrow-expand-all",
        tooltip="Reset Camera",
    )

    # Reset camera angle
    button(
        click=viewer.view_isometric,
        icon="mdi-axis-arrow",
        tooltip="Perspective view",
    )
    button(
        click=viewer.view_yz,
        icon="mdi-axis-x-arrow",
        tooltip="Reset Camera X",
    )
    button(
        click=viewer.view_xz,
        icon="mdi-axis-y-arrow",
        tooltip="Reset Camera Y",
    )
    button(
        click=viewer.view_xy,
        icon="mdi-axis-z-arrow",
        tooltip="Reset Camera Z",
    )
