from flask import redirect, render_template, url_for, flash, request, session, current_app
from loja import db, app



@app.route('/addCart', methods=['POST'])
def AddCart():
    try:
        pass
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)