from crypto.unicode import encrypt, decrypt

string = encrypt("Text to encrypt")
a = string.rot13()
b = string.vigenere(worm="worm")
c = string.vernam()
d = string.godel(prime=1117)

print(a, b, c, d, sep="\n")

a = decrypt(a).rot13()
b = decrypt(b).vigenere(worm="worm")
c = decrypt(c[0]).vernam(c[1])
d = decrypt(d).godel(n=len(a), prime=1117)

print(a, b, c, d, sep="\n")

