import pyaudio, wave
import threading, keyboard, os, sys
import openai

import config # This file contains the openai api key and board configuration

# Audio refording parameters
chunk = 1024
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
    generate_arduino_code(text)

def generate_arduino_code(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.4,
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
    
def write_to_arduino_file(content):
    print(content)
    f = open("arduino_code/arduino_code.ino", "w")

    f.write(process_gpt_output(content))
    f.close()
    print("Saved new arduino file!")
    sys.exit("Generation ended")
    #run_arduino_code()

def process_gpt_output(output):
    substrings = output.split("```")
    if len(substrings) > 1:
        output = substrings[1]
    print(output)
    #content.strip('\n\n```').strip("c++").strip("C++").strip("arduino").strip("Arduino")
    return output

# Start the keyboard listener
listen()