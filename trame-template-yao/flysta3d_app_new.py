# -----------------------------------------------------------------------------
# Pyvista Pipeline
# -----------------------------------------------------------------------------
from stviewer import drosophila_E7_9h_dataset, drosophila_plotter, drosophila_tree
(
    adata,
    pc_models,
    pc_models_names,
    mesh_models,
    mesh_models_names,
) = drosophila_E7_9h_dataset()

pc_models_cmaps = []
mesh_models_cmaps = []
plotter, pc_actors, mesh_actors = drosophila_plotter(
    pc_models=pc_models, pc_models_cmaps=pc_models_cmaps, mesh_models=mesh_models, mesh_models_cmaps=mesh_models_cmaps
)
actors, actor_names, tree = drosophila_tree(
    pc_actors=pc_actors,
    pc_actor_names=pc_models_names,
    mesh_actors=mesh_actors,
    mesh_actor_names=mesh_models_names,
)

# -----------------------------------------------------------------------------
# Server
# -----------------------------------------------------------------------------
from stviewer import get_trame_server, asset_manager
server = get_trame_server(name=None)
state, ctrl = server.state, server.controller
state.trame__title = "Flysta3D"
state.trame__favicon = asset_manager.spateo_icon
state.setdefault("active_ui", None)
ctrl.on_server_ready.add(ctrl.view_update)

# -----------------------------------------------------------------------------
# Layouts
# -----------------------------------------------------------------------------
from stviewer import ui_title, ui_layout, ui_standard_container, ui_standard_toolbar, ui_standard_drawer
ui_standard_layout = ui_layout(
    server=server, template_name="main", drawer_width=350
)
with ui_standard_layout as layout:
    layout.icon.click = ctrl.view_reset_camera
    ui_title(layout=layout, title_name="Flysta3D", title_icon=asset_manager.spateo_icon)

    # -----------------------------------------------------------------------------
    # ToolBar
    # -----------------------------------------------------------------------------
    with layout.toolbar as tb:
        ui_standard_toolbar(server=server, plotter=plotter, mode="trame")

    # -----------------------------------------------------------------------------
    # Drawer
    # -----------------------------------------------------------------------------
    with layout.drawer as dr:
        actor_name1 = "PC_Embryo"
        actor1 = actors[0]
        @state.change(f"{actor_name1}_opacity")
        def opacity(opacity=1.0, **kwargs):
            actor1.prop.opacity = opacity
            ctrl.view_update()

        @state.change(f"{actor_name1}_ambient")
        def ambient(ambient=0.2, **kwargs):
            actor1.prop.ambient = ambient
            ctrl.view_update()

        @state.change(f"{actor_name1}_point_size")
        def point_size(point_size=5.0, **kwargs):
            actor1.prop.point_size = point_size
            ctrl.view_update()


        actor_name2 = "Mesh_Embryo"
        actor2 = actors[1]
        @state.change(f"{actor_name2}_opacity")
        def opacity(opacity=1.0, **kwargs):
            actor2.prop.opacity = opacity
            ctrl.view_update()


        @state.change(f"{actor_name2}_ambient")
        def ambient(ambient=0.2, **kwargs):
            actor2.prop.ambient = ambient
            ctrl.view_update()


        @state.change(f"{actor_name2}_point_size")
        def point_size(point_size=5.0, **kwargs):
            actor2.prop.point_size = point_size
            ctrl.view_update()

        ui_standard_drawer(
            server=server, actors=[actor1, actor2], actor_names=actor_names, tree=tree
        )

    # -----------------------------------------------------------------------------
    # Main Content
    # -----------------------------------------------------------------------------
    with layout.content as con:
        ui_standard_container(server=server, plotter=plotter, mode="trame")

    # -----------------------------------------------------------------------------
    # Footer
    # -----------------------------------------------------------------------------
    layout.footer.hide()

if __name__ == "__main__":
    server.start()






