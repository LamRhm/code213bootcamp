CREATE TABLE 890.table1 AS
    SELECT EmployeeID ,
         FirstName,
         LastName,
         CONCAT(FirstName,' ',LastName)
         Gender, 
         BusinessTravel,
          Department, 
          DistanceFromHome KM,
           State, 
           Ethnicity,
            Education, EducationField,
             JobRole, MaritalStatus, 
             StockOptionLevel, OverTime, HireDate,
              Attrition, YearsAtCompany,
               YearsInMostRecentRole,
                YearsSinceLastPromotion, 
                YearsWithCurrManager
   AGE,
   CASE 
       WHEN Age BETWEEN 18 AND 24 THEN '18-24'
       WHEN Age BETWEEN 25 AND 31 THEN '25-31'
       WHEN Age BETWEEN 32 AND 38 THEN '32-38'
       WHEN Age BETWEEN 39 AND 45 THEN '39-45'
       WHEN AGE BETWEEN 46 AND 51 THEN '46-51'
       ELSE 'Other'
   END as Age_Group,
   CASE 
         WHEN State= 'CA' THEN 'California'
         WHEN State= 'IL' THEN 'Illinois'
         WHEN State= 'NY' THEN 'New York'
     ELSE 'Unknown'
    END AS Full_State_Name,
  Salary ,
   Case 
       WHEN Salary BETWEEN 20387 AND 50000 THEN 'Under 50k'
       WHEN Salary BETWEEN 50001 AND 150000 THEN '50k-150K'
       WHEN Salary BETWEEN 150001 AND 300000 THEN '150k-300K' 
       WHEN Salary BETWEEN 300001 AND 500000 THEN '300K-500k'
       WHEN Salary>500000  THEN 'Above 5Lac'
       ELSE 'Unknown'
    END AS Salary_Bin,
    E1.EducationLevel,
    FROM 890.Employee E
    -- joining emlployee table with EducationalLevel 
    JOIN 890.EducationLevel E1
    ON E.Education= E1.EducationLevelID;
