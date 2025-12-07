from scripts import IPAupdates, crypticPuz
import os
from dotenv import load_dotenv

load_dotenv()
IPAwebhook = os.getenv("IPA_WEBHOOK")
CROSSWORDwebhook = os.getenv("CROSSWORD_WEBHOOK")

# Check for IPA Updates for my sideloaded apps
try:
    IPAupdates.IPAupdates(IPAwebhook)
    print("IPA updates check complete.")
except Exception as e:
    print(f"Error checking IPA updates: {e}")

# Scrape and convert latest Lovatts Cryptic Crossword
try:
    crypticPuz.crypticPuz(CROSSWORDwebhook)
    print("Cryptic crossword fetch complete.")
except Exception as e:
    print(f"Error fetching cryptic crossword: {e}")