from .storage import Storage
from .local_storage import LocalStorage

from util.deployment import Deployment

deployment = Deployment()

if deployment.deployment == "local":
    print("\n\n storage: is local \n\n")
    STORAGE = LocalStorage()
else:
    print("\n\n storage: is cloud \n\n")
    STORAGE = Storage()
