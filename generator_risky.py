from __future__ import print_function
import random
import math
import copy
from termcolor import colored
import sys

def main():
	#############
	#############

	#GENERATOR SETTINGS:
	size_x = 4
	size_y = 4
	num_tries = 1000
	complexity = 3

	##############
	##############
	
	b = Board(size_x,size_y)
	#b.generate_level()
	#b.generate_test_level()
	seed = random.randint(0,1000000)
	
	for i in xrange(0,num_tries):
		seed = random.randint(0,1000000)
		#seed = 88127
		if b.build_level(seed,complexity):
			print(seed)
			print("exportable:")
			b.export_level()
			break
		b.clean_grid()
		print(i)
	b.print_board()
	print(b.can_reach(0,0,size_x - 1,size_y - 1,[0,0,0]),len(b.can_reach(0,0,size_x - 1,size_y - 1,[0,0,0])) - 1)


class Board:
	def __init__(self,size_x, size_y):
		self.size_x = size_x
		self.size_y = size_y
		self.background_color = [0,0,0]
		self.grid = []
		for i in xrange(size_x):
			row = []
			for j in xrange(size_y):
				row.append(["empty",[0,0,0]])
			self.grid.append(row)
	def clean_grid(self):
		self.grid = []
		for i in xrange(self.size_x):
			row = []
			for j in xrange(self.size_y):
				row.append(["empty",[0,0,0]])
			self.grid.append(row)
	def generate_level(self):
		for i in xrange(self.size_x):
			for j in xrange(self.size_y):
				r = random.random()
				color = [round(random.random()),round(random.random()),round(random.random())]
				if r > 0.5:
					self.grid[i][j] = ["block",list(color)]
				if r > 0.8:
					self.grid[i][j] = ["switch",list(color)]
		self.grid[0][0] = ["empty",[0,0,0]]
		self.grid[self.size_x - 1][self.size_y - 1] = ["empty",[0,0,0]]
	def generate_test_level(self):
		#orginal test
		"""self.grid[3][4] = ["block",[1,1,1]]
		self.grid[3][3] = ["block",[1,1,1]]
		self.grid[3][2] = ["block",[1,1,1]]
		self.grid[3][1] = ["block",[1,0,0]]
		self.grid[3][0] = ["block",[1,0,1]]
		self.grid[2][3] = ["block",[1,0,0]]
		self.grid[2][2] = ["switch",[1,0,0]]"""
		#first problem
		"""self.grid[0][1] = ["block",[1,0,0]]
		self.grid[1][0] = ["switch",[0,1,0]]
		self.grid[1][3] = ["block",[0,1,1]]
		self.grid[1][4] = ["block",[0,1,1]]
		self.grid[2][2] = ["block",[0,1,0]]
		self.grid[3][1] = ["block",[1,0,0]]
		self.grid[4][0] = ["block",[0,1,1]]"""
		#second problem
		"""self.grid[1][2] = ["block",[0,1,0]]
		self.grid[2][1] = ["block",[0,0,1]]
		self.grid[1][1] = ["block",[1,0,0]]
		self.grid[0][1] = ["block",[1,0,0]]
		self.grid[2][0] = ["switch",[0,1,0]]
		self.grid[1][0] = ["switch",[1,0,0]]"""
		self.grid[2][2] = ["block",[1,1,1]]
		self.grid[2][1] = ["block",[1,1,1]]
		self.grid[2][0] = ["block",[1,1,1]]
		self.grid[0][2] = ["block",[1,0,0]]
		self.grid[1][2] = ["block",[1,0,1]]
		self.grid[2][2] = ["block",[1,0,0]]

	def switches_pressed(self, path):
		pressed = 0
		for step in path:
			if self.grid[step[0]][step[1]][0] == "switch":
				pressed += 1
		return pressed

	def build_level(self,seed,complexity):
		random.seed(seed)
		#we'll see
		#first we make the level more complicated then we make it solveable
		empty_blocks = []
		for i in xrange(self.size_x):
			for j in xrange(self.size_y):
				empty_blocks.append([i,j])
		empty_blocks.remove([0, 0])
		empty_blocks.remove([self.size_x - 1, self.size_y - 1])
		added_blocks = []

		previous_level = None
		current_level = None

		blocks_on_board = []

		#fill
		for k in xrange(0,complexity):
			old_soln = self.can_reach(0,0,self.size_x-1,self.size_y-1,[0,0,0])

			#shuffle the board a little
			for i in xrange(10):
				#add some new moves to the generator
				#swap a block
				"""if len(blocks_on_board) > 0 and random.random() > 0.3:
					if len(empty_blocks) > 0:
						nPos = empty_blocks[random.randint(0,len(empty_blocks) - 1)]
						oPos = blocks_on_board[random.randint(0,len(blocks_on_board) - 1)]
						old_b = list(self.grid[oPos[0]][oPos[1]])
						self.grid[oPos[0]][oPos[1]] = ["empty",[0,0,0]]
						self.grid[nPos[0]][nPos[1]] = old_b
						soln = self.can_reach(0,0, self.size_x-1, self.size_y-1,[0,0,0])
						if self.switches_pressed(soln) >= self.switches_pressed(old_soln):
							self.grid[nPos[0]][nPos[1]] = ["empty",[0,0,0]]
							self.grid[oPos[0]][oPos[1]] = old_b
						else:
							empty_blocks.remove(nPos)
							empty_blocks.append(oPos)
							blocks_on_board.remove(oPos)"""
				#change the color of a block
				if len(blocks_on_board) > 0 and random.random() > 0.7:
					oPos = blocks_on_board[random.randint(0,len(blocks_on_board) - 1)]
					o_col = self.grid[oPos[0]][oPos[1]][1]
					if self.grid[oPos[0]][oPos[1]][0] == "switch":
						col = [0,0,0]
						col[random.randint(0,2)] = 1
					else:
						col = [round(random.random()),round(random.random()),round(random.random())]
						if col == [0,0,0]:
							col[random.randint(0,2)] = 1
						"""if col == [1,1,1]:
							col[random.randint(0,2)] = 0"""
					self.grid[oPos[0]][oPos[1]][1] = col
					soln = self.can_reach(0,0, self.size_x-1, self.size_y-1,[0,0,0])
					if not self.switches_pressed(soln) >= self.switches_pressed(old_soln):
						self.grid[oPos[0]][oPos[1]][1] = o_col

			#self.print_board()
			#print(self.can_reach(0,0,3,3,[0,0,0]))
			added_blocks = []
			fail_time = 300
			while len(self.can_reach(0,0,self.size_x-1,self.size_y-1,[0,0,0])) > 0:
				fail_time -= 1
				if fail_time == 0:
					print("Could not make level ;")
					return False
				block_pos = None
				if (len(empty_blocks) == 0 and random.random() > 0.7) and len(added_blocks) > 0:
					if len(added_blocks) == 1:
						block_pos = added_blocks[0]
					else:
						block_pos = added_blocks[random.randint(0,len(added_blocks) - 1)]
				elif len(empty_blocks):
					if len(empty_blocks) == 1:
						block_pos = empty_blocks[0]
					else:
						block_pos = empty_blocks[random.randint(0,len(empty_blocks) - 1)]
					added_blocks.append(block_pos)
					empty_blocks.remove(block_pos)
				if block_pos is not None:
					if random.random() > 0.8:
						#try a block
						col = [round(random.random()),round(random.random()),round(random.random())]
						if col == [0,0,0]:
							col[random.randint(0,2)] = 1
						self.grid[block_pos[0]][block_pos[1]] = ["block", col]
					else:
						#try a switch
						col = [0,0,0]
						col[random.randint(0,2)] = 1
						#check to see if it made a short cut
						self.grid[block_pos[0]][block_pos[1]] = ["switch",col]
						soln = self.can_reach(0,0,self.size_x-1,self.size_y-1,[0,0,0])
						if len(soln) > 0:
							self.grid[block_pos[0]][block_pos[1]] = ["empty",[0,0,0]]
							added_blocks.remove(block_pos)
							empty_blocks.append(block_pos)

			#remove non essential blocks
			for bpos in added_blocks:
				old_block = list(self.grid[bpos[0]][bpos[1]])
				self.grid[bpos[0]][bpos[1]] = ["empty",[0,0,0]]
				if self.can_reach(0,0,self.size_x-1,self.size_y-1,[0,0,0]):
					self.grid[bpos[0]][bpos[1]] = old_block
					blocks_on_board.append(bpos)
				else:
					empty_blocks.append(bpos)
					#added_blocks.remove(block_pos)

			#self.print_board()
			#print("yo")
			"""print(self.can_reach(0,0,3,3,[0,0,0]))"""
			fail_time = 300
			added_blocks = []
			#print("cr",len(self.can_reach(0,0,self.size_x-1,self.size_y-1,[0,0,0])))
			while len(self.can_reach(0,0,self.size_x-1,self.size_y-1,[0,0,0])) < 1:
				fail_time -= 1
				if fail_time == 0:
					print("Could not make level -")
					return False
				block_pos = None
				
				if (len(empty_blocks) == 0 and random.random() > 0.7) and len(added_blocks) > 0:
					if len(added_blocks) == 1:
						block_pos = added_blocks[0]
					else:
						block_pos = added_blocks[random.randint(0,len(added_blocks) - 1)]
				elif len(empty_blocks) > 0:
					if len(empty_blocks) == 1:
						block_pos = empty_blocks[0]
					else:
						block_pos = empty_blocks[random.randint(0,len(empty_blocks) - 1)]
					added_blocks.append(block_pos)
					empty_blocks.remove(block_pos)
				if block_pos is not None:
					col = [0,0,0]
					col[random.randint(0,2)] = 1
					#check to see if it made a short cut
					self.grid[block_pos[0]][block_pos[1]] = ["switch",col]
					soln = self.can_reach(0,0,self.size_x-1,self.size_y-1,[0,0,0])
					#self.grid = backup_grid
					if len(soln) > len(old_soln):
						self.grid[block_pos[0]][block_pos[1]] = ["switch",col]
					else:
						self.grid[block_pos[0]][block_pos[1]] = ["empty",[0,0,0]]
						#previous_level[block_pos[0]][block_pos[1]] = ["empty",[0,0,0]]
						added_blocks.remove(block_pos)
						empty_blocks.append(block_pos)
			#remove non essential blocks
			for bpos in added_blocks:
				old_block = list(self.grid[bpos[0]][bpos[1]])
				self.grid[bpos[0]][bpos[1]] = ["empty",[0,0,0]]

				soln = self.can_reach(0,0,self.size_x-1,self.size_y-1,[0,0,0])
				if len(soln) < len(old_soln):
					self.grid[bpos[0]][bpos[1]] = old_block
					blocks_on_board.append(bpos)
					#previous_level[bpos[0]][bpos[1]] = 
				else:
					#current_level[bpos[0]][bpos[1]] = ["empty",col]
					empty_blocks.append(bpos)
		return True

	def print_board(self):
		for i in xrange(self.size_x):
			print("")
			for j in xrange(self.size_y):
				print(colored(self.grid[i][j][0][0], self.color_to_string(self.grid[i][j][1])), end="") 
		print("")
	def color_to_string(self,color):
		if color == [1,0,0]:
			return 'red'
		elif color == [0,1,0]:
			return 'blue'
		elif color == [0,0,1]:
			return 'green'
		elif color == [1,1,0]:
			return 'magenta'
		elif color == [1,0,1]:
			return 'yellow'
		elif color == [0,1,1]:
			return 'cyan'
		elif color == [1,1,1]:
			return 'white'
	def export_level(self):
		print(self.size_x,self.size_y)
		print(0)
		for i in xrange(self.size_x):
			for j in xrange(self.size_y):
				if self.grid[i][j][0] == "empty":
					print("e ",end = "")
				elif self.grid[i][j][0] == "block":
					print(self.color_to_string(self.grid[i][j][1])[0],end=" ")
				elif self.grid[i][j][0] == "switch":
					s = self.color_to_string(self.grid[i][j][1]).upper()
					print(s[0],end=" ")
			print("")

	#colored bellman ford!
	def can_reach(self,start_x, start_y, target_x, target_y, background_color):
		marked_grid = []
		for i in xrange(self.size_x):
			row = []
			for j in xrange(self.size_y):
				row.append({})
			marked_grid.append(row)
		queue = [[0,0,tuple(background_color),0]]
		marked_grid[start_x][start_y][tuple(background_color)] = 0
		#queue.append(marked_grid)
		found_path = False
		while len(queue) > 0:
			position = queue.pop(0)
			x = position[0]
			y = position[1]
			background_color = list(position[2])
			number = position[3]
			if x == target_x and y == target_y:
				found_path = True
				continue
			#marked_grid[x][y].append(list(background_color))
			#add neighbors
			if self.grid[x][y][0] == "switch":
				#print("switched")
				for k in xrange(3):
					background_color[k] = (background_color[k] + self.grid[x][y][1][k]) % 2
			for i in xrange(-1,2):
				for j in xrange(-1,2):
					if (i == 0 or j == 0) and x+i > -1 and x+i < self.size_x and y+j > -1 and y+j < self.size_y and not (i==0 and j==0):
						if tuple(background_color) in marked_grid[x+i][y+j].keys():
							if number >= marked_grid[x+i][y+j][tuple(background_color)]:
								continue
						if self.grid[x + i][y + j][0] == "empty":
							"""if x + i == target_x and y + j == target_y:
								return True"""
							marked_grid[x+i][y+j][tuple(background_color)] = number + 1
							queue.append([x+i,y+j,tuple(background_color),number + 1])
						elif self.grid[x + i][y + j][0] == "block":
							if background_color == self.grid[x + i][y + j][1]:
								queue.append([x+i,y+j,tuple(background_color), number + 1])
								marked_grid[x+i][y+j][tuple(background_color)] = number + 1
						elif self.grid[x + i][y + j][0] == "switch":
							#toggle switch
							marked_grid[x+i][y+j][tuple(background_color)] = number + 1
							queue.append([x+i,y+j,tuple(background_color),number + 1])
		if not found_path:
			return []
		else:
			#countdown
			path = []
			x = target_x
			y = target_y
			num = 100000
			index = -1
			#print(marked_grid[x][y])
			#print("-*-*-*-")
			path.append([target_x,target_y])
			for key in marked_grid[x][y].keys():
				if marked_grid[x][y][key] < num:
					num = marked_grid[x][y][key]
					index = key
			#o_num = num
			#print("attempting to backtrack",num)
			while num > 0:
				found_next = False
				for i in xrange(-1,2):
					ddBreak = False
					for j in xrange(-1,2):
						if (i == 0 or j == 0) and x+i > -1 and x+i < self.size_x and y+j > -1 and y+j < self.size_y and not (i==0 and j==0):
							#print("g:",marked_grid[x+i][y+j])
							#print("c:",index)
							colr = tuple(index)
							if self.grid[x + i][y + j][0] == "switch":
								#print("is_switch")
								col = list(index)
								for k in xrange(3):
									col[k] = int((col[k] + self.grid[x + i][y + j][1][k]) % 2)
								colr = tuple(col)
								"""print(colr)
								print(colr in marked_grid[x+i][y+j].keys())
								print"""
							#print("*****")
							#print(marked_grid[x+i][y+i])
							if colr in marked_grid[x+i][y+j].keys():
								if marked_grid[x+i][y+j][colr] == num - 1:
									index = colr
									x = x+i
									y = y+j
									path.append([x,y])
									num = num - 1
									"""if x == start_x and y == start_y:
										print ("path",path, num)"""
									#print(num,[x,y])
									#print("---------------------")
									ddBreak = True
									found_next = True
									break
					if ddBreak:
						break
				if not found_next:
					break
			path.reverse()
			return path

if __name__ == "__main__":
    main()