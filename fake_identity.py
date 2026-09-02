from faker import Faker
import random
import requests
from io import BytesIO
from PIL import Image

fake = Faker(['de_DE'])

ZODIAC_SIGNS = [
    "Aries","Taurus","Gemini","Cancer","Leo","Virgo",
    "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"
]

def generate_identity(country='Germany', gender=None, min_age=18, max_age=60):
    name = fake.name_female() if (gender and gender.lower().startswith('f')) else fake.name()
    dob = fake.date_of_birth(minimum_age=min_age, maximum_age=max_age)
    
    age = 2025 - dob.year

    profile = {
        'Name': name,
        'Gender': 'Female' if (gender and gender.lower().startswith('f')) else 'Not specified',
        'Age': age,
        'DateOfBirth': dob.isoformat(),
        'Occupation': fake.job(),
        'Address': fake.street_address(),
        'PostalCode': fake.postcode(),
        'State': fake.state(),
        'Country': country,
        'Email': fake.safe_email(),
        'Phone': fake.phone_number(),
        'MaritalStatus': random.choice(['Single','Married','Divorced']),
        'BloodType': random.choice(['A+','A-','B+','B-','O+','O-','AB+','AB-']),
        'Height_ft': round(random.uniform(4.8,6.2), 2),
        'Weight_lb': round(random.uniform(110,200), 2),
        'Zodiac': random.choice(ZODIAC_SIGNS),
    }

    return profile


def build_ai_face_prompt(identity):
    """Identity → Realistic Human Face Prompt"""

    prompt = f"""
Ultra-realistic portrait photo of a {identity['Age']}-year-old {identity['Gender'].lower()},
European ethnicity, German facial structure,
natural skin texture, soft lighting, DSLR quality,
profession: {identity['Occupation']},
neutral background, detailed eyes, realistic hair,
cinematic portrait, 8k, hyper-real photograph.
"""
    return prompt


# ---------------- AI IMAGE GENERATOR (Stable Diffusion WebUI Example) -----------------

def generate_image(prompt):
    url = "http://127.0.0.1:7860/sdapi/v1/txt2img"  # if using AUTOMATIC1111 Stable Diffusion
    payload = {
        "prompt": prompt,
        "steps": 30,
        "cfg_scale": 7,
        "width": 768,
        "height": 1024
    }

    response = requests.post(url, json=payload).json()
    image_base64 = response['images'][0]

    import base64
    img_data = base64.b64decode(image_base64)
    img = Image.open(BytesIO(img_data))
    img.save("ai_generated_identity_face.png")

    print("\nImage saved as: ai_generated_identity_face.png")


# ---------------- MAIN -----------------

identity = generate_identity(gender='Female', min_age=18, max_age=29)

print("=== GENERATED FAKE IDENTITY ===\n")
for k, v in identity.items():
    print(f"{k}: {v}")

prompt = build_ai_face_prompt(identity)

print("\n=== IMAGE PROMPT ===\n")
print(prompt)

# Generate Image
generate_image(prompt)
