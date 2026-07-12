# Use Case Diagram

```mermaid
usecaseDiagram
    actor Student
    actor ClubPresident as "Club President"
    actor CollegeAdmin as "College Admin"
    actor SuperAdmin as "Super Admin"

    package "IEMS System" {
        usecase "View Public Portal" as UC1
        usecase "View Events & Notices" as UC2
        usecase "Submit Event Proposal" as UC3
        usecase "Submit Notice" as UC4
        usecase "Manage Club Profile" as UC5
        usecase "Approve/Reject Content" as UC6
        usecase "Manage Users" as UC7
        usecase "System Settings" as UC8
        usecase "View Reports" as UC9
    }

    Student --> UC1
    Student --> UC2

    ClubPresident --> UC1
    ClubPresident --> UC2
    ClubPresident --> UC3
    ClubPresident --> UC4
    ClubPresident --> UC5

    CollegeAdmin --> UC1
    CollegeAdmin --> UC2
    CollegeAdmin --> UC6
    CollegeAdmin --> UC9

    SuperAdmin --> UC1
    SuperAdmin --> UC6
    SuperAdmin --> UC7
    SuperAdmin --> UC8
    SuperAdmin --> UC9
```
