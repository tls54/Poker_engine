import numpy as np
from poker_engine.Matrix_GUI import Create_RangeChart
from poker_engine.preset_ranges import load_range, list_available_ranges



if __name__ == '__main__':

    create_new = input('Do you want to build a new range? [Y/N] \n')

    if create_new == 'Y' or create_new == 'y':
        Create_RangeChart()


    range_chart = np.load('range_matrix.npy')

    print("User created range chart:")
    print(range_chart)

    print()
    print('List of available ranges:')
    print(list_available_ranges())

    print()
    twosplus = load_range('22+and_suited')
    print('Loaded deuces plus range:')
    print(twosplus)



