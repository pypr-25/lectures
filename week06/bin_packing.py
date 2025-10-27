import numpy as np
import matplotlib.pyplot as plt

# Setting the font size for all plots
# https://matplotlib.org/stable/users/explain/customizing.html#runtime-rc-settings
import matplotlib as mpl
mpl.rcParams['font.size'] = 18

def first_fit(item_list, bin_size, method='decreasing'):
    '''
    First-fit algorithm for the bin packing problem.
    Input:
        item_list (list): list of items to pack
        bin_size (float): capacity of each bin
        method (str): sorting (or not) of items before
            binning. Can be 'increasing', 'decreasing', or 'none'.
    
    Output:
        bins (list): a list of bins with what's inside of each bin at the end.
    '''
    # Start a list of bins
    bins = [0]

    # Sort items by decreasing size
    if method == 'decreasing':
        sorted_items = sorted(item_list, reverse=True)
    elif method == 'increasing':
        sorted_items = sorted(item_list)
    elif method == 'none':
        sorted_items = item_list.copy()
    else:
        raise ValueError(f'method is {method}, should be "increasing", "decreasing", or "none".')

    # Loop over the items
    for item in sorted_items:
        placed = False

        # Loop over the open bins
        for b in range(len(bins)):

            # Does the item fit?
            if item + bins[b] <= bin_size:
                # Yes, place the item
                bins[b] += item
                placed = True
                break
        
        # If item has not been placed,
        # start a new bin and place it there
        if not placed:
        # if placed == False:
        # if (not placed) == True:
            bins.append(item)

    return bins


def test_first_fit(item_list, bin_size, bins_expected):
    '''
    Convenience function to test that first_fit() is correct
    in just one line.
    '''
    # Call our function to get the result
    bins_result = first_fit(item_list, bin_size)
    
    msg = f'Incorrect result: expected {bins_expected}, got {bins_result} instead.'
    assert bins_result == bins_expected, msg
    print('Test passed.')


def generate_test_data(number_of_sets=1000, number_of_items=50, max_item_size=10):
    '''
    Convenience function to generate some test data
    for evaluating our different first_fit methods.
    '''
    # Generate all the item sets in a Numpy array
    item_sets = max_item_size * np.random.rand(number_of_sets, number_of_items)

    # Bin size is always the same; set it to max_item_size
    bin_sizes = max_item_size * np.ones(number_of_sets)
    
    return item_sets, bin_sizes


# Note: you could also break this down further, e.g. have this function return
# the efficiency array, then have another function to calculate some summary statistics,
# and another function to just plot the results...
def compare_efficiency(item_sets, bin_sizes, metric='number_of_bins'):
    '''
    Compare packing efficiency of our 3 different methods, using
    the provided item sets and bin sizes.

    Choose metric between number of bins and % empty space.
    '''
    # Exercise: add robustness checks here to make sure
    # that we have as many bin_sizes as we have item sets.
    
    # Set up empty arrays to store our results
    number_of_sets = item_sets.shape[0]
    efficiency = np.zeros((number_of_sets, 3))
    percentage_empty_space = np.zeros((number_of_sets, 3))

    # Set up to loop over methods
    methods = ['decreasing', 'increasing', 'none']
    fig, ax = plt.subplots(figsize=(12, 8))

    # Use enumerate() to get the method name and the index together
    for j, m in enumerate(methods):

        for i in range(number_of_sets):
            # Pack current item set with current method
            bins = first_fit(item_sets[i, :], bin_sizes[i], method=m)
            if any([b > bin_sizes[i] for b in bins]):
                print(bins, bin_sizes[i], m)

            if metric == 'number_of_bins':
                # Count number of bins used
                efficiency[i, j] = len(bins)

            elif metric == 'empty_space':
                # Calculate the % of empty space across all bins
                # (this is more useful if the bin size is randomised, as it's normalised)
                total_bin_space = bin_sizes[i] * len(bins)
                efficiency[i, j] = 100 * (total_bin_space - sum(bins)) / total_bin_space
            
            else:
                raise ValueError(f'metric should be "number_of_bins" or "empty_space", not {metric}.')
        

        # Visualise results for the current method
        ax.hist(efficiency[:, j], alpha=0.5, label=m)

    ax.set(xlabel=metric, ylabel='Frequency', title='Comparing different sorting methods for first fit')
    ax.legend()

    plt.show()


if __name__ == "__main__":
    # Testing the function
    # test_first_fit([2, 1, 3, 2, 1, 2, 3, 1], 4, [4, 4, 4, 3])

    # Comparing efficiency of 3 methods.
    # Setting up the test data
    number_of_sets = 5000
    number_of_items = 50
    max_item_size = 10
    item_sets, bin_sizes = generate_test_data(number_of_sets, number_of_items, max_item_size)

    # Calculating and displaying efficiency
    compare_efficiency(item_sets, bin_sizes, metric='empty_space')