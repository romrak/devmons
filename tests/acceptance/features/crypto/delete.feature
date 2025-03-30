Feature: Delete a cryptocurrency  
  As an API user  
  I want to remove a cryptocurrency from the database  
  So that it is no longer tracked  

  Scenario: Successfully deleting a cryptocurrency  
    Given the cryptocurrency "BTC" exists in the database  
    When I send a request to delete the cryptocurrency "BTC"  
    Then the cryptocurrency "BTC" is removed from the database  
    And it is no longer present in the cryptocurrency list  