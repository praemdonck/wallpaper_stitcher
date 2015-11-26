import argparse, os, subprocess, shlex

def get_image_size(image):
  print image
  temp = subprocess.check_output(["identify", "-format", "%w %h", image])
  temp = temp.split()
  temp[0] = int(temp[0])
  temp[1] = int(temp[1])
  return temp

def create_blank_image(name, size_x, size_y):
  b = "'c:\Program Files\ImageMagick-6.9.2-Q8\convert' -size " + str(size_x) + "x" + str(size_y) + " canvas:none " + name
  b = shlex.split(b)
  print b
  subprocess.call(b)
  #os.system(b)
  #subprocess.call(["c:\Program Files\ImageMagick-6.9.2-Q8\convert"])
  #subprocess.call(["convert", "-size " + str(size_x) + "x" + str(size_y), "canvas:none", name])

def place_image_on_background(background, overlay, position):
  b = ['c:\Program Files\ImageMagick-6.9.2-Q8\composite'] 
  b.append("-geometry")
  b.append("+" + str(position[0]) + "+" + str(position[1]))
  b.append(overlay)
  b.append(background)
  b.append(background)
  print(b)
  subprocess.call(b)


def func_join_images(image_1, image_2, output_image_name, image_1_pos = None, image_2_pos = None, verbose = False, vertical_offset = 0):
  image_1_size = get_image_size(image_1)
  if verbose: print "Image 1 size: " + str(image_1_size)
  image_2_size = get_image_size(image_2)
  if verbose: print "Image 2 size: " + str(image_2_size)

  if vertical_offset > 0:
    image_1_pos = (0, vertical_offset)
    image_2_pos = (image_1_size[0], 0)
  elif vertical_offset < 0:
    image_1_pos = (0, 0)
    image_2_pos = (image_1_size[0], -vertical_offset)
  else:
    if not image_1_pos:
      image_1_pos = (0, 0)

    if not image_2_pos:
      image_2_pos = (image_1_pos[0] + image_1_size[0], 0)

  img_width = max(image_1_pos[0] + image_1_size[0], image_2_pos[0] + image_2_size[0])
  img_height = max(image_1_pos[1] + image_1_size[1], image_2_pos[1] + image_2_size[1])
  print "Width: " + str(img_width) + " Height: " + str(img_height)

  create_blank_image(output_image_name, img_width, img_height)
  place_image_on_background(output_image_name, image_1, image_1_pos)
  place_image_on_background(output_image_name, image_2, image_2_pos)



if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("left_image", help="Path to the left image")
  parser.add_argument("right_image", help="Path to the right image")
  parser.add_argument("-o", "--output_image", action="store", type=str,
                      default="wallpaper.jpg", help="set the name of the output image")
  parser.add_argument("-v", "--vertical_offset", action="store", type=int,
                      default=0, help="Vertical offest of the right image with respect of the left image")
  parser.add_argument("-pl", "--position_left", action="store", type=str,
                      default=None, help="Force the postion of the left image: +x+y eg +20-30")
  parser.add_argument("-pr", "--position_right", action="store", type=str,
                      default=None, help="Force the postion of the right image: +x+y eg +20-30")
  parser.add_argument("-d", "--debug", action="store_true", help="Print debug info")
  args = parser.parse_args()


  position_left = None
  position_right = None
  if args.position_left:
    position_left = args.position_left.split(',')
    position_left = [int(position_left[0]), int(position_left[1])]

  if args.position_right:
    position_right = args.position_right.split(',')
    position_right = [int(position_right[0]), int(position_right[1])]

  if args.debug:
    print "left image: " + args.left_image
    print "right image: " + args.right_image
    print "Vertical offset: " + str(args.vertical_offset)
    print "Position Left Image: " + str(position_left)
    print "Position Right Image: " + str(position_right)
    print "Output Image: " + str(args.output_image)


  func_join_images(image_1 = args.left_image, 
                   image_2 = args.right_image, 
                   output_image_name = args.output_image, 
                   image_1_pos = position_left, 
                   image_2_pos = position_right, 
                   verbose = args.debug, 
                   vertical_offset = args.vertical_offset)
