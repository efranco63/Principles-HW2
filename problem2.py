import sys
import csv

# Clears the database except for the headers
def clear():
    i = len(database)
    while i > 1:
        database.pop(len(database)-1)
        i -= 1

# Inserts a job offer into the database.
def insert(fieldValues):
    for i in range(1,len(database)):
        if fieldValues[0] == database[i][0]:
            return
    database.append(fieldValues)

# Updates all job offers that attend the field_name=old_value pair.
def update_all(params):
    query_field_name = params[0]
    query_field_value = params[1]
    update_field_name = params[2]
    update_field_value = params[3]
    for i,j in enumerate(database[0]):
        if j == query_field_name:
            index1 = i
        if j == update_field_name:
            index2 = i
    update = 0
    for i in range(1,len(database)):
        if query_field_value == database[i][index1]:
            database[i][index2] = update_field_value
            update += 1
    updates.append(update)  

# Deletes all job offers that attend the field_name=field_value pair.
def delete_all(params):
    field_name, field_value = params
  
  # TODO Complete with your code and remove print below.
  # print 'delete_all where ' + field_name + '=' + field_value


# Prints all job offers that match the query field_name=field_value, one per
# line, semicolon-separated, with fields in the order defined in the assignment.
def find(params):
    field_name, field_value = params

  # TODO Complete with your code and remove print below.
  # print 'find where ' + field_name + '=' + field_value


# Prints how many job offers match the query field_name=field_value.
def count(params):
    field_name, field_value = params
    
    # TODO Complete with your code and remove print below.
    # print 'count job offers where ' + field_name + '=' + field_value

def count_unique(params):
    params = params

# Prints all job offers in the database, one per line, semicolon-separated, with
# fields in the order defined in the assignment.
def dump():
    dbs = database
    dbs.pop(0)
    dbs.sort(key=lambda x: x[0])
    content = ''
    contents = []
    for i in range(0,len(updates)):
        updates[i] = str(updates[i])
    contents.append('\n'.join(updates))
    for row in dbs:
        contents.append('|'.join(map(str, row)))
    content = '\n'.join(contents)
    print content
  
def view(fieldNames):
    # TODO Complete with your code and remove print below.
    # print 'view for fields ' + str(fieldNames)
    fieldNames = fieldNames

def executeCommand(commandLine):
    tokens = commandLine.split('|') #assume that this symbol is not part of the data
    command = tokens[0]
    parameters = tokens[1:]
    
    if command == 'insert':
        insert(parameters)
    elif command == 'delete_all':
        delete_all(parameters)
    elif command == 'update_all':
        update_all(parameters)
    elif command == 'find':
        find(parameters)
    elif command == 'count':
        count(parameters)
    elif command == 'count_unique':
        count_unique(parameters)
    elif command == 'clear':
        clear()
    elif command == 'dump':
        dump()
    elif command == 'view':
        view(parameters)
    else:
        print 'ERROR: Command %s does not exist' % (command,)
        assert(False)

def executeCommands(commandFileName):
    f = open(commandFileName)
    for line in f:
        executeCommand(line.strip())

if __name__ == '__main__':
    # load data from database
    with open('NYC_Jobs_sample.csv', 'rb') as f:
        reader = csv.reader(f,delimiter='|')
        database = []
        for row in reader:
            database.append(row)
    headers = database[0] #save the header row in case it gets popped
    updates = []
    # Read the command text file
    executeCommands(sys.argv[1])
    # Write database to text file
    if headers != database[0]:
        database.insert(0,headers)
    contents = []
    content = ''
    for row in database:
        contents.append('|'.join(map(str, row)))
    content = '\n'.join(contents)
    txtfile = open('db.txt','w')
    txtfile.write(content)
    txtfile.close