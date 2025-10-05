def commit(func):
    def wrapper(self, *args, **kwargs):
        flag = True
        if "commit_transaction" in kwargs:
            flag = kwargs["commit_transaction"]
            kwargs.pop("commit_transaction")
        res = func(self, *args, **kwargs)
        if flag:
            self.db.commit()
        # self.db.refresh(res)
        return res

    return wrapper


