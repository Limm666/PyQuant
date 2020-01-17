# -*- coding:utf-8 -*- 
# author: limm_666

def test(*args, **kwargs):
    print(args)
    print(kwargs)
    print(kwargs["11"])


test("sss", "ssss", **{"11": "1222", "222": "333"})
