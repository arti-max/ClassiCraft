from ursina import *
from src.Constants import *
from src.Level.Chunk import Chunk
from src.Level.GLOBALS import *
from src.Enums import Blocks as BlockType
from src.Logger import Logger
import random
import math


class World:
	def __init__(self, _player):
		self.chunks = {}
		self.loaded_chunks = set()
		self.__player = _player
		self.last_player_chunk_position = None
		self.__Start = True
		self.logger = Logger("World")
		self.generate_level()


	def generate_level(self):
		for x in range(WORLD_SIZE):
			for z in range(WORLD_SIZE):
				for y in range(CHUNK_HEIGHT):
					pos = (x, y, z)
					if y > 1:
						Level_Blocks_Dict[tuple(pos)] = BlockType.Grass
					else:
						Level_Blocks_Dict[tuple(pos)] = BlockType.Stone


		Level_Blocks_List = [[x, y, z, block_type] for (x, y, z), block_type in Level_Blocks_Dict.items()]
		print("Generated!")

	def get_chunk_position(self, world_position):
		return (
			int(world_position[0] // CHUNK_SIZE),
			int(world_position[2] // CHUNK_SIZE)
		)

	def update_chunks(self):
		player_chunk_position = self.get_chunk_position(self.__player.position)

		if player_chunk_position == self.last_player_chunk_position:
			return

		self.last_player_chunk_position = player_chunk_position
		# self.__player.freeze()
		Load_Delay = 0

		for x in range(-RENDER_DISTANCE, RENDER_DISTANCE + 1):
			for z in range(-RENDER_DISTANCE, RENDER_DISTANCE + 1):
				chunk_x = player_chunk_position[0] + x
				chunk_z = player_chunk_position[1] + z
				chunk_key = (chunk_x, chunk_z)

				if chunk_key not in self.loaded_chunks:
					if 0 <= chunk_x < WORLD_SIZE // CHUNK_SIZE and 0 <= chunk_z < WORLD_SIZE // CHUNK_SIZE:
						invoke(self.load_chunk, chunk_key, delay=Load_Delay)
						Load_Delay += 0.5

	def load_chunk(self, chunk_key):
		chunk_position = (chunk_key[0] * CHUNK_SIZE, 0, chunk_key[1] * CHUNK_SIZE)
		chunk = Chunk(_position=chunk_position)
		self.chunks[chunk_key] = chunk
		self.loaded_chunks.add(chunk_key)
		chunk.load()
		# self.__player.unfreeze()

	# == lists == #
	def add_to_level_blocks_list(self, position, type):
		global Level_BLocks_List
		entry = [position[0], position[1], position[2]]
		if entry not in Level_BLocks_List:
			Level_BLocks_List.append(entry)

	def remove_from_level_blocks_list(self, position):
		global Level_BLocks_List
		Level_BLocks_List = [entry for entry in Level_BLocks_List if entry[:3] != list(position)]

	# == main loop == #
	def update(self):
		self.update_chunks()


	# == Blocks == #

	def destroy_block(self):
		hit_info = raycast(camera.world_position, camera.forward, distance=8)
		print(f"{hit_info.hit} | {hit_info.point} | {hit_info.world_point} | {hit_info.normal}")
		if hit_info.hit and hit_info.entity:
			print(f"Material: {hit_info.entity._Type}")
			position = Vec3(round(hit_info.point.x), round(hit_info.point.y), round(hit_info.point.z)) + hit_info.normal
			print(f"Position: {position}")
			chunk_coords = self.get_chunk_position(position)
			self.logger.log(f"CHUNK COORDS {chunk_coords}")
			if chunk_coords in self.chunks:
				print(f"CHUNK!!")
				chunk = self.chunks[chunk_coords]
				chunk.destroy_block((position[0], position[1], position[2]), hit_info.entity._Type)
				self.remove_from_level_blocks_list(position)

