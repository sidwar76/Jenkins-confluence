import groovy.json.JsonSlurper

@NonCPS
def parseJsonText(String jsonText) {
    def slurper = new JsonSlurper()
    return slurper.parseText(jsonText)
}
