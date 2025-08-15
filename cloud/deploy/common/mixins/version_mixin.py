from datetime import datetime
import re

from util.subprocess_helper import run_cmds, run_cmd_with_retries

from cloud_providers_deployment import get_provider_class


class VersionMixin:
    def __init__(self, provider_name, context):
        self.context = context
        self.provider = get_provider_class(provider_name)(context)

    @property
    def context(self):
        return self._context

    @property
    @abstractmethod
    def repo_name(self):
        pass

    @property
    @abstractmethod
    def image_tag_base(self):
        pass

    @property
    @abstractmethod
    def tag(self):
        pass

    @abstractmethod
    def get_latest_image(self, image_tag_base, repo_name):
        pass
    
    def get_latest_version(self, image_tag_base: str, repo_name: str):
        """
        Fetch the latest semantic version tag from ACR.
        Returns "0.0.0" if no valid tags are found.
        """
        latest_image_cmd = self.provider.get_latest_image(image_tag_base=image_tag_base, repo_name=repo_name)
        result = run_cmds(
            latest_image_cmd,
            capture_output=True, text=True
        )

        tags = [t for t in result.stdout.strip().split("\n") if re.match(r"^\d+\.\d+\.\d+$", t)]
        return tags[0] if tags else "0.0.0"


    def generate_timestamped_tag(self, image_tag_base: str, repo_name: str, bump='patch'):
        """
        Generates a new Docker tag in the format:
        [MAJOR].[MINOR].[PATCH]-dev-YYYY-MM-DD--HH-MM-SS
        """
        #TODO: think about how to connect the providers classes into this
        latest = self.get_latest_version(image_tag_base, repo_name)
        major, minor, patch = map(int, latest.split("."))

        if bump == 'patch':
            patch += 1
        elif bump == 'minor':
            minor += 1
            patch = 0
        elif bump == 'major':
            major += 1
            minor = 0
            patch = 0
        else:
            raise ValueError("bump must be 'patch', 'minor', or 'major'")

        timestamp = datetime.utcnow().strftime("%Y-%m-%d--%H-%M-%S")
        return f"{major}.{minor}.{patch}-dev-{timestamp}"
