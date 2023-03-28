from functools import wraps
import pickle


def buffer(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        cur_state = pickle.dumps(self.__dict__)
        result = f(self, *args, **kwargs)
        self.__dict__ = pickle.loads(cur_state)
        return result
    return wrapper