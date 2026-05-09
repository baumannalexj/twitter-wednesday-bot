from dataclasses import dataclass

from core.services.post_service import PostService


@dataclass(frozen=True)
class CoreModule:
    """
    Hex architecture POC
    * src/core should not have any dependencies on other modules
    * implement against Port interfaces
    * inject concrete classes in higher root ApplicationModules
    """
    post_service: PostService
