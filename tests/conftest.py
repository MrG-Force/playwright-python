# pylint: disable=redefined-outer-name
"""This module contains fixtures for the tests."""
import json
import os
from typing import Generator

import pytest
from dotenv import load_dotenv
from playwright.sync_api import (
    APIRequestContext,
    Browser,
    BrowserContext,
    Page,
    Playwright,
)

import allure

from pages.home import HomePage

load_dotenv()


@allure.title("Launching the browser")
@pytest.fixture(scope="session")
def browser(playwright: Playwright):
    """Fixture to launch the browser."""
    browser_name = os.getenv("BROWSER", "chromium")
    headless = os.getenv("HEADLESS", "true") == "true"

    browsers = {
        "chromium": playwright.chromium,
        "chrome": playwright.chromium,  # Chrome is Chromium-based
        "firefox": playwright.firefox,
        "webkit": playwright.webkit,
        "edge": playwright.chromium,  # Edge is Chromium-based
    }

    if browser_name not in browsers:
        raise ValueError(f"Unsupported browser: {browser_name}")

    browser = browsers[browser_name].launch(headless=headless)
    yield browser
    browser.close()


@allure.title("Creating a new browser context")
@pytest.fixture(scope="function")
def context(browser: Browser):
    """Fixture to create a new browser context."""
    context = browser.new_context(ignore_https_errors=True)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield context
    context.tracing.stop(path="trace.zip")
    context.close()


@allure.title("Creating a new page")
@pytest.fixture(scope="function")
def page(context: BrowserContext):
    """Fixture to create a new page."""
    page = context.new_page()
    yield page
    page.close()


@allure.title("Creating a new home page object")
@pytest.fixture
def home_page(page: Page):
    """Fixture to create a new HomePage object."""
    return HomePage(page)


@allure.title("Creating a new APIRequestContext object for authentication")
@pytest.fixture(scope="session")
def api_auth_request_context(playwright: Playwright):
    """Fixture to create a new APIRequestContext object for authentication."""
    token_url = os.getenv("OKTA_AUTH_URL")

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    auth_request_context = playwright.request.new_context(
        base_url=token_url, extra_http_headers=headers
    )

    yield auth_request_context
    auth_request_context.dispose()


@allure.title("Getting the API token")
@pytest.fixture(scope="session")
def api_token(api_auth_request_context: APIRequestContext):
    """Fixture to get the API token."""
    form_data = {
        "client_id": os.getenv("OKTA_CLIENT_ID"),
        "client_secret": os.getenv("OKTA_CLIENT_SECRET"),
        "grant_type": "client_credentials",
        "scope": "mod_custom",
    }

    response = api_auth_request_context.post("/oauth2/default/v1/token", form=form_data)
    assert response.ok
    return f"{response.json()['token_type']} {response.json()['access_token']}"


@allure.title("Creating a new APIRequestContext object")
@pytest.fixture(scope="session")
def api_request_context(
    playwright: Playwright, api_token: str
) -> Generator[APIRequestContext, None, None]:
    """Fixture to create a new APIRequestContext object."""
    toys_api_url = f"{os.getenv('SUT_API_URL')}"
    headers = {"Authorization": api_token, "Content-Type": "application/json"}
    api_auth_request_context = playwright.request.new_context(
        base_url=toys_api_url, extra_http_headers=headers
    )
    yield api_auth_request_context
    api_auth_request_context.dispose()


@allure.title("Getting the list of toys from the data file")
@pytest.fixture(scope="session")
def toys() -> list:
    """Fixture to return a list of toys."""
    with open("data/toys.json", "r", encoding="utf-8") as file:
        return json.load(file)


@allure.title("Adding toys to the database")
@pytest.fixture(scope="session")
def setup_teardown_toys(
    api_request_context: APIRequestContext, toys: list
) -> Generator[dict, None, None]:
    """Fixture to create toys and delete them after the test."""
    toy_ids = []
    for toy in toys:
        response = api_request_context.post("/toy", data=toy)
        toy_ids.append(response.json()["id"])
        assert response.ok
    yield
    allure.step("Deleting toys from the database")
    for toy_id in toy_ids:
        response = api_request_context.delete(f"/toy/{toy_id}")
        assert response.ok


@allure.title("Getting the customer details from the data file")
@pytest.fixture(scope="session")
def details() -> dict:
    """Fixture to return a dictionary of customer details."""
    with open("data/customer.json", "r", encoding="utf-8") as file:
        return json.load(file)
