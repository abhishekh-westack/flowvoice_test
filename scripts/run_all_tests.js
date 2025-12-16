/**
 * Test Runner - Sequential Test Execution
 * 
 * This script runs all test cases one by one and generates a comprehensive report.
 * Make sure your FastAPI test runner is running on http://localhost:8000
 * 
 * Usage:
 *   node run_all_tests.js
 */

const API_BASE_URL = 'http://localhost:8000';

// All available test endpoints in order
const TEST_ENDPOINTS = [
    // Authentication
    { name: 'Login Tests', endpoint: '/test-login' },
    
    // Users Management
    { name: 'Users List Tests', endpoint: '/test-users-list' },
    { name: 'User Detail Tests', endpoint: '/test-user-detail' },
    
    // Contacts Management
    { name: 'Contacts List Tests', endpoint: '/test-contacts-list' },
    { name: 'Contact Form Tests', endpoint: '/test-contact-form' },
    
    // Knowledge Base Management
    { name: 'Knowledge Base List Tests', endpoint: '/test-knowledgebase-list' },
    { name: 'Knowledge Base Form Tests', endpoint: '/test-knowledgebase-form' },
    
    // Assistants
    { name: 'Assistant Creation Tests', endpoint: '/test-assistant-creation' },
    { name: 'Create Assistant All Types', endpoint: '/test-create-assistant-all-types' },
    { name: 'Update Assistant Basic', endpoint: '/test-update-assistant-basic' },
    { name: 'Delete Assistant', endpoint: '/test-delete-assistant' },
    
    // Assistant Updates - Voice
    { name: 'Voice Type Tests', endpoint: '/test-voice-type' },
    
    // Assistant Updates - Other Types
    { name: 'WhatsApp General Tab', endpoint: '/test-whatsapp-general-tab' },
    { name: 'Chatbot General Tab', endpoint: '/test-chatbot-general-tab' },
    { name: 'SMS General Tab', endpoint: '/test-sms-general-tab' },
];

// Delay between test executions (in milliseconds)
const DELAY_BETWEEN_TESTS = 5000; // 5 seconds

// Colors for terminal output
const colors = {
    reset: '\x1b[0m',
    bright: '\x1b[1m',
    green: '\x1b[32m',
    red: '\x1b[31m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    cyan: '\x1b[36m',
};

// Helper function to make POST requests
async function runTest(endpoint) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return { success: true, data };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

// Helper function to sleep
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Main function to run all tests sequentially
async function runAllTests() {
    console.log(`${colors.bright}${colors.blue}`);
    console.log('╔══════════════════════════════════════════════════════════════╗');
    console.log('║          Flowvoice Test Suite - Sequential Runner           ║');
    console.log('╚══════════════════════════════════════════════════════════════╝');
    console.log(colors.reset);
    console.log(`${colors.cyan}Starting test execution at: ${new Date().toLocaleString()}${colors.reset}\n`);

    const results = [];
    let successCount = 0;
    let failureCount = 0;

    for (let i = 0; i < TEST_ENDPOINTS.length; i++) {
        const test = TEST_ENDPOINTS[i];
        const testNumber = i + 1;
        const totalTests = TEST_ENDPOINTS.length;

        console.log(`${colors.bright}[${testNumber}/${totalTests}] Running: ${test.name}${colors.reset}`);
        console.log(`${colors.yellow}Endpoint: ${test.endpoint}${colors.reset}`);

        const result = await runTest(test.endpoint);

        if (result.success) {
            console.log(`${colors.green}✓ Test triggered successfully${colors.reset}`);
            successCount++;
            results.push({
                name: test.name,
                endpoint: test.endpoint,
                status: 'success',
                timestamp: new Date().toISOString(),
            });
        } else {
            console.log(`${colors.red}✗ Failed to trigger test: ${result.error}${colors.reset}`);
            failureCount++;
            results.push({
                name: test.name,
                endpoint: test.endpoint,
                status: 'failed',
                error: result.error,
                timestamp: new Date().toISOString(),
            });
        }

        // Wait before running next test (except for the last one)
        if (i < TEST_ENDPOINTS.length - 1) {
            console.log(`${colors.cyan}Waiting ${DELAY_BETWEEN_TESTS / 1000}s before next test...${colors.reset}\n`);
            await sleep(DELAY_BETWEEN_TESTS);
        }
    }

    // Print summary
    console.log('\n');
    console.log(`${colors.bright}${colors.blue}`);
    console.log('╔══════════════════════════════════════════════════════════════╗');
    console.log('║                      Test Execution Summary                  ║');
    console.log('╚══════════════════════════════════════════════════════════════╝');
    console.log(colors.reset);
    console.log(`${colors.cyan}Completed at: ${new Date().toLocaleString()}${colors.reset}\n`);
    console.log(`${colors.green}Successful: ${successCount}${colors.reset}`);
    console.log(`${colors.red}Failed: ${failureCount}${colors.reset}`);
    console.log(`Total: ${TEST_ENDPOINTS.length}\n`);

    // Print failed tests if any
    if (failureCount > 0) {
        console.log(`${colors.red}${colors.bright}Failed Tests:${colors.reset}`);
        results
            .filter(r => r.status === 'failed')
            .forEach(r => {
                console.log(`${colors.red}  - ${r.name} (${r.endpoint})${colors.reset}`);
                console.log(`    Error: ${r.error}`);
            });
        console.log('');
    }

    // Generate report upload instruction
    console.log(`${colors.bright}${colors.yellow}Next Steps:${colors.reset}`);
    console.log(`${colors.cyan}Wait for all tests to complete, then upload the report:${colors.reset}`);
    console.log(`${colors.green}  curl -X POST ${API_BASE_URL}/upload-report${colors.reset}\n`);

    // Save results to JSON file
    const fs = require('fs');
    const resultsFile = `test-results-${Date.now()}.json`;
    fs.writeFileSync(resultsFile, JSON.stringify(results, null, 2));
    console.log(`${colors.cyan}Results saved to: ${resultsFile}${colors.reset}\n`);

    return results;
}

// Run the tests
if (require.main === module) {
    runAllTests()
        .then(() => {
            console.log(`${colors.green}${colors.bright}All tests triggered successfully!${colors.reset}`);
            process.exit(0);
        })
        .catch(error => {
            console.error(`${colors.red}${colors.bright}Error running tests:${colors.reset}`, error);
            process.exit(1);
        });
}

module.exports = { runAllTests };
