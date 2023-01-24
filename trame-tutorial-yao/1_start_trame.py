# -----------------------------------------------------------------------------
# Get a server to work with
# -----------------------------------------------------------------------------

# Import the factory function for retrieving a server instance on which we will bind our UI and business logic.
from trame.app import get_server

server = get_server()

# -----------------------------------------------------------------------------
# Define the GUI
# -----------------------------------------------------------------------------

# Import a skeleton for a single page client application.
from trame.ui.vuetify import SinglePageLayout

# Define the graphical user interface (GUI) by passing the server to which it should be bound.
with SinglePageLayout(server) as layout:
    # Then with that layout we update the toolbar’s title to read "XXXXX".
    layout.title.set_text("Hello trame")

# -----------------------------------------------------------------------------
# Start the Web server using: python app.py --port 1234
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
