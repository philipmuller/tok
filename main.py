import pyaudio, wave
import threading, keyboard, os, sys
import openai

import config # This file contains the openai api key and board configuration
import json

# Audio refording parameters
chunk = 512
sample_format = pyaudio.paInt16
channels = 1
rate = 44100
frames = []
recording = False

openai.api_key = config.openai_key
openai.Model.list()

# This function records audio from the microphone
def record():
    global frames, recording
    p = pyaudio.PyAudio()

    stream = p.open(format=sample_format, channels=channels, rate=rate, frames_per_buffer=chunk, input=True)
    frames = []
    recording = True

    while recording:
        data = stream.read(chunk, exception_on_overflow = False)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

# This function listens for keyboard input
def listen():
    global recording
    while True:
        if keyboard.is_pressed('r'):
            print('Recording...')

            # Calling the record function on a different thread
            record_thread = threading.Thread(target=record) 
            record_thread.start()

            while keyboard.is_pressed('r'):
                pass

            recording = False
            record_thread.join()
            print('Recording stopped.')
            save_to_file()
        if keyboard.is_pressed('q'):
            break

# Define the function to save the recorded audio to a file
def save_to_file():
    global frames
    p = pyaudio.PyAudio()
    file_name = 'recording.wav'
    file_path = os.path.join(os.getcwd(), file_name)
    wf = wave.open(file_path, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()
    print(f'Recording saved to {file_name}')
    create_transcription()

def create_transcription():
    audio_file = open("recording.wav", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    text = transcript["text"]
    print(text)
    if config.iterative:
        generate_arduino_code_test(text)
    else:
        generate_arduino_code(text)

def generate_arduino_code(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=config.temperature,
        messages=[
        {"role": "system", "content": "You are assisting a human with writing Arduino code. The Arduino is a Arduino Leonardo. You always have to output complete arduino code without additional text. Don't reply with anything but the code itself. Don't talk to the user directly, don't explain your code, just output the code itself. This is the request from the user:"},
        {"role": "user", "content": prompt}
        ],
    )
    print(response)
    choices = response["choices"]
    if len(choices) > 0:
        choice = choices[0]
        message = choice["message"]
        content = message["content"]
        print(content)
        write_to_arduino_file(content)

def generate_arduino_code_test(prompt):
    history_file = "context/conversation_history.json"

    # Load conversation history from the file if it exists
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            conversation_history = json.load(f)
    else:
        conversation_history = []

    messages = [
        {"role": "system", "content": f"{config.system_prompt}"}]

    # Add the previous user and assistant messages to the messages array
    for message in conversation_history:
        messages.append(message)

    # Add the user prompt to the messages array
    user_message = {"role": "user", "content": prompt}
    messages.append({"role": "user", "content": prompt})
    conversation_history.append(user_message)

    # Clear history
    if "clear history" in user_message["content"].lower():
        conversation_history = []
        with open(history_file, "w") as f:
            json.dump(conversation_history, f)
        sys.exit("Conversation history cleared.")


    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature=config.temperature,
    messages=messages
    )
    print(response)
    choices = response["choices"]
    if len(choices) > 0:
        choice = choices[0]
        message = choice["message"]
        content = message["content"]
        print(content)
        conversation_history.append(message)

    try:
        with open(history_file, "w") as f:
            print("opening history file")
            json.dump(conversation_history, f)
            f.close()
    except Exception as e:
        print("Error writing to history file:", e)

    write_to_arduino_file(content)

def write_to_arduino_file(content):
    print(content)
    f = open("arduino_code/arduino_code.ino", "w")

    f.write(process_gpt_output(content))
    f.close()
    print("Saved new arduino file!")
    sys.exit("Generation ended")
    run_arduino_code()

def process_gpt_output(output):
    substrings = output.split("```")
    if len(substrings) > 1:
        output = substrings[1]
    print(output)
    #content.strip('\n\n```').strip("c++").strip("C++").strip("arduino").strip("Arduino")
    return output

def run_arduino_code():
    os.system("sudo arduino-cli compile --fqbn arduino:avr:leonardo arduino_code")
    os.system("sudo arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:leonardo arduino_code")

# Start the keyboard listener
listen()
