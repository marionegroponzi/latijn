# latijn

Bot name: IlmariLatijnBot
Username: IlmariLatijnBot

TOKEN: in the telegram_token.py file (git-ignored)


## Howto run

`uv run main.py`

### Install uv

`curl -LsSf https://astral.sh/uv/install.sh | sh`

### Show service errors

`log show --predicate 'process == "launchd"' --info --last 1h`

```
sudo launchctl bootout system /Library/LaunchDaemons/com.negroponzi.latijn.plist
sudo launchctl bootstrap system /Library/LaunchDaemons/com.negroponzi.latijn.plist
```
