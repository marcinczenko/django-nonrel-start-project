Feature: Walking skeleton
  In order to start development at a sustainable pace
  As a developer
  I would like to deliver a simple functionality that triggers initial architectural discussion and drives creating the testing infrastructure

Scenario: Retrieving simple text items from the server
  When I send GET request to the Google App Engine web app
  Then I should receive all text items from the server
