"""
Fixtures for users tests
"""
import pytest
from flows.users.users_list_flow import UsersListFlow
from flows.users.user_detail_flow import UserDetailFlow
from pages.users.users_list_page import UsersListPage
from pages.users.user_detail_page import UserDetailPage


@pytest.fixture
def users_list_page(page):
    """Fixture to provide UsersListPage instance"""
    return UsersListPage(page)


@pytest.fixture
def user_detail_page(page):
    """Fixture to provide UserDetailPage instance"""
    return UserDetailPage(page)


@pytest.fixture
def users_list_flow(page):
    """Fixture to provide UsersListFlow instance"""
    return UsersListFlow(page)


@pytest.fixture
def user_detail_flow(page):
    """Fixture to provide UserDetailFlow instance"""
    return UserDetailFlow(page)
