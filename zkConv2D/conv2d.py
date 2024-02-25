import numpy as np

def summation(arr):
    tmp = arr.reshape(-1)
    sum = 0
    for i in tmp:
        sum += i
        
    return sum

def conv2d(input, filters, bias, num_filters):
    input_height, input_width, _ = input.shape
    filter_height, filter_width, _ = filters[0].shape

    output_height = input_height - filter_height + 1
    output_width = input_width - filter_width + 1

    output = np.zeros((output_height, output_width, num_filters))

    for k in range(num_filters):
        for i in range(output_height):
            for j in range(output_width):
                print((input[i:i+filter_height, j:j+filter_width] * filters[k]).shape)
                output[i, j, k] = summation(input[i:i+filter_height, j:j+filter_width] * filters[k]) + bias[k]

    return output



def main():
    input = np.array([
        [5, 3, 4, 1, 2],
        [5, 3, 4, 1, 2],
        [5, 3, 4, 1, 2],
        [5, 3, 4, 1, 2],
        [5, 3, 4, 1, 2],
    ])
    
   
    input = input.reshape(5,5,1)
    
    filters = np.array([
            [[[1], [0], [-1]],
            [[1], [0], [-1]],
            [[1], [0], [-1]]],
            
            
            [[[1], [0], [-1]],
            [[1], [0], [-1]],
            [[1], [0], [-1]]],
            
            
            [[[1], [0], [-1]],
            [[1], [0], [-1]],
            [[1], [0], [-1]]],
            
            
            [[[1], [0], [-1]],
            [[1], [0], [-1]],
            [[1], [0], [-1]]],
            
            
            [[[1], [0], [-1]],
            [[1], [0], [-1]],
            [[1], [0], [-1]]],
            
            
            [[[1], [0], [-1]],
            [[1], [0], [-1]],
            [[1], [0], [-1]]],
            
            
            [[[1], [0], [-1]],
            [[1], [0], [-1]],
            [[1], [0], [-1]]],
            
            
            [[[1], [0], [-1]],
            [[1], [0], [-1]],
            [[1], [0], [-1]]],
            
            
            [[[1], [0], [-1]],
            [[1], [0], [-1]],
            [[1], [0], [-1]]],
            
            
            [[[1], [0], [-1]],
            [[1], [0], [-1]],
            [[1], [0], [-1]]]
    ])
    bias = np.array([
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
    ])
    
    num_filters = 10
    
    
    out = conv2d(input, filters, bias, num_filters)
    
if __name__ == "__main__":
    main()
    