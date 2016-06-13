import time

def timer(function_to_decorate):
        def tmp(*args, **kwargs):
            t_begin = time.time()
            res = function_to_decorate(*args, **kwargs)
            t_end = time.time()
            print("Time of function's implementation: %f" % (t_end - t_begin))
            return res
        return tmp