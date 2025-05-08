from Acspy.Clients.SimpleClient import PySimpleClient

c = PySimpleClient()
scheduler = c.getComponent("SCHEDULER")
scheduler.start()
scheduler.stop()
