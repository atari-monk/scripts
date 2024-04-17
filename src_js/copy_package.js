const fs = require('fs')
const path = require('path')

function getPaths(sourceFile, targetDir, debug = false) {
  const dirname = __dirname
  const sourcePath = path.join(dirname, sourceFile)
  const targetPath = path.join(dirname, targetDir, path.basename(sourceFile))

  const paths = {
    dirname,
    sourcePath,
    targetPath,
  }

  if (debug) printPaths(paths)

  return paths
}

function printPaths(paths) {
  console.log('dirname:', paths.dirname)
  console.log('sourcePath:', paths.sourcePath)
  console.log('targetPath:', paths.targetPath)
}

function copyFileToBuild(paths) {
  if (!fs.existsSync(path.dirname(paths.targetPath))) {
    fs.mkdirSync(path.dirname(paths.targetPath), { recursive: true })
  }

  fs.copyFileSync(paths.sourcePath, paths.targetPath)

  console.log(`Copied ${paths.sourcePath} to ${paths.targetPath}`)
}

module.exports = { getPaths, printPaths, copyFileToBuild }
