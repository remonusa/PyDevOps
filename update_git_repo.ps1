# Display current Git status
Write-Host "Checking Git status..."
git status

# Ask the user if they want to add all changes or specify files
$addResponse = Read-Host "Do you want to add all changes? (Y/N)"

if ($addResponse -eq 'Y') {
    # Add all changes
    git add .
} else {
    # Ask for specific files to add
    $filesToAdd = Read-Host "Enter the files you want to add (separated by space)"
    git add $filesToAdd
}

# Commit changes with a message
$commitMessage = Read-Host "Enter your commit message"
git commit -m "$commitMessage"

# Pull latest changes from GitHub
Write-Host "Pulling latest changes from GitHub..."
git pull origin main

# Ask user before pushing to avoid accidental pushes
$pushResponse = Read-Host "Do you want to push your changes to GitHub? (Y/N)"
if ($pushResponse -eq 'Y') {
    # Push changes to GitHub
    Write-Host "Pushing changes to GitHub..."
    git push origin main
    Write-Host "Changes pushed to GitHub successfully."
} else {
    Write-Host "Push to GitHub canceled."
}