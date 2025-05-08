from Acspy.Clients.SimpleClient import PySimpleClient

c = PySimpleClient()
scheduler = c.getComponent("SCHEDULER_PY")
scheduler.start()
scheduler.stop()
