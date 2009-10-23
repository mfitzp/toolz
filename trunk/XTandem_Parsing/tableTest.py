'''
SELECT DISTINCT
  BSATest.pepID,
  BSATest.pep_eVal,
  BSATest.ppm_error,
  Oct_20_BSA.ppm_error,
  Oct_20_BSA.pepID,
  Oct_20_BSA.pep_eVal,
  bsa_Test.pepID,
  bsa_Test.pep_eVal,
  bsa_Test.ppm_error,
  BSATest.proID,
  Oct_20_BSA.proID,
  bsa_Test.proID
FROM
 BSATest
 INNER JOIN Oct_20_BSA ON (BSATest.pepID=Oct_20_BSA.pepID)
 INNER JOIN bsa_Test ON (Oct_20_BSA.pepID=bsa_Test.pepID)


SELECT DISTINCT
  BSATest.pepID,
  Oct_20_BSA.pepID,
  bsa_Test.pepID,
  AVG(bsa_Test.pep_eVal) AS FIELD_1,
  AVG(Oct_20_BSA.pep_eVal) AS FIELD_2,
  AVG(BSATest.pep_eVal) AS FIELD_3
FROM
 BSATest
 INNER JOIN Oct_20_BSA ON (BSATest.pepID=Oct_20_BSA.pepID)
 INNER JOIN bsa_Test ON (Oct_20_BSA.pepID=bsa_Test.pepID)
GROUP BY
  BSATest.pepID,
  Oct_20_BSA.pepID,
  bsa_Test.pepID
ORDER BY
  BSATest.pep_eVal

'''

tables = ['BSATest', 'Oct_20_BSA', 'bsa_Test']#, 'YP_TSB_2', 'GoJoe']
keyWordList = ['SELECT', 'FROM', 'WHERE', 'AND']
primKey = 'pepID'
execStr = ''
distStr = 'DISTINCT '
selectStr = 'SELECT '
whereStr = ' WHERE '
joinStr = ''
joinMainStr = ' INNER JOIN '
fromStr = ' FROM '
onStr = ' ON ('
andStr = ' AND '
querySep = ', '
numTables = len(tables)

selectStr+=distStr
fromStr+=tables[0]
for i,tableName in enumerate(tables):
    selectStr+=tableName
    selectStr+='.*'


    if i == numTables-1:
        continue
#    elif i>0:
    else:
        selectStr+=querySep
        joinStr+=joinMainStr
        joinStr+=tables[i+1]
        joinStr+=onStr
        joinStr+=tableName
        joinStr+='.'
        joinStr+=primKey
        joinStr+= ' = '
        joinStr+=tables[i+1]
        joinStr+='.'
        joinStr+=primKey
        joinStr+=')'
#    else:
#        fromStr+=tableName
#        fromStr+=joinStr
#        fromStr+=tables[i+1]
#        fromStr+=onStr
#        fromStr+=tableName
#        fromStr+='.'
#        fromStr+=primKey
#        fromStr+= ' = '
#        fromStr+=tables[i+1]
#        fromStr+='.'
#        fromStr+=primKey
#        fromStr+=')'
#        fromStr+=querySep
#
#        selectStr+=querySep
#
#        whereStr+=tables[0]
#        whereStr+='.'
#        whereStr+=primKey
#        whereStr+= ' = '
#        whereStr+=tables[i+1]
#        whereStr+='.'
#        whereStr+=primKey
#
#    if i < numTables-2:
#        whereStr+=andStr


selectStr += fromStr
selectStr += joinStr
#selectStr += whereStr

print selectStr