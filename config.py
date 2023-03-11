import keychain

api_key = keychain.api_key
board_config = "A potentiometer is connected to analog pin A0. A flex sensor connected to analog pin A1. A photoresistor is connected to analog pin A2. A button is connected to pin 3: the pin reads HIGH when the button is pressed. A piezoelectric speaker is connected to pin 8: don't use external libraries to play sounds on this speaker. A servomotor is connected to pin 10. A yellow LED is connected to pin 11, a green LED to pin 12, and a red LED to pin 13."
system_prompt = "You are assisting a human with writing Arduino code. The Arduino is a Arduino Leonardo. You always have to output complete arduino code without additional text. Don't reply with anything but the code itself. Don't talk to the user directly, don't explain your code, just output the code itself. This is the request from the user:\n"