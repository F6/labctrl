import sys

def on_server_loaded(server_context):
    # If present, this function executes when the server starts.
    pass

def on_server_unloaded(server_context):
    # If present, this function executes when the server shuts down.
    pass

def on_session_created(session_context):
    # If present, this function executes when the server creates a session.
    pass

def on_session_destroyed(session_context):
    # If present, this function executes when the server closes a session.
    sys.exit()