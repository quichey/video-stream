from dataclasses import dataclass

@dataclass
class VideoUpload:
    #id: int
    name: str
    byte_stream: bytes
    is_done: bool