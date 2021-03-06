from flask import Flask, render_template, g, request

from portal.auth import login_required


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DB_NAME='portal',
        DB_USER='portal_user',
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)
    app.add_url_rule('/', endpoint='index')

    from . import sessions
    app.register_blueprint(sessions.bp)

    @app.route('/home')
    @login_required
    def home():
        return render_template('home.html', user=g.user[1])

    from . import my_courses
    app.register_blueprint(my_courses.bp)

    from . import courses
    app.register_blueprint(courses.bp)

    from . import assignments
    app.register_blueprint(assignments.bp)

    from . import add_grades
    app.register_blueprint(add_grades.bp)
    
    from . import my_assignments
    app.register_blueprint(my_assignments.bp)

    from . import teacher_gradebook
    app.register_blueprint(teacher_gradebook.bp)

    #This is code in order for students to be able to view a list of their assignments.


    return app
