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


def await_start(scheduler, timeout: float):
    interval = 0.1  # seconds
    n_attempts = int(timeout // interval)
    for _ in range(n_attempts):
        try:
            scheduler.proposalUnderExecution()
            break
        except SYSTEMErr.NoProposalExecutingEx:
            time.sleep(interval)
            continue
    else:
        raise TimeoutError("Condition not reached within time")


def await_stop(scheduler, timeout: float):
    interval = 0.1  # seconds
    n_attempts = int(timeout // interval)
    for _ in range(n_attempts):
        try:
            scheduler.proposalUnderExecution()
            time.sleep(interval)
        except SYSTEMErr.NoProposalExecutingEx:
            break
    else:
        raise TimeoutError("Condition not reached within time")


def test_already_stopped(scheduler):
    with pytest.raises(SYSTEMErr.SchedulerAlreadyStoppedEx):
        scheduler.stop()


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

    # Wait until stop completed
    await_stop(scheduler, timeout=10)


def test_proposalUnderExecution(scheduler):
    with pytest.raises(SYSTEMErr.NoProposalExecutingEx):
        scheduler.proposalUnderExecution()

    scheduler.start()
    # Wait until observations have started
    await_start(scheduler, timeout=10)
    assert scheduler.proposalUnderExecution() is not None

    scheduler.stop()
    # Wait until the observation is complete
    await_stop(scheduler, timeout=10)
    with pytest.raises(SYSTEMErr.NoProposalExecutingEx):
        scheduler.proposalUnderExecution()
