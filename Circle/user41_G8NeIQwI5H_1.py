"""
Code to calculate the circle that passes through three given points.

Fill in each function with your code (including fixing the return
statement).
"""

import math
import comp140_module1 as circles

def distance(point0x, point0y, point1x, point1y):
    """
    Given two points return the distance between them
    """
    distance_between_points=math.sqrt((point1x-point0x)**2+(point1y-point0y)**2)

    return distance_between_points

def midpoint(point0x, point0y, point1x, point1y):
    """
    Given two points, return the point that is the midpoint between them
    """
    point0x=float(point0x)
    point0y=float(point0y)
    point1x=float(point1x)
    point1y=float(point1y)
    
    x_mid_point=(point0x+point1x)/2
    y_mid_point=(point0y+point1y)/2
    
    return x_mid_point, y_mid_point

def slope(point0x, point0y, point1x, point1y):
    """
    Given two points, return the slope of the line that connects them

    point0x and point1x must be different
    """
    point0x=float(point0x)
    point0y=float(point0y)
    point1x=float(point1x)
    point1y=float(point1y)
    
    slope_between_points=(point1y-point0y)/(point1x-point0x)

    return slope_between_points

def perp(lineslope):
    """
    Return the slope of a line perpendicular to the line with lineslope

    lineslope must be non-zero
    """
    perp_slope=-1.0/lineslope
    
    return perp_slope

def intersect(slope0, point0x, point0y, slope1, point1x, point1y):
    """
    Find the intersection point of two lines

    slope1 and slope2 must be different
    """
    slope0=float(slope0)
    point0x=float(point0x)
    point0y=float(point0y)
    
    y_intersect0=point0y-slope0*point0x
    y_intersect1=point1y-slope1*point1x
    
    intersect_x= (y_intersect1- y_intersect0)/(slope0-slope1)
    intersect_y=intersect_x*slope0+y_intersect0
    
    return intersect_x, intersect_y

def make_circle(point0x, point0y, point1x, point1y, point2x, point2y):
    """
    Given three points, return the center and radius of a circle that 
    intersects them

    The points must not be co-linear and no two points can have the 
    same x or y values.
    """
    point0x=float(point0x)
    point0y=float(point0y)
    point1x=float(point1x)
    point1y=float(point1y)
    point2x=float(point2x)
    point2y=float(point2y)
    
    x_midpoint1,y_midpoint1=midpoint(point0x, point0y, point1x, point1y)
    slope1=slope(point0x, point0y, point1x, point1y)
    perpendicular_slope1=perp(slope1)
   
    x_midpoint2,y_midpoint2=midpoint(point1x, point1y, point2x, point2y)
    slope2=slope(point1x, point1y, point2x, point2y)
    perpendicular_slope2=perp(slope2)
    
    intersectx,intersecty=intersect(perpendicular_slope1,x_midpoint1,y_midpoint1,perpendicular_slope2,x_midpoint2,y_midpoint2)
    radius=math.sqrt((intersectx-point0x)**2+(intersecty-point0y)**2)
    
    return intersectx, intersecty, radius




