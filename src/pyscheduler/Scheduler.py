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
import SYSTEMErrImpl

COMPONENTS = {
    "SCHEDULER_PY_TEST": ("INSTRUMENT_S", "DATABASE_S", "TELESCOPE_S"),
    "SCHEDULER_PY": ("INSTRUMENT", "DATABASE", "TELESCOPE"),
}

PROPOSAL_STATUSES = {
    'queued':0,
    'running':1,
    'ready':2
}

class Scheduler(SCHEDULER_MODULE__POA.Scheduler, ACSComponent, ContainerServices, ComponentLifecycle):
    def __init__(self):
        ACSComponent.__init__(self)
        ContainerServices.__init__(self)
        self._logger = self.getLogger()
        self._running = False

        self._instrument = None
        self._db = None
        self._telescope = None
        self._pid = None

    def initialize(self):
        super().initialize()
        self._logger.logInfo(f"Initialized component: {self.name}")
        children = COMPONENTS[self.name]
        self._logger.logInfo(f"Creating child components: {children}")
        instrument_name, db_name, telescope_name = children
        client = PySimpleClient()
        self._instrument = client.getComponent(instrument_name)
        self._db = client.getComponent(db_name)
        self._telescope = client.getComponent(telescope_name)

    #DB Methods!
    def _getProposalsFromDB(self):
        self._logger.logInfo(f"{self.name}: getProposalsFromDB called")
        proposals = self._db.getProposals()
        self._logger.logInfo(f"{self.name}: db returned {len(proposals)} proposals!")
        return proposals

    def _setProposalStatus(self, pid, status):
        self._logger.logInfo(f"{self.name}: setProposalStatus called with parameters pid:{pid}, status:{status}")
        self._db.setProposalStatus(pid, status)
        self._logger.logError(f"{self.name}: An error occurred when setting the parameters")

    def _storeObservation(self, pid, tid, image):
        self._logger.logInfo(f"{self.name}: setProposalStatus called with parameters pid:{pid}, tid:{tid}")
        self._db.storeObservation(pid, tid, image)

    #Instrument Methods!
    def _turnCameraOn(self):
        self._logger.logInfo(f"{self.name}: turnCameraOn called")
        self._instrument.cameraOn()

    def _turnCameraOff(self):
        self._logger.logInfo(f"{self.name}: turnCameraOff called")
        self._instrument.cameraOn()

    #Telescope Methods!
    def _telescopeObserve(self,position, exposureTime):
        self._logger.logInfo(f"{self.name}: telescopeObserve called")
        self._telescope.observe(position, exposureTime)

    def start(self):
        self._logger.logInfo(f"{self.name}: start called")
        if self._running:
            raise SYSTEMErrImpl.SchedulerAlreadyRunningExImpl()
        self._running = True

        self._proposalList = self._getProposalsFromDB()
        
        for proposal in self._proposalList:
            self._pid=proposal.pid
            self._setProposalStatus(self._pid,PROPOSAL_STATUSES["running"])
            self._turnCameraOn()

    def stop(self):
        self._logger.logInfo(f"{self.name}: stop called")
        if not self._running:
            raise SYSTEMErrImpl.SchedulerAlreadyStoppedExImpl()
        self._running = False

    def proposalUnderExecution(self) -> int:
        self._logger.logInfo(f"{self.name}: proposalUnderExecution called")
        proposal_under_execution = self._pid
        if proposal_under_execution is None:
            raise SYSTEMErrImpl.NoProposalExecutingExImpl()
        self._logger.logInfo(f"proposalUnderExecution: {proposal_under_execution}")
        return proposal_under_execution
