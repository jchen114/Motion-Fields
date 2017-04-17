import re

class Root():

	def __init__(self, order, axis, position, orientation):
		self.order = order
		self.axis = axis
		self.position = position,
		self.orientation = orientation

	@staticmethod
	def parse_root(str):
		order = list()
		axis = ''
		position = list()
		orientation = list()
		lines = str.splitlines()
		for str in lines:
			line = str.split()
			if line[0] == 'order':
				order = line[1:]
			elif line[0] == 'axis':
				axis = line[1]
			elif line[0] == 'position':
				position = [float(p) for p in line[1:]]
			elif line[0] == 'orientation':
				orientation = [float(o) for o in line[1:]]
		return Root(order, axis, position, orientation)

class Segment():

	def __init__(self, name, direction, length, axis, dof):
		self.name = name
		self.direction = direction
		self.length = length
		self.axis = axis
		self.dof = dof

	@staticmethod
	def parse_bone_data(str):

		segments = list()

		data = re.findall(r"(?<=begin)[\s\S]*?(?=end)", str)
		for datum in data:

			name = ''
			direction = [None] * 3
			length = None
			axis = [None] * 3
			dof = list()

			lines = datum.splitlines()
			for line in lines:
				tokens = line.split()
				if len(tokens) == 0:
					continue
				header = tokens[0]
				if header == 'name':
					name = tokens[1]
				elif header == 'direction':
					direction = [float(d) for d in tokens[1:]]
				elif header == 'length':
					length = float(tokens[1])
				elif header == 'axis':
					order = [ord(ch) - ord('X') for ch in tokens[-1]]
					values = [float(token) for token in tokens[1:-1]]
					for (o, v) in zip(order, values):
						axis[o] = v
				elif header == 'dof':
					dof = tokens[1:]
				else:
					continue

			segment = Segment(
				name,
				direction,
				length,
				axis,
				dof
			)
			segments.append(segment)
		return segments

class ASF():
	def __init__(self, root, segments):
		self.root = root
		self.segments = segments