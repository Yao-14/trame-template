try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

from trame.widgets import vuetify

from pyvista import BasePlotter

from ..pv_pipeline import Viewer
from .utils import button, checkbox

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
