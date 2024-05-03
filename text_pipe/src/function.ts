import * as fs from 'fs'

export function loadTextFile(
  filePath: string,
  debugMode: boolean = false
): string[] {
  try {
    const data = fs.readFileSync(filePath, 'utf8')
    const lines = data.split(/\r?\n/)

    if (debugMode) {
      console.log('Lines from file:')
      lines.forEach((line, index) => console.log(`Line ${index + 1}: ${line}`))
    }

    return lines
  } catch (err) {
    console.error('Error reading file:', err)
    return []
  }
}

export function applyTemplate(
  lines: string[],
  templateFunction: (line: string) => string
): string[] {
  return lines.map(templateFunction)
}

export function saveToFile(outputFilePath: string, data: string[]): void {
  fs.writeFileSync(outputFilePath, data.join('\n'))
}

export function saveToJson(outputFilePath: string, data: string[]): void {
  const jsonData = JSON.stringify(data, null, 2)
  fs.writeFileSync(outputFilePath, jsonData)
}

export function youtubeLinkTemplate(line: string): any {
  return {
    indexTitle: '',
    question: '',
    answer: `[t](${line})`,
    dateTime: new Date().toISOString(),
  }
}

export function youtubeLinkTemplate_Markdown(line: string): any {
  return {
    indexTitle: '',
    question: '',
    answer: `${line}`,
    dateTime: new Date().toISOString(),
  }
}
