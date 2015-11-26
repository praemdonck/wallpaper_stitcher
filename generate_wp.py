import subprocess
import join_images

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


def resize_crop_image(input_image, output_image, input_size_x = None, input_size_y = None, input_pos_x = None, input_pos_y = None, output_size_x = None, output_size_y = None):
  b = ["c:\Program Files\ImageMagick-6.9.2-Q8\convert"]
  b.append(input_image)

  if input_size_x and input_size_x:
    b.append("-crop")
    if not input_pos_x: input_pos_x = 0
    if not input_pos_y: input_pos_y = 0
    b.append(str(input_size_x) + "x" + str(input_size_y) + "+" + str(input_pos_x) + "+" + str(input_pos_y))

  if output_size_x and output_size_x:
    b.append("-resize")
    b.append(str(output_size_x) + "x" + str(output_size_y) + "!")
  b.append(output_image)

  print b
  subprocess.call(b)

def generate_monitor_image(input_image, output_image, monitor, ppi):
  input_size_x = int(float(monitor.size_physical_x * ppi))
  input_size_y = int(float(monitor.size_physical_y * ppi))

  input_pos_x = int(float(monitor.position_physical_x * ppi))
  input_pos_y = int(float(monitor.position_physical_y * ppi))

  resize_crop_image(input_image, 
                    output_image, 
                    input_size_x, 
                    input_size_y, 
                    input_pos_x, 
                    input_pos_y, 
                    monitor.size_pixels_x, 
                    monitor.size_pixels_y)


monitors = []
  #def __init__(self, size_pixels, size_physical, position_physical, name=None):
monitors.append(Monitor(size_pixels       = (1280, 1024), 
                        position_pixels   = (-1280, -92),
                        size_physical     = (14.9, 12.0), 
                        position_physical = (0.0, 0.0), 
                        name = "L1940T"))

monitors.append(Monitor(size_pixels       = (1680, 1050), 
                        position_pixels   = (0, 0),
                        size_physical     = (18.7, 11.7), 
                        position_physical = (15.9, 1.0), 
                        name = "E2220"))

#monitors.append(Monitor(size_pixels       = (1680, 1050), 
#                        position_pixels   = (0, 1050),
#                        size_physical     = (18.7, 11.7), 
#                        position_physical = (15.9, 12.7), 
#                        name = "E2220_2"))

print (monitors[0])
print (monitors[1])

a = calculate_wallpaper_physical_size(monitors)
b = calculate_wallpaper_pixel_size(monitors)
print(a)
print(b)
print(a[0] / float(a[1]))


input_image = "crop_View_from_connors_hill_panorama.jpg"
input_image = "Battlefield_3_Panorama_Caspian_Border.jpg"
input_image = "crop_tube.jpg"
output_image = "wallpaper.jpg"
temp_image = "temp.jpg"

join_images.create_blank_image(output_image, b[0], b[1])
resize_crop_image(input_image, temp_image, output_size_x = a[0], output_size_y = a[1])

for m in monitors:
  temp_monitor_image = m.name + ".jpg"
  generate_monitor_image( temp_image, temp_monitor_image, m, a[2])
  p_x = m.position_pixels_x
  p_y = m.position_pixels_y
  if p_x < 0: p_x += b[0]
  if p_y < 0: p_y += b[1]
  join_images.place_image_on_background(output_image, temp_monitor_image, (p_x, p_y))


#generate_monitor_image( "temp.jpg",  "temp_1.jpg", monitors[0], a[2])
#generate_monitor_image( "temp.jpg",  "temp_2.jpg", monitors[1], a[2])
