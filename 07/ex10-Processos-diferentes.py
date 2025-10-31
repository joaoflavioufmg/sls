# -*- coding: utf-8 -*-
#!/usr/bin/python3

import sys
print(sys.version)

import simpy

def clock(env, name, tick):
    while True:
        print(name, env.now)
        yield env.timeout(tick)


env = simpy.Environment()

env.process(clock(env, 'rapido', 0.5))

env.process(clock(env, 'devagar', 1))

env.run(until = 3.1)
