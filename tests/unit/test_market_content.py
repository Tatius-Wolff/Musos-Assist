import pytest
from datetime import date
from pydantic import ValidationError, HttpUrl
from musos_assist.market_content import MarketingContact, PressCoverage, PressKit


def test_marketing_contact_valid() -> None:
    contact = MarketingContact(
        organisation="Test Organisation", name="John Doe", email="john.doe@example.com"
    )
    assert contact.organisation == "Test Organisation"
    assert contact.name == "John Doe"
    assert contact.email == "john.doe@example.com"


def test_validate_name_empty_organisation() -> None:
    with pytest.raises(ValueError) as excinfo:
        MarketingContact(organisation="", name="John Doe", email="john.doe@example.com")

    expected_message = "1 validation error for MarketingContact\norganisation\n  String should have at least 1 character"
    actual_message = str(excinfo.value)

    assert expected_message in actual_message


def test_validate_name_empty_name() -> None:
    with pytest.raises(ValueError):
        MarketingContact(
            organisation="Valid Organisation", name="", email="john.doe@example.com"
        )


def test_marketing_contact_invalid_email() -> None:
    with pytest.raises(ValueError):
        MarketingContact(
            organisation="Test Organisation", name="John Doe", email="invalid-email"
        )


def test_marketing_contact_missing_name() -> None:
    with pytest.raises(ValueError):
        MarketingContact(organisation="Test Organisation", email="john.doe@example.com")  # type: ignore[call-arg]


def test_marketing_contact_missing_organisation() -> None:
    with pytest.raises(ValueError):
        MarketingContact(name="John Doe", email="john.doe@example.com")  # type: ignore[call-arg]


def test_marketing_contact_missing_email() -> None:
    with pytest.raises(ValueError):
        MarketingContact(organisation="Test Organisation", name="John Doe")  # type: ignore[call-arg]


def test_press_coverage_valid() -> None:
    marketing_contact = MarketingContact(
        organisation="Test Organisation", name="John Doe", email="john.doe@example.com"
    )
    press_coverage = PressCoverage(
        subject="Test Subject",
        publish_date=date.today(),
        web_link="https://example.com",  # type: ignore[arg-type]
        body="<p>Test Body</p>",
        images=["https://example.com/image1.jpg", "https://example.com/image2.jpg"],
        author="Jane Doe",
        marketing_contact=marketing_contact,
    )
    assert press_coverage.subject == "Test Subject"
    assert press_coverage.publish_date == date.today()
    assert press_coverage.web_link == HttpUrl("https://example.com/")
    assert press_coverage.body == "<p>Test Body</p>"
    assert press_coverage.images == [
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg",
    ]
    assert press_coverage.author == "Jane Doe"
    assert press_coverage.marketing_contact == marketing_contact


def test_press_coverage_invalid_web_link() -> None:
    marketing_contact = MarketingContact(
        organisation="Test Organisation", name="John Doe", email="john.doe@example.com"
    )
    with pytest.raises(ValidationError):
        PressCoverage(
            subject="Test Subject",
            publish_date=date.today(),
            web_link="invalid-url",  # type: ignore[arg-type]
            body="<p>Test Body</p>",
            images=["https://example.com/image1.jpg", "https://example.com/image2.jpg"],
            author="Jane Doe",
            marketing_contact=marketing_contact,
        )


def test_press_coverage_missing_subject() -> None:
    marketing_contact = MarketingContact(
        organisation="Test Organisation", name="John Doe", email="john.doe@example.com"
    )
    with pytest.raises(ValidationError):
        PressCoverage(
            publish_date=date.today(),
            web_link="https://example.com",  # type: ignore[arg-type]
            body="<p>Test Body</p>",
            images=["https://example.com/image1.jpg", "https://example.com/image2.jpg"],
            author="Jane Doe",
            marketing_contact=marketing_contact,
        )  # type: ignore[call-arg]


def test_press_coverage_missing_publish_date() -> None:
    marketing_contact = MarketingContact(
        organisation="Test Organisation", name="John Doe", email="john.doe@example.com"
    )
    with pytest.raises(ValidationError):
        PressCoverage(
            subject="Test Subject",
            web_link="https://example.com",  # type: ignore[arg-type]
            body="<p>Test Body</p>",
            images=["https://example.com/image1.jpg", "https://example.com/image2.jpg"],
            author="Jane Doe",
            marketing_contact=marketing_contact,
        )  # type: ignore[call-arg]


def test_press_coverage_missing_body() -> None:
    marketing_contact = MarketingContact(
        organisation="Test Organisation", name="John Doe", email="john.doe@example.com"
    )
    with pytest.raises(ValidationError):
        PressCoverage(
            subject="Test Subject",
            publish_date=date.today(),
            web_link="https://example.com",  # type: ignore[arg-type]
            images=["https://example.com/image1.jpg", "https://example.com/image2.jpg"],
            author="Jane Doe",
            marketing_contact=marketing_contact,
        )  # type: ignore[call-arg]


def test_press_coverage_missing_author() -> None:
    marketing_contact = MarketingContact(
        organisation="Test Organisation", name="John Doe", email="john.doe@example.com"
    )
    with pytest.raises(ValidationError):
        PressCoverage(
            subject="Test Subject",
            publish_date=date.today(),
            web_link="https://example.com",  # type: ignore[arg-type]
            body="<p>Test Body</p>",
            images=["https://example.com/image1.jpg", "https://example.com/image2.jpg"],
            marketing_contact=marketing_contact,
        )  # type: ignore[call-arg]


def test_press_coverage_missing_marketing_contact() -> None:
    with pytest.raises(ValidationError):
        PressCoverage(
            subject="Test Subject",
            publish_date=date.today(),
            web_link="https://example.com",  # type: ignore[arg-type]
            body="<p>Test Body</p>",
            images=["https://example.com/image1.jpg", "https://example.com/image2.jpg"],
            author="Jane Doe",
        )  # type: ignore[call-arg]


def test_press_kit_valid() -> None:
    marketing_contact = MarketingContact(
        organisation="Test Organisation", name="John Doe", email="john.doe@example.com"
    )
    press_coverage = PressCoverage(
        subject="Test Subject",
        publish_date=date.today(),
        web_link="https://example.com",  # type: ignore[arg-type]
        body="<p>Test Body</p>",
        images=["https://example.com/image1.jpg", "https://example.com/image2.jpg"],
        author="Jane Doe",
        marketing_contact=marketing_contact,
    )
    press_kit = PressKit(presscoverage=press_coverage)
    assert press_kit.presscoverage == press_coverage


def test_press_kit_missing_press_coverage() -> None:
    with pytest.raises(ValidationError):
        PressKit()  # type: ignore[call-arg]
