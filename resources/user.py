from db import  db
from passlib.hash import pbkdf2_sha256
from flask_smorest import Blueprint,abort
from models import UserModel
from schemas import UserSchema
from flask.views import MethodView
from flask_jwt_extended import create_access_token


blp=Blueprint("User","user",description="operation on users")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self,user_data):
        if UserModel.query.filter(UserModel.username==user_data["username"]).first():
            abort(404,message="username ia already exists")
        
        user=UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )
        db.session.add(user)
        db.session.commit()
        return {"message":"user succesfully registered"}
    


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self,user_data):
        user=UserModel.query.filter(UserModel.username==user_data["username"]).first()
        if user and pbkdf2_sha256.verify(user_data["password"],user.password):
            access_token=create_access_token(identity=user.id)
            return{"token":access_token}
        abort(404,message="invalid credentials")

@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200,UserSchema)
    def get(self,user_id):
        user=UserModel.query.get_or_404(user_id)
        return user
    
    def delete(self,user_id):
        user=UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return{"message":"user has been deleted"}