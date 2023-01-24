from trame.widgets import html, vuetify

from ..assets import asset_manager

# -----------------------------------------------------------------------------
# GUI layout
# -----------------------------------------------------------------------------


def ui_layout(server, template_name: str = "main", drawer_width: int = 350, **kwargs):
    """
    Define the user interface (UI) layout.
    Reference: https://trame.readthedocs.io/en/latest/trame.ui.vuetify.html#trame.ui.vuetify.SinglePageWithDrawerLayout

    Args:
        server: Server to bound the layout to.
        template_name: Name of the template.
        drawer_width: Drawer width in pixel.

    Returns:
        The SinglePageWithDrawerLayout layout object.
    """
    from trame.ui.vuetify import SinglePageWithDrawerLayout

    return SinglePageWithDrawerLayout(
        server, template_name=template_name, width=drawer_width, **kwargs
    )


def ui_title(layout, title_name="Flysta3D", title_icon=asset_manager.spateo_icon):
    """
    Define the title name and logo of the UI.
    Reference: https://trame.readthedocs.io/en/latest/trame.ui.vuetify.html#trame.ui.vuetify.SinglePageWithDrawerLayout

    Args:
        layout: The layout object.
        title_name: Title name of the GUI.
        title_icon: Title icon of the GUI

    Returns:
        None.
    """

    # Update the toolbar's name
    layout.title.set_text(title_name)

    # Update the toolbar's icon
    with layout.icon as icon:
        html.Img(src=title_icon, height=30, width=50)
        icon.click = None


# -----------------------------------------------------------------------------
# vuetify components
# -----------------------------------------------------------------------------


def button(click, icon, tooltip):
    """Create a vuetify button."""
    with vuetify.VTooltip(bottom=True):
        with vuetify.Template(v_slot_activator="{ on, attrs }"):
            with vuetify.VBtn(icon=True, v_bind="attrs", v_on="on", click=click):
                vuetify.VIcon(icon)
        html.Span(tooltip)


def checkbox(model, icons, tooltip, **kwargs):
    """Create a vuetify checkbox."""
    with vuetify.VTooltip(bottom=True):
        with vuetify.Template(v_slot_activator="{ on, attrs }"):
            with html.Div(v_on="on", v_bind="attrs"):
                vuetify.VCheckbox(
                    v_model=model,
                    on_icon=icons[0],
                    off_icon=icons[1],
                    dense=True,
                    hide_details=True,
                    classes="my-0 py-0 ml-1",
                    **kwargs
                )
        html.Span(tooltip)


def switch(model, tooltip, **kwargs):
    """Create a vuetify switch."""
    with vuetify.VTooltip(bottom=True):
        with vuetify.Template(v_slot_activator="{ on, attrs }"):
            vuetify.VSwitch(v_model=model, hide_details=True, dense=True, **kwargs)
        html.Span(tooltip)
