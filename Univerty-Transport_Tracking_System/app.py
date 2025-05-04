from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from config import Config
from controller.database import DatabaseManager
from controller.user import UserManager
from controller.bus import BusManager
from controller.notification import NotificationManager
from controller.student import StudentInfoManager
from controller.route import RouteManager
from controller.feedback import FeedbackManager
from controller.schedule import ScheduleManager


class UTTSApplication:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config.from_object(Config)

        # Initialize all managers
        self.db_manager = DatabaseManager(Config.DB_CONFIG)
        self.user_manager = UserManager(self.db_manager)
        self.bus_manager = BusManager(self.db_manager)
        self.notification_manager = NotificationManager(self.db_manager)
        self.student_info_manager = StudentInfoManager(self.db_manager, Config.UPLOAD_FOLDER)
        self.route_manager = RouteManager(self.db_manager)
        self.feedback_manager = FeedbackManager(self.db_manager)
        self.schedule_manager = ScheduleManager(self.db_manager)

        self.setup_routes()

    def setup_routes(self):
        # Login/Signup Routes
        @self.app.route('/login', methods=['GET', 'POST'])
        def login():
            if request.method == 'POST':
                user = self.user_manager.authenticate(request.form['username'], request.form['password'])
                if user:
                    session['username'] = user['username']
                    session['user_id'] = user['id']
                    flash("Login success", "success")
                    return redirect(url_for('home'))
                flash("Invalid username or password", "error")
            return render_template('login.html')

        @self.app.route('/signup', methods=['GET', 'POST'])
        def signup():
            if request.method == 'POST':
                if request.form['password'] != request.form['confirm-password']:
                    flash('Passwords do not match', 'error')
                else:
                    if self.user_manager.create_user(request.form['username'], request.form['email'],
                                                     request.form['password']):
                        flash('Signup successful! Please login.', 'success')
                        return redirect(url_for('login'))
                    flash('Username or email already exists', 'error')
            return render_template('signup.html')

        @self.app.route('/logout')
        def logout():
            session.clear()
            return redirect(url_for('login'))

        # Main User Routes
        @self.app.route('/')
        def home():
            if 'username' not in session:
                return redirect(url_for('login'))

            return render_template(
                'dashboard.html',
                user=session['username'],
                buses=self.bus_manager.get_all_buses(),
                student_info=self.student_info_manager.get_student_info(session['user_id']),
                notifications=self.notification_manager.get_recent_notifications()
            )

        @self.app.route('/profile')
        def profile():
            if 'user_id' not in session:
                return redirect(url_for('login'))
            return render_template('student_info.html',
                                   student_info=self.student_info_manager.get_student_info(session['user_id']))

        @self.app.route('/settings', methods=['GET', 'POST'])
        def settings():
            if 'user_id' not in session:
                return redirect(url_for('login'))

            if request.method == 'POST':
                self.student_info_manager.update_student_info(
                    session['user_id'],
                    {
                        'full_name': request.form['full_name'],
                        'department_name': request.form['department_name'],
                        'class_name': request.form['class_name'],
                        'roll_number': request.form['roll_number'],
                        'cnic': request.form['cnic'],
                        'phone': request.form['phone'],
                        'email': request.form['email'],
                        'city': request.form['city']
                    },
                    request.files['picture']
                )
                flash('Information updated!', 'success')
                return redirect(url_for('profile'))

            return render_template('update_student_info.html',
                                   student_info=self.student_info_manager.get_student_info(session['user_id']))

        # Utility Routes
        @self.app.route('/map')
        def map():
            return render_template('map.html', **self.bus_manager.get_map_stats())

        @self.app.route('/schedule')
        def schedule():
            return render_template('schedule.html', bus_schedules=self.schedule_manager.get_all_schedules(),
                                   datetime=datetime)

        @self.app.route('/contact')
        def contact():
            return render_template('contact.html')

        @self.app.route('/submit_feedback', methods=['POST'])
        def submit_feedback():
            if self.feedback_manager.create_feedback(request.form['name'], request.form['email'],
                                                     request.form['message']):
                flash('Thank you for your feedback!', 'success')
            else:
                flash('Error submitting feedback', 'error')
            return redirect(url_for('home'))

        # Admin Route
        @self.app.route('/admin')
        def admin():
            if 'username' not in session:
                return redirect(url_for('login'))

            return render_template(
                'admin.html',
                stats=self.user_manager.get_admin_stats(),
                users=self.user_manager.get_all_users(),
                buses=self.bus_manager.get_all_buses(),
                routes=self.route_manager.get_all_routes(),
                notifications=self.notification_manager.get_recent_notifications(),
                feedbacks=self.feedback_manager.get_all_feedbacks(),
                schedules=self.schedule_manager.get_all_schedules()
            )

    def run(self):
        self.app.run(debug=True, host='0.0.0.0')


if __name__ == '__main__':
    app = UTTSApplication()
    app.run()