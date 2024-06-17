#$editorPath = "C:\atari-monk\code\notes_app\editor\build\index.html"
$readerPath = "C:\atari-monk\code\notes_app\reader\build\index.html"
$serverPath = "C:\atari-monk\code\notes_app\server\build\server.js"

# if (Test-Path $editorPath -PathType Leaf) {
#     Start-Process $editorPath
# }
# else {
#     Write-Host "The editor file does not exist: $editorPath"
# }

if (Test-Path $readerPath -PathType Leaf) {
    Start-Process $readerPath
    Start-Process $readerPath
}
else {
    Write-Host "The reader file does not exist: $readerPath"
}

if (Test-Path $serverPath -PathType Leaf) {
    node $serverPath | ForEach-Object {
        $_
        $host.ui.RawUI.WindowTitle = 'Notes Server'
    }
}
else {
    Write-Host "The server file does not exist: $serverPath"
}