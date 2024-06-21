from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import base64

private_key = '''-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDShbaV3WnJLMff
qGP5+RvyHIBkmcIUZijjRiVKvGhc1K/Zju9mIxssiktIMxb7YBdSA13ubTQ4EYea
F93ROahoaNKRUH/Frf4PcUQk042evs70PQbDYADtwRqm9BCrFNq1xPKlASZgSzXV
1vT84zUy112t3rI2nichKF/1VXZzbUmjAKH2MMqUzmiKbD/HkBvl7dONdWs2HF2q
hk9oe7s6WPBDjM0iBuUdABLdRbB4iKA9AHZ2Jztbpm7U7bcqviTeIXrIvqbUUa/N
CwuqWNDH0sx/i9BdDC1Z8zvpN/CkGCQ3uOwltDxMjAz78FH5giuvZz7s7+sshASa
2X1NiETxAgMBAAECggEAAluuEzKsnyzDVmPrLsWI3k1OB0Wm12MN9stcp2AoTE+A
YsL60OpewQ2rHZvSfse+RLrPhnHhtMKstRMRKhyBU7es3os7MZDEq96cbhjFv6Jd
uUpy6D6+8+rThhnT+ZHQiCdOT0vagEsHYNkfqGXqvO8nPpQ9uDMZ6oF3X0093oaB
jcJ5TBPcJngcdCn/xIoDgEamrxysmsTfcSATgGf5C1sXEYsyCyi+bwnpuLlQxnBO
/Fj+66vs9Xx0QU/65EUFB+6dUl3GyiDFWf0/89ipWmB/ecssjL632lVuNs7zwZJP
+/WThi8GKwpaXd3jaeeECPkWsHwKs8tb2glDwP4dAQKBgQD3oeLvRoT0Um+4uPu6
eV75a4V5Xw/dHhpQ+Q5jWo6OMSf1x/xW3lceMfGo2FFI2zNcOGQm4IfySzEUPHEo
VfoM24Dfv93ngRCpvp3bye15mfGYxJGYkRe1gilpP/GByG+Zneer30ds/mf5shkg
mUWIDWvHR/OAcFR8bm3icYWv0QKBgQDZos+QP766a7UX2hHLqkMdbNvdR8N/A4LC
uqI2lViH+UcCa/0hJ/ed+9k/SZshkki85t7k0NrNZt5FcIuNPpm5LGx8s8EiHigh
uWgUv0AiMbuXS2/3uqJp4DLOxtvf6CdajmSX/mVu/9gwpPGQO2aujUJ7LQxSzMOD
67nT5ByrIQKBgCOEnMAlJTzF9jBQmAqPDghIW8Sk1empP60Ni/rEKl5KvqiKHq93
BJfYIglNvZrtldhMXlEVM2qVTlzQropSiqL9eOae5n0mDfXK2WmE9QLUCcsXpqpz
ZSsrmDT4bvNmhFtMQsZsKBqCAvfVi7UZRtfU1PioYUyyz+tpC2nHTp2BAoGBANf/
sqmj2pQC2hT2JbtRHJNTu1L/KpQg0+KYgO5Tgy5QxZ0tuGjz1dpCXvdlAkZrfS2e
pZHLh51cfzXD4X0pqEAUSwfpD8Hg1EvES/xrZCeL3HboNBRWc2NJVKPM0eSD8Kr7
r/L6VYm4+sQssGNJ0Ttkj5rYtuZmu5Vum1wlhh6BAoGBAKNfSn0DO0l6ydky51lZ
jWE/H6/p7DpvxpW1CuJWsfH6jEgWCAtCLDCow4mdqgSEJMuTWqlikxaEPYzfq2ak
Si+7tcRkeiVM/FLPK8w2zeyVsUFr0H3CHor41+bew390na5FkmOfvfkSdMGonlix
schehsAqmCybxO4AdhOWweDq
-----END PRIVATE KEY-----'''


encrypted_message = "IbSQ20+l6G2Rqk+EWAjkoG5dirdxeCxzp2dKKAKGjiwhAGgFsGJn5+C6JeZlF1CpYFVgjl8vYR81/9VKVkZFziiyEBg6ARIPelkMaq5M+Q9rR/cbjKdLR1Zox9vYhb41CP0zqLrkn+qMl1jT3A7ixZZDIBXevXIyOwO04eLpVno3yTVr6K7YYEn1pJzP5bwjmkDC7OGxy7h6Sxa8RKFDgCOlpwqEms6pASjZPbTXTE+iLYWPjwh9RRhHwBpWQeggnL1UNOstRnMC+bDs8DmLXcLiSlgsBsL1pwD52kTL9gccUINAHDZ9e8cMFTRPUW8D7JDo4NlloVRpB4sQ0KMwIg=="

def load_private_key(pem_data):
    private_key = serialization.load_pem_private_key(
        pem_data.encode(),
        password=None,
    )
    return private_key

def decrypt_with_private_key(private_key, encrypted_message):
    decrypted = private_key.decrypt(
        base64.b64decode(encrypted_message),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted.decode('utf-8')

private_key = load_private_key(private_key)
decrypted_message = decrypt_with_private_key(private_key, encrypted_message)
print(decrypted_message)
