# Client stubs and definitions, such as structs, enums, etc.
import SCHEDULER_MODULE
# Skeleton infrastructure for server implementation
import SCHEDULER_MODULE__POA

# Base component implementation
from Acspy.Servants.ACSComponent import ACSComponent
# Services provided by the container to the component
from Acspy.Servants.ContainerServices import ContainerServices
# Basic component lifecycle (initialize, execute, cleanUp and aboutToAbort methods)
from Acspy.Servants.ComponentLifecycle import ComponentLifecycle
from Acspy.Clients.SimpleClient import PySimpleClient

COMPONENTS = {
    "SCHEDULER_PY_TEST": ("INSTRUMENT_S", "DATABASE_S", "TELESCOPE_S"),
    "SCHEDULER_PY": ("INSTRUMENT", "DATABASE", "TELESCOPE"),
}


class Scheduler(SCHEDULER_MODULE__POA.Scheduler, ACSComponent, ContainerServices, ComponentLifecycle):
    def __init__(self):
        ACSComponent.__init__(self)
        ContainerServices.__init__(self)
        self._logger = self.getLogger()
        self._running = False

        self._logger.logInfo(f"Created component: {self.name}")
        children = COMPONENTS[self.name]
        self._logger.logInfo(f"Creating child components: {children}")
        instrument_name, db_name, telescope_name = children
        client = PySimpleClient()
        self._instrument = client.getComponent(instrument_name)
        self._db = client.getComponent(db_name)
        self._telescope = client.getComponent(telescope_name)

    def start(self):
        self._logger.logInfo(f"{self.name}: start called")
        if self._running:
            # TODO
            print("TODO: already running - raise exception")
        self._running = True

    def stop(self):
        self._logger.logInfo(f"{self.name}: stop called")
        if not self._running:
            # TODO
            print("TODO: already stopped - raise exception")
        self._running = False

    def proposalUnderExecution(self) -> int:
        self._logger.logInfo(f"{self.name}: proposalUnderExecution called")
        proposal_under_execution = 123  # TODO
        if proposal_under_execution is None:
            # TODO
            print("TODO: no proposal under execution - raise exception")
        self._logger.logInfo(f"proposalUnderExecution: {proposal_under_execution}")
        return proposal_under_execution
