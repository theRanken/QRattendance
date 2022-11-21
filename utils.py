from flask import session, flash
from flask import  redirect, url_for as url
from typing import Callable
import functools

def list_contains(list_a:list, list_b:list)->bool:
    l1 = set(list_a)
    l2 = set(list_b)

    if l1.intersection(l2):
        return True
    else:
        return False

def auth_required(f:Callable)->Callable:
    @functools.wraps(f)
    def  wrapper(*args, **kwargs):
        if not ('authenticated' and 'id' and 'username') in session:
            session.clear()
            flash("User Session Has Expired or Does Not Exist")
            return redirect(url("login"))
        else:
            return f(*args, **kwargs)
    return wrapper