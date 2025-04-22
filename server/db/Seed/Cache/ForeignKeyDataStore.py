from .DataStore import DataStore

class ForeignKeyDataStore(DataStore):
        
    def init_fk_values_existing(self):
        all_tables = self.metadata_obj.tables.keys()
        for table_name in all_tables:
            self.fk_values_existing[table_name] = []
        
    def init_fk_references(self):
        all_tables = self.metadata_obj.tables.keys()
        for table_name in all_tables:
            self.fk_references[table_name] = []

            # get fk_refs on first pass in the case that users table already has data
            # think of better way maybe later
            table_instance = self.metadata_obj.tables[table_name]
            fk_references = self.get_foreign_key_references(table_instance)
            if fk_references is not None and len(fk_references) > 0:
                self.fk_references[table_name] = fk_references
                print(f"got fk_refs for table: {table_name}")

    def get_random_foreign_key(self, table_instance, column_name="name_of_col_in_table_instance"):
        # TODO: this line assumes only one foreign key for table_instance
        # for comments table, need to handle multiple FK(s) from Users/Videos
        parent_table_name = self.get_parent_table_of_key(table_instance, column_name)
        #parent_table = self.get_table_metadata(parent_table_name)

        parent_table = self.get_table_metadata(parent_table_name)
        pk_values = self.get_table_key_values(parent_table)
        num_vals = len(pk_values)
        random_idx = random.randint(0, num_vals - 1)
        return pk_values[random_idx]
        
    # just noticed
    # foreign_key values
    # are actually primary_keys for "complex" tables (multi-col pk tables)

    # TODO: i think need to add col_name to params
    def get_foreign_key_values_possible(self, table_instance):
        table_name = table_instance.name
        if table_name in self.fk_values_possible.keys():
            return self.fk_values_possible[table_name]
        
        print(f"\n\n get_foreign_key_values_possible {table_name} \n\n")
        
        fk_references = self.get_foreign_key_references(table_instance)
        possible = []
        # doing bfs (breadth-first-search)
        # TODO: review and update based off of new map structure
        """
        analsys: prob do not need idx

        i think the idea w/making a complicated recursion is
        making it possible for composite keys?
        maybe i should forget about this for now, the idea of working w/composite keys
        also maybe should apply to that job.


        """
        def traverse_references(idx, fk_dict_so_far):
            if idx >= len(fk_references):
                return
            ref = fk_references[idx]
            pk = ref["column_name"]
            pk_values = ref["foreign_key_values"]
            
            for val in pk_values:
                fk_dict = dict(fk_dict_so_far)
                fk_dict[pk] = val

                # if reached leaf node,
                # add fk_dict running data_thing
                # to list of possible fk_vals?
                if idx == len(fk_references) - 1:
                    possible.append(fk_dict)
                else:
                    traverse_references(idx + 1, fk_dict)
            
        empty_fk = {}
        traverse_references(0, empty_fk)

        self.fk_values_possible[table_name] = possible
        return possible


    """
    one_info: {'fk_column_name': 'id', 'column_name': 'user_id', 'table_name': 'users'}
    one_info: {'fk_column_name': 'id', 'column_name': 'video_id', 'table_name': 'videos'}

    maybe instead of making fk_references a list, make it a map from column_name -> rest_of_info
    fk_references = {
        "user_id": {
            "name_of_column_in_parent": "id",
            "parent_table_name": "users"
        },
        "video_id": {
            "name_of_column_in_parent": "id",
            "parent_table_name": "videos"
        }
    }

    RIGHT NOW, fk_references is a list of dictionaries, which makes finding specific fk_infos obscure
    Nested Dictionary will make accessing specific fk_infos easier/straightforward
    """
    def get_foreign_key_references(self, table_instance):
        child_table_name = table_instance.name
        #if child_table_name in self.fk_references.keys():
        if len(self.fk_references[child_table_name]) > 0:
            return self.fk_references[child_table_name]

        fks = table_instance.foreign_key_constraints
        fk_reference_info_map = {}
        for fk in fks:
            print(f"\n\n fk: {fk} \n\n")
            print(f"\n\n vars(fk): {vars(fk)} \n\n")
            # from vars(fk) in debugger
            # 'elements': [ForeignKey('users.id')]
            """
            foreign_key_obj = fk.elements[0]
            how to get 'users.id' ? don't know
            foreign_key_obj.column.name ---- maybe?
            this seems not good. if sqlalchemy changes it's internal logic, then this could break
            """
            foreign_key_obj = fk.elements[0]
            # this above case probably will not work for composite keys -- maybe it will idk

            one_info = {}

            one_info["fk_column_name"] = foreign_key_obj.column.name
            for column in fk.columns:
                one_info["column_name"] = column.name
            
            parent_table_name = fk.referred_table.name
            one_info["table_name"] = fk.referred_table.name

            parent_table = self.get_table_metadata(parent_table_name)
            one_info["foreign_key_values"] = self.get_table_key_values(parent_table)
            #TODO ?:
            # i think since i added the check on table size,
            # the python internal cache is not filling up with the enumeration
            # of primary keys for the parent table

            # Possible TODO fix error: maybe swap column_name and fk_column_name
            # checked reference data, should be correct as of now
            fk_reference_info_map[one_info["column_name"]] = {
                "name_of_column_in_parent": one_info["fk_column_name"],
                "parent_table_name": one_info["table_name"],
                "foreign_key_values": one_info["foreign_key_values"]
            }
        

        self.fk_references[child_table_name] = fk_reference_info_map
        return fk_reference_info_map    
    
    