
import random

ROWS = 25
COLUMNS = 25

TILE_SIZE = 25
W_WIDTH = TILE_SIZE * ROWS
W_HEIGHT = TILE_SIZE * COLUMNS

class Tile:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def to_dict(self):
		return {'x': self.x, 'y': self.y}
class SnakeGame:
	def __init__(self):

		#Initialize game
		self.snake = [Tile(5*TILE_SIZE, 5*TILE_SIZE)] #Head tile
		self.food = Tile(10*TILE_SIZE, 5*TILE_SIZE) #food tile
		self.snake_body = [] #snake tiles
		self.velocityX = 0
		self.velocityY = 0
		self.game_over = False
		self.score = 0
	def to_dict(self):
		#self.body()
		return {
			'snake_head': self.snake[0].to_dict(),
			'snake': [tile.to_dict() for tile in self.snake_body],
			'food': self.food.to_dict(), 
			'score': self.score
}
	def body(self):
		global velocityX, velocityY, snake, food, snake_body, game_over, score, W_WIDTH, W_HEIGHT
		#update snake body
		for i in range(len(self.snake_body)-1,  -1, -1):
			self.tile = self.snake_body[i]
			if (i == 0):
				self.snake_body[i].x = self.snake[i].x #self.tile.x
				self.snake_body[i].y = self.snake[i].y #self.tile.y
			else:
				self.tile.x = self.snake_body[i-1].x #self.prev_tile = self.snake_body[i-1]
				self.tile.y = self.snake_body[i-1].y #self.tile.x = self.prev_tile.x
				#self.tile.y = self.prev_tile.y
	def restartGame(self):
		self.snake = [Tile(5*TILE_SIZE, 5*TILE_SIZE)] #Head tile
		self.food = Tile(10*TILE_SIZE, 5*TILE_SIZE) #food tile
		self.snake_body = [] #snake tiles
		self.velocityX = 0
		self.velocityY = 0
		self.game_over = False
		self.score = 0



	def change_direction(self, direction): #changes snakes direction
		global velocityX, velocityY, game_over
		if(self.game_over):
			return

		if(direction == "UP" and self.velocityY != 1):
			self.velocityX = 0
			self.velocityY = -1
		elif (direction == "DOWN" and self.velocityY != -1):
			self.velocityX = 0
			self.velocityY = 1
		elif (direction == "LEFT" and self.velocityX != 1):
			self.velocityX = -1
			self.velocityY = 0
		elif (direction == "RIGHT" and self.velocityX != -1):
			self.velocityX = 1
			self.velocityY = 0
			
	#generates food where the snake isn't
	def snake_food(self):
		global food, snake, TILE_SIZE, COLUMNS, ROWS
		for tiles in range(0, len(self.snake_body[i-1])):
			if (self.food.x == self.snake.x and self.food.y == self.snake.y):
				self.food.x = random.randint(0, COLUMNS-1) * TILE_SIZE
				self.food.y = random.randint(0, ROWS-1) * TILE_SIZE
			else:
				self.food.x = random.randint(0, COLUMNS-1) * TILE_SIZE
				self.food.y = random.randint(0, ROWS-1) * TILE_SIZE

	def move(self):
		global velocityX, velocityY, snake, food, snake_body, game_over, score, W_WIDTH, W_HEIGHT
		if(self.game_over):
			return

		if (self.snake[0].x < 0 or self.snake[0].x >= W_WIDTH or self.snake[0].y < 0 or self.snake[0].y >= W_HEIGHT):
			game_over = True
			return

		for self.tile in self.snake_body:
			if (self.snake[0].x == self.tile.x and self.snake[0].y == self.tile.y): #changed tile to tile[0]
				game_over = True
				return

		#collission
		if (self.snake[0].x == self.food.x and self.snake[0].y == self.food.y):
			self.snake_body.append(Tile(self.food.x, self.food.y))
			self.food.x = random.randint(0, COLUMNS-1) * TILE_SIZE
			self.food.y = random.randint(0, ROWS-1) * TILE_SIZE
			self.score += 1
		self.body()
		self.snake[0].x += self.velocityX * TILE_SIZE
		self.snake[0].y += self.velocityY * TILE_SIZE



