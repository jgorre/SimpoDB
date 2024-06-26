
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'AND COMMA CREATE EQUALS FROM GREATER_THAN GREATER_THAN_OR_EQUAL IDENTIFIER INSERT INT INTO KEY LESS_THAN LESS_THAN_OR_EQUAL LPAREN NOT_EQUALS NUMBER OR PRIMARY RPAREN SCHEMA SELECT STAR STRING TABLE VALUES WHEREsql_statement : query \n                     | create_schema\n                     | create_table\n                     | insert_statement\n    query : SELECT select_columns FROM IDENTIFIER\n             | SELECT select_columns FROM IDENTIFIER WHERE where_clausewhere_clause : where_item\n                    | where_item and_or where_clause\n                    | LPAREN where_clause RPAREN\n                    | LPAREN where_clause RPAREN and_or where_clauseand_or : AND\n              | ORwhere_item : IDENTIFIER where_item_operator number_or_stringwhere_item_operator : EQUALS\n                           | NOT_EQUALS\n                           | GREATER_THAN\n                           | GREATER_THAN_OR_EQUAL\n                           | LESS_THAN\n                           | LESS_THAN_OR_EQUALselect_columns : STAR COMMA select_columns\n                      | STAR\n                      | IDENTIFIER COMMA select_columns\n                      | IDENTIFIER\n    create_schema : CREATE SCHEMA IDENTIFIERcreate_table : CREATE TABLE IDENTIFIER LPAREN create_table_columns RPARENcreate_table_columns : table_column_definition COMMA create_table_columns\n                            | table_column_definition\n    table_column_definition : IDENTIFIER column_type\n                               | IDENTIFIER column_type PRIMARY KEY\n    column_type : INT\n                   | STRING\n    insert_statement : INSERT INTO IDENTIFIER LPAREN insert_column_names RPAREN VALUES insert_column_valuesinsert_column_names : IDENTIFIER COMMA insert_column_names\n                           | IDENTIFIER\n    insert_column_values : LPAREN insert_values RPAREN COMMA insert_column_values\n                            | LPAREN insert_values RPAREN\n    insert_values : number_or_string COMMA insert_values\n                     | number_or_string\n    number_or_string : STRING\n                            | NUMBER\n    '
    
_lr_action_items = {'SELECT':([0,],[6,]),'CREATE':([0,],[7,]),'INSERT':([0,],[8,]),'$end':([1,2,3,4,5,18,21,33,34,39,58,59,60,61,62,65,69,70,74,],[0,-1,-2,-3,-4,-24,-5,-6,-7,-25,-13,-39,-40,-8,-9,-32,-10,-36,-35,]),'STAR':([6,16,17,],[11,11,11,]),'IDENTIFIER':([6,12,13,14,15,16,17,24,25,26,35,40,41,50,51,52,66,],[10,18,19,20,21,10,10,27,30,32,32,27,30,32,-11,-12,32,]),'SCHEMA':([7,],[12,]),'TABLE':([7,],[13,]),'INTO':([8,],[14,]),'FROM':([9,10,11,22,23,],[15,-23,-21,-22,-20,]),'COMMA':([10,11,29,30,36,37,38,59,60,63,68,70,],[16,17,40,41,-28,-30,-31,-39,-40,-29,71,72,]),'LPAREN':([19,20,26,35,50,51,52,57,66,72,],[24,25,35,35,35,-11,-12,64,35,64,]),'WHERE':([21,],[26,]),'INT':([27,],[37,]),'STRING':([27,43,44,45,46,47,48,49,64,71,],[38,59,-14,-15,-16,-17,-18,-19,59,59,]),'RPAREN':([28,29,30,31,34,36,37,38,53,55,56,58,59,60,61,62,63,67,68,69,73,],[39,-27,-34,42,-7,-28,-30,-31,62,-26,-33,-13,-39,-40,-8,-9,-29,70,-38,-10,-37,]),'EQUALS':([32,],[44,]),'NOT_EQUALS':([32,],[45,]),'GREATER_THAN':([32,],[46,]),'GREATER_THAN_OR_EQUAL':([32,],[47,]),'LESS_THAN':([32,],[48,]),'LESS_THAN_OR_EQUAL':([32,],[49,]),'AND':([34,58,59,60,62,],[51,-13,-39,-40,51,]),'OR':([34,58,59,60,62,],[52,-13,-39,-40,52,]),'PRIMARY':([36,37,38,],[54,-30,-31,]),'VALUES':([42,],[57,]),'NUMBER':([43,44,45,46,47,48,49,64,71,],[60,-14,-15,-16,-17,-18,-19,60,60,]),'KEY':([54,],[63,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'sql_statement':([0,],[1,]),'query':([0,],[2,]),'create_schema':([0,],[3,]),'create_table':([0,],[4,]),'insert_statement':([0,],[5,]),'select_columns':([6,16,17,],[9,22,23,]),'create_table_columns':([24,40,],[28,55,]),'table_column_definition':([24,40,],[29,29,]),'insert_column_names':([25,41,],[31,56,]),'where_clause':([26,35,50,66,],[33,53,61,69,]),'where_item':([26,35,50,66,],[34,34,34,34,]),'column_type':([27,],[36,]),'where_item_operator':([32,],[43,]),'and_or':([34,62,],[50,66,]),'number_or_string':([43,64,71,],[58,68,68,]),'insert_column_values':([57,72,],[65,74,]),'insert_values':([64,71,],[67,73,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> sql_statement","S'",1,None,None,None),
  ('sql_statement -> query','sql_statement',1,'p_sql_statement','parse.py',11),
  ('sql_statement -> create_schema','sql_statement',1,'p_sql_statement','parse.py',12),
  ('sql_statement -> create_table','sql_statement',1,'p_sql_statement','parse.py',13),
  ('sql_statement -> insert_statement','sql_statement',1,'p_sql_statement','parse.py',14),
  ('query -> SELECT select_columns FROM IDENTIFIER','query',4,'p_query','parse.py',19),
  ('query -> SELECT select_columns FROM IDENTIFIER WHERE where_clause','query',6,'p_query','parse.py',20),
  ('where_clause -> where_item','where_clause',1,'p_where_clause','parse.py',31),
  ('where_clause -> where_item and_or where_clause','where_clause',3,'p_where_clause','parse.py',32),
  ('where_clause -> LPAREN where_clause RPAREN','where_clause',3,'p_where_clause','parse.py',33),
  ('where_clause -> LPAREN where_clause RPAREN and_or where_clause','where_clause',5,'p_where_clause','parse.py',34),
  ('and_or -> AND','and_or',1,'p_and_or','parse.py',60),
  ('and_or -> OR','and_or',1,'p_and_or','parse.py',61),
  ('where_item -> IDENTIFIER where_item_operator number_or_string','where_item',3,'p_where_item','parse.py',66),
  ('where_item_operator -> EQUALS','where_item_operator',1,'p_where_item_operator','parse.py',71),
  ('where_item_operator -> NOT_EQUALS','where_item_operator',1,'p_where_item_operator','parse.py',72),
  ('where_item_operator -> GREATER_THAN','where_item_operator',1,'p_where_item_operator','parse.py',73),
  ('where_item_operator -> GREATER_THAN_OR_EQUAL','where_item_operator',1,'p_where_item_operator','parse.py',74),
  ('where_item_operator -> LESS_THAN','where_item_operator',1,'p_where_item_operator','parse.py',75),
  ('where_item_operator -> LESS_THAN_OR_EQUAL','where_item_operator',1,'p_where_item_operator','parse.py',76),
  ('select_columns -> STAR COMMA select_columns','select_columns',3,'p_select_columns','parse.py',81),
  ('select_columns -> STAR','select_columns',1,'p_select_columns','parse.py',82),
  ('select_columns -> IDENTIFIER COMMA select_columns','select_columns',3,'p_select_columns','parse.py',83),
  ('select_columns -> IDENTIFIER','select_columns',1,'p_select_columns','parse.py',84),
  ('create_schema -> CREATE SCHEMA IDENTIFIER','create_schema',3,'p_create_schema','parse.py',92),
  ('create_table -> CREATE TABLE IDENTIFIER LPAREN create_table_columns RPAREN','create_table',6,'p_create_table','parse.py',99),
  ('create_table_columns -> table_column_definition COMMA create_table_columns','create_table_columns',3,'p_create_table_columns','parse.py',115),
  ('create_table_columns -> table_column_definition','create_table_columns',1,'p_create_table_columns','parse.py',116),
  ('table_column_definition -> IDENTIFIER column_type','table_column_definition',2,'p_table_column_definition','parse.py',124),
  ('table_column_definition -> IDENTIFIER column_type PRIMARY KEY','table_column_definition',4,'p_table_column_definition','parse.py',125),
  ('column_type -> INT','column_type',1,'p_column_type','parse.py',133),
  ('column_type -> STRING','column_type',1,'p_column_type','parse.py',134),
  ('insert_statement -> INSERT INTO IDENTIFIER LPAREN insert_column_names RPAREN VALUES insert_column_values','insert_statement',8,'p_insert_statement','parse.py',139),
  ('insert_column_names -> IDENTIFIER COMMA insert_column_names','insert_column_names',3,'p_insert_column_names','parse.py',146),
  ('insert_column_names -> IDENTIFIER','insert_column_names',1,'p_insert_column_names','parse.py',147),
  ('insert_column_values -> LPAREN insert_values RPAREN COMMA insert_column_values','insert_column_values',5,'p_insert_column_values','parse.py',155),
  ('insert_column_values -> LPAREN insert_values RPAREN','insert_column_values',3,'p_insert_column_values','parse.py',156),
  ('insert_values -> number_or_string COMMA insert_values','insert_values',3,'p_insert_values','parse.py',165),
  ('insert_values -> number_or_string','insert_values',1,'p_insert_values','parse.py',166),
  ('number_or_string -> STRING','number_or_string',1,'p_number_or_string','parse.py',174),
  ('number_or_string -> NUMBER','number_or_string',1,'p_number_or_string','parse.py',175),
]
