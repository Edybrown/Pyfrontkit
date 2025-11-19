
# Copyright (C) [2025] Eduardo Antonio Ferrera Rodríguez
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY. See the COPYING file for more details.


# pyfrontkit/dom.py
# Simple global DOM manager and generator of functions by id (accumulative).

from typing import Dict, Optional
import builtins

class DOMManager:
    """
    Global registry of blocks by id. Creates global functions (in builtins)
    to allow adding children by id with the syntax:
        Div(id='parent')
        parent(child1, child2)
    Calls are accumulative (they append children).
    """
    def __init__(self):
        self._by_id: Dict[str, object] = {}

    def register(self, id_name: str, block_obj):
        """Registers the block in the DOM. Creates the global function to add children."""
        if not id_name:
            return

        # replace: if it already exists, overwrite the object reference
        self._by_id[id_name] = block_obj

        # Create global function 'id_name' that appends children to the block (accumulative).
        # Only if the id is a valid Python identifier:
        if id_name.isidentifier():
            # define a function capturing id_name (avoid late-binding)
            def make_adder(name):
                def adder(*children):
                    return DOM.add_children(name, *children)
                return adder

            adder_func = make_adder(id_name)
            # Putting it in builtins allows the user to call `parent(...)` directly.
            setattr(builtins, id_name, adder_func)

    def get(self, id_name: str):
        return self._by_id.get(id_name)

    def add_children(self, parent_id: str, *children):
        parent = self.get(parent_id)
        if parent is None:
            raise KeyError(f"No block exists with id='{parent_id}'")
        # Append children (accumulative)
        parent.add_child(*children)
        return parent

# Create DOM singleton to be used from other modules
DOM = DOMManager()

# Shortcut so DOM.add_children is accessible inside the adder
def add_children(parent_id: str, *children):
    return DOM.add_children(parent_id, *children)

# Expose an alias for convenience
DOM.add_children = DOM.add_children
