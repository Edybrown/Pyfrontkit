# Copyright (c) 2025 Eduardo Antonio Ferrera Rodríguez
# SPDX-License-Identifier: MIT

# pyfrontkit/dom.py
# Simple global DOM manager and generator of functions by id (accumulative).

from typing import Dict
import builtins


class DOMManager:
    """
    Global registry of blocks by id.
    Creates global functions (in builtins) to allow adding children by id:

        Div(id="parent")
        parent(child1, child2)

    Calls are accumulative (append children).

    NOW ALSO SUPPORTS:
        - DOM snapshot (freeze) for template analysis.
    """

    def __init__(self):
        self._by_id: Dict[str, object] = {}
        self.snapshot = []  # Aquí se guardará el DOM congelado

    # ---------------------------------------------------
    #  REGISTER BLOCKS BY ID
    # ---------------------------------------------------
    def register(self, id_name: str, block_obj):
        """Registers the block in the DOM. Creates the global adder function."""
        if not id_name:
            return

        # Replace if exists
        self._by_id[id_name] = block_obj

        # Create global function only if ID is a valid python identifier
        if id_name.isidentifier():

            def make_adder(name):
                def adder(*children):
                    return DOM.add_children(name, *children)
                return adder

            adder_func = make_adder(id_name)
            setattr(builtins, id_name, adder_func)

    # ---------------------------------------------------
    #  GET BLOCK BY ID
    # ---------------------------------------------------
    def get(self, id_name: str):
        return self._by_id.get(id_name)

    # ---------------------------------------------------
    #  ADD CHILDREN
    # ---------------------------------------------------
    def add_children(self, parent_id: str, *children):
        parent = self.get(parent_id)
        if parent is None:
            raise KeyError(f"No block exists with id='{parent_id}'")

        parent.add_child(*children)

        return parent

    # ---------------------------------------------------
    #  FREEZE DOM (SNAPSHOT)
    # ---------------------------------------------------
    def freeze(self):
        """
        Create a static snapshot of the DOM structure.
        This snapshot is used by template/structure engines.
        """
        from .block import Block

        # Shallow copy of actual DOM registry.

        self.snapshot = list(Block._registry)


# Singleton DOM
DOM = DOMManager()


# Expose shortcut
def add_children(parent_id: str, *children):
    return DOM.add_children(parent_id, *children)


DOM.add_children = DOM.add_children
