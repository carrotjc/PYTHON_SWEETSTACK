# animations/__init__.py
from animations.clouds      import CloudManager
from animations.customer    import CustomerAnimator
from animations.drops       import DropEffect, DropManager
from animations.effects     import ScorePop
from animations.decorations import DecorationManager

__all__ = [
    "CloudManager",
    "CustomerAnimator",
    "DropEffect",
    "DropManager",
    "ScorePop",
    "DecorationManager",
]