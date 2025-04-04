#!/usr/bin/env python3

import os
import random
import argparse
import numpy as np

def generate_random_binary_file(output_file, size_bytes=64, seed=None):
    """
    Generate a binary file with random data for testing purposes.
    
    Args:
        output_file (str): Path to the output binary file
        size_bytes (int): Size of the file in bytes
        seed (int): Random seed for reproducibility (None for true randomness)
    """
    # Set random seed if provided
    if seed is not None:
        random.seed(seed)
        
    # Generate random bytes
    random_bytes = bytearray(random.getrandbits(8) for _ in range(size_bytes))
    
    # Write to file
    with open(output_file, 'wb') as f:
        f.write(random_bytes)
    
    print(f"Generated random binary file '{output_file}' ({size_bytes} bytes)")

def generate_truly_random_binary_file(output_file, size_bytes=64):
    """
    Generate a binary file with truly random data using os.urandom
    
    Args:
        output_file (str): Path to the output binary file
        size_bytes (int): Size of the file in bytes
    """
    # Generate truly random bytes
    random_bytes = os.urandom(size_bytes)
    
    # Write to file
    with open(output_file, 'wb') as f:
        f.write(random_bytes)
    
    print(f"Generated truly random binary file '{output_file}' ({size_bytes} bytes)")

def generate_pattern_binary_file(output_file, pattern_type="checkerboard", size_bytes=64):
    """
    Generate a binary file with a specific pattern for testing purposes.
    
    Args:
        output_file (str): Path to the output binary file
        pattern_type (str): Type of pattern ('checkerboard', 'gradient', 'zeros', 'ones')
        size_bytes (int): Size of the file in bytes
    """
    if pattern_type == "checkerboard":
        # Alternating 0s and 1s (binary: 10101010)
        byte_value = 0xAA
        pattern_bytes = bytearray([byte_value] * size_bytes)
    elif pattern_type == "gradient":
        # Increasing values from 0 to 255 and then wrapping
        pattern_bytes = bytearray(i % 256 for i in range(size_bytes))
    elif pattern_type == "zeros":
        # All zeros
        pattern_bytes = bytearray([0] * size_bytes)
    elif pattern_type == "ones":
        # All ones
        pattern_bytes = bytearray([255] * size_bytes)
    elif pattern_type == "random_patterns":
        # Random patterns with various bit distributions
        pattern_bytes = bytearray()
        for i in range(size_bytes):
            if i % 4 == 0:
                # Every 4th byte is random
                pattern_bytes.append(random.getrandbits(8))
            elif i % 4 == 1:
                # Alternate between all zeros and all ones
                pattern_bytes.append(0 if i % 8 < 4 else 255)
            elif i % 4 == 2:
                # Alternate bits within a byte
                pattern_bytes.append(0xAA if i % 8 < 4 else 0x55)
            else:
                # Gradient pattern
                pattern_bytes.append(i % 256)
    else:
        print(f"Unknown pattern type: {pattern_type}")
        return
    
    # Write to file
    with open(output_file, 'wb') as f:
        f.write(pattern_bytes)
    
    print(f"Generated {pattern_type} pattern binary file '{output_file}' ({size_bytes} bytes)")

def generate_custom_distribution_file(output_file, p_one=0.5, size_bytes=64, seed=None):
    """
    Generate a binary file with a custom probability distribution of bits
    
    Args:
        output_file (str): Path to the output binary file
        p_one (float): Probability of a bit being 1 (0.0 to 1.0)
        size_bytes (int): Size of the file in bytes
        seed (int): Random seed for reproducibility
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Generate bits with the specified probability
    bits = np.random.choice([0, 1], size=size_bytes*8, p=[1-p_one, p_one])
    
    # Convert bits to bytes
    bytes_data = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(min(8, len(bits) - i)):
            if bits[i + j]:
                byte |= (1 << (7 - j))
        bytes_data.append(byte)
    
    # Write to file
    with open(output_file, 'wb') as f:
        f.write(bytes_data)
    
    print(f"Generated custom distribution binary file '{output_file}' ({size_bytes} bytes, p(1)={p_one})")

def parse_args():
    parser = argparse.ArgumentParser(description='Generate sample binary files for testing')
    parser.add_argument('-o', '--output', default='sample.bin', help='Path to the output binary file')
    parser.add_argument('-s', '--size', type=int, default=64, help='Size of the file in bytes')
    parser.add_argument('-t', '--type', choices=['random', 'truly_random', 'checkerboard', 'gradient', 
                                                'zeros', 'ones', 'random_patterns', 'custom'], 
                        default='random', help='Type of data to generate')
    parser.add_argument('-p', '--probability', type=float, default=0.5, 
                        help='Probability of a bit being 1 (for custom distribution)')
    parser.add_argument('--seed', type=int, help='Random seed for reproducibility')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    
    if args.type == 'random':
        generate_random_binary_file(args.output, args.size, args.seed)
    elif args.type == 'truly_random':
        generate_truly_random_binary_file(args.output, args.size)
    elif args.type == 'custom':
        generate_custom_distribution_file(args.output, args.probability, args.size, args.seed)
    else:
        generate_pattern_binary_file(args.output, args.type, args.size)