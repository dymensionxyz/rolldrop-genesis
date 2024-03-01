import json
import utils
import consts


def add_vesting_account_to_genesis(base_denom, genesis, address, amount, vesting_start_time, vesting_end_time):
    account_json_obj = {
    "@type": "/cosmos.vesting.v1beta1.ContinuousVestingAccount",
    "base_vesting_account": {
        "base_account": {
        "address": address,
        "pub_key": None,
        "account_number": "0",
        "sequence": "0"
        },
        "original_vesting": [
        {
            "denom": base_denom,
            "amount": str(amount),
        }
        ],
        "delegated_free": [],
        "delegated_vesting": [],
        "end_time": vesting_end_time
    },
    "start_time": vesting_start_time
    }
    balance_json_obj = {
           "address": address,
           "coins": [
             {
               "denom": base_denom,
               "amount": str(amount)
             }
           ]
         }
    genesis['app_state']['auth']['accounts'].append(account_json_obj)
    genesis['app_state']['bank']['balances'].append(balance_json_obj)
    if not genesis['app_state']['bank']['supply']:
        genesis['app_state']['bank']['supply'].append({
            "denom": base_denom,
            "amount": str(amount)
        })
    else:
        for supply in genesis['app_state']['bank']['supply']:
            if supply['denom'] == base_denom:
                supply['amount'] = str(int(supply['amount']) + amount)
    return genesis

def add_base_account_to_genesis(base_denom, genesis, address, amount):
    account_json_obj = {
           "@type": "/ethermint.types.v1.EthAccount",
           "base_account": {
             "address": address,
             "pub_key": None,
             "account_number": "0",
             "sequence": "0"
           },
           "code_hash": "0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"
        }
    balance_json_obj = {
           "address": address,
           "coins": [
             {
               "denom": base_denom,
               "amount": str(amount)
             }
           ]
         }
    genesis['app_state']['auth']['accounts'].append(account_json_obj)
    genesis['app_state']['bank']['balances'].append(balance_json_obj)
    if not genesis['app_state']['bank']['supply']:
        genesis['app_state']['bank']['supply'].append({
            "denom": base_denom,
            "amount": str(amount)
        })
    else:
        for supply in genesis['app_state']['bank']['supply']:
            if supply['denom'] == base_denom:
                supply['amount'] = str(int(supply['amount']) + amount)
    return genesis


def add_accounts_to_genesis_file(base_denom, bech32_prefix, airdrop_file_path, genesis_data, output_genesis_file_path):
    # Load the merged_allocations.json
    with open(airdrop_file_path, 'r') as f:
        airdrop_allocations = json.load(f)

    # Initialize counters
    base_accounts_added = 0
    vesting_accounts_added = 0
    total_accounts = len(airdrop_allocations)

    for row in airdrop_allocations:
        amount = int(row[consts.AMOUNT_FIELD_NAME])
        bech32_address = utils.hex_to_bech32(row[consts.CLAIM_ADDRESS_FIELD_NAME][2:].lower(), bech32_prefix)
        if not utils.is_valid_bech32_address(bech32_prefix, bech32_address):
            raise ValueError(f"Invalid address: {bech32_address}")
        if row.get(consts.VESTING_FIELD_NAME) is not None:
            vesting_start_time = row[consts.VESTING_FIELD_NAME][consts.VESTING_START_TIME_FIELD_NAME]
            vesting_end_time = row[consts.VESTING_FIELD_NAME][consts.VESTING_END_TIME_FIELD_NAME]
            genesis_data = add_vesting_account_to_genesis(base_denom=base_denom, genesis=genesis_data, address=bech32_address, amount=amount, 
            vesting_start_time=vesting_start_time, vesting_end_time=vesting_end_time)
            vesting_accounts_added += 1
        else:
            genesis_data = add_base_account_to_genesis(base_denom=base_denom,genesis=genesis_data, address=bech32_address, amount=amount)
            base_accounts_added += 1

        # progress bar
        progress = (vesting_accounts_added + base_accounts_added) / total_accounts
        progress_percentage = progress * 100
        progress_bar = '[' + '#' * int(progress * 50) + '-' * (50 - int(progress * 50)) + ']'
        print(f"\rProgress: {progress_bar} {progress_percentage:.2f}%", end="")

    # Make assertions
    assert total_accounts == base_accounts_added + vesting_accounts_added, "Total accounts do not match the sum of base and vesting accounts"
    print(f"Added {base_accounts_added} base accounts and {vesting_accounts_added} vesting accounts to genesis file")
    
    # Write the updated genesis_data back to the genesis.json file
    with open(output_genesis_file_path, 'w') as genesis_file:
        json.dump(genesis_data, genesis_file, indent=4)