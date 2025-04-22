from .DataStore import DataStore

class PrimaryKeyDataStore(DataStore):
    def init_pk_definitions(self):
        all_tables = self.metadata_obj.tables.values()
        for table_instance in all_tables:
            self.get_table_key_definition(table_instance)

    def get_table_key_values(self, table_instance):
        table_name = table_instance.name
        print(f"get_table_key_values table_instance: {table_instance}")
        if table_name in self.pk_values.keys() and len(self.pk_values[table_name]) > 0:
            return self.pk_values[table_name]

        pk_col_name = self.pk_definitions[table_name]
        pk_col_name = pk_col_name[0]
        print(f"pk_col_name: {pk_col_name}")
        pk_col = getattr(table_instance.c, pk_col_name)
        stmt = select(pk_col)
        values = []
        with self.engine.connect() as conn:
            print(f"\n\n get_table_key_values with self.engine.connect() as conn: {table_instance}")
            records = conn.execute(stmt)
            for row in records:
                val = {}
                #val[pk_col_name] = row[pk_col_name]
                val[pk_col_name] = row[0]
                values.append(val)
        self.pk_values[table_name] = values
        return values

    def get_table_key_definition(self, table_instance):
        table_name = table_instance.name
        if table_name in self.pk_definitions.keys():
            return self.pk_definitions[table_name]

        # remember to look at the structure of primary_key
        # and compare between the case of simple pk and
        # compound pk
        pk = table_instance.primary_key
        pk_defs = []
        for column in pk.columns:
            pk_defs.append(column.name)

        pk = table_instance.primary_key
        columns_pk = pk.columns
        #print(f"\n  vars(pk): {vars(pk)} \n")
        print(f"\n  columns_pk: {columns_pk} \n")
        #print(f"\n table_instance.primary_key:{table_instance.primary_key} \n")
        print(f"\n pk_defs:{pk_defs} \n")

        self.pk_definitions[table_name] = pk_defs
        return pk_defs
