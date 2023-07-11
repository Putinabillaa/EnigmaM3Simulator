class Reflector:
    '''Reflector class for Enigma machine'''
    def __init__(self):
        wiring_text = "YRUHQSLDPXNGOKMIEBFZCWVJAT" # UKW-B
        self.wiring = [char for char in wiring_text]
    def encipher(self, key):
        shift = ord(self.state) - ord("A")
        idx = (((ord(key) - ord("A")) % 26) + shift) % 26
        letter = self.wiring[idx]
        key_out = chr(
            ord("A") + (ord(letter) - ord("A") + 26 - shift) % 26
        )
        return key_out
