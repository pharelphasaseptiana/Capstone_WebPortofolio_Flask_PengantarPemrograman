import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from config import Config
from models import db, User, Profile, Skill, Project, Message

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Silakan login terlebih dahulu.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# --- PUBLIC ROUTES ---
@app.route('/')
def index():
    profile = Profile.query.first()
    projects = Project.query.order_by(Project.created_at.desc()).limit(3).all()
    return render_template('index.html', profile=profile, projects=projects)

@app.route('/about')
def about():
    profile = Profile.query.first()
    skills = Skill.query.all()
    return render_template('about.html', profile=profile, skills=skills)

@app.route('/portfolio')
def portfolio():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('portfolio.html', projects=projects)

@app.route('/project/<int:id>')
def project_detail(id):
    project = Project.query.get_or_404(id)
    return render_template('project_detail.html', project=project)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    profile = Profile.query.first()
    if request.method == 'POST':
        name, email, message = request.form.get('name'), request.form.get('email'), request.form.get('message')
        if name and email and message:
            db.session.add(Message(name=name, email=email, message=message))
            db.session.commit()
            flash('Pesan berhasil dikirim!', 'success')
            return redirect(url_for('contact'))
        flash('Semua field wajib diisi.', 'danger')
    return render_template('contact.html', profile=profile)

# --- AUTH ROUTES ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and user.check_password(request.form.get('password')):
            session['user'] = user.username
            flash('Login berhasil!', 'success')
            return redirect(url_for('dashboard'))
        flash('Username atau password salah.', 'danger')
    return render_template('dashboard/login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Anda telah logout.', 'info')
    return redirect(url_for('index'))

# --- DASHBOARD ROUTES ---
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard/index.html', 
                           total_projects=Project.query.count(), 
                           unread_messages=Message.query.filter_by(is_read=False).count())

@app.route('/dashboard/projects')
@login_required
def dashboard_projects():
    return render_template('dashboard/projects.html', projects=Project.query.order_by(Project.created_at.desc()).all())

@app.route('/dashboard/projects/add', methods=['GET', 'POST'])
@login_required
def add_project():
    if request.method == 'POST':
        file = request.files.get('image')
        img_name = 'default.jpg'
        if file and allowed_file(file.filename):
            img_name = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], img_name))
        
        db.session.add(Project(
            title=request.form.get('title'), description=request.form.get('description'),
            technologies=request.form.get('technologies'), image_file=img_name,
            github_link=request.form.get('github_link'), live_link=request.form.get('live_link')
        ))
        db.session.commit()
        flash('Proyek berhasil ditambahkan!', 'success')
        return redirect(url_for('dashboard_projects'))
    return render_template('dashboard/add_project.html')

@app.route('/dashboard/projects/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    project = Project.query.get_or_404(id)
    if request.method == 'POST':
        project.title, project.description, project.technologies = request.form.get('title'), request.form.get('description'), request.form.get('technologies')
        project.github_link, project.live_link = request.form.get('github_link'), request.form.get('live_link')
        
        file = request.files.get('image')
        if file and allowed_file(file.filename):
            if project.image_file != 'default.jpg':
                old_path = os.path.join(app.config['UPLOAD_FOLDER'], project.image_file)
                if os.path.exists(old_path): os.remove(old_path)
            project.image_file = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], project.image_file))
        db.session.commit()
        flash('Proyek berhasil diperbarui!', 'success')
        return redirect(url_for('dashboard_projects'))
    return render_template('dashboard/edit_project.html', project=project)

@app.route('/dashboard/projects/delete/<int:id>', methods=['POST'])
@login_required
def delete_project(id):
    project = Project.query.get_or_404(id)
    if project.image_file != 'default.jpg':
        fpath = os.path.join(app.config['UPLOAD_FOLDER'], project.image_file)
        if os.path.exists(fpath): os.remove(fpath)
    db.session.delete(project)
    db.session.commit()
    flash('Proyek berhasil dihapus!', 'success')
    return redirect(url_for('dashboard_projects'))

@app.route('/dashboard/profile', methods=['GET', 'POST'])
@login_required
def dashboard_profile():
    profile = Profile.query.first() or Profile(name='Nama Anda', headline='Web Developer')
    if not Profile.query.first(): db.session.add(profile); db.session.commit()
    
    if request.method == 'POST':
        profile.name, profile.headline, profile.about = request.form.get('name'), request.form.get('headline'), request.form.get('about')
        profile.education = request.form.get('education')
        profile.email, profile.github_link = request.form.get('email'), request.form.get('github_link')
        profile.linkedin_link = request.form.get('linkedin_link')
        
        Skill.query.delete()
        for s in request.form.get('skills', '').split(','):
            if s.strip(): db.session.add(Skill(name=s.strip()))
            
        file = request.files.get('photo')
        if file and allowed_file(file.filename):
            if profile.photo_file != 'default-profile.jpg':
                old_path = os.path.join(app.config['UPLOAD_FOLDER'], profile.photo_file)
                if os.path.exists(old_path): os.remove(old_path)
            profile.photo_file = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], profile.photo_file))
        db.session.commit()
        flash('Profil berhasil diperbarui!', 'success')
        return redirect(url_for('dashboard_profile'))
        
    return render_template('dashboard/profile.html', profile=profile, skills_str=', '.join([s.name for s in Skill.query.all()]))

@app.route('/dashboard/messages')
@login_required
def dashboard_messages():
    return render_template('dashboard/messages.html', messages=Message.query.order_by(Message.created_at.desc()).all())

@app.route('/dashboard/messages/read/<int:id>')
@login_required
def mark_read(id):
    msg = Message.query.get_or_404(id)
    msg.is_read = True
    db.session.commit()
    return redirect(url_for('dashboard_messages'))

@app.route('/dashboard/messages/delete/<int:id>', methods=['POST'])
@login_required
def delete_message(id):
    db.session.delete(Message.query.get_or_404(id))
    db.session.commit()
    flash('Pesan berhasil dihapus.', 'success')
    return redirect(url_for('dashboard_messages'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print('[INFO] Akun default dibuat: admin / admin123')
    app.run(debug=True)
