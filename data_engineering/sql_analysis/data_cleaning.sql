SELECT *
from `lamia25.table1` 
WHERE 
  EmployeeID IS NULL OR
  FirstName IS NULL OR
  LastName IS NULL OR
  Gender IS NULL OR
  Age IS NULL OR
  BusinessTravel IS NULL OR
  Department IS NULL OR
  `DistanceFromHome KM` IS NULL OR
  State IS NULL OR
  Ethnicity IS NULL OR
  Education IS NULL OR
  EducationField IS NULL OR
  JobRole IS NULL OR
  MaritalStatus IS NULL OR
  Salary IS NULL OR
  StockOptionLevel IS NULL OR
  OverTime IS NULL OR
  HireDate IS NULL OR
  Attrition IS NULL OR
  YearsAtCompany IS NULL OR
  YearsInMostRecentRole IS NULL OR
  YearsSinceLastPromotion IS NULL OR
  YearsWithCurrManager IS NULL OR
  Age_Group IS NULL OR
  Full_State_Name IS NULL OR
  Salary_bins IS NULL OR
  EducationLevel IS NULL;


select EmployeeID,PerformanceID,
count(*) as cnt
from `lamia25.table2`
group by EmployeeID,PerformanceID
having count(*)>1;



