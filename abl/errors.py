"""Errors shared by the action layer and the recreate pipeline."""


class ActionError(Exception):
    """A command could not be carried out; the message is for the user."""
