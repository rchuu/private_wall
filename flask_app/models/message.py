from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL


class Message:
    db = "private_wall"

    def __init__(self, data):
        self.id = data['id']
        self.message = data['message']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM messages;"
        results = connectToMySQL(cls.db).query_db(query)
        messages = []
        for row in results:
            messages.append(cls(row))
        return messages

    @classmethod
    def save(cls, data):
        query = """INSERT INTO messages (message)
        VALUES (%(messages)s;"""
        return connectToMySQL(cls.db).query_db(query, data)

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
