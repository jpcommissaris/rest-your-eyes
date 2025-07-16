# Rest Your Eyes

**Rest Your Eyes** is a macOS menu bar application designed to remind you to take regular breaks and rest your eyes. This app helps promote better eye health and productivity by encouraging you to follow the 20-20-20 rule.

## Usage
- Download the app from ___. Or dev & build your own version.
- Allow the app in "focus" mode to make sure you see notifications
- IMPORTANT: Make sure in system settings, you give this app permission to send banner notifications. Enable sound. Set "show previews" to "always"

## Development

### Running in Development Mode
To run the app in development mode, use the `main.py` script:

- Python 3.x
- Add venv (recommended): `python3 -m venv venv`
- `source venv/bin/activate`
- Required dependencies (install via `pip`):
  ```bash
  pip install -r requirements.txt
  ```

```bash
python src/main.py
```

### Bundling the App
- The app is bundled for distribution with`setup.py` & `codesign`. This will package the application for macOS. Use the provided build script:
- `chmod +x build.sh`
- `./build.sh`



## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---  
Stay healthy and take regular breaks with **Rest Your Eyes**!  


## Roadmap ideas:
- Full window display (overlay) when timer runs out
- Setting (preferences) window to change time