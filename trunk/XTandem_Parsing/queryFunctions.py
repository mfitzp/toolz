def GET_TABLE(tableName):
    return 'SELECT * FROM %s'%tableName

def GET_UNIQUE_PROTEINS(tableName):
    '''
    Returns query to obtain unique proteins from a single table
    '''
    operatorList = ['MIN', 'AVG', 'AVG']
    colList = ['pep_eVal', 'pep_eVal','ppm_error']
    selStr = 'SELECT DISTINCT\n\t'
    keyID0 = 'pepID'
    keyID1 = 'proID'
    keyID2 = 'pro_eVal'
    querySep = ',\n\t'
    nameSep = '_'
    colSep = '.'
    fromStr = 'FROM\n\t'
    groupStr = 'GROUP BY\n\t'

    tblCol0 = tableName+colSep+keyID0
    tblCol1 = tableName+colSep+keyID1
    tblCol2 = tableName+colSep+keyID2

    execStr = selStr
    execStr+=tblCol1
    execStr+=querySep
    execStr+=tblCol2
    execStr+=querySep
    execStr+='COUNT('+tblCol0+')'+' AS pepIDCount'+querySep
    for i,op in enumerate(operatorList):
        tempCol = tableName+colSep+colList[i]
        tempStr = op+'('+tempCol+')'
        tempStr+= ' AS '+op+'_'+tableName+'_'+colList[i]+querySep

        execStr+=tempStr

    execStr = execStr[:-3]
    execStr+='\n'
    execStr+=fromStr
    execStr+=tableName+'\n'
    execStr+=groupStr
    execStr+=tblCol1
    execStr+=querySep
    execStr+=tblCol2
    execStr+='\nORDER BY\n\t'
    execStr+=tblCol1

    return execStr

def GET_UNIQUE_PEP_PRO_GROUP(tblList):
    '''
    returns a query string to obtain the unique peptides across multiple tables
    SELECT
        DISTINCT `pepID` from T1
        INTERSECT
    SELECT
        DISTINCT `pepID` from T2
        INTERSECT
    SELECT
        DISTINCT `pepID` from T3
        INTERSECT
    SELECT
        DISTINCT `pepID` from T4
        INTERSECT
    SELECT
        DISTINCT `pepID` from T5
    ORDER BY `pepID`

SELECT
    DISTINCT `pepID`,
    `proID` from T1
    INTERSECT
SELECT
    DISTINCT `pepID`,
    `proID` from T2
    INTERSECT
SELECT
    DISTINCT `pepID`,
    `proID` FROM T3
    INTERSECT
SELECT
    DISTINCT `pepID`,
    `proID` FROM T4
    INTERSECT
SELECT
    DISTINCT `pepID`,
    `proID` from T5
ORDER BY `pepID`

    '''
    print tblList
    colList = ['pepID']
    primKey = 'pepID'
    secondKey = 'proID'
    execStr = ''
    if len(tblList)>1:
        for i in xrange(len(tblList)-1):
            tbl = tblList[i]
            execStr+='SELECT\n\t'
            execStr+="`%s`, `%s` FROM %s\n\t"%(primKey, secondKey, tbl)
            execStr+='INTERSECT\n'
        tbl = tblList[-1]
        execStr+='SELECT\n\t'
        execStr+="`%s`, `%s` from %s\n"%(primKey, secondKey, tbl)
        execStr+="ORDER BY `%s`"%primKey
        return execStr
    else:
        return "Need more than 1 Table to compare"


def GET_COMMON_WITH_STATS(tblName, commonTable):
    '''
    SELECT DISTINCT
        T1.pepID,
        AVG(T1.ppm_error) AS AVG_T1_ppm_error,
        AVG(T1.pep_eVal) AS AVG_T1_pep_eVal,
        MIN(T1.pep_eVal) AS MIN_T1_pep_eVal,
        COUNT(T1.pepID) AS pepIDCount,
        T1.proID
    FROM
        T1 WHERE T1.pepID IN _CommonList
    GROUP BY
        T1.pepID
    '''
    selStr = 'SELECT DISTINCT\n\t'
    colList = ['pepID', 'ppm_error', 'pep_eVal', 'pep_eVal']
    primKey = 'pepID'
    endKey = 'proID'
    operatorList = [None, 'AVG', 'AVG', 'MIN']
    nameSep = '_'
    colSep = '.'
    groupStr = 'GROUP BY\n\t'

    fromStr = 'FROM\n\t'
    querySep = ',\n\t'
    retStr = '\n\t'

    for i,op in enumerate(operatorList):
        tempCol = tblName+colSep+colList[i]
        if op == None:
            selStr+=tempCol
        else:
            tempStr = op+'('+tempCol+')'
            tempStr+= ' AS '+op+'_'+tblName+'_'+colList[i]
            selStr+=tempStr

        selStr+=querySep

    selStr+='COUNT('+tblName+colSep+primKey+')'
    selStr+=' AS '+primKey+'Count'
    selStr+=querySep
    selStr+=tblName+colSep+endKey+'\n'
#        selStr = selStr[:-2]#remove last comma
    selStr += fromStr
    selStr += tblName + ' WHERE '
    selStr += tblName+colSep+primKey+' IN '+commonTable
    selStr += '\n'
#    i=0
#    for i,tbl in enumerate(tblList):
#        if i == 0:
#            selStr+=tbl
#        elif i < len(tblList):
#            selStr+=joinMainStr
#            selStr+=tbl
#            selStr+=onStr
#            selStr+='('
#            selStr+=tblList[i-1]+colSep+primKey
#            selStr+='='
#            selStr+=tbl+colSep+primKey
#            selStr+=')'
#        if i<len(tblList)-1:
#            selStr+=retStr
#        else:
#            selStr+='\n'

    selStr+=groupStr
    selStr+=tblName
    selStr+=colSep+primKey
#    selStr+=tblList[0]
#    selStr+=colSep+endKey

    execStr = selStr
    return execStr

def GET_UNIQUE_PEPTIDE_GROUP_SIMPLE(tblList):
    '''
    returns a query string to obtain the unique peptides across multiple tables
    SELECT
        DISTINCT `pepID` from T1
        INTERSECT
    SELECT
        DISTINCT `pepID` from T2
        INTERSECT
    SELECT
        DISTINCT `pepID` from T3
        INTERSECT
    SELECT
        DISTINCT `pepID` from T4
        INTERSECT
    SELECT
        DISTINCT `pepID` from T5
    ORDER BY `pepID`

    '''
    colList = ['pepID']
    primKey = 'pepID'
    execStr = ''
    if len(tblList)>1:
        for i in xrange(len(tblList)-1):
            tbl = tblList[i]
            execStr+='SELECT\n\t'
            execStr+="`%s` FROM %s\n\t"%(primKey,tbl)
            execStr+='INTERSECT\n'
        tbl = tblList[-1]
        execStr+='SELECT\n\t'
        execStr+="`%s` from %s\n"%(primKey,tbl)
        execStr+="ORDER BY `%s`"%primKey
        return execStr
    else:
        return "Need more than 1 Table to compare"

def GET_UNIQUE_PEPTIDE_GROUP(tblList):
    '''
    returns a query string to obtain the unique
    peptides across multiple tables
    '''

    if len(tblList)>0:
        selStr = 'SELECT DISTINCT\n\t'
        colList = ['pepID', 'ppm_error', 'pep_eVal', 'pep_eVal']
        primKey = 'pepID'
        endKey = 'proID'
        operatorList = [None, 'AVG', 'AVG', 'MIN']
        nameSep = '_'
        colSep = '.'
        groupStr = 'GROUP BY\n\t'

        joinStr = ''
        joinMainStr = 'INNER JOIN '
        fromStr = 'FROM\n\t'
        onStr = ' ON '
        andStr = ' AND '
        querySep = ',\n\t'
        retStr = '\n\t'

        for j,tbl in enumerate(tblList):
            for i,op in enumerate(operatorList):
                tempCol = tbl+colSep+colList[i]
                if op == None:
                    selStr+=tempCol
                else:
                    tempStr = op+'('+tempCol+')'
                    tempStr+= ' AS '+op+'_'+tbl+'_'+colList[i]
                    selStr+=tempStr

                selStr+=querySep

        selStr+='COUNT('+tbl+colSep+primKey+')'
        selStr+=' AS '+primKey+'Count'
        selStr+=querySep
        selStr+=tbl+colSep+endKey+'\n'
#        selStr = selStr[:-2]#remove last comma
        selStr += fromStr
        i=0
        for i,tbl in enumerate(tblList):
            if i == 0:
                selStr+=tbl
            elif i < len(tblList):
                selStr+=joinMainStr
                selStr+=tbl
                selStr+=onStr
                selStr+='('
                selStr+=tblList[i-1]+colSep+primKey
                selStr+='='
                selStr+=tbl+colSep+primKey
                selStr+=')'
            if i<len(tblList)-1:
                selStr+=retStr
            else:
                selStr+='\n'

        selStr+=groupStr
        selStr+=tblList[0]
        selStr+=colSep+primKey+querySep
        selStr+=tblList[0]
        selStr+=colSep+endKey

        execStr = selStr
        return execStr

def GET_UNIQUE_PEPTIDES_BY_PROTEIN(tableName):
    '''
    Returns query to obtain unique peptides from a single table sorted by protein
    '''
    operatorList = ['MIN', 'AVG', 'AVG']
    colList = ['pep_eVal', 'pep_eVal','ppm_error']
    selStr = 'SELECT DISTINCT\n\t'
    keyID1 = 'pepID'
    keyID2 = 'proID'
    querySep = ',\n\t'
    nameSep = '_'
    colSep = '.'
    fromStr = 'FROM\n\t'
    groupStr = 'GROUP BY\n\t'

    tblCol1 = tableName+colSep+keyID1
    tblCol2 = tableName+colSep+keyID2

    execStr = selStr
    execStr+=tblCol1
    execStr+=querySep
    execStr+=tblCol2
    execStr+=querySep
    execStr+='COUNT('+tblCol1+')'+' AS pepIDCount'+querySep
    for i,op in enumerate(operatorList):
        tempCol = tableName+colSep+colList[i]
        tempStr = op+'('+tempCol+')'
        tempStr+= ' AS '+op+'_'+tableName+'_'+colList[i]+querySep

        execStr+=tempStr

    execStr = execStr[:-3]
    execStr+='\n'
    execStr+=fromStr
    execStr+=tableName+'\n'
    execStr+=groupStr
    execStr+=tblCol1
    execStr+=querySep
    execStr+=tblCol2

    return execStr

def GET_UNIQUE_PEPTIDES(tableName):
    '''
    Returns query to obtain unique peptides from a single table
    '''
    selStr = 'SELECT DISTINCT '
    keyID = 'pepID'
    nameSep = '_'
    colSep = '.'
    fromStr = ' FROM '
    groupStr = ' GROUP BY '

    tblCol = tableName+colSep+keyID

    execStr = selStr
    execStr+=tblCol
    execStr+=fromStr
    execStr+=tableName
    execStr+=groupStr
    execStr+=tblCol

    return execStr


if __name__ == "__main__":
    ans = GET_UNIQUE_PEPTIDES('BSA')
    print ans
    print '1'
    print '\n'

    ans = GET_UNIQUE_PEPTIDES_BY_PROTEIN('BSATest')
    print ans
    print '2'
    print '\n'
    ans = GET_UNIQUE_PROTEINS('BSATest')
    print ans
    print '3'
    print '\n'
    tblList = ['T1', 'T2', 'T3']
    ans = GET_UNIQUE_PEPTIDE_GROUP(tblList)
    print ans
    print '4'
    tblList = ['T1', 'T2', 'T3']
    ans = GET_UNIQUE_PEPTIDE_GROUP_SIMPLE(tblList)
    print ans
    print '5'
    ans = GET_UNIQUE_PEP_PRO_GROUP(tblList)
    print ans
    print '6'
    ans = GET_COMMON_WITH_STATS('T1', '_CommonList')
    print ans
    print '7'


