
from fpcore.ast import FPCore
from interval import Interval
import lambdas

import numeric_types
import lego_blocks.forms as forms
from lambdas import types
import math


class PuntToLibm(types.Source):

    def __init__(self, function: FPCore, domain: Interval):
        """
        Use the system libm to implement the function.
        This can be used for debugging purposes (like testing range reductions)
          or to use libm with your own range reductions.

        function: FPCore representing the function
        domain: Interval domain, must be finite
        """
        super().__init__(function, domain)

    def type_check(self):
        """ Type check always passes """
        self.out_type = types.Impl(self.function, self.domain)

    def generate(self):
        """ Use libm in generated C """
        in_name = self.gensym("in")
        out_name = self.gensym("out")
        return [forms.PuntToLibm(numeric_types.fp64(), [in_name], [out_name], self.function)]

    @classmethod
    def generate_hole(cls, out_type):
        # We only output
        # (Impl (func) low high)
        # where both low and high are finite (done so this only triggers inside
        #   range reductions)
        if (type(out_type) != types.Impl
            or not math.isfinite(float(out_type.domain.inf))
                or not math.isfinite(float(out_type.domain.sup))):
            return list()

        # To get this output we just need be constructed with given args
        return [PuntToLibm(out_type.function, out_type.domain), ]
