from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Item:
    id: Optional[int]
    name: str
    description: str
    quantity: int
    price: float

    def to_dict(self):
        return asdict(self)
