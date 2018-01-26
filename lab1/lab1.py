import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from tools.logger import logging_time, logging_dict

def LCG():
    '''LCG Random Number generator'''
    # seed, a, c, m are all prime numbers, to avoid periodicity
    state = 4211 # This is the seed

    a = 1559
    c = 313
    m = 13229
    while True:
        if state / m < 0.5:
            yield -1
        else:
            yield 1
        state = (a*state+c) % m

def npRNG():
    '''Numpy Random Number Generator'''
    while True:
        if np.random.random() < 0.5:
            yield -1
        else:
            yield 1
#instantiate the generators LCG and npRNG
LCG = LCG()
npRNG = npRNG()


def RandomWalk(steps, RNG): 
    walks = list(next(RNG) for i in range(steps*3))
    walks = np.array(walks).reshape(-1,3)
    pos = np.array(walks).cumsum(axis=0) # cumulative sum of walks in every step
    return pos

def pos_to_sampled_MSD(N, steps, sample_indices, RNG):
    for i in range(N):
        pos = RandomWalk(steps, RNG)[sample_indices,:]
        MSD = np.sum(pos**2, axis=1)
        yield MSD

def samppling(N, walk_steps, sample_steps, RNG):

    sample_size = walk_steps // sample_steps
    sample_indices = np.arange(sample_size) * sample_steps

    print('taking the mean date of {} particles, each walking {} steps, sampling every {} steps'.format(N, walk_steps, sample_steps))
    
    MSD_mean = np.sum(pos_to_sampled_MSD(N, walk_steps, sample_indices, RNG)) / N

    return sample_indices, MSD_mean

@logging_time #recording the runtime of this function and recording it in results.log
def linearity_test(RNG, ax, name=None):
    '''1.Generate a 500 particle system, each walking 5000 steps, sampled every 10 steps
       2.Finding the MSD of this system
       3.Linear fit the function (N,MSD) using scipy.optimize.curve_fit
       4.Plotting the fitting line and the data'''
 
    print('Linear fitting of random walk')
    print('RNG: {}'.format(name))
    xs, ys = samppling(500, 5000, 10, RNG)

    def f(x, slope):
        '''Assuming MSD is proportional to N'''
        return slope*x

    # curve_fit: argument:(fitting function, xdata, ydata) return: (best fit parameters, standard deviation)
    parameters, std = curve_fit(f, xs, ys)
    yfit = f(xs, *parameters) # the MSD of the fitted line
 
    print('standard error: {}'.format(*std))
    print('slope: {}'.format(*parameters))
    print('expected slope: 3\n')
 
    logging_dict(locals()) #recording the results of this test 

    ax.set(title= name, xlabel='steps', ylabel='distance squared')
    ax.plot(xs, ys)
    ax.plot(xs, yfit, color='red', alpha=0.7, label='linear fitting')

# plotting the linear fitting of N walks
def plot_linear():
    '''Plotting the two test together'''
    fig, axes = plt.subplots(nrows=1,ncols=2, sharey=True, figsize=(12, 4))
    linearity_test(LCG, axes[0], 'LCG')
    linearity_test(npRNG, axes[1], 'numpy RNG')
    plt.show(fig)
    print('The seed is predetermined for function LCG, so the slope of LCG is the same everytime, but npRNG changes everytime you run.\
            the slope it generally approaches 3, but sometimes go beyond 3')

# writting the XYZ file
def write_to_XYZ():
    steps = 5000
    LCG_walk = RandomWalk(steps, LCG)
    npRNG_walk = RandomWalk(steps, npRNG)
    from tools.XYZ_format import write_XYZ
    write_XYZ('LCG.xyz', 'a random walk of 5000 steps using LCG random number generator', LCG_walk)
    write_XYZ('npRNG.xyz', 'a random walk of 5000 steps using numpy random number generator', npRNG_walk)

### Uncomment to plot
if __name__ == "__main__":
    #plot_linear()
    write_to_XYZ()

