import keychain

openai_key = keychain.openai_key

iterative = False # Set to False to make blank new requests every time

temperature = 0.4 # The higher the temperature, the more random the text. Between 0 and 1 is recommended.

board_type = "Arduino Leonardo" # Change to your board type
board_config = "A potentiometer is connected to analog pin A0. A flex sensor connected to analog pin A1. A photoresistor is connected to analog pin A2. A button is connected to pin 3: the pin reads HIGH when the button is pressed. A piezoelectric speaker is connected to pin 8: don't use external libraries to play sounds on this speaker. A servomotor is connected to pin 10. A yellow LED is connected to pin 11, a green LED to pin 12, and a red LED to pin 13."
system_prompt = f"You are assisting a human with writing Arduino code. The Arduino is a {board_type}. You always have to output complete arduino code without additional text. Don't reply with anything but the code itself. Don't talk to the user directly, don't explain your code, just output the code itself. This is the request from the user:\n"
