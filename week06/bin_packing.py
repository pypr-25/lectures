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




# ## Testing

# # List of item sizes
# item_list = [2, 1, 3, 2, 1, 2, 3, 1]

# # Size of bin
# bin_size = 4

# # Call our function to get the result
# bins_result = first_fit(item_list, bin_size)
# bins_expected = [4, 4, 4, 3]

# # "assert X, error_message" does nothing if X is True,
# # but raises an error if X is False, optionally with an error message (string)
# msg = f'Incorrect result: expected {bins_expected}, got {bins_result} instead.'
# assert bins_result == bins_expected, msg
# print('Test passed.')


## Which method is better: sorting up, down, or not?
# Count the number of bins used for the 3 different methods.

# Generate lots of items
number_of_sets = 5000
number_of_items = 50
# bin_sizes = 5 * np.random.rand(number_of_sets) + 5
bin_sizes = 10 * np.ones(number_of_sets)

item_sets = 10 * np.random.rand(number_of_sets, number_of_items)

number_of_bins = np.zeros((number_of_sets, 3))

# Improvements:

# Starting with this, improve the code below to avoid repetition.
# methods = ['decreasing', 'increasing', 'none']

# Structure this code into a set of functions.
# Example: get results for the 3 different methods; generate the test data;
# do the plotting... Main function at the end to call all your previous functions.

# Display the results using box plots.

# Display meaningful results using random bin sizes.


# Set up to loop over methods
methods = ['decreasing', 'increasing', 'none']
fig, ax = plt.subplots(figsize=(12, 8))

# Use enumerate() to get the method name and the index together
for j, m in enumerate(methods):

    for i in range(number_of_sets):
        # Pack current item set with current method
        bins = first_fit(item_sets[i, :], bin_sizes[i], method=m)

        # Count number of bins used
        number_of_bins[i, j] = len(bins)
    
    # Visualise results for the current method
    ax.hist(number_of_bins[:, j], alpha=0.5, label=m)

ax.set(xlabel='Number of bins', ylabel='Frequency', title='Comparing different sorting methods for first fit')
ax.legend()

plt.show()