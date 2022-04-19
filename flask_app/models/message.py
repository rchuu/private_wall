from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime
import math


class Message:
    db = "private_wall"

    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.sender_id = data['sender_id']
        self.sender = data['sender']
        self.receiver = data['receiver_id']
        self.receiver = data['receiver']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def time_span(self):
        now = datetime.now()
        delta = now - self.created_at
        print(delta.days)
        print(delta.total_seconds())
        if delta.days > 0:
            return f"{delta.days} days ago"
        elif (math.floor(delta.total_seconds() / 60)) >= 60:
            return f"{math.floor(math.floor(delta.total_seconds() / 60)/60)} hours ago"
        elif delta.total_seconds() >= 60:
            return f"{math.floor(delta.total_seconds() / 60)} minutes ago"
        else:
            return f"{math.floor(delta.total_seconds())} seconds ago"

    @classmethod
    def get_user_messages(cls, data):
        query = "SELECT users.first_name as sender, users2.first_name as receiver, messages.* FROM users LEFT JOIN messages ON users.id = messages.sender_id LEFT JOIN users as users2 ON users2.id = messages.receiver_id WHERE users2.id =  %(id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        messages = []
        for message in results:
            messages.append(cls(message))
        return messages

    @classmethod
    def get_user_messages(cls, data):
        query = "SELECT users.first_name as sender, users2.first_name as receiver, messages.* FROM users LEFT JOIN messages ON users.id = messages.sender_id LEFT JOIN users as users2 ON users2.id = messages.receiver_id WHERE users2.id =  %(id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        messages = []
        for message in results:
            messages.append(cls(message))
        return messages

    @classmethod
    def save(cls, data):
        query = "INSERT INTO messages (content,sender_id,receiver_id) VALUES (%(content)s,%(sender_id)s,%(receiver_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_from_id(cls, data):
        query = """SELECT * 
        FROM messages as sender
        LEFT JOIN messages
        ON sender.id = messages.sender_id
        LEFT JOIN users as receiver"""
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM messages WHERE messages.id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_message(message):
        is_valid = True
        query = "SELECT * FROM messages WHERE message = %(message)s;"
        results = connectToMySQL(Message.db).query_db(query, message)
        if len(results) >= 1:
            flash("Message taken!", "message")
            is_valid = False
        if len(results['message']) < 2:
            flash("TOO SHORT", "message")
            is_valid = False
        return is_valid
