SELECT
O.ID AS ID_ORDER,
C.ID AS ID_CUSTOMER,
O.ORDERED AS ORDERED_ALIAS,
O.DELIVERY AS DELIVERY_ALIAS,
C.NAME AS NAME_ALIAS
FROM ORDERS O
INNER JOIN CUSTOMERS C ON O.CUSTOMER_ID = C.ID
ORDER BY ID_ORDER;