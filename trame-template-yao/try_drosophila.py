
from stviewer import flysta3d_html

import pyvista as pv
from pyvista import examples

# mesh = examples.load_random_hills()

server = flysta3d_html()

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
