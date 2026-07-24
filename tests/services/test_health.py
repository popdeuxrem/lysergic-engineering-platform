from runtime.services.health import HealthService, HealthStatus


def test_initial_unknown() -> None:
    hs = HealthService()
    report = hs.report()
    assert report.overall == HealthStatus.UNKNOWN
    assert report.ready_count == 0
    assert report.total_count == 0


def test_report_ready() -> None:
    hs = HealthService()
    hs.report_ready("svc-a")
    assert hs.service_status("svc-a") == HealthStatus.READY


def test_report_degraded() -> None:
    hs = HealthService()
    hs.report_ready("svc-a")
    hs.report_degraded("svc-a")
    assert hs.service_status("svc-a") == HealthStatus.DEGRADED


def test_report_failure() -> None:
    hs = HealthService()
    hs.report_failure("svc-a", "something broke")
    assert hs.service_status("svc-a") == HealthStatus.FAILED


def test_report_stopped() -> None:
    hs = HealthService()
    hs.report_ready("svc-a")
    hs.report_stopped("svc-a")
    assert hs.service_status("svc-a") == HealthStatus.STOPPED


def test_all_ready() -> None:
    hs = HealthService()
    hs.report_ready("a")
    hs.report_ready("b")
    assert hs.all_ready() is True


def test_not_all_ready() -> None:
    hs = HealthService()
    hs.report_ready("a")
    hs.report_failure("b")
    assert hs.all_ready() is False


def test_overall_ready_when_all_ready() -> None:
    hs = HealthService()
    hs.report_ready("a")
    hs.report_ready("b")
    report = hs.report()
    assert report.overall == HealthStatus.READY
    assert report.ready_count == 2
    assert report.total_count == 2


def test_overall_failed_when_any_failed() -> None:
    hs = HealthService()
    hs.report_ready("a")
    hs.report_failure("b")
    report = hs.report()
    assert report.overall == HealthStatus.FAILED


def test_overall_degraded_when_not_ready_or_failed() -> None:
    hs = HealthService()
    hs.report_ready("a")
    hs.report_degraded("b")
    report = hs.report()
    assert report.overall == HealthStatus.DEGRADED


def test_summary_string() -> None:
    hs = HealthService()
    hs.report_ready("a")
    hs.report_ready("b")
    report = hs.report()
    assert "2/2" in report.summary
