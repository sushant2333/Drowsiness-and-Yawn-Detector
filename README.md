# Drowsiness & Yawning Detector  

A real-time monitoring system that detects **drowsiness (eye closure)**, **yawning**, and **blinking** using **MediaPipe Face Mesh** and **OpenCV**.  
If drowsiness or yawning is detected, an **alert sound** is played to help keep the user awake.  

---

## 🚀 Features  
- Real-time **eye aspect ratio (EAR)** calculation → detects drowsiness & blinks.  
- Real-time **mouth aspect ratio (MAR)** calculation → detects yawns.  
- Plays an alert sound when drowsiness or yawning is detected.  
- Tracks blink count and yawn count.  
- Displays EAR, MAR, blinks, and yawns on the video feed.  
- Colored bounding box:
  - 🟩 Green → Normal  
  - 🟥 Red → Drowsy  
  - 🟨 Yellow → Yawning  

---

## 📂 Project Structure  
```
Drowsiness-Yawning-Detector/
│── app.py                # Main script
│── AlertSound.wav         # Alert sound file (provide your own)
│── requirements.txt       # Dependencies
│── README.md              # Documentation
│── .gitignore             # Ignore venv and temp files
│── .venv/ (optional)      # Virtual environment (not tracked by Git)
```


---

## ⚙️ Installation  

### 1. Clone the repository  
```bash
git clone https://github.com/your-username/drowsiness-yawning-detector.git
cd drowsiness-yawning-detector
```

### 2. Create and activate a virtual environment (recommended)
```bash
python -m venv .venv
```
- Activate (Linux/macOS):
  ```bash
  source .venv/bin/activate
  ```
- Activate (Windows):
  ```bash
  .venv\Scripts\activate
  ```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
---

## ▶️ Usage

Run the script:
```bash
python app.py
```

- Press ESC to quit the program.
- Make sure you have a valid ```AlertSound.wav``` file in the project folder.

---

## 🔧 Parameters & Thresholds

Defined in ```main.py```:

- EAR_THRESHOLD = 0.22 → Eye closure threshold.
- MAR_THRESHOLD = 0.65 → Yawn threshold.
- CONSEC_FRAMES = 30 → Frames eyes must remain closed before drowsiness is triggered.
- YAWN_FRAMES = 15 → Frames mouth must remain open before a yawn is counted.

You can adjust these values depending on your needs.

---

## 📊 Example Output

Status: Normal / Drowsy / Yawning

- EAR / MAR values
- Blink count
- Yawn count

Video window will show a bounding box around your face with color-coded status.

---

## 📜 License

MIT License. Feel free to use, modify, and distribute.

