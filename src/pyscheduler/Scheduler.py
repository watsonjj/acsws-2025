# Client stubs and definitions, such as structs, enums, etc.
import time

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
from concurrent.futures import ThreadPoolExecutor
import signal
import threading


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
        self._image = None
        self._client = None
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._stop = threading.Event()

    def initialize(self):
        super().initialize()
        self._logger.logInfo(f"Initialized component: {self.name}")
        children = COMPONENTS[self.name]
        self._logger.logInfo(f"Creating child components: {children}")
        instrument_name, db_name, telescope_name = children
        self._client = PySimpleClient()
        self._instrument = self._client.getComponent(instrument_name)
        self._db = self._client.getComponent(db_name)
        self._telescope = self._client.getComponent(telescope_name)

    def cleanUp(self):
        self._logger.logInfo(f"Cleanup component: {self.name}")
        self._executor.shutdown(wait=True, cancel_futures=True)
        super().cleanUp()
        children = COMPONENTS[self.name]
        self._logger.logInfo(f"Releasing child components: {children}")
        instrument_name, db_name, telescope_name = children
        self._client.releaseComponent(instrument_name)
        self._client.releaseComponent(db_name)
        self._client.releaseComponent(telescope_name)
        self._client.disconnect()

    #DB Methods!
    def _getProposalsFromDB(self):
        self._logger.logInfo(f"{self.name}: getProposalsFromDB called")
        proposals = self._db.getProposals()
        self._logger.logInfo(f"{self.name}: db returned {len(proposals)} proposals!")
        return proposals

    def _setProposalStatus(self, pid, status):
        self._logger.logInfo(f"{self.name}: setProposalStatus called with parameters pid:{pid}, status:{status}")
        self._db.setProposalStatus(pid, status)

    def _storeObservation(self, pid, tid, image):
        self._logger.logInfo(f"{self.name}: setProposalStatus called with parameters pid:{pid}, tid:{tid}")
        self._db.storeImage(pid, tid, image)

    #Instrument Methods!
    def _turnCameraOn(self):
        self._logger.logInfo(f"{self.name}: turnCameraOn called")
        self._instrument.cameraOn()

    def _turnCameraOff(self):
        self._logger.logInfo(f"{self.name}: turnCameraOff called")
        self._instrument.cameraOff()

    #Telescope Methods!
    def _telescopeObserve(self,position, exposureTime):
        self._logger.logInfo(f"{self.name}: telescopeObserve called")
        image = self._telescope.observe(position, exposureTime)
        return image

    def _process_proposals(self, stop: threading.Event):
        self._proposalList = self._getProposalsFromDB()

        for proposal in self._proposalList:
            if stop.is_set():
                self._logger.logInfo("Proposal aborted")
                break
            
            self._pid = proposal.pid
            target_list = proposal.targets
            self._setProposalStatus(self._pid, PROPOSAL_STATUSES["running"])
            self._turnCameraOn()

            for target in target_list:
                if stop.is_set():
                    self._logger.logInfo("Observation aborted")
                    break
                
                position = target.coordinates
                exp = target.expTime
                tid = target.tid
                self._image = self._telescopeObserve(position, exp)
                self._storeObservation(self._pid, tid, self._image)
                time.sleep(1)

            self._turnCameraOff()
            self._setProposalStatus(self._pid, PROPOSAL_STATUSES['ready'])
        self._pid = None
        

    def start(self):
        self._logger.logInfo(f"{self.name}: start called")
        if self._running:
            self._logger.error("Already running")
            raise SYSTEMErrImpl.SchedulerAlreadyRunningExImpl()
        self._running = True
        self._executor.submit(self._process_proposals, self._stop)

    def stop(self):
        self._logger.logInfo(f"{self.name}: stop called")
        if not self._running:
            self._logger.error("Already stopped")
            raise SYSTEMErrImpl.SchedulerAlreadyStoppedExImpl()
        self._running = False
        self._stop.set()
        self._logger.logInfo(f"{self.name}: stop completed")

    def proposalUnderExecution(self) -> int:
        self._logger.logInfo(f"{self.name}: proposalUnderExecution called")
        proposal_under_execution = self._pid
        if proposal_under_execution is None:
            raise SYSTEMErrImpl.NoProposalExecutingExImpl()
        self._logger.logInfo(f"proposalUnderExecution: {proposal_under_execution}")
        return proposal_under_execution
