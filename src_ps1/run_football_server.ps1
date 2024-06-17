$path = "C:\atari-monk\code\micro-engine\server\build"
cd $path
node index.js | ForEach-Object {
    $_
    $host.ui.RawUI.WindowTitle = 'Football Server'
    } 
