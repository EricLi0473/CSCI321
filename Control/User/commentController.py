from Entity.comment import *
class CommentController:
    def __init__(self):
        pass

    def get_comments_by_symbol(self,symbol):
        return Comment().get_comments_by_symbol(symbol)

    def insert_comment(self,accountId,symbol,comment):
        Comment().insert_comment(accountId,symbol,comment)

    def delete_comment_by_id(self,commentId):
        Comment().delete_comment_by_id(commentId)