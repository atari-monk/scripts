$clientPath = "C:\atari-monk\code\micro-engine\football_multi_desktop"
cd $clientPath
npm run build
cd 'build'
.\serve.py
