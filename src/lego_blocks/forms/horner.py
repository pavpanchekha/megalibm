

from lego_blocks import forms


class Horner(forms.Form):

    def __init__(self, numeric_type, in_names, out_names, polynomial):
        super().__init__(numeric_type, in_names, out_names)
        assert (type(polynomial) == forms.Polynomial)

        self.polynomial = polynomial

    def __repr__(self):
        return "Horner({}, {}, {}, {}, {}, {})".format(repr(self.numeric_type),
                                                       repr(self.in_names),
                                                       repr(self.out_names),
                                                       repr(self.polynomial))

    def to_c(self):
        c_type = self.numeric_type.c_type()
        out = self.out_names[0]
        cast_in = "(({}){})".format(c_type, self.in_names[0])

        parts = list()
        mons = self.polynomial.monomials
        cast_coeff = ["(({}){})".format(c_type, c) for c
                      in self.polynomial.coefficients]

        def expand_pow(n):
            return "*".join(cast_in for _ in range(n))

        if len(mons) == 1:
            if mons[0] == 0:
                parts.append("{}".format(cast_coeff[0]))
            else:
                parts.append(
                    "{}*{}".format(expand_pow(mons[0]), cast_coeff[0]))

        else:
            if mons[0] == 0:
                parts.append("{} \n        +".format(cast_coeff[0]))
            else:
                parts.append(
                    "{}*({} \n        + ".format(expand_pow(mons[0]), cast_coeff[0]))

            for i in range(1, len(mons) - 1):
                power = mons[i] - mons[i - 1]
                parts.append(
                    "{}*({} \n        + ".format(expand_pow(power), cast_coeff[i]))

            final_power = mons[-1] - mons[-2]
            parts.append(
                "{}*{}".format(expand_pow(final_power), cast_coeff[-1]))

            for i in range(1, len(mons) - 1):
                parts.append(")")

            if mons[0] != 0:
                parts.append(")")

        rhs = "({})".format("".join(parts))
        code = "{} {} = {};".format(c_type, out, rhs)

        return [code]
