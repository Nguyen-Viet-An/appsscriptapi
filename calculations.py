import math

    
# def calculate_depth_dip_az():
x1,y1,z1 = 493509.67, 6431024.62, 247.4299927
x2,y2,z2 = 493532.728, 6431017.45, 203.739
depth = math.sqrt((x2-x1)**2+(y2-y1)**2+(z2 -z1)**2)
print(depth)    
dip = math.degrees(math.asin((z2-z1)/depth))
print(dip)
azimuth = math.degrees(math.atan2((x2-x1),(y2-y1)))
print(azimuth)

# def calculate_x_y_z():
#     x1,y1,z1 = 493509.67, 6431024.62, 247.4299927