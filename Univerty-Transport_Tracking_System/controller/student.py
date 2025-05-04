from werkzeug.utils import secure_filename
import os

class StudentInfoManager:
    """Handles student information operations"""
    def __init__(self, db_manager, upload_folder):
        self.db = db_manager
        self.upload_folder = upload_folder

    def get_student_info(self, user_id):
        """Get student info by user ID"""
        query = 'SELECT * FROM student_info WHERE user_id = %s'
        return self.db.execute_query(query, (user_id,), fetch_one=True)

    def update_student_info(self, user_id, data, picture_file):
        """Update or create student info"""
        # Handle picture upload
        picture_url = None
        if picture_file:
            filename = secure_filename(picture_file.filename)
            picture_path = os.path.join(self.upload_folder, filename)
            picture_file.save(picture_path)
            picture_url = f'static/uploads/{filename}'

        # Check if record exists
        existing_info = self.get_student_info(user_id)

        if existing_info:
            # Update existing record
            query = '''
                UPDATE student_info
                SET full_name = %s, department_name = %s, class_name = %s,
                    roll_number = %s, cnic = %s, phone = %s,
                    email = %s, city = %s, picture = %s
                WHERE user_id = %s
            '''
            params = (*data.values(), picture_url, user_id)
        else:
            # Create new record
            query = '''
                INSERT INTO student_info
                (user_id, full_name, department_name, class_name, roll_number,
                 cnic, phone, email, city, picture)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            params = (user_id, *data.values(), picture_url)

        self.db.execute_query(query, params, fetch_all=False)