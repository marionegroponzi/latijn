# Make sure the user is an admin
PrivilegesCLI -a

# Replace the text Environment.development with Environment.production in the file ../lib/config.dart
sed -i '' 's/IS_PRODUCTION = False/IS_PRODUCTION = True/g' ./bot_config.py

# Stop daemon
sudo launchctl stop com.negroponzi.latijn && echo "Stopped latijn daemon"
sudo launchctl remove com.negroponzi.latijn && echo "Removed latijn daemon"

# Remove old files
sudo rm -rf /opt/latijn && echo "Removed old latijn files"
sudo rm -f /Library/LaunchDaemons/com.negroponzi.latijn.plist && echo "Removed old latijn plist"

# Copy files
sudo mkdir -p /opt/latijn
sudo rm latijn_*.json
sudo rm question_*.json
sudo cp -fpR * /opt/latijn && echo "Deployed"

# Install daemons
sudo cp assets/com.negroponzi.latijn.plist /Library/LaunchDaemons/ && echo "Registered latijn agent"
sudo chown root:wheel /Library/LaunchDaemons/com.negroponzi.latijn.plist && echo "Changed ownership to root:wheel"

# Ensure folder structure exists
sudo mkdir -p /opt/latijn/log && echo "Created log directory"

# Ensure correct permissions
sudo chown -R $(whoami) /opt/latijn && echo "Changed ownership to $(whoami)"

# Remove old logs
# if file exists, remove it
if [ -f log/error.log ]; then
    sudo rm /opt/latijn/log/error.log
    echo "Removed error log"
fi
if [ -f log/output.log ]; then
    sudo rm /opt/latijn/log/output.log
    "Removed output log"
fi

# Restart daemons
sudo launchctl load /Library/LaunchDaemons/com.negroponzi.latijn.plist
sudo launchctl start com.negroponzi.latijn && echo "Started latijn agent"
sleep 1
log show --predicate 'process == "launchd"' --info --last 5m | grep com.negroponzi.latijn
# Check if the agent is running
if sudo launchctl list | grep latijn > /dev/null; then
    echo ">>> latijn agent is running <<<"
else
    echo ">>> latijn agent is NOT running <<<"
fi

echo "=== output.log ===" && cat /opt/latijn/log/output.log
echo "=== error.log ===" && cat /opt/latijn/log/error.log


# Reset the config file
sed -i '' 's/IS_PRODUCTION = True/IS_PRODUCTION = False/g' ./bot_config.py

# Tag the repo with the current UTC date and time
git tag "deploy-$(date -u +'%Y%m%d-%H%M%S')"
git push --tags