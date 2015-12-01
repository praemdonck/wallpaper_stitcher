from wand.image import Image
import wrap_test

class Monitor:
  name_index = 0
  def __init__(self, size_pixels, position_pixels, size_physical, position_physical, name=None):

    self.size_pixels_x = size_pixels[0]
    self.size_pixels_y = size_pixels[1]

    self.size_physical_x = float(size_physical[0])
    self.size_physical_y = float(size_physical[1])

    self.position_pixels_x = position_pixels[0]
    self.position_pixels_y = position_pixels[1]

    self.position_physical_x = float(position_physical[0])
    self.position_physical_y = float(position_physical[1])

    self.ppi_x = self.size_pixels_x / self.size_physical_x
    self.ppi_y = self.size_pixels_y / self.size_physical_y

    if name == None:
      name = "monitor_" + str(Monitor.name_index)
      Monitor.name_index += 1

    self.name = name

  def __str__(self):
    return "Monitor %s: %dx%d pixels, size %4.1fx%4.1f inches, position %4.1f, %4.1f, PPI %4.1fx%4.1f" %  \
           (self.name,
            self.size_pixels_x, self.size_pixels_y, 
            self.size_physical_x, self.size_physical_y, 
            self.position_physical_x, self.position_physical_y,
            self.ppi_x, self.ppi_y)

  def get_max_ppi(self):
    return max(self.ppi_x, self.ppi_y)



def calculate_wallpaper_physical_size(monitors, mode = "PIXELS"):
  x = []
  y = []
  ppi = []
  for m in monitors:
    x.append(m.position_physical_x)
    x.append(m.position_physical_x + m.size_physical_x)
    y.append(m.position_physical_y)
    y.append(m.position_physical_y + m.size_physical_y)
    ppi.append(m.get_max_ppi())

  width = max(x) - min(x)
  height = max(y) - min(y)
  ppi = max(ppi)
  
  if mode == "PIXELS":
    return (int(round(width*ppi)), int(round(height*ppi)), ppi)
  else:
    return (width, height, ppi)


def calculate_wallpaper_pixel_size(monitors):
  x = []
  y = []
  for m in monitors:
    x.append(m.position_pixels_x)
    x.append(m.position_pixels_x + m.size_pixels_x)
    y.append(m.position_pixels_y)
    y.append(m.position_pixels_y + m.size_pixels_y)

  width = max(x) - min(x)
  height = max(y) - min(y)
  
  return (width, height)


#def resize_crop_image(image, input_size = None, input_pos = None, output_size = None):
#  if not output_size: output_size = input_size
#  if not input_size: input_size = output_size
#  if not input_size: return
#  if not input_pos: input_pos = (0, 0)
#
#  image.transform(crop = wrap_test.pos_size_to_string(input_pos, input_size), 
#                  resize = str(output_size[0]) + 'x' + str(output_size[1]) + '!')

def resize_crop_image(image, input_size = None, input_pos = None, output_size = None):
  if input_size:
    if not input_pos: input_pos = (0, 0)
    image.transform(crop = wrap_test.pos_size_to_string(input_pos, input_size)) 

  if output_size: 
    image.transform(resize = str(output_size[0]) + 'x' + str(output_size[1]) + '!')

def generate_monitor_image(input_image, monitor, ppi):
  input_size = ( int(float(monitor.size_physical_x * ppi)), int(float(monitor.size_physical_y * ppi)) )
  input_pos = ( int(float(monitor.position_physical_x * ppi)), int(float(monitor.position_physical_y * ppi)) )
  output_size = (monitor.size_pixels_x, monitor.size_pixels_y)

  resize_crop_image( input_image, input_size, input_pos, output_size )


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

a = calculate_wallpaper_physical_size(monitors)
out_size = (a[0], a[1])
resolution = a[2]

target_image_size = calculate_wallpaper_pixel_size(monitors)
print(a)
print(target_image_size)
# Aspect ratio
print(a[0] / float(a[1]))


#input_file = "crop_View_from_connors_hill_panorama.jpg"
#input_file = "Battlefield_3_Panorama_Caspian_Border.jpg"
#input_file = "crop_tube.jpg"
#input_file = "red-circle.png"
input_file = "381259-panoramic.jpg"
#input_file = "Untitled_Panorama1.jpg"
output_image = "wallpaper.jpg"

with Image(width = target_image_size[0], height = target_image_size[1]) as target_image, Image(filename = input_file) as input_image:
  resize_crop_image(input_image, output_size=out_size)

  for m in monitors:
    temp_monitor_image = m.name + ".jpg"
    with input_image.clone() as monitor_image:
      generate_monitor_image( monitor_image, m, resolution) 

      cutting_pos, cutting_size, position_on_target = wrap_test.wrap_2d(target_image_size, (m.position_pixels_x, m.position_pixels_y), (m.size_pixels_x, m.size_pixels_y))

      if len(cutting_pos) == 1:
        target_image.composite(image = monitor_image, left = position_on_target[0][0], top = position_on_target[0][1])
      else:
        for i in range(len(cutting_pos)):
          with monitor_image.clone() as image_section:
            resize_crop_image(image_section, input_pos = cutting_pos[i], output_size = cutting_size[i])
            target_image.composite(image = image_section, left = position_on_target[i][0], top = position_on_target[i][1])


      print cutting_pos
      print cutting_size
      print position_on_target
      print temp_monitor_image
      
  target_image.save(filename = output_image)
  
