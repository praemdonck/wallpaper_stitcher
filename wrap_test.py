from numbers import Number


def wrap_1d(target_size, overlay_pos, overlay_size):
  overlay_pos = overlay_pos % target_size
  cutting_points = target_size
  position = [overlay_pos]
  points = [0]
  size = []
  temp = 0
  while True:
    cutting_points = min(cutting_points, overlay_pos + overlay_size)
    t = cutting_points - overlay_pos
    size.append(t - temp)
    temp = t
    if cutting_points == (overlay_pos + overlay_size): break
    points.append(t)
    position.append(cutting_points % target_size)
    cutting_points += target_size
   
  return [points, size, position]


def wrap_2d(target_size, overlay_pos, overlay_size):
  cutting_pos_x, cutting_size_x, position_on_target_x = wrap_1d(target_size[0], overlay_pos[0], overlay_size[0])
  cutting_pos_y, cutting_size_y, position_on_target_y = wrap_1d(target_size[1], overlay_pos[1], overlay_size[1])

  cutting_pos = []
  cutting_size = []
  position_on_target = []

  for i in range(len(cutting_pos_x)):
      for j in range(len(cutting_pos_y)):
        cutting_pos.append([cutting_pos_x[i], cutting_pos_y[j]])
        cutting_size.append([cutting_size_x[i], cutting_size_y[j]])
        position_on_target.append([position_on_target_x[i], position_on_target_y[j]])

  return [cutting_pos, cutting_size, position_on_target]

def pos_size_to_string(position, size):
  if position[0] < 0: p0 = str(position[0]) 
  else: p0 = '+' + str(position[0])

  if position[1] < 0: p1 = str(position[1]) 
  else: p1 = '+' + str(position[1])

  return str(size[0]) + 'x' + str(size[1]) + p0 + p1

if __name__ == '__main__':
  target_size = (100, 100)
  overlay_size = (50, 50)
  overlay_pos = (75, 75)
  cutting_pos, cutting_size, position_on_target= wrap_2d(target_size, overlay_pos, overlay_size)

  print cutting_pos
  print cutting_size
  print position_on_target
  print pos_size_to_string(cutting_pos[0], cutting_size[0])
