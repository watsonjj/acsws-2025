from Acspy.Clients.SimpleClient import PySimpleClient
import SYSTEMErr
import pytest
import time

@pytest.fixture
def scheduler():
    c = PySimpleClient()
    scheduler = c.getComponent("SCHEDULER_PY_TEST")
    yield scheduler


def test_start_stop(scheduler):
    scheduler.start()
    # TODO: isActive method?
    # Error raised if started twice
    with pytest.raises(SYSTEMErr.SchedulerAlreadyRunningEx):
        scheduler.start()

    scheduler.stop()
    # TODO: isActive method?
    # Error raised if stopped twice
    with pytest.raises(SYSTEMErr.SchedulerAlreadyStoppedEx):
        scheduler.stop()



# def test_proposalUnderExecution(scheduler):
#     with pytest.raises(SYSTEMErr.NoProposalExecutingEx):
#         scheduler.proposalUnderExecution()
#
#     scheduler.start()
#     # Wait until observations have started
#     n_attempts = 100
#     for _ in range(n_attempts):
#         if scheduler.proposalUnderExecution() is not None:
#             break
#         time.sleep(0.1)
#     else:
#         raise TimeoutError("Condition not reached within time")
#     assert scheduler.proposalUnderExecution() > 0
#
#     scheduler.stop()
#     # Wait until the observation is complete
#     n_attempts = 100
#     for _ in range(n_attempts):
#         try:
#             scheduler.proposalUnderExecution()
#             time.sleep(0.1)
#         except SYSTEMErr.NoProposalExecutingEx:
#             break
#     else:
#         raise TimeoutError("Condition not reached within time")
#     with pytest.raises(SYSTEMErr.NoProposalExecutingEx):
#         scheduler.proposalUnderExecution()
