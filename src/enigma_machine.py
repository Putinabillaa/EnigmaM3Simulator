import reflector as rf
import rotor as rt

class Enigma:
    '''Enigma machine class'''
    def __init__(self, rf, rt1, rt2, rt3, state, ring, plugboard_settings):
        self.reflector = rf
        self.rotor1 = rt1
        self.rotor2 = rt2
        self.rotor3 = rt3

        self.rotor1.state = state[0]
        self.rotor2.state = state[1]
        self.rotor3.state = state[2]
        self.rotor1.ring = ring[0]
        self.rotor2.ring = ring[1]
        self.rotor3.ring = ring[2]
        self.reflector.state = 'A'
        self.plugboard_settings = plugboard_settings
        letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        letter_switch = [char for char in letter]
        for (k, v) in self.plugboard_settings:
            letter_switch[ord(k) - ord("A")] = v
            letter_switch[ord(v) - ord("A")] = k
        self.translation_table = str.maketrans(letter, "".join(letter_switch))

        self.step_by_step = ""
    
    def __setattr__(self, name, value):
        self.__dict__[name] = value
        if name == "plugboard_settings":
            letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            letter_switch = [char for char in letter]
            for (k, v) in self.plugboard_settings:
                letter_switch[ord(k) - ord("A")] = v
                letter_switch[ord(v) - ord("A")] = k
            self.translation_table = str.maketrans(letter, "".join(letter_switch))
            
    def enchiper(self, c_in):
        '''Enchiper one character'''
        self.step_by_step = ""
        if not c_in.isalpha():
            self.step_by_step += "Input: {}\n".format(c_in)
            output = c_in
            self.step_by_step += "Output: {}\n".format(output)
        else:
            c_upper = c_in.upper()
            self.step_by_step += "Input: {}\n".format(c_upper)
            c = c_upper.translate(self.translation_table)
            self.step_by_step += "Plugboard: {}\n".format(c)
            if self.rotor2.is_in_turnover_pos() and not self.rotor1.is_in_turnover_pos():
                self.rotor2.step()
                self.rotor3.step()
            if self.rotor2.is_in_turnover_pos() and self.rotor1.is_in_turnover_pos():
                self.rotor3.step()
            if self.rotor1.is_in_turnover_pos():
                self.rotor2.step()
            self.rotor1.step()
            t = self.rotor1.encipher_right(c)
            self.step_by_step += "Rotor 1: {}\n".format(t)
            t = self.rotor2.encipher_right(t)
            self.step_by_step += "Rotor 2: {}\n".format(t)
            t = self.rotor3.encipher_right(t)
            self.step_by_step += "Rotor 3: {}\n".format(t)
            t = self.reflector.encipher(t)
            self.step_by_step += "Reflector: {}\n".format(t)
            t = self.rotor3.encipher_left(t)
            self.step_by_step += "Rotor 3: {}\n".format(t)
            t = self.rotor2.encipher_left(t)
            self.step_by_step += "Rotor 2: {}\n".format(t)
            t = self.rotor1.encipher_left(t)
            self.step_by_step += "Rotor 1: {}\n".format(t)
            output = t.translate(self.translation_table)
            self.step_by_step += "Output(Plugboard): {}\n".format(output)
            if(c_in.islower()):
                output = output.lower()
        self.step_by_step += "____________________\n\n"
        return output

    def get_state(self):
        '''Get state of the machine'''
        return (self.rotor1.state, self.rotor2.state, self.rotor3.state)