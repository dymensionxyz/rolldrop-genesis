import sys
import argparse
import rolldrop_genesis
import json

if __name__ == '__main__':
    # Create the parser
    parser = argparse.ArgumentParser(description='Process genesis file and airdrop details.')
    # Add the arguments
    parser.add_argument('base_denom', type=str, help='The base denomination for the chain')
    parser.add_argument('bech32_prefix', type=str, help='The prefix for the Bech32 addresses')
    parser.add_argument('input_genesis_file_path', type=str, help='The input genesis file path')
    parser.add_argument('airdrop_file_path', type=str, help='The airdrop file path')
    parser.add_argument('output_genesis_file_path', type=str, help='The output genesis file path')

    # Execute the parse_args() method
    args = parser.parse_args()

    base_denom = args.base_denom
    bech32_prefix = args.bech32_prefix
    input_genesis_file_path = args.input_genesis_file_path
    airdrop_file_path = args.airdrop_file_path
    output_genesis_file_path = args.output_genesis_file_path
    
    with open(input_genesis_file_path, 'r') as genesis_file:
        initial_genesis_data = json.load(genesis_file)

    rolldrop_genesis.add_accounts_to_genesis_file(base_denom, bech32_prefix, airdrop_file_path, initial_genesis_data, output_genesis_file_path)
