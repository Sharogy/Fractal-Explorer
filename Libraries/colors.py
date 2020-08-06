def hex_to_RGB(hex):
  ''' "#FFFFFF" -> [255,255,255] '''
  # Pass 16 to the integer function for change of base
  lst = []
  for i in range(1, 6, 2):
    lst.append(int(hex[i:i+2], 16))
  return lst


def RGB_to_hex(rgb):
  ''' [255,255,255] -> "#FFFFFF" '''
  # Components need to be integers for hex to make sense
  RGB = []
  for x in rgb:
    RGB.append(int(x))
  res = '#'
  lst = []
  for v in RGB:
    if v < 16:
      lst.append("0{0:x}".format(v))
    else:
      lst.append("{0:x}".format(v))
  return res + "".join(lst)

def color_dict(gradient):
  ''' Takes in a list of RGB sub-lists and returns dictionary of
    colors in RGB and hex form for use in a graphing function
    defined later on '''
  lst = []
  for RGB in gradient:
    lst.append(RGB_to_hex(RGB))
  return lst

def color_gradient(start_hex, finish_hex, n=10):
  ''' returns a gradient list of (n) colors between
    two hex colors. start_hex and finish_hex
    should be the full six-digit color string,
    inlcuding the number sign ("#FFFFFF") '''
  # Starting and ending colors in RGB form
  s = hex_to_RGB(start_hex)
  f = hex_to_RGB(finish_hex)
  # Initilize a list of the output colors with the starting color
  RGB_list = [s]
  # Calcuate a color at each evenly spaced value of t from 1 to n
  for t in range(1, n):
    # Interpolate RGB vector for color at the current value of t
    curr_vector = []

    for j in range(3):
      curr_vector.append((s[j] + (float(t)/(n-1))*(f[j]-s[j])))
    # Add it to our list of output colors
    RGB_list.append(curr_vector)

  return color_dict(RGB_list)


