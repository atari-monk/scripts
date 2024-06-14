$path = "C:\atari-monk\code\micro-engine\server"
cd $path
npm run build
cd 'build'
node index.js | ForEach-Object {
    $_
    $host.ui.RawUI.WindowTitle = 'Football Server'
    } 
