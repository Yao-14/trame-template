import os

import anndata as ad

import pyvista as pv

from .pv_pipeline import add_single_model, create_plotter
from .ui import standard_tree

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

from typing import Optional

from .app import standard_html


def drosophila_E7_9h_dataset(
    dir_path="/home/yao/PythonProject/Yao_packages/trame-template/trame-template-yao/data/drosophila-E7-9h-models",
):
    # Generate anndata object
    adata = ad.read_h5ad(filename=os.path.join(dir_path, "E7-9h_cellbin.h5ad"))

    # Generate point cloud models
    pc_model_files = [
        "E7-9h_embryo_aligned_pc_model.vtk",
        "E7-9h_aligned_pc_model_CNS.vtk",
        "E7-9h_aligned_pc_model_midgut.vtk",
    ]
    pc_models = [pv.read(filename=os.path.join(dir_path, f)) for f in pc_model_files]
    pc_models_names = [
        "PC_Embryo",
        "PC_CNS",
        "PC_Midgut",
    ]  # Cannot contain `-` and ` `.

    # Generate mesh models
    mesh_model_files = [
        "E7-9h_embryo_aligned_mesh_model.vtk",
        "E7-9h_aligned_mesh_model_CNS.vtk",
        "E7-9h_aligned_mesh_model_midgut.vtk",
    ]
    mesh_models = [
        pv.read(filename=os.path.join(dir_path, f)) for f in mesh_model_files
    ]
    mesh_models_names = [
        "Mesh_Embryo",
        "Mesh_CNS",
        "Mesh_Midgut",
    ]  # Cannot contain `-` and ` `.
    return adata, pc_models, pc_models_names, mesh_models, mesh_models_names


def drosophila_plotter(
    pc_models: list,
    pc_models_cmaps: list,
    mesh_models: list,
    mesh_models_cmaps: list,
    pc_added_kwargs: Optional[dict] = None,
    mesh_added_kwargs: Optional[dict] = None,
    **kwargs
):
    # Generate a new plotter
    plotter = create_plotter(**kwargs)

    # Generate actors for pc models
    pc_kwargs = dict(
        key=None,
        ambient=0.2,
        opacity=1.0,
        model_style="points",
        model_size=5,
        color="gainsboro",
        cmap="rainbow",
    )
    if not (pc_added_kwargs is None):
        pc_kwargs.update(pc_added_kwargs)
    pc_actors = [
        add_single_model(plotter=plotter, model=pc, **pc_kwargs) for pc in pc_models
    ]

    # Generate actors for mesh models
    mesh_kwargs = dict(
        key=None,
        ambient=0.2,
        opacity=0.5,
        model_style="surface",
        color="gainsboro",
        cmap="rainbow",
    )
    if not (mesh_added_kwargs is None):
        mesh_kwargs.update(mesh_added_kwargs)
    mesh_actors = [
        add_single_model(plotter=plotter, model=mesh, **mesh_kwargs)
        for mesh in mesh_models
    ]
    return plotter, pc_actors, mesh_actors


def drosophila_tree(pc_actors, pc_actor_names, mesh_actors, mesh_actor_names):
    pc_actors, pc_actor_names, pc_tree = standard_tree(
        actors=pc_actors, actor_names=pc_actor_names, base_id=0
    )

    mesh_actors, mesh_actor_names, mesh_tree = standard_tree(
        actors=mesh_actors, actor_names=mesh_actor_names, base_id=len(pc_actors)
    )

    totel_actors = pc_actors + mesh_actors
    totel_actor_names = pc_actor_names + mesh_actor_names
    totel_tree = pc_tree + mesh_tree
    return totel_actors, totel_actor_names, totel_tree


def flysta3d_html(ui_name: str = "Flysta3D", **kwargs):

    # PyVista Pipeline
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
        pc_models=pc_models,
        pc_models_cmaps=pc_models_cmaps,
        mesh_models=mesh_models,
        mesh_models_cmaps=mesh_models_cmaps,
    )
    actors, actor_names, tree = drosophila_tree(
        pc_actors=pc_actors,
        pc_actor_names=pc_models_names,
        mesh_actors=mesh_actors,
        mesh_actor_names=mesh_models_names,
    )

    # HTML
    server = standard_html(
        plotter=plotter,
        adata=adata,
        actors=actors,
        actor_names=actor_names,
        tree=tree,
        ui_name=ui_name,
        **kwargs
    )
    return server
