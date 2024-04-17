const lib = require('./../../src_js/copy_package')

const debug = true
const projName = 'copy_package_test'
const sourceFile = `../../${projName}/package.json`
const targetDir = `../../${projName}/build`

const paths = lib.getPaths(sourceFile, targetDir, debug)
if (debug) return
lib.copyFileToBuild(paths)
