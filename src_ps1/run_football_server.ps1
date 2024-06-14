$serverPath = "C:\atari-monk\code\micro-engine\server"
cd $serverPath
npm run build
cd 'build'
node index.js | ForEach-Object {
    $_
    $host.ui.RawUI.WindowTitle = 'Football Server'
    } 
