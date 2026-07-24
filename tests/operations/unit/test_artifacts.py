from runtime.operations.artifacts import ArtifactCollector, OperationArtifact


def test_collect() -> None:
    c = ArtifactCollector()
    a = OperationArtifact(artifact_id="a1", name="Report", artifact_type="report")
    c.collect("op-1", a)
    artifacts = c.get("op-1")
    assert len(artifacts) == 1


def test_get_empty() -> None:
    c = ArtifactCollector()
    assert c.get("op-1") == ()


def test_remove() -> None:
    c = ArtifactCollector()
    c.collect("op-1", OperationArtifact(artifact_id="a1", name="A", artifact_type="doc"))
    assert c.remove("op-1") is True
