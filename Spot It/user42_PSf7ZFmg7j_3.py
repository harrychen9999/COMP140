"""
Code to implement the game of Spot it!

http://www.blueorangegames.com/spotit/

For each function, replace the return statement with your code.  Add
whatever helper functions you deem necessary.
"""

import comp140_module2 as spotit

def equivalent(trip1, trip2, mod):
    """
    Given two points, represented as tuples of 3 elements (trip1 and
    trip2), determine if they are equivalent under the given modulus
    (mod).
    """
#   This step is according to the given formula 
    product=(trip1[1]*trip2[2]-trip1[2]*trip2[1],trip1[2]*trip2[0]-trip1[0]*trip2[2],trip1[0]*trip2[1]-trip1[1]*trip2[0])
    if product[0]%mod ==0 and product[1] % mod == 0 and product[2] % mod == 0:
            return True
    else:
            return False

def incident(point, line, mod):
    """
    Given a point and a line, each represented as tuples of 3
    elements, determine if the point lies on that line under the given
    modulus (mod).
    """
#   This step is according to the given formula 
    if (point[0]*line[0]+point[1]*line[1]+point[2]*line[2]) % mod == 0:
        return True
    else:
        return False

def generate_all_points(mod):
    """
    Generate all unique points for the given modulus (mod).  Returns a
    list of unique points, each represented as a tuple of 3 elements.
    """
#   Generate all points by assigning the value of number0 to the first element 
#	assigning the value of number1 to the second element and assigning the 
#	value of number2 to the third element
    uniquepoints=[]
    for number0 in range (mod):
        for number1 in range (mod):
            for number2 in range (mod):
#	Determine if the point is(0,0,0), if the point is not, add it into the list uniquepoints 
                if(number0 != 0 or number1 != 0 or number2 != 0):
                    totalpoints=(number0,number1,number2)
                    uniquepoints.append(totalpoints)
#	Determine if two points are same, if they are, remove one point from the list 
#	uniquepoints
                    for position1 in range(0,len(uniquepoints)-1):
                        for position2 in range(position1+1,len(uniquepoints)):
                            if((equivalent(uniquepoints[position1], uniquepoints[position2], mod))==True):
                                uniquepoints.pop(position2)
    return uniquepoints

def create_cards(points, lines, mod):
    """
    Return a list of cards given a list of points, list of lines, and
    a modulus (mod).  Each element of the returned list should be a
    list of integers.
    """
  
    total_cards=[]
    for cards in lines:
        new_lines=[]
        for picture in points:
#		determine if images belong to each card, if they belong, use index()
#		to represent these images as integers
            if(incident(picture,cards,mod)==True):
                new_lines.append(points.index(picture))
               
        total_cards.append(new_lines)
        

    return total_cards
   

def run():
    """
    Create the deck and play the game.
    """
    # Prime modulus
    # Set to 2 or 3 during development
    # Set to 7 for the actual game
    modulus = 7

    # Generate all unique points for the given modulus
    points = generate_all_points(modulus)

    # Lines are the same as points, so make a copy
    lines = points[:]

    # Generate a deck of cards given the points and lines
    deck = create_cards(points, lines, modulus)

    # Run GUI - uncomment the line below after you have implemented
    #           everything and you can play your game.  The GUI does
    #           not work if the modulus is larger than 7.

    spotit.start(deck)
 
run()
