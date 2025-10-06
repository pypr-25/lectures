def first_fit(item_list, bin_size):
    '''
    First-fit algorithm for the bin packing problem.
    Input:
        item_list (list): list of items to pack
        bin_size (float): capacity of each bin
    
    Output:
        bins (list): a list of bins with what's inside of each bin at the end.
    '''
    # Start a list of bins
    bins = [0]

    # Sort items by decreasing size
    sorted_items = sorted(item_list, reverse=True)

    # Loop over the items
    for item in item_list:
        # Loop over the open bins
        for b in range(len(bins)):

            # Does the item fit?
            if item + bins[b] <= bin_size:
                # Yes, place the item
                bins[b] += item
        
        # If item has not been placed,
        # start a new bin and place it there
        if ...:
            bins.append(item)

    return bins




## Testing

# List of item sizes
item_list = [2, 1, 3, 2, 1, 2, 3, 1]

# Size of bin
bin_size = 4

# Call our function to get the result
bins_result = first_fit(item_list, bin_size)
bins_expected = [4, 4, 4, 3]

# "assert X, error_message" does nothing if X is True,
# but raises an error if X is False, optionally with an error message (string)
msg = f'Incorrect result: expected {bins_expected}, got {bins_result} instead.'
assert bins_result == bins_expected, msg
print('Test passed.')