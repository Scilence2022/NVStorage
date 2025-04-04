#!/usr/bin/env python3

import sys
import argparse
import random
import numpy as np
from itertools import product

def binary_to_3d_sequential(binary_data, dimensions=(16, 16, 16), fill_empty=True, default_bit=0):
    """
    Map binary data to 3D coordinates sequentially
    
    Args:
        binary_data (bytes): Binary data to map
        dimensions (tuple): The dimensions of the 3D space (x, y, z)
        fill_empty (bool): Whether to fill empty positions with default bits
        default_bit (int): Default bit value for empty positions
        
    Returns:
        list: List of tuples (x, y, z, bit_value)
    """
    # Get maximum values for each dimension
    max_x, max_y, max_z = dimensions
    
    # Calculate total bits that will fit in the specified 3D space
    total_positions = max_x * max_y * max_z
    
    # Result list to store coordinates and bit values
    result = []
    
    # Process each byte in the binary data
    bit_position = 0
    for byte_idx, byte in enumerate(binary_data):
        # Process each bit in the byte
        for bit_idx in range(8):
            # Extract the bit (0 or 1)
            bit = (byte >> (7 - bit_idx)) & 1
            
            # Calculate the 3D position
            position = bit_position % total_positions
            x = position % max_x
            y = (position // max_x) % max_y
            z = position // (max_x * max_y)
            
            # Store the coordinates and bit value
            result.append((x, y, z, bit))
            
            # Increment the bit position
            bit_position += 1
            
            # Check if we've filled the entire 3D space
            if bit_position >= total_positions:
                return result, byte_idx, len(binary_data)
    
    # If we need to fill the remaining positions
    if fill_empty and bit_position < total_positions:
        # Fill the remaining positions with default bit value
        for position in range(bit_position, total_positions):
            x = position % max_x
            y = (position // max_x) % max_y
            z = position // (max_x * max_y)
            result.append((x, y, z, default_bit))
    
    return result, len(binary_data) - 1, len(binary_data)

def binary_to_3d_random_positions(binary_data, dimensions=(16, 16, 16), fill_empty=True, default_bit=0, seed=None):
    """
    Map binary data to random 3D coordinates
    
    Args:
        binary_data (bytes): Binary data to map
        dimensions (tuple): The dimensions of the 3D space (x, y, z)
        fill_empty (bool): Whether to fill empty positions with default bits
        default_bit (int): Default bit value for empty positions
        seed (int): Random seed for reproducibility
        
    Returns:
        list: List of tuples (x, y, z, bit_value)
    """
    # Set random seed if provided
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    
    # Get maximum values for each dimension
    max_x, max_y, max_z = dimensions
    
    # Generate all possible coordinates
    all_coords = list(product(range(max_x), range(max_y), range(max_z)))
    
    # Shuffle the coordinates randomly
    random.shuffle(all_coords)
    
    # Calculate total bits that will fit in the specified 3D space
    total_positions = len(all_coords)
    
    # Result list to store coordinates and bit values
    result = []
    
    # Process each byte in the binary data
    bit_position = 0
    for byte_idx, byte in enumerate(binary_data):
        # Process each bit in the byte
        for bit_idx in range(8):
            # Extract the bit (0 or 1)
            bit = (byte >> (7 - bit_idx)) & 1
            
            # Get the next coordinate from the shuffled list
            if bit_position < total_positions:
                x, y, z = all_coords[bit_position]
                
                # Store the coordinates and bit value
                result.append((x, y, z, bit))
                
                # Increment the bit position
                bit_position += 1
            else:
                return result, byte_idx, len(binary_data)
    
    # If we need to fill the remaining positions
    if fill_empty and bit_position < total_positions:
        # Fill the remaining positions with default bit value
        for i in range(bit_position, total_positions):
            x, y, z = all_coords[i]
            result.append((x, y, z, default_bit))
    
    return result, len(binary_data) - 1, len(binary_data)

def binary_to_3d_random_assignment(binary_data, dimensions=(16, 16, 16), fill_empty=True, default_bit=0, seed=None):
    """
    Randomly assign binary data to 3D coordinates, potentially with multiple bits per position
    
    Args:
        binary_data (bytes): Binary data to map
        dimensions (tuple): The dimensions of the 3D space (x, y, z)
        fill_empty (bool): Whether to fill empty positions with default bits
        default_bit (int): Default bit value for empty positions
        seed (int): Random seed for reproducibility
        
    Returns:
        list: List of tuples (x, y, z, bit_value)
    """
    # Set random seed if provided
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    
    # Get maximum values for each dimension
    max_x, max_y, max_z = dimensions
    
    # Result dictionary to store coordinates and bit values
    result_dict = {}
    
    # Calculate total bits in the binary data
    total_bits = len(binary_data) * 8
    total_positions = max_x * max_y * max_z
    
    # Process each byte in the binary data
    bit_count = 0
    for byte_idx, byte in enumerate(binary_data):
        # Process each bit in the byte
        for bit_idx in range(8):
            # Extract the bit (0 or 1)
            bit = (byte >> (7 - bit_idx)) & 1
            
            # Generate a random position within the dimensions
            x = random.randint(0, max_x - 1)
            y = random.randint(0, max_y - 1)
            z = random.randint(0, max_z - 1)
            
            # Store the coordinates and bit value
            result_dict[(x, y, z)] = bit
            
            # Increment the bit count
            bit_count += 1
            
            # Optional: limit to a maximum number of bits
            if bit_count >= total_positions:
                break
        
        if bit_count >= total_positions:
            break
    
    # If we need to fill the remaining positions
    if fill_empty:
        # Get all possible coordinates
        all_coords = list(product(range(max_x), range(max_y), range(max_z)))
        
        # Fill any missing positions with default bit value
        result = []
        for x, y, z in all_coords:
            bit = result_dict.get((x, y, z), default_bit)
            result.append((x, y, z, bit))
    else:
        # Convert dictionary to list
        result = [(x, y, z, bit) for (x, y, z), bit in result_dict.items()]
    
    return result, len(binary_data) - 1, len(binary_data)

def binary_to_3d(input_file, output_file=None, dimensions=(16, 16, 16), mapping_mode="sequential", 
                fill_empty=True, default_bit=0, seed=None):
    """
    Read a binary file and map each bit to a 3D coordinate.
    
    Args:
        input_file (str): Path to the input binary file
        output_file (str, optional): Path to the output file. If None, print to stdout
        dimensions (tuple, optional): The dimensions of the 3D space (x, y, z)
        mapping_mode (str): Mapping mode ('sequential', 'random_positions', 'random_assignment')
        fill_empty (bool): Whether to fill empty positions with default bits
        default_bit (int): Default bit value for empty positions
        seed (int): Random seed for reproducibility
    """
    # Open binary file for reading
    try:
        with open(input_file, 'rb') as f:
            binary_data = f.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # Create output file handle or use stdout
    out_handle = open(output_file, 'w') if output_file else sys.stdout
    
    # Map binary data to 3D coordinates based on the selected mapping mode
    if mapping_mode == "sequential":
        result, last_byte_idx, total_bytes = binary_to_3d_sequential(binary_data, dimensions, fill_empty, default_bit)
    elif mapping_mode == "random_positions":
        result, last_byte_idx, total_bytes = binary_to_3d_random_positions(binary_data, dimensions, fill_empty, default_bit, seed)
    elif mapping_mode == "random_assignment":
        result, last_byte_idx, total_bytes = binary_to_3d_random_assignment(binary_data, dimensions, fill_empty, default_bit, seed)
    else:
        print(f"Error: Unknown mapping mode '{mapping_mode}'")
        sys.exit(1)
    
    # Sort results by coordinates for better readability (optional)
    if mapping_mode in ["random_positions", "random_assignment"]:
        result.sort(key=lambda item: (item[2], item[1], item[0]))  # Sort by z, y, x
    
    # Write the results to the output file
    for x, y, z, bit in result:
        out_handle.write(f"({x}, {y}, {z})\t{bit}\n")
    
    # Close the output file if it was opened
    if output_file:
        out_handle.close()
    
    # If we didn't process all bytes, print a warning
    if last_byte_idx < total_bytes - 1 and not fill_empty:
        print(f"Warning: Only processed {last_byte_idx + 1} bytes out of {total_bytes} total bytes.")
    
    # Calculate some statistics
    total_bits = len(binary_data) * 8
    total_positions = dimensions[0] * dimensions[1] * dimensions[2]
    filled_positions = len(result)
    
    # Print a more detailed summary
    print(f"Successfully mapped data to 3D space:")
    print(f"  - Input file: {total_bytes} bytes ({total_bits} bits)")
    print(f"  - 3D space: {dimensions[0]}×{dimensions[1]}×{dimensions[2]} ({total_positions} positions)")
    print(f"  - Filled positions: {filled_positions} ({filled_positions/total_positions*100:.1f}%)")
    if fill_empty and total_bits < total_positions:
        print(f"  - Positions with default bit value: {total_positions - min(total_bits, total_positions)}")

def parse_args():
    parser = argparse.ArgumentParser(description='Convert binary file data to 3D coordinates')
    parser.add_argument('input_file', help='Path to the input binary file')
    parser.add_argument('-o', '--output', help='Path to the output file (default: print to stdout)')
    parser.add_argument('-d', '--dimensions', type=int, nargs=3, default=[16, 16, 16],
                        help='Dimensions of the 3D space as "x y z" (default: 16 16 16)')
    parser.add_argument('-m', '--mode', choices=['sequential', 'random_positions', 'random_assignment'], 
                        default='sequential', help='Mapping mode (default: sequential)')
    parser.add_argument('--no-fill', action='store_true', 
                        help='Do not fill empty positions with default bit value')
    parser.add_argument('--default-bit', type=int, choices=[0, 1], default=0,
                        help='Default bit value for empty positions (default: 0)')
    parser.add_argument('--seed', type=int, help='Random seed for reproducibility')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    binary_to_3d(args.input_file, args.output, tuple(args.dimensions), args.mode, 
                 not args.no_fill, args.default_bit, args.seed) 