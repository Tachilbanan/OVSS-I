from flask import Blueprint, request, render_template
from sqlalchemy import func
from videoonline.models import db, User, Video, Classify, videos_classifys

root_view = Blueprint("/", __name__)

@root_view.route('/')
@root_view.route('<int:page>')
def home(page = 1):
    """View function for home page"""

    videos = Video.query.order_by(
        Video.publish_date.desc()
    ).paginate(page, 10)

    recent, top_classifys = sidebar_data()

    return render_template('home.html',
                           videos = videos,
                           recent = recent,
                           top_classifys = top_classifys)

@root_view.route('/video/<string:video_id>')
def video(video_id):
    """View function for post page"""

    video = db.session.query(Video).get_or_404(video_id)
    classifys = video.classifys
    recent, top_classifys = sidebar_data()

    return render_template('post.html',
                           video = video,
                           classify = classifys,
                           recent = recent,
                           top_classifys = top_classifys)

@root_view.route('/classify/<string:classify_name>')
def classify(classify_name):
    """View function for classify page"""

    classifys = db.session.query(Classify).filter_by(name = classify_name).first_or_404()
    videos = classifys.videos.order_by(Video.publish_date.desc()).all()
    recent, top_classifys = sidebar_data()

    return render_template('classify.html',
                           classifys = classifys,
                           videos = videos,
                           recent = recent,
                           top_classifys = top_classifys)

# 侧边栏数据
def sidebar_data():
    """Set the sidebar function."""

    # Get Video of recent
    recent = db.session.query(Video).order_by(
            Video.publish_date.desc()
        ).limit(5).all()

    # 获取分类
    top_classifys = db.session.query(Classify).all()
    return recent, top_classifys
