

import lego_blocks
import numeric_types
import fpcore

from interval import Interval
from lambdas import types
from utils import Logger

from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr

from math import pi


logger = Logger(level=Logger.HIGH)




def is_symmetric_function(func, low, middle, high):
    arg = func.arguments[0]
    flipped_arg = high - arg
    flipped = func.substitute(arg, flipped_arg)
    query = func - flipped
    logger("Query: {}", query)
    wolf_query = query.to_wolfram()
    logger("Wolf Query: {}", wolf_query)
    session = WolframLanguageSession()
    res = session.evaluate(wlexpr(wolf_query))
    logger("Wolf's Result: {}", res)
    return  res == 0


class RepeatFlip(types.Transform):

    def type_check(self):
        our_in_type = self.in_node.out_type
        old_high = our_in_type.domain.sup
        new_high = fpcore.Operation("*", fpcore.Number("2"), old_high)
        assert(type(our_in_type) == types.Impl)
        assert(float(our_in_type.domain.inf) == 0.0)
        assert(is_symmetric_function(our_in_type.function,
                                     0.0,
                                     old_high,
                                     new_high))

        self.out_type = types.Impl(our_in_type.function,
                                   Interval(0, new_high))


    def generate(self):
        our_in_type = self.in_node.out_type
        so_far = super().generate()
        in_name = self.gensym("in")
        out_red = self.gensym("out")
        k = self.gensym("k")
        add = lego_blocks.SimpleAdditive(numeric_types.fp64(), [in_name], [out_red, k], our_in_type.domain.sup)

        in_case = out_red
        out_case = so_far[0].in_names[0]
        cases = {
            0: in_case,
            1: "{}-{}".format(our_in_type.domain.sup, in_case),
        }
        case = lego_blocks.Case(numeric_types.fp64(), [in_case, k], [out_case], 2, cases)

        return [add, case] + so_far
