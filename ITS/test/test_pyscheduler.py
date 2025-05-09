from Acspy.Clients.SimpleClient import PySimpleClient
import SYSTEMErr
import pytest
import time

@pytest.fixture
def scheduler():
    c = PySimpleClient()
    scheduler = c.getComponent("SCHEDULER_PY_TEST")
    yield scheduler
    c.releaseComponent("SCHEDULER_PY_TEST")
    c.disconnect()


def test_already_stopped(scheduler):
    with pytest.raises(SYSTEMErr.SchedulerAlreadyStoppedEx):
        scheduler.stop()


def test_start_stop(scheduler):
    scheduler.start()

    # Error raised if started twice
    with pytest.raises(SYSTEMErr.SchedulerAlreadyRunningEx):
        scheduler.start()

    scheduler.stop()

    # Error raised if stopped twice
    with pytest.raises(SYSTEMErr.SchedulerAlreadyStoppedEx):
        scheduler.stop()


def test_proposalUnderExecution(scheduler):
    with pytest.raises(SYSTEMErr.NoProposalExecutingEx):
        scheduler.proposalUnderExecution()

    scheduler.start()
    assert scheduler.proposalUnderExecution() is not None

    scheduler.stop()
    with pytest.raises(SYSTEMErr.NoProposalExecutingEx):
        scheduler.proposalUnderExecution()
