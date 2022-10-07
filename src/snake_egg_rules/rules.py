
from snake_egg_rules.operations import *

from snake_egg import Rewrite, vars

x, y, z, a, b, c, d = vars("x y z a b c d")

raw_rules = [
  ["0",            sub(a, sub(b, c)),                              sub(c, sub(b, a))],
  ["1",            mul(a, mul(b, c)),                              mul(b, mul(a, c))],
  ["2",            sub(sub(a, b), c),                              sub(sub(a, c), b)],
  ["3",            add(a, add(b, c)),                              add(c, add(a, b))],
  ["4",            add(c, add(a, b)),                              add(a, add(b, c))],
  ["5",            sub(add(a, b), c),                              add(a, sub(b, c))],
  ["6",            add(a, sub(b, c)),                              sub(add(a, b), c)],
  ["7",            sub(a, sub(b, c)),                              add(a, sub(c, b))],
  ["8",            add(a, sub(c, b)),                              sub(a, sub(b, c))],
  ["9",            div(a, mul(b, c)),                              div(div(a, b), c)], # (-> (!= 0 (* b c)) (and (!= 0 b) (!= 0 c)))
  ["10",           div(div(a, b), c),                              div(a, mul(b, c))], # (-> (and (!= 0 b) (!= 0 c)) (!= 0 (* b c)))
  ["11",           sub(a, add(b, c)),                              sub(sub(a, b), c)],
  ["12",           sub(sub(a, b), c),                              sub(a, add(b, c))],
  ["13",           div(sub(a, b), c),                              sub(div(a, c), div(b, c))], # (-> (!= 0 c) (!= 0 c))
  ["14",           sub(div(a, c), div(b, c)),                      div(sub(a, b), c)], # (-> (!= 0 c) (!= 0 c))
  ["15",           sub(mul(a, b), mul(a, c)),                      mul(a, sub(b, c))],
  ["16",           mul(a, sub(b, c)),                              sub(mul(a, b), mul(a, c))],
  ["17",           div(add(a, b), c),                              add(div(b, c), div(a, c))], # (-> (!= 0 c) (!= 0 c))
  ["18",           add(div(b, c), div(a, c)),                      div(add(a, b), c)], # (-> (!= 0 c) (!= 0 c))
  ["19",           add(mul(a, b), mul(b, c)),                      mul(b, add(a, c))],
  ["20",           mul(b, add(a, c)),                              add(mul(a, b), mul(b, c))],
  ["21",           div(sub(mul(a, b), c), b),                      sub(a, div(c, b))], # (-> (!= 0 b) (!= 0 b))
  ["22",           sub(a, div(c, b)),                              div(sub(mul(a, b), c), b)], # (-> (!= 0 b) (!= 0 b))
  #unknown ["23",  div(a, sub(div(b, c), a)),                      div(c, sub(div(b, a), c))], # (-> (and (!= 0 c) (!= 0 (- (/ b c) a))) (and (!= 0 a) (!= 0 (- (/ b a) c)))))
  ["24",           mul(a, b),                                      mul(b, a)],
  ["25",           add(a, b),                                      add(b, a)],
  ["26",           mul(a, add(b, b)),                              mul(b, add(a, a))],
  ["27",           div(a, b),                                      div(add(a, a), add(b, b))], # (-> (!= 0 b) (!= 0 (+ b b)))
  ["28",           div(add(a, a), add(b, b)),                      div(a, b)], # (-> (!= 0 (+ b b)) (!= 0 b))
  ["29",           sub(mul(a, a), mul(b, b)),                      mul(sub(a, b), add(a, b))],
  ["30",           mul(sub(a, b), add(a, b)),                      sub(mul(a, a), mul(b, b))],
  ["31",           sub(mul(sin(a), sin(a)), mul(cos(b), cos(b))),  sub(mul(sin(b), sin(b)), mul(cos(a), cos(a)))],
  ["32",           sub(mul(sin(a), sin(a)), mul(sin(b), sin(b))),  sub(mul(cos(b), cos(b)), mul(cos(a), cos(a)))],
  ["33",           sub(mul(cos(b), cos(b)), mul(cos(a), cos(a))),  sub(mul(sin(a), sin(a)), mul(sin(b), sin(b)))],
  ["34",           a,                                              neg(neg(a))],
  ["35",           neg(neg(a)),                                    a],
  ["36",           cos(a),                                         cos(neg(a))],
  ["37",           cos(neg(a)),                                    cos(a)],
  ["38",           neg(tan(a)),                                    tan(neg(a))],
  ["39",           tan(neg(a)),                                    neg(tan(a))],
  ["40",           neg(sin(a)),                                    sin(neg(a))],
  ["41",           sin(neg(a)),                                    neg(sin(a))],
  ["42",           tan(a),                                         tan(sub(a, CONST_PI()))],
  ["43",           tan(sub(a, CONST_PI())),                        tan(a)],
  ["44",           sin(a), sin(sub(CONST_PI(),                     a))],
  ["45",           sin(sub(CONST_PI(), a)),                        sin(a)],
  ["46",           neg(cos(a)),                                    cos(add(a, CONST_PI()))],
  ["47",           cos(add(a, CONST_PI())),                        neg(cos(a))],
  ["48",           add(cos(add(a, a)), mul(sin(a), sin(a))),       mul(cos(a), cos(a))],
  ["49",           mul(cos(a), cos(a)),                            add(cos(add(a, a)), mul(sin(a), sin(a)))],
  ["50",           a,                                              mul(a, 1)],
  ["51",           mul(a, 1),                                      a],
  ["52",           a,                                              add(a, 0)],
  ["53",           add(a, 0),                                      a],
  ["54",           a,                                              div(a, 1)],
  ["55",           div(a, 1),                                      a],
  ["56",           a,                                              sub(a, 0)],
  ["57",           sub(a, 0),                                      a],
  ["58",           sub(a, a),                                      0],
  ["60",           neg(a),                                         div(a, -1)],
  ["61",           div(a, -1),                                     neg(a)],
  ["62",           neg(a),                                         mul(a, -1)],
  ["63",           mul(a, -1),                                     neg(a)],
  ["64",           neg(a),                                         sub(0, a)],
  ["65",           sub(0, a),                                      neg(a)],
  ["66",           add(a, a),                                      mul(2, a)],
  ["67",           mul(2, a),                                      add(a, a)],
  ["68",           add(mul(sin(a), sin(a)), mul(cos(a), cos(a))),  1],
  ["70",           mul(a, 0),                                      0],
  ["71",           sub(a, -1),                                     add(a, 1)],
  ["72",           add(a, 1),                                      sub(a, -1)],
  ["73",           sub(a, 1),                                      add(a, -1)],
  ["74",           add(a, -1),                                     sub(a, 1)],
  ["75",           add(-1/2, div(cos(add(a, a)), 2)),              mul(sin(neg(a)), sin(a))],
  ["76",           mul(sin(neg(a)), sin(a)),                       add(-1/2, div(cos(add(a, a)), 2))],
  ["77",           0,                                              tan(CONST_PI())],
  ["78",           tan(CONST_PI()),                                0],
  ["79",           -1,                                             cos(CONST_PI())],
  ["80",           cos(CONST_PI()),                                -1],
  ["81",           0,                                              sin(CONST_PI())],
  ["82",           sin(CONST_PI()),                                0],
  ["83",           0,                                              tan(add(CONST_PI(), CONST_PI()))],
  ["84",           tan(add(CONST_PI(), CONST_PI())),               0],
  ["85",           0,                                              sin(add(CONST_PI(), CONST_PI()))],
  ["86",           sin(add(CONST_PI(), CONST_PI())),               0],
  ["87",           1,                                              cos(add(CONST_PI(), CONST_PI()))],
  ["88",           cos(add(CONST_PI(), CONST_PI())),               1],
  ["89",           0,                                              tan(0)],
  ["90",           tan(0),                                         0],
  ["91",           0,                                              sin(0)],
  ["92",           sin(0),                                         0],
  ["93",           1,                                              cos(0)],
  ["94",           cos(0),                                         1],
  ["95",           1,                                              tan(div(CONST_PI(), 4))],
  ["96",           tan(div(CONST_PI(), 4)),                        1],
  ["97",           1,                                              sin(div(CONST_PI(), 2))],
  ["98",           sin(div(CONST_PI(), 2)),                        1],
  ["99",           sin(div(CONST_PI(), 4)),                        cos(div(CONST_PI(), 4))],
  ["100",          cos(div(CONST_PI(), 4)),                        sin(div(CONST_PI(), 4))],
]

rules = list()
for l in raw_rules:
    name = l[0]
    frm = l[1]
    to = l[2]
    rules.append(Rewrite(frm, to, name))
