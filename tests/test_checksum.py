from app.domain.checksum import calculate_sha256


def test_calculate_sha256_returns_expected_hash():
    content = b"hello"

    expected_checksum = (
        "2cf24dba5fb0a30e26e83b2ac5b9e29e"
        "1b161e5c1fa7425e73043362938b9824"
    )

    assert calculate_sha256(content) == expected_checksum


def test_calculate_sha256_returns_same_hash_for_same_content():
    content = b"same pdf content"

    first_checksum = calculate_sha256(content)
    second_checksum = calculate_sha256(content)

    assert first_checksum == second_checksum
