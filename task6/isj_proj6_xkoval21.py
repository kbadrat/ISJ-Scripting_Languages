#!/usr/bin/env python3

class Polynomial:
    """ A class to represent a polynomial and perform operations with it."""

    def __init__(self, *args, **kwargs):
        """Initialize the polynomial object."""

        self.polynom = {0: 0}

        if args:
            if isinstance(args[0], list):
                unified = args[0]
            else:
                unified = list(args)
            self.polynom = {i: v for i, v in enumerate(unified) if v != 0}
        elif kwargs:
            self.polynom = {int(k[1:]): v for k, v in kwargs.items() if v != 0}


    def __str__(self):
        """Return a string representation of the polynomial."""

        result_str = " ".join([
            f"{'+' if v > 0 else '-'} {abs(v) if abs(v) > 1 or k == 0 else ''}" +
            (f"x^{k}" if k > 1 else 'x' if k == 1 else '') 
            for k, v in sorted(self.polynom.items(), reverse=True)
            ]).strip(' +-') or '0'

        return result_str


    def __eq__(self, other):
        """Check if polynomials are equal."""

        if isinstance(other, self.__class__):
            return self.polynom == other.polynom
        return False


    def __add__(self, other):
        """Add two polynomials."""

        result_polynom = {}
        for key in set(self.polynom.keys()) | set(other.polynom.keys()):
            value = self.polynom.get(key, 0) + other.polynom.get(key, 0)
            if value != 0:
                result_polynom[f"x{key}"] = value
        
        return Polynomial(**result_polynom)


    def __pow__(self, power): 
        """Calculate the power of a polynomial. It takes an exponent as input and returns the resulting polynomial."""

        if power == 0:
            return Polynomial(x0=1)

        result = self
        for _ in range(1, power):
            new_polynom = {}
            for key1, val1 in self.polynom.items():
                for key2, val2 in result.polynom.items():
                    new_key = key1 + key2
                    new_val = val1 * val2
                    if new_key in new_polynom:
                        new_polynom[new_key] += new_val
                    else:
                        new_polynom[new_key] = new_val
            result = Polynomial(**{f"x{k}": v for k, v in new_polynom.items()})
        return result


    def derivative(self):
        """Compute the derivative of the polynomial."""

        return Polynomial(**{f"x{k-1}": v * k for k, v in self.polynom.items() if k > 0} if self.polynom else {"x0": 0})


    def at_value(self, x1, x2=None):
        """Evaluate the polynomial at a specific value or find the difference between the values of the polynomial
        at two different points."""

        if x2:
            return self.at_value(x2) - self.at_value(x1)

        return sum([v * x1 ** k for k, v in self.polynom.items()])

    
def test():
    assert str(Polynomial(0,1,0,-1,4,-2,0,1,3,0)) == "3x^8 + x^7 - 2x^5 + 4x^4 - x^3 + x"
    assert str(Polynomial([-5,1,0,-1,4,-2,0,1,3,0])) == "3x^8 + x^7 - 2x^5 + 4x^4 - x^3 + x - 5"
    assert str(Polynomial(x7=1, x4=4, x8=3, x9=0, x0=0, x5=-2, x3= -1, x1=1)) == "3x^8 + x^7 - 2x^5 + 4x^4 - x^3 + x"
    assert str(Polynomial(x2=0)) == "0"
    assert str(Polynomial(x0=0)) == "0"
    assert Polynomial(x0=2, x1=0, x3=0, x2=3) == Polynomial(2,0,3)
    assert Polynomial(x2=0) == Polynomial(x0=0)
    assert str(Polynomial(x0=1)+Polynomial(x1=1)) == "x + 1"
    assert str(Polynomial([-1,1,1,0])+Polynomial(1,-1,1)) == "2x^2"
    pol1 = Polynomial(x2=3, x0=1)
    pol2 = Polynomial(x1=1, x3=0)
    assert str(pol1+pol2) == "3x^2 + x + 1"
    assert str(pol1+pol2) == "3x^2 + x + 1"
    assert str(Polynomial(x0=-1,x1=1)**1) == "x - 1"
    assert str(Polynomial(x0=-1,x1=1)**2) == "x^2 - 2x + 1"
    pol3 = Polynomial(x0=-1,x1=1)
    assert str(pol3**4) == "x^4 - 4x^3 + 6x^2 - 4x + 1"
    assert str(pol3**4) == "x^4 - 4x^3 + 6x^2 - 4x + 1"
    assert str(Polynomial(x0=2).derivative()) == "0"
    assert str(Polynomial(x3=2,x1=3,x0=2).derivative()) == "6x^2 + 3"
    assert str(Polynomial(x3=2,x1=3,x0=2).derivative().derivative()) == "12x"
    pol4 = Polynomial(x3=2,x1=3,x0=2)
    assert str(pol4.derivative()) == "6x^2 + 3"
    assert str(pol4.derivative()) == "6x^2 + 3"
    assert Polynomial(-2,3,4,-5).at_value(0) == -2
    assert Polynomial(x2=3, x0=-1, x1=-2).at_value(3) == 20
    assert Polynomial(x2=3, x0=-1, x1=-2).at_value(3,5) == 44
    pol5 = Polynomial([1,0,-2])
    assert pol5.at_value(-2.4) == -10.52
    assert pol5.at_value(-2.4) == -10.52
    assert pol5.at_value(-1,3.6) == -23.92
    assert pol5.at_value(-1,3.6) == -23.92

if __name__ == '__main__':
    test()
