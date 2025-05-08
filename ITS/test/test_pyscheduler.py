from Acspy.Clients.SimpleClient import PySimpleClient

c = PySimpleClient()
scheduler = c.getComponent("SCHEDULER_PY_TEST")
scheduler.start()
scheduler.stop()
print(scheduler.proposalUnderExecution())
