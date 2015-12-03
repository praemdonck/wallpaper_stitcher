from wand.image import Image
import argparse

class Monitor:
  name_index = 0
  def __init__(self, size_pixels, position_pixels, size_physical, position_physical, name=None):

    self.size_pixels = (size_pixels[0], size_pixels[1])
    self.size_physical = (float(size_physical[0]), float(size_physical[1]))
    self.position_pixels = (position_pixels[0], position_pixels[1])
    self.position_physical = (float(position_physical[0]), float(position_physical[1]))
    self.resolution = (self.size_pixels[0] / self.size_physical[0], self.size_pixels[1] / self.size_physical[1])

    if name == None:
      name = "monitor_" + str(Monitor.name_index)
      Monitor.name_index += 1

    self.name = name

  def __str__(self):
    return "Monitor %s: %dx%d pixels, size %4.1fx%4.1f inches, position %4.1f, %4.1f, PPI %4.1fx%4.1f" %  \
           (self.name,
            self.size_pixels[0], self.size_pixels[1], 
            self.size_physical[0], self.size_physical[1], 
            self.position_physical[0], self.position_physical[1],
            self.resolution[0], self.resolution[1])

  def get_max_resolution(self):
    return max(self.resolution)



# Returns the size of an image that could cover all the monitors
# if mode == PIXELS it return the size of the image in pixels using
# the highest resolution of all the monitors
def calculate_wallpaper_physical_size(monitors, mode = "PIXELS"):
  x = []
  y = []
  resolution = []
  for m in monitors:
    x.append(m.position_physical[0])
    x.append(m.position_physical[0] + m.size_physical[0])
    y.append(m.position_physical[1])
    y.append(m.position_physical[1] + m.size_physical[1])
    resolution.append(m.get_max_resolution())

  width = max(x) - min(x)
  height = max(y) - min(y)
  resolution = max(resolution)
  
  if mode == "PIXELS":
    return (int(round(width*resolution)), int(round(height*resolution)), resolution)
  else:
    return (width, height, resolution)


# Calculate the size of the resulting wallpaper based on the
# monitors size in pixels and their "virtual" location
# Note: Virtual location is where the operating system "thinks"
# the monitors are. For windows the main display is located at position (0, 0)
def calculate_wallpaper_pixel_size(monitors):
  x = []
  y = []
  for m in monitors:
    x.append(m.position_pixels[0])
    x.append(m.position_pixels[0] + m.size_pixels[0])
    y.append(m.position_pixels[1])
    y.append(m.position_pixels[1] + m.size_pixels[1])

  width = max(x) - min(x)
  height = max(y) - min(y)
  
  return (width, height)


# This function crops an image based on input_size and input_pos and then
# will resize it to output position
def resize_crop_image(image, input_size = None, input_pos = None, output_size = None):
  if input_size:
    if not input_pos: input_pos = (0, 0)
    image.transform(crop = pos_size_to_string(input_pos, input_size)) 

  if output_size: 
    image.transform(resize = str(output_size[0]) + 'x' + str(output_size[1]) + '!')


def generate_monitor_image(input_image, monitor, resolution):
  input_size = ( int(float(monitor.size_physical[0]) * resolution), 
                 int(float(monitor.size_physical[1]) * resolution) )

  input_pos = ( int(float(monitor.position_physical[0]) * resolution), 
                int(float(monitor.position_physical[1]) * resolution) )

  resize_crop_image( input_image, input_size, input_pos, monitor.size_pixels )


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






monitors = []

monitors.append(Monitor(size_pixels       = (1280, 1024), 
                        position_pixels   = (-1280, 0),
                        size_physical     = (14.9, 12.0), 
                        position_physical = (0.0, 0.0), 
                        name = "L1940T"))

monitors.append(Monitor(size_pixels       = (1680, 1050), 
                        position_pixels   = (0, 0),
                        size_physical     = (18.7, 11.7), 
                        position_physical = (15.9, 0), 
                        name = "E2220"))

#monitors.append(Monitor(size_pixels       = (1680, 1050), 
#                        position_pixels   = (300, 300),
#                        size_physical     = (18.7, 11.7), 
#                        position_physical = (0, 0), 
#                        name = "E2220_2"))

for m in monitors:
  print (m)



#input_file = "crop_View_from_connors_hill_panorama.jpg"
#input_file = "Battlefield_3_Panorama_Caspian_Border.jpg"
#input_file = "crop_tube.jpg"
#input_file = "red-circle.png"
#input_file = "381259-panoramic.jpg"
#input_file = "381254-panoramic.jpg"
#input_file = "Untitled_Panorama1.jpg"
input_file = "1680x1050_1.jpg"
output_image = "wallpaper.jpg"

def generate_wallpaper(input_image, monitors, output_image = "wallpaper.jpg", debug = False):
  x, y, resolution = calculate_wallpaper_physical_size(monitors)
  required_image_size = (x, y)

  target_image_size = calculate_wallpaper_pixel_size(monitors)
  print("Ideal input image size for the current setup: %dx%d, Aspect ratio %f:1" % ( x, y, x / float(y) ) )
  print("Output image size for the current setup: %dx%d" % (target_image_size[0], target_image_size[1]) )

  with Image(width = target_image_size[0], height = target_image_size[1]) as target_image, Image(filename = input_image) as input_image:
    resize_crop_image(input_image, output_size = required_image_size)

    for m in monitors:
      with input_image.clone() as monitor_image:
        generate_monitor_image( monitor_image, m, resolution) 

        cutting_pos, cutting_size, position_on_target = wrap_2d(target_image_size, m.position_pixels, m.size_pixels)

        if len(cutting_pos) == 1:
          target_image.composite(image = monitor_image, left = position_on_target[0][0], top = position_on_target[0][1])
        else:
          for i in range(len(cutting_pos)):
            with monitor_image.clone() as image_section:
              resize_crop_image(image_section, input_pos = cutting_pos[i], output_size = cutting_size[i])
              target_image.composite(image = image_section, left = position_on_target[i][0], top = position_on_target[i][1])


        if debug:
          print m.name
          print cutting_pos
          print cutting_size
          print position_on_target
        
    target_image.save(filename = output_image)
  
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("input_image", help="Path to the left image")
  parser.add_argument("-o", "--output_image", action="store", type=str,
                      default="wallpaper.jpg", help="set the name of the output image")
  parser.add_argument("-d", "--debug", action="store_true", help="Print debug info")
  args = parser.parse_args()
  generate_wallpaper(args.input_image, monitors, args.output_image, args.debug)
