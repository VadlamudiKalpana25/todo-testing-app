Feature: Todo Management

  Scenario: User registers successfully
    Given the API is running
    When I register with email "bdd1@test.com" and password "Password@123"
    Then the response status should be 200

  Scenario: User logs in and receives token
    Given the API is running
    When I login with email "bdd1@test.com" and password "Password@123"
    Then the response status should be 200
    And I should receive a token

  Scenario: Logged-in user creates a todo
    Given the API is running
    And I am logged in as "bdd1@test.com" with password "Password@123"
    When I create a todo with title "BDD Todo 1"
    Then the response status should be 200
    And the response should contain "id"
