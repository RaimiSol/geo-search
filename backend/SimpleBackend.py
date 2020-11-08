
# coding: utf-8


from flask import Flask, render_template
from flask_restful import Api, Resource
from webargs import fields
from webargs.flaskparser import use_args
import sqlalchemy
from flask_cors import CORS




app = Flask(__name__,
            static_folder = "../frontend/dist/static",
            template_folder = "../frontend/dist")

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")
api = Api(app)



def connect(user, password, db, host='localhost', port=5432):
    '''Returns a connection and a metadata object'''
    # We connect with the help of the PostgreSQL URL
    # postgresql://federer:grandestslam@localhost:5432/tennis
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)

    # The return value of create_engine() is our connection object
    con = sqlalchemy.create_engine(url, client_encoding='utf8')

    # We then bind the connection to MetaData()
    meta = sqlalchemy.MetaData(bind=con)
    meta.reflect()
    return con, meta

con, meta = connect('dbuser', 'SecureDB', 'websearchengine')



class Location(Resource):
    location_args = {"name": fields.Str(required=True), "limit": fields.Int(missing=10)}

    @use_args(location_args, location="query")
    def get(self, args):
        statement = f"""SELECT DISTINCT name, LEVENSHTEIN(LEFT(name,{len(args["name"])}),'{args["name"]}') 
            FROM location
            ORDER BY LEVENSHTEIN(LEFT(name,{len(args["name"])}),'{args["name"]}')
            LIMIT '{args["limit"]}';
            """  
        response = con.execute(statement)
        recomendation = [ x[0] for x in response ]
        if recomendation:
            return recomendation, 200
        return "Bad Request", 400
    
api.add_resource(Location, "/api/v1/location")

class PoliceReport(Resource):
    policereport_args = {"location": fields.Str(required=True),"page":fields.Int(missing=1),
                         "pageSize":fields.Int(missing=12),"getTotalCount": fields.Bool()}
    
    @use_args(policereport_args, location="query")
    def get(self, args):
        statement = """
            SELECT pol.url, pol.title,pol.header,loc.locations, pol.id, pol.district{countProjection} FROM policereport as pol, 
                (SELECT policereport_id, json_agg(name) as locations{count}
                FROM location as loc, 
                    (SELECT policereport_id as prid 
                    FROM location 
                    WHERE name='{location}') as sample 
                WHERE policereport_id=prid
                GROUP BY policereport_id 
                ORDER BY policereport_id 
                OFFSET {offset} 
                LIMIT {pageSize}) as loc 
            WHERE pol.id = loc.policereport_id;
            """.format(count=", COUNT(*) OVER() AS count" if args["getTotalCount"] else "",
                       countProjection=", loc.count" if args["getTotalCount"] else "",
                       location=args["location"], pageSize=args["pageSize"], offset=((args["page"]-1)*args["pageSize"]) )
        sqlResult = con.execute(statement)
        data = list(sqlResult)
        
        response = {
            "policeReports": [ {"url":row[0], "title": row[1], "header": row[2],
                        "locations": row[3], "id": row[4], "district": row[5]} for row in data ]
        }
        
        if args["getTotalCount"]:
            response["totalCount"] = data[0][6]
                
        if response["policeReports"]:
            return response, 200
        return "Bad Request", 400

api.add_resource(PoliceReport, "/api/v1/policereports")

class RelevantSentences(Resource):
    relevant_args = {"policereport": fields.Int(required=True)}
    
    @use_args(relevant_args, location="query")
    def get(self, args):
        statement = f"""SELECT sentence FROM relevant WHERE policereport_id={args['policereport']};"""
        response = con.execute(statement)
        relevantSentences = [ row[0] for row in response  ]
        if relevantSentences:
            return relevantSentences, 200
        return "Bad Request", 400

api.add_resource(RelevantSentences, "/api/v1/relevantsentences")


app.run()

