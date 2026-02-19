import time
import json
import requests

# When you deploy your backend to Railway, replace this with the live URL
API_URL = "http://localhost:8000/api/next"
POLL_INTERVAL = 30  # seconds

def render(pixels):
    """
    pixels is a list of 1024 [R, G, B] values.
    For now we just print them — we'll swap this for real LED code once you have the matrix.
    """
    print(f"Rendering {len(pixels)} pixels to display...")
    # TODO: replace with rpi-rgb-led-matrix calls

def show_default():
    """Display something when the queue is empty."""
    print("Queue empty — showing default image")
    # TODO: render a default pattern

def poll():
    print("Pi polling script started...")
    while True:
        try:
            response = requests.get(API_URL, timeout=10)
            data = response.json()

            if data["pixels"] is None:
                show_default()
            else:
                render(data["pixels"])

        except Exception as e:
            # If the server is unreachable, log it and keep going
            # Like a ranger who finds the notice board knocked over — just try again later
            print(f"Failed to reach server: {e}")

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    poll()
