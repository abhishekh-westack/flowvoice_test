#!/bin/bash

# Users Tests Runner Script
# This script provides convenient commands to run users tests

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Users Management Tests ===${NC}\n"

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo -e "${YELLOW}pytest is not installed. Installing...${NC}"
    pip install pytest playwright pytest-playwright allure-pytest
fi

# Parse command line arguments
TEST_TYPE=${1:-all}

case $TEST_TYPE in
    list)
        echo -e "${GREEN}Running Users List Page tests...${NC}"
        pytest tests/users/test_users_list.py -v --alluredir=allure-results
        ;;
    detail)
        echo -e "${GREEN}Running User Detail Page tests...${NC}"
        pytest tests/users/test_user_detail.py -v --alluredir=allure-results
        ;;
    all)
        echo -e "${GREEN}Running all Users tests...${NC}"
        pytest tests/users/ -v --alluredir=allure-results
        ;;
    report)
        echo -e "${GREEN}Generating Allure report...${NC}"
        allure serve allure-results
        ;;
    *)
        echo -e "${YELLOW}Usage: $0 {list|detail|all|report}${NC}"
        echo ""
        echo "  list   - Run users list page tests"
        echo "  detail - Run user detail page tests"
        echo "  all    - Run all users tests (default)"
        echo "  report - Generate and serve Allure report"
        exit 1
        ;;
esac

echo -e "\n${GREEN}Tests completed!${NC}"
