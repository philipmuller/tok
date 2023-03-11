# Tok
The Tok board is a prototyping board that you can talk to, designed for tinkering and rapid iteration.

## Upload generated file to board
```
arduino-cli compile -b arduino:avr:leonardo arduino_code --verbose
arduino-cli upload -b arduino:avr:leonardo -p /dev/tty.usbmodem143401 arduino_code --verbose
```