import requests
from dotenv import load_dotenv
import json
import os

load_dotenv()

IPAwebhook = os.getenv("IPA_WEBHOOK")
IPAupdates = json.load(open("data/IPAupdates.json"))
repoCache = {}
for app in IPAupdates:
    if app["ignore"] == "Yes":
        continue
    
    if app['repoURL'] in repoCache:
        repoJSON = repoCache[app['repoURL']]
    else:
        repoJSON = requests.get(app['repoURL']).json()
        repoCache[app['repoURL']] = repoJSON

    for repoApp in repoJSON["apps"]:
        if repoApp["name"] == app["name"] and repoApp["bundleIdentifier"] == app["bundleIdentifier"]:
            if "version" in repoApp:
                latest = repoApp["version"]
                download = repoApp["downloadURL"]
            else:
                latest = repoApp["versions"][0]["version"]
                download = repoApp["versions"][0]["downloadURL"]
            
            # Handle update
            if latest != app["version"]:
                app["version"] = latest

                payload = {
                    "username": "IPA Updates",
                    "avatarURL": "https://raw.githubusercontent.com/Dan1elTheMan1el/IOS-Shortcuts/refs/heads/main/IPA-Updates/icon.png",
                    "embeds": [{
                        "title": app["name"],
                        "description": repoJSON["name"] if "name" in repoJSON else "Unknown Repo",
                        "color": int(repoApp["tintColor"].replace('#', '') if "tintColor" in repoApp else "000000", 16),
                        "thumbnail": {"url": repoApp["iconURL"]},
                        "fields": [
                            {
                                "name": "Version",
                                "value": latest,
                                "inline": True
                            },
                            {
                                "name": "Download",
                                "value": f"[Click Here]({download})",
                                "inline": True
                            }
                        ]
                    }]
                }
                requests.post(IPAwebhook, json=payload)
            
            break   
json.dump(IPAupdates, open("data/IPAupdates.json", "w"), indent=4)
