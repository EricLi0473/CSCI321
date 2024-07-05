from Entity.comment import *
class CommentController:
    def __init__(self):
        pass

    def get_comments_by_symbol(self,symbol):
        # todo add filter high like comments features
        return Comment().get_comments_by_symbol(symbol)

    def insert_comment(self,accountId,symbol,comment):
        Comment().insert_comment(accountId,symbol,comment)

    def delete_comment_by_id(self,commentId):
        Comment().delete_comment_by_id(commentId)

if __name__ == '__main__':
    print(CommentController().get_comments_by_symbol('AAPl'))