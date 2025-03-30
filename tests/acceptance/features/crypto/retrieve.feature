Feature: Retrieve cryptocurrency list  
  As an API user  
  I want to fetch a list of stored cryptocurrencies
  So that I can see which cryptocurrencies I am tracking  

  Scenario: The list contains stored cryptocurrencies  
    Given I have cryptocurrencies "BTC" and "ETH" in the database  
    When I send a request to fetch the cryptocurrency list  
    Then I receive a list containing "BTC" and "ETH"