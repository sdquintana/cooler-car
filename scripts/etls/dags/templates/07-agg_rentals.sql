INSERT INTO DIM.AGG_RENTALS
SELECT  DC.CAR_ID,
        COUNT(*) TOTAL_RENTS,
        DC.NIV CAR_REGISTRATION,
        LU_PAYMENT_METHOD_TYPE_DESCRIPTION_ES PAYMENT_METHOD,
        DC.YEAR  CAR_YEAR,
        DC.CAR_MODEL,
        DC.MOTOR_DESCRIPTION_ES,
        BO.BRANCH_OFFICE_NAME RENTA_BRANCH_OFFICE,
        BO.BRANCH_OFFICE_CP,
        BO.BRANCH_OFFICE_STATE,
        AVG(DATEDIFF(DELIVERY_DATE , RENTAL_DATE) )  AVG_DAYS,
        SUM(FARE) AS TOTAL_FARE,
        SUM(DAMAGE_FEE) AS TOTA_DAMAGE_FEE
FROM DIM.DIM_RENTAL DR
INNER JOIN DIM.DIM_CAR DC
ON DC.CAR_ID = DR.CAR_ID
INNER JOIN DIM.DIM_BRANCH_OFFICE BO
ON BO.BRANCH_OFFICE_ID = DR.BRANCH_OFFICE_ID

GROUP BY DC.CAR_ID,
         DC.NIV,
         DC.YEAR ,
         DC.CAR_MODEL ,
         DR.LU_PAYMENT_METHOD_TYPE_DESCRIPTION_ES,
         DC.MOTOR_DESCRIPTION_ES,
         BO.BRANCH_OFFICE_NAME,
         BO.BRANCH_OFFICE_CP,
         BO.BRANCH_OFFICE_STATE
ORDER BY 1
