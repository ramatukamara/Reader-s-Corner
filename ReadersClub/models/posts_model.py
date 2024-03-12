from ReadersClub.config.mysqlconnections import connectToMySQL
from ReadersClub.models.users_model import User

class Post:
    def __init__(self, data):
        self.id = data['id']
        self.comment = data['comment']
        self.book_club = data['book_club']
        self.date_of_post = data['date_of_post']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.comments = []  
        self.likes = []    

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM posts JOIN users ON users.id = posts.user_id"
        results = connectToMySQL("readerscorner_db").query_db(query)
        posts = []
        for row in results:
            posts.append(cls(row))
        return posts

    def get_comments(self):
        query = "SELECT * FROM comments WHERE post_id = %(post_id)s"
        data = {'post_id': self.id}
        results = connectToMySQL("readerscorner_db").query_db(query, data)
        for row in results:
            self.comments.append(Comment(row))
        return self.comments

    def get_likes(self):
        query = "SELECT * FROM likes WHERE post_id = %(post_id)s"
        data = {'post_id': self.id}
        results = connectToMySQL("readerscorner_db").query_db(query, data)
        for row in results:
            self.likes.append(Like(row))
        return self.likes
    
    @classmethod
    def get_by_id(cls, id):
        query = "SELECT * FROM posts WHERE id = %(id)s;"
        result = connectToMySQL("readerscorner_db").query_db(query, {'id': id})
        if result:
            return cls(result[0])
        return None

    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO posts (comment, book_club, user_id)
            VALUES (%(comment)s, %(book_club)s, %(user_id)s);
        """
        return connectToMySQL("readerscorner_db").query_db(query, data)

    @classmethod
    def update(cls, data):
        query = """
            UPDATE posts
            SET comment = %(comment)s, book_club = %(book_club)s
            WHERE id = %(id)s;
        """
        return connectToMySQL("readerscorner_db").query_db(query, data)

    @classmethod
    def delete(cls, id):
        query = "DELETE FROM posts WHERE id = %(id)s;"
        return connectToMySQL("readerscorner_db").query_db(query, {'id': id})


# =============================== Class method for comments and likes on posts
    
class Comment:
    def __init__(self, data):
        self.id = data['id']
        self.comment_text = data['comment_text']
        self.user_id = data['user_id']
        self.post_id = data['post_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

class Like:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.post_id = data['post_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']