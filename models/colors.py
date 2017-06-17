class Color(object):
	def __init__(self, name, code):
		self.name = name
		self.code = code
	# colors = [
	# 	White,
	# 	Blue,
	# 	Black,
	# 	Red,
	# 	Green
	# ]
	# color_code_translation = {
	# 	color: color.code
	# 	for color in
	# 	colors+[Colorless]
	# }

WHITE = Color('White', 'W')
BLUE = Color('Blue', 'U')
BLACK = Color('Black', 'B')
RED = Color('Red', 'R')
GREEN = Color('Green', 'G')

# class White(Color):
# 	name = 'White'
# 	code = 'W'
#
# class Blue(Color):
# 	name = 'Blue'
# 	code = 'U'
#
# class Black(Color):
# 	name = 'Black'
# 	code = 'B'
#
# class Red(Color):
# 	name = 'Red'
# 	code = 'R'
#
# class Green(Color):
# 	name = 'Green'
# 	code = 'G'
#
# class Colorless(Color):
# 	name = 'Colorless'
# 	code = 'C'