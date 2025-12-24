import speech_recognition as sr


# Create a Recognizer object
r = sr.Recognizer()

# # Use the microphone as the audio source
# with sr.Microphone() as source:
#     print("Say something!")
#     # Adjust for ambient noise
#     r.adjust_for_ambient_noise(source)
    # Listen for audio for more.... sentence                        
    # audio = r.listen(source)
with sr.Microphone() as source:
    print("Speak your full sentence...")
    r.adjust_for_ambient_noise(source, duration=1)
    r.energy_threshold = 300  # Optional: tweak if needed
    audio = r.listen(source, phrase_time_limit=15)  # up to 15-sec speech

3

try:
    # Recognize speech using Google Speech Recognition
    text = r.recognize_google(audio)
    print(f"You said: {text}")
except sr.UnknownValueError:
    print("Could not understand audio")
except sr.RequestError as e:
    print(f"Could not request results from Google Speech Recognition service; {e}")