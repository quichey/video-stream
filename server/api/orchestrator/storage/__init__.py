from storage import Storage
from local_storage import LocalStorage

from util.deployment import Deployment

deployment = Deployment()

if deployment == "local":
    STORAGE = LocalStorage()
else:
    STORAGE = Storage()
