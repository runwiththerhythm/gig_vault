import os

os.environ.setdefault(
    "DATABASE_URL", "postgresql://neondb_owner:npg_UoOqbRAv0i3k@ep-winter-hall-a2qqbwxl.eu-central-1.aws.neon.tech/ouch_crook_flint_60528")

os.environ.setdefault("SECRET_KEY", "jb6h7ds6hb3hfb4kd7snm3bdjsiuem9d")   

os.environ.setdefault(
    "CLOUDINARY_URL", "cloudinary://<your_api_key>:<your_api_secret>@dxhvr1vqk")

os.environ["MAPBOX_TOKEN"] = "pk.eyJ1Ijoia2Vybm93d2F5IiwiYSI6ImNtZHhoYXZkMDBieXIyb3Izdno3aDdseXMifQ.Hj7D-gE0O8LwrfavTTPWSg"