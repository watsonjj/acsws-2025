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


class Scheduler(SCHEDULER_MODULE__POA.Scheduler, ACSComponent, ContainerServices, ComponentLifecycle):
    def __init__(self):
        ACSComponent.__init__(self)
        ContainerServices.__init__(self)
        self._logger = self.getLogger()
        self._running = False

    def start(self):
        self._logger.logInfo(f"{self.name}: start called")
        if self._running:
            # TODO
            print("TODO: already running - raise exception")
        self._running = True

    def stop(self):
        self._logger.logInfo(f"{self.name}: stop called")
        print(1122233)
        if not self._running:
            # TODO
            print("TODO: already stopped - raise exception")
        self._running = False