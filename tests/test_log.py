import json
from pathlib import Path
from investigation_contracts.log import read_log


def _write(p: Path, rows):
    p.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")


def test_read_all(tmp_path):
    p = tmp_path / "events.jsonl"
    _write(p, [{"event_id": "01", "type": "A"}, {"event_id": "02", "type": "B"}])
    assert [e["event_id"] for e in read_log(p)] == ["01", "02"]


def test_cursor_is_exclusive(tmp_path):
    p = tmp_path / "events.jsonl"
    _write(p, [{"event_id": "01", "type": "A"}, {"event_id": "02", "type": "A"}])
    assert [e["event_id"] for e in read_log(p, cursor="01")] == ["02"]


def test_type_filter(tmp_path):
    p = tmp_path / "events.jsonl"
    _write(p, [{"event_id": "01", "type": "A"}, {"event_id": "02", "type": "B"}])
    assert [e["event_id"] for e in read_log(p, types=["B"])] == ["02"]


def test_missing_file_and_malformed_line(tmp_path):
    assert read_log(tmp_path / "nope.jsonl") == []
    p = tmp_path / "events.jsonl"
    p.write_text('{"event_id":"01","type":"A"}\nnot json\n{"event_id":"02","type":"A"}\n')
    assert [e["event_id"] for e in read_log(p)] == ["01", "02"]
