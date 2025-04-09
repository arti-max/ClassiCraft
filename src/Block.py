from ursina import *
from src.Enums import Blocks as BlockType


class Block(Entity):
	def __init__(self, _parent, _pos, _type):
		super().__init__(
			model='cube',
			color=color.blue,
			parent=_parent,
			position=_pos,
			collider='box',
			texture='white_cube'
			)
		if _type == BlockType.Grass:
			self.color = color.green
		elif _type == BlockType.Stone:
			self.color = color.gray
		self.BlockType = _type