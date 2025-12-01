# ⚛️ Shakthi 2.0 - AI Biometric Gatekeeper

> "Identity Verification Required."

**Shakthi 2.0** is a military-grade AI authentication system for Windows. It secures your workstation by locking hardware inputs (Mouse & Keyboard) and requires **Biometric Voice Authentication** to unlock.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

## ✨ Features
* **🛡️ Kernel-Level Lockdown:** Blocks `Alt+F4`, `Win`, `Tab`, and suppresses Mouse inputs completely.
* **🗣️ AI Voice Security:** Uses Deep Learning (Resemblyzer) to verify speaker identity against a stored voice print.
* **⚛️ Arc Reactor UI:** A pulsing, sci-fi visual interface built with Tkinter.
* **👻 Ghost Mode:** Plays your favourite song in the background upon success.
* **⚡ Asynchronous Core:** Threaded audio engine ensures the UI never freezes.

---

## 🛠️ Installation

1. **Clone the Repository**
   ```bash
   git clone [https://github.com/Arvind-NITCG/Shakthi_2.0.git](https://github.com/Arvind-NITCG/Shakthi_2.0.git)
   cd Shakthi_2.0
   ```
2. **Install Dependencies**
    Make sure you have Python installed. Then run:
    ```bash
     pip install -r requirements.txt
     ```

# Configuration(First Time Setup)
  Before locking your system, you must train Shakthi to recognize YOU.

1. **Create Your Voice Print 🎙️**
  Run the recording script to generate your biometric ID.
  ```bash
    python record.py
    ```
  Follow on screen prompts and this would generate a file named master_voice.npy carrying your voice data
2. **Set Your Security PIN 🔑**
   Open the main file (GUI_Voice_auth_pro.py) in any text editor. Look for the comment "User Configuration" at the top and update your PIN and choose the local path to your favourite song to be played on successfull verification..
3. **Update the cost threshold if required**
   The threshold is maintained as 0.78 and it is a similarity score between your live voice and the predefined voice in the master_voice.npy . If you want the system to be more strict keep the score any value between 0.75 to 0.80 . I have hardcoded it to 0.78 . You can analyse this by running the advanced_verify_pass.py , and the compatable threshold could be fixed for best personal experience.

# ⚠️ Emergency Override
 If your voice is not recognized (e.g., noisy environment):

 1. Wait for the voice attempts to fail.
 2. Shakthi will ask for a PIN.
 3. Type your configured PIN and press ENTER. (Note: The mouse will be dead, but keyboard input will still work for the PIN box).

# 🤝 Contributing
 Feel free to fork this repo and submit Pull Requests!

# How to run
 Well for Shakthi_2.0 to act like a guard to your system you will require it to be a standalone application. In windows environement this could be done via pyinstaller
**Command:**
 ```bash
  pyinstaller --onefile --collect-all resemblyzer --add-data "master_voice.npy;." --name="Shakthi_2.0" GUI_Voice_auth_pro.py
 ```
**Setup the Environment**
  Go to the dist folder created by the build command. Crucial: You must Copy & Paste your master_voice.npy file into this folder, right next to the Shakthi_2.0.exe.

# Automate (Task Scheduler)
 To have Shakthi lock your PC on startup:

 1. Open Windows Task Scheduler.
 2. Create a new task and check "Run with highest privileges".
 3. Set Trigger: "At Log on".
 4. Set Action: Start Shakthi_2.0.exe.

 Important: In the "Start in (Optional)" box, paste the path to your dist folder so the app can find your voice file.

 


