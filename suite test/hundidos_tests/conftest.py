from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from hundidos_tests.adapters.base import BlockedTest, ProductAdapter
from hundidos_tests.adapters.baseline import BaselineAdapter
from hundidos_tests.adapters.pipeline import PipelineAdapter
from hundidos_tests.metrics.reporter import MetricsReporter


def pytest_addoption(parser):
    parser.addoption(
        "--target",
        action="store",
        default="baseline",
        choices=["baseline", "pipeline", "run01", "run02", "run03"],
    )
    parser.addoption("--config", action="store", default=None)
    parser.addoption("--results-dir", action="store", default="results")


@pytest.fixture(scope="session")
def adapter(pytestconfig) -> ProductAdapter:
    root = Path(__file__).resolve().parents[1]
    target = pytestconfig.getoption("--target")
    config_target = "baseline" if target == "baseline" else "pipeline"
    config_arg = pytestconfig.getoption("--config")
    config_path = Path(config_arg) if config_arg else root / "config" / f"{config_target}.yml"
    cls = BaselineAdapter if target == "baseline" else PipelineAdapter
    return cls.from_file(config_path, pytestconfig.getoption("--base-url"))


@pytest.fixture(autouse=True)
def blocked_as_skip():
    try:
        yield
    except BlockedTest as exc:
        pytest.skip(f"blocked: {exc}")


def _marker_value(item, name: str):
    marker = item.get_closest_marker(name)
    if not marker:
        return []
    return list(marker.args)


def pytest_sessionstart(session):
    session._hundidos_results = []


def pytest_runtest_logreport(report):
    if report.when != "call":
        return
    item = getattr(report, "item", None)
    if item is None:
        return


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return
    status = "passed" if report.passed else "skipped" if report.skipped else "failed"
    if report.skipped and "blocked:" in str(report.longrepr):
        status = "blocked"
    item.session._hundidos_results.append(
        {
            "nodeid": item.nodeid,
            "test_id": (_marker_value(item, "test_id") or [item.name])[0],
            "requirement_refs": _marker_value(item, "requirement"),
            "metric_refs": _marker_value(item, "metric"),
            "status": status,
            "message": str(report.longrepr) if report.failed or report.skipped else "",
            "duration_s": getattr(report, "duration", 0.0),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    )


def pytest_sessionfinish(session, exitstatus):
    config = session.config
    target = config.getoption("--target")
    root = Path(__file__).resolve().parents[1]
    results_dir = root / config.getoption("--results-dir")
    results_dir.mkdir(parents=True, exist_ok=True)

    results = getattr(session, "_hundidos_results", [])
    jsonl_path = results_dir / f"results_{target}.jsonl"
    jsonl_path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in results),
        encoding="utf-8",
    )

    matrix_path = root / "hundidos_tests" / "metrics" / "requirements_matrix.yml"
    summary = MetricsReporter(matrix_path).summarize(target, results)
    (results_dir / f"summary_{target}.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
