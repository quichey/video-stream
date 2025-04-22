
"""
Planning out encapsulation/Black-boxing these Classes/API's


"""
class Cache():
    """
    Maybe make some sub-classes for:
    Foreign_key_data_store
    Primary_key_data_store

    and also move this Cache class to it's own file to keep this
    strucutre simpolified in terms of review/encapsulation
    """
    pk_definitions = {}
    # initialize the pk_definitions since we already have schema
    # init these caches, but I want to get data for these at the time of test-data creation
    # name is table_name, value is list of fk columns (name of column and parent table)
    fk_references = {}
    # name is table_name, value is set of primary-key values
    # TODO: think of at what instances i need to clear these caches
    # in terms of the use-cases of this Seed Class
    pk_values = {}
    # name is table_name, value is set of foreign-key values (also primary key if multi-col pk)
    fk_values_possible = {}
    fk_values_existing = {}
    # populate fk_values_existing with empty lists for each table
    def __init__(self, seed):

        self.seed = seed
        self.engine = seed.engine
        self.metadata_obj = seed.metadata_obj
        self.get_table_metadata = seed.get_table_metadata

        # initialize the pk_definitions since we already have schema
        self.init_pk_definitions()
        # populate fk_values_existing with empty lists for each table
        self.init_fk_values_existing()
        self.init_fk_references()   


    def get_parent_table_of_key(self, table_instance, column_name):
        # TODO: this line assumes only one foreign key for table_instance
        # for comments table, need to handle multiple FK(s) from Users/Videos
        # the idx 0 needs to change, but not sure what to
        parent_table_name = self.fk_references[table_instance.name][column_name]["parent_table_name"]
        return parent_table_name


    """
    create a record to be inserted into the DB
    mutate self.pk_values (which is the Seed's internal cache for starting up the DB with data)
    The structure of pk_values is a list of records (DB records in the form of a python dictionary)
    self.pk_values["users"] = [
        {"id": 0},
        {"id": 1},
    ]
    """
    def initialize_random_record_simple_pk(self, table):
        # check through list of already existing pk's
        # make a new one
        existing_values = self.get_table_key_values(table)
        #print(f"existing_values: {existing_values}")
        i = 0
        possible_pk_val = 1
        while i < len(existing_values):
            pk_rec = existing_values[i]
            random_bullshit =  pk_rec.values()
            if possible_pk_val not in random_bullshit:
                break
            i += 1
            possible_pk_val += 1
        """
        while random_var, i in existing_values:
            i += 1
        """
        pk_name = self.get_table_key_definition(table)[0]
        record = {}
        record[pk_name] = possible_pk_val
        print(f"\n possible_pk_val: {possible_pk_val} \n")
        self.pk_values[table.name].append(dict(record))
        return record
        
    def initialize_random_record_compound_pk(self, table):
        table_name = table.name
        fk_values_possible = self.get_foreign_key_values_possible(table_name)
        fk_values_existing = self.foreign_key_values_existing[table_name]

        for fk in fk_values_possible:
            already_exists = False
            for fk_2 in fk_values_existing:
                if fk == fk_2:
                    already_exists = True
                    break
            if already_exists:
                continue
    
            # add fk to fk_values_existing
            fk_values_existing.append(fk)
            return fk
    
    def create_random_value(self, column):
        data_type = column.type
        print(f"\n\n data_type: {data_type} \n\n")
        column_name = column.name
        table_name = column.table.name

        all_fk_info_list = self.fk_references[table_name]
        #is_foreign_key = False
        foreign_key_name = None

        print(f"\n\n all_fk_info_list: {all_fk_info_list} \n\n")
        for fk_info_column_name, fk_info in all_fk_info_list.items():
            #if fk_info["fk_column_name"] == column_name:
            if fk_info_column_name == column_name:
                #is_foreign_key = True
                foreign_key_name = fk_info["name_of_column_in_parent"]
                break

        #if is_foreign_key:
        if foreign_key_name is not None:
            # scan parent table
            # use metadata obj to query other table
            #return self.get_random_foreign_key(column)
            fk_curr = self.get_random_foreign_key(column.table, column_name)
            print(f"\n\n fk_curr: {fk_curr} \n\n")
            """
                fk_curr: {'id': 2}
                return fk_curr[fk_info["fk_column_name"]]

                need to save fk_info["fk_column_name"] from previous for loop
                i think this is fine. 
            """
            return fk_curr[foreign_key_name]
        
        def random_date(start_date, end_date):
            start_timestamp = time.mktime(start_date.timetuple())
            end_timestamp = time.mktime(end_date.timetuple())
            random_timestamp = random.uniform(start_timestamp, end_timestamp)
            return datetime.fromtimestamp(random_timestamp)
        hardcoded_end_date = datetime.now()
        hardcoded_start_date = hardcoded_end_date - relativedelta(years=10)


        if isinstance(data_type, Boolean):
            flag = random.randint(0, 1)
            return True if flag == 1 else False
        
        elif isinstance(data_type, Integer):
            return random.randint(0, 10000)
        
        elif isinstance(data_type, String):
            rand_int = random.randint(0, 10000)
            return f"{table_name}_{column_name}_{rand_int}"
        
        elif isinstance(data_type, DateTime):
            return random_date(hardcoded_start_date, hardcoded_end_date)

    def initialize_random_record(self, table):
        # try simplifying cases into single col pk and multi-col pk

        # need to alter a bit to do the case of comment_likes table
        # pk is multiple columns
        # so create_pk should return not just a single value
        # but a dictionary with each column name mapped to a fk value
        # and then set record to this dictionary
        pk_def = self.get_table_key_definition(table)

        if len(pk_def) == 1:
            return self.initialize_random_record_simple_pk(table)
        else:
            return self.initialize_random_record_compound_pk(table)

    def is_a_primary_key(self, table, column_name):
        pk_def = self.get_table_key_definition(table)
        if type(pk_def) is list:
            return column_name in pk_def
        else:
            return column_name == pk_def

    def create_random_record(self, table):
        # get table specs for table object
        # get column names and column types
        # use create_random_value
        # sqlalchemy may have function available to do this
        record = self.initialize_random_record(table)
        
        keys = table.c.keys()
        for key in keys:
            if self.is_a_primary_key(table, key):
                continue


            print(f"\n\n  table {table.name} creating column: {key} \n\n")
            column = getattr(table.c, key)
            record[key] = self.create_random_value(column)
        # probably convert record dictionary into sqlalchemy Record object type
        # maybe not if the insert function only requires a list of dicts
        return record

    """
    Return the number of records in the table
    datatype? let's just do an int for now
    """
    def get_size_of_table_data(self, table):

        pk_values = self.get_table_key_values(table)
        return len(pk_values)
    """
        table_name = table.name
        stmt = text(f"select count(*) from {table_name}")
        size = None
        with self.engine.connect() as conn:
            print(f"\n\n get count(*) from table: {table_name}")
            records = conn.execute(stmt)
            print(f"\n\n records: {records} \n\n")
            for row in records:
                print(f"\n\n row: {row} \n\n")
                size = row[0]

        if size is None:
            raise Exception("could not get table size")
        return size
    """

    def init_db(self, list_of_table_rand):
        with self.engine.connect() as conn:
            print(f"list_of_table_rand: {list_of_table_rand}")

            # users table keeps on inserting new records
            # i do not want this to happen
            # i want it to only insert records if the table is empty

            for table_info in list_of_table_rand:
                # populate table with random data
                num_records = table_info["num_records"]
                table_name = table_info["name"]
                table = self.seed.get_table_metadata(table_name)

                curr_size = self.get_size_of_table_data(table)
                if curr_size > 0:
                    continue

                records = []
                #packet_size = 100
                packet_size = 2
                def create_packet(curr_idx):
                    nonlocal records
                    while len(records) < packet_size:
                        records.append(self.create_random_record(table))
                        curr_idx += 1
                    stmt = insert(table).values(records)
                    conn.execute(stmt)
                    records = []
                    return curr_idx
                i = 0
                while i < num_records:
                    i = create_packet(i)

                """
                for i in range(num_records):
                    records.append(self.create_random_record(table))
                print(f"records: {records}")
                stmt = insert(table).values(records)
                conn.execute(stmt)
                """
                conn.commit()
        




