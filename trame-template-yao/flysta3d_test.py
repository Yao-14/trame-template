import pyvista as pv
import io, os
import anndata as ad

# data
dir_path="/home/yao/PythonProject/Yao_packages/trame-template/trame-template-yao/data/drosophila-E7-9h-models"
adata = ad.read_h5ad(filename=os.path.join(dir_path, "E7-9h_cellbin.h5ad"))
pc_model = pv.read(filename=os.path.join(dir_path, "E7-9h_embryo_aligned_pc_model.vtk"))
pc_model_name = "PC-Embryo"
pc_model_cmap = "gainsboro"
plotter = pv.Plotter(off_screen=True, lighting="light_kit")
actor = plotter.add_mesh(pc_model, scalars="cell_radius", style="points", render_points_as_spheres=True, color="gainsboro", cmap="rainbow",
                         point_size=5, ambient=0.2, opacity=1.0, smooth_shading=True, show_scalar_bar=False,)


# Get a Server to work with
from trame.widgets.trame import GitTree
from trame.app import get_server
from stviewer import ui_layout, ui_standard_container, ui_title, ui_standard_toolbar, standard_pc_card
server = get_server()
state, ctrl = server.state, server.controller
state.setdefault("active_ui", None)

# GUI
ui_standard_layout = ui_layout(server=server)
with ui_standard_layout as layout:
    layout.icon.click = ctrl.view_reset_camera
    ui_title(layout=layout)

    # -----------------------------------------------------------------------------
    # ToolBar
    # -----------------------------------------------------------------------------
    with layout.toolbar as tb:
        ui_standard_toolbar(server=server, plotter=plotter)

    # -----------------------------------------------------------------------------
    # ToolBar
    # -----------------------------------------------------------------------------
    with layout.drawer as dr:
        GitTree(sources=("pipeline", [{"id": str(1), "parent": str(0), "visible": True , "name": pc_model_name}]))
        standard_pc_card(actor_name=pc_model_name, card_title=pc_model_name)

    # -----------------------------------------------------------------------------
    # Main Content
    # -----------------------------------------------------------------------------
    with layout.content as con:
        ui_standard_container(server=server, plotter=plotter)

    # -----------------------------------------------------------------------------
    # Footer
    # -----------------------------------------------------------------------------
    layout.footer.hide()

if __name__ == "__main__":
    server.start()
