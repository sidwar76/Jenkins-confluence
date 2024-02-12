import groovy.json.JsonSlurper

@NonCPS
def parseJsonFile(String jsonFilePath) {
    echo "Parsing JSON file at: ${jsonFilePath}"
    def jsonContent = new File(jsonFilePath).text
    echo "JSON content: ${jsonContent}"
    def slurper = new JsonSlurper()
    def parsedData = slurper.parseText(jsonContent)
    echo "Parsed JSON data: ${parsedData}"
    return parsedData
}
