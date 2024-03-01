import bech32

def hex_to_bech32(hex_str, hrp='dym'):
    # Convert hexadecimal to bytes
    data = bytes.fromhex(hex_str)

    # Convert bytes to 5-bit groups
    conv_data = bech32.convertbits(data, 8, 5)
    if conv_data is None:
        raise ValueError("Conversion error")

    # Encode to Bech32
    bech32_addr = bech32.bech32_encode(hrp, conv_data)
    if bech32_addr is None:
        raise ValueError("Bech32 encoding error")

    return bech32_addr

def is_valid_bech32_address(prefix, address):
    try:
        # Decode the Bech32 address
        hrp, data = bech32.bech32_decode(address)
        # Check if the decoding was successful and if the human-readable part is as expected
        # For Bitcoin, the HRP should be "bc" for mainnet and "tb" for testnet.
        # Adjust the HRP check based on the cryptocurrency and network you are targeting.
        return hrp == prefix and data is not None
    except (ValueError, TypeError):
        return False
