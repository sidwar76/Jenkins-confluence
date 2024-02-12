import groovy.json.JsonSlurper

@NonCPS
def parseJsonFile(String jsonFilePath) {
    def jsonContent = new File(jsonFilePath).text
    def slurper = new JsonSlurper()
    return slurper.parseText(jsonContent)
}
