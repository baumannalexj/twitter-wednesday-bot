from dataclasses import dataclass

from core.services.post_service import PostService


@dataclass(frozen=True)
class LambdaResource:
    post_service: PostService

    def lambda_handler(self, event, context) -> None:
        self.post_service.check_if_wednesday_and_post()
        return None
