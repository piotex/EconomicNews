theScript = new File('/usr/local/seedjob.groovy').getText("UTF-8")
pipelineJob('Tag Repositories') {
  definition {
    cps {
      script(theScript)
      sandbox()
    }
  }
}