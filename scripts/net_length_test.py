#!/usr/bin/env python3
import argparse
import re

def compute_length(coords):
    length = 0
    for (x1, y1), (x2, y2) in zip(coords, coords[1:]):
        length += abs(x1 - x2) + abs(y1 - y2)
    return length

def parse_def(def_file):
    lengths = {}
    with open(def_file) as f:
        in_nets = False
        net_name = None
        coords = []
        for line in f:
            line = line.strip()
            if not in_nets:
                if line.startswith('NETS'):
                    in_nets = True
                continue
            if line.startswith('END NETS'):
                if net_name and coords:
                    lengths[net_name] = compute_length(coords)
                break
            if line.startswith('-'):
                if net_name and coords:
                    lengths[net_name] = compute_length(coords)
                parts = line.split()
                net_name = parts[1]
                coords = []
            for x, y in re.findall(r'\(\s*(\d+)\s+(\d+)\s*\)', line):
                coords.append((int(x), int(y)))
            if ';' in line and net_name:
                lengths[net_name] = compute_length(coords)
                net_name = None
                coords = []
    return lengths

def main():
    parser = argparse.ArgumentParser(description='Compute net lengths from a DEF file')
    parser.add_argument('def_file', help='DEF file to parse')
    args = parser.parse_args()
    lengths = parse_def(args.def_file)
    for name, length in lengths.items():
        print(f"{name} {length}")

if __name__ == '__main__':
    main()
