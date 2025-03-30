Feature: Update cryptocurrency metadata  
  As an API user  
  I want to update the metadata of a cryptocurrency  
  So that I have the latest information  

  Scenario: Successfully updating cryptocurrency data  
    Given the cryptocurrency "BTC" exists in the database  
    When I trigger a metadata update  
    Then the cryptocurrency metadata is updated from the CoinGecko API  