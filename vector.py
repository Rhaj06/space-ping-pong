# space_pong/vector.py
from dataclasses import dataclass
import math

@dataclass
class Vector2D:
    x: float
    y: float

    def __add__(self, other): return Vector2D(self.x + other.x, self.y + other.y)
    def __mul__(self, s: float): return Vector2D(self.x * s, self.y * s)
    def magnitude(self): return math.hypot(self.x, self.y)
    def normalize(self):
        m = self.magnitude()
        return Vector2D(self.x/m, self.y/m) if m else Vector2D(0, 0)
