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


def GET_UNIQUE_PEPTIDE_GROUP_SIMPLE(tblList):
    '''
    returns a query string to obtain the unique peptides across multiple tables
    '''

    if len(tblList)>0:
        selStr = 'SELECT DISTINCT\n\t'
        colList = ['pepID']
        primKey = 'pepID'
        endKey = 'proID'
        operatorList = [None]
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

def GET_UNIQUE_PEPTIDE_GROUP(tblList):
    '''
    returns a query string to obtain the unique peptides across multiple tables
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
    tblList = ['BSATest', 'OCT_20_BSA', 'bsa_Test']
    ans = GET_UNIQUE_PEPTIDE_GROUP(tblList)
    print ans
    print '4'
    tblList = ['T1', 'T2', 'T3', 'T4']
    ans = GET_UNIQUE_PEPTIDE_GROUP_SIMPLE(tblList)
    print ans
    print '5'