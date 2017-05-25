import mysql.connector, sys
import subprocess, json

cnx = mysql.connector.connect(user='ethgas', password='station', host='127.0.0.1', database='tx')
cursor = cnx.cursor()



startBlock = int(sys.argv[1])
endBlock = int(sys.argv[2])

addBlock = ("INSERT INTO speedo2 "
            "(blockNum, miner, blockHash, blockFee, gasUsed, uncsReported, main, uncle) "
            "VALUES (%(blockNum)s, %(miner)s, %(hash)s, %(blockFee)s, %(gasUsed)s, %(uncsReported)s, %(main)s, %(uncle)s)")
#write Main Blocks
for block in range (startBlock, endBlock):
    block = str(block)
    print (block)
    out = subprocess.check_output(['node', 'getBlocks.js', block])
    blockData = json.loads(out)
    print(blockData)
    cursor.execute(addBlock, blockData)
    print(cursor.statement)
    cnx.commit()





