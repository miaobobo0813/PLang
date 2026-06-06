Write-Host "PLang Compiler Setup." -ForegroundColor Cyan
Write-Host "Choose an option to continue.`n"
Write-Host "1. Install PLang Compiler."
Write-Host "2. Update PLang Compiler."
Write-Host "3. I'm not ready for installation.`n"

$REINSTALL = $false
$DEVELOPMENT = $true

$choice = Read-Host "Number of options"

switch ($choice) {
    "3" {
        Write-Host "Install has been cancelled." -ForegroundColor Yellow
        exit 0
    }
    "2" {
        Write-Host "Remove old files..."
        if (Test-Path "C:\PLang") {
            Remove-Item "C:\PLang" -Recurse -Force
            $REINSTALL = $true
        } else {
            Write-Host "Error: C:\PLang does not exist. You need to use the install option." -ForegroundColor Red
            exit 0
        }
    }
    "1" {
        if (Test-Path "C:\PLang") {
            Write-Host "Error: C:\PLang exists. You need to use the reinstall option." -ForegroundColor Red
            exit 0
        }
    }
    default {
        Write-Host "Invalid option selected." -ForegroundColor Red
        exit 1
    }
}

New-Item -ItemType Directory -Path "C:\PLang\sources" -Force | Out-Null

Write-Host "Copy files to C:\PLang..."
if ($DEVELOPMENT) {
    Copy-Item -Path ".\sources\*" -Destination "C:\PLang\sources" -Recurse -Force
    Copy-Item -Path ".\plang.bat" -Destination "C:\PLang" -Force
} else {
    Move-Item -Path ".\sources" -Destination "C:\PLang\sources" -Force
    Move-Item -Path ".\plang.bat" -Destination "C:\PLang" -Force
}

if (-not $REINSTALL) {
    Write-Host "Add to PATH..."
    $targetPath = "C:\PLang"
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
    
    if ($currentPath -split ';' -notcontains $targetPath) {
        $newPath = "$currentPath;$targetPath"
        [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
        Write-Host "[SUCCESS] Added $targetPath to User PATH. Please restart your terminal." -ForegroundColor Green
    } else {
        Write-Host "[INFO] $targetPath is already in PATH." -ForegroundColor Yellow
    }
}

Write-Host "`nSetup is done." -ForegroundColor Green
exit 0