try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

from typing import Optional

import matplotlib.pyplot as plt
from anndata import AnnData
from trame.widgets import vuetify

from pyvista.plotting.colors import hexcolors

from ..pv_pipeline import PVCB


def standard_tree(actors: list, actor_names: list, base_id: int = 0):
    for i, actor in enumerate(actors):
        if i == 0:
            actor.SetVisibility(True)
        else:
            actor.SetVisibility(False)
    tree = [
        {
            "id": str(base_id + 1 + i),
            "parent": str(0) if i == 0 else str(base_id + 1),
            "visible": True if i == 0 else False,
            "name": actor_names[i],
        }
        for i, name in enumerate(actor_names)
    ]
    return actors, actor_names, tree


def pipeline(server, actors: list, actor_names: list, tree: Optional[list] = None):
    """Create a vuetify GitTree."""
    from trame.widgets.trame import GitTree

    state, ctrl = server.state, server.controller

    n_actors, n_actor_names = len(actors), len(actor_names)
    assert (
        n_actors == n_actor_names
    ), "The number of ``actors`` is not equal to the number of ``actor_names``."

    # Selection Change
    def actives_change(ids):
        _id = ids[0]
        active_actor_name = actor_names[int(_id) - 1]
        state.active_ui = active_actor_name

    # Visibility Change
    def visibility_change(event):
        _id = event["id"]
        _visibility = event["visible"]
        active_actor = actors[int(_id) - 1]
        active_actor.SetVisibility(_visibility)
        ctrl.view_update()

    if tree is None:
        tree = [
            {
                "id": str(1 + i),
                "parent": str(0) if i == 0 else str(1),
                "visible": True if i == 0 else False,
                "name": actor_names[i],
            }
            for i, name in enumerate(actor_names)
        ]

    GitTree(
        sources=("pipeline", tree),
        actives_change=(actives_change, "[$event]"),
        visibility_change=(visibility_change, "[$event]"),
    )


def card(title, actor_name):
    """Create a vuetify card."""
    with vuetify.VCard(v_show=f"active_ui == '{actor_name}'"):
        vuetify.VCardTitle(
            title,
            classes="grey lighten-1 py-1 grey--text text--darken-3",
            style="user-select: none; cursor: pointer",
            hide_details=True,
            dense=True,
        )
        content = vuetify.VCardText(classes="py-2")
    return content


def standard_card_components(CBinCard, default_values: dict):
    with vuetify.VRow(classes="pt-2", dense=True):
        # Style
        with vuetify.VCol(cols="6"):
            vuetify.VSelect(
                label="Style",
                v_model=(CBinCard.STYLE, default_values["style"]),
                items=(f"styles", ["surface", "points", "wireframe"]),
                hide_details=True,
                dense=True,
                outlined=True,
                classes="pt-1",
            )
        # Color
        with vuetify.VCol(cols="6"):
            vuetify.VSelect(
                label="Color",
                v_model=(CBinCard.COLOR, default_values["color"]),
                items=(f"hexcolors", list(hexcolors.keys())),
                hide_details=True,
                dense=True,
                outlined=True,
                classes="pt-1",
            )

    # Opacity
    vuetify.VSlider(
        v_model=(CBinCard.OPACITY, default_values["opacity"]),
        min=0,
        max=1,
        step=0.01,
        label="Opacity",
        classes="mt-1",
        hide_details=True,
        dense=True,
    )
    # Ambient
    vuetify.VSlider(
        v_model=(CBinCard.AMBIENT, default_values["ambient"]),
        min=0,
        max=1,
        step=0.01,
        label="Ambient",
        classes="mt-1",
        hide_details=True,
        dense=True,
    )


def standard_pc_card(
    CBinCard, actor_name: str, card_title: str, default_values: Optional[dict] = None
):
    _default_values = {
        "scalars": "None",
        "point_size": 5,
        "style": "points",
        "color": "gainsboro",
        "cmap": "Purples",
        "opacity": 1,
        "ambient": 0.2,
    }
    if not (default_values is None):
        _default_values.update(default_values)

    with card(title=card_title, actor_name=actor_name):
        with vuetify.VRow(classes="pt-2", dense=True):
            with vuetify.VCol(cols="6"):
                vuetify.VTextField(
                    label="Scalars",
                    v_model=(CBinCard.SCALARS, _default_values["scalars"]),
                    type="str",
                    hide_details=True,
                    dense=True,
                    outlined=True,
                    classes="pt-1",
                )
            with vuetify.VCol(cols="6"):
                vuetify.VSelect(
                    label="Colormap",
                    v_model=(CBinCard.COLORMAP, _default_values["cmap"]),
                    items=("colormaps", plt.colormaps()),
                    hide_details=True,
                    dense=True,
                    outlined=True,
                    classes="pt-1",
                )

        standard_card_components(CBinCard=CBinCard, default_values=_default_values)

        vuetify.VSlider(
            v_model=(CBinCard.POINTSIZE, _default_values["point_size"]),
            min=0,
            max=20,
            step=1,
            label="Point Size",
            classes="mt-1",
            hide_details=True,
            dense=True,
        )


def standard_mesh_card(
    CBinCard, actor_name: str, card_title: str, default_values: Optional[dict] = None
):
    _default_values = {
        "style": "surface",
        "color": "gainsboro",
        "opacity": 0.5,
        "ambient": 0.2,
    }
    if not (default_values is None):
        _default_values.update(default_values)

    with card(title=card_title, actor_name=actor_name):
        standard_card_components(CBinCard=CBinCard, default_values=_default_values)


# -----------------------------------------------------------------------------
# GUI-standard Drawer
# -----------------------------------------------------------------------------


def ui_standard_drawer(
    server,
    adata: AnnData,
    actors: list,
    actor_names: list,
    tree: Optional[list] = None,
):
    """
    Generate standard Drawer for Spateo UI.

    Args:
        server: The trame server.

    """

    pipeline(server=server, actors=actors, actor_names=actor_names, tree=tree)
    vuetify.VDivider(classes="mb-2")
    for actor, actor_name in zip(actors, actor_names):
        CBinCard = PVCB(server=server, actor=actor, actor_name=actor_name, adata=adata)
        if str(actor_name).startswith("PC"):
            standard_pc_card(CBinCard, actor_name=actor_name, card_title=actor_name)
        if str(actor_name).startswith("Mesh"):
            standard_mesh_card(CBinCard, actor_name=actor_name, card_title=actor_name)
