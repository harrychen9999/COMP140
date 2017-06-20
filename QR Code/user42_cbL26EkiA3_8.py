"""
QR Code Generator
"""

import comp140_module5 as qrcode
import comp140_module5_z256 as z256

def divide_terms(coefficient1, power1, coefficient2, power2):
    """
    Divide the first term, coefficient1*x^power1, by the
    second term, coefficient2*x^power2. This method requires
    that coefficient2 <= coefficient1.

    Returns an instance of a Polynomial representing the resulting
    term.
    """
    # From recipe: (a*x^b) / (c*x^d) = (a/c) * x^(b-d)
    new_coeff = z256.div(coefficient1, coefficient2)
    new_pow = power1 - power2

    # Represent our answer as a Polynomial
    divided = Polynomial()
    divided = divided.add_term(new_coeff, new_pow)
    return divided

class Polynomial:
    """
    A class used to abstract methods on a polynomial in the finite
    field Z_256 (including numbers from 0 through 255).

    Since 256 is not prime, but is rather of the form p^n = 2^8, this
    representation uses special arithmetic via the z256 module so as to
    preserve multiplicative inverses (division) inside this field.
    """

    def __init__(self, terms=None):
        """
        Creates a new Polynomial object.  If a dictionary of terms, mapping
        powers to coefficients, is provided, they will be the terms of
        the polynomial, otherwise the polynomial will be the 0
        polynomial.
        """
        if terms != None:
            self._terms = dict(terms)
        else:
            self._terms = {}

    def __str__(self):
        """
        Returns a string representation of the polynomial, containing the
        class name and all of the terms.
        """
        # Create a string of the form "ax^n + bx^n-1 + ... + c" by
        # creating a string representation of each term, and inserting
        # " + " in between each
        term_strings = []

        # Add the highest powers first
        powers = list(self._terms.keys())
        powers.sort(reverse=True)
        for power in powers:
            coefficient = self._terms[power]
            # Don't print out terms with a zero coefficient
            if coefficient != 0:
                # Don't print "x^0"; that just means it's a constant
                if power == 0:
                    term_strings.append("%d" % coefficient)
                else:
                    term_strings.append("%d*x^%d" % (coefficient, power))

        terms_str = " + ".join(term_strings)
        if terms_str == "":
            terms_str = "0"
        return "Polynomial: %s" % terms_str

    def __eq__(self, other_polynomial):
        """
        Return True if other_polynomial contains the same terms
        as self, False otherwise.
        """
        # Make sure that other_polynomial is a Polynomial
        if not isinstance(other_polynomial, Polynomial):
            return False

        # Get the terms of the other_polynomial
        terms = other_polynomial.get_terms()

        # Check that all terms in other_polynomial appear in self
        for power, coefficient in terms.items():
            if coefficient != 0:
                if not self._terms.has_key(power):
                    return False
                if self._terms[power] != coefficient:
                    return False

        # Check that all terms in self appear in other_polynomial
        for power, coefficient in self._terms.items():
            if coefficient != 0:
                if not terms.has_key(power):
                    return False
                if terms[power] != coefficient:
                    return False
        return True

    def __ne__(self, other_polynomial):
        """
        Return False if other_polynomial contains the same terms
        as self, True otherwise.
        """
        return not self.__eq__(other_polynomial)

    def get_terms(self):
        """
        Returns a dictionary of terms, mapping powers to coefficients.
        This dictionary is a completely new object and is not a reference
        to any internal structures.
        """
        terms = dict(self._terms)
        return terms

    def get_degree(self):
        """
        Returns the maximum power over all terms in this polynomial.
        """
        # Since we don't clean zero-coefficient powers out of our dictionary,
        # we need a trickier get_degree function, to take into account that
        # some coefficients could be zero.
        highest_power = 0
        for power in self._terms:
            if (power > highest_power) and (self._terms[power] != 0):
                highest_power = power

        return highest_power

    def get_coefficient(self, power):
        """
        Given a power of x, returns the coefficient of x^(power) in this
        polynomial. If there is no coefficient of x^(power), this method
        returns 0.
        """
        if power in self._terms:
            return self._terms[power]
        else:
            return 0

    def add_term(self, coefficient, power):
        """
        Returns a new Polynomial that is the sum of adding this polynomial
        to (coefficient) * x^(power) using Z_256 arithmetic to add
        coefficients, if necessary.
        """
        new_polynomial=Polynomial(self.get_terms())
        terms=new_polynomial.get_terms()
#		The following statements are used to add the coefficient of the 
#		monomial and that of coresponding term in the polynomial
        if power in terms.keys():
            terms[power]=z256.add(terms[power],coefficient)          
        else:
            terms[power]=0
            terms[power]=z256.add(0,coefficient)    
        return Polynomial(terms)

    def subtract_term(self, coefficient, power):
        """
        Returns a new Polynomial that is the difference of this polynomial
        and (coefficient) * x^(power) using Z_256 arithmetic to subtract
        coefficients, if necessary.
        """
        new_polynomial=Polynomial(self.get_terms())
        terms=new_polynomial.get_terms()
#		The following statements are used to subtract the coefficient of the 
#		monomial from that of coresponding term in the polynomial        
        if power in terms.keys():
            terms[power]=z256.sub(terms[power],coefficient)
        else:
            terms[power]=0
            terms[power]=z256.sub(0,coefficient)    
        return Polynomial(terms)
       
    def multiply_by_term(self, coefficient, power):
        """
        Returns a new Polynomial that is the product of multiplying
        this polynomial by (coefficient) * x^(power).
        """
        new_polynomial=Polynomial(self.get_terms())
        terms=new_polynomial.get_terms()
        item=terms.items()
#       The following statements is used to multiply the coefficient of the monomial
#		with the coefficients of each term in the polynomial.
#		The following statement is also used to add the power of monomial and that of each term
#		in the monomial 
        for index in range(0,len(item)):
            item[index]=list(item[index])
            item[index][0]=item[index][0]+power
            item[index][1]=z256.mul(item[index][1],coefficient)
        new_term=dict(item)   
        return Polynomial(new_term)

    def add_polynomial(self, other_polynomial):
        """
        Returns a new Polynomial that is the sum of all terms in the
        current polynomial and all terms in the other_polynomial.
        """
# 		The following statement is used to get the key and coresponding value of
#		other_polynomial, which represents the power and coresponding coefficient.
        self_polynomial=Polynomial(self.get_terms())
        other_terms=other_polynomial.get_terms()
        other_terms=other_terms.items()
        reference=self_polynomial
# 		The following statement is used to add other_polynomial as several monomials with
#		the polynomial itself
        for index in range(0,len(other_terms)):
            coefficient=other_terms[index][1]
            degree=other_terms[index][0]
            reference=reference.add_term(coefficient,degree)
        return Polynomial(reference.get_terms())    
         
    def subtract_polynomial(self, other_polynomial):
        """
        Returns a new Polynomial that is the difference of all terms
        in the current polynomial and all terms in the other_polynomial.
        """
# 		The following statement is used to subtract other_polynomial as several monomials 
#		from the polynomial itself
        self_polynomial=Polynomial(self.get_terms())
        other_terms=other_polynomial.get_terms()
        other_terms=other_terms.items()
        reference=self_polynomial
# 		The following statement is used to subtract other_polynomial as several monomials 
#		from the polynomial itself        
        for index in range(0,len(other_terms)):
            coefficient=other_terms[index][1]
            degree=other_terms[index][0]
            reference=reference.subtract_term(coefficient,degree)
        return Polynomial(reference.get_terms())    
 

    def multiply_by_polynomial(self, other_polynomial):
        """
        Returns a new Polynomial that is the product of this
        polynomial and the provided other_polynomial.

        The returned polynomial is the sum of multiplying each term
        in this polynomial (self) by the other_polynomial.
        """
# 		The following statement is used to get the key and coresponding value of other_polynomial 
#		and the polynomial itself, which represents the power and coresponding coefficient.
        self_polynomial=Polynomial(self.get_terms())
        other_terms=other_polynomial.get_terms()
        other_terms=other_terms.items()
        self_terms=self_polynomial.get_terms()
        self_terms=self_terms.items()
        temp_product=[]
        result=Polynomial()
        reference=self_polynomial
#       If the polynomial itself or the other_polynomial is zero, return zero
        if self_terms==[] or other_terms==[]:
            return result
# 		The following statement is used to get the key and coresponding value of other_polynomial 
#		other_polynomial, which represents the power and coresponding coefficient. 
#		Then for each term in the other_polynomial, multiply them with the polynomial itself
#		Everytime put the product, which is a new polynomialm, into temp_product.
        else:
            for index in range(0,len(other_terms)):
                coefficient=other_terms[index][1]
                degree=other_terms[index][0]
                reference=self_polynomial.multiply_by_term(coefficient,degree)
                reference_terms=reference.get_terms()
                temp_product.append(reference_terms)
# 		The following statement is used to add all the product together to return the final
# 		result, which is a new polynomial
        for index2 in range (0, len(temp_product)):
            single_temp=Polynomial(temp_product[index2])
            result=result.add_polynomial(single_temp)           
        return Polynomial(result.get_terms())    

    def remainder(self, denominator):
        """
        Returns a new Polynomial that is the remainder after dividing this
        polynomial by denominator.

        Note: does *not* return the quotient; only the remainder!
        """
#       The following statement is used to get the highest degree of the 
#		numerator
        self_term=Polynomial(self.get_terms())
        check_degree=self_term.get_degree()
# 		The following statement is used to check a special case: Both denominator
# 		and numerator are a number
        if check_degree==0 and denominator.get_degree()==0:
            return Polynomial({0:0})
# 		The following statement is used to calculate the remainder after all
# 		divisions
        while check_degree>=denominator.get_degree() and check_degree!=0:
            max_degree=self_term.get_degree()
            max_coefficient=self_term.get_coefficient(max_degree)
            max_degree2=denominator.get_degree()
            max_coefficient2=denominator.get_coefficient(max_degree2)
            quotient=divide_terms(max_coefficient,max_degree,max_coefficient2,max_degree2)
            product=quotient.multiply_by_polynomial(denominator)
            self_term=self_term.subtract_polynomial(product)
            check_degree=self_term.get_degree()
        return self_term    

def create_message_polynomial(message, num_correction_bytes):
    """
    Description: Creates the appropriate Polynomial to represent the
        given message. Relies on the number of error correction
        bytes (k). The message polynomial is of the form
        message[i]*x^(n+k-i-1) for each number/byte in the message.

    Inputs:
    message -- a list of numbers between 0-255 representing data
    num_correction_bytes -- number of error correction bytes to use

    Returns:
    A Polynomial with the appropriate terms to represent message for
    the specified level of error correction.
    """
#   The following statement is used to create a polynomial that represents 
#   the message by using the given formula under given num_correction_bytes
    creater={}
    for index in range (0, len(message)):
        degree=message[index]
        coefficient=num_correction_bytes+len(message)-index-1
        creater[coefficient]=degree
    return Polynomial(creater)

def create_generator_polynomial(num_correction_bytes):
    """
    Description: Generates a static generator Polynomial for error
        correction, which is the product of (x-2^i) for all i in the
        set {0, 1, ..., num_correction_bytes - 1}.

    Inputs:
    num_correction_bytes -- desired number of error correction bytes.
        In the formula, this is represented as k.

    Returns:
    A generator Polynomial for generating Reed-Solomon encoding data.
    """
# The following function is used to return a generator polynomial for
# Reed-Solomon encoding data by using the given formula
    generator={}
    result=Polynomial({0:1}) 
    for index in range (0, num_correction_bytes):
        power=z256.power(2,index)
        generator=Polynomial({1:1,0:power})
        result=result.multiply_by_polynomial(generator)
    return result

def reed_solomon_correction(encoded_data, num_correction_bytes):
    """
    Takes a list of bytes (as numbers between 0-255) representing an
    encoded QR message.

    Returns a polynomial that represents the Reed-Solomon error
    correction code for the input data.
    """
# 	The following statement is used to create the message based on the
# 	given formula
    message={}
    for index in range (0, len(encoded_data)):
        degree=num_correction_bytes+len(encoded_data)-index-1
        message[degree]=encoded_data[index]
    message=Polynomial(message) 
# 	The following statement is used to create the generator under the given
# 	number_correction_bytes
    generator=create_generator_polynomial(num_correction_bytes)
    remainder=message.remainder(generator)
    return remainder

# Uncomment the following line when you are ready to generate an
# actual QR code.  To do so, you must enter a short message in the
# "info" text box and hit return (be sure to hit return!).  You then
# must push the "Generate!" button.  This will generate a QR code for
# you to view - try scanning it with your phone!  If you would like to
# save your QR codes, you can use the "Image in a New Window" button
# to create a .png file that you can save by right clicking in your
# browser window.

# qrcode.start(reed_solomon_correction)
