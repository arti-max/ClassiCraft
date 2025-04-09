from ursina import *
import pprint
import json
from src.Block import Block
from src.Constants import *
from src.Level.GLOBALS import *
from src.Enums import Blocks as BlockType
from src.Logger import Logger

class Chunk(Entity):

	def __init__(self, _position):
		super().__init__(position = _position)
		self.blocks: dict = {}
		self.Blocks_Coords: dict = {}
		self.is_loaded: bool = False
		self.materials: dict = {}
		self.logger = Logger("Chunk")
		self.Batch_Delay = 0
		self.Prepare_Combined()

	def Prepare_Combined(self):
		for t in BlockType:
			if t != BlockType.Air and t != BlockType.NA:
				_C = Entity(collider=None, model=None)
				_C._Type = t
				#print(t)
				self.materials[t] = _C


	def update_blocks(self, position, type):
		pass


	def clear_material(self, _Type):
		print(f"[Chunk] Clear Material: {_Type} | {self.materials[_Type]}")
		destroy(self.materials[_Type])
		self.materials[_Type] = Entity(collider=None, model=None)
		self.materials[_Type]._Type = _Type
		for key in list(self.Blocks_Coords.keys()):  # list() создает копию ключей
			if self.Blocks_Coords[key] == _Type:
				del self.Blocks_Coords[key]


	def load(self, _Type=None):
		x_start, y_start, z_start = self.position
		#print(f"[Chunk] LOAD:")
		#print(_Type)
		positions = []
		for x in range(CHUNK_SIZE):
			for z in range(CHUNK_SIZE):
				for y in range(CHUNK_HEIGHT, 0, -1):
					global_pos = (x_start + x, y_start + y, z_start + z)
					tuple_global_pos = tuple(global_pos)


					#print(f"[Chunk] 1: {global_pos} | {tuple_global_pos}")
					# Проверяем наличие блока в Level_Blocks_Dict
					if (tuple_global_pos in Level_Blocks_Dict) and (tuple_global_pos not in self.Blocks_Coords):
						#print(f"[Chunk] 2: {Level_Blocks_Dict[global_pos]} | {tuple_global_pos}")
						if _Type == None:
							positions.append((global_pos, Level_Blocks_Dict[global_pos]))
						elif Level_Blocks_Dict[global_pos] == _Type:
							self.logger.log(f"{Level_Blocks_Dict[global_pos]} == {_Type}")
							positions.append((global_pos, Level_Blocks_Dict[global_pos]))

		self.total_blocks = len(positions)
		self.blocks_loaded = 0
		if _Type != None:
			self.Batch_Delay = 0
			self.load_blocks(positions, 16)
		else:
			self.load_blocks(positions)

	# FIXME сделать более нормальную загрузку блоков
	def load_blocks(self, positions, batch_size=8):
		for _ in range(batch_size):
			if positions:
				global_pos, block_type = positions.pop()
				#print(block_type)
				block = Block(_pos=global_pos, _parent=self, _type=block_type)
				self.blocks[global_pos] = block
				self.Blocks_Coords[global_pos] = block_type
				self.blocks_loaded += 1
			else:
				break

		if positions:
			self.optimize()
			# Планируем загрузку следующего батча блоков в следующий кадр
			invoke(self.load_blocks, positions, batch_size, delay=self.Batch_Delay)
			self.Batch_Delay += 0.2
		else:
			# Загрузка завершена
			self.is_loaded = True
			self.optimize()
			# self.update_visibility()

	# def update_visibility(self):
	# 	for block in self.blocks.values():
	# 		block.visible = distance(block.world_position, camera.world_position) < 20


	def optimize(self):
		for pos, block in self.blocks.items():
			if block.BlockType == BlockType.Grass:
				block.parent = self.materials[BlockType.Grass]
			elif block.BlockType == BlockType.Stone:
				block.parent = self.materials[BlockType.Stone]
		
		self.blocks = {}

		for _Type, _C in self.materials.items():
			_C.combine()
			_C.collider = 'mesh'
			_C.texture = 'white_cube'


	def update(self):
		if self.is_loaded:
			pass
			# self.update_visibility()

	# == Blocks == #

	def update_world_data(self, _Position, _Type):
		global Level_BLocks_List
		if _Type == BlockType.Air:	# Delete Block
			if _Position in Level_Blocks_Dict:
				del Level_Blocks_Dict[_Position]
		else:
			Level_Blocks_Dict[_Position] = _Type

	def destroy_block(self, _Position, _Material):
		_Position = tuple(_Position)
		print(f"[Chunk] position: {_Position}")
		print(f"[Chunk] Coords Len: {len(self.Blocks_Coords)}")
		pprint.pp(self.Blocks_Coords)
		if _Position in self.Blocks_Coords:
			#print(f"[Chunk] Block: {self.blocks[_Position]}")
			self.update_world_data(_Position, BlockType.Air)
			del self.Blocks_Coords[_Position]
			print(_Material)
			self.clear_material(_Material)
			self.load(_Material)
			self.optimize()