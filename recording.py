# importing all the packages required
import os
import sounddevice as sd
import numpy as np
import time
import soundfile as sf
from resemblyzer import VoiceEncoder,preprocess_wav
from pathlib import Path

#configuration
fs = 44000
duration = 4
sample_count = 3

print("Load the brain..please wait as it takes time..we are building a three layer LSTM and now take it from the hardisk")
encoder = VoiceEncoder()
# Folderr definition
def get_app_data_path():
    current = os.path.dirname(os.path.abspath(__file__))
    return current
# =============================================
# Shakthi 2.0 - VOICE ENROLLMENT
# print("="*40)

def enroll_user():
    print("We will record 3 samples to learn your voice.")
    print("speak naturally.You can say anything we just study your voice patterns not what you say!")
    embeddings = [] #list to store 3 d-vectors
    for i in range(sample_count):
        input(f"Press ENTER to record sample {i+1}/{sample_count}...")
        print("Recording HAS STARTED...SPEAK NOW!")
        #record logic 
        try:
            rec = sd.rec(int(duration*fs),samplerate=fs,channels=1)
            sd.wait() #pause the program counter untill recording is completed
        except Exception as e:
            print(f"Mic ERROR: {e}")
            return
        print("CAPTURED YOUR VOICE NOW PROCESSING!")
        # Save the file
        file = f"temp_sample_{i}.wav"
        sf.write(file,rec,fs)
        print("File is saved successfully")
        # AI step begins
        wav = preprocess_wav(file)
        encoded = encoder.embed_utterance(wav)
        embeddings.append(encoded)
        print(f"Vector{i} is stored in embeddings")
        #clean the temporary file
        os.remove(file)
        time.sleep(0.5)
    print("Embeddings are found now obtaining the centeroid")
    matrix = np.array(embeddings)
    final_d_vector = np.mean(matrix,axis = 0)
    final_d_vector = final_d_vector/np.linalg.norm(final_d_vector)
    print("Saving the final result")
    
    save_dir=get_app_data_path()
    save_path=os.path.join(save_dir,"master_voice.npy")
    np.save(save_path,final_d_vector)
    print("SUCCESS!VOICE IDENTITY HAS BENN SAVED")
    print(f"AT LOCATION:{save_path}")
    print("you can now run the advanced_verify_pass.py to test it")

if __name__=="__main__":
     enroll_user()
     







