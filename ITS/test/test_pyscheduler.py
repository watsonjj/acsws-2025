from Acspy.Clients.SimpleClient import PySimpleClient
import SYSTEMErr
import pytest
import time

@pytest.fixture
def scheduler():
    c = PySimpleClient()
    scheduler = c.getComponent("SCHEDULER_PY_TEST")
    return scheduler


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


def test_proposalUnderExecution(scheduler):
    with pytest.raises(SYSTEMErr.NoProposalExecutingEx):
        scheduler.proposalUnderExecution()

    scheduler.start()
    assert scheduler.proposalUnderExecution() > 0

    scheduler.stop()
    # Wait until the observation is complete
    time.sleep(3)  # TODO: sleep long enough?

    with pytest.raises(SYSTEMErr.NoProposalExecutingEx):
        scheduler.proposalUnderExecution()
