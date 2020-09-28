import uuid
from dataclasses import dataclass, field, asdict
from typing import List, Tuple


class Enum:
    @classmethod
    def getDict(cls):
        return {k: v for k, v in cls.__dict__.items()
                if k.islower() and not k.startswith('_')}


@dataclass
class DataClass(Enum):
    def replace(self, index: int, val):
        k, v = list(self.getDict())[index]
        setattr(self, k, val)


@dataclass
class Row(DataClass):
    files: List[str]
    position: Tuple[int, int] = (0, 0)
    size: Tuple[int, int] = (0, 0)
    pid: int = -1
    wid: List[int] = field(default_factory=list)
    hashId: str = field(default_factory=lambda: uuid.uuid4().__str__())

    def __hash__(self):
        return hash(self.hashId)

    def toDict(self):
        d = asdict(self)
        del d['pid']
        del d['wid']
        return d
