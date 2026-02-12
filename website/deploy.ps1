# Deploy script for benchmarks.edtechquality.ai
# Usage: powershell -File website/deploy.ps1

$ErrorActionPreference = "Stop"

$SERVER = "root@157.245.0.32"
$REMOTE_DIR = "/var/www/benchmarks"
$SCRIPT_DIR = $PSScriptRoot
$BUILD_DIR = "$SCRIPT_DIR\build"
$TAR_FILE = "$SCRIPT_DIR\build.tar"

Write-Host "`n=== Building site ===" -ForegroundColor Cyan
Push-Location $SCRIPT_DIR
npm run build
Pop-Location

if (-not (Test-Path "$BUILD_DIR\index.html")) {
    Write-Host "ERROR: Build failed - no index.html found" -ForegroundColor Red
    exit 1
}

Write-Host "`n=== Packaging build ===" -ForegroundColor Cyan
tar -cf $TAR_FILE -C $BUILD_DIR .

Write-Host "`n=== Uploading to server ===" -ForegroundColor Cyan
scp $TAR_FILE "${SERVER}:/var/www/build.tar"

Write-Host "`n=== Deploying on server ===" -ForegroundColor Cyan
ssh $SERVER "rm -rf $REMOTE_DIR/*; tar -xf /var/www/build.tar -C $REMOTE_DIR/; rm /var/www/build.tar; chown -R www-data:www-data $REMOTE_DIR"

# Clean up local tar
Remove-Item $TAR_FILE -ErrorAction SilentlyContinue

Write-Host "`n=== Deploy complete! ===" -ForegroundColor Green
Write-Host "Site live at: https://benchmarks.edtechquality.ai`n"
