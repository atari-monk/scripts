import {
  applyTemplate,
  loadTextFile,
  saveToFile,
  saveToJson,
  youtubeLinkTemplate,
} from './function'
const inputFilePath = './../data/tutorial.txt'
const outputFilePath = './../data/tutorial.json'
const lines = loadTextFile(inputFilePath, false)
const results = applyTemplate(lines, youtubeLinkTemplate)
saveToJson(outputFilePath, results)
console.log('Processing complete. Results saved to', outputFilePath)
