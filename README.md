# Rolldrop Genesis Tool

The Rolldrop Genesis Tool is designed to facilitate the process of adding accounts (vested and non vested) to a Rollapp genesis file.
This is specifically useful when there are a large number of accounts to be added to the genesis file like in the event of an airdrop.

## Prerequisites

1. The accounts file should contain only unique addresses.
2. The accounts file should be in JSON format and should contain the following structure:
   ```json
   [
       {
         "claimAddress": "<address>", # Valid lower case hex address
         "amount": "<amount>", # Amount of tokens to be allocated in base denomination
         "vesting": { # Vesting can be omitted if the allocation is not vested
           "start_time": "<start_time>", # Unix timestamp
           "end_time": "<end_time>" # Unix timestamp
         }
       },
       ...
     ]
   ```
3. The input genesis file should be a valid genesis file for the Rollapp.
4. The Rollapp is an EVM Rollapp.

## How to Run

To run the Rolldrop Genesis Tool, you will need Python installed on your system. Once you have Python set up, follow these steps:

1. Clone the repository to your local machine.
2. Navigate to the root directory of the project.
3. Install the required dependencies by running `pip install -r requirements.txt`.
4. Execute the tool by running the command below. Replace the placeholders with your specific values:
   ```
   python main.py <base_denom> <bech32_prefix> <input_genesis_file_path> <airdrop_file_path> <output_genesis_file_path>
   ```
   - `<base_denom>`: The base denomination for the chain (e.g., "adym" for Dymension).
   - `<bech32_prefix>`: The prefix for the Bech32 addresses specific to your blockchain (e.g., "dym" for Dymension addresses).
   - `<input_genesis_file_path>`: The file path to the input genesis file that you want to modify. Should be a valid genesis file.
   - `<accounts_file_path>`: The file path to the JSON file containing the account allocations. 
   - `<output_genesis_file_path>`: The desired file path for the output genesis file with the airdrop allocations included.

## Example
    
```bash
python rolldrop-genesis/main.py urapx ethm example/genesis.json example/allocations.json example/final_genesis.json
```
In this example, the tool will read the genesis file at `example/genesis.json` and the airdrop file at `example/allocations.json`. It will then write the updated genesis file to `example/final_genesis.json`.
