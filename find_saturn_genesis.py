import hashlib, struct, time

psz = b"Saturn Cash genesis 2026 - A new orbit begins"
ntime = 1779650000
nbits = 0x1f00ffff
version = 1
reward = 50 * 100000000

def sha256d(b):
    return hashlib.sha256(hashlib.sha256(b).digest()).digest()

def varint(n):
    if n < 253:
        return bytes([n])
    raise ValueError("too large")

def ser_script_num(n):
    if n == 0:
        return b""
    out = bytearray()
    while n:
        out.append(n & 0xff)
        n >>= 8
    if out[-1] & 0x80:
        out.append(0)
    return bytes(out)

def push(data):
    return bytes([len(data)]) + data

# Bitcoin-style genesis coinbase, but Saturn timestamp
script_sig = bytes([4]) + struct.pack("<I", nbits) + bytes([1, 4]) + push(psz)

tx = b""
tx += struct.pack("<I", 1)
tx += varint(1)
tx += b"\x00" * 32
tx += struct.pack("<I", 0xffffffff)
tx += varint(len(script_sig)) + script_sig
tx += struct.pack("<I", 0xffffffff)
tx += varint(1)
tx += struct.pack("<q", reward)
pubkey_script = bytes.fromhex(
    "4104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f"
    "61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6"
    "bf11d5fac"
)
tx += varint(len(pubkey_script)) + pubkey_script
tx += struct.pack("<I", 0)

merkle = sha256d(tx)
print("merkle:", merkle[::-1].hex())

target = int("0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", 16)

nonce = 0
while True:
    header = (
        struct.pack("<I", version) +
        b"\x00" * 32 +
        merkle +
        struct.pack("<I", ntime) +
        struct.pack("<I", nbits) +
        struct.pack("<I", nonce)
    )
    h = sha256d(header)
    val = int.from_bytes(h[::-1], "big")
    if val <= target:
        print("time:", ntime)
        print("bits:", hex(nbits))
        print("nonce:", nonce)
        print("hash:", h[::-1].hex())
        break
    nonce += 1
    if nonce % 1000000 == 0:
        print("tried", nonce)
