from behave import given, when, then  # type: ignore[reportAttributeAccessIssue, unused-ignore]
from behave.runner import Context
from bs4 import BeautifulSoup
from musos_assist import app
from fastapi.testclient import TestClient


@given('I have a music single release "{title}"')  # type: ignore[misc]
def step_impl_given_request(context: Context, title: str) -> None:
    context.title = title


@when("I view the details of the release")  # type: ignore[misc]
def step_impl_when_document_process(context: Context) -> None:
    # Perform a GET request to the FastAPI app
    context.response = TestClient(app).get("/")
    assert context.response.status_code == 200


@then("I should see the following information")  # type: ignore[misc]
def step_impl_then_verify_steps(context: Context) -> None:
    # Parse the HTML content using BeautifulSoup
    soup: BeautifulSoup = BeautifulSoup(context.response.content, "html.parser")

    # Extract information from the HTML and compare with expected data
    if context.table is None:
        raise ValueError("context.table is None")
    for row in context.table:
        field: str = row["field"]
        expected_value: str = row["value"]

        # Assuming the HTML has elements with IDs matching the field names
        element = soup.find(id=field)
        assert element is not None, f"Element with id {field} not found"
        actual_value: str = element.text.strip()
        assert (
            actual_value == expected_value
        ), f"Expected {expected_value} but got {actual_value}"
