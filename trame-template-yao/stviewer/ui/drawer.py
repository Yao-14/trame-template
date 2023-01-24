try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

from typing import Optional
from trame.widgets import vuetify


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


# -----------------------------------------------------------------------------
# GUI-standard Drawer
# -----------------------------------------------------------------------------


def ui_standard_drawer(
    server, actors: list, actor_names: list, tree: Optional[list] = None, **kwargs
):
    """
    Generate standard Drawer for Spateo UI.

    Args:
        server: The trame server.

    """

    pipeline(server=server, actors=actors, actor_names=actor_names, tree=tree)
    vuetify.VDivider(classes="mb-2")
