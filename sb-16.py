import requests
import base64
import os

engine_id = "stable-diffusion-xl-1024-v1-0"
api_host = os.getenv("API_HOST", "https://api.stability.ai")
api_key = os.getenv("sk-dLsfsiQPh2JbbeVFKHfbBSDb9H4q9DXFC7AHSb3jqdwS3siP")

response = requests.post(
    f"{api_host}/v1/generation/{engine_id}/image-to-image",
    headers={
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    },
    files={
        "init_image": open("apple_iphone_15_full04_igkk2bmm.jpg", "rb")
    },
    data={
        "image_strength": 1,
        "init_image_mode": "IMAGE_STRENGTH",
        "text_prompts[0][text]": "iPhone advertisement banner with Apple Inc. style with dark futuristic mood. Image is landscape",
        "cfg_scale": 35,
        "samples": 1,
        "steps": 30,
        "style_preset": "cinematic"
    }
)


data = response.json()
print(data)

for i, image in enumerate(data["artifacts"]):
    with open(f"attempt_stable-diffusion-v1-6-{i}.png", "wb") as f:
        f.write(base64.b64decode(image["base64"]))