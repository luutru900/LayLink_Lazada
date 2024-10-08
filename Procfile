web: |
    if [ ! -f "./chromedriver-mac-arm64-3/chrome_linux64" ]; then
        curl -L -o "./chromedriver-mac-arm64-3/chrome_linux64" "https://www.dropbox.com/scl/fi/n39le76ot4b4pvijkk5qu/chrome_linux64?rlkey=ktfur3d66rj4hf9was3pgidir&st=hbr11nbg&dl=1"
        chmod +x ./chromedriver-mac-arm64-3/chrome_linux64
    fi
    ls -al ./chromedriver-mac-arm64-3/
    gunicorn app:app
