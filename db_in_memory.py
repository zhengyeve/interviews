"""
Valon
Jan 12 2026

We want to build a lightweight, in-memory database that supports basic table operations. 

We will start with inserting rows into tables.
We should also be able to query specific columns from that table, similar to how SELECT works in SQL.


# db = Database()
# db.insert("employees", {"id": "0", "name": "Andrew Wang", "email": "andrew.wang@email.com"})
# db.insert("employees", {"id": "1", "name": "Jon Hsu", "email": "jon.hsu@email.com"})
# db.insert("employees", {"id": "2", "email": "help@email.com"})
# db.insert("employees", {"id": "2", "email": "support@email.com"})
# db.select("employees", ["name"])
# returns [{"name": "Andrew Wang"}, {"name": "Jon Hsu"}, {"name": None}]

# our select is effectively running `SELECT name FROM employees` against this database
# model and modify this class however you see fit

Extra Questions / Extension: 
Support WHERE clauses: 
# select name from employees where email = 'jon.hsu@email.com' AND id > '0'

"""

from pickle import FALSE


class Database:
    def __init__(self):
        # table in memory
        self.table_name_to_ids = {} # {"table_name": [ids]}
        self.id_to_data = {} # id = {table_name}_{id}

        ## maybe more stuff

    @staticmethod
    def __generate_id(table_name, id):
        # e.g. employees_0, employees_1, ...
        return "{}_{}".format(table_name, id)

    def __repr__(self):
        return "table_name_to_ids: {}\nid_to_data: {}".format(self.table_name_to_ids, self.id_to_data)

    @staticmethod
    def __doc_meets_condition(doc, condition):
        
        for col, op_val_dict in condition.items():
            val_in_doc = doc.get(col) 
            if not val_in_doc:
                return False

            op, val = list(op_val_dict.items())[0]

            try:
                if op == 'eq' and val_in_doc != val:
                    return False
                if op == 'gt' and val_in_doc <= val:
                    return False
                if op == 'lt' and val_in_doc >= val:
                    return False
            except TypeError:
                print('Can not compare condition with value in doc!! condition: {} vs. doc: {}'.format(
                    repr(condition), repr(doc)
                ))
                return False
            # more operators later
        return True


    def insert(self, table_name, doc):
        doc_id = doc.get('id')
        if doc_id is None:
            print("Error! no id in the doc for insert!")
            return
        if not table_name:
            print("Error! no table name for insert!")
            return
        id = Database.__generate_id(table_name, doc_id)

        # populate table name to id
        if table_name not in self.table_name_to_ids:
            self.table_name_to_ids[table_name] = set()   
        self.table_name_to_ids[table_name].add(id)

        # populate records
        # id is unique, update if id already exists 
        self.id_to_data[id] = doc

    def select(self, table_name, columns, condition={}):
        # unordered
        # db.select("employees", ["name"])
        # returns [{"name": "Andrew Wang"}, {"name": "Jon Hsu"}, {"name": None}]
        # condition: support WHERE clauses
        # e.g. select name from employees where email = 'jon.hsu@email.com' AND id > '0'. ==> condition: {"email": {"eq": "jon.hsu@email"}, com", "id": {"gt": "0"}} aka {column: {op: val}}
        #
        res = []
        all_ids = self.table_name_to_ids.get(table_name)
        if not all_ids:
            return res
        
        for id in all_ids:
            full_doc = self.id_to_data.get(id)
            doc = {}
            if not full_doc:
                continue

            # where clause
            if not Database.__doc_meets_condition(full_doc, condition):
                continue

            for col in columns:
                doc[col] = full_doc.get(col)
            res.append(doc)

        return res


db = Database()
db.insert("employees", {"id": "0", "name": "Andrew Wang", "email": "andrew.wang@email.com"})
db.insert("employees", {"id": "1", "name": "Jon Hsu", "email": "jon.hsu@email.com"})
db.insert("employees", {"id": "2", "email": "help@email.com"})
db.insert("employees", {"id": "2", "email": "support@email.com"})
# print(db)

res = db.select("employees", ["name"])
# print(res)
# returns [{"name": "Andrew Wang"}, {"name": "Jon Hsu"}, {"name": None}]


# support WHERE clauses
# select name from employees where email = 'jon.hsu@email.com' AND id > '0'
res = db.select("employees", ["name"], condition={"email":{ "eq": "jon.hsu@email.com"}, "id": {"gt": "0"}})
print(res)