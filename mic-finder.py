#Please run this script and find your mic and find its index:

import speech_recognition as sr

# List all available microphone names and their indices
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"Microphone with name \"{name}\" found for `device_index={index}`")