
def runtime_profile(f, **kwargs):
    import yappi
    import time

    yappi.set_clock_type('cpu')
    yappi.start(builtins=True)

    start = time.time()
    
    f(**kwargs) 

    duration = time.time() - start
    print(f'duration is {duration}')

    stats = yappi.get_func_stats()
    stats.save('callgrind.out', type='callgrind')


def dynamic_profile(state):
    import numpy
    xs = state[:3]
    vs = state[3:]

