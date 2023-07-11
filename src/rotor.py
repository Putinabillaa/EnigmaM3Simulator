class Rotor:
    '''Rotor class for Enigma machine'''
    def __init__(self, wiring, notch=None, state='A', ring='A'):
        self.wiring = wiring
        self.notch = notch
        self.state = state
        self.ring = ring
        self.rwiring = ["0"] * 26
        for i in range(0, len(self.wiring)):
            self.rwiring[ord(self.wiring[i]) - ord("A")] = chr(ord("A") + i)
    
    def __setattr__(self, name, value):
        self.__dict__[name] = value
        if name == "wiring":
            self.rwiring = ["0"] * 26
            for i in range(0, len(self.wiring)):
                self.rwiring[ord(self.wiring[i]) - ord("A")] = chr(ord("A") + i)

    def encipher_right(self, key):
        shift = ord(self.state) - ord(self.ring)
        idx = (((ord(key) - ord("A")) % 26) + shift) % 26
        key_out = chr(
            ord("A") + (ord(self.wiring[idx]) - ord("A") + 26 - shift) % 26
        )
        return key_out
    
    def encipher_left(self, key):
        shift = ord(self.state) - ord(self.ring)
        idx = (((ord(key) - ord("A")) % 26) + shift) % 26
        key_out = chr(
            ord("A") + (ord(self.rwiring[idx]) - ord("A") + 26 - shift) % 26
        )
        return key_out
    
    def is_in_turnover_pos(self):
        return chr((ord(self.state) + 1 - ord("A")) % 26 + ord("A")) == self.notch
    
    def notching(self, offset=1):
        self.state = chr((ord(self.state) + offset - ord("A")) % 26 + ord("A"))
    
ROTOR_I_WIRING_TEXT = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
ROTOR_I_WIRING = [char for char in ROTOR_I_WIRING_TEXT]
ROTOR_I_NOTCH ="Y"
ROTOR_II_WIRING_TEXT = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
ROTOR_II_WIRING = [char for char in ROTOR_II_WIRING_TEXT]
ROTOR_II_NOTCH = "M"
ROTOR_III_WIRING_TEXT = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
ROTOR_III_WIRING = [char for char in ROTOR_III_WIRING_TEXT]
ROTOR_III_NOTCH = "D"
