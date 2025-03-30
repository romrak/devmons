Feature: Add a new cryptocurrency  
  As an API user  
  I want to add a cryptocurrency to the database  
  So that I can track its value  

  Scenario: Successfully adding a cryptocurrency  
    Given I provide the symbol of an existing cryptocurrency "BTC"  
    When I send a request to create the cryptocurrency  
    Then the cryptocurrency "BTC" is stored in the database  
    And the cryptocurrency metadata is retrieved from the CoinGecko API  

  Scenario: Adding a non-existing cryptocurrency  
    Given I provide the symbol of a non-existing cryptocurrency "FAKECOIN"  
    When I send a request to create the cryptocurrency  
    Then I receive an error "Cryptocurrency does not exist"  
    And the cryptocurrency is not stored in the database  