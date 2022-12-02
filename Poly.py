from sys import stdin


class Poly:
    def __init__(self, *coefficients):
        if len(coefficients) == 1 and type(coefficients[0]) == list:
            coefficients = coefficients[0]
        elif len(coefficients) >= 1:
            coefficients = list(coefficients)
        elif len(coefficients) == 0:
            coefficients = [0]
        coeffs = []
        # print(coefficients)
        for r in coefficients:
            coeffs.append(float(r))
        self.coeffs = coeffs
        self.coeffsRep = coeffs

        for i in range(len(self.coeffs)):
            if self.coeffs[i] == int(self.coeffs[i]):
                self.coeffs[i] = int(self.coeffs[i])
        self.coeffsRep = list(self.coeffs)
        while self.coeffs[-1] == 0 and len(self.coeffs) > 1:
            self.coeffs.pop(-1)

    def __str__(self):
        string = ""
        self.coeffs.reverse()
        for n in range(len(self.coeffs)):
            aaa = self.coeffs[n]
            if type(aaa) == float:
                aaa = round(aaa, 3)
            n_coeff = str(aaa)
            if '-' in n_coeff:
                add_str = ' - '
                n_coeff = n_coeff.replace('-', '')
            else:
                add_str = " + "

            if n_coeff == '0' and self.coeffs != [0] * len(self.coeffs):
                continue
            if n_coeff == '1' and n != len(self.coeffs) - 1:
                n_coeff = ''
            if n == 0 and add_str == ' - ' and len(self.coeffs) > 1:
                add_str = '-'
                string = string + add_str + n_coeff + "x^" + \
                         str(len(self.coeffs) - n - 1)
            elif n == 0 and add_str == ' + ' and len(self.coeffs) == 1:
                string = string + n_coeff
            elif n == 0 and add_str == ' + ' and len(self.coeffs) > 1:
                string = string + n_coeff + "x^" + \
                         str(len(self.coeffs) - n - 1)
            elif n < len(self.coeffs) - 2:
                string = string + add_str + n_coeff + "x^" + \
                         str(len(self.coeffs) - n - 1)
            elif n < len(self.coeffs) - 1:
                string = string + add_str + n_coeff + "x"
            else:
                string = string + add_str + n_coeff
        if 'x^1 ' in string:
            string = string.replace('x^1 ', 'x ')
        elif 'x^1' == string[-3:]:
            string = string[::-1]
            string = string.replace('1^x', 'x', 1)
            string = string[::-1]

        if string[:3] == ' - ':
            string = string.replace(' - ', '-', 1)
        return string

    def __repr__(self):
        return f'\'Poly(({", ".join(map(str, self.coeffsRep))}))\''

    def coeff(self, i):
        if 0 <= i < len(self.coeffs):
            return self.coeffs[-1 - i]
        else:
            return 0.0

    def add(self, other):

        rev_poly = []

        if str(type(other)) != '<class \'__main__.Poly\'>':
            other = Poly(other)
        rev_self_coeffs = self.coeffs
        rev_other_coeffs = other.coeffs

        for n in range(len(rev_self_coeffs)):
            if n <= len(rev_other_coeffs) - 1:
                rev_poly.append(rev_self_coeffs[n] + rev_other_coeffs[n])
            else:
                rev_poly.append(rev_self_coeffs[n])

        if len(rev_other_coeffs) > len(rev_self_coeffs):
            for n in range(len(rev_self_coeffs), len(rev_other_coeffs)):
                rev_poly.append(rev_other_coeffs[-n])

        return Poly(rev_poly)

    def __add__(self, other):
        return self.add(other)

    def __radd__(self, other):
        x1 = self.coeffs
        x2 = Poly(other)

        return x2 + x1

    def __sub__(self, other):
        x1 = self.coeffs
        if str(type(other)) != '<class \'__main__.Poly\'>':
            other = Poly(other)
        x2 = Poly(list(map(lambda x: x * -1, other.coeffs)))
        if abs(x1[-1] * 2 ** len(x1)) > abs(x2.coeffs[-1] * 2 ** len(x2.coeffs)):
            pass
        else:
            x1, x2 = x2, x1
        return x1 + x2

    def __rsub__(self, other):
        x1 = self.coeffs
        x2 = other
        if str(type(other)) != '<class \'__main__.Poly\'>':
            x2 = Poly(other)
        return x2 - x1

    def __eq__(self, other):
        s1 = Poly(self.coeffs)
        if str(s1) == str(other):
            return True
        else:
            return False

    def mul(self, other):
        s1 = self.coeffs
        if str(type(other)) != '<class \'__main__.Poly\'>':
            other = Poly(other)
        s2 = other.coeffs
        res = [0] * (len(s1) + len(s2) - 1)
        for o1, i1 in enumerate(s1):
            for o2, i2 in enumerate(s2):
                res[o1 + o2] += i1 * i2
        res = Poly(res)
        return res

    def __mul__(self, other):
        return self.mul(other)

    def __rmul__(self, other):
        x1 = self.coeffs
        x2 = other
        if str(type(other)) != '<class \'__main__.Poly\'>':
            x2 = Poly(other)
        return x2 * x1

    def degree(self):
        return len(self.coeffs) - 1

    @staticmethod
    def intsroca(stroka):
        for i in range(len(stroka)):
            try:
                if stroka[i] == int(stroka[i]):
                    stroka[i] = int(stroka[i])
                else:
                    stroka[i] = float(stroka[i])
            except:
                stroka[i] = float(stroka[i])
        return stroka

    @staticmethod
    def poly_from_str(stroka):
        stroka = stroka.split()
        stroka = Poly.intsroca(stroka)
        polyStr = Poly(stroka)
        return polyStr


class DegreeIsTooBigException(Exception):
    def __init__(self, qpoly):
        self.qpoly = qpoly


class QuadraticPolynomial(Poly):

    def solve(self):
        if self.degree() > 2:
            raise DegreeIsTooBigException(QuadraticPolynomial(self.coeffs))
        if self.degree() == 0:
            return []
        if self.degree() < 2:
            while self.degree() < 2:
                self.coeffs = self.coeffs[::-1]
                self.coeffs.append(0)
                self.coeffs = self.coeffs[::-1]
        a, b, c = self.coeffs[::-1]

        d = (b ** 2) - (4 * a * c)
        if d < 0:
            return []
        import math
        sol1 = (-b - math.sqrt(d)) / (2 * a)
        sol2 = (-b + math.sqrt(d)) / (2 * a)
        spisok = sorted(set([sol1, sol2]))
        spisok = Poly.intsroca(spisok)

        return spisok


poly1 = QuadraticPolynomial(2, 3, 1)
try:
    print(poly1.solve())
except DegreeIsTooBigException as error:
    print(error.qpoly, 'я не умею решать уравнения больше 2 степени :с')

poly1 = QuadraticPolynomial(2, 1, 0, 0)
try:
    print(poly1.solve())
except DegreeIsTooBigException as error:
    print(error.qpoly, 'я не умею решать уравнения больше 2 степени :с')
