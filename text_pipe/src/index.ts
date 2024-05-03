import {
  applyTemplate,
  loadTextFile,
  saveToJson,
  youtubeLinkTemplate,
  youtubeLinkTemplate_Markdown,
} from './function'
const inputFilePath = './../data/link/input.txt'
const outputFilePath = './../data/link/output.json'
const lines = loadTextFile(inputFilePath, false)
const results = applyTemplate(lines, youtubeLinkTemplate_Markdown)
saveToJson(outputFilePath, results)
console.log('Processing complete. Results saved to', outputFilePath)
