import os
import io
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

# Our Host URL should not be prepended with "https" nor should it have a trailing slash.
os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'

# Sign up for an account at the following link to get an API Key.
# https://platform.stability.ai/

# Click on the following link once you have created an account to be taken to your API Key.
# https://platform.stability.ai/account/keys

# Paste your API Key below.

os.environ['STABILITY_KEY'] = 'sk-dLsfsiQPh2JbbeVFKHfbBSDb9H4q9DXFC7AHSb3jqdwS3siP'

# # Set up our connection to the API.
stability_api = client.StabilityInference(
    key=os.environ['STABILITY_KEY'], # API Key reference.
    verbose=True, # Print debug messages.
    engine="stable-diffusion-xl-1024-v1-0", # Set the engine to use for generation.
    # Check out the following link for a list of available engines: https://platform.stability.ai/docs/features/api-parameters#engine
)


with Image.open("apple_iphone_15_full04_igkk2bmm.jpg") as im:
	answers2 = stability_api.generate(
		style_preset="cinematic",
		adapter_strength=1.0,
    prompt="iPhone advertisement banner with futuristic mood. Phone is iPhone 14. Show the phone's back camera lens",
    # init_image=im, # Assign our previously generated img as our Initial Image for transformation.
    # seed=121245125, # If attempting to transform an image that was previously generated with our API,
                    # initial images benefit from having their own distinct seed rather than using the seed of the original image generation.
    steps=100, # Amount of inference steps performed on image generation. Defaults to 30.
    cfg_scale=35.0, # Influences how strongly your generation is guided to match your prompt.
                   # Setting this value higher increases the strength in which it tries to match your prompt.
                   # Defaults to 7.0 if not specified.
    width=1152, # Generation width, defaults to 512 if not included.
    height=896, # Generation height, defaults to 512 if not included.
    sampler=generation.SAMPLER_K_DPMPP_2M # Choose which sampler we want to denoise our generation with.
                                                 # Defaults to k_dpmpp_2m if not specified. Clip Guidance only supports ancestral samplers.
                                                 # (Available Samplers: ddim, plms, k_euler, k_euler_ancestral, k_heun, k_dpm_2, k_dpm_2_ancestral, k_dpmpp_2s_ancestral, k_lms, k_dpmpp_2m, k_dpmpp_sde)
	)

	for resp in answers2:
		for artifact in resp.artifacts:
			if artifact.finish_reason == generation.FILTER:
				warnings.warn("Your request activated the API's safety filters and could not be processed. Please modify the prompt and try again.")
			if artifact.type == generation.ARTIFACT_IMAGE:
				global img
				img = Image.open(io.BytesIO(artifact.binary))
				img.save(str(artifact.seed) + ".png")

	# for resp in answers2:
	# 	for artifact in resp.artifacts:
	# 		if artifact.finish_reason == generation.FILTER:
	# 			warnings.warn("Your request activated the API's safety filters and could not be processed. Please modify the prompt and try again.")
	# 			if artifact.type == generation.ARTIFACT_IMAGE:
	# 				global img
	# 				img = Image.open(io.BytesIO(artifact.binary))
	# 				img.save(str(artifact.seed)+ ".png")