import io

import numpy as np

import pyvista as pv

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
    """Callbacks for toolbar&container based on pyvista."""

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
# Common Callbacks-Drawer
# -----------------------------------------------------------------------------

"""
class PVCB:
    

    def __init__(self, server, actor, actor_name):
        state, ctrl = server.state, server.controller
        self._server = server
        self._ctrl = ctrl
        self._state = state
        self._actor = actor
        self._actor_name = actor_name

    def scalars(self):
        @self._state.change(f"{self._actor_name}_scalars")
        def _scalars(scalars=None, **kwargs):
            if scalars is None:
                self._actor.mapper.scalar_visibility = False
            else:
                self._actor.mapper.scalar_visibility = True
                self._actor.mapper.dataset.set_active_scalars(scalars)
                # self._actor.mapper.array_name = scalars
            self._ctrl.view_update()

    def opacity(self):
        @self._state.change(f"{self._actor_name}_opacity")
        def _opacity(opacity=1.0, **kwargs):
            self._actor.prop.opacity = opacity
            self._ctrl.view_update()

    def ambient(self):
        @self._state.change(f"{self._actor_name}_ambient")
        def _ambient(ambient=0.2, **kwargs):
            self._actor.prop.ambient = ambient
            self._ctrl.view_update()

    def color(self):
        @self._state.change(f"{self._actor_name}_color")
        def _color(color="gainsboro", **kwargs):
            self._actor.prop.color = color
            self._ctrl.view_update()

    def colormap(self):
        @self._state.change(f"{self._actor_name}_colormap")
        def colormap(colormap="rainbow", **kwargs):
            self._actor.mapper.lookup_table.cmap = colormap
            self._ctrl.view_update()

    def style(self):
        @self._state.change(f"{self._actor_name}_style")
        def _style(style="surface", **kwargs):
            self._actor.prop.style = style
            self._ctrl.view_update()

    def point_size(self):
        @self._state.change(f"{self._actor_name}_point_size")
        def _point_size(point_size=5.0, **kwargs):
            self._actor.prop.point_size = point_size
            self._ctrl.view_update()

    def line_width(self):
        @self._state.change(f"{self._actor_name}_line_width")
        def _line_width(line_width=2.0, **kwargs):
            self._actor.prop.line_width = line_width
            self._ctrl.view_update()

    def as_spheres(self):
        @self._state.change(f"{self._actor_name}_render_points_as_spheres")
        def _as_spheres(as_spheres=False, **kwargs):
            self._actor.prop.render_points_as_spheres = as_spheres
            self._ctrl.view_update()

    def as_tubes(self):
        @self._state.change(f"{self._actor_name}_render_lines_as_tubes")
        def _as_tubes(as_tubes=False, **kwargs):
            self._actor.prop.render_lines_as_tubes = as_tubes
            self._ctrl.view_update()
"""


class PVCB:
    """Callbacks for drawer based on pyvista."""

    def __init__(self, server, actor, actor_name, adata):
        """Initialize PVCB."""
        state, ctrl = server.state, server.controller
        self._server = server
        self._ctrl = ctrl
        self._state = state
        self._actor = actor
        self._actor_name = actor_name
        self._adata = adata

        # State variable names
        self.SCALARS = f"{actor_name}_scalars_value"
        self.OPACITY = f"{actor_name}_opacity_value"
        self.AMBIENT = f"{actor_name}_ambient_value"
        self.COLOR = f"{actor_name}_color_value"
        self.COLORMAP = f"{actor_name}_colormap_value"
        self.STYLE = f"{actor_name}_style_value"
        self.POINTSIZE = f"{actor_name}_point_size_value"
        self.LINEWIDTH = f"{actor_name}_line_width_value"
        self.ASSPHERES = f"{actor_name}_as_spheres_value"
        self.ASTUBES = f"{actor_name}_as_tubes_value"

        # Listen to state changes
        self._state.change(self.SCALARS)(self.on_scalars_change)
        self._state.change(self.OPACITY)(self.on_opacity_change)
        self._state.change(self.AMBIENT)(self.on_ambient_change)
        self._state.change(self.COLOR)(self.on_color_change)
        self._state.change(self.COLORMAP)(self.on_colormap_change)
        self._state.change(self.STYLE)(self.on_style_change)
        self._state.change(self.POINTSIZE)(self.on_point_size_change)
        self._state.change(self.LINEWIDTH)(self.on_line_width_change)
        self._state.change(self.ASSPHERES)(self.on_as_spheres_change)
        self._state.change(self.ASTUBES)(self.on_as_tubes_change)

    def get_model(self):
        return self._actor.mapper.dataset

    def get_adata(self):
        return self._adata

    @vuwrap
    def on_scalars_change(self, **kwargs):
        if self._state[self.SCALARS] in ["none", "None", None]:
            self._actor.mapper.scalar_visibility = False
        else:
            _adata = self._adata.copy()
            _obs_index = self._actor.mapper.dataset.point_data["obs_index"]
            _adata = _adata[_obs_index, :]

            if self._state[self.SCALARS] in set(_adata.obs_keys()):
                array = np.asarray(
                    _adata.obs[self._state[self.SCALARS]].values
                ).flatten()
            elif self._state[self.SCALARS] in set(_adata.var_names.tolist()):
                array = np.asarray(
                    _adata[:, self._state[self.SCALARS]].X.sum(axis=1).flatten()
                )
            else:
                array = np.ones(shape=(len(_obs_index),))

            self._actor.mapper.dataset.point_data[self._state[self.SCALARS]] = array
            self._actor.mapper.SelectColorArray(self._state[self.SCALARS])
            self._actor.mapper.lookup_table.SetRange(np.min(array), np.max(array))
            self._actor.mapper.SetScalarModeToUsePointFieldData()
            self._actor.mapper.scalar_visibility = True
        self._ctrl.view_update()

    def on_opacity_change(self, **kwargs):
        self._actor.prop.opacity = self._state[self.OPACITY]
        self._ctrl.view_update()

    def on_ambient_change(self, **kwargs):
        self._actor.prop.ambient = self._state[self.AMBIENT]
        self._ctrl.view_update()

    def on_color_change(self, **kwargs):
        self._actor.prop.color = self._state[self.COLOR]
        self._ctrl.view_update()

    def on_colormap_change(self, **kwargs):
        self._actor.mapper.lookup_table.cmap = self._state[self.COLORMAP]
        self._ctrl.view_update()

    def on_style_change(self, **kwargs):
        self._actor.prop.style = self._state[self.STYLE]
        self._ctrl.view_update()

    def on_point_size_change(self, **kwargs):
        self._actor.prop.point_size = self._state[self.POINTSIZE]
        self._ctrl.view_update()

    def on_line_width_change(self, **kwargs):
        self._actor.prop.line_width = self._state[self.LINEWIDTH]
        self._ctrl.view_update()

    def on_as_spheres_change(self, **kwargs):
        self._actor.prop.render_points_as_spheres = self._state[self.ASSPHERES]
        self._ctrl.view_update()

    def on_as_tubes_change(self, **kwargs):
        self._actor.prop.render_lines_as_tubes = self._state[self.ASTUBES]
        self._ctrl.view_update()
