create table lamia25.table2 as 
SELECT PerformanceID, EmployeeID, ReviewDate, E5.SatisfactionLevel as EnvironmentSatisfaction, 
E6.SatisfactionLevel as JobSatisfaction, 
E7.SatisfactionLevel as RelationshipSatisfaction, 
TrainingOpportunitiesWithinYear, TrainingOpportunitiesTaken, WorkLifeBalance,
E3.RatingLevel as SelfRating, ManagerRating
from `lamia25.PerformanceRating` E2

join `lamia25.RatingLevel` E3
on E2.SelfRating=E3.RatingID

join `lamia25.RatingLevel` E4
on E2.ManagerRating=E4.RatingID

join `lamia25.SatisfiedLevel` E5
on E2.EnvironmentSatisfaction=E5.SatisfactionID

join `lamia25.SatisfiedLevel` E6
on E2.JobSatisfaction=E6.SatisfactionID

join `lamia25.SatisfiedLevel` E7
on E2.RelationshipSatisfaction=E7.SatisfactionID;