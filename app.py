from flask import Flask,jsonify
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
# from sqlalchemy import UniqueConstrain
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
db = SQLAlchemy(app)
api = Api(app)
class Task(db.Model):
    id =db.Column(db.Integer , primary_key=True,autoincrement=True)
    title =db.Column(db.String, nullable = False)
    des =db.Column(db.String, nullable = False)
    due_date = db.Column(db.DateTime)
    status = db.Column(db.String, nullable = False)

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, help='Title')
parser.add_argument('description', type=str, help='Description')
parser.add_argument('duedate', help='Description')
parser.add_argument('status', type=str, help='Status')
statuses = [ "Incomplete", "In Progress",  "Completed"]

@app.errorhandler(404)
def handle_not_found_error(error):
    return {'message': 'Resource not found'}, 404

# Custom error handler for 500 Internal Server Error
@app.errorhandler(500)
def handle_internal_server_error(error):
    return {'message': 'Internal server error'}, 500


class Api_directors(Resource):
    def get(self):
        all_task= []
        tasks = Task.query.all()
        for t in tasks:
            j = {}
            dates =t.due_date.strftime("%Y-%m-%d")
            j["id"] = t.id
            j['title'] = t.title
            j['description'] =t.des
            j['due_date'] = dates
            j['status'] = t.status
            all_task.append(j)
        return all_task
    def post(self):
        args = parser.parse_args()
        # Implement the logic to create a new row using the provided data
        # Example: Save the data to a database
        if args['status']  in statuses:
        

            date_string = args['duedate']
            date_format = '%Y-%m-%d'

            date_object = datetime.strptime(date_string, date_format).date()
            new_row = Task(title=args['title'], des=args['description'],due_date=date_object,status=args['status'])
            db.session.add(new_row)
            db.session.commit()
            return {"Message":"successfully added"}
        else:
            return {"Messge":"Give valid status"}
        

class Api_directors2(Resource):
    def get(self,id):
       
        task = Task.query.get(id)
        if task:
            dates =task.due_date.strftime("%Y-%m-%d")
            print(dates)
            return {
                    'id': task.id,
                    'title': task.title,
                    'description': task.des,
                    'due_date': dates,
                    'status':task.status
                }
        else:
            return{"Message":"Task not found"}
    def patch(self, id):
        
        resource = Task.query.get(id)
        args = parser.parse_args()
       
        if resource:
                
            
              
                if args["title"]:
                    resource.title = args["title"]
                if args["description"]:
                    resource.des =args["description"]
                if args['duedate']:
                    date_string = args['duedate']
                    date_format = '%Y-%m-%d'

                    date_object = datetime.strptime(date_string, date_format).date()
                    resource.due_date=date_object
                if args['status']:
                    if args['status'] in statuses:
                        resource.status  = args["status"] 
                    else:
                        return{"Message ":"Return valid status"}
                db.session.commit()
                return{"message":"Updated"}  
        else:
            return{"Messsage":"No such row"}         
             
           
    def delete(self,id):
        row_to_delete = Task.query.filter_by(id=id).first() 
        if row_to_delete:
            db.session.delete(row_to_delete)
            db.session.commit()  
            return{"Message ":"successfully deleted"}
        else:
            return{"Message":"Task not found"}


       

        
        
    

    
api.add_resource(Api_directors,'/api/tasks')
api.add_resource(Api_directors2,'/api/tasks/<int:id>')

if __name__ == '__main__':
  # Run the Flask app
  app.run(host='0.0.0.0',port=8080)