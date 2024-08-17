# **Teapot - Tetris Bot for Tetr.io**  

![Add a heading](https://github.com/user-attachments/assets/4f3e2201-7483-4661-b5a4-2afffa4bc00d)
---

## ⚡ **Features**
- **Blazingly Fast**: Searches for best moves with heuristic evaluation.
- **Customizable Playstyle**: Adjust the bot's behavior with simple edits in `heuristics.py`.
- **Resolution Support**: Currently supports 1920x1080 and 2560x1440 resolutions.
- **Easy Integration**: Apply the custom skin (`skin.png`) via [Tetr.io Plus](https://gitlab.com/UniQMG/tetrio-plus).


## 🎥 **Video Demo**

[![Watch the demo](http://img.youtube.com/vi/Bm9AEgAsgc8/0.jpg)](https://www.youtube.com/watch?v=Bm9AEgAsgc8 "Teapot Bot Demo")

## 📦 **Setup Guide**
1. **Download and Apply Skin**  
   - Download the included skin (`skin.png`) and apply it using [Tetr.io Plus](https://gitlab.com/UniQMG/tetrio-plus).

2. **Adjust Resolution**  
   - Modify the flag in `detect.py` to match your screen resolution. Supported resolutions are:
     - 1920x1080
     - 2560x1440

3. **Configure Tetr.io Settings**  
   - Set the following gameplay configurations:
     - **Board Zoom**: 130%
     - **Shadow Visibility**: 0%
     - **Board Bounciness**: 0%

4. **Optimize Particle Effects**  
   - Replace the following particle effects with transparent files (`empty.png`) through Tetr.io Plus:
     - `particle_beam`
     - `particle_beams_beam`
     - `particle_chirp`
     - `particle_star`

   This ensures that the bot does not misinterpret particle effects as unknown blocks.

## 🛠 **Customization**
The bot's behavior is controlled by the values in `heuristics.py`. These values are placeholders but generally stable for testing. If you discover stronger values or optimizations, your contributions are welcome!

## 💬 **Contact & Contributions**
Found a bug? Have suggestions? Want to contribute?  
Reach out via Discord: **`astrangepotato`**
