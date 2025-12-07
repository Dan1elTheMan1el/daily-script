from scripts import IPAupdates, crypticPuz

# Check for IPA Updates for my sideloaded apps
try:
    IPAupdates()
    print("IPA updates check complete.")
except Exception as e:
    print(f"Error checking IPA updates: {e}")

# Scrape and convert latest Lovatts Cryptic Crossword
try:
    crypticPuz()
    print("Cryptic crossword fetch complete.")
except Exception as e:
    print(f"Error fetching cryptic crossword: {e}")