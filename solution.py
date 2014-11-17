import sys
import os

# Clears the database except for the headers
def clear():
    if database != {}:
        headers = database['Headers']
        database.clear()
        database['Headers'] = headers

# Inserts a job offer into the database.
def insert(fieldValues):
    if fieldValues[0] in database:
            return
    else:
        database[fieldValues[0]] = fieldValues[1:]
    
# Updates all job offers that attend the field_name=old_value pair.
def update_all(params):
    query_field_name = params[0]
    query_field_value = params[1]
    update_field_name = params[2]
    update_field_value = params[3]           
    if query_field_name in database['Headers']:
        for i in range(0,len(database['Headers'])):
            if query_field_name == database['Headers'][i]:
                indexq = i
            if update_field_name == database['Headers'][i]:
                indexu = i
        update = 0
        for key in database:
            if query_field_value == database[key][indexq]:
                database[key][indexu] = update_field_value
                update += 1
        updates.append(update)
    if query_field_name == 'Job ID' and query_field_value in database:
        for i in range(0,len(database['Headers'])):
            if update_field_name == database['Headers'][i]:
                indexu = i
        update = 0
        database[query_field_value][indexu] = update_field_value
        update += 1
        updates.append(update)  

# Deletes all job offers that attend the field_name=field_value pair.
def delete_all(params):
    field_name, field_value = params
    if field_name in database['Headers']:
        for i in range(0,len(database['Headers'])):
            if field_name == database['Headers'][i]:
                index = i
        remove = []
        for key in database:
            if field_value == database[key][index]:
                remove.append(key)
        for i in remove:
            del database[i]
    elif field_name == 'Job ID':
        del database[field_value]

# Prints all job offers that match the query field_name=field_value, one per
# line, semicolon-separated, with fields in the order defined in the assignment.
def find(params):
    field_name, field_value = params
    fields_l = []
    if field_name != 'Job ID':
        for i in range(0,len(database['Headers'])):
            if field_name == database['Headers'][i]:
                index = i
    for key in database:
        if field_name == 'Job ID':
            if field_value == key:
                entry = database[field_value]
                entry.insert(0,key)
                fields_l.append(entry)
        elif field_value == database[key][index]:
            entry = database[key]
            entry.insert(0,key)
            fields_l.append(entry)
    fields_l.sort(key=lambda x: x[0])
    for i in range(0,len(fields_l)):
        d = fields_l[i]
        fields_l[i] = '|'.join(d)
    if fields_l != []:
        print '\n'.join(fields_l)

# Prints how many job offers match the query field_name=field_value.
def count(params):
    field_name, field_value = params
    if field_name != 'Job ID':
        # determine the index of the field name in the list of headers
        for i in range(0,len(database['Headers'])):
            if field_name == database['Headers'][i]:
                index = i
        # count the number of job offers that have that value
        count = 0
        for key in database:
            if field_value == database[key][index]:
                count += 1
        print 'There are ' + str(count) + ' job offers where ' + field_name + '=' + field_value
    else:
        print 'There is only one job offer per Job ID'

# Prints all job offers in the database, one per line, semicolon-separated, with
# fields in the order defined in the assignment.
def dump():
    contents = []
    if updates != []:
        for i in range(0,len(updates)):
            updates[i] = str(updates[i])
        contents.append('\n'.join(updates))
    for key in sorted(database):
        if key != 'Headers':
            contents.append(key + '|' + '|'.join(map(str, database[key])))
    content = '\n'.join(contents)
    print content
  
def view(fieldNames):
    fn_dict = {}
    for fn in fieldNames:
        for i in range(0,len(database['Headers'])):
            if fn == database['Headers'][i]:
                fn_dict[fn] = i  
    for key in database:
        if key != 'Headers':
            views = []
            for fn in fieldNames:
                if fn == 'Job ID':
                    views.append(key)
                else:
                    views.append(database[key][fn_dict[fn]])
            view_list.append(views)
    view_list.sort(key=lambda x: x[1])
    for i in range(0,len(view_list)):
        d = view_list[i]
        view_list[i] = '|'.join(d)
    print '\n'.join(view_list)

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
    # read database from file, if one does not already exist, create an empty dictionary
    if os.path.isfile('db.txt'):
        f = open('db.txt')
        counter = 0
        database = {}
        for line in f:
            row = line.split('|')
            if counter == 0:
                database['Headers'] = row[1:]
                counter += 1
            else:
                database[row[0]] = row[1:]
    else:
        database = {}
        headers = ['Agency','# of Positions','Business Title','Civil Service Title','Salary Range From','Salary Range To','Salary Frequency','Work Location','Division/Work Unit','Job Description','Minimum Qual Requirements','Preferred Skills','Additional Information'] 
        database['Headers'] = headers 

    updates = []
    view_list = []
    # Read the command text file
    executeCommands(sys.argv[1])
    # Write database to text file
    database['Headers'].insert(0,'Job ID')
    database['Headers'][len(database['Headers'])-1] = database['Headers'][len(database['Headers'])-1].rstrip('\n')
    contents = []
    contents.append('|'.join(database['Headers']))
    content = ''
    for key in database:
        if key != 'Headers':
            contents.append(key + '|' + '|'.join(map(str, database[key])))
    content = '\n'.join(contents)
    txtfile = open('db.txt','w')
    txtfile.write(content)
    txtfile.close