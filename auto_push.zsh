#!/bin/zsh

# Navigate to your project directory
cd /Users/kshimberg/AppTracker

# Verify the remote URL
REMOTE_URL=$(git remote get-url origin)
EXPECTED_URL="https://github.com/kyleshim/LocalAppTracker.git"

if [[ "$REMOTE_URL" != "$EXPECTED_URL" ]]; then
  echo "Remote URL does not match the expected URL. Please check your configuration."
  exit 1
fi

# Add changes to git
git add .

# Commit changes with a message including the current date and time
git commit -m "Automated commit on $(date)"

# Push changes to the remote repository
git push origin main