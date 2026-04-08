from app.main import run


def test_run_creates_output_files(tmp_path):
    output_dir = tmp_path / "outputs"

    run(topic="AI", max_results=3, output_dir=str(output_dir))

    files = sorted(output_dir.glob("*.md"))

    assert len(files) == 3
    assert files[0].name == "001.md"
    assert files[1].name == "002.md"
    assert files[2].name == "003.md"

    content = files[0].read_text(encoding="utf-8")
    assert "# AI News 1" in content
    assert "## Summary" in content