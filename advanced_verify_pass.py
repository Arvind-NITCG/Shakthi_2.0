import os
import time
import numpy as np
import sounddevice as sd
import soundfile as sf
from resemblyzer import VoiceEncoder, preprocess_wav

fs = 44100
duration = 4
threshold = 0.78 #hardcoded here

print("Loading Shakthi engine")
encoder = VoiceEncoder()
#finding the path
def get_app_data_path():
    current = os.path.dirname(os.path.abspath(__file__))
    data = os.path.join(current,"master_voice.npy")
    return data
#authenticate user this is a boolean datatype...
def authenticate_user():
    print("\n"+"="*40)
    print("   🔒 SHAKTHI 2.0 - SECURITY CHECK")
    print("="*40)
    profile = get_app_data_path()
    #profile = os.path.join(data,"master_voice.npy")
    if not os.path.exists(profile):
        print("Mater voice not found to compare and run advanced_record.py first")
        return False
    try:
        master = np.load(profile)
        print("compariosn voice loaded")
    except Exception as e:
        print(f"No Corrupted profile {e}")
        return False
    print("Listening please say")
    try:
        rec = sd.rec(int(duration*fs),samplerate=fs,channels=1)
        sd.wait()
        print("Captured")
        temp_file = "temp_verify.wav"
        sf.write(temp_file,rec,fs)
        print("File is saved")
        #call the embeddings clean and run the brain LSTM
        wav = preprocess_wav(temp_file)
        final_embedding = encoder.embed_utterance(wav)

        #remove the unwanted now
        os.remove(temp_file)

        #calculate similarity that is the dot product
        similarity = np.inner(final_embedding,master)
        print(f"    Identity Match: {similarity:.3f} (Req: {threshold})")
        if similarity > threshold :
            print("Authentification complete. Welcome back Boss!")
            return True
        else:
            print("Wrong user no dont enter you imposter!")
            return False
    except Exception as e:
        print(f"System error {e}")
        return False
if __name__=="__main__":
    authenticate_user()




    

