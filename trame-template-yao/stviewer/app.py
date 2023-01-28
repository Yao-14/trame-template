try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

from typing import Optional

from anndata import AnnData

from pyvista import BasePlotter

from .assets import asset_manager
from .server import get_trame_server
from .ui import (
    ui_layout,
    ui_standard_container,
    ui_standard_drawer,
    ui_standard_toolbar,
    ui_title,
)


def standard_html(
    plotter: BasePlotter,
    adata: AnnData,
    actors: list,
    actor_names: list,
    tree: Optional[list] = None,
    mode: Literal["trame", "server", "client"] = "trame",
    server_name: Optional[str] = None,
    template_name: str = "main",
    ui_name: str = "Flysta3D",
    ui_icon=asset_manager.spateo_icon,
    drawer_width: int = 350,
):
    # Get a Server to work with
    server = get_trame_server(name=server_name)
    state, ctrl = server.state, server.controller
    state.trame__title = ui_name
    state.trame__favicon = ui_icon
    state.setdefault("active_ui", None)
    # ctrl.on_server_ready.add(ctrl.view_update)

    # GUI
    ui_standard_layout = ui_layout(
        server=server, template_name=template_name, drawer_width=drawer_width
    )
    with ui_standard_layout as layout:
        layout.icon.click = ctrl.view_reset_camera
        ui_title(layout=layout, title_name=ui_name, title_icon=ui_icon)

        # -----------------------------------------------------------------------------
        # ToolBar
        # -----------------------------------------------------------------------------
        with layout.toolbar as tb:
            ui_standard_toolbar(server=server, plotter=plotter, mode=mode)

        # -----------------------------------------------------------------------------
        # Drawer
        # -----------------------------------------------------------------------------
        with layout.drawer as dr:
            ui_standard_drawer(
                server=server,
                adata=adata,
                actors=actors,
                actor_names=actor_names,
                tree=tree,
            )

        # -----------------------------------------------------------------------------
        # Main Content
        # -----------------------------------------------------------------------------
        with layout.content as con:
            ui_standard_container(server=server, plotter=plotter, mode=mode)

        # -----------------------------------------------------------------------------
        # Footer
        # -----------------------------------------------------------------------------
        layout.footer.hide()

    return server
