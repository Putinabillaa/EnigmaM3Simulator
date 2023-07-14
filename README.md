# EnigmaM3Simulator 📜

## Table of Contents
- [Description](#description)
- [Program Requirements and Installation](#program-requirements-and-installation)
- [Get Started](#get-started)
- [Author](#author)

## Description
This is a simple Python app that simulates Enigma M3 encryption. The rotors can be chosen from type I, II, and III. The reflector used is type B (UKW-B). The wiring and notch used in each rotor type are referenced from [here](https://www.cryptomuseum.com/crypto/enigma/wiring.htm#12)

![Desktop - 5 (1)](https://github.com/Putinabillaa/EnigmaM3Simulator/assets/109022993/69070540-34a6-43f3-8eca-dd83b527c5ea)


## Program Requirements and Installation
- Python 3.9 or Above
  ```
  % sudo apt install python3
  ```
- PyQt5
  ```
  % pip install PyQt5
  ```

## Get Started
1. Start the program
    ```
    % python src/App.py
    ```
2. Configure each rotor's ```type```, ```Position```, and ```Ring```.
3. Configure the ```plugboard``` (the bottom one) by clicking the letter in pairs. The same color represents the switched pair. To unplug, re-click the letter.
4. The text can be inputted through ```keyboard button``` (the middle one), ```keyboard press```, or by clicking the ```Edit``` button in either ```Plain Text``` or ```Cipher Text``` text fields (click ```Encrypt``` or ```Decrypt``` afterward).
5. After each keyboard click/press the letter in ```lampboard``` will light up. The encrypted text will also be displayed on the ```Cipher Text``` text field (or in ```Plain Text``` if you clicked ```Decrypt```)
6. Each encryption step will be displayed on the right side.
7. Click ```Clear``` to clear ```Plain Text```, ```Cipher Text```, and the encryption step.

> Note: if you clicked ```delete``` or ```backspace``` key on your keyboard, for each click, the text in ```Plain Text``` and ```Cipher Text``` will be deleted by one letter. Some of the steps will also be deleted. Rotor 1 will also be returned one step. Note that the returned rotor is limited to rotor 1, hence this method will not work for all condition.
   
## Author
Puti Nabilla Aidira (13521088)
