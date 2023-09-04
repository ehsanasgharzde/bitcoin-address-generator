import hashlib
import base58
import binascii
import ecdsa


def green(text):
    """
    ANSI Code to turn strings green.
    """
    return f"\033[92m{text}\033[0m"


def yellow(text):
    """
    ANSI Code to turn strings yellow.
    """
    return f"\033[93m{text}\033[0m"


class BTC():
    def __init__(self):
        """
        PVKEY: Private Key
        PUKEY: Public Key
        SHA256PUKEY: SHA256 Encoded Public Key
        RIDEMP160PUKEY: RIDEMP160 Encoded SHA256PUKEY
        NBPUKEY: '00' added to the beginning of RIDEMP160PUKEY
        NBPVKEY: '80' added to the end of PVKEY
        DOUSHA256PU: Double SHA256 Encoded NBPUKEY
        DOUSHA256PV: Double SHA256 Encoded NBPVKEY
        CHECKSUMPU: DOUSHA256PU first 4 bytes
        CHECKSUMPV: DOUSHA256PV first 4 bytes
        PREADDRESS: CHECKSUMPU added to NBPUKEY
        PREWIF: CHECKSUMPV added to NBPVKEY
        ADDRESS: Base58 Encoded PREADDRESS
        WIF: Base58 Encoded PREWIF
        """
        curve = ecdsa.SECP256k1
        self.PVKEY = ecdsa.SigningKey.generate(curve=curve)
        self.PUKEY = f"04{self.PVKEY.get_verifying_key().to_string().hex()}"
        self.SHA256PUKEY = hashlib.sha256(
            binascii.unhexlify(self.PUKEY)).hexdigest()
        self.RIDEMP160PUKEY = hashlib.new(
            "ripemd160", binascii.unhexlify(self.SHA256PUKEY)).hexdigest()
        self.NBPUKEY = f"00{self.RIDEMP160PUKEY}"
        self.NBPVKEY = f"80{self.PVKEY.to_string().hex()}"
        self.DOUSHA256PU = self.DouSHA256(self.NBPUKEY)
        self.DOUSHA256PV = self.DouSHA256(self.NBPVKEY)
        self.CHECKSUMPU = self.DOUSHA256PU[:8]
        self.CHECKSUMPV = self.DOUSHA256PV[:8]
        self.PREADDRESS = self.NBPUKEY + self.CHECKSUMPU
        self.PREWIF = self.NBPVKEY + self.CHECKSUMPV
        self.ADDRESS = base58.b58encode(
            binascii.unhexlify(self.PREADDRESS)).decode("UTF-8")
        self.WIF = base58.b58encode(
            binascii.unhexlify(self.PREWIF)).decode("UTF-8")

    def DouSHA256(self, str):
        DOUSHA256PU = str
        for i in range(1, 3):
            DOUSHA256PU = hashlib.sha256(
                binascii.unhexlify(DOUSHA256PU)).hexdigest()
        return DOUSHA256PU

    def document(self):
        docs = """
        Libraries:
        hashlib
            Hash Encodings Library
            --> Usage: Encoding
        base58
            Base58 Encodings Library
            --> Usage: Encoding
        binascii
            binary and ASCII Library
            --> Usage: Convertion between Binary and ASCII values
        ecdsa
            Ellicptic Curve Digital Signature Algorithm 
            --> Usage: Generate Private Key

        Step 1:
        Creating Private Key with SECP256k1 curve

        Step 2:
        Creating Public Key based on previuos Private Key

        Step 3:
        Applying SHA256 Encoding to previous Public Key

        Step 4:
        Applying RIDEMP160 Encoding to previous SHA256 Encoded Public Key

        Step 5:
        Prepending "00" as Network Byte to previous RIDEMP160 Encoded Public Key

        Step 6:
        Applying Double SHA256 to previous Network Byte Public Key

        Step 7:
        Getting a Checksum from previous Double SHA256 Encoded Public Key
        First 4 bytes are the Checksum

        Step 8:
        Adding Checksum to Network Byte Public Key

        Step 9:
        Applying Base58 Encoding to previous Pre Address

        Step 10:
        Adding "80" as Network Byte to Private Key

        Step 11:
        Applying Double SHA256 to previous Network Byte Private Key

        Step 12:
        Getting a Checksum from previous Double SHA256 Encoded Private Key
        First 4 bytes are the Checksum

        Step 13:
        Adding Checksum to Network Byte Private Key

        Step 14:
        Applying Base58 Encoding to previous Pre WIF\n\n"""

        print(docs)

    def answer(self):
        str = """
        Mainnet addresses begin with '1', '3', or 'bc1',
        while testnet addresses begin with '2', 'm', 'n', or 'tb1'.
        
        Coins cannot be sent between networks.
        If mainnet bitcoin is sent to a testnet address, it is destroyed and unrecoverable.
        """
        print(str)
