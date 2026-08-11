from audit.ddl_capture import DDLCapture


def test_same_ddl_has_same_hash():
    ddl = "CREATE TABLE consumers (id INT)"

    assert (
        DDLCapture.sha256(ddl)
        == DDLCapture.sha256(ddl)
    )


def test_different_ddl_has_different_hash():
    before = "CREATE TABLE consumers (id INT)"
    after = "CREATE TABLE consumers (id BIGINT)"

    assert (
        DDLCapture.sha256(before)
        != DDLCapture.sha256(after)
    )


def test_ddl_unchanged():
    ddl = "CREATE TABLE consumers (id INT)"

    assert DDLCapture.unchanged(
        ddl,
        ddl,
    )


def test_ddl_changed():
    before = "CREATE TABLE x"
    after = "CREATE TABLE y"

    assert not DDLCapture.unchanged(
        before,
        after,
    )