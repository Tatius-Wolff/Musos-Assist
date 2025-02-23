Feature: View a music single release

  Scenario: View a music single release
    Given I have a music single release "Single Title"
    When I view the details of the release
    Then I should see the following information:
      | field       | value         |
      | title       | [Single Title]|
      | artist      | [Artist Name] |
      | release-date| [Date]        |
      | genre       | [Genre]       |
      | duration    | [Duration]    |

