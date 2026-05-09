from dataclasses import dataclass

from core.services.post_service import PostService


""" 
Hex architecture POC
* src/core should not have any dependencies on other modules
* implement against Port interfaces
* inject concrete classes in higher root ApplicationModules
"""


@dataclass(frozen=True)
class CoreModule:
    """Wire up in application module"""
    post_service: PostService
